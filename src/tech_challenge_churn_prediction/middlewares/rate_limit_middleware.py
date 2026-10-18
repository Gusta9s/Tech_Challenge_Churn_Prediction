from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from tech_challenge_churn_prediction.schemas.error_response import (
    ErrorResponse,
)
from tech_challenge_churn_prediction.services.rate_limiter_service import (
    RateLimiterService,
)

IDENTIFICADOR_CLIENTE_DESCONHECIDO = "desconhecido"


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Aplica rate limiting por endereco IP a todas as requisicoes HTTP.

    O ASGI nao distingue HTTP de HTTPS no tipo de escopo da requisicao
    (TLS e tratado de forma transparente pelo servidor): o filtro por
    `scope["type"] == "http"` cobre ambos igualmente, excluindo apenas
    conexoes websocket/lifespan. O limite e aplicado de forma universal
    a todos os endpoints, que compartilham a mesma contagem por cliente.
    """

    def __init__(
        self,
        app,
        rate_limiter_service: RateLimiterService,
        cabecalho_requisicoes_restantes: str,
    ) -> None:
        """Armazena o servico de rate limiting e o cabecalho de resposta.

        Parameters
        ----------
        app : starlette.types.ASGIApp
            Aplicacao ASGI envolvida por este middleware.
        rate_limiter_service : RateLimiterService
            Servico que mantem o historico de requisicoes por cliente.
        cabecalho_requisicoes_restantes : str
            Nome do cabecalho HTTP usado para informar quantas
            requisicoes ainda restam na janela atual.
        """
        super().__init__(app)
        self._rate_limiter_service = rate_limiter_service
        self._cabecalho_requisicoes_restantes = cabecalho_requisicoes_restantes

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Bloqueia ou encaminha a requisicao conforme o limite do cliente.

        Parameters
        ----------
        request : starlette.requests.Request
            Requisicao HTTP recebida.
        call_next : RequestResponseEndpoint
            Proxima etapa da cadeia de middlewares/endpoint.

        Returns
        -------
        starlette.responses.Response
            Resposta 429 (JSON, sem processar a requisicao original) se
            o limite foi excedido, ou a resposta normal do endpoint com
            o cabecalho de requisicoes restantes.
        """
        if request.scope["type"] != "http":
            return await call_next(request)

        identificador_cliente = (
            request.client.host
            if request.client
            else IDENTIFICADOR_CLIENTE_DESCONHECIDO
        )
        permitido, requisicoes_restantes = (
            await self._rate_limiter_service.registrar_requisicao(
                identificador_cliente
            )
        )

        if not permitido:
            return self._criar_resposta_limite_excedido()

        resposta = await call_next(request)
        resposta.headers[self._cabecalho_requisicoes_restantes] = str(
            requisicoes_restantes
        )
        return resposta

    def _criar_resposta_limite_excedido(self) -> JSONResponse:
        """Monta a resposta 429 padronizada de limite de requisicoes excedido.

        Returns
        -------
        starlette.responses.JSONResponse
            Resposta 429 no formato {level, message, erro, cause}, com
            o cabecalho de requisicoes restantes zerado.
        """
        corpo = ErrorResponse(
            level="WARNING",
            message="Limite de requisicoes por minuto ultrapassado.",
            erro="LIMITE_DE_REQUISICOES_EXCEDIDO",
        )
        resposta = JSONResponse(status_code=429, content=corpo.model_dump())
        resposta.headers[self._cabecalho_requisicoes_restantes] = "0"
        return resposta

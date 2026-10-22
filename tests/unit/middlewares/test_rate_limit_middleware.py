import asyncio
from dataclasses import dataclass, field

from fastapi import FastAPI
from fastapi.testclient import TestClient

from tech_challenge_churn_prediction.middlewares.rate_limit_middleware import (
    RateLimitMiddleware,
)
from tech_challenge_churn_prediction.services.rate_limiter_service import (
    RateLimiterService,
)

CABECALHO_REQUISICOES_RESTANTES_FICTICIO = "X-Teste-Restantes"
JANELA_EM_SEGUNDOS_FICTICIA = 45


def _criar_client(limite_requisicoes: int) -> TestClient:
    app = FastAPI()

    @app.get("/exemplo")
    def endpoint_exemplo():
        return {"ok": True}

    @app.get("/outro-endpoint")
    def outro_endpoint():
        return {"ok": True}

    rate_limiter_service = RateLimiterService(
        limite_requisicoes=limite_requisicoes,
        janela_em_segundos=JANELA_EM_SEGUNDOS_FICTICIA,
    )
    app.add_middleware(
        RateLimitMiddleware,
        rate_limiter_service=rate_limiter_service,
        cabecalho_requisicoes_restantes=(
            CABECALHO_REQUISICOES_RESTANTES_FICTICIO
        ),
    )
    return TestClient(app)


def test_requisicao_dentro_do_limite_retorna_200_com_cabecalho():
    """Requisicao dentro do limite retorna 200 com cabecalho."""
    client = _criar_client(limite_requisicoes=2)

    resposta = client.get("/exemplo")

    assert resposta.status_code == 200
    assert resposta.headers[CABECALHO_REQUISICOES_RESTANTES_FICTICIO] == "1"


def test_requisicao_acima_do_limite_retorna_429_sem_processar(caplog):
    """Requisicao acima do limite retorna 429 sem processar."""
    client = _criar_client(limite_requisicoes=1)

    client.get("/exemplo")
    resposta = client.get("/exemplo")

    assert resposta.status_code == 429
    assert resposta.headers[CABECALHO_REQUISICOES_RESTANTES_FICTICIO] == "0"
    corpo = resposta.json()
    assert corpo["erro"] == "LIMITE_DE_REQUISICOES_EXCEDIDO"
    assert corpo["level"] == "WARNING"


def test_limite_e_compartilhado_entre_endpoints_diferentes():
    """Limite e compartilhado entre endpoints diferentes."""
    client = _criar_client(limite_requisicoes=2)

    client.get("/exemplo")
    resposta = client.get("/outro-endpoint")

    assert resposta.status_code == 200
    assert resposta.headers[CABECALHO_REQUISICOES_RESTANTES_FICTICIO] == "0"

    resposta_excedente = client.get("/exemplo")

    assert resposta_excedente.status_code == 429


@dataclass
class _RequestFalsoNaoHttp:
    """Dublê minimo de Request, apenas com o atributo `scope` usado pelo
    middleware para decidir se aplica o rate limiting.
    """

    scope: dict = field(default_factory=lambda: {"type": "websocket"})


def test_ignora_rate_limit_para_escopos_nao_http():
    """Ignora rate limit para escopos nao http."""
    rate_limiter_service = RateLimiterService(
        limite_requisicoes=0, janela_em_segundos=JANELA_EM_SEGUNDOS_FICTICIA
    )
    middleware = RateLimitMiddleware(
        app=None,
        rate_limiter_service=rate_limiter_service,
        cabecalho_requisicoes_restantes=(
            CABECALHO_REQUISICOES_RESTANTES_FICTICIO
        ),
    )
    request = _RequestFalsoNaoHttp()
    resposta_esperada = object()

    async def call_next(_request):
        return resposta_esperada

    resposta = asyncio.run(middleware.dispatch(request, call_next))

    assert resposta is resposta_esperada

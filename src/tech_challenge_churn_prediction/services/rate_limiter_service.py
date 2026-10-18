import asyncio
import math
import time
from collections import defaultdict


class RateLimiterService:
    """Controla o limite de requisicoes por cliente em uma janela deslizante.

    Mantem, por cliente, um historico no formato
    `{timestamp_da_requisicao: requisicoes_restantes_no_momento}`. A
    cada nova requisicao, as entradas mais antigas que a janela
    configurada sao removidas antes de avaliar o limite, mantendo o
    historico sempre atualizado com o estado mais recente.

    Nao conhece nada sobre HTTP: recebe um identificador de cliente
    (ex.: endereco IP) e devolve se a requisicao e permitida e quantas
    restam, mantendo baixo acoplamento com a camada de middleware.
    """

    def __init__(
        self, limite_requisicoes: int, janela_em_segundos: float
    ) -> None:
        """Inicializa o limitador com o limite e a janela configurados.

        Parameters
        ----------
        limite_requisicoes : int
            Quantidade maxima de requisicoes permitidas por cliente
            dentro da janela de tempo.
        janela_em_segundos : float
            Duracao, em segundos, da janela deslizante de contagem.
        """
        self._limite_requisicoes = limite_requisicoes
        self._janela_em_segundos = janela_em_segundos
        self._historico_por_cliente: dict[str, dict[float, int]] = defaultdict(
            dict
        )
        self._lock = asyncio.Lock()

    async def registrar_requisicao(
        self, identificador_cliente: str
    ) -> tuple[bool, int]:
        """Registra uma requisicao do cliente e avalia o limite.

        Parameters
        ----------
        identificador_cliente : str
            Identificador unico do cliente (ex.: endereco IP).

        Returns
        -------
        tuple[bool, int]
            Par `(permitido, requisicoes_restantes)`: `permitido` e
            False quando o limite ja foi atingido, e
            `requisicoes_restantes` e a quantidade de requisicoes
            ainda disponiveis dentro da janela atual.
        """
        agora = time.monotonic()
        limite_inferior_da_janela = agora - self._janela_em_segundos

        async with self._lock:
            historico_cliente = self._historico_por_cliente[
                identificador_cliente
            ]
            self._remover_requisicoes_antigas(
                historico_cliente, limite_inferior_da_janela
            )

            if len(historico_cliente) >= self._limite_requisicoes:
                return False, 0

            requisicoes_restantes = self._limite_requisicoes - (
                len(historico_cliente) + 1
            )
            historico_cliente[
                self._gerar_chave_unica(historico_cliente, agora)
            ] = requisicoes_restantes
            return True, requisicoes_restantes

    @staticmethod
    def _gerar_chave_unica(
        historico_cliente: dict[float, int], timestamp: float
    ) -> float:
        """Garante uma chave de timestamp unica, mesmo sob colisao de relogio.

        Parameters
        ----------
        historico_cliente : dict[float, int]
            Historico de requisicoes de um unico cliente.
        timestamp : float
            Timestamp candidato para a nova entrada.

        Returns
        -------
        float
            Timestamp unico, ainda nao usado como chave no historico.
        """
        while timestamp in historico_cliente:
            timestamp = math.nextafter(timestamp, math.inf)
        return timestamp

    @staticmethod
    def _remover_requisicoes_antigas(
        historico_cliente: dict[float, int], limite_inferior_da_janela: float
    ) -> None:
        """Remove do historico as requisicoes fora da janela deslizante.

        Parameters
        ----------
        historico_cliente : dict[float, int]
            Historico de requisicoes de um unico cliente, modificado
            em memoria.
        limite_inferior_da_janela : float
            Timestamp abaixo do qual uma requisicao e considerada
            antiga e deve ser removida.
        """
        timestamps_antigos = [
            timestamp
            for timestamp in historico_cliente
            if timestamp <= limite_inferior_da_janela
        ]
        for timestamp in timestamps_antigos:
            del historico_cliente[timestamp]

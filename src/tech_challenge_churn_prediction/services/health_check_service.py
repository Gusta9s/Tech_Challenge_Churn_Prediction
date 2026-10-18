from tech_challenge_churn_prediction.exceptions.app_exceptions import (
    ModeloNaoDisponivelException,
)
from tech_challenge_churn_prediction.services.model_loader_service import (
    ModelLoaderService,
)


class HealthCheckService:
    """Avalia a saude da aplicacao: liveness e readiness.

    Depende apenas do ModelLoaderService (injetado), sem conhecer nada
    sobre pre-processamento, predicao ou a camada HTTP.
    """

    def __init__(self, model_loader_service: ModelLoaderService) -> None:
        """Armazena o ModelLoaderService usado na verificacao de readiness.

        Parameters
        ----------
        model_loader_service : ModelLoaderService
            Servico responsavel por carregar o modelo campeao.
        """
        self._model_loader_service = model_loader_service

    @staticmethod
    def verificar_liveness() -> bool:
        """Confirma que o processo esta ativo.

        Returns
        -------
        bool
            Sempre True, pois nao ha dependencias externas verificadas.
        """
        return True

    def verificar_readiness(self) -> bool:
        """Confirma que o modelo campeao pode ser carregado.

        Returns
        -------
        bool
            True se o modelo carregar com sucesso.

        Raises
        ------
        ModeloNaoDisponivelException
            Se o modelo nao puder ser carregado.
        """
        try:
            self._model_loader_service.carregar()
        except Exception as erro:
            raise ModeloNaoDisponivelException(cause=erro) from erro
        return True

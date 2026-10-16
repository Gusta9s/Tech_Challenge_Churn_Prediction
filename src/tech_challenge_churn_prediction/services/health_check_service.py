from tech_challenge_churn_prediction.exceptions.app_exceptions import (
    ModeloNaoDisponivelException,
)
from tech_challenge_churn_prediction.services.model_loader_service import (
    ModelLoaderService,
)


class HealthCheckService:
    """Responsavel exclusivamente por avaliar a saude da aplicacao: liveness
    (processo ativo, sem dependencias externas) e readiness (dependencias
    criticas, como o modelo treinado, disponiveis para uso).

    Depende apenas do ModelLoaderService (injetado), sem conhecer nada sobre
    pre-processamento, predicao ou a camada HTTP.
    """

    def __init__(self, model_loader_service: ModelLoaderService) -> None:
        self._model_loader_service = model_loader_service

    @staticmethod
    def verificar_liveness() -> bool:
        return True

    def verificar_readiness(self) -> bool:
        try:
            self._model_loader_service.carregar()
        except Exception as erro:
            raise ModeloNaoDisponivelException(cause=erro) from erro
        return True

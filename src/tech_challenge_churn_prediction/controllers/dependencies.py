"""Fabricas centralizadas de dependencias dos controllers.

Cada servico e construido por uma Factory dedicada, que mantem a
instancia singleton e a entrega pronta para uso. As factories sao
injetadas nos controllers via FastAPI `Depends`, mantendo os
controllers desacoplados da construcao/ciclo de vida dos servicos.
"""

from tech_challenge_churn_prediction.config.logging_config import obter_logger
from tech_challenge_churn_prediction.services.churn_prediction_logging_service import (  # noqa: E501
    ChurnPredictionLoggingService,
)
from tech_challenge_churn_prediction.services.churn_prediction_service import (
    ChurnPredictionService,
)
from tech_challenge_churn_prediction.services.churn_preprocessing_service import (  # noqa: E501
    ChurnPreprocessingService,
)
from tech_challenge_churn_prediction.services.health_check_service import (
    HealthCheckService,
)
from tech_challenge_churn_prediction.services.model_loader_service import (
    ModelLoaderService,
)

NOME_LOGGER_PREDICAO = "tech_challenge_churn_prediction.predict"


class ModelLoaderServiceFactory:
    """Fabrica responsavel pela instancia singleton de ModelLoaderService."""

    _instancia: ModelLoaderService | None = None

    @classmethod
    def criar(cls) -> ModelLoaderService:
        """Cria (ou reutiliza) a instancia singleton de ModelLoaderService.

        Returns
        -------
        ModelLoaderService
            Servico responsavel por carregar o modelo campeao.
        """
        if cls._instancia is None:
            cls._instancia = ModelLoaderService()
        return cls._instancia


class ChurnPreprocessingServiceFactory:
    """Fabrica responsavel pela instancia singleton de
    ChurnPreprocessingService.
    """

    _instancia: ChurnPreprocessingService | None = None

    @classmethod
    def criar(cls) -> ChurnPreprocessingService:
        """Cria (ou reutiliza) o singleton de ChurnPreprocessingService.

        Returns
        -------
        ChurnPreprocessingService
            Servico responsavel por pre-processar o payload de entrada.
        """
        if cls._instancia is None:
            cls._instancia = ChurnPreprocessingService()
        return cls._instancia


class ChurnPredictionServiceFactory:
    """Fabrica responsavel pelo singleton de ChurnPredictionService."""

    _instancia: ChurnPredictionService | None = None

    @classmethod
    def criar(cls) -> ChurnPredictionService:
        """Cria (ou reutiliza) a instancia singleton de ChurnPredictionService.

        Returns
        -------
        ChurnPredictionService
            Servico responsavel por executar a predicao do modelo.
        """
        if cls._instancia is None:
            cls._instancia = ChurnPredictionService()
        return cls._instancia


class HealthCheckServiceFactory:
    """Fabrica responsavel pela instancia singleton de HealthCheckService."""

    _instancia: HealthCheckService | None = None

    @classmethod
    def criar(cls) -> HealthCheckService:
        """Cria (ou reutiliza) a instancia singleton de HealthCheckService.

        Returns
        -------
        HealthCheckService
            Servico responsavel pelas verificacoes de liveness/readiness.
        """
        if cls._instancia is None:
            cls._instancia = HealthCheckService(
                ModelLoaderServiceFactory.criar()
            )
        return cls._instancia


class ChurnPredictionLoggingServiceFactory:
    """Fabrica responsavel pela instancia singleton de
    ChurnPredictionLoggingService.
    """

    _instancia: ChurnPredictionLoggingService | None = None

    @classmethod
    def criar(cls) -> ChurnPredictionLoggingService:
        """Cria (ou reutiliza) a instancia singleton de
        ChurnPredictionLoggingService.

        Returns
        -------
        ChurnPredictionLoggingService
            Servico responsavel por logar o ciclo de vida da predicao.
        """
        if cls._instancia is None:
            cls._instancia = ChurnPredictionLoggingService(
                obter_logger(NOME_LOGGER_PREDICAO)
            )
        return cls._instancia

"""Fabrica centralizada de dependencias dos controllers.

Cada servico e instanciado uma unica vez (singleton via lru_cache) e
injetado nos controllers via FastAPI `Depends`, mantendo os controllers
desacoplados da construcao/ciclo de vida dos servicos.
"""

from functools import lru_cache

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


@lru_cache
def obter_model_loader_service() -> ModelLoaderService:
    """Retorna a instancia singleton de ModelLoaderService.

    Returns
    -------
    ModelLoaderService
        Servico responsavel por carregar o modelo campeao.
    """
    return ModelLoaderService()


@lru_cache
def obter_preprocessing_service() -> ChurnPreprocessingService:
    """Retorna a instancia singleton de ChurnPreprocessingService.

    Returns
    -------
    ChurnPreprocessingService
        Servico responsavel por pre-processar o payload de entrada.
    """
    return ChurnPreprocessingService()


@lru_cache
def obter_prediction_service() -> ChurnPredictionService:
    """Retorna a instancia singleton de ChurnPredictionService.

    Returns
    -------
    ChurnPredictionService
        Servico responsavel por executar a predicao do modelo.
    """
    return ChurnPredictionService()


@lru_cache
def obter_health_check_service() -> HealthCheckService:
    """Retorna a instancia singleton de HealthCheckService.

    Returns
    -------
    HealthCheckService
        Servico responsavel pelas verificacoes de liveness/readiness.
    """
    return HealthCheckService(obter_model_loader_service())


@lru_cache
def obter_prediction_logging_service() -> ChurnPredictionLoggingService:
    """Retorna a instancia singleton de ChurnPredictionLoggingService.

    Returns
    -------
    ChurnPredictionLoggingService
        Servico responsavel por logar o ciclo de vida da predicao.
    """
    return ChurnPredictionLoggingService(
        obter_logger("tech_challenge_churn_prediction.predict")
    )

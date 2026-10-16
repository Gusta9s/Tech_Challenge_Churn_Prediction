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

"""Fabrica centralizada de dependencias dos controllers.

Cada servico e instanciado uma unica vez (singleton via lru_cache) e
injetado nos controllers via FastAPI `Depends`, mantendo os controllers
desacoplados da construcao/ciclo de vida dos servicos.
"""


@lru_cache
def obter_model_loader_service() -> ModelLoaderService:
    return ModelLoaderService()


@lru_cache
def obter_preprocessing_service() -> ChurnPreprocessingService:
    return ChurnPreprocessingService()


@lru_cache
def obter_prediction_service() -> ChurnPredictionService:
    return ChurnPredictionService()


@lru_cache
def obter_health_check_service() -> HealthCheckService:
    return HealthCheckService(obter_model_loader_service())


@lru_cache
def obter_prediction_logging_service() -> ChurnPredictionLoggingService:
    return ChurnPredictionLoggingService(
        obter_logger("tech_challenge_churn_prediction.predict")
    )

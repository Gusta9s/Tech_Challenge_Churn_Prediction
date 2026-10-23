from tech_challenge_churn_prediction.controllers import dependencies as alvo
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


def test_model_loader_service_factory_criar_retorna_singleton():
    """Model loader service factory criar retorna singleton."""
    assert isinstance(
        alvo.ModelLoaderServiceFactory.criar(), ModelLoaderService
    )
    assert (
        alvo.ModelLoaderServiceFactory.criar()
        is alvo.ModelLoaderServiceFactory.criar()
    )


def test_churn_preprocessing_service_factory_criar_retorna_singleton():
    """Churn preprocessing service factory criar retorna singleton."""
    assert isinstance(
        alvo.ChurnPreprocessingServiceFactory.criar(),
        ChurnPreprocessingService,
    )
    assert (
        alvo.ChurnPreprocessingServiceFactory.criar()
        is alvo.ChurnPreprocessingServiceFactory.criar()
    )


def test_churn_prediction_service_factory_criar_retorna_singleton():
    """Churn prediction service factory criar retorna singleton."""
    assert isinstance(
        alvo.ChurnPredictionServiceFactory.criar(), ChurnPredictionService
    )
    assert (
        alvo.ChurnPredictionServiceFactory.criar()
        is alvo.ChurnPredictionServiceFactory.criar()
    )


def test_health_check_service_factory_criar_retorna_singleton():
    """Health check service factory criar retorna singleton."""
    servico = alvo.HealthCheckServiceFactory.criar()

    assert isinstance(servico, HealthCheckService)
    assert servico is alvo.HealthCheckServiceFactory.criar()


def test_churn_prediction_logging_service_factory_criar_retorna_singleton():
    """Churn prediction logging service factory criar retorna singleton."""
    servico = alvo.ChurnPredictionLoggingServiceFactory.criar()

    assert isinstance(servico, ChurnPredictionLoggingService)
    assert servico is alvo.ChurnPredictionLoggingServiceFactory.criar()

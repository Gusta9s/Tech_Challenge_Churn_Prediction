from tech_challenge_churn_prediction.controllers import dependencies as alvo
from tech_challenge_churn_prediction.services.churn_prediction_logging_service import ChurnPredictionLoggingService
from tech_challenge_churn_prediction.services.churn_prediction_service import ChurnPredictionService
from tech_challenge_churn_prediction.services.churn_preprocessing_service import ChurnPreprocessingService
from tech_challenge_churn_prediction.services.health_check_service import HealthCheckService
from tech_challenge_churn_prediction.services.model_loader_service import ModelLoaderService


def test_obter_model_loader_service_retorna_singleton_do_tipo_esperado():
    assert isinstance(alvo.obter_model_loader_service(), ModelLoaderService)
    assert alvo.obter_model_loader_service() is alvo.obter_model_loader_service()


def test_obter_preprocessing_service_retorna_singleton_do_tipo_esperado():
    assert isinstance(alvo.obter_preprocessing_service(), ChurnPreprocessingService)
    assert alvo.obter_preprocessing_service() is alvo.obter_preprocessing_service()


def test_obter_prediction_service_retorna_singleton_do_tipo_esperado():
    assert isinstance(alvo.obter_prediction_service(), ChurnPredictionService)
    assert alvo.obter_prediction_service() is alvo.obter_prediction_service()


def test_obter_health_check_service_retorna_singleton_com_model_loader_injetado():
    servico = alvo.obter_health_check_service()

    assert isinstance(servico, HealthCheckService)
    assert servico is alvo.obter_health_check_service()


def test_obter_prediction_logging_service_retorna_singleton_do_tipo_esperado():
    servico = alvo.obter_prediction_logging_service()

    assert isinstance(servico, ChurnPredictionLoggingService)
    assert servico is alvo.obter_prediction_logging_service()

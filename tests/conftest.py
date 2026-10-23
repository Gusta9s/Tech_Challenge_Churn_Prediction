import pytest

from tech_challenge_churn_prediction.config.app_settings import (
    AppSettingsFactory,
)
from tech_challenge_churn_prediction.config.cors_settings import (
    CorsSettingsFactory,
)
from tech_challenge_churn_prediction.config.logging_settings import (
    LoggingSettingsFactory,
)
from tech_challenge_churn_prediction.config.model_settings import (
    ModelSettingsFactory,
)
from tech_challenge_churn_prediction.config.prediction_settings import (
    PredictionSettingsFactory,
)
from tech_challenge_churn_prediction.config.rate_limit_settings import (
    RateLimitSettingsFactory,
)
from tech_challenge_churn_prediction.config.security_settings import (
    SecuritySettingsFactory,
)
from tech_challenge_churn_prediction.controllers.dependencies import (
    ChurnPredictionLoggingServiceFactory,
    ChurnPredictionServiceFactory,
    ChurnPreprocessingServiceFactory,
    HealthCheckServiceFactory,
    ModelLoaderServiceFactory,
)
from tech_challenge_churn_prediction.schemas.churn_prediction_input import (
    ChurnPredictionInput,
)
from tech_challenge_churn_prediction.services.rate_limiter_service import (
    RateLimiterServiceFactory,
)

FABRICAS_COM_SINGLETON = (
    AppSettingsFactory,
    CorsSettingsFactory,
    LoggingSettingsFactory,
    ModelSettingsFactory,
    PredictionSettingsFactory,
    RateLimitSettingsFactory,
    SecuritySettingsFactory,
    ModelLoaderServiceFactory,
    ChurnPreprocessingServiceFactory,
    ChurnPredictionServiceFactory,
    HealthCheckServiceFactory,
    ChurnPredictionLoggingServiceFactory,
    RateLimiterServiceFactory,
)


@pytest.fixture(autouse=True)
def limpar_caches_de_singletons():
    """Isola os testes entre si limpando os singletons das factories antes
    e depois de cada teste, evitando que o estado de um teste vaze para
    outro.
    """
    for fabrica in FABRICAS_COM_SINGLETON:
        fabrica._instancia = None
    yield
    for fabrica in FABRICAS_COM_SINGLETON:
        fabrica._instancia = None


@pytest.fixture
def payload_valido_dict() -> dict:
    return {
        "cliente_em_idade_avancada": 0,
        "casado": "Yes",
        "meses_como_cliente": 5,
        "possui_servico_telefonico": "Yes",
        "possui_multiplas_linhas": "No",
        "possui_servico_de_internet": "Fiber optic",
        "possui_seguranca_online": "No",
        "possui_backup_online": "No",
        "possui_protecao_dispositivo": "No",
        "possui_suporte_tecnico_premium": "No",
        "possui_streaming_tv_terceiros": "Yes",
        "possui_streaming_filmes_terceiros": "Yes",
        "tipo_contrato": "Month-to-month",
        "fatura_sem_papel": "Yes",
        "metodo_pagamento": "Electronic check",
        "cobranca_mensal": 95.5,
        "total_cobrado_durante_trimestre": 480.75,
    }


@pytest.fixture
def payload_valido(payload_valido_dict: dict) -> ChurnPredictionInput:
    return ChurnPredictionInput(**payload_valido_dict)

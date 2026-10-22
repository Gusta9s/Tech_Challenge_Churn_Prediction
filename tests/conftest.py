import pytest

from tech_challenge_churn_prediction.config import (
    app_settings,
    cors_settings,
    logging_settings,
    model_settings,
    prediction_settings,
    rate_limit_settings,
    security_settings,
)
from tech_challenge_churn_prediction.controllers import dependencies
from tech_challenge_churn_prediction.schemas.churn_prediction_input import (
    ChurnPredictionInput,
)


@pytest.fixture(autouse=True)
def limpar_caches_de_singletons():
    """Isola os testes entre si limpando os singletons via lru_cache antes e
    depois de cada teste, evitando que o estado de um teste vaze para outro.
    """
    getters_com_cache = [
        app_settings.obter_app_settings,
        cors_settings.obter_cors_settings,
        logging_settings.obter_logging_settings,
        model_settings.obter_model_settings,
        prediction_settings.obter_prediction_settings,
        rate_limit_settings.obter_rate_limit_settings,
        security_settings.obter_security_settings,
        dependencies.obter_model_loader_service,
        dependencies.obter_preprocessing_service,
        dependencies.obter_prediction_service,
        dependencies.obter_health_check_service,
        dependencies.obter_prediction_logging_service,
    ]
    for getter in getters_com_cache:
        getter.cache_clear()
    yield
    for getter in getters_com_cache:
        getter.cache_clear()


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

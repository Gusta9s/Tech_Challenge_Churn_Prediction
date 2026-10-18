from tech_challenge_churn_prediction.schemas.churn_prediction_input import (
    ChurnPredictionInput,
)
from tech_challenge_churn_prediction.services.churn_preprocessing_service import (  # noqa: E501
    ChurnPreprocessingService,
)
from tech_challenge_churn_prediction.utils.constantes_modelo import (
    ORDEM_FEATURES_RANDOM_FOREST,
)


def test_transformar_gera_as_colunas_na_ordem_esperada_pelo_modelo(
    payload_valido,
):
    """Transformar gera as colunas na ordem esperada pelo modelo."""
    servico = ChurnPreprocessingService()

    features = servico.transformar(payload_valido)

    assert list(features.columns) == list(ORDEM_FEATURES_RANDOM_FOREST)
    assert features.shape == (1, len(ORDEM_FEATURES_RANDOM_FOREST))


def test_transformar_soma_corretamente_os_addons_contratados(
    payload_valido_dict,
):
    """Transformar soma corretamente os addons contratados."""
    dados = dict(
        payload_valido_dict,
        possui_seguranca_online="No",
        possui_backup_online="No",
        possui_protecao_dispositivo="No",
        possui_suporte_tecnico_premium="No",
        possui_streaming_tv_terceiros="Yes",
        possui_streaming_filmes_terceiros="Yes",
    )
    payload = ChurnPredictionInput(**dados)
    servico = ChurnPreprocessingService()

    features = servico.transformar(payload)

    assert features["quantidade_de_addons"].iloc[0] == 2.0


def test_transformar_trata_cliente_sem_servico_de_internet(
    payload_valido_dict,
):
    """Transformar trata cliente sem servico de internet."""
    dados = dict(
        payload_valido_dict,
        possui_servico_de_internet="No",
        possui_seguranca_online="No internet service",
        possui_backup_online="No internet service",
        possui_protecao_dispositivo="No internet service",
        possui_suporte_tecnico_premium="No internet service",
        possui_streaming_tv_terceiros="No internet service",
        possui_streaming_filmes_terceiros="No internet service",
    )
    payload = ChurnPredictionInput(**dados)
    servico = ChurnPreprocessingService()

    features = servico.transformar(payload)

    assert features["possui_servico_de_internet_sem_internet"].iloc[0] == 1.0
    assert features["possui_servico_de_internet_dsl"].iloc[0] == 0.0
    assert features["possui_servico_de_internet_fibra_optica"].iloc[0] == 0.0
    assert features["quantidade_de_addons"].iloc[0] == 0.0


def test_transformar_codifica_metodo_de_pagamento_em_one_hot(
    payload_valido_dict,
):
    """Transformar codifica metodo de pagamento em one hot."""
    dados = dict(
        payload_valido_dict, metodo_pagamento="Credit card (automatic)"
    )
    payload = ChurnPredictionInput(**dados)
    servico = ChurnPreprocessingService()

    features = servico.transformar(payload)

    assert features["metodo_pagamento_credit_card_automatic"].iloc[0] == 1.0
    assert features["metodo_pagamento_bank_transfer_automatic"].iloc[0] == 0.0
    assert features["metodo_pagamento_electronic_check"].iloc[0] == 0.0
    assert features["metodo_pagamento_mailed_check"].iloc[0] == 0.0

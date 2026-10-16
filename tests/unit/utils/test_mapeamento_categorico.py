from tech_challenge_churn_prediction.utils.mapeamento_categorico import (
    MAPA_BINARIO_COM_AUSENCIA_DE_SERVICO,
    MAPA_TIPO_CONTRATO,
)


def test_mapa_binario_com_ausencia_de_servico_contem_as_chaves_esperadas():
    assert MAPA_BINARIO_COM_AUSENCIA_DE_SERVICO == {
        "Yes": 1,
        "No": 0,
        "No internet service": 0,
        "No phone service": 0,
    }


def test_mapa_tipo_contrato_contem_a_ordinalidade_esperada():
    assert MAPA_TIPO_CONTRATO == {"Month-to-month": 0, "One year": 1, "Two year": 2}

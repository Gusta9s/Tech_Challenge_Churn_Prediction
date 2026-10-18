import numpy as np

from tech_challenge_churn_prediction.utils.transformadores_sklearn import (
    ContadorAddonsTransformer,
    MapeadorBinarioTransformer,
)

MAPA = {"Yes": 1, "No": 0, "No internet service": 0}


def test_mapeador_binario_transformer_fit_retorna_a_propria_instancia():
    """Mapeador binario transformer fit retorna a propria instancia."""
    transformer = MapeadorBinarioTransformer(MAPA)

    assert transformer.fit([["Yes"]]) is transformer


def test_mapeador_binario_transformer_transform_mapeia_os_valores():
    """Mapeador binario transformer transform mapeia os valores."""
    transformer = MapeadorBinarioTransformer(MAPA)

    resultado = transformer.transform(
        [["Yes"], ["No"], ["No internet service"]]
    )

    np.testing.assert_array_equal(resultado, [[1.0], [0.0], [0.0]])


def test_mapeador_binario_transformer_get_feature_names_out_retorna_entrada():
    """Mapeador binario transformer get feature names out retorna entrada."""
    transformer = MapeadorBinarioTransformer(MAPA)

    resultado = transformer.get_feature_names_out(["coluna_a", "coluna_b"])

    np.testing.assert_array_equal(resultado, ["coluna_a", "coluna_b"])


def test_contador_addons_transformer_fit_retorna_a_propria_instancia():
    """Contador addons transformer fit retorna a propria instancia."""
    transformer = ContadorAddonsTransformer(MAPA)

    assert transformer.fit([["Yes", "No"]]) is transformer


def test_contador_addons_transformer_transform_soma_os_valores_binarizados():
    """Contador addons transformer transform soma os valores binarizados."""
    transformer = ContadorAddonsTransformer(MAPA)

    resultado = transformer.transform(
        [["Yes", "Yes", "No"], ["No", "No", "No internet service"]]
    )

    np.testing.assert_array_equal(resultado, [[2.0], [0.0]])


def test_contador_addons_transformer_get_feature_names_out_retorna_nome_fixo():
    """Contador addons transformer get feature names out retorna nome fixo."""
    transformer = ContadorAddonsTransformer(MAPA)

    resultado = transformer.get_feature_names_out()

    np.testing.assert_array_equal(resultado, ["quantidade_de_addons"])

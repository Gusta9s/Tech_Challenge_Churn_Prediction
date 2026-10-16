from tech_challenge_churn_prediction.utils import constantes_modelo as alvo


def test_ordem_das_features_contem_as_23_colunas_esperadas_pelo_modelo():
    assert len(alvo.ORDEM_FEATURES_RANDOM_FOREST) == 23
    assert alvo.ORDEM_FEATURES_RANDOM_FOREST[0] == "cliente_em_idade_avancada"
    assert alvo.ORDEM_FEATURES_RANDOM_FOREST[-1] == "quantidade_de_addons"


def test_colunas_addons_estao_na_ordem_esperada():
    assert alvo.COLUNAS_ADDONS == (
        "possui_seguranca_online",
        "possui_backup_online",
        "possui_protecao_dispositivo",
        "possui_suporte_tecnico_premium",
        "possui_streaming_tv_terceiros",
        "possui_streaming_filmes_terceiros",
    )


def test_categorias_binarias_simples():
    assert alvo.CATEGORIAS_BINARIAS_SIMPLES == ("No", "Yes")


def test_categorias_tipo_contrato_e_derivada_do_mapa_de_tipo_contrato():
    assert alvo.CATEGORIAS_TIPO_CONTRATO == ("Month-to-month", "One year", "Two year")


def test_categorias_servico_de_internet_casa_em_quantidade_com_as_colunas():
    assert len(alvo.CATEGORIAS_SERVICO_DE_INTERNET) == len(alvo.COLUNAS_SERVICO_DE_INTERNET)


def test_categorias_metodo_pagamento_casa_em_quantidade_com_as_colunas():
    assert len(alvo.CATEGORIAS_METODO_PAGAMENTO) == len(alvo.COLUNAS_METODO_PAGAMENTO)

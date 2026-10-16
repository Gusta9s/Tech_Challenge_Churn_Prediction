from tech_challenge_churn_prediction.config.model_settings import ModelSettings, obter_model_settings


def test_model_settings_constroi_a_partir_dos_valores_informados():
    configuracoes = ModelSettings(diretorio_modelos="modelos", nome_arquivo_modelo="modelo.joblib")

    assert configuracoes.diretorio_modelos == "modelos"
    assert configuracoes.nome_arquivo_modelo == "modelo.joblib"


def test_obter_model_settings_retorna_a_mesma_instancia_em_chamadas_subsequentes():
    primeira_chamada = obter_model_settings()
    segunda_chamada = obter_model_settings()

    assert primeira_chamada is segunda_chamada

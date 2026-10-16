from tech_challenge_churn_prediction.config.app_settings import AppSettings, obter_app_settings


def test_app_settings_constroi_a_partir_dos_valores_informados():
    configuracoes = AppSettings(titulo="Minha API", versao="9.9.9")

    assert configuracoes.titulo == "Minha API"
    assert configuracoes.versao == "9.9.9"


def test_obter_app_settings_retorna_a_mesma_instancia_em_chamadas_subsequentes():
    primeira_chamada = obter_app_settings()
    segunda_chamada = obter_app_settings()

    assert primeira_chamada is segunda_chamada

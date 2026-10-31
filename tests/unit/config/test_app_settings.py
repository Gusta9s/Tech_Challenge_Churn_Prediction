from tech_challenge_churn_prediction.config.app_settings import (
    AppSettings,
    AppSettingsFactory,
)


def test_app_settings_constroi_a_partir_dos_valores_informados():
    """App settings constroi a partir dos valores informados."""
    configuracoes = AppSettings(titulo="Minha API", versao="9.9.9")

    assert configuracoes.titulo == "Minha API"
    assert configuracoes.versao == "9.9.9"


def test_app_settings_factory_criar_retorna_singleton():
    """App settings factory criar retorna singleton."""
    primeira_chamada = AppSettingsFactory.criar()
    segunda_chamada = AppSettingsFactory.criar()

    assert primeira_chamada is segunda_chamada

from tech_challenge_churn_prediction.config.logging_settings import (
    LoggingSettings,
    LoggingSettingsFactory,
)


def test_logging_settings_constroi_a_partir_dos_valores_informados():
    """Logging settings constroi a partir dos valores informados."""
    configuracoes = LoggingSettings(nivel="DEBUG", formato="%(message)s")

    assert configuracoes.nivel == "DEBUG"
    assert configuracoes.formato == "%(message)s"


def test_logging_settings_factory_criar_retorna_singleton():
    """Logging settings factory criar retorna singleton."""
    primeira_chamada = LoggingSettingsFactory.criar()
    segunda_chamada = LoggingSettingsFactory.criar()

    assert primeira_chamada is segunda_chamada

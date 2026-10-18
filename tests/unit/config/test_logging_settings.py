from tech_challenge_churn_prediction.config.logging_settings import (
    LoggingSettings,
    obter_logging_settings,
)


def test_logging_settings_constroi_a_partir_dos_valores_informados():
    """Logging settings constroi a partir dos valores informados."""
    configuracoes = LoggingSettings(nivel="DEBUG", formato="%(message)s")

    assert configuracoes.nivel == "DEBUG"
    assert configuracoes.formato == "%(message)s"


def test_obter_logging_settings_retorna_singleton():
    """Obter logging settings retorna singleton."""
    primeira_chamada = obter_logging_settings()
    segunda_chamada = obter_logging_settings()

    assert primeira_chamada is segunda_chamada

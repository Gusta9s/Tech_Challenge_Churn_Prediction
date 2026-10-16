from tech_challenge_churn_prediction.config.logging_settings import LoggingSettings, obter_logging_settings


def test_logging_settings_constroi_a_partir_dos_valores_informados():
    configuracoes = LoggingSettings(nivel="DEBUG", formato="%(message)s")

    assert configuracoes.nivel == "DEBUG"
    assert configuracoes.formato == "%(message)s"


def test_obter_logging_settings_retorna_a_mesma_instancia_em_chamadas_subsequentes():
    primeira_chamada = obter_logging_settings()
    segunda_chamada = obter_logging_settings()

    assert primeira_chamada is segunda_chamada

from tech_challenge_churn_prediction.config.rate_limit_settings import (
    RateLimitSettings,
    obter_rate_limit_settings,
)


def test_rate_limit_settings_constroi_a_partir_dos_valores_informados():
    """Rate limit settings constroi a partir dos valores informados."""
    configuracoes = RateLimitSettings(
        limite_requisicoes=7,
        janela_em_segundos=45,
        cabecalho_requisicoes_restantes="X-Teste-Restantes",
    )

    assert configuracoes.limite_requisicoes == 7
    assert configuracoes.janela_em_segundos == 45
    assert configuracoes.cabecalho_requisicoes_restantes == "X-Teste-Restantes"


def test_obter_rate_limit_settings_retorna_singleton():
    """Obter rate limit settings retorna singleton."""
    primeira_chamada = obter_rate_limit_settings()
    segunda_chamada = obter_rate_limit_settings()

    assert primeira_chamada is segunda_chamada

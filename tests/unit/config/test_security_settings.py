from tech_challenge_churn_prediction.config.security_settings import SecuritySettings, obter_security_settings


def test_security_settings_constroi_a_partir_dos_valores_informados():
    configuracoes = SecuritySettings(campos_sensiveis=frozenset({"senha"}), mascara_padrao="[OCULTO]")

    assert configuracoes.campos_sensiveis == frozenset({"senha"})
    assert configuracoes.mascara_padrao == "[OCULTO]"


def test_obter_security_settings_retorna_a_mesma_instancia_em_chamadas_subsequentes():
    primeira_chamada = obter_security_settings()
    segunda_chamada = obter_security_settings()

    assert primeira_chamada is segunda_chamada

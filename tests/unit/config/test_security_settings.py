from tech_challenge_churn_prediction.config.security_settings import (
    SecuritySettings,
    SecuritySettingsFactory,
)


def test_security_settings_constroi_a_partir_dos_valores_informados():
    """Security settings constroi a partir dos valores informados."""
    configuracoes = SecuritySettings(
        campos_sensiveis=frozenset({"senha"}), mascara_padrao="[OCULTO]"
    )

    assert configuracoes.campos_sensiveis == frozenset({"senha"})
    assert configuracoes.mascara_padrao == "[OCULTO]"


def test_security_settings_factory_criar_retorna_singleton():
    """Security settings factory criar retorna singleton."""
    primeira_chamada = SecuritySettingsFactory.criar()
    segunda_chamada = SecuritySettingsFactory.criar()

    assert primeira_chamada is segunda_chamada

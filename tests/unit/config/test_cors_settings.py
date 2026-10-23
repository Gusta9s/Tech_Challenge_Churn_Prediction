from tech_challenge_churn_prediction.config.cors_settings import (
    CorsSettings,
    CorsSettingsFactory,
)

ORIGEM_FICTICIA = "http://cliente-de-teste.exemplo:4000"


def test_cors_settings_constroi_a_partir_dos_valores_informados():
    """Cors settings constroi a partir dos valores informados."""
    configuracoes = CorsSettings(
        origens_permitidas=(ORIGEM_FICTICIA,),
        metodos_permitidos=("GET", "POST"),
        cabecalhos_permitidos=("*",),
        permitir_credenciais=False,
    )

    assert configuracoes.origens_permitidas == (ORIGEM_FICTICIA,)
    assert configuracoes.metodos_permitidos == ("GET", "POST")
    assert configuracoes.cabecalhos_permitidos == ("*",)
    assert configuracoes.permitir_credenciais is False


def test_cors_settings_factory_criar_retorna_singleton():
    """Cors settings factory criar retorna singleton."""
    primeira_chamada = CorsSettingsFactory.criar()
    segunda_chamada = CorsSettingsFactory.criar()

    assert primeira_chamada is segunda_chamada

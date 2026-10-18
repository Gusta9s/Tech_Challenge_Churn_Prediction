from tech_challenge_churn_prediction.config.cors_settings import (
    CorsSettings,
    obter_cors_settings,
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


def test_obter_cors_settings_retorna_singleton():
    """Obter cors settings retorna singleton."""
    primeira_chamada = obter_cors_settings()
    segunda_chamada = obter_cors_settings()

    assert primeira_chamada is segunda_chamada

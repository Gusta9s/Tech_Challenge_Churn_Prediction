from fastapi import FastAPI
from fastapi.testclient import TestClient

from tech_challenge_churn_prediction.config.cors_settings import CorsSettings
from tech_challenge_churn_prediction.middlewares import cors_middleware as alvo
from tech_challenge_churn_prediction.middlewares.cors_middleware import (
    configurar_cors,
)

ORIGEM_PERMITIDA = "http://cliente-de-teste.exemplo:4000"
ORIGEM_NAO_PERMITIDA = "http://origem-nao-cadastrada.exemplo:9999"


def _criar_client(monkeypatch) -> TestClient:
    monkeypatch.setattr(
        alvo.CorsSettingsFactory,
        "criar",
        lambda: CorsSettings(
            origens_permitidas=(ORIGEM_PERMITIDA,),
            metodos_permitidos=("GET", "POST"),
            cabecalhos_permitidos=("*",),
            permitir_credenciais=False,
        ),
    )
    app = FastAPI()

    @app.get("/exemplo")
    def endpoint_get():
        return {"ok": True}

    @app.post("/exemplo")
    def endpoint_post():
        return {"ok": True}

    configurar_cors(app)
    return TestClient(app)


def test_requisicao_simples_da_origem_permitida_recebe_o_cabecalho_cors(
    monkeypatch,
):
    """Requisicao simples da origem permitida recebe o cabecalho cors."""
    client = _criar_client(monkeypatch)

    resposta = client.get("/exemplo", headers={"Origin": ORIGEM_PERMITIDA})

    assert resposta.status_code == 200
    assert resposta.headers["access-control-allow-origin"] == ORIGEM_PERMITIDA
    assert "access-control-allow-credentials" not in resposta.headers


def test_preflight_da_origem_permitida_libera_get_e_post(monkeypatch):
    """Preflight da origem permitida libera get e post."""
    client = _criar_client(monkeypatch)

    resposta = client.options(
        "/exemplo",
        headers={
            "Origin": ORIGEM_PERMITIDA,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "x-cabecalho-customizado",
        },
    )

    assert resposta.status_code == 200
    assert "GET" in resposta.headers["access-control-allow-methods"]
    assert "POST" in resposta.headers["access-control-allow-methods"]
    assert (
        resposta.headers["access-control-allow-headers"]
        == "x-cabecalho-customizado"
    )


def test_preflight_de_origem_nao_permitida_e_rejeitado(monkeypatch):
    """Preflight de origem nao permitida e rejeitado."""
    client = _criar_client(monkeypatch)

    resposta = client.options(
        "/exemplo",
        headers={
            "Origin": ORIGEM_NAO_PERMITIDA,
            "Access-Control-Request-Method": "POST",
        },
    )

    assert resposta.status_code == 400


def test_preflight_com_metodo_nao_permitido_e_rejeitado(monkeypatch):
    """Preflight com metodo nao permitido e rejeitado."""
    client = _criar_client(monkeypatch)

    resposta = client.options(
        "/exemplo",
        headers={
            "Origin": ORIGEM_PERMITIDA,
            "Access-Control-Request-Method": "DELETE",
        },
    )

    assert resposta.status_code == 400

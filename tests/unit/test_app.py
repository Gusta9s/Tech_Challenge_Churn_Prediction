from fastapi import FastAPI
from fastapi.testclient import TestClient

from tech_challenge_churn_prediction.app import app, criar_app


def test_app_e_uma_instancia_fastapi_com_os_routers_registrados():
    assert isinstance(app, FastAPI)
    client = TestClient(app)

    assert client.get("/health/liveness").status_code == 200
    assert client.get("/health/readiness").status_code in (200, 503)
    assert client.post("/predict", json={}).status_code == 422


def test_criar_app_monta_uma_nova_instancia_independente_da_global():
    nova_app = criar_app()

    assert isinstance(nova_app, FastAPI)
    assert nova_app is not app

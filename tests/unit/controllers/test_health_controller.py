import pytest
from fastapi.testclient import TestClient

from tech_challenge_churn_prediction.app import app
from tech_challenge_churn_prediction.controllers import dependencies
from tech_challenge_churn_prediction.services.health_check_service import (
    HealthCheckService,
)


class ModelLoaderFalsoOk:
    def carregar(self):
        return object()


class ModelLoaderFalsoComFalha:
    def carregar(self):
        raise FileNotFoundError("modelo ausente")


@pytest.fixture(autouse=True)
def limpar_overrides_apos_cada_teste():
    yield
    app.dependency_overrides.clear()


def test_liveness_retorna_200_e_status_up():
    """Liveness retorna 200 e status up."""
    client = TestClient(app)

    resposta = client.get("/health/liveness")

    assert resposta.status_code == 200
    assert resposta.json() == {"status": "UP"}


def test_readiness_retorna_200_quando_o_modelo_esta_disponivel():
    """Readiness retorna 200 quando o modelo esta disponivel."""
    app.dependency_overrides[dependencies.HealthCheckServiceFactory.criar] = (
        lambda: HealthCheckService(ModelLoaderFalsoOk())
    )
    client = TestClient(app)

    resposta = client.get("/health/readiness")

    assert resposta.status_code == 200
    assert resposta.json() == {"status": "UP"}


def test_readiness_retorna_503_quando_o_modelo_nao_esta_disponivel():
    """Readiness retorna 503 quando o modelo nao esta disponivel."""
    app.dependency_overrides[dependencies.HealthCheckServiceFactory.criar] = (
        lambda: HealthCheckService(ModelLoaderFalsoComFalha())
    )
    client = TestClient(app)

    resposta = client.get("/health/readiness")

    assert resposta.status_code == 503
    corpo = resposta.json()
    assert corpo["erro"] == "MODELO_INDISPONIVEL"

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from tech_challenge_churn_prediction.app import app
from tech_challenge_churn_prediction.controllers import dependencies
from tech_challenge_churn_prediction.schemas.churn_prediction_result import ChurnPredictionResult


class PreprocessingFalsoOk:
    def transformar(self, payload):
        return pd.DataFrame([{"coluna": 1.0}])


class PreprocessingFalsoComFalha:
    def transformar(self, payload):
        raise ValueError("payload incompativel com o pipeline")


class ModelLoaderFalsoOk:
    def carregar(self):
        return object()


class ModelLoaderFalsoComFalha:
    def carregar(self):
        raise FileNotFoundError("modelo ausente")


class PredictionFalsoOk:
    def prever(self, modelo, features):
        return ChurnPredictionResult(churn_previsto=True, probabilidade_churn=0.8, probabilidade_nao_churn=0.2)


@pytest.fixture(autouse=True)
def limpar_overrides_apos_cada_teste():
    yield
    app.dependency_overrides.clear()


def test_predict_retorna_200_com_o_resultado_no_fluxo_feliz(payload_valido_dict):
    app.dependency_overrides[dependencies.obter_preprocessing_service] = lambda: PreprocessingFalsoOk()
    app.dependency_overrides[dependencies.obter_model_loader_service] = lambda: ModelLoaderFalsoOk()
    app.dependency_overrides[dependencies.obter_prediction_service] = lambda: PredictionFalsoOk()
    client = TestClient(app)

    resposta = client.post("/predict", json=payload_valido_dict)

    assert resposta.status_code == 200
    assert resposta.json() == {
        "churn_previsto": True,
        "probabilidade_churn": 0.8,
        "probabilidade_nao_churn": 0.2,
    }


def test_predict_retorna_400_quando_o_pre_processamento_falha(payload_valido_dict):
    app.dependency_overrides[dependencies.obter_preprocessing_service] = lambda: PreprocessingFalsoComFalha()
    client = TestClient(app)

    resposta = client.post("/predict", json=payload_valido_dict)

    assert resposta.status_code == 400
    assert resposta.json()["erro"] == "ERRO_PRE_PROCESSAMENTO"


def test_predict_retorna_500_quando_o_carregamento_do_modelo_falha(payload_valido_dict):
    app.dependency_overrides[dependencies.obter_preprocessing_service] = lambda: PreprocessingFalsoOk()
    app.dependency_overrides[dependencies.obter_model_loader_service] = lambda: ModelLoaderFalsoComFalha()
    client = TestClient(app)

    resposta = client.post("/predict", json=payload_valido_dict)

    assert resposta.status_code == 500
    assert resposta.json()["erro"] == "ERRO_PREDICAO"


def test_predict_retorna_422_quando_o_payload_e_invalido(payload_valido_dict):
    payload_invalido = dict(payload_valido_dict)
    del payload_invalido["casado"]
    client = TestClient(app)

    resposta = client.post("/predict", json=payload_invalido)

    assert resposta.status_code == 422
    assert resposta.json()["erro"] == "PAYLOAD_INVALIDO"

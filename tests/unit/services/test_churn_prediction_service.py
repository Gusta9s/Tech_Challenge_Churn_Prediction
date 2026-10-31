import numpy as np
import pandas as pd

from tech_challenge_churn_prediction.config.prediction_settings import (
    PredictionSettings,
)
from tech_challenge_churn_prediction.services import (
    churn_prediction_service as alvo,
)
from tech_challenge_churn_prediction.services.churn_prediction_service import (
    ChurnPredictionService,
)

LIMIAR_FICTICIO = 0.6


class ModeloFalso:
    """Estimador falso, desacoplado do sklearn real, usado para isolar o
    teste de ChurnPredictionService da responsabilidade de treino do modelo.
    """

    def __init__(self, probabilidades: list[float]) -> None:
        self._probabilidades = probabilidades

    def predict_proba(self, features: pd.DataFrame) -> np.ndarray:
        return np.array([self._probabilidades])


def _criar_servico(monkeypatch) -> ChurnPredictionService:
    monkeypatch.setattr(
        alvo.PredictionSettingsFactory,
        "criar",
        lambda: PredictionSettings(limiar_decisao_churn=LIMIAR_FICTICIO),
    )
    return ChurnPredictionService()


def test_prever_retorna_churn_previsto_true_acima_do_limiar(monkeypatch):
    """Prever retorna churn previsto true acima do limiar."""
    servico = _criar_servico(monkeypatch)

    resultado = servico.prever(ModeloFalso([0.3, 0.7]), pd.DataFrame([{}]))

    assert resultado.churn_previsto is True
    assert resultado.probabilidade_churn == 0.7
    assert resultado.probabilidade_nao_churn == 0.3


def test_prever_retorna_churn_previsto_true_no_limiar(monkeypatch):
    """Prever retorna churn previsto true no limiar."""
    servico = _criar_servico(monkeypatch)

    resultado = servico.prever(
        ModeloFalso([1 - LIMIAR_FICTICIO, LIMIAR_FICTICIO]),
        pd.DataFrame([{}]),
    )

    assert resultado.churn_previsto is True


def test_prever_retorna_churn_previsto_false_abaixo_do_limiar(monkeypatch):
    """Prever retorna churn previsto false abaixo do limiar."""
    servico = _criar_servico(monkeypatch)

    resultado = servico.prever(ModeloFalso([0.9, 0.1]), pd.DataFrame([{}]))

    assert resultado.churn_previsto is False
    assert resultado.probabilidade_churn == 0.1
    assert resultado.probabilidade_nao_churn == 0.9

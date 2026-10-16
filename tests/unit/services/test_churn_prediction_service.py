import numpy as np
import pandas as pd

from tech_challenge_churn_prediction.services.churn_prediction_service import ChurnPredictionService


class ModeloFalso:
    """Estimador falso, desacoplado do sklearn real, para isolar o teste de
    ChurnPredictionService da responsabilidade de carregamento/treino do modelo.
    """

    def __init__(self, probabilidades: list[float]) -> None:
        self._probabilidades = probabilidades

    def predict_proba(self, features: pd.DataFrame) -> np.ndarray:
        return np.array([self._probabilidades])


def test_prever_retorna_churn_previsto_true_quando_probabilidade_e_maior_que_o_limiar():
    servico = ChurnPredictionService()

    resultado = servico.prever(ModeloFalso([0.3, 0.7]), pd.DataFrame([{}]))

    assert resultado.churn_previsto is True
    assert resultado.probabilidade_churn == 0.7
    assert resultado.probabilidade_nao_churn == 0.3


def test_prever_retorna_churn_previsto_true_quando_probabilidade_e_igual_ao_limiar():
    servico = ChurnPredictionService()

    resultado = servico.prever(ModeloFalso([0.5, 0.5]), pd.DataFrame([{}]))

    assert resultado.churn_previsto is True


def test_prever_retorna_churn_previsto_false_quando_probabilidade_e_menor_que_o_limiar():
    servico = ChurnPredictionService()

    resultado = servico.prever(ModeloFalso([0.9, 0.1]), pd.DataFrame([{}]))

    assert resultado.churn_previsto is False
    assert resultado.probabilidade_churn == 0.1
    assert resultado.probabilidade_nao_churn == 0.9

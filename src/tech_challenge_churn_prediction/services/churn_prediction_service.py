import pandas as pd
from sklearn.base import BaseEstimator

from tech_challenge_churn_prediction.schemas.churn_prediction_result import ChurnPredictionResult

INDICE_CLASSE_NAO_CHURN = 0
INDICE_CLASSE_CHURN = 1
LIMIAR_DECISAO_CHURN = 0.5


class ChurnPredictionService:
    """Responsavel exclusivamente por executar a predicao do modelo treinado
    sobre features ja pre-processadas e traduzir a saida bruta do sklearn em
    um resultado de dominio (ChurnPredictionResult).

    Nao carrega o modelo nem pre-processa dados: recebe ambos por parametro,
    mantendo baixo acoplamento com as demais responsabilidades do fluxo.
    """

    def prever(self, modelo: BaseEstimator, features: pd.DataFrame) -> ChurnPredictionResult:
        probabilidades = modelo.predict_proba(features)[0]
        probabilidade_churn = float(probabilidades[INDICE_CLASSE_CHURN])
        probabilidade_nao_churn = float(probabilidades[INDICE_CLASSE_NAO_CHURN])

        return ChurnPredictionResult(
            churn_previsto=probabilidade_churn >= LIMIAR_DECISAO_CHURN,
            probabilidade_churn=probabilidade_churn,
            probabilidade_nao_churn=probabilidade_nao_churn,
        )

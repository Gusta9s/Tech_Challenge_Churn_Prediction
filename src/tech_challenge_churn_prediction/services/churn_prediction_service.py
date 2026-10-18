import pandas as pd
from sklearn.base import BaseEstimator

from tech_challenge_churn_prediction.config.prediction_settings import (
    obter_prediction_settings,
)
from tech_challenge_churn_prediction.schemas.churn_prediction_result import (
    ChurnPredictionResult,
)

INDICE_CLASSE_NAO_CHURN = 0
INDICE_CLASSE_CHURN = 1


class ChurnPredictionService:
    """Executa a predicao do modelo e traduz o resultado para o dominio.

    Nao carrega o modelo nem pre-processa dados: recebe ambos por
    parametro, mantendo baixo acoplamento com as demais
    responsabilidades do fluxo.
    """

    def __init__(self) -> None:
        """Resolve o limiar de decisao de churn a partir das settings."""
        self._limiar_decisao_churn = (
            obter_prediction_settings().limiar_decisao_churn
        )

    def prever(
        self, modelo: BaseEstimator, features: pd.DataFrame
    ) -> ChurnPredictionResult:
        """Executa a predicao do modelo sobre as features informadas.

        Parameters
        ----------
        modelo : sklearn.base.BaseEstimator
            Estimador treinado, ja carregado em memoria.
        features : pandas.DataFrame
            Features pre-processadas, na ordem esperada pelo modelo.

        Returns
        -------
        ChurnPredictionResult
            Resultado de dominio com a decisao e as probabilidades.
        """
        probabilidades = modelo.predict_proba(features)[0]
        probabilidade_churn = float(probabilidades[INDICE_CLASSE_CHURN])
        probabilidade_nao_churn = float(
            probabilidades[INDICE_CLASSE_NAO_CHURN]
        )

        return ChurnPredictionResult(
            churn_previsto=probabilidade_churn >= self._limiar_decisao_churn,
            probabilidade_churn=probabilidade_churn,
            probabilidade_nao_churn=probabilidade_nao_churn,
        )

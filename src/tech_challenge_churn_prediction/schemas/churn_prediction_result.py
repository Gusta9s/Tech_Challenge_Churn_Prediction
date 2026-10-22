from pydantic import BaseModel


class ChurnPredictionResult(BaseModel):
    """Resultado de dominio de uma predicao de churn.

    Attributes
    ----------
    churn_previsto : bool
        True se a probabilidade de churn atinge o limiar de decisao.
    probabilidade_churn : float
        Probabilidade estimada do cliente cancelar.
    probabilidade_nao_churn : float
        Probabilidade estimada do cliente nao cancelar.
    """

    churn_previsto: bool
    probabilidade_churn: float
    probabilidade_nao_churn: float

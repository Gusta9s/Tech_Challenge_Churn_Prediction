from pydantic import BaseModel


class ChurnPredictionResult(BaseModel):
    """Resultado de dominio de uma predicao de churn para uma unica requisicao."""

    churn_previsto: bool
    probabilidade_churn: float
    probabilidade_nao_churn: float

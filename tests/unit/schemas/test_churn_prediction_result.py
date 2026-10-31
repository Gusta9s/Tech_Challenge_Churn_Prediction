from tech_challenge_churn_prediction.schemas.churn_prediction_result import (
    ChurnPredictionResult,
)


def test_cria_resultado_valido_com_os_campos_informados():
    """Cria resultado valido com os campos informados."""
    resultado = ChurnPredictionResult(
        churn_previsto=True,
        probabilidade_churn=0.9,
        probabilidade_nao_churn=0.1,
    )

    assert resultado.churn_previsto is True
    assert resultado.probabilidade_churn == 0.9
    assert resultado.probabilidade_nao_churn == 0.1

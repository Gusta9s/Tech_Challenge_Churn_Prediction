from tech_challenge_churn_prediction.config.prediction_settings import (
    PredictionSettings,
    obter_prediction_settings,
)


def test_prediction_settings_constroi_a_partir_dos_valores_informados():
    """Prediction settings constroi a partir dos valores informados."""
    configuracoes = PredictionSettings(limiar_decisao_churn=0.42)

    assert configuracoes.limiar_decisao_churn == 0.42


def test_obter_prediction_settings_retorna_singleton():
    """Obter prediction settings retorna singleton."""
    primeira_chamada = obter_prediction_settings()
    segunda_chamada = obter_prediction_settings()

    assert primeira_chamada is segunda_chamada

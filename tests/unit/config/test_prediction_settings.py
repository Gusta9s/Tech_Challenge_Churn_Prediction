from tech_challenge_churn_prediction.config.prediction_settings import (
    PredictionSettings,
    PredictionSettingsFactory,
)


def test_prediction_settings_constroi_a_partir_dos_valores_informados():
    """Prediction settings constroi a partir dos valores informados."""
    configuracoes = PredictionSettings(limiar_decisao_churn=0.42)

    assert configuracoes.limiar_decisao_churn == 0.42


def test_prediction_settings_factory_criar_retorna_singleton():
    """Prediction settings factory criar retorna singleton."""
    primeira_chamada = PredictionSettingsFactory.criar()
    segunda_chamada = PredictionSettingsFactory.criar()

    assert primeira_chamada is segunda_chamada

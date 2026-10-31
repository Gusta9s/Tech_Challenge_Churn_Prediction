from tech_challenge_churn_prediction.config.model_settings import (
    ModelSettings,
    ModelSettingsFactory,
)


def test_model_settings_constroi_a_partir_dos_valores_informados():
    """Model settings constroi a partir dos valores informados."""
    configuracoes = ModelSettings(
        diretorio_modelos="modelos", nome_arquivo_modelo="modelo.joblib"
    )

    assert configuracoes.diretorio_modelos == "modelos"
    assert configuracoes.nome_arquivo_modelo == "modelo.joblib"


def test_model_settings_factory_criar_retorna_singleton():
    """Model settings factory criar retorna singleton."""
    primeira_chamada = ModelSettingsFactory.criar()
    segunda_chamada = ModelSettingsFactory.criar()

    assert primeira_chamada is segunda_chamada

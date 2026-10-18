from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class PredictionSettings(BaseSettings):
    """Configuracoes do comportamento de decisao da predicao.

    Nao possui valores pre-setados: depende exclusivamente de variaveis
    de ambiente com prefixo `PREDICTION_`, lidas do ambiente do processo
    ou do arquivo `.env` na raiz do projeto.

    Attributes
    ----------
    limiar_decisao_churn : float
        Probabilidade minima para classificar a predicao como churn
        (PREDICTION_LIMIAR_DECISAO_CHURN).
    """

    model_config = SettingsConfigDict(
        env_prefix="PREDICTION_", env_file=".env", extra="ignore"
    )

    limiar_decisao_churn: float


@lru_cache
def obter_prediction_settings() -> PredictionSettings:
    """Retorna a instancia singleton de PredictionSettings.

    Returns
    -------
    PredictionSettings
        Configuracoes de decisao da predicao.
    """
    return PredictionSettings()

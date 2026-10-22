from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class LoggingSettings(BaseSettings):
    """Configuracoes de logging, lidas do ambiente.

    Nao possui valores pre-setados: depende exclusivamente de variaveis
    de ambiente com prefixo `LOG_`, lidas do ambiente do processo ou do
    arquivo `.env` na raiz do projeto.

    Attributes
    ----------
    nivel : str
        Nivel minimo de log a ser emitido (LOG_NIVEL).
    formato : str
        Formato das mensagens de log (LOG_FORMATO).
    """

    model_config = SettingsConfigDict(
        env_prefix="LOG_", env_file=".env", extra="ignore"
    )

    nivel: str
    formato: str


@lru_cache
def obter_logging_settings() -> LoggingSettings:
    """Retorna a instancia singleton de LoggingSettings.

    Returns
    -------
    LoggingSettings
        Configuracoes de logging da aplicacao.
    """
    return LoggingSettings()

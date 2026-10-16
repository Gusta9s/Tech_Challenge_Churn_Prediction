from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class LoggingSettings(BaseSettings):
    """Configuracoes de logging.

    Nao possui valores pre-setados: depende exclusivamente de variaveis de
    ambiente com prefixo `LOG_` (ex.: LOG_NIVEL, LOG_FORMATO), lidas do
    ambiente do processo ou do arquivo `.env` na raiz do projeto.
    """

    model_config = SettingsConfigDict(
        env_prefix="LOG_", env_file=".env", extra="ignore"
    )

    nivel: str
    formato: str


@lru_cache
def obter_logging_settings() -> LoggingSettings:
    return LoggingSettings()

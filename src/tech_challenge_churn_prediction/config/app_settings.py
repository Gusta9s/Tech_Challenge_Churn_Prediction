from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Configuracoes gerais da aplicacao FastAPI (titulo, versao).

    Nao possui valores pre-setados: depende exclusivamente de variaveis de
    ambiente com prefixo `APP_` (ex.: APP_TITULO, APP_VERSAO), lidas do
    ambiente do processo ou do arquivo `.env` na raiz do projeto.
    """

    model_config = SettingsConfigDict(
        env_prefix="APP_", env_file=".env", extra="ignore"
    )

    titulo: str
    versao: str


@lru_cache
def obter_app_settings() -> AppSettings:
    return AppSettings()

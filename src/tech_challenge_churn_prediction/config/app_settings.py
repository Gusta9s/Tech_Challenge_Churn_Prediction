from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Configuracoes gerais da aplicacao FastAPI, lidas do ambiente.

    Nao possui valores pre-setados: depende exclusivamente de variaveis
    de ambiente com prefixo `APP_`, lidas do ambiente do processo ou do
    arquivo `.env` na raiz do projeto.

    Attributes
    ----------
    titulo : str
        Titulo exibido na documentacao OpenAPI (APP_TITULO).
    versao : str
        Versao exibida na documentacao OpenAPI (APP_VERSAO).
    """

    model_config = SettingsConfigDict(
        env_prefix="APP_", env_file=".env", extra="ignore"
    )

    titulo: str
    versao: str


@lru_cache
def obter_app_settings() -> AppSettings:
    """Retorna a instancia singleton de AppSettings.

    Returns
    -------
    AppSettings
        Configuracoes gerais da aplicacao.
    """
    return AppSettings()

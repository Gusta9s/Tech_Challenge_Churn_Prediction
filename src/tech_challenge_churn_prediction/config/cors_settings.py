from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class CorsSettings(BaseSettings):
    """Configuracoes de CORS (Cross-Origin Resource Sharing) do ambiente.

    Nao possui valores pre-setados: depende exclusivamente de variaveis
    de ambiente com prefixo `CORS_`, lidas do ambiente do processo ou
    do arquivo `.env` na raiz do projeto.

    Attributes
    ----------
    origens_permitidas : tuple[str, ...]
        Origens (esquema + host + porta) autorizadas a consumir a API
        via navegador, como JSON de lista (CORS_ORIGENS_PERMITIDAS).
    metodos_permitidos : tuple[str, ...]
        Metodos HTTP autorizados em requisicoes entre origens, como
        JSON de lista (CORS_METODOS_PERMITIDOS).
    cabecalhos_permitidos : tuple[str, ...]
        Cabecalhos autorizados em requisicoes entre origens, como JSON
        de lista (CORS_CABECALHOS_PERMITIDOS).
    permitir_credenciais : bool
        Indica se cookies/credenciais podem ser enviados entre origens
        (CORS_PERMITIR_CREDENCIAIS).
    """

    model_config = SettingsConfigDict(
        env_prefix="CORS_", env_file=".env", extra="ignore"
    )

    origens_permitidas: tuple[str, ...]
    metodos_permitidos: tuple[str, ...]
    cabecalhos_permitidos: tuple[str, ...]
    permitir_credenciais: bool


@lru_cache
def obter_cors_settings() -> CorsSettings:
    """Retorna a instancia singleton de CorsSettings.

    Returns
    -------
    CorsSettings
        Configuracoes de CORS da aplicacao.
    """
    return CorsSettings()

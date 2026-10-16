from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class SecuritySettings(BaseSettings):
    """Configuracoes de seguranca para mascaramento de dados sensiveis em logs.

    Nao possui valores pre-setados: depende exclusivamente de variaveis de
    ambiente com prefixo `SECURITY_` (ex.: SECURITY_CAMPOS_SENSIVEIS como
    JSON de lista, SECURITY_MASCARA_PADRAO), lidas do ambiente do processo
    ou do arquivo `.env` na raiz do projeto.
    """

    model_config = SettingsConfigDict(
        env_prefix="SECURITY_", env_file=".env", extra="ignore"
    )

    campos_sensiveis: frozenset[str]
    mascara_padrao: str


@lru_cache
def obter_security_settings() -> SecuritySettings:
    return SecuritySettings()

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelSettings(BaseSettings):
    """Configuracoes do artefato do modelo campeao.

    Nao possui valores pre-setados: depende exclusivamente de variaveis de
    ambiente com prefixo `MODEL_` (ex.: MODEL_DIRETORIO_MODELOS,
    MODEL_NOME_ARQUIVO_MODELO), lidas do ambiente do processo ou do arquivo
    `.env` na raiz do projeto.
    """

    model_config = SettingsConfigDict(
        env_prefix="MODEL_", env_file=".env", extra="ignore"
    )

    diretorio_modelos: str
    nome_arquivo_modelo: str


@lru_cache
def obter_model_settings() -> ModelSettings:
    return ModelSettings()

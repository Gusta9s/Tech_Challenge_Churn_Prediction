from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelSettings(BaseSettings):
    """Configuracoes do artefato do modelo campeao, lidas do ambiente.

    Nao possui valores pre-setados: depende exclusivamente de variaveis
    de ambiente com prefixo `MODEL_`, lidas do ambiente do processo ou
    do arquivo `.env` na raiz do projeto.

    Attributes
    ----------
    diretorio_modelos : str
        Nome do diretorio onde as versoes do modelo sao salvas
        (MODEL_DIRETORIO_MODELOS).
    nome_arquivo_modelo : str
        Nome do arquivo `.joblib` do modelo (MODEL_NOME_ARQUIVO_MODELO).
    """

    model_config = SettingsConfigDict(
        env_prefix="MODEL_", env_file=".env", extra="ignore"
    )

    diretorio_modelos: str
    nome_arquivo_modelo: str


@lru_cache
def obter_model_settings() -> ModelSettings:
    """Retorna a instancia singleton de ModelSettings.

    Returns
    -------
    ModelSettings
        Configuracoes do artefato do modelo campeao.
    """
    return ModelSettings()

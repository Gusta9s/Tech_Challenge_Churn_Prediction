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


class LoggingSettingsFactory:
    """Fabrica responsavel pela instancia singleton de LoggingSettings."""

    _instancia: LoggingSettings | None = None

    @classmethod
    def criar(cls) -> LoggingSettings:
        """Cria (ou reutiliza) a instancia singleton de LoggingSettings.

        Returns
        -------
        LoggingSettings
            Configuracoes de logging da aplicacao.
        """
        if cls._instancia is None:
            cls._instancia = LoggingSettings()
        return cls._instancia

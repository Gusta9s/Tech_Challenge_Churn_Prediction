from pydantic_settings import BaseSettings, SettingsConfigDict


class SecuritySettings(BaseSettings):
    """Configuracoes de mascaramento de dados sensiveis em logs.

    Nao possui valores pre-setados: depende exclusivamente de variaveis
    de ambiente com prefixo `SECURITY_`, lidas do ambiente do processo
    ou do arquivo `.env` na raiz do projeto.

    Attributes
    ----------
    campos_sensiveis : frozenset[str]
        Nomes dos campos a mascarar em logs, como JSON de lista
        (SECURITY_CAMPOS_SENSIVEIS).
    mascara_padrao : str
        Valor usado para substituir campos sensiveis (SECURITY_MASCARA_PADRAO).
    """

    model_config = SettingsConfigDict(
        env_prefix="SECURITY_", env_file=".env", extra="ignore"
    )

    campos_sensiveis: frozenset[str]
    mascara_padrao: str


class SecuritySettingsFactory:
    """Fabrica responsavel pela instancia singleton de SecuritySettings."""

    _instancia: SecuritySettings | None = None

    @classmethod
    def criar(cls) -> SecuritySettings:
        """Cria (ou reutiliza) a instancia singleton de SecuritySettings.

        Returns
        -------
        SecuritySettings
            Configuracoes de mascaramento de dados sensiveis.
        """
        if cls._instancia is None:
            cls._instancia = SecuritySettings()
        return cls._instancia

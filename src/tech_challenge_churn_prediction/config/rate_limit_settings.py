from pydantic_settings import BaseSettings, SettingsConfigDict


class RateLimitSettings(BaseSettings):
    """Configuracoes do limite de requisicoes por cliente, lidas do ambiente.

    Nao possui valores pre-setados: depende exclusivamente de variaveis
    de ambiente com prefixo `RATE_LIMIT_`, lidas do ambiente do processo
    ou do arquivo `.env` na raiz do projeto.

    Attributes
    ----------
    limite_requisicoes : int
        Quantidade maxima de requisicoes por cliente dentro da janela
        de tempo (RATE_LIMIT_LIMITE_REQUISICOES).
    janela_em_segundos : float
        Duracao, em segundos, da janela deslizante usada para contar
        requisicoes (RATE_LIMIT_JANELA_EM_SEGUNDOS).
    cabecalho_requisicoes_restantes : str
        Nome do cabecalho HTTP com a contagem de requisicoes restantes
        (RATE_LIMIT_CABECALHO_REQUISICOES_RESTANTES).
    """

    model_config = SettingsConfigDict(
        env_prefix="RATE_LIMIT_", env_file=".env", extra="ignore"
    )

    limite_requisicoes: int
    janela_em_segundos: float
    cabecalho_requisicoes_restantes: str


class RateLimitSettingsFactory:
    """Fabrica responsavel pela instancia singleton de RateLimitSettings."""

    _instancia: RateLimitSettings | None = None

    @classmethod
    def criar(cls) -> RateLimitSettings:
        """Cria (ou reutiliza) a instancia singleton de RateLimitSettings.

        Returns
        -------
        RateLimitSettings
            Configuracoes do limite de requisicoes por cliente.
        """
        if cls._instancia is None:
            cls._instancia = RateLimitSettings()
        return cls._instancia

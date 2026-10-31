class ChurnPredictionAppException(Exception):
    """Excecao base de dominio da aplicacao.

    Carrega os metadados padronizados usados tanto para montar a resposta
    de erro (level, message, erro, cause) quanto para o registro em log,
    desacoplando as excecoes de dominio de como sao exibidas/logadas.
    """

    def __init__(
        self,
        message: str,
        erro: str,
        status_code: int,
        level: str = "ERROR",
        cause: Exception | None = None,
    ) -> None:
        """Inicializa a excecao com os metadados de resposta e log.

        Parameters
        ----------
        message : str
            Mensagem voltada ao cliente da API.
        erro : str
            Codigo curto que identifica o tipo de erro.
        status_code : int
            Codigo HTTP a ser retornado pelo exception handler.
        level : str, default="ERROR"
            Nivel de log usado ao registrar a excecao.
        cause : Exception or None, default=None
            Excecao original que motivou este erro, se houver.
        """
        super().__init__(message)
        self.message = message
        self.erro = erro
        self.status_code = status_code
        self.level = level
        self.cause = cause


class PayloadInvalidoException(ChurnPredictionAppException):
    """O payload de entrada nao atende ao contrato esperado pela API."""

    def __init__(self, cause: Exception | None = None) -> None:
        """Inicializa a excecao com os metadados fixos de payload invalido.

        Parameters
        ----------
        cause : Exception or None, default=None
            Excecao original que motivou este erro, se houver.
        """
        super().__init__(
            message="O payload de entrada e invalido ou esta incompleto.",
            erro="PAYLOAD_INVALIDO",
            status_code=422,
            level="WARNING",
            cause=cause,
        )


class PreProcessamentoException(ChurnPredictionAppException):
    """Falha ao transformar o payload de entrada nas features do modelo."""

    def __init__(self, cause: Exception | None = None) -> None:
        """Inicializa a excecao com os metadados fixos de pre-processamento.

        Parameters
        ----------
        cause : Exception or None, default=None
            Excecao original que motivou este erro, se houver.
        """
        super().__init__(
            message=(
                "Nao foi possivel processar os dados de entrada "
                "para predicao."
            ),
            erro="ERRO_PRE_PROCESSAMENTO",
            status_code=400,
            level="WARNING",
            cause=cause,
        )


class ModeloNaoDisponivelException(ChurnPredictionAppException):
    """O artefato do modelo nao pode ser carregado (ausente ou corrompido)."""

    def __init__(self, cause: Exception | None = None) -> None:
        """Inicializa a excecao com os metadados fixos de modelo indisponivel.

        Parameters
        ----------
        cause : Exception or None, default=None
            Excecao original que motivou este erro, se houver.
        """
        super().__init__(
            message="O modelo de predicao nao esta disponivel no momento.",
            erro="MODELO_INDISPONIVEL",
            status_code=503,
            level="ERROR",
            cause=cause,
        )


class PredicaoException(ChurnPredictionAppException):
    """Falha ao executar a predicao do modelo sobre as features processadas."""

    def __init__(self, cause: Exception | None = None) -> None:
        """Inicializa a excecao com os metadados fixos de erro de predicao.

        Parameters
        ----------
        cause : Exception or None, default=None
            Excecao original que motivou este erro, se houver.
        """
        super().__init__(
            message="Ocorreu um erro ao executar a predicao do modelo.",
            erro="ERRO_PREDICAO",
            status_code=500,
            level="ERROR",
            cause=cause,
        )

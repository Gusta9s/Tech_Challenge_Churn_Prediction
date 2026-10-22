from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Formato padronizado de resposta de erro para os cenarios 4xx/5xx.

    Attributes
    ----------
    level : str
        Nivel de severidade (ex.: "WARNING", "ERROR").
    message : str
        Mensagem de erro voltada ao cliente da API.
    erro : str
        Codigo curto que identifica o tipo de erro.
    cause : str or None, default=None
        Causa original do erro, quando aplicavel.
    """

    level: str
    message: str
    erro: str
    cause: str | None = None

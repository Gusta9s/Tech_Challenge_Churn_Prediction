from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Formato padronizado de resposta de erro para todos os cenarios 4xx/5xx
    da API: nivel de severidade, mensagem para o cliente, codigo do erro e
    causa (quando aplicavel).
    """

    level: str
    message: str
    erro: str
    cause: str | None = None

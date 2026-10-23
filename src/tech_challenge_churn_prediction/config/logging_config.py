import logging
import sys

from tech_challenge_churn_prediction.config.logging_settings import (
    LoggingSettingsFactory,
)

_logging_configurado = False


def configurar_logging() -> None:
    """Configura o logging da aplicacao de forma idempotente."""
    global _logging_configurado
    if _logging_configurado:
        return

    configuracoes = LoggingSettingsFactory.criar()
    logging.basicConfig(
        level=configuracoes.nivel,
        format=configuracoes.formato,
        stream=sys.stdout,
    )
    _logging_configurado = True


def obter_logger(nome: str) -> logging.Logger:
    """Retorna um logger ja configurado para o nome informado.

    Parameters
    ----------
    nome : str
        Nome do logger (geralmente `__name__` do modulo chamador).

    Returns
    -------
    logging.Logger
        Logger configurado com o nivel e formato centralizados.
    """
    configurar_logging()
    return logging.getLogger(nome)

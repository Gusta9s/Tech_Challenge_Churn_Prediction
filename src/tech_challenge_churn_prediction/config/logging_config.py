import logging
import sys

from tech_challenge_churn_prediction.config.logging_settings import (
    obter_logging_settings,
)

_logging_configurado = False


def configurar_logging() -> None:
    """Configura o logging da aplicacao uma unica vez (idempotente), usando
    o nivel e formato centralizados em LoggingSettings para todos os loggers
    obtidos via `obter_logger`.
    """
    global _logging_configurado
    if _logging_configurado:
        return

    configuracoes = obter_logging_settings()
    logging.basicConfig(
        level=configuracoes.nivel,
        format=configuracoes.formato,
        stream=sys.stdout,
    )
    _logging_configurado = True


def obter_logger(nome: str) -> logging.Logger:
    """Ponto unico de obtencao de logger, garantindo que a configuracao
    centralizada seja aplicada antes de qualquer uso.
    """
    configurar_logging()
    return logging.getLogger(nome)

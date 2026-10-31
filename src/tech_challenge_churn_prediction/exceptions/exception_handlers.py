import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from tech_challenge_churn_prediction.config.logging_config import obter_logger
from tech_challenge_churn_prediction.exceptions.app_exceptions import (
    ChurnPredictionAppException,
)
from tech_challenge_churn_prediction.schemas.error_response import (
    ErrorResponse,
)

_logger = obter_logger(__name__)


def registrar_exception_handlers(app: FastAPI) -> None:
    """Registra todos os exception handlers padronizados na aplicacao.

    Parameters
    ----------
    app : FastAPI
        Instancia da aplicacao onde os handlers serao registrados.
    """
    app.add_exception_handler(
        ChurnPredictionAppException, _tratar_excecao_de_dominio
    )
    app.add_exception_handler(
        RequestValidationError, _tratar_erro_de_validacao
    )
    app.add_exception_handler(Exception, _tratar_erro_inesperado)


async def _tratar_excecao_de_dominio(
    request: Request, exc: ChurnPredictionAppException
) -> JSONResponse:
    """Converte uma excecao de dominio na resposta de erro padronizada.

    Parameters
    ----------
    request : Request
        Requisicao HTTP que originou a excecao (nao utilizada).
    exc : ChurnPredictionAppException
        Excecao de dominio capturada.

    Returns
    -------
    JSONResponse
        Resposta no formato {level, message, erro, cause}.
    """
    nivel_log = logging.getLevelName(exc.level)
    _logger.log(
        nivel_log, "%s | erro=%s | cause=%s", exc.message, exc.erro, exc.cause
    )

    corpo = ErrorResponse(
        level=exc.level,
        message=exc.message,
        erro=exc.erro,
        cause=str(exc.cause) if exc.cause else None,
    )
    return JSONResponse(
        status_code=exc.status_code, content=corpo.model_dump()
    )


async def _tratar_erro_de_validacao(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Converte um erro de validacao do Pydantic em resposta padronizada.

    Parameters
    ----------
    request : Request
        Requisicao HTTP que originou o erro (nao utilizada).
    exc : RequestValidationError
        Erro de validacao do payload de entrada.

    Returns
    -------
    JSONResponse
        Resposta 422 no formato {level, message, erro, cause}.
    """
    _logger.warning("Payload de entrada invalido: %s", exc.errors())

    corpo = ErrorResponse(
        level="WARNING",
        message="O payload de entrada e invalido ou esta incompleto.",
        erro="PAYLOAD_INVALIDO",
        cause=str(exc.errors()),
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=corpo.model_dump(),
    )


async def _tratar_erro_inesperado(
    request: Request, exc: Exception
) -> JSONResponse:
    """Converte qualquer excecao nao mapeada em resposta padronizada.

    Parameters
    ----------
    request : Request
        Requisicao HTTP que originou a excecao (nao utilizada).
    exc : Exception
        Excecao inesperada capturada pelo handler global.

    Returns
    -------
    JSONResponse
        Resposta 500 no formato {level, message, erro, cause}.
    """
    _logger.error("Erro interno inesperado: %s", exc, exc_info=exc)

    corpo = ErrorResponse(
        level="ERROR",
        message="Ocorreu um erro interno inesperado.",
        erro="ERRO_INTERNO",
        cause=str(exc),
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=corpo.model_dump(),
    )

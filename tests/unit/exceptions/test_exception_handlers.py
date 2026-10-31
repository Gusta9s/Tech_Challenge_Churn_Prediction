import asyncio
import json

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from tech_challenge_churn_prediction.exceptions import (
    exception_handlers as alvo,
)
from tech_challenge_churn_prediction.exceptions.app_exceptions import (
    ChurnPredictionAppException,
    PredicaoException,
)


def _executar(corrotina):
    return asyncio.run(corrotina)


def _corpo_json(resposta):
    return json.loads(resposta.body)


def test_registrar_exception_handlers_registra_os_tres_handlers_esperados():
    """Registrar exception handlers registra os tres handlers esperados."""
    app = FastAPI()

    alvo.registrar_exception_handlers(app)

    assert (
        app.exception_handlers[ChurnPredictionAppException]
        is alvo._tratar_excecao_de_dominio
    )
    assert (
        app.exception_handlers[RequestValidationError]
        is alvo._tratar_erro_de_validacao
    )
    assert app.exception_handlers[Exception] is alvo._tratar_erro_inesperado


def test_tratar_excecao_de_dominio_com_causa_informada():
    """Tratar excecao de dominio com causa informada."""
    excecao = PredicaoException(cause=ValueError("falha interna"))

    resposta = _executar(alvo._tratar_excecao_de_dominio(None, excecao))

    assert resposta.status_code == 500
    corpo = _corpo_json(resposta)
    assert corpo["level"] == "ERROR"
    assert corpo["erro"] == "ERRO_PREDICAO"
    assert corpo["cause"] == "falha interna"


def test_tratar_excecao_de_dominio_sem_causa_informada():
    """Tratar excecao de dominio sem causa informada."""
    excecao = PredicaoException()

    resposta = _executar(alvo._tratar_excecao_de_dominio(None, excecao))

    corpo = _corpo_json(resposta)
    assert corpo["cause"] is None


def test_tratar_erro_de_validacao_retorna_422_com_detalhes_do_erro():
    """Tratar erro de validacao retorna 422 com detalhes do erro."""
    excecao = RequestValidationError(
        errors=[
            {"loc": ("body", "campo"), "msg": "obrigatorio", "type": "missing"}
        ]
    )

    resposta = _executar(alvo._tratar_erro_de_validacao(None, excecao))

    assert resposta.status_code == 422
    corpo = _corpo_json(resposta)
    assert corpo["erro"] == "PAYLOAD_INVALIDO"
    assert corpo["level"] == "WARNING"


def test_tratar_erro_inesperado_retorna_500_com_a_mensagem_da_excecao():
    """Tratar erro inesperado retorna 500 com a mensagem da excecao."""
    excecao = RuntimeError("explodiu")

    resposta = _executar(alvo._tratar_erro_inesperado(None, excecao))

    assert resposta.status_code == 500
    corpo = _corpo_json(resposta)
    assert corpo["erro"] == "ERRO_INTERNO"
    assert corpo["cause"] == "explodiu"

import pytest

from tech_challenge_churn_prediction.exceptions.app_exceptions import (
    ChurnPredictionAppException,
    ModeloNaoDisponivelException,
    PayloadInvalidoException,
    PredicaoException,
    PreProcessamentoException,
)


def test_excecao_base_guarda_todos_os_metadados_informados():
    causa = ValueError("detalhe")

    excecao = ChurnPredictionAppException(
        message="mensagem", erro="COD", status_code=418, level="WARNING", cause=causa
    )

    assert excecao.message == "mensagem"
    assert excecao.erro == "COD"
    assert excecao.status_code == 418
    assert excecao.level == "WARNING"
    assert excecao.cause is causa
    assert str(excecao) == "mensagem"


def test_excecao_base_usa_level_error_e_cause_none_por_padrao():
    excecao = ChurnPredictionAppException(message="mensagem", erro="COD", status_code=500)

    assert excecao.level == "ERROR"
    assert excecao.cause is None


@pytest.mark.parametrize(
    ("classe", "erro_esperado", "status_esperado", "level_esperado"),
    [
        (PayloadInvalidoException, "PAYLOAD_INVALIDO", 422, "WARNING"),
        (PreProcessamentoException, "ERRO_PRE_PROCESSAMENTO", 400, "WARNING"),
        (ModeloNaoDisponivelException, "MODELO_INDISPONIVEL", 503, "ERROR"),
        (PredicaoException, "ERRO_PREDICAO", 500, "ERROR"),
    ],
)
def test_subclasses_definem_metadados_fixos_e_propagam_a_causa(
    classe, erro_esperado, status_esperado, level_esperado
):
    causa = ValueError("falha")

    excecao = classe(cause=causa)

    assert excecao.erro == erro_esperado
    assert excecao.status_code == status_esperado
    assert excecao.level == level_esperado
    assert excecao.cause is causa


@pytest.mark.parametrize(
    "classe",
    [PayloadInvalidoException, PreProcessamentoException, ModeloNaoDisponivelException, PredicaoException],
)
def test_subclasses_aceitam_cause_padrao_none(classe):
    excecao = classe()

    assert excecao.cause is None

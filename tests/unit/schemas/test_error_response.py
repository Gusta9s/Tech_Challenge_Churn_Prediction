from tech_challenge_churn_prediction.schemas.error_response import ErrorResponse


def test_cria_resposta_de_erro_com_causa_informada():
    erro = ErrorResponse(level="ERROR", message="mensagem", erro="CODIGO", cause="detalhe")

    assert erro.cause == "detalhe"


def test_cria_resposta_de_erro_sem_causa_informada():
    erro = ErrorResponse(level="ERROR", message="mensagem", erro="CODIGO")

    assert erro.cause is None

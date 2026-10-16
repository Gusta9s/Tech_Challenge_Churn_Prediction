import logging

import pandas as pd

from tech_challenge_churn_prediction.schemas.churn_prediction_result import ChurnPredictionResult
from tech_challenge_churn_prediction.services.churn_prediction_logging_service import (
    ChurnPredictionLoggingService,
)


def test_registrar_entrada_mascara_os_campos_sensiveis_no_log(payload_valido, caplog):
    logger = logging.getLogger("teste.churn_prediction_logging.entrada")
    servico = ChurnPredictionLoggingService(logger)

    with caplog.at_level(logging.INFO, logger=logger.name):
        servico.registrar_entrada(payload_valido)

    assert "***" in caplog.text
    assert str(payload_valido.cobranca_mensal) not in caplog.text


def test_registrar_dados_transformados_loga_a_primeira_linha_do_dataframe(caplog):
    logger = logging.getLogger("teste.churn_prediction_logging.transformados")
    servico = ChurnPredictionLoggingService(logger)
    features = pd.DataFrame([{"cobranca_mensal": 10.0, "outra_coluna": 1.0}])

    with caplog.at_level(logging.INFO, logger=logger.name):
        servico.registrar_dados_transformados(features)

    assert "Dados transformados" in caplog.text


def test_registrar_resultado_predicao_loga_o_resultado_do_modelo(caplog):
    logger = logging.getLogger("teste.churn_prediction_logging.resultado")
    servico = ChurnPredictionLoggingService(logger)
    resultado = ChurnPredictionResult(churn_previsto=True, probabilidade_churn=0.9, probabilidade_nao_churn=0.1)

    with caplog.at_level(logging.INFO, logger=logger.name):
        servico.registrar_resultado_predicao(resultado)

    assert "Resultado da predicao" in caplog.text


def test_registrar_resposta_loga_o_payload_de_resposta(caplog):
    logger = logging.getLogger("teste.churn_prediction_logging.resposta")
    servico = ChurnPredictionLoggingService(logger)
    resultado = ChurnPredictionResult(churn_previsto=False, probabilidade_churn=0.1, probabilidade_nao_churn=0.9)

    with caplog.at_level(logging.INFO, logger=logger.name):
        servico.registrar_resposta(resultado)

    assert "Payload de resposta" in caplog.text

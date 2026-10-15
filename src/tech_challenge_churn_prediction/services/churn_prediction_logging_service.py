import logging

import pandas as pd

from tech_challenge_churn_prediction.schemas.churn_prediction_input import ChurnPredictionInput
from tech_challenge_churn_prediction.schemas.churn_prediction_result import ChurnPredictionResult
from tech_challenge_churn_prediction.utils.mascaramento_dados_sensiveis import mascarar_campos_sensiveis


class ChurnPredictionLoggingService:
    """Responsavel exclusivamente por registrar os eventos do ciclo de vida
    de uma requisicao de predicao: payload de entrada (mascarado), dados
    transformados, resultado do modelo e payload de resposta encaminhado.

    Apenas observa e loga o que as demais camadas produzem; nao participa
    do pre-processamento, da predicao ou da decisao de status HTTP,
    mantendo baixo acoplamento com a logica de negocio.
    """

    def __init__(self, logger: logging.Logger) -> None:
        self._logger = logger

    def registrar_entrada(self, payload: ChurnPredictionInput) -> None:
        payload_mascarado = mascarar_campos_sensiveis(payload.model_dump())
        self._logger.info("Payload de entrada recebido: %s", payload_mascarado)

    def registrar_dados_transformados(self, features: pd.DataFrame) -> None:
        features_mascaradas = mascarar_campos_sensiveis(features.iloc[0].to_dict())
        self._logger.info("Dados transformados para o modelo: %s", features_mascaradas)

    def registrar_resultado_predicao(self, resultado: ChurnPredictionResult) -> None:
        self._logger.info("Resultado da predicao do modelo: %s", resultado.model_dump())

    def registrar_resposta(self, resposta: ChurnPredictionResult) -> None:
        self._logger.info("Payload de resposta encaminhado: %s", resposta.model_dump())

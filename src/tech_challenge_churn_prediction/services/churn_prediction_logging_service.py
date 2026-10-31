import logging

import pandas as pd

from tech_challenge_churn_prediction.schemas.churn_prediction_input import (
    ChurnPredictionInput,
)
from tech_challenge_churn_prediction.schemas.churn_prediction_result import (
    ChurnPredictionResult,
)
from tech_challenge_churn_prediction.utils.mascaramento_dados_sensiveis import (  # noqa: E501
    mascarar_campos_sensiveis,
)


class ChurnPredictionLoggingService:
    """Registra os eventos do ciclo de vida de uma requisicao de predicao.

    Apenas observa e loga o que as demais camadas produzem; nao
    participa do pre-processamento, da predicao ou da decisao de
    status HTTP, mantendo baixo acoplamento com a logica de negocio.
    """

    def __init__(self, logger: logging.Logger) -> None:
        """Armazena o logger usado para registrar os eventos.

        Parameters
        ----------
        logger : logging.Logger
            Logger ja configurado a ser usado nos registros.
        """
        self._logger = logger

    def registrar_entrada(self, payload: ChurnPredictionInput) -> None:
        """Loga o payload de entrada com os campos sensiveis mascarados.

        Parameters
        ----------
        payload : ChurnPredictionInput
            Payload recebido na requisicao de predicao.
        """
        payload_mascarado = mascarar_campos_sensiveis(payload.model_dump())
        self._logger.info("Payload de entrada recebido: %s", payload_mascarado)

    def registrar_dados_transformados(self, features: pd.DataFrame) -> None:
        """Loga a primeira linha das features ja transformadas.

        Parameters
        ----------
        features : pandas.DataFrame
            Features geradas pelo pre-processamento.
        """
        features_mascaradas = mascarar_campos_sensiveis(
            features.iloc[0].to_dict()
        )
        self._logger.info(
            "Dados transformados para o modelo: %s", features_mascaradas
        )

    def registrar_resultado_predicao(
        self, resultado: ChurnPredictionResult
    ) -> None:
        """Loga o resultado bruto produzido pelo modelo.

        Parameters
        ----------
        resultado : ChurnPredictionResult
            Resultado da predicao antes de ser devolvido ao cliente.
        """
        self._logger.info(
            "Resultado da predicao do modelo: %s", resultado.model_dump()
        )

    def registrar_resposta(self, resposta: ChurnPredictionResult) -> None:
        """Loga o payload de resposta encaminhado ao cliente.

        Parameters
        ----------
        resposta : ChurnPredictionResult
            Resposta final devolvida pela API.
        """
        self._logger.info(
            "Payload de resposta encaminhado: %s", resposta.model_dump()
        )

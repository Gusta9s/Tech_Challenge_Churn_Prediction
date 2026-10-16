from fastapi import APIRouter, Depends

from tech_challenge_churn_prediction.controllers.dependencies import (
    obter_model_loader_service,
    obter_prediction_logging_service,
    obter_prediction_service,
    obter_preprocessing_service,
)
from tech_challenge_churn_prediction.exceptions.app_exceptions import (
    PredicaoException,
    PreProcessamentoException,
)
from tech_challenge_churn_prediction.schemas.churn_prediction_input import (
    ChurnPredictionInput,
)
from tech_challenge_churn_prediction.schemas.churn_prediction_result import (
    ChurnPredictionResult,
)
from tech_challenge_churn_prediction.services.churn_prediction_logging_service import (  # noqa: E501
    ChurnPredictionLoggingService,
)
from tech_challenge_churn_prediction.services.churn_prediction_service import (
    ChurnPredictionService,
)
from tech_challenge_churn_prediction.services.churn_preprocessing_service import (  # noqa: E501
    ChurnPreprocessingService,
)
from tech_challenge_churn_prediction.services.model_loader_service import (
    ModelLoaderService,
)

router = APIRouter(prefix="/predict", tags=["predict"])


@router.post("", response_model=ChurnPredictionResult, status_code=200)
def prever_churn(
    payload: ChurnPredictionInput,
    preprocessing_service: ChurnPreprocessingService = Depends(
        obter_preprocessing_service
    ),
    model_loader_service: ModelLoaderService = Depends(
        obter_model_loader_service
    ),
    prediction_service: ChurnPredictionService = Depends(
        obter_prediction_service
    ),
    logging_service: ChurnPredictionLoggingService = Depends(
        obter_prediction_logging_service
    ),
) -> ChurnPredictionResult:
    logging_service.registrar_entrada(payload)

    try:
        features = preprocessing_service.transformar(payload)
    except Exception as erro:
        raise PreProcessamentoException(cause=erro) from erro
    logging_service.registrar_dados_transformados(features)

    try:
        modelo = model_loader_service.carregar()
        resultado = prediction_service.prever(modelo, features)
    except Exception as erro:
        raise PredicaoException(cause=erro) from erro
    logging_service.registrar_resultado_predicao(resultado)

    logging_service.registrar_resposta(resultado)
    return resultado

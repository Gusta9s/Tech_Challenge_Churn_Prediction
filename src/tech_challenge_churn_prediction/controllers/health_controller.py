from fastapi import APIRouter, Depends

from tech_challenge_churn_prediction.controllers.dependencies import (
    HealthCheckServiceFactory,
)
from tech_challenge_churn_prediction.schemas.health_status import HealthStatus
from tech_challenge_churn_prediction.services.health_check_service import (
    HealthCheckService,
)

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/liveness", response_model=HealthStatus, status_code=200)
def verificar_liveness() -> HealthStatus:
    """Endpoint de liveness: confirma que o processo esta ativo.

    Returns
    -------
    HealthStatus
        Status "UP".
    """
    HealthCheckService.verificar_liveness()
    return HealthStatus(status="UP")


@router.get("/readiness", response_model=HealthStatus, status_code=200)
def verificar_readiness(
    health_check_service: HealthCheckService = Depends(
        HealthCheckServiceFactory.criar
    ),
) -> HealthStatus:
    """Endpoint de readiness: confirma que o modelo esta carregado.

    Parameters
    ----------
    health_check_service : HealthCheckService
        Servico injetado responsavel por verificar as dependencias.

    Returns
    -------
    HealthStatus
        Status "UP".

    Raises
    ------
    ModeloNaoDisponivelException
        Se o modelo nao puder ser carregado (resulta em 503).
    """
    health_check_service.verificar_readiness()
    return HealthStatus(status="UP")

from fastapi import APIRouter, Depends

from tech_challenge_churn_prediction.controllers.dependencies import obter_health_check_service
from tech_challenge_churn_prediction.schemas.health_status import HealthStatus
from tech_challenge_churn_prediction.services.health_check_service import HealthCheckService

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/liveness", response_model=HealthStatus, status_code=200)
def verificar_liveness() -> HealthStatus:
    HealthCheckService.verificar_liveness()
    return HealthStatus(status="UP")


@router.get("/readiness", response_model=HealthStatus, status_code=200)
def verificar_readiness(
    health_check_service: HealthCheckService = Depends(obter_health_check_service),
) -> HealthStatus:
    health_check_service.verificar_readiness()
    return HealthStatus(status="UP")

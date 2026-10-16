from fastapi import FastAPI

from tech_challenge_churn_prediction.config.app_settings import (
    obter_app_settings,
)
from tech_challenge_churn_prediction.config.logging_config import (
    configurar_logging,
)
from tech_challenge_churn_prediction.controllers.health_controller import (
    router as health_router,
)
from tech_challenge_churn_prediction.controllers.prediction_controller import (
    router as prediction_router,
)
from tech_challenge_churn_prediction.exceptions.exception_handlers import (
    registrar_exception_handlers,
)


def criar_app() -> FastAPI:
    """Monta a aplicacao FastAPI: configura logging, registra os routers de
    cada controller e centraliza o tratamento de excecoes.
    """
    configurar_logging()

    configuracoes_app = obter_app_settings()
    app = FastAPI(
        title=configuracoes_app.titulo, version=configuracoes_app.versao
    )
    app.include_router(health_router)
    app.include_router(prediction_router)
    registrar_exception_handlers(app)

    return app


app = criar_app()

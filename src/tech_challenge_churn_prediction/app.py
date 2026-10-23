from fastapi import FastAPI

from tech_challenge_churn_prediction.config.app_settings import (
    AppSettingsFactory,
)
from tech_challenge_churn_prediction.config.logging_config import (
    configurar_logging,
)
from tech_challenge_churn_prediction.config.rate_limit_settings import (
    RateLimitSettingsFactory,
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
from tech_challenge_churn_prediction.middlewares.cors_middleware import (
    configurar_cors,
)
from tech_challenge_churn_prediction.middlewares.rate_limit_middleware import (
    RateLimitMiddleware,
)
from tech_challenge_churn_prediction.services.rate_limiter_service import (
    RateLimiterServiceFactory,
)


class AppFactory:
    """Fabrica responsavel por montar a aplicacao FastAPI completa."""

    @staticmethod
    def criar() -> FastAPI:
        """Monta a aplicacao FastAPI com routers, middlewares e handlers.

        Returns
        -------
        FastAPI
            Aplicacao pronta para ser servida pelo uvicorn.
        """
        configurar_logging()

        configuracoes_app = AppSettingsFactory.criar()
        app = FastAPI(
            title=configuracoes_app.titulo, version=configuracoes_app.versao
        )
        app.include_router(health_router)
        app.include_router(prediction_router)
        registrar_exception_handlers(app)

        configuracoes_rate_limit = RateLimitSettingsFactory.criar()
        app.add_middleware(
            RateLimitMiddleware,
            rate_limiter_service=RateLimiterServiceFactory.criar(),
            cabecalho_requisicoes_restantes=(
                configuracoes_rate_limit.cabecalho_requisicoes_restantes
            ),
        )
        # Registrado por ultimo para ficar na camada mais externa,
        # garantindo que os cabecalhos de CORS sejam aplicados mesmo em
        # respostas 429 geradas pelo RateLimitMiddleware.
        configurar_cors(app)

        return app


app = AppFactory.criar()

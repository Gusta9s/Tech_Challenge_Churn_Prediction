from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tech_challenge_churn_prediction.config.cors_settings import (
    obter_cors_settings,
)


def configurar_cors(app: FastAPI) -> None:
    """Registra o CORSMiddleware com a politica configurada via ambiente.

    Reaproveita a implementacao oficial do Starlette/FastAPI (em vez de
    reimplementar a validacao de CORS); origens, metodos, cabecalhos e
    a permissao de credenciais sao lidos de CorsSettings, sem valores
    fixos no codigo-fonte.

    Parameters
    ----------
    app : FastAPI
        Instancia da aplicacao onde o middleware sera registrado.
    """
    configuracoes_cors = obter_cors_settings()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(configuracoes_cors.origens_permitidas),
        allow_methods=list(configuracoes_cors.metodos_permitidos),
        allow_headers=list(configuracoes_cors.cabecalhos_permitidos),
        allow_credentials=configuracoes_cors.permitir_credenciais,
    )

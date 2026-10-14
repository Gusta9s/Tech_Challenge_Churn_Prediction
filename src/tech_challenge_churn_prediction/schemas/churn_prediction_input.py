from typing import Literal

from pydantic import BaseModel, Field


class ChurnPredictionInput(BaseModel):
    """Payload de uma unica requisicao de predicao de churn.

    Os campos correspondem aos dados brutos de um cliente (equivalentes ao
    dataset de treinamento, antes das transformacoes de pre-processamento).
    Campos sem poder preditivo e descartados no treinamento (id do cliente,
    genero, dependentes) nao fazem parte do payload.
    """

    cliente_em_idade_avancada: Literal[0, 1] = Field(
        ..., description="Indica se o cliente e idoso (1) ou nao (0)."
    )
    casado: Literal["Yes", "No"] = Field(..., description="Possui conjuge.")
    meses_como_cliente: int = Field(..., ge=0, description="Tempo de permanencia em meses.")
    possui_servico_telefonico: Literal["Yes", "No"]
    possui_multiplas_linhas: Literal["Yes", "No", "No phone service"]
    possui_servico_de_internet: Literal["DSL", "Fiber optic", "No"]
    possui_seguranca_online: Literal["Yes", "No", "No internet service"]
    possui_backup_online: Literal["Yes", "No", "No internet service"]
    possui_protecao_dispositivo: Literal["Yes", "No", "No internet service"]
    possui_suporte_tecnico_premium: Literal["Yes", "No", "No internet service"]
    possui_streaming_tv_terceiros: Literal["Yes", "No", "No internet service"]
    possui_streaming_filmes_terceiros: Literal["Yes", "No", "No internet service"]
    tipo_contrato: Literal["Month-to-month", "One year", "Two year"]
    fatura_sem_papel: Literal["Yes", "No"]
    metodo_pagamento: Literal[
        "Mailed check",
        "Electronic check",
        "Bank transfer (automatic)",
        "Credit card (automatic)",
    ]
    cobranca_mensal: float = Field(..., ge=0, description="Valor da cobranca mensal.")
    total_cobrado_durante_trimestre: float = Field(
        ..., ge=0, description="Valor total cobrado no trimestre."
    )

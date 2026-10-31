import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

from tech_challenge_churn_prediction.schemas.churn_prediction_input import (
    ChurnPredictionInput,
)
from tech_challenge_churn_prediction.utils.constantes_modelo import (
    CATEGORIAS_BINARIAS_SIMPLES,
    CATEGORIAS_METODO_PAGAMENTO,
    CATEGORIAS_SERVICO_DE_INTERNET,
    CATEGORIAS_TIPO_CONTRATO,
    COLUNAS_ADDONS,
    ORDEM_FEATURES_RANDOM_FOREST,
)
from tech_challenge_churn_prediction.utils.mapeamento_categorico import (
    MAPA_BINARIO_COM_AUSENCIA_DE_SERVICO,
)
from tech_challenge_churn_prediction.utils.transformadores_sklearn import (
    ContadorAddonsTransformer,
    MapeadorBinarioTransformer,
)


class ChurnPreprocessingService:
    """Transforma o payload de predicao nas features do modelo campeao.

    Todas as regras de transformacao sao centralizadas em um unico
    `sklearn.pipeline.Pipeline` (um `ColumnTransformer` com um encoder/
    transformer dedicado por grupo de colunas). O pipeline e stateless:
    os encoders recebem categorias explicitas (nao aprendidas de
    dados), entao pode ser reaproveitado em qualquer requisicao sem
    retreinar nada alem da propria validacao de schema.
    """

    def __init__(self) -> None:
        """Constroi e armazena o pipeline de pre-processamento."""
        self._pipeline = self._construir_pipeline()

    def transformar(self, payload: ChurnPredictionInput) -> pd.DataFrame:
        """Transforma o payload de entrada nas features do modelo.

        Parameters
        ----------
        payload : ChurnPredictionInput
            Dados brutos de um cliente.

        Returns
        -------
        pandas.DataFrame
            Features codificadas, na ordem esperada pelo modelo.
        """
        dados_brutos = pd.DataFrame([payload.model_dump()])
        features_transformadas = self._pipeline.fit_transform(dados_brutos)
        return pd.DataFrame(
            features_transformadas, columns=list(ORDEM_FEATURES_RANDOM_FOREST)
        )

    @staticmethod
    def _construir_pipeline() -> Pipeline:
        """Monta o pipeline de pre-processamento com encoders explicitos.

        Returns
        -------
        sklearn.pipeline.Pipeline
            Pipeline stateless pronto para transformar um payload.
        """
        codificador_features = ColumnTransformer(
            transformers=[
                (
                    "idade_avancada",
                    "passthrough",
                    ["cliente_em_idade_avancada"],
                ),
                (
                    "casado",
                    OrdinalEncoder(
                        categories=[list(CATEGORIAS_BINARIAS_SIMPLES)]
                    ),
                    ["casado"],
                ),
                ("meses_como_cliente", "passthrough", ["meses_como_cliente"]),
                (
                    "servico_telefonico",
                    OrdinalEncoder(
                        categories=[list(CATEGORIAS_BINARIAS_SIMPLES)]
                    ),
                    ["possui_servico_telefonico"],
                ),
                (
                    "multiplas_linhas",
                    MapeadorBinarioTransformer(
                        MAPA_BINARIO_COM_AUSENCIA_DE_SERVICO
                    ),
                    ["possui_multiplas_linhas"],
                ),
                (
                    "addons_binarizados",
                    MapeadorBinarioTransformer(
                        MAPA_BINARIO_COM_AUSENCIA_DE_SERVICO
                    ),
                    list(COLUNAS_ADDONS),
                ),
                (
                    "tipo_contrato",
                    OrdinalEncoder(
                        categories=[list(CATEGORIAS_TIPO_CONTRATO)]
                    ),
                    ["tipo_contrato"],
                ),
                (
                    "fatura_sem_papel",
                    OrdinalEncoder(
                        categories=[list(CATEGORIAS_BINARIAS_SIMPLES)]
                    ),
                    ["fatura_sem_papel"],
                ),
                ("cobranca_mensal", "passthrough", ["cobranca_mensal"]),
                (
                    "total_cobrado_durante_trimestre",
                    "passthrough",
                    ["total_cobrado_durante_trimestre"],
                ),
                (
                    "servico_de_internet",
                    OneHotEncoder(
                        categories=[list(CATEGORIAS_SERVICO_DE_INTERNET)],
                        sparse_output=False,
                    ),
                    ["possui_servico_de_internet"],
                ),
                (
                    "metodo_pagamento",
                    OneHotEncoder(
                        categories=[list(CATEGORIAS_METODO_PAGAMENTO)],
                        sparse_output=False,
                    ),
                    ["metodo_pagamento"],
                ),
                (
                    "quantidade_de_addons",
                    ContadorAddonsTransformer(
                        MAPA_BINARIO_COM_AUSENCIA_DE_SERVICO
                    ),
                    list(COLUNAS_ADDONS),
                ),
            ],
        )
        return Pipeline(steps=[("codificador_features", codificador_features)])

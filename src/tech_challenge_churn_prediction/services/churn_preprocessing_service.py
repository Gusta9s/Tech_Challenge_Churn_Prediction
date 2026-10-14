import pandas as pd

from tech_challenge_churn_prediction.schemas.churn_prediction_input import ChurnPredictionInput
from tech_challenge_churn_prediction.utils.constantes_modelo import (
    COLUNAS_ADDONS,
    COLUNAS_METODO_PAGAMENTO,
    COLUNAS_SERVICO_DE_INTERNET,
    ORDEM_FEATURES_RANDOM_FOREST,
)
from tech_challenge_churn_prediction.utils.mapeamento_categorico import (
    MAPA_BINARIO_COM_AUSENCIA_DE_SERVICO,
    MAPA_BINARIO_SIMPLES,
    MAPA_CODIGO_METODO_PAGAMENTO,
    MAPA_CODIGO_SERVICO_DE_INTERNET,
    MAPA_TIPO_CONTRATO,
    mapear_valor_binario,
)


class ChurnPreprocessingService:
    """Responsavel exclusivamente por transformar o payload de uma unica
    requisicao de predicao nas features esperadas pelo modelo campeao
    (Random Forest), replicando as transformacoes aplicadas no treinamento
    (ver notebooks/arvore_de_descisao/modelo_final/V6-Validacao_cruzada_k_fold_random_forest.ipynb).
    """

    def transformar(self, payload: ChurnPredictionInput) -> pd.DataFrame:
        linha = self._mapear_campos_binarios(payload)
        linha |= self._codificar_servico_de_internet(payload.possui_servico_de_internet)
        linha |= self._codificar_metodo_pagamento(payload.metodo_pagamento)
        linha["quantidade_de_addons"] = sum(linha[coluna] for coluna in COLUNAS_ADDONS)

        dataframe = pd.DataFrame([linha])
        return dataframe[list(ORDEM_FEATURES_RANDOM_FOREST)]

    @staticmethod
    def _mapear_campos_binarios(payload: ChurnPredictionInput) -> dict:
        return {
            "cliente_em_idade_avancada": int(payload.cliente_em_idade_avancada),
            "casado": mapear_valor_binario(payload.casado, MAPA_BINARIO_SIMPLES),
            "meses_como_cliente": payload.meses_como_cliente,
            "possui_servico_telefonico": mapear_valor_binario(
                payload.possui_servico_telefonico, MAPA_BINARIO_SIMPLES
            ),
            "possui_multiplas_linhas": mapear_valor_binario(
                payload.possui_multiplas_linhas, MAPA_BINARIO_COM_AUSENCIA_DE_SERVICO
            ),
            "possui_seguranca_online": mapear_valor_binario(
                payload.possui_seguranca_online, MAPA_BINARIO_COM_AUSENCIA_DE_SERVICO
            ),
            "possui_backup_online": mapear_valor_binario(
                payload.possui_backup_online, MAPA_BINARIO_COM_AUSENCIA_DE_SERVICO
            ),
            "possui_protecao_dispositivo": mapear_valor_binario(
                payload.possui_protecao_dispositivo, MAPA_BINARIO_COM_AUSENCIA_DE_SERVICO
            ),
            "possui_suporte_tecnico_premium": mapear_valor_binario(
                payload.possui_suporte_tecnico_premium, MAPA_BINARIO_COM_AUSENCIA_DE_SERVICO
            ),
            "possui_streaming_tv_terceiros": mapear_valor_binario(
                payload.possui_streaming_tv_terceiros, MAPA_BINARIO_COM_AUSENCIA_DE_SERVICO
            ),
            "possui_streaming_filmes_terceiros": mapear_valor_binario(
                payload.possui_streaming_filmes_terceiros, MAPA_BINARIO_COM_AUSENCIA_DE_SERVICO
            ),
            "tipo_contrato": MAPA_TIPO_CONTRATO[payload.tipo_contrato],
            "fatura_sem_papel": mapear_valor_binario(payload.fatura_sem_papel, MAPA_BINARIO_SIMPLES),
            "cobranca_mensal": payload.cobranca_mensal,
            "total_cobrado_durante_trimestre": payload.total_cobrado_durante_trimestre,
        }

    @staticmethod
    def _codificar_servico_de_internet(valor: str) -> dict:
        codigo = MAPA_CODIGO_SERVICO_DE_INTERNET[valor]
        return {coluna: int(coluna.endswith(codigo)) for coluna in COLUNAS_SERVICO_DE_INTERNET}

    @staticmethod
    def _codificar_metodo_pagamento(valor: str) -> dict:
        codigo = MAPA_CODIGO_METODO_PAGAMENTO[valor]
        return {coluna: int(coluna.endswith(codigo)) for coluna in COLUNAS_METODO_PAGAMENTO}

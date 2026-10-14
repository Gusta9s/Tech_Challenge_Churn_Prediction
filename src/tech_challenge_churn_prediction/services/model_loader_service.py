from pathlib import Path

import joblib
from sklearn.base import BaseEstimator

from tech_challenge_churn_prediction.utils.caminho_projeto import encontrar_raiz_projeto
from tech_challenge_churn_prediction.utils.versionamento_modelo import (
    encontrar_diretorio_versao_mais_recente,
)

NOME_ARQUIVO_MODELO_CAMPEAO = "random_forest.joblib"


class ModelLoaderService:
    """Responsavel exclusivamente por carregar o artefato do modelo treinado (.joblib).

    A versao do modelo e resolvida dinamicamente (maior versao semantica
    disponivel em `models/`), nao conhece nada sobre pre-processamento ou
    predicao, apenas entrega um estimador sklearn pronto para uso, mantendo
    o carregamento desacoplado do restante do fluxo de inferencia.
    """

    def __init__(self, caminho_modelo: Path | None = None) -> None:
        self._caminho_modelo = caminho_modelo or self._resolver_caminho_modelo_campeao()
        self._modelo: BaseEstimator | None = None

    @staticmethod
    def _resolver_caminho_modelo_campeao() -> Path:
        diretorio_modelos = encontrar_raiz_projeto() / "models"
        diretorio_versao_mais_recente = encontrar_diretorio_versao_mais_recente(diretorio_modelos)
        return diretorio_versao_mais_recente / NOME_ARQUIVO_MODELO_CAMPEAO

    def carregar(self) -> BaseEstimator:
        """Carrega o modelo uma unica vez e reutiliza a instancia em memoria
        nas chamadas subsequentes (evita custo de I/O repetido por requisicao).
        """
        if self._modelo is None:
            if not self._caminho_modelo.exists():
                raise FileNotFoundError(f"Modelo nao encontrado em: {self._caminho_modelo}")
            self._modelo = joblib.load(self._caminho_modelo)
        return self._modelo

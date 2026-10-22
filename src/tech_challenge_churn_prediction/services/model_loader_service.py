from pathlib import Path

import joblib
from sklearn.base import BaseEstimator

from tech_challenge_churn_prediction.config.model_settings import (
    obter_model_settings,
)
from tech_challenge_churn_prediction.utils.caminho_projeto import (
    encontrar_raiz_projeto,
)
from tech_challenge_churn_prediction.utils.versionamento_modelo import (
    encontrar_diretorio_versao_mais_recente,
)


class ModelLoaderService:
    """Carrega o artefato do modelo campeao treinado (.joblib).

    A versao do modelo e resolvida dinamicamente (maior versao
    semantica disponivel em `ModelSettings.diretorio_modelos`), nao
    conhece nada sobre pre-processamento ou predicao, apenas entrega um
    estimador sklearn pronto para uso.
    """

    def __init__(self, caminho_modelo: Path | None = None) -> None:
        """Resolve o caminho do modelo a carregar.

        Parameters
        ----------
        caminho_modelo : pathlib.Path or None, default=None
            Caminho explicito do artefato `.joblib`. Se None, resolve
            dinamicamente a versao mais recente em `ModelSettings`.
        """
        self._caminho_modelo = (
            caminho_modelo or self._resolver_caminho_modelo_campeao()
        )
        self._modelo: BaseEstimator | None = None

    @staticmethod
    def _resolver_caminho_modelo_campeao() -> Path:
        """Resolve dinamicamente o caminho do artefato do modelo campeao.

        Returns
        -------
        pathlib.Path
            Caminho do arquivo `.joblib` da versao mais recente.
        """
        configuracoes_modelo = obter_model_settings()
        diretorio_modelos = (
            encontrar_raiz_projeto() / configuracoes_modelo.diretorio_modelos
        )
        diretorio_versao_mais_recente = (
            encontrar_diretorio_versao_mais_recente(diretorio_modelos)
        )
        return (
            diretorio_versao_mais_recente
            / configuracoes_modelo.nome_arquivo_modelo
        )

    def carregar(self) -> BaseEstimator:
        """Carrega o modelo, reutilizando a instancia a partir do cache.

        Returns
        -------
        sklearn.base.BaseEstimator
            Estimador treinado, pronto para predicao.

        Raises
        ------
        FileNotFoundError
            Se o arquivo do modelo nao existir no caminho resolvido.
        """
        if self._modelo is None:
            if not self._caminho_modelo.exists():
                raise FileNotFoundError(
                    f"Modelo nao encontrado em: {self._caminho_modelo}"
                )
            self._modelo = joblib.load(self._caminho_modelo)
        return self._modelo

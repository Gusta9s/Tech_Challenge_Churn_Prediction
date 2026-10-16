import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class MapeadorBinarioTransformer(BaseEstimator, TransformerMixin):
    """Transformer sklearn stateless que aplica um mapeamento categorico fixo
    (ex.: "Yes"/"No"/"No internet service" -> 1/0/0) a uma ou mais colunas.

    Nao depende de dados de treinamento: o mapeamento e uma regra de dominio
    conhecida a priori, por isso `fit` e um no-op.
    """

    def __init__(self, mapa: dict[str, int]):
        self.mapa = mapa

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        mapear = np.vectorize(self.mapa.__getitem__)
        return mapear(np.asarray(X, dtype=object)).astype(float)

    def get_feature_names_out(self, input_features=None):
        return np.asarray(input_features)


class ContadorAddonsTransformer(BaseEstimator, TransformerMixin):
    """Transformer sklearn stateless que conta quantos addons (colunas
    binarias Yes/No/No internet service) um cliente possui, somando os
    valores binarizados das colunas informadas em uma unica coluna de saida.
    """

    def __init__(self, mapa: dict[str, int]):
        self.mapa = mapa

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        mapear = np.vectorize(self.mapa.__getitem__)
        binarizado = mapear(np.asarray(X, dtype=object)).astype(float)
        return binarizado.sum(axis=1, keepdims=True)

    def get_feature_names_out(self, input_features=None):
        return np.asarray(["quantidade_de_addons"])

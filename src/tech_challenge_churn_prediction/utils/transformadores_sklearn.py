import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class MapeadorBinarioTransformer(BaseEstimator, TransformerMixin):
    """Aplica um mapeamento categorico fixo a uma ou mais colunas.

    Nao depende de dados de treinamento: o mapeamento e uma regra de
    dominio conhecida a priori (ex.: "Yes"/"No"/"No internet service"
    -> 1/0/0), por isso `fit` e um no-op.

    Attributes
    ----------
    mapa : dict[str, int]
        Mapeamento fixo de categoria para valor binario.
    """

    def __init__(self, mapa: dict[str, int]):
        """Armazena o mapeamento categorico a ser aplicado.

        Parameters
        ----------
        mapa : dict[str, int]
            Mapeamento fixo de categoria para valor binario.
        """
        self.mapa = mapa

    def fit(self, X, y=None):
        """Nao realiza nenhum aprendizado, apenas satisfaz a API sklearn.

        Parameters
        ----------
        X : array-like
            Dados de entrada, ignorados.
        y : array-like or None, default=None
            Alvo, ignorado.

        Returns
        -------
        MapeadorBinarioTransformer
            A propria instancia.
        """
        return self

    def transform(self, X):
        """Aplica o mapeamento categorico elemento a elemento.

        Parameters
        ----------
        X : array-like
            Matriz de valores categoricos a serem mapeados.

        Returns
        -------
        numpy.ndarray
            Matriz de valores binarios, com o mesmo formato de `X`.
        """
        mapear = np.vectorize(self.mapa.__getitem__)
        return mapear(np.asarray(X, dtype=object)).astype(float)

    def get_feature_names_out(self, input_features=None):
        """Retorna os nomes de saida, iguais aos nomes de entrada.

        Parameters
        ----------
        input_features : array-like or None, default=None
            Nomes das colunas de entrada.

        Returns
        -------
        numpy.ndarray
            Os mesmos nomes recebidos em `input_features`.
        """
        return np.asarray(input_features)


class ContadorAddonsTransformer(BaseEstimator, TransformerMixin):
    """Conta quantos addons binarios um cliente possui contratados.

    Soma os valores binarizados das colunas informadas (ex.:
    seguranca online, backup online) em uma unica coluna de saida.

    Attributes
    ----------
    mapa : dict[str, int]
        Mapeamento fixo de categoria para valor binario.
    """

    def __init__(self, mapa: dict[str, int]):
        """Armazena o mapeamento categorico usado na binarizacao.

        Parameters
        ----------
        mapa : dict[str, int]
            Mapeamento fixo de categoria para valor binario.
        """
        self.mapa = mapa

    def fit(self, X, y=None):
        """Nao realiza nenhum aprendizado, apenas satisfaz a API sklearn.

        Parameters
        ----------
        X : array-like
            Dados de entrada, ignorados.
        y : array-like or None, default=None
            Alvo, ignorado.

        Returns
        -------
        ContadorAddonsTransformer
            A propria instancia.
        """
        return self

    def transform(self, X):
        """Soma os valores binarizados das colunas de addons.

        Parameters
        ----------
        X : array-like
            Matriz de colunas categoricas de addons.

        Returns
        -------
        numpy.ndarray
            Vetor coluna com a quantidade de addons por linha.
        """
        mapear = np.vectorize(self.mapa.__getitem__)
        binarizado = mapear(np.asarray(X, dtype=object)).astype(float)
        return binarizado.sum(axis=1, keepdims=True)

    def get_feature_names_out(self, input_features=None):
        """Retorna o nome fixo da coluna de saida gerada.

        Parameters
        ----------
        input_features : array-like or None, default=None
            Nomes das colunas de entrada, ignorados.

        Returns
        -------
        numpy.ndarray
            Array contendo apenas "quantidade_de_addons".
        """
        return np.asarray(["quantidade_de_addons"])

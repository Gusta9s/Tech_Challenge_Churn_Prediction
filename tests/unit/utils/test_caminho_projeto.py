import pytest

from tech_challenge_churn_prediction.utils.caminho_projeto import encontrar_raiz_projeto


def test_encontra_a_raiz_do_projeto_a_partir_do_diretorio_atual():
    raiz = encontrar_raiz_projeto()

    assert (raiz / "pyproject.toml").exists()


def test_levanta_erro_quando_o_marcador_nao_existe_em_nenhum_diretorio_pai():
    with pytest.raises(FileNotFoundError):
        encontrar_raiz_projeto(marcador="arquivo-marcador-que-nunca-existira.inexistente")

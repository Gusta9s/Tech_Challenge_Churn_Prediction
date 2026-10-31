import pytest

from tech_challenge_churn_prediction.utils.versionamento_modelo import (
    encontrar_diretorio_versao_mais_recente,
)


def _criar_versao(diretorio_base, nome_versao, com_joblib=True):
    diretorio_versao = diretorio_base / nome_versao
    diretorio_versao.mkdir()
    if com_joblib:
        (diretorio_versao / "modelo.joblib").touch()
    return diretorio_versao


def test_encontra_a_versao_mais_recente_entre_varios_diretorios_validos(
    tmp_path,
):
    """Encontra a versao mais recente entre varios diretorios validos."""
    _criar_versao(tmp_path, "v1.0.0")
    versao_mais_recente = _criar_versao(tmp_path, "v1.0.2")
    _criar_versao(tmp_path, "v1.0.1")

    resultado = encontrar_diretorio_versao_mais_recente(tmp_path)

    assert resultado == versao_mais_recente


def test_ignora_entradas_que_nao_sao_diretorios(tmp_path):
    """Ignora entradas que nao sao diretorios."""
    (tmp_path / "arquivo_solto.txt").touch()
    versao_valida = _criar_versao(tmp_path, "v1.0.0")

    resultado = encontrar_diretorio_versao_mais_recente(tmp_path)

    assert resultado == versao_valida


def test_ignora_diretorios_que_nao_seguem_o_padrao_de_versao(tmp_path):
    """Ignora diretorios que nao seguem o padrao de versao."""
    (tmp_path / "rascunho").mkdir()
    ((tmp_path / "rascunho") / "modelo.joblib").touch()
    versao_valida = _criar_versao(tmp_path, "v1.0.0")

    resultado = encontrar_diretorio_versao_mais_recente(tmp_path)

    assert resultado == versao_valida


def test_ignora_diretorios_de_versao_sem_artefato_joblib(tmp_path):
    """Ignora diretorios de versao sem artefato joblib."""
    _criar_versao(tmp_path, "v1.0.1", com_joblib=False)
    versao_valida = _criar_versao(tmp_path, "v1.0.0")

    resultado = encontrar_diretorio_versao_mais_recente(tmp_path)

    assert resultado == versao_valida


def test_levanta_erro_quando_nenhuma_versao_valida_e_encontrada(tmp_path):
    """Levanta erro quando nenhuma versao valida e encontrada."""
    with pytest.raises(FileNotFoundError):
        encontrar_diretorio_versao_mais_recente(tmp_path)

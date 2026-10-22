import pytest

from tech_challenge_churn_prediction.services import (
    model_loader_service as alvo,
)
from tech_challenge_churn_prediction.services.model_loader_service import (
    ModelLoaderService,
)


class ConfiguracoesModeloFalsas:
    diretorio_modelos = "models"
    nome_arquivo_modelo = "modelo-falso.joblib"


def test_carregar_levanta_erro_quando_o_arquivo_do_modelo_nao_existe(tmp_path):
    """Carregar levanta erro quando o arquivo do modelo nao existe."""
    caminho_inexistente = tmp_path / "nao_existe.joblib"
    servico = ModelLoaderService(caminho_modelo=caminho_inexistente)

    with pytest.raises(FileNotFoundError):
        servico.carregar()


def test_carregar_retorna_o_modelo_e_reutiliza_a_instancia_em_cache(
    tmp_path, mocker
):
    """Carregar retorna o modelo e reutiliza a instancia em cache."""
    caminho_modelo = tmp_path / "modelo.joblib"
    caminho_modelo.touch()
    modelo_falso = object()
    mock_joblib_load = mocker.patch.object(
        alvo.joblib, "load", return_value=modelo_falso
    )
    servico = ModelLoaderService(caminho_modelo=caminho_modelo)

    primeira_chamada = servico.carregar()
    segunda_chamada = servico.carregar()

    assert primeira_chamada is modelo_falso
    assert segunda_chamada is modelo_falso
    mock_joblib_load.assert_called_once_with(caminho_modelo)


def test_resolve_caminho_do_modelo_dinamicamente_quando_nao_informado(
    tmp_path, mocker
):
    """Resolve caminho do modelo dinamicamente quando nao informado."""
    diretorio_versao = tmp_path / "v9.9.9"
    diretorio_versao.mkdir()
    mocker.patch.object(
        alvo, "obter_model_settings", return_value=ConfiguracoesModeloFalsas()
    )
    mocker.patch.object(alvo, "encontrar_raiz_projeto", return_value=tmp_path)
    mocker.patch.object(
        alvo,
        "encontrar_diretorio_versao_mais_recente",
        return_value=diretorio_versao,
    )

    servico = ModelLoaderService()

    assert servico._caminho_modelo == diretorio_versao / "modelo-falso.joblib"

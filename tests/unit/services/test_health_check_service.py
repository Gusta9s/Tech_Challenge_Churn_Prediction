import pytest

from tech_challenge_churn_prediction.exceptions.app_exceptions import ModeloNaoDisponivelException
from tech_challenge_churn_prediction.services.health_check_service import HealthCheckService


class ModelLoaderFalsoOk:
    def carregar(self):
        return object()


class ModelLoaderFalsoComFalha:
    def carregar(self):
        raise FileNotFoundError("modelo ausente")


def test_verificar_liveness_sempre_retorna_true():
    assert HealthCheckService.verificar_liveness() is True


def test_verificar_readiness_retorna_true_quando_o_modelo_carrega_com_sucesso():
    servico = HealthCheckService(ModelLoaderFalsoOk())

    assert servico.verificar_readiness() is True


def test_verificar_readiness_levanta_excecao_de_dominio_quando_o_modelo_falha():
    servico = HealthCheckService(ModelLoaderFalsoComFalha())

    with pytest.raises(ModeloNaoDisponivelException) as excecao:
        servico.verificar_readiness()

    assert isinstance(excecao.value.cause, FileNotFoundError)

import pytest
from pydantic import ValidationError

from tech_challenge_churn_prediction.schemas.churn_prediction_input import ChurnPredictionInput


def test_cria_payload_valido_a_partir_de_dados_corretos(payload_valido_dict):
    entrada = ChurnPredictionInput(**payload_valido_dict)

    assert entrada.casado == "Yes"
    assert entrada.meses_como_cliente == 5


def test_rejeita_valor_fora_das_categorias_permitidas(payload_valido_dict):
    dados_invalidos = dict(payload_valido_dict, tipo_contrato="Three year")

    with pytest.raises(ValidationError):
        ChurnPredictionInput(**dados_invalidos)


def test_rejeita_payload_com_campo_obrigatorio_ausente(payload_valido_dict):
    dados_incompletos = dict(payload_valido_dict)
    del dados_incompletos["casado"]

    with pytest.raises(ValidationError):
        ChurnPredictionInput(**dados_incompletos)


def test_rejeita_meses_como_cliente_negativo(payload_valido_dict):
    dados_invalidos = dict(payload_valido_dict, meses_como_cliente=-1)

    with pytest.raises(ValidationError):
        ChurnPredictionInput(**dados_invalidos)


def test_rejeita_cobranca_mensal_negativa(payload_valido_dict):
    dados_invalidos = dict(payload_valido_dict, cobranca_mensal=-10.0)

    with pytest.raises(ValidationError):
        ChurnPredictionInput(**dados_invalidos)

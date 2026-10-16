import logging

from tech_challenge_churn_prediction.config import logging_config as alvo


def test_configurar_logging_aplica_configuracao_na_primeira_chamada(monkeypatch):
    monkeypatch.setattr(alvo, "_logging_configurado", False)
    chamadas = {}

    def basic_config_falso(**kwargs):
        chamadas.update(kwargs)

    monkeypatch.setattr(logging, "basicConfig", basic_config_falso)

    alvo.configurar_logging()

    assert chamadas
    assert alvo._logging_configurado is True


def test_configurar_logging_e_idempotente_na_segunda_chamada(monkeypatch):
    monkeypatch.setattr(alvo, "_logging_configurado", True)
    foi_chamado = False

    def basic_config_falso(**kwargs):
        nonlocal foi_chamado
        foi_chamado = True

    monkeypatch.setattr(logging, "basicConfig", basic_config_falso)

    alvo.configurar_logging()

    assert foi_chamado is False


def test_obter_logger_retorna_logger_com_o_nome_informado(monkeypatch):
    monkeypatch.setattr(alvo, "_logging_configurado", True)

    logger = alvo.obter_logger("teste.logger")

    assert isinstance(logger, logging.Logger)
    assert logger.name == "teste.logger"

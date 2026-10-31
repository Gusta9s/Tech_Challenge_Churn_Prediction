import asyncio

from tech_challenge_churn_prediction.services import (
    rate_limiter_service as alvo,
)
from tech_challenge_churn_prediction.config.rate_limit_settings import (
    RateLimitSettings,
)
from tech_challenge_churn_prediction.services.rate_limiter_service import (
    RateLimiterService,
    RateLimiterServiceFactory,
)


def _executar(corrotina):
    return asyncio.run(corrotina)


def test_permite_requisicao_e_decresce_as_restantes_corretamente(monkeypatch):
    """Permite requisicao e decresce as restantes corretamente."""
    monkeypatch.setattr(alvo.time, "monotonic", lambda: 0.0)
    servico = RateLimiterService(limite_requisicoes=3, janela_em_segundos=45)

    permitido_1, restantes_1 = _executar(
        servico.registrar_requisicao("127.0.0.1")
    )
    permitido_2, restantes_2 = _executar(
        servico.registrar_requisicao("127.0.0.1")
    )

    assert permitido_1 is True
    assert restantes_1 == 2
    assert permitido_2 is True
    assert restantes_2 == 1


def test_bloqueia_requisicao_quando_limite_e_atingido(monkeypatch):
    """Bloqueia requisicao quando limite e atingido."""
    monkeypatch.setattr(alvo.time, "monotonic", lambda: 0.0)
    servico = RateLimiterService(limite_requisicoes=2, janela_em_segundos=45)

    _executar(servico.registrar_requisicao("127.0.0.1"))
    _executar(servico.registrar_requisicao("127.0.0.1"))
    permitido, restantes = _executar(servico.registrar_requisicao("127.0.0.1"))

    assert permitido is False
    assert restantes == 0


def test_libera_capacidade_quando_requisicoes_antigas_saem_da_janela(
    monkeypatch,
):
    """Libera capacidade quando requisicoes antigas saem da janela."""
    tempo_atual = {"valor": 0.0}
    monkeypatch.setattr(alvo.time, "monotonic", lambda: tempo_atual["valor"])
    servico = RateLimiterService(limite_requisicoes=1, janela_em_segundos=45)

    _executar(servico.registrar_requisicao("127.0.0.1"))
    bloqueado, _ = _executar(servico.registrar_requisicao("127.0.0.1"))

    tempo_atual["valor"] = 46.0
    permitido_apos_janela, restantes = _executar(
        servico.registrar_requisicao("127.0.0.1")
    )

    assert bloqueado is False
    assert permitido_apos_janela is True
    assert restantes == 0


def test_mantem_historicos_isolados_por_cliente(monkeypatch):
    """Mantem historicos isolados por cliente."""
    monkeypatch.setattr(alvo.time, "monotonic", lambda: 0.0)
    servico = RateLimiterService(limite_requisicoes=1, janela_em_segundos=45)

    permitido_cliente_a, _ = _executar(
        servico.registrar_requisicao("10.0.0.1")
    )
    permitido_cliente_b, _ = _executar(
        servico.registrar_requisicao("10.0.0.2")
    )

    assert permitido_cliente_a is True
    assert permitido_cliente_b is True


def test_rate_limiter_service_factory_criar_retorna_singleton_configurado(
    monkeypatch,
):
    """Rate limiter service factory criar retorna singleton configurado."""
    monkeypatch.setattr(
        alvo.RateLimitSettingsFactory,
        "criar",
        lambda: RateLimitSettings(
            limite_requisicoes=3,
            janela_em_segundos=45,
            cabecalho_requisicoes_restantes="X-Teste-Restantes",
        ),
    )

    primeira_chamada = RateLimiterServiceFactory.criar()
    segunda_chamada = RateLimiterServiceFactory.criar()

    assert isinstance(primeira_chamada, RateLimiterService)
    assert primeira_chamada is segunda_chamada
    assert primeira_chamada._limite_requisicoes == 3
    assert primeira_chamada._janela_em_segundos == 45

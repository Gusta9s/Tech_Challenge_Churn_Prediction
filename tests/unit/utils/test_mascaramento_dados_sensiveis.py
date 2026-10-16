from tech_challenge_churn_prediction.config.security_settings import SecuritySettings
from tech_challenge_churn_prediction.utils import mascaramento_dados_sensiveis as alvo


def test_mascara_apenas_os_campos_configurados_como_sensiveis(monkeypatch):
    configuracoes = SecuritySettings(campos_sensiveis=frozenset({"senha"}), mascara_padrao="[OCULTO]")
    monkeypatch.setattr(alvo, "obter_security_settings", lambda: configuracoes)

    resultado = alvo.mascarar_campos_sensiveis({"usuario": "joao", "senha": "123"})

    assert resultado == {"usuario": "joao", "senha": "[OCULTO]"}


def test_nao_altera_valores_quando_nenhum_campo_e_sensivel(monkeypatch):
    configuracoes = SecuritySettings(campos_sensiveis=frozenset(), mascara_padrao="[OCULTO]")
    monkeypatch.setattr(alvo, "obter_security_settings", lambda: configuracoes)

    resultado = alvo.mascarar_campos_sensiveis({"a": 1, "b": 2})

    assert resultado == {"a": 1, "b": 2}


def test_nao_modifica_o_dicionario_original(monkeypatch):
    configuracoes = SecuritySettings(campos_sensiveis=frozenset({"senha"}), mascara_padrao="[OCULTO]")
    monkeypatch.setattr(alvo, "obter_security_settings", lambda: configuracoes)
    original = {"senha": "123"}

    alvo.mascarar_campos_sensiveis(original)

    assert original == {"senha": "123"}

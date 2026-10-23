from tech_challenge_churn_prediction.config.security_settings import (
    SecuritySettingsFactory,
)


def mascarar_campos_sensiveis(dados: dict) -> dict:
    """Mascara os valores dos campos sensiveis de um dicionario para log.

    Parameters
    ----------
    dados : dict
        Dicionario original, nao modificado por esta funcao.

    Returns
    -------
    dict
        Copia de `dados` com os campos sensiveis (definidos em
        SecuritySettings) substituidos pela mascara configurada.
    """
    configuracoes_seguranca = SecuritySettingsFactory.criar()
    return {
        chave: (
            configuracoes_seguranca.mascara_padrao
            if chave in configuracoes_seguranca.campos_sensiveis
            else valor
        )
        for chave, valor in dados.items()
    }

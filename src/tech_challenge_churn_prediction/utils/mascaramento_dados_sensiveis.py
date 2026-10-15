from tech_challenge_churn_prediction.config.security_settings import obter_security_settings


def mascarar_campos_sensiveis(dados: dict) -> dict:
    """Retorna uma copia do dicionario com os valores dos campos sensiveis
    (definidos em SecuritySettings) substituidos por uma mascara fixa, para
    uso seguro em logs (nao altera o dicionario original nem os dados usados
    no fluxo de processamento).
    """
    configuracoes_seguranca = obter_security_settings()
    return {
        chave: (
            configuracoes_seguranca.mascara_padrao
            if chave in configuracoes_seguranca.campos_sensiveis
            else valor
        )
        for chave, valor in dados.items()
    }

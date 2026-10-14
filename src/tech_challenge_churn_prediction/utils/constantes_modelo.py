COLUNAS_ADDONS: tuple[str, ...] = (
    "possui_seguranca_online",
    "possui_backup_online",
    "possui_protecao_dispositivo",
    "possui_suporte_tecnico_premium",
    "possui_streaming_tv_terceiros",
    "possui_streaming_filmes_terceiros",
)

COLUNAS_SERVICO_DE_INTERNET: tuple[str, ...] = (
    "possui_servico_de_internet_dsl",
    "possui_servico_de_internet_fibra_optica",
    "possui_servico_de_internet_sem_internet",
)

COLUNAS_METODO_PAGAMENTO: tuple[str, ...] = (
    "metodo_pagamento_bank_transfer_automatic",
    "metodo_pagamento_credit_card_automatic",
    "metodo_pagamento_electronic_check",
    "metodo_pagamento_mailed_check",
)

# Ordem exata exigida pelo modelo campeao (RandomForestClassifier.feature_names_in_),
# treinado em notebooks/arvore_de_descisao/modelo_final/V6-Validacao_cruzada_k_fold_random_forest.ipynb.
ORDEM_FEATURES_RANDOM_FOREST: tuple[str, ...] = (
    "cliente_em_idade_avancada",
    "casado",
    "meses_como_cliente",
    "possui_servico_telefonico",
    "possui_multiplas_linhas",
    *COLUNAS_ADDONS,
    "tipo_contrato",
    "fatura_sem_papel",
    "cobranca_mensal",
    "total_cobrado_durante_trimestre",
    *COLUNAS_SERVICO_DE_INTERNET,
    *COLUNAS_METODO_PAGAMENTO,
    "quantidade_de_addons",
)

from tech_challenge_churn_prediction.utils.mapeamento_categorico import MAPA_TIPO_CONTRATO

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

# Categorias explicitas usadas pelos encoders do pipeline de pre-processamento
# (OrdinalEncoder/OneHotEncoder), na mesma ordem das colunas de saida acima,
# garantindo que o pipeline seja stateless (nao depende de dados de treino).
CATEGORIAS_BINARIAS_SIMPLES: tuple[str, str] = ("No", "Yes")

CATEGORIAS_TIPO_CONTRATO: tuple[str, ...] = tuple(MAPA_TIPO_CONTRATO)

# Ordem casada com COLUNAS_SERVICO_DE_INTERNET (dsl, fibra_optica, sem_internet).
CATEGORIAS_SERVICO_DE_INTERNET: tuple[str, ...] = ("DSL", "Fiber optic", "No")

# Ordem casada com COLUNAS_METODO_PAGAMENTO (bank_transfer, credit_card, electronic_check, mailed_check).
CATEGORIAS_METODO_PAGAMENTO: tuple[str, ...] = (
    "Bank transfer (automatic)",
    "Credit card (automatic)",
    "Electronic check",
    "Mailed check",
)

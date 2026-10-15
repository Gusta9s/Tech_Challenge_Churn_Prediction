MAPA_BINARIO_COM_AUSENCIA_DE_SERVICO: dict[str, int] = {
    "Yes": 1,
    "No": 0,
    "No internet service": 0,
    "No phone service": 0,
}

# Fonte de verdade da ordinalidade de tipo_contrato: usada tanto para
# documentar a regra de dominio quanto para derivar CATEGORIAS_TIPO_CONTRATO
# (ordem de categorias do OrdinalEncoder no pipeline de pre-processamento).
MAPA_TIPO_CONTRATO: dict[str, int] = {
    "Month-to-month": 0,
    "One year": 1,
    "Two year": 2,
}

MAPA_BINARIO_SIMPLES: dict[str, int] = {"Yes": 1, "No": 0}

MAPA_BINARIO_COM_AUSENCIA_DE_SERVICO: dict[str, int] = {
    "Yes": 1,
    "No": 0,
    "No internet service": 0,
    "No phone service": 0,
}

MAPA_TIPO_CONTRATO: dict[str, int] = {
    "Month-to-month": 0,
    "One year": 1,
    "Two year": 2,
}

MAPA_CODIGO_SERVICO_DE_INTERNET: dict[str, str] = {
    "No": "sem_internet",
    "Fiber optic": "fibra_optica",
    "DSL": "dsl",
}

MAPA_CODIGO_METODO_PAGAMENTO: dict[str, str] = {
    "Mailed check": "mailed_check",
    "Electronic check": "electronic_check",
    "Bank transfer (automatic)": "bank_transfer_automatic",
    "Credit card (automatic)": "credit_card_automatic",
}


def mapear_valor_binario(valor: str, mapa: dict[str, int]) -> int:
    """Converte um valor categorico textual (ex.: "Yes"/"No") no binario
    esperado pelo modelo, reutilizado por todos os campos binarios do payload.
    """
    try:
        return mapa[valor]
    except KeyError as erro:
        valores_aceitos = sorted(mapa)
        raise ValueError(
            f"Valor '{valor}' nao reconhecido. Valores aceitos: {valores_aceitos}"
        ) from erro

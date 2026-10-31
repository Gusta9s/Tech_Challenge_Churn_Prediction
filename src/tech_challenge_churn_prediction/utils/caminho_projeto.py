from pathlib import Path


def encontrar_raiz_projeto(marcador: str = "pyproject.toml") -> Path:
    """Localiza a raiz do projeto subindo a partir do diretorio atual.

    Parameters
    ----------
    marcador : str, default="pyproject.toml"
        Nome do arquivo usado para identificar a raiz do projeto.

    Returns
    -------
    pathlib.Path
        Diretorio onde o arquivo marcador foi encontrado.

    Raises
    ------
    FileNotFoundError
        Se o marcador nao existir em nenhum diretorio pai.
    """
    for diretorio in [Path.cwd(), *Path.cwd().parents]:
        if (diretorio / marcador).exists():
            return diretorio

    raise FileNotFoundError(
        "Nao foi possivel localizar a raiz do projeto "
        f"(marcador '{marcador}' nao encontrado)."
    )

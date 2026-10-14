from pathlib import Path


def encontrar_raiz_projeto(marcador: str = "pyproject.toml") -> Path:
    """Localiza a raiz do projeto subindo a partir do diretorio atual ate
    encontrar o arquivo marcador, garantindo reprodutibilidade em qualquer
    maquina ou diretorio de execucao (mesma estrategia usada nos notebooks).
    """
    for diretorio in [Path.cwd(), *Path.cwd().parents]:
        if (diretorio / marcador).exists():
            return diretorio

    raise FileNotFoundError(
        f"Nao foi possivel localizar a raiz do projeto (marcador '{marcador}' nao encontrado)."
    )

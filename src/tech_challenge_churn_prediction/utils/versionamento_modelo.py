import re
from pathlib import Path

PADRAO_VERSAO = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")


def encontrar_diretorio_versao_mais_recente(diretorio_modelos: Path) -> Path:
    """Varre os diretorios "vX.Y.Z" dentro de `diretorio_modelos` e retorna o
    de maior versao semantica que contenha um artefato de modelo (.joblib),
    mesma convencao de versionamento dinamico adotada nos notebooks.
    """
    versoes_disponiveis: dict[tuple[int, int, int], Path] = {}

    for diretorio in diretorio_modelos.iterdir():
        if not diretorio.is_dir():
            continue

        correspondencia = PADRAO_VERSAO.match(diretorio.name)
        if correspondencia and any(diretorio.glob("*.joblib")):
            versao = tuple(int(grupo) for grupo in correspondencia.groups())
            versoes_disponiveis[versao] = diretorio

    if not versoes_disponiveis:
        raise FileNotFoundError(
            "Nenhuma versao de modelo (.joblib) encontrada em: "
            f"{diretorio_modelos}"
        )

    versao_mais_recente = max(versoes_disponiveis)
    return versoes_disponiveis[versao_mais_recente]

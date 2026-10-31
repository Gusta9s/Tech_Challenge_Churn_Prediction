import re
from pathlib import Path

PADRAO_VERSAO = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")


def encontrar_diretorio_versao_mais_recente(diretorio_modelos: Path) -> Path:
    """Localiza o diretorio de maior versao semantica com um artefato.

    Parameters
    ----------
    diretorio_modelos : pathlib.Path
        Diretorio onde as versoes "vX.Y.Z" do modelo estao salvas.

    Returns
    -------
    pathlib.Path
        Diretorio da maior versao que contenha um arquivo `.joblib`.

    Raises
    ------
    FileNotFoundError
        Se nenhuma versao valida com `.joblib` for encontrada.
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

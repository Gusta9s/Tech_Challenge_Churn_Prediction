from typing import Literal

from pydantic import BaseModel


class HealthStatus(BaseModel):
    """Resultado de uma verificacao de saude (liveness ou readiness).

    Attributes
    ----------
    status : {"UP"}
        Status da verificacao de saude.
    """

    status: Literal["UP"]

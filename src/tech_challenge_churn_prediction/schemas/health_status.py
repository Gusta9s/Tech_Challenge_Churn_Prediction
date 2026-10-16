from typing import Literal

from pydantic import BaseModel


class HealthStatus(BaseModel):
    """Resultado de uma verificacao de saude (liveness ou readiness)."""

    status: Literal["UP"]

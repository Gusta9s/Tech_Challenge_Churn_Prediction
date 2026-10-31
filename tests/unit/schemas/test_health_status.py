from tech_challenge_churn_prediction.schemas.health_status import HealthStatus


def test_cria_status_up():
    """Cria status up."""
    status = HealthStatus(status="UP")

    assert status.status == "UP"

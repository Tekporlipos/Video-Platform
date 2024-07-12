from app import app
from src.services.healthService import HealthService

healthService = HealthService()


@app.route('/api/v1/health/')
def health():
    return healthService.check_health(logger=app.logger)

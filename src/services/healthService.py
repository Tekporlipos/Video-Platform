from sqlalchemy import text

from app import db
from src.utils.responseEntity import *


class HealthService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HealthService, cls).__new__(cls)
        return cls._instance

    def check_health(self, logger=None):
        try:
            db.session.execute(text("SELECT 1")).scalar()
            return success_response("Service Available", logger=logger, logger_type="info")
        except Exception as e:
            return error_response(str(e), status_code=500, logger=logger, logger_type="error")

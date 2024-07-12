from instance.config import Config


class DbConfig:
    SQLALCHEMY_DATABASE_URI = Config.DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

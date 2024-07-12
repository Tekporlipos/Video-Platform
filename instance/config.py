import os
from datetime import timedelta


class Config:
    # Database URL
    DATABASE_URI = os.environ.get('DATABASE_URI')

    # Flask Environment
    FLASK_ENV = os.environ.get('FLASK_ENV')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES_DAYS', 1)))
    APP_URL = os.environ.get('APP_URL')

    # Upload Folder
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'static/videos')

    # Mail Server Configuration
    MAIL_MAILER = os.environ.get('MAIL_MAILER', 'smtp')
    MAIL_HOST = os.environ.get('MAIL_HOST', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_ENCRYPTION = os.environ.get('MAIL_ENCRYPTION', 'TLS')
    MAIL_FROM_ADDRESS = os.environ.get('MAIL_FROM_ADDRESS')
    MAIL_FROM_NAME = os.environ.get('MAIL_FROM_NAME', '${APP_NAME}')

from datetime import timedelta

from flask import Flask

from instance.config import Config
from instance.dbconfig import DbConfig
from migration.Base import db
from dotenv import load_dotenv
from instance.logger import setup_logging
from flask_cors import CORS

from src.services.EmailService import mail
from src.services.JWTService import jwt

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__, static_url_path='/static', static_folder='static')

# Load database configuration from DbConfig
app.config.from_object(DbConfig)

# Initialize SQLAlchemy with the Flask application
db.init_app(app)

# Initialize Flask-Mail
mail.init_app(app)

# Setup logging configuration
setup_logging(app)

# Enable CORS for all endpoints
CORS(app)
# JWT Configuration
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
app.config['JWT_IDENTITY_CLAIM'] = 'sub'
# Initialize Flask-JWT-Extended
jwt.init_app(app)

# Configure email server settings
app.config['MAIL_SERVER'] = Config.MAIL_MAILER
app.config['MAIL_PORT'] = Config.MAIL_PORT
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = Config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = Config.MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = Config.MAIL_FROM_ADDRESS

# Import API routes (assumed to be defined in routes/api.py)
import routes.api

# Create database tables within the application context
with app.app_context():
    # Import all models here to ensure SQLAlchemy can find them
    import src.models.UserModel
    import src.models.VideoModel
    import src.models.ResetPasswordTokenModel
    import src.models.EmailVerificationModel

    # Create all tables defined in the models
    try:
        db.create_all()
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error creating database tables: {str(e)}")

# Entry point of the Flask application
if __name__ == '__main__':
    app.run()

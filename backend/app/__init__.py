from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import RotatingFileHandler
from .config import Config

# Create Flask application instance
app = Flask(__name__)

app.config['CORS_HEADERS'] = ['Content-Type', 'Authorization']

# Load configuration settings
app.config.from_object(Config)

# Initialize SQLAlchemy database
db = SQLAlchemy(app)

# Initialize logging
file_handler = RotatingFileHandler('app.log', maxBytes=1024 * 1024 * 10, backupCount=5)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
file_handler.setLevel(logging.INFO)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

# Initialize logger
logger = logging.getLogger(__name__)

# Import routes and register them with the application
from app.routes.prediction import prediction_bp
app.register_blueprint(prediction_bp, url_prefix='/predict')

from app.routes.health import health_bp
app.register_blueprint(health_bp)

# Import models to ensure they are registered with SQLAlchemy
from app.models import prediction

try:
    # Create tables
    with app.app_context():
        db.create_all()
    logger.info("DB Initialized")
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")


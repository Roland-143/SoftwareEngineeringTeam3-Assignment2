"""Flask application factory."""

from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.routes.students import students_bp
from app.routes.health import health_bp


def create_app():
    """Create and configure the Flask application."""
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)

    CORS(flask_app)

    flask_app.register_blueprint(health_bp)
    flask_app.register_blueprint(students_bp, url_prefix="/api")

    return flask_app

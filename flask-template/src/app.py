from dotenv import load_dotenv
from flask import Flask

from src.config import Config
from src.db import init_engine
from src.errors import register_error_handlers
from src.extensions import cors, jwt
from src.routes.health import health_bp

load_dotenv()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    cors.init_app(app, origins=app.config["ALLOWED_HOSTS"])
    jwt.init_app(app)

    init_engine(app.config["DATABASE_URL"])

    app.register_blueprint(health_bp)

    register_error_handlers(app)

    return app


app = create_app()

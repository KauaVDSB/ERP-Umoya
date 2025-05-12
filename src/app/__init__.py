import os
import pytest

from flask import Flask

from .config import get_config
from .extensions import db, migrate


def create_app():
    """
    Cria app e carrega configs, extensões e blueprints
    """

    env = os.getenv("FLASK_ENV", "development")
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(get_config(env))


    # Extensões
    db.init_app(app)
    migrate.init_app(app, db)


    # Blueprints

    from .blueprints.health.routes import health_bp
    from .blueprints.cliente.routes import cliente_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(cliente_bp)

    return app


@pytest.fixture
def app():
    return create_app()

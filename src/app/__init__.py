import os
import pytest

from flask import Flask
from supabase import create_client, Client

from .config import get_config
from .extensions import db, migrate


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def create_app():
    """
    Cria app e carrega configs, extensões e blueprints
    """

    env = os.getenv("FLASK_ENV", "development")
    # pylint: disable=redefined-outer-name
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(get_config(env))

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Extensões
    db.init_app(app)
    migrate.init_app(app, db)

    app.supabase = supabase

    # Blueprints

    from .blueprints.health.routes import (  # pylint: disable=import-outside-toplevel
        health_bp,
    )
    from .blueprints.cliente.routes import (  # pylint: disable=import-outside-toplevel
        cliente_bp,
    )
    from .blueprints.inventory import (  # pylint: disable=import-outside-toplevel
        bp as inventory_bp,
    )

    app.register_blueprint(health_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(inventory_bp)

    return app


@pytest.fixture
def app():
    return create_app()

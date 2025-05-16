import pytest
import os
from app import create_app
from app.extensions import db


@pytest.fixture(autouse=True)
def set_test_env(monkeypatch):
    # monkeypatch cria banco SQLite temporário em memória
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory")


@pytest.fixture
def app():
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    app = create_app()

    with app.app_context():
        # db.drop_all()
        db.create_all()

    yield app

    # Remove conexões e dados após o teste
    # with app.app_context():
    #     db.session.remove()
    #     db.drop_all()

from modules.app.config import create_app
import pytest


@pytest.fixture
def app():
    app = create_app()
    app.debug = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_index(client):
    assert True

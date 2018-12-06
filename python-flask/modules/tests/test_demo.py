import os
import tempfile
import pytest
import index

@pytest.fixture
def client():
    db_fd, index.app.config['DATABASE'] = tempfile.mkstemp()
    index.app.config['TESTING'] = True
    client = index.app.test_client()


    yield client

    os.close(db_fd)
    os.unlink(index.app.config['DATABASE'])


def test_empty_db(client):
    """Start with a blank database."""
    rv = client.get('/')
    assert b'Hello World' in rv.data


def func(x):
    return x + 1


def test_answer():
    assert func(3) == 4



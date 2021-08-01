import pytest
from edamam_flask import app

@pytest.fixture
def client():
    test_app = app.create_app()
    with test_app.test_client() as client:
        yield client

def test_root(client):
    request = client.get('/')
    assert request.status_code == 200
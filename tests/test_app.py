import pytest
from edamam_flask import app

@pytest.fixture
def client():
    test_app = app.create_app()
    with test_app.test_client() as client:
        yield client

def test_get_root(client):
    request = client.get('/')
    assert request.status_code == 200

def test_get_upc(client):
    request = client.get('/upc/00000000')
    assert request.status_code != 404
    assert request.json['query']['upc'] == '00000000'

def test_get_ingredient(client):
    request = client.get('/ingredient/apple')
    assert request.status_code != 404
    assert request.json['query']['ingr'] == 'apple'
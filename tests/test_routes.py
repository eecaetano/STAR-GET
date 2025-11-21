import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_display_route(client):
    """Testa a rota de display (/)"""
    response = client.get('/')
    assert response.status_code == 200

def test_cadastro_route_get(client):
    """Testa a rota de cadastro via GET"""
    response = client.get('/cadastro')
    assert response.status_code == 200

def test_login_route_get(client):
    """Testa a rota de login via GET"""
    response = client.get('/login')
    assert response.status_code == 200


def test_pos_login_route(client):
    """Testa a rota de pós-login"""
    response = client.get('/pos_login')
    assert response.status_code == 200

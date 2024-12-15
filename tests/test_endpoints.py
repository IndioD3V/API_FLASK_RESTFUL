import pytest 
from app import app
from libs.database import db
from models import Customer
from os import getenv

SQL_LITE_TESTS = getenv('SQL_LITE_TESTS')


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  
            db.session.begin()  
            yield client 
            db.session.rollback() 


def test_post_customer_success(client):
    # Dado
    data = [
        {
        "name": "Cliente Teste",
        "legacy_id": "123",
        "cnpj": "12345678901234"
        }
    ]

    response = client.post('/clientes', json=data)
    
    assert response.status_code == 201
    json_data = response.get_json()['values'][0]
    assert json_data['name'] == "Cliente Teste"
    assert json_data['legacy_id'] == "123"
    assert json_data['cnpj'] == "12345678901234"


def test_get_customers(client):
    response = client.get('/clientes')
    assert response.status_code == 200
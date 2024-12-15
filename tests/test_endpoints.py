import pytest 
from tests.conftest import app
from libs.database import db
from models import Customer
from sqlalchemy import Column, String
from os import getenv
from datetime import date

SQL_LITE_TESTS = getenv('SQL_LITE_TESTS')


@pytest.fixture
def test_app():
    with app.app_context():
        db.create_all()  # Cria as tabelas no SQLite
        yield app
        db.session.remove()
        db.drop_all()  # Limpa o banco após os testes


@pytest.fixture
def test_client(test_app):
    """Cria um cliente de teste para as requisições HTTP"""
    return test_app.test_client()


class TestCustomerResource:
    @pytest.fixture(autouse=True)
    def setup(self, test_client):
        self.client = test_client
    
    def test_post_new_customer(self):

        data = {
            "name": "John Dee",
            "legacy_id": "blackmagic@example.com",
            "status": "Ativo",
            "cnpj": "123456789123"
        }
        
        response = self.client.post("/clientes", json=data)
        
        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data["success"] is True
        assert json_data["operation"] == "created"
        assert json_data["values"]["name"] == "John Dee"
    
    def test_get_with_filter_legacy_id(self):

        new_customer = Customer(id=1, name="John Doe", legacy_id="johnsmith@example.com", dt_created=date.today())
        db.session.add(new_customer)
        db.session.commit()


        response = self.client.get("/clientes?legacy_id=johnsmith@example.com")
        assert response.status_code == 200


    def test_put_existing_record(self):
        # Cria um registro inicial no banco de dados
        new_customer = Customer(id=1, name="John Doe", legacy_id="johnsmith@example.com", dt_created=date.today())
        db.session.add(new_customer)
        db.session.commit()

        # Dados atualizados
        updated_data = {
            "name": "John Smith",
            "legacy_id": "johnsmith@example.com"
        }

        response = self.client.put(
            "/clientes", json=updated_data  # Altere a URL para o endpoint correto
        )
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["success"] is True
        assert json_data["operation"] == "update"
        assert json_data["values"]["name"] == "John Smith"

    def test_put_nonexistent_record(self):
        # Dados para um registro inexistente
        data = {
            "name": "Non Existent",
            "legacy_id": "nonexistent@example.com"
        }

        response = self.client.put(
            "/clientes", json=data  # Altere a URL para o endpoint correto
        )
        assert response.status_code == 404
        json_data = response.get_json()
        assert json_data["success"] is False
        assert json_data["error"] == "NotFound"

    def test_delete_existing_record(self):
        # Cria um registro inicial
        new_customer = Customer(id=1,  dt_created=date.today(), legacy_id = 'testestes')
        db.session.add(new_customer)
        db.session.commit()

        response = self.client.delete(
            f"/clientes?id={new_customer.id}"  # Altere a URL para o endpoint correto
        )
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["success"] is True
        assert json_data["message"] == f"Record with id {new_customer.id} successfully deleted."

        # Confirma que o registro foi removido
        record = Customer.query.get(new_customer.id)
        assert record is None

    def test_delete_nonexistent_record(self):
        response = self.client.delete(
            "/clientes?id=999"  # ID inexistente
        )
        assert response.status_code == 404
        json_data = response.get_json()
        assert json_data["success"] is False
        assert json_data["error"] == "RecordNotFound"
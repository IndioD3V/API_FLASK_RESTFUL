import pytest
from app import app  # Importa a instância do app configurado no app.py
from libs.database import db
from libs.database import init_db
from libs.resources import CustomerResource

@pytest.fixture
def app_test():
    # Configura a aplicação para o ambiente de teste
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5435/test'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True

    # Inicializa o banco de dados com o app de teste
    init_db(app)

    with app.app_context():
        db.create_all()  # Cria as tabelas antes de cada teste
        yield app  # Fornece o app para o teste
        db.drop_all()  # Limpa as tabelas após o teste

from flask import Flask
from flask_restful import Api
from database import init_db
from endpoints import CustomerEndpoint, ProjectsEndpoint, TasksEndpoint
import os
app = Flask(__name__)
api = Api(app)

postgres_port = os.getenv('POSTGRES_PORT')
postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_host = os.getenv('POSTGRES_HOST')
postgres_db = os.getenv('POSTGRES_DB')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)

# Registrando as classes de endpoint

api.add_resource(CustomerEndpoint, '/clientes')
api.add_resource(ProjectsEndpoint, '/projetos')
api.add_resource(TasksEndpoint, '/atividades')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

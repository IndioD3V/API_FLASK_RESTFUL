from flask import Flask
from flask_restful import Api
from libs.database import init_db
from libs.resources import (
    CustomerResource, ProjectsResource, 
    TasksResource
)
import os
app = Flask(__name__)
api = Api(app)

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)


# Registrando as classes de endpoint

api.add_resource(CustomerResource, '/clientes')
api.add_resource(ProjectsResource, '/projetos')
api.add_resource(TasksResource, '/atividades')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

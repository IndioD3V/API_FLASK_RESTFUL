from flask_restful import Resource
from flask import request, jsonify, make_response
from models import Customer, Tasks, Projects
from producer import send_event
from database import db
from dataclasses import dataclass
from datetime import date

@dataclass
class ClassBase(Resource):
    table = None
    
    def get(self):
        table_objs = self.table.query.all()
        return jsonify([
            {column.name: getattr(obj, column.name) for column in self.table.__table__.columns}
            for obj in table_objs
        ])
        
    def post(self):
        data = request.get_json()
        try:

            new_customer_data = {
                column.name: data.get(column.name)  
                for column in self.table.__table__.columns
                if column.name in data  
            }

            new_customer = self.table(**new_customer_data)

            db.session.add(new_customer)
            db.session.commit()
            
            data = {column.name: self.serialize(getattr(new_customer, column.name)) for column in self.table.__table__.columns}

            send_event({
                'action': 'create',
                'entity': self.table.__tablename__,
                'data': data
            })
            
            return make_response(jsonify(data), 201)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 400)
    
    def serialize(self, value):

        if isinstance(value, date):
            return value.strftime('%Y-%m-%d')  # Converte para string no formato YYYY-MM-DD
        return value

@dataclass
class CustomerEndpoint(ClassBase):
    table = Customer
    
@dataclass
class ProjectsEndpoint(ClassBase):
    table = Projects

@dataclass
class TasksEndpoint(ClassBase):
    table = Tasks


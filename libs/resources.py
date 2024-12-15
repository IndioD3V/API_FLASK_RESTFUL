from flask_restful import Resource
from flask import request, jsonify, make_response
from models import Customer, Projects, Tasks
#from libs.producer import send_event
from libs.database import db
from dataclasses import dataclass
from datetime import date
from sqlalchemy.exc import IntegrityError 
from psycopg2.errors import NotNullViolation, UniqueViolation
import datetime


@dataclass
class BaseResource(Resource):
    table = None
    
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        total = self.table.query.count()
        table_objs = self.table.query.offset((page - 1) * per_page).limit(per_page).all()
        total_pages = (total + per_page - 1) // per_page

        data = [
            {
                column.name: self.format_type(
                    getattr(obj, column.name),
                    column.type.python_type
                )
                for column in self.table.__table__.columns
            }
            for obj in table_objs
        ]

        return make_response(jsonify({
            'data': data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages
            }
        }), 200)


    def post(self):
        data = request.get_json()
        columns = [column for column in self.table.__table__.columns]
        values = []

        try:
            for customer_data in data:
                new_customer_data = {
                    column.name: customer_data.get(column.name)
                    for column in columns
                    if column.name in customer_data
                }
                new_customer = self.table(**new_customer_data)

                try:
                    db.session.add(new_customer)
                    values.append({column.name: self.serialize(getattr(new_customer, column.name))for column in columns})
                    

                except IntegrityError as e:
                    if isinstance(e.orig, UniqueViolation):
                        db.session.rollback()
                        key = self.table.__foreign_key__
                        key_value = customer_data.pop(key)
                        
                        if key_value:
                            existing_record = self.table.query.filter(getattr(self.table, key) == key_value).first()

                            if existing_record:
                                self.table.query.filter(getattr(self.table, key) == key_value).update(customer_data)
                                values.append({column.name: self.serialize(getattr(new_customer, column.name))for column in columns})
                
                return make_response(
                        jsonify(
                            {
                                "success": True,
                                "operation": "created",
                                "values": values
                            }
                        ), 201
                    )

        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({
                "success": False,
                "error": "InternalServerError",
                "message": str(e)
            }), 500)


            
    def format_type(self, value, type_value:type):
        try:
            if type_value == datetime.date:
                return value.strftime('%Y-%m-%d')
            return type_value(value)
        except Exception as e:
            return ''
        
        
    def serialize(self, value):
        if isinstance(value, date):
            return value.strftime('%Y-%m-%d') 
        return value

@dataclass
class CustomerResource(BaseResource):
    table = Customer
    
@dataclass
class ProjectsResource(BaseResource):
    table = Projects

@dataclass
class TasksResource(BaseResource):
    table = Tasks

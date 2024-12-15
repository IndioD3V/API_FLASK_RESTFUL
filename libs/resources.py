# External
from flask_restful import Resource
from flask import request, jsonify, make_response
from sqlalchemy.exc import IntegrityError 
from psycopg2.errors import NotNullViolation, UniqueViolation
from datetime import datetime

# Internal
from models import Customer, Projects, Tasks
#from libs.producer import send_event
from libs.database import db
from dataclasses import dataclass
from libs.errors import UniqueViolationError, InternalServerError
from libs.common import serialize, format_type


@dataclass
class BaseResource(Resource):
    table = None
    
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status_filter = request.args.get('status', None)
        customer_id_filter = request.args.get('customer_id', None)
        project_id = request.args.get('project_id', None)
        task_id = request.args.get('task_id', None)
        legacy_id = request.args.get('legacy_id', None)
        dt_created = request.args.get('dt_created', None)

        query = self.table.query
        
        filters = {
            "status": status_filter,
            "customer_id": customer_id_filter,
            "project_id": project_id,
            "task_id": task_id,
            "legacy_id": legacy_id,
            "dt_created": dt_created
        }
        
        columns = [column.name for column in self.table.__table__.columns]
        
        for field, value in filters.items():
            if value is not None and field in columns:
                query = query.filter(getattr(self.table, field) == value)

        total = query.count()
        table_objs = query.offset((page - 1) * per_page).limit(per_page).all()
        total_pages = (total + per_page - 1) // per_page

        data = [
            {
                column.name: format_type(
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

        for column in columns:
            if column.type.python_type == datetime.date and column.name in data:
                if isinstance(data[column.name], str):
                    data[column.name] = datetime.strptime(data[column.name], "%Y-%m-%d").date()

        new_customer_data = {
            column.name: data.get(column.name)
            for column in columns
            if column.name in data
        }
        new_customer = self.table(**new_customer_data)

        try:
            db.session.add(new_customer)
            db.session.commit()
            rows = {
                column.name: serialize(
                    getattr(new_customer, column.name)
                ) for column in columns
            }
            
            return make_response(
                jsonify({
                    "success": True,
                    "operation": "created",
                    "values": rows
                }), 201
            )
            
        except IntegrityError as e:
            db.session.rollback()
            if isinstance(e.orig, UniqueViolation):
                return make_response(jsonify(UniqueViolationError.msg), UniqueViolationError.code)

        except Exception as e:
            db.session.rollback()
            error = InternalServerError(e)
            return make_response(jsonify(error.msg), error.code)

    
    def put(self):
        data = request.get_json()
        columns = [column for column in self.table.__table__.columns]

        new_customer_data = {
            column.name: data.get(column.name)
            for column in columns
            if column.name in data
        }
        new_customer = self.table(**new_customer_data)
        key = self.table.__foreign_key__
        key_value = data.pop(key, None)

        if key_value:
            existing_record = self.table.query.filter(getattr(self.table, key) == key_value).first()
            if existing_record:
                self.table.query.filter(getattr(self.table, key) == key_value).update(data)
                db.session.commit() 
                rows = {
                    column.name: serialize(
                    getattr(
                        new_customer, 
                        column.name
                        )
                    ) for column in columns
                }
                return make_response(
                    jsonify({
                        "success": True,
                        "operation": "update",
                        "values": rows
                    }), 200
                    )
            else:
                return make_response(jsonify({
                    "success": False,
                    "error": "NotFound",
                    "message": f"Record with {key} = {key_value} not found."
                }), 404)
                
    def delete(self):
        id = request.args.get('id')
        try:
            record_to_delete = self.table.query.get(id)
            if not record_to_delete:
                return make_response(jsonify({
                    "success": False,
                    "error": "RecordNotFound",
                    "message": f"No record found with id {id}."
                }), 404)

            db.session.delete(record_to_delete)
            db.session.commit()

            return make_response(jsonify({
                "success": True,
                "message": f"Record with id {id} successfully deleted.",
                "table": self.table.__tablename__
            }), 200)

        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({
                "success": False,
                "error": "InternalServerError",
                "message": str(e)
            }), 500)

        
    

@dataclass
class CustomerResource(BaseResource):
    table = Customer
    
@dataclass
class ProjectsResource(BaseResource):
    table = Projects

@dataclass
class TasksResource(BaseResource):
    table = Tasks

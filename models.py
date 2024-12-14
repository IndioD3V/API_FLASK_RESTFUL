from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, VARCHAR, Float
from sqlalchemy.orm import relationship
from datetime import date as dt, datetime
from database import db


class Customer(db.Model):
    __tablename__ = 'customer'
    
    id = Column(Integer, primary_key=True, index=True)
    legacy_id = Column(VARCHAR(50), index=True, unique=True, nullable=True)
    dt_created = Column(Date, index=True, default=(dt.today()).strftime('%Y-%m-%d'))
    name = Column(String)
    cnpj = Column(VARCHAR(14), index=True)
    
    # Relação com Projects e Tasks
    projects = relationship('Projects', back_populates='customer')
    tasks = relationship('Tasks', back_populates='customer')


class Projects(db.Model):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True, index=True)
    legacy_id = Column(VARCHAR(50), index=True, unique=True)
    dt_created = Column(Date, index=True, default=(dt.today()).strftime('%Y-%m-%d'))
    customer_id = Column(Integer, ForeignKey('customer.id'))
    start_datetime = Column(DateTime, default=datetime.now())
    notes = Column(String)
    amount = Column(Float, default=0.0)
    project_name = Column(String)

    # Relação com Customer e Tasks
    customer = relationship('Customer', back_populates='projects')
    tasks = relationship('Tasks', back_populates='project')


class Tasks(db.Model):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    legacy_id = Column(VARCHAR(50), index=True, unique=True)
    dt_created = Column(Date, index=True, default=(dt.today()).strftime('%Y-%m-%d'))
    customer_id = Column(Integer, ForeignKey('customer.id'))
    start_datetime = Column(DateTime, default=datetime.now())
    description = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))

    # Relação com Projects e Customer
    project = relationship('Projects', back_populates='tasks')
    customer = relationship('Customer', back_populates='tasks')

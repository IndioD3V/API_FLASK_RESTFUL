from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from libs.database import db

class Tasks(db.Model):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, index=True)
    legacy_id = Column(String(50), unique=True, index=True, nullable=False)
    dt_created = Column(Date)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    start_datetime = Column(DateTime)
    description = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))
    status = Column(String, default='Ativo')
    
    customer = relationship('Customer', back_populates='tasks')
    projects = relationship('Projects', back_populates='tasks')

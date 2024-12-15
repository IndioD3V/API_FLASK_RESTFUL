from sqlalchemy import Column, Integer, String, Date, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from libs.database import db

class Projects(db.Model):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True, index=True)
    legacy_id = Column(String(50), unique=True, index=True, nullable=False)
    dt_created = Column(Date, default=db.func.current_date())
    customer_id = Column(Integer, ForeignKey('customer.id'))
    start_datetime = Column(DateTime, default=db.func.now())
    status = Column(String, default='Ativo')
    notes = Column(String)
    amount = Column(Float)
    project_name = Column(String)
    
    customer = relationship('Customer', back_populates='projects')
    tasks = relationship('Tasks', back_populates='projects')

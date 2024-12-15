from sqlalchemy import Column, Integer, String, Date, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship
from datetime import date, datetime
from libs.database import db

class Customer(db.Model):
    __tablename__ = 'customer'
    
    id = Column(Integer, primary_key=True, index=True)
    legacy_id = Column(VARCHAR(50), unique=True, index=True, nullable=False)
    dt_created = Column(Date, default=date.today())
    status = Column(String, default='Ativo')
    name = Column(String)
    cnpj = Column(VARCHAR(14))
    
    __foreign_key__ = 'legacy_id'
    
    # Relações
    projects = relationship('Projects', back_populates='customer')
    tasks = relationship('Tasks', back_populates='customer')
    
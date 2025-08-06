from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.db.database import Base 
from typing import Optional, List

# Modelo SQLAlchemy ORM para la tabla 'companies'
class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    appointments = relationship("Appointment", back_populates="company")  # Relación con citas

# Modelos Pydantic para validación de entrada/salida de la API
class CompanyBase(BaseModel):
    name: str

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: Optional[str] = None # Para permitir actualizaciones parciales

class CompanyResponse(CompanyBase):
    id: int
    class Config:
        orm_mode = True # Esto permite que los modelos Pydantic lean datos de objetos ORM
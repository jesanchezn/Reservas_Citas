from sqlalchemy import Column, Integer, DateTime, Boolean
from app.database import Base

class Disponibilidad(Base):
    __tablename__ = "disponibilidad"

    id = Column(Integer, primary_key=True, index=True)
    fecha_hora = Column(DateTime, nullable=False, unique=True)
    disponible = Column(Boolean, default=True)

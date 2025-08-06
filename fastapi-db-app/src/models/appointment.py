# src/models/appointment.py
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.db.database import Base
from datetime import datetime
from typing import List, Optional
# Modelo SQLAlchemy ORM para la tabla 'appointments'
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id")) # Relaciona con la tabla de empresas
    start_time = Column(DateTime, index=True)
    end_time = Column(DateTime)
    is_booked = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Opcional, si un usuario la reserva

    # Relaciones (opcional, pero útil para ORM)
    company = relationship("Company", back_populates="appointments")
    user = relationship("User", back_populates="appointments")


# Modelos Pydantic para validación de entrada/salida de la API

# Modelo base para una cita
class AppointmentBase(BaseModel):
    company_id: int
    start_time: datetime
    end_time: datetime

# Modelo para crear una cita (puede ser una cita disponible o una a reservar)
class AppointmentCreate(AppointmentBase):
    pass

# Modelo para la respuesta de la API para una cita
class AppointmentResponse(AppointmentBase):
    id: int
    is_booked: bool
    user_id: Optional[int] = None
    class Config:
        orm_mode = True

# Modelo para la disponibilidad (para el frontend)
class AvailabilitySlot(BaseModel):
    date: str # Ej: "2024-08-05"
    times: List[str] # Ej: ["09:00", "10:00", "11:00"]

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Cita(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    fecha_hora = Column(DateTime, nullable=False)
    servicio = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey("users.id"))

    usuario = relationship("User")

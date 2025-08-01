from pydantic import BaseModel, Field
from datetime import datetime

class CitaCreate(BaseModel):
    fecha_hora: datetime = Field(..., description="Fecha y hora de la cita (ISO 8601)")
    servicio: str = Field(..., min_length=3, max_length=100, description="Nombre del servicio solicitado")

class CitaResponse(BaseModel):
    id: int
    fecha_hora: datetime
    servicio: str
    usuario_id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel, Field
from datetime import datetime

class DisponibilidadCreate(BaseModel):
    fecha_hora: datetime = Field(..., description="Fecha y hora disponible para agendar")

class DisponibilidadResponse(BaseModel):
    id: int
    fecha_hora: datetime
    disponible: bool

    class Config:
        orm_mode = True

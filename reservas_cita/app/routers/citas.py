from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.cita import CitaCreate, CitaResponse
from app.models import cita as cita_model, disponibilidad as dispo_model, user as user_model
from app.database import get_db
from app.services.auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/citas", tags=["citas"])

@router.post("/", response_model=CitaResponse)
def agendar_cita(cita: CitaCreate, db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    disponible = db.query(dispo_model.Disponibilidad).filter_by(fecha_hora=cita.fecha_hora, disponible=True).first()
    if not disponible:
        raise HTTPException(status_code=400, detail="Horario no disponible")

    nueva_cita = cita_model.Cita(
        fecha_hora=cita.fecha_hora,
        servicio=cita.servicio,
        usuario_id=current_user.id
    )
    db.add(nueva_cita)

    disponible.disponible = False
    db.commit()
    db.refresh(nueva_cita)
    return nueva_cita

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.disponibilidad import DisponibilidadCreate, DisponibilidadResponse
from app.models import disponibilidad as dispo_model
from app.database import get_db

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/disponibilidad", response_model=DisponibilidadResponse)
def agregar_disponibilidad(data: DisponibilidadCreate, db: Session = Depends(get_db)):
    # Verificar si ya existe una disponibilidad en esa fecha y hora
    existente = db.query(dispo_model.Disponibilidad).filter_by(fecha_hora=data.fecha_hora).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe disponibilidad en esa fecha y hora.")

    nueva = dispo_model.Disponibilidad(fecha_hora=data.fecha_hora)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/disponibilidad", response_model=list[DisponibilidadResponse])
def listar_disponibilidad(db: Session = Depends(get_db)):
    return db.query(dispo_model.Disponibilidad).order_by(dispo_model.Disponibilidad.fecha_hora).all()

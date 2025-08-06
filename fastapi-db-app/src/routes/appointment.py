# src/routes/appointment.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.models.appointment import Appointment, AppointmentCreate, AppointmentResponse, AvailabilitySlot
from datetime import datetime, timedelta
from typing import List, Dict

router = APIRouter()

# Endpoint para obtener horarios disponibles para una empresa y fecha específica
@router.get("/appointments/available_times/{company_id}", response_model=List[str])
def get_available_time_slots_for_date(
    company_id: int,
    date: str = Query(..., description="Fecha en formato YYYY-MM-DD"), # Parámetro de consulta para la fecha
    db: Session = Depends(get_db)
):
    try:
        selected_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD.")

    # Lógica para obtener citas disponibles de la base de datos para la empresa y fecha dadas.
    # Filtramos las citas que ya están reservadas para la empresa y fecha seleccionada.
    booked_appointments = db.query(Appointment.start_time).filter(
        Appointment.company_id == company_id,
        Appointment.start_time >= datetime.combine(selected_date, datetime.min.time()),
        Appointment.start_time <= datetime.combine(selected_date, datetime.max.time()),
        Appointment.is_booked == True
    ).all()
    
    # Convertimos los objetos datetime a strings de hora para fácil comparación
    booked_times = {slot.strftime("%H:%M") for slot, in booked_appointments}

    # Generar todos los posibles horarios de 9 AM a 5 PM, cada hora
    all_possible_slots = []
    for hour in range(9, 17): # De 9 AM (09) a 4 PM (16)
        all_possible_slots.append(f"{hour:02d}:00")

    # Filtrar horarios que ya estén reservados
    available_slots = [
        slot for slot in all_possible_slots if slot not in booked_times
    ]

    return available_slots

# Endpoint para crear/reservar una cita
@router.post("/appointments/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    # Verificar si la empresa existe
    from src.models.company import Company # Importar Company aquí para evitar circular imports
    company = db.query(Company).filter(Company.id == appointment.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    # Verificar si el slot ya está ocupado para esa empresa y hora
    existing_appointment = db.query(Appointment).filter(
        Appointment.company_id == appointment.company_id,
        Appointment.start_time == appointment.start_time,
        Appointment.is_booked == True
    ).first()
    
    if existing_appointment:
        raise HTTPException(status_code=400, detail="Time slot already booked for this company.")

    # Crear una nueva instancia de cita
    new_appointment = Appointment(
        company_id=appointment.company_id,
        start_time=appointment.start_time,
        end_time=appointment.end_time,
        is_booked=True # Asumimos que al crearla, ya está reservada
        # user_id=... si tienes autenticación de usuario y quieres asociar la cita
    )
    
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    
    return new_appointment

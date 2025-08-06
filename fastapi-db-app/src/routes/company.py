# src/routes/company.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.models.company import Company, CompanyCreate, CompanyResponse # Importa el modelo ORM y Pydantic

router = APIRouter()

# Endpoint para obtener todas las empresas desde la base de datos
@router.get("/companies/", response_model=list[CompanyResponse])
def get_all_companies(db: Session = Depends(get_db)):
    # Consulta todas las empresas en la base de datos
    companies = db.query(Company).all()
    return companies

# Endpoint para crear una nueva empresa en la base de datos
@router.post("/companies/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    # Verifica si ya existe una empresa con el mismo nombre
    db_company = db.query(Company).filter(Company.name == company.name).first()
    if db_company:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Esta empresa ya existe")

    # Crea una nueva instancia del modelo ORM Company
    new_company = Company(name=company.name)
    
    # Añade la nueva empresa a la sesión de la base de datos
    db.add(new_company)
    # Confirma la transacción
    db.commit()
    # Refresca el objeto para obtener el ID generado por la base de datos
    db.refresh(new_company)
    
    return new_company # Retorna el objeto de la empresa creada

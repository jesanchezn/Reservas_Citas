from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import timedelta, datetime

from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.token import Token
from app.models import user as user_model
from app.database import get_db
from app.config import JWT_SECRET
from app.services.email import enviar_correo  # <-- Import del servicio de correo

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=5)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(user_model.User).filter_by(email=user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    hashed_password = pwd_context.hash(user.password)
    new_user = user_model.User(
        nombre=user.nombre,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Enviar correo de confirmación
    try:
        enviar_correo(
            destinatario=new_user.email,
            asunto="Confirmación de registro",
            cuerpo=f"<h3>Hola {new_user.nombre},</h3><p>Tu cuenta ha sido registrada con éxito.</p>"
        )
    except Exception as e:
        print("Error al enviar correo:", e)

    return new_user

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(user_model.User).filter_by(email=user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = create_token({"email": db_user.email})
    return {"access_token": token, "token_type": "bearer"}

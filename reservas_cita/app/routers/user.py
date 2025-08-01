# app/routers/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.config import JWT_SECRET
from fastapi.security import OAuth2PasswordBearer
from fastapi import Request, Header

router = APIRouter(prefix="/users", tags=["users"])

# Definir el esquema de seguridad OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        email: str = payload.get("email")
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    
    user = db.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    return user

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Obtiene el usuario actual a partir del token de autenticación.
    """
    return current_user

# Nueva ruta para ver todos los usuarios
@router.get("/all_users", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """
    Obtiene y devuelve una lista de todos los usuarios registrados.
    """
    users = db.query(User).all()
    return users

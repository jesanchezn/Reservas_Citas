# src/models/user.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.db.database import Base # Importa el objeto Base desde tu configuración de base de datos
from pydantic import BaseModel
from typing import Optional, List # Asegúrate de importar Optional y List

# Modelo SQLAlchemy ORM para la tabla 'users'
# Esta clase define la estructura de la tabla 'users' en tu base de datos.
class User(Base):
    __tablename__ = "users" # Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String) # Almacena la contraseña hasheada

    # Relación con el modelo Appointment
    # Esto permite acceder a las citas de un usuario desde el objeto User.
    # 'back_populates' asegura una relación bidireccional.
    appointments = relationship("Appointment", back_populates="user")

# Modelos Pydantic para validación de entrada/salida de la API
# Estos modelos definen la forma de los datos que tu API espera recibir
# y la forma de los datos que tu API enviará como respuesta.

# Modelo base para los atributos de un usuario
class UserBase(BaseModel):
    username: str
    email: str

# Modelo para crear un nuevo usuario (incluye la contraseña sin hashear para la entrada)
class UserCreate(UserBase):
    password: str # La contraseña se enviará aquí y se hasheará en el endpoint

# Modelo para actualizar un usuario (todos los campos son opcionales para permitir actualizaciones parciales)
class UserUpdate(BaseModel):
    username: Optional[str] = None # ¡CORREGIDO: Usando Optional!
    email: Optional[str] = None   # ¡CORREGIDO: Usando Optional!
    password: Optional[str] = None # ¡CORREGIDO: Usando Optional!

# Modelo para la respuesta de la API (no incluye la contraseña por seguridad)
class UserResponse(UserBase):
    id: int # Incluye el ID del usuario al devolver la respuesta
    class Config:
        # orm_mode = True (Pydantic V1)
        # from_attributes = True (Pydantic V2)
        # Esta configuración permite que Pydantic lea datos directamente de objetos ORM de SQLAlchemy.
        from_attributes = True # Usar from_attributes para Pydantic V2+

# Modelo para la solicitud de inicio de sesión
class LoginRequest(BaseModel):
    email: str
    password: str

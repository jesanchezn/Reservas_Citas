from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=50, description="Nombre completo del usuario")
    email: EmailStr = Field(..., description="Correo electrónico válido")
    password: str = Field(..., min_length=6, max_length=100, description="Contraseña segura")

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    password: str = Field(..., min_length=6, max_length=100, description="Contraseña del usuario")

class UserResponse(BaseModel):
    id: int
    nombre: str
    email: EmailStr

    class Config:
        orm_mode = True

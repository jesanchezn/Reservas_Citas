from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import auth, citas, admin, user  # Asegúrate de tener routers/user.py

# Crear las tablas en la base de datos (solo si no existen)
Base.metadata.create_all(bind=engine)

# Crear la aplicación FastAPI
app = FastAPI(title="Sistema de Reservas de Citas")

# Configurar CORS para permitir conexiones del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringirlo a tu dominio en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas de la API
app.include_router(auth.router)
app.include_router(citas.router)
app.include_router(admin.router)
app.include_router(user.router)  # <--- Agregada la ruta del usuario actual

# Ejecutar con: python main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

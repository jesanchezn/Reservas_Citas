from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.db.database import engine
from src.routes import user, company, appointment

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes poner ["file://"] si solo usas archivos locales
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include user routes
app.include_router(user.router)
app.include_router(company.router)
app.include_router(appointment.router)

# Create the database tables
@app.on_event("startup")
def startup_event():
    import src.db.database as db
    db.create_database()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}
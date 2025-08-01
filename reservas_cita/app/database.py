from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Ruta al archivo SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./reservas.db"

# Conexión con SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 🔧 Función para obtener la sesión de base de datos
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

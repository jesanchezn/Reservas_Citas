import os
from dotenv import load_dotenv

load_dotenv()


JWT_SECRET = os.getenv("JWT_SECRET")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


if not JWT_SECRET:
    raise ValueError("JWT_SECRET no está definido en el archivo .env")

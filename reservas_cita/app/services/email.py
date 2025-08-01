import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import SMTP_EMAIL, SMTP_PASSWORD

def enviar_correo(destinatario: str, asunto: str, cuerpo: str):
    mensaje = MIMEMultipart()
    mensaje["From"] = SMTP_EMAIL
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto

    mensaje.attach(MIMEText(cuerpo, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.starttls()
            servidor.login(SMTP_EMAIL, SMTP_PASSWORD)
            servidor.sendmail(SMTP_EMAIL, destinatario, mensaje.as_string())
        print("Correo enviado con éxito")
    except Exception as e:
        print("Error al enviar el correo:", e)

import smtplib
from email.mime.text import MIMEText
from config import EMAIL_ORIGEN, EMAIL_DESTINO, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT


def enviar_email(nuevos_pisos):
    if not nuevos_pisos:
        return

    contenido = "Se han detectado nuevos pisos:\n\n"

    for piso in nuevos_pisos:
        contenido += f"Título: {piso['titulo']}\n"
        contenido += f"Precio: {piso['precio']}\n"
        contenido += f"Zona: {piso['zona']}\n"
        contenido += f"Enlace: {piso['enlace']}\n"
        contenido += "-" * 50 + "\n"

    msg = MIMEText(contenido, "plain", "utf-8")
    msg["Subject"] = "Nuevos pisos detectados"
    msg["From"] = EMAIL_ORIGEN
    msg["To"] = EMAIL_DESTINO

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ORIGEN, EMAIL_PASSWORD)
        server.send_message(msg)
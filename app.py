from flask import Flask, render_template, redirect, url_for, flash, session
from database import (
    init_db,
    init_config_table,
    obtener_pisos,
    guardar_ultima_actualizacion,
    obtener_ultima_actualizacion,
    contar_pisos,
)
from scraper import ejecutar_scraping
from notifier import enviar_email
from datetime import datetime

app = Flask(__name__)
app.secret_key = "clave_secreta_para_desarrollo"


@app.route("/")
def index():
    pisos = obtener_pisos()
    ultima_actualizacion = obtener_ultima_actualizacion()
    total_pisos = contar_pisos()
    total_nuevos = session.pop("total_nuevos", None)

    return render_template(
        "index.html",
        pisos=pisos,
        ultima_actualizacion=ultima_actualizacion,
        total_pisos=total_pisos,
        total_nuevos=total_nuevos,
    )


@app.route("/actualizar")
def actualizar():
    try:
        resultado = ejecutar_scraping()
        nuevos_pisos = resultado["nuevos"]
        total_nuevos = resultado["total_nuevos"]
        total_filtrados = resultado["total_filtrados"]

        session["total_nuevos"] = total_nuevos

        fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        guardar_ultima_actualizacion(fecha_hora)

        if total_nuevos > 0:
            try:
                enviar_email(nuevos_pisos)
            except Exception as email_error:
                print(f"Error enviando email: {email_error}")

            flash(
                f"Actualización completada. Se han añadido {total_nuevos} pisos nuevos de {total_filtrados} anuncios filtrados.",
                "success",
            )
        else:
            flash(
                f"Actualización completada. No se han encontrado pisos nuevos. Anuncios válidos filtrados: {total_filtrados}.",
                "info",
            )

    except Exception as e:
        print(f"Error al actualizar: {e}")
        flash(f"Ha ocurrido un error al actualizar los pisos: {e}", "error")

    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    init_config_table()
    app.run(debug=True)

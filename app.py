from flask import Flask, render_template, redirect, url_for, flash
from database import init_db, obtener_pisos
from scraper import ejecutar_scraping
from notifier import enviar_email

app = Flask(__name__)
app.secret_key = "clave_secreta_para_desarrollo"


@app.route("/")
def index():
    pisos = obtener_pisos()
    return render_template("index.html", pisos=pisos)


@app.route("/actualizar")
def actualizar():
    try:
        resultado = ejecutar_scraping()
        nuevos_pisos = resultado["nuevos"]
        total_nuevos = resultado["total_nuevos"]
        total_filtrados = resultado["total_filtrados"]

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
    app.run(debug=True)

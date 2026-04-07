import re
import requests
from bs4 import BeautifulSoup
from database import piso_existe, guardar_piso
from config import MODO_PRUEBA, URL_OBJETIVO, PRECIO_MAXIMO, ZONAS_PERMITIDAS


def obtener_html_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.text


def obtener_html_local(ruta_archivo):
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        return f.read()


def obtener_html():
    if MODO_PRUEBA:
        return obtener_html_local("prueba.html")
    return obtener_html_url(URL_OBJETIVO)


def limpiar_precio(precio_texto):
    """
    Convierte algo como '150000 €' en 150000
    """
    numeros = re.sub(r"[^\d]", "", precio_texto)
    if numeros:
        return int(numeros)
    return None


def zona_permitida(zona):
    if not ZONAS_PERMITIDAS:
        return True
    return zona in ZONAS_PERMITIDAS


def precio_permitido(precio_texto):
    precio_num = limpiar_precio(precio_texto)
    if precio_num is None:
        return False
    return precio_num <= PRECIO_MAXIMO


def extraer_pisos(html):
    soup = BeautifulSoup(html, "html.parser")
    resultados = []

    anuncios = soup.select(".anuncio")

    for anuncio in anuncios:
        titulo_elem = anuncio.select_one(".titulo")
        precio_elem = anuncio.select_one(".precio")
        zona_elem = anuncio.select_one(".zona")
        enlace_elem = anuncio.select_one("a")

        titulo = titulo_elem.get_text(strip=True) if titulo_elem else "Sin título"
        precio = precio_elem.get_text(strip=True) if precio_elem else "Sin precio"
        zona = zona_elem.get_text(strip=True) if zona_elem else "Sin zona"
        enlace = enlace_elem["href"].strip() if enlace_elem and enlace_elem.has_attr("href") else ""

        if enlace and not enlace.startswith("http"):
            enlace = "https://ejemplo.com" + enlace

        piso = {
            "titulo": titulo,
            "precio": precio,
            "zona": zona,
            "enlace": enlace
        }

        if precio_permitido(precio) and zona_permitida(zona):
            resultados.append(piso)

    return resultados


def guardar_nuevos_pisos(pisos):
    nuevos = []

    for piso in pisos:
        if piso["enlace"] and not piso_existe(piso["enlace"]):
            guardar_piso(
                piso["titulo"],
                piso["precio"],
                piso["zona"],
                piso["enlace"]
            )
            nuevos.append(piso)

    return nuevos


def ejecutar_scraping():
    html = obtener_html()
    pisos_filtrados = extraer_pisos(html)
    nuevos = guardar_nuevos_pisos(pisos_filtrados)

    return {
        "total_filtrados": len(pisos_filtrados),
        "nuevos": nuevos,
        "total_nuevos": len(nuevos)
    }
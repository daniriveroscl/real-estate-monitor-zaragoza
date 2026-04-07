import sqlite3

DB_NAME = "pisos.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pisos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            precio TEXT,
            zona TEXT,
            enlace TEXT UNIQUE,
            fecha_detectado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def piso_existe(enlace):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM pisos WHERE enlace = ?", (enlace,))
    resultado = cursor.fetchone()

    conn.close()
    return resultado is not None


def guardar_piso(titulo, precio, zona, enlace):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pisos (titulo, precio, zona, enlace)
        VALUES (?, ?, ?, ?)
    """, (titulo, precio, zona, enlace))

    conn.commit()
    conn.close()


def obtener_pisos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM pisos
        ORDER BY fecha_detectado DESC, id DESC
    """)
    pisos = cursor.fetchall()

    conn.close()
    return pisos
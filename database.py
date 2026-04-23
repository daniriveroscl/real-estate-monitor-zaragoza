import sqlite3

DB_NAME = "pisos.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pisos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            precio TEXT,
            zona TEXT,
            enlace TEXT UNIQUE,
            fecha_detectado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

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

    cursor.execute(
        """
        INSERT INTO pisos (titulo, precio, zona, enlace)
        VALUES (?, ?, ?, ?)
    """,
        (titulo, precio, zona, enlace),
    )

    conn.commit()
    conn.close()


def obtener_pisos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM pisos
        ORDER BY fecha_detectado DESC, id DESC
    """
    )
    pisos = cursor.fetchall()

    conn.close()
    return pisos


def init_config_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS config (
            clave TEXT PRIMARY KEY,
            valor TEXT
        )
    """
    )

    conn.commit()
    conn.close()


def guardar_ultima_actualizacion(fecha_hora):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO config (clave, valor)
        VALUES ('ultima_actualizacion', ?)
        ON CONFLICT(clave) DO UPDATE SET valor=excluded.valor
    """,
        (fecha_hora,),
    )

    conn.commit()
    conn.close()


def obtener_ultima_actualizacion():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT valor FROM config WHERE clave = 'ultima_actualizacion'
    """
    )
    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return resultado["valor"]
    return None


def contar_pisos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS total FROM pisos")
    resultado = cursor.fetchone()

    conn.close()
    return resultado["total"]

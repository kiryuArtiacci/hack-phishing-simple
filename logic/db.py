import sqlite3
from contextlib import contextmanager


@contextmanager
def get_db_connection():
    """
    Un context manager que maneja la apertura y cierre de la conexión a la BD.
    Garantiza que la conexión siempre se cierre, incluso si hay errores.
    """
    conn = None
    try:
        conn = sqlite3.connect("hiring_group.db", timeout=10)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        yield conn
    except sqlite3.Error as e:
        print(f"Error de conexión a la base de datos: {e}")
        raise
    finally:
        if conn:
            conn.close()

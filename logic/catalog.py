import sqlite3
from datetime import datetime
from .db import get_db_connection


def get_catalogo(tabla, id_col, nombre_col):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if isinstance(nombre_col, list):
            nombre_col_str = ", ".join(nombre_col)
            order_col = nombre_col[0]
        else:
            nombre_col_str = nombre_col
            order_col = nombre_col

        cursor.execute(
            f"SELECT {id_col}, {nombre_col_str} FROM {tabla} ORDER BY {order_col}"
        )
        return cursor.fetchall()


def crear_item_catalogo(tabla, nombre_col, nombre_valor):
    try:
        with get_db_connection() as conn:
            conn.execute(
                f"INSERT INTO {tabla} ({nombre_col}) VALUES (?)", (nombre_valor,)
            )
            conn.commit()
            return True, "Elemento agregado con éxito."
    except sqlite3.IntegrityError:
        return False, f"Error: Ese valor ya existe en {tabla}."
    except sqlite3.Error as e:
        return False, f"Error inesperado: {e}"


def actualizar_item_catalogo(tabla, id_col, nombre_col, id_valor, nuevo_nombre):
    try:
        with get_db_connection() as conn:
            conn.execute(
                f"UPDATE {tabla} SET {nombre_col} = ? WHERE {id_col} = ?",
                (nuevo_nombre, id_valor),
            )
            conn.commit()
            return True, "Elemento actualizado con éxito."
    except sqlite3.Error as e:
        return False, f"Error al actualizar: {e}"


def eliminar_item_catalogo(tabla, id_col, id_valor):
    try:
        with get_db_connection() as conn:
            conn.execute(f"DELETE FROM {tabla} WHERE {id_col} = ?", (id_valor,))
            conn.commit()
            return True, "Elemento eliminado con éxito."
    except sqlite3.IntegrityError:
        return False, "Error: El elemento está en uso y no se puede eliminar."
    except sqlite3.Error as e:
        return False, f"Error inesperado: {e}"

import sqlite3
from .db import get_db_connection


def login_usuario(email, password):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT ID_Usuario, Email, Tipo_Usuario, Estatus FROM Usuarios WHERE Email = ? AND Password = ?"
        cursor.execute(query, (email, password))
        usuario_data = cursor.fetchone()

        if not usuario_data:
            return None, None

        usuario = dict(usuario_data)
        if usuario["Estatus"] != "Activo":
            return None, None

        if usuario["Tipo_Usuario"] == "Postulante":
            query_contrato = "SELECT c.ID_Contrato FROM Contratos c JOIN Postulaciones p ON c.ID_Postulacion = p.ID_Postulacion WHERE p.ID_Postulante = ? AND c.Estatus = 'Activo'"
            cursor.execute(query_contrato, (usuario["ID_Usuario"],))
            if cursor.fetchone():
                usuario["Tipo_Usuario"] = "Contratado"

        return usuario, usuario["Tipo_Usuario"]


def registrar_usuario_db(tipo_usuario, datos):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            sql_usuario = (
                "INSERT INTO Usuarios (Email, Password, Tipo_Usuario) VALUES (?, ?, ?)"
            )
            cursor.execute(
                sql_usuario, (datos["Email"], datos["Contraseña"], tipo_usuario)
            )
            id_usuario = cursor.lastrowid

            if tipo_usuario == "Empresa":
                sql_empresa = "INSERT INTO Empresas (ID_Empresa, Nombre_Empresa, RIF, Sector_Industrial, Persona_Contacto, Telefono_Contacto, Email_Contacto) VALUES (?, ?, ?, ?, ?, ?, ?)"
                valores = (
                    id_usuario,
                    datos["Nombre Empresa"],
                    datos["RIF"],
                    datos["Sector"],
                    datos["Persona de Contacto"],
                    datos["Teléfono de Contacto"],
                    datos["Email de Contacto"],
                )
                cursor.execute(sql_empresa, valores)
            elif tipo_usuario == "Postulante":
                sql_postulante = "INSERT INTO Postulantes (ID_Postulante, Nombres, Apellidos, Cedula_Identidad, Telefono, ID_Universidad) VALUES (?, ?, ?, ?, ?, ?)"
                valores = (
                    id_usuario,
                    datos["Nombres"],
                    datos["Apellidos"],
                    datos["Cédula"],
                    datos["Teléfono"],
                    datos["ID_Universidad"],
                )
                cursor.execute(sql_postulante, valores)

            conn.commit()
            return True, f"Usuario tipo '{tipo_usuario}' creado con éxito."
    except sqlite3.IntegrityError as e:
        return False, f"Error de integridad: El Email, RIF o Cédula ya existen. ({e})"
    except sqlite3.Error as e:
        return False, f"Error inesperado al crear usuario: {e}"


def actualizar_usuario_db(id_usuario, tipo_usuario, datos):
    try:
        with get_db_connection() as conn:
            if "Contraseña" in datos and datos["Contraseña"]:
                conn.execute(
                    "UPDATE Usuarios SET Password = ? WHERE ID_Usuario = ?",
                    (datos["Contraseña"], id_usuario),
                )
            if tipo_usuario == "Empresa":
                sql = "UPDATE Empresas SET Nombre_Empresa = ?, Sector_Industrial = ?, Persona_Contacto = ?, Telefono_Contacto = ?, Email_Contacto = ? WHERE ID_Empresa = ?"
                valores = (
                    datos["Nombre Empresa"],
                    datos["Sector"],
                    datos["Persona de Contacto"],
                    datos["Teléfono de Contacto"],
                    datos["Email de Contacto"],
                    id_usuario,
                )
                conn.execute(sql, valores)
            elif tipo_usuario in ["Postulante", "Contratado"]:
                sql = "UPDATE Postulantes SET Nombres = ?, Apellidos = ?, Telefono = ?, ID_Universidad = ? WHERE ID_Postulante = ?"
                valores = (
                    datos["Nombres"],
                    datos["Apellidos"],
                    datos["Teléfono"],
                    datos["ID_Universidad"],
                    id_usuario,
                )
                conn.execute(sql, valores)
            conn.commit()
            return True, "Datos actualizados con éxito."
    except sqlite3.Error as e:
        return False, f"Error al actualizar los datos: {e}"


def eliminar_usuario_db(id_usuario):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Usuarios WHERE ID_Usuario = ?", (id_usuario,))
            conn.commit()
            if cursor.rowcount > 0:
                return True, "Usuario eliminado con éxito."
            else:
                return False, "No se encontró el usuario para eliminar."
    except sqlite3.IntegrityError as e:
        return (
            False,
            f"Error de integridad: No se puede eliminar. Revise contratos o postulaciones asociadas. ({e})",
        )
    except sqlite3.Error as e:
        return False, f"Error inesperado al eliminar el usuario: {e}"


def hay_usuarios_registrados():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM Usuarios LIMIT 1")
            return cursor.fetchone() is not None
    except sqlite3.Error:
        return False


def get_single_postulante(id_postulante):
    with get_db_connection() as conn:
        return conn.execute(
            "SELECT * FROM Postulantes WHERE ID_Postulante = ?", (id_postulante,)
        ).fetchone()


def get_single_empresa(id_empresa):
    with get_db_connection() as conn:
        return conn.execute(
            "SELECT * FROM Empresas WHERE ID_Empresa = ?", (id_empresa,)
        ).fetchone()

import sqlite3
from .db import get_db_connection

def aplicar_a_vacante_db(id_postulante, id_vacante):
    try:
        with get_db_connection() as conn:
            sql = "INSERT INTO Postulaciones (ID_Postulante, ID_Vacante) VALUES (?, ?)"
            conn.execute(sql, (id_postulante, id_vacante))
            conn.commit()
            return True, "¡Postulación exitosa!"
    except sqlite3.IntegrityError:
        return False, "Error: Ya te has postulado a esta vacante."
    except sqlite3.Error as e:
        return False, f"Error inesperado: {e}"


def get_postulaciones_para_contratar():
    with get_db_connection() as conn:
        return conn.execute("""SELECT post.ID_Postulacion, p.Nombres, p.Apellidos, v.Cargo_Vacante 
                               FROM Postulaciones post JOIN Postulantes p ON post.ID_Postulante = p.ID_Postulante 
                               JOIN Vacantes v ON post.ID_Vacante = v.ID_Vacante 
                               WHERE post.Estatus IN ('Recibida', 'En Revision')""").fetchall()



def get_postulaciones_por_postulante(id_postulante):
    with get_db_connection() as conn:
        query = "SELECT v.Cargo_Vacante, v.Salario_Ofrecido, e.Nombre_Empresa, strftime('%Y-%m-%d %H:%M', p.Fecha_Postulacion) as Fecha_Postulacion, p.Estatus FROM Postulaciones p JOIN Vacantes v ON p.ID_Vacante = v.ID_Vacante JOIN Empresas e ON v.ID_Empresa = e.ID_Empresa WHERE p.ID_Postulante = ? ORDER BY p.Fecha_Postulacion DESC"
        return conn.execute(query, (id_postulante,)).fetchall()

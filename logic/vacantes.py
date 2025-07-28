import sqlite3
from .db import get_db_connection


def crear_vacante_db(id_empresa, cargo, descripcion, salario, id_profesion):
    try:
        with get_db_connection() as conn:
            sql = 'INSERT INTO Vacantes (ID_Empresa, Cargo_Vacante, Descripcion_Perfil, Salario_Ofrecido, ID_Profesion) VALUES (?, ?, ?, ?, ?)'
            conn.execute(
                sql, (id_empresa, cargo, descripcion, salario, id_profesion)
            )
            conn.commit()
            return True, 'Vacante creada con éxito.'
    except sqlite3.Error as e:
        return False, f'Error al crear vacante: {e}'


def get_active_vacantes(filtro_area=None, filtro_prof=None, sort_salary=None):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = """SELECT v.ID_Vacante, v.Cargo_Vacante, v.Descripcion_Perfil, v.Salario_Ofrecido, 
                   e.Nombre_Empresa, p.Nombre_Profesion, ac.Nombre_Area
                   FROM Vacantes v JOIN Empresas e ON v.ID_Empresa = e.ID_Empresa JOIN Profesiones p ON v.ID_Profesion = p.ID_Profesion
                   LEFT JOIN Areas_Conocimiento ac ON p.ID_Area_Conocimiento = ac.ID_Area_Conocimiento
                   WHERE v.Estatus = 'Activa'"""
        params = []
        if filtro_area:
            query += ' AND ac.ID_Area_Conocimiento = ?'
            params.append(filtro_area)
        if filtro_prof:
            query += ' AND p.ID_Profesion = ?'
            params.append(filtro_prof)
        if sort_salary:
            query += f' ORDER BY v.Salario_Ofrecido {sort_salary}'
        cursor.execute(query, params)
        return cursor.fetchall()


def get_vacantes_por_empresa(id_empresa):
    with get_db_connection() as conn:
        return conn.execute(
            'SELECT ID_Vacante, Cargo_Vacante, Descripcion_Perfil, Salario_Ofrecido, Estatus FROM Vacantes WHERE ID_Empresa = ?',
            (id_empresa,),
        ).fetchall()


def actualizar_vacante_db(id_vacante, cargo, descripcion, salario, estatus):
    try:
        with get_db_connection() as conn:
            sql = 'UPDATE Vacantes SET Cargo_Vacante = ?, Descripcion_Perfil = ?, Salario_Ofrecido = ?, Estatus = ? WHERE ID_Vacante = ?'
            conn.execute(
                sql, (cargo, descripcion, salario, estatus, id_vacante)
            )
            conn.commit()
            return True, 'Vacante actualizada con éxito.'
    except sqlite3.Error as e:
        return False, f'Error al actualizar la vacante: {e}'


def eliminar_vacante_db(id_vacante):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT COUNT(*) as count FROM Postulaciones WHERE ID_Vacante = ?',
                (id_vacante,),
            )
            if cursor.fetchone()['count'] > 0:
                return (
                    False,
                    "No se puede eliminar la vacante porque tiene postulaciones. Considere marcarla como 'Cerrada' o 'Inactiva'.",
                )
            cursor.execute(
                'DELETE FROM Vacantes WHERE ID_Vacante = ?', (id_vacante,)
            )
            conn.commit()
            return True, 'Vacante eliminada con éxito.'
    except sqlite3.Error as e:
        return False, f'Error al eliminar la vacante: {e}'

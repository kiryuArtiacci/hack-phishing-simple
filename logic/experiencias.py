import sqlite3
from .db import get_db_connection


def crear_experiencia_db(id_postulante, datos):
    try:
        with get_db_connection() as conn:
            sql = 'INSERT INTO Experiencias_Laborales (ID_Postulante, Empresa, Cargo_Ocupado, Fecha_Inicio, Fecha_Fin, Descripcion) VALUES (?, ?, ?, ?, ?, ?)'
            fecha_fin = datos.get('Fecha Fin (YYYY-MM-DD, opcional)') or None
            conn.execute(
                sql,
                (
                    id_postulante,
                    datos['Empresa'],
                    datos['Cargo'],
                    datos['Fecha Inicio (YYYY-MM-DD)'],
                    fecha_fin,
                    datos['Descripción'],
                ),
            )
            conn.commit()
            return True, 'Experiencia agregada.'
    except sqlite3.Error as e:
        return False, f'Error al agregar experiencia: {e}'


def get_experiencias_db(id_postulante):
    with get_db_connection() as conn:
        return conn.execute(
            'SELECT ID_Experiencia, Empresa, Cargo_Ocupado, Fecha_Inicio, Fecha_Fin, Descripcion FROM Experiencias_Laborales WHERE ID_Postulante = ? ORDER BY Fecha_Inicio DESC',
            (id_postulante,),
        ).fetchall()


def eliminar_experiencia_db(id_experiencia):
    try:
        with get_db_connection() as conn:
            conn.execute(
                'DELETE FROM Experiencias_Laborales WHERE ID_Experiencia = ?',
                (id_experiencia,),
            )
            conn.commit()
            return True, 'Experiencia eliminada.'
    except sqlite3.Error as e:
        return False, f'Error al eliminar: {e}'

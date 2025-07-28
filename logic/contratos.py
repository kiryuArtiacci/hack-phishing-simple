import sqlite3
from .db import get_db_connection


def contratar_postulante_db(id_postulacion, datos):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            sql_contrato = """INSERT INTO Contratos (ID_Postulacion, Fecha_Contratacion, Tipo_Contrato, Salario_Acordado, Tipo_Sangre, 
                              Contacto_Emergencia_Nombre, Contacto_Emergencia_Telefono, Numero_Cuenta, ID_Banco) 
                              VALUES (?, date('now'), ?, ?, ?, ?, ?, ?, ?)"""
            valores = (
                id_postulacion,
                datos['Tipo_Contrato'],
                datos['Salario_Acordado'],
                datos['Tipo_Sangre'],
                datos['Contacto_Emergencia_Nombre'],
                datos['Contacto_Emergencia_Telefono'],
                datos['Numero_Cuenta'],
                datos['ID_Banco'],
            )
            cursor.execute(sql_contrato, valores)
            cursor.execute(
                'SELECT ID_Vacante FROM Postulaciones WHERE ID_Postulacion = ?',
                (id_postulacion,),
            )
            id_vacante = cursor.fetchone()['ID_Vacante']
            cursor.execute(
                "UPDATE Vacantes SET Estatus = 'Cerrada' WHERE ID_Vacante = ?",
                (id_vacante,),
            )
            cursor.execute(
                "UPDATE Postulaciones SET Estatus = 'Aceptada' WHERE ID_Postulacion = ?",
                (id_postulacion,),
            )
            conn.commit()
            return True, 'Contratación exitosa.'
    except sqlite3.Error as e:
        return False, f'Error al contratar: {e}'

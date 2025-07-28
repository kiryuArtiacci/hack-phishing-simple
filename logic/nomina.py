import sqlite3
from .db import get_db_connection


def ejecutar_nomina_db(id_empresa, mes, anio):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            check_query = "SELECT ID_Nomina FROM Nominas WHERE ID_Empresa = ? AND Mes = ? AND Anio = ?"
            cursor.execute(check_query, (id_empresa, mes, anio))
            if cursor.fetchone():
                return (
                    False,
                    "Ya se generó una nómina para esta empresa en este periodo.",
                    None,
                )
            sql_nomina = "INSERT INTO Nominas (ID_Empresa, Mes, Anio) VALUES (?, ?, ?)"
            cursor.execute(sql_nomina, (id_empresa, mes, anio))
            id_nomina = cursor.lastrowid
            sql_contratos = "SELECT c.ID_Contrato, c.Salario_Acordado FROM Contratos c JOIN Postulaciones post ON c.ID_Postulacion = post.ID_Postulacion JOIN Vacantes v ON post.ID_Vacante = v.ID_Vacante WHERE v.ID_Empresa = ? AND c.Estatus = 'Activo'"
            cursor.execute(sql_contratos, (id_empresa,))
            contratos = cursor.fetchall()
            if not contratos:
                conn.rollback()
                return False, "No hay empleados activos para esta empresa.", None
            for contrato in contratos:
                salario = contrato["Salario_Acordado"]
                ded_inces, ded_ivss, comision = (
                    float(salario) * 0.005,
                    float(salario) * 0.01,
                    float(salario) * 0.02,
                )
                neto = float(salario) - ded_inces - ded_ivss
                sql_recibo = "INSERT INTO Recibos (ID_Nomina, ID_Contrato, Salario_Base, Monto_Deduccion_INCES, Monto_Deduccion_IVSS, Comision_Hiring_Group, Salario_Neto_Pagado, Fecha_Pago) VALUES (?, ?, ?, ?, ?, ?, ?, date('now'))"
                cursor.execute(
                    sql_recibo,
                    (
                        id_nomina,
                        contrato["ID_Contrato"],
                        salario,
                        ded_inces,
                        ded_ivss,
                        comision,
                        neto,
                    ),
                )
            conn.commit()
            return (
                True,
                f"Nómina generada con éxito para {len(contratos)} empleado(s).",
                id_nomina,
            )
    except sqlite3.Error as e:
        conn.rollback()
        return False, f"Error al generar nómina: {e}", None


def get_recibos_por_contratado(id_postulante, mes=None, anio=None):
    with get_db_connection() as conn:
        query = "SELECT r.Fecha_Pago, r.Salario_Base, r.Salario_Neto_Pagado, n.Mes, n.Anio FROM Recibos r JOIN Nominas n ON r.ID_Nomina = n.ID_Nomina JOIN Contratos c ON r.ID_Contrato = c.ID_Contrato JOIN Postulaciones p ON c.ID_Postulacion = p.ID_Postulacion WHERE p.ID_Postulante = ?"
        params = [id_postulante]
        if mes:
            query += " AND n.Mes = ?"
            params.append(mes)
        if anio:
            query += " AND n.Anio = ?"
            params.append(anio)
        query += " ORDER BY n.Anio DESC, n.Mes DESC"
        return conn.execute(query, params).fetchall()


def get_nomina_reporte_db(id_empresa, mes, anio):
    with get_db_connection() as conn:
        query = """SELECT (p.Nombres || ' ' || p.Apellidos) AS Empleado, p.Cedula_Identidad, rec.Salario_Base
                   FROM Recibos rec JOIN Nominas nom ON rec.ID_Nomina = nom.ID_Nomina
                   JOIN Contratos c ON rec.ID_Contrato = c.ID_Contrato JOIN Postulaciones post ON c.ID_Postulacion = post.ID_Postulacion
                   JOIN Postulantes p ON post.ID_Postulante = p.ID_Postulante
                   WHERE nom.ID_Empresa = ? AND nom.Mes = ? AND nom.Anio = ?"""
        return conn.execute(query, (id_empresa, mes, anio)).fetchall()


def get_toda_nomina_reporte_db():
    with get_db_connection() as conn:
        query = """SELECT e.Nombre_Empresa, nom.Mes, nom.Anio, SUM(rec.Salario_Base) as Total_Nomina
                   FROM Recibos rec JOIN Nominas nom ON rec.ID_Nomina = nom.ID_Nomina
                   JOIN Empresas e ON nom.ID_Empresa = e.ID_Empresa
                   GROUP BY e.Nombre_Empresa, nom.Mes, nom.Anio ORDER BY e.Nombre_Empresa, nom.Anio DESC, nom.Mes DESC"""
        return conn.execute(query).fetchall()


def get_nomina_generada_detalle_db(id_nomina):
    with get_db_connection() as conn:
        query = """SELECT (p.Nombres || ' ' || p.Apellidos) AS Empleado, p.Cedula_Identidad, rec.Salario_Base,
                   (rec.Monto_Deduccion_INCES + rec.Monto_Deduccion_IVSS) as Total_Deducciones, rec.Salario_Neto_Pagado
                   FROM Recibos rec JOIN Contratos c ON rec.ID_Contrato = c.ID_Contrato 
                   JOIN Postulaciones post ON c.ID_Postulacion = post.ID_Postulacion
                   JOIN Postulantes p ON post.ID_Postulante = p.ID_Postulante
                   WHERE rec.ID_Nomina = ? ORDER BY Empleado"""
        return conn.execute(query, (id_nomina,)).fetchall()

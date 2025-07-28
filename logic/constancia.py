from datetime import datetime
from .db import get_db_connection


def get_datos_constancia(id_postulante):
    with get_db_connection() as conn:
        query = """SELECT p.Nombres, p.Apellidos, c.Fecha_Contratacion, c.Salario_Acordado, 
                   v.Cargo_Vacante, e.Nombre_Empresa 
                   FROM Contratos c JOIN Postulaciones post ON c.ID_Postulacion = post.ID_Postulacion
                   JOIN Postulantes p ON post.ID_Postulante = p.ID_Postulante
                   JOIN Vacantes v ON post.ID_Vacante = v.ID_Vacante
                   JOIN Empresas e ON v.ID_Empresa = e.ID_Empresa
                   WHERE p.ID_Postulante = ? AND c.Estatus = 'Activo'"""
        datos = conn.execute(query, (id_postulante,)).fetchone()
        if not datos:
            return None
        meses_es = (
            'Enero',
            'Febrero',
            'Marzo',
            'Abril',
            'Mayo',
            'Junio',
            'Julio',
            'Agosto',
            'Septiembre',
            'Octubre',
            'Noviembre',
            'Diciembre',
        )
        fecha_contrato = datetime.strptime(
            datos['Fecha_Contratacion'], '%Y-%m-%d'
        )
        fecha_hoy = datetime.now()
        fecha_inicio_str = f'{fecha_contrato.day} de {meses_es[fecha_contrato.month - 1]} de {fecha_contrato.year}'
        fecha_actual_str = f'{fecha_hoy.day} de {meses_es[fecha_hoy.month - 1]} de {fecha_hoy.year}'
        nombre_completo = f"{datos['Nombres']} {datos['Apellidos']}"
        salario_str = f"{float(datos['Salario_Acordado']):.2f}"
        return (
            f'                 A QUIEN PUEDA INTERESAR\n\n'
            f'Por medio de la presente la empresa HIRING GROUP hace constar que el ciudadano(a)\n'
            f'{nombre_completo}, labora con nosotros desde {fecha_inicio_str}, cumpliendo\n'
            f"funciones en el cargo de {datos['Cargo_Vacante']} en la empresa {datos['Nombre_Empresa']}, devengando un\n"
            f'salario mensual de {salario_str}.\n\n'
            f'Constancia que se pide por la parte interesada en la ciudad de Puerto Ordaz en fecha\n'
            f'{fecha_actual_str}'
        )

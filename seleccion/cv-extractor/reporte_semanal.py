#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reporte Semanal de Seleccion - Pescados La Carihuela
Genera PDF automatico cada lunes a las 05:00 (hora España)
"""

import os
import pymysql
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Para PDF
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT

load_dotenv()

# Configuracion BD
DB_CONFIG = {
    'host': os.getenv('DB_HOST', '192.168.1.133'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'gestion.pescadoslacarihuela.es'),
    'charset': 'utf8mb4'
}


def get_connection():
    """Obtener conexion a la base de datos"""
    return pymysql.connect(**DB_CONFIG)


def get_semana_actual(fecha=None):
    """Obtener informacion de la semana actual desde la tabla calendario_anual"""
    if fecha is None:
        fecha = datetime.now().date()

    conn = get_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # Obtener numero de semana y rango de fechas
            cursor.execute("""
                SELECT
                    semana,
                    MIN(fecha) as inicio_semana,
                    MAX(fecha) as fin_semana,
                    SUM(laboral) as dias_laborables
                FROM nuevo_carihuela_jorge_calendario_anual
                WHERE semana = (
                    SELECT semana
                    FROM nuevo_carihuela_jorge_calendario_anual
                    WHERE fecha = %s
                )
                AND YEAR(fecha) = YEAR(%s)
                GROUP BY semana
            """, (fecha, fecha))
            return cursor.fetchone()
    except Exception as e:
        print(f"Aviso: No se pudo obtener semana de calendario_anual: {e}")
        return None
    finally:
        conn.close()


def get_peticiones_abiertas():
    """Obtener peticiones de trabajador abiertas"""
    conn = get_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT
                    id,
                    perfil_codigo,
                    posicion,
                    solicitante_rol,
                    DATE_FORMAT(fecha_solicitud, '%d/%m/%Y') as fecha_solicitud,
                    COALESCE(publicado_en, '-') as publicado_en,
                    COALESCE(DATE_FORMAT(fecha_publicacion_desde, '%d/%m/%Y'), '-') as desde,
                    COALESCE(DATE_FORMAT(fecha_publicacion_hasta, '%d/%m/%Y'), '-') as hasta,
                    estado
                FROM peticiones_trabajador
                WHERE estado IN ('ABIERTA', 'EN_PROCESO')
                ORDER BY id ASC
            """)
            return cursor.fetchall()
    finally:
        conn.close()


def generar_reporte_pdf(fecha_reporte=None):
    """Generar el reporte PDF semanal"""

    if fecha_reporte is None:
        fecha_reporte = datetime.now()

    # Obtener semana desde la tabla calendario_anual (integracion con RRHH_Flujo_Trabajadores)
    semana_info = get_semana_actual(fecha_reporte.date() if hasattr(fecha_reporte, 'date') else fecha_reporte)

    if semana_info:
        numero_semana = semana_info['semana']
        inicio_semana = semana_info['inicio_semana']
        fin_semana = semana_info['fin_semana']
        dias_laborables = semana_info['dias_laborables']
    else:
        # Fallback: calcular localmente si no hay datos en BD
        numero_semana = fecha_reporte.isocalendar()[1]
        inicio_semana = fecha_reporte - timedelta(days=fecha_reporte.weekday())
        fin_semana = inicio_semana + timedelta(days=6)
        dias_laborables = None

    # Nombre del archivo
    nombre_archivo = f"reporte_semanal_{fecha_reporte.strftime('%Y%m%d')}.pdf"
    ruta_archivo = os.path.join(os.path.dirname(__file__), 'reportes', nombre_archivo)

    # Crear directorio si no existe
    os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)

    # Crear documento
    doc = SimpleDocTemplate(
        ruta_archivo,
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm
    )

    # Estilos
    styles = getSampleStyleSheet()

    titulo_style = ParagraphStyle(
        'Titulo',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=TA_CENTER,
        spaceAfter=20
    )

    subtitulo_style = ParagraphStyle(
        'Subtitulo',
        parent=styles['Heading2'],
        fontSize=12,
        alignment=TA_LEFT,
        spaceAfter=10,
        spaceBefore=15
    )

    fecha_style = ParagraphStyle(
        'Fecha',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        spaceAfter=20
    )

    # Contenido
    elementos = []

    # Titulo
    elementos.append(Paragraph("REPORTE SEMANAL RRHH", titulo_style))
    elementos.append(Paragraph("Pescados La Carihuela", fecha_style))

    # Formatear fechas (pueden ser date o datetime)
    if hasattr(inicio_semana, 'strftime'):
        inicio_str = inicio_semana.strftime('%d/%m/%Y')
        fin_str = fin_semana.strftime('%d/%m/%Y')
    else:
        inicio_str = inicio_semana
        fin_str = fin_semana

    # Mostrar semana con numero
    texto_semana = f"Semana {numero_semana} - del {inicio_str} al {fin_str}"
    if dias_laborables:
        texto_semana += f" ({int(dias_laborables)} dias laborables)"

    elementos.append(Paragraph(texto_semana, fecha_style))

    # Seccion 1: Necesidades de Personal
    elementos.append(Paragraph("1. NECESIDADES DE PERSONAL", subtitulo_style))

    peticiones = get_peticiones_abiertas()

    if peticiones:
        # Cabecera de la tabla
        datos_tabla = [
            ['ID', 'Perfil', 'Posicion', 'Solicitante', 'Fecha Sol.', 'Publicado', 'Desde', 'Hasta', 'Estado']
        ]

        # Datos
        for p in peticiones:
            datos_tabla.append([
                str(p['id']),
                p['perfil_codigo'],
                p['posicion'][:25] + '...' if len(p['posicion']) > 25 else p['posicion'],
                p['solicitante_rol'].replace('_', ' ').title(),
                p['fecha_solicitud'],
                p['publicado_en'],
                p['desde'],
                p['hasta'],
                p['estado']
            ])

        # Crear tabla
        tabla = Table(datos_tabla, colWidths=[0.8*cm, 2*cm, 3.5*cm, 2*cm, 2*cm, 1.8*cm, 2*cm, 2*cm, 1.8*cm])

        tabla.setStyle(TableStyle([
            # Cabecera
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1565C0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

            # Contenido
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),

            # Bordes
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),

            # Colores alternados
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),

            # Padding
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))

        elementos.append(tabla)
    else:
        elementos.append(Paragraph("No hay peticiones de personal abiertas.", styles['Normal']))

    # Espacio
    elementos.append(Spacer(1, 20))

    # Generar PDF
    doc.build(elementos)

    print(f"Reporte generado: {ruta_archivo}")
    return ruta_archivo


if __name__ == '__main__':
    # Generar reporte de la semana actual
    ruta = generar_reporte_pdf()
    print(f"Archivo: {ruta}")

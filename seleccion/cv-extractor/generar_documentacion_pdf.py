#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de documentacion PDF - Sistema de Seleccion
Pescados La Carihuela
"""

import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


def generar_documentacion_pdf():
    """Genera PDF con documentacion completa del sistema"""

    nombre_archivo = f"documentacion_sistema_{datetime.now().strftime('%Y%m%d')}.pdf"
    ruta_archivo = os.path.join(os.path.dirname(__file__), 'reportes', nombre_archivo)
    os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)

    doc = SimpleDocTemplate(
        ruta_archivo,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()

    # Estilos personalizados
    titulo_principal = ParagraphStyle(
        'TituloPrincipal',
        parent=styles['Heading1'],
        fontSize=20,
        alignment=TA_CENTER,
        spaceAfter=30,
        textColor=colors.HexColor('#1565C0')
    )

    titulo_seccion = ParagraphStyle(
        'TituloSeccion',
        parent=styles['Heading1'],
        fontSize=14,
        alignment=TA_LEFT,
        spaceBefore=20,
        spaceAfter=10,
        textColor=colors.HexColor('#1565C0')
    )

    subtitulo = ParagraphStyle(
        'Subtitulo',
        parent=styles['Heading2'],
        fontSize=11,
        alignment=TA_LEFT,
        spaceBefore=15,
        spaceAfter=8
    )

    normal = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=8
    )

    nota = ParagraphStyle(
        'Nota',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_CENTER,
        textColor=colors.grey
    )

    elementos = []

    # === PORTADA ===
    elementos.append(Spacer(1, 3*cm))
    elementos.append(Paragraph("SISTEMA DE SELECCION DE PERSONAL", titulo_principal))
    elementos.append(Paragraph("Pescados La Carihuela", ParagraphStyle('Empresa', parent=styles['Heading2'], fontSize=16, alignment=TA_CENTER)))
    elementos.append(Spacer(1, 2*cm))
    elementos.append(Paragraph("DOCUMENTACION DEL SISTEMA", ParagraphStyle('Doc', parent=styles['Heading2'], fontSize=14, alignment=TA_CENTER)))
    elementos.append(Spacer(1, 1*cm))
    elementos.append(Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", nota))
    elementos.append(Paragraph("Version: 1.0", nota))
    elementos.append(PageBreak())

    # === INDICE ===
    elementos.append(Paragraph("INDICE", titulo_seccion))
    indice = [
        "0. Peticion de Trabajador",
        "1. Perfiles Profesionales",
        "2. Ofertas de Empleo",
        "3. Reporte Semanal",
        "4. Integracion de Bases de Datos",
        "5. Estructura de Archivos"
    ]
    for i, item in enumerate(indice):
        elementos.append(Paragraph(f"{item}", normal))
    elementos.append(PageBreak())

    # === SECCION 0: PETICION DE TRABAJADOR ===
    elementos.append(Paragraph("0. PETICION DE TRABAJADOR", titulo_seccion))

    elementos.append(Paragraph("Descripcion", subtitulo))
    elementos.append(Paragraph(
        "El proceso de seleccion comienza cuando el Gerente o el Director de RRHH solicita un nuevo trabajador. "
        "Esta peticion se registra en el sistema y genera automaticamente una alerta.",
        normal
    ))

    elementos.append(Paragraph("Flujo del Proceso", subtitulo))
    elementos.append(Paragraph(
        "1. Gerente/Director RRHH crea peticion de trabajador<br/>"
        "2. Selecciona el PERFIL necesario<br/>"
        "3. Indica la posicion especifica<br/>"
        "4. La peticion queda en estado ABIERTA<br/>"
        "5. Se publica la oferta (manual en InfoJobs)<br/>"
        "6. Llegan candidatos al sistema",
        normal
    ))

    elementos.append(Paragraph("Datos de la Peticion", subtitulo))
    datos_peticion = [
        ['Campo', 'Descripcion', 'Obligatorio'],
        ['ID', 'Identificador unico', 'Auto'],
        ['Perfil', 'PESCADERIA, LOGISTICA, PRODUCCION, ADMINISTRATIVO, GESTION, BECARIO', 'SI'],
        ['Posicion', 'Nombre especifico del puesto', 'SI'],
        ['Solicitante', 'Gerente o Director RRHH', 'Auto'],
        ['Fecha Solicitud', 'Fecha de creacion', 'SI'],
        ['Publicado en', 'Donde se ha publicado', 'NO'],
        ['Desde/Hasta', 'Periodo de publicacion', 'NO'],
        ['Estado', 'ABIERTA, EN_PROCESO, CUBIERTA, CANCELADA', 'Auto']
    ]
    tabla = Table(datos_peticion, colWidths=[3*cm, 10*cm, 2.5*cm])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1565C0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elementos.append(tabla)

    elementos.append(Paragraph("Peticiones Actuales", subtitulo))
    peticiones_actuales = [
        ['ID', 'Perfil', 'Posicion', 'Fecha Sol.', 'Publicado', 'Desde', 'Hasta', 'Estado'],
        ['1', 'LOGISTICA', 'Operario/a Logistica', '15/01/2026', 'InfoJobs', '27/01/2026', '28/03/2026', 'ABIERTA'],
        ['2', 'PESCADERIA', 'Dependiente/a Pescaderia', '13/02/2026', 'InfoJobs', '13/02/2026', '14/04/2026', 'ABIERTA'],
        ['3', 'BECARIO', 'Becario Administracion', '01/02/2026', '-', '-', '-', 'ABIERTA']
    ]
    tabla2 = Table(peticiones_actuales, colWidths=[0.8*cm, 2.2*cm, 3.5*cm, 2*cm, 1.5*cm, 2*cm, 2*cm, 1.5*cm])
    tabla2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1565C0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elementos.append(tabla2)

    elementos.append(PageBreak())

    # === SECCION 1: PERFILES PROFESIONALES ===
    elementos.append(Paragraph("1. PERFILES PROFESIONALES", titulo_seccion))

    elementos.append(Paragraph(
        "Los perfiles profesionales definen las categorias de puestos disponibles en la empresa.",
        normal
    ))

    perfiles = [
        ['Codigo', 'Descripcion', 'Keywords'],
        ['PESCADERIA', 'Pescaderia, carniceria, comercio', 'pescad, carnicer, dependient, tienda'],
        ['LOGISTICA', 'Almacen, reparto, transporte', 'logistic, almacen, repartidor, mozo'],
        ['PRODUCCION', 'Fabrica, envasado, sushi', 'sushi, envase, produccion, operario'],
        ['ADMINISTRATIVO', 'Oficina, secretariado', 'secretari, administrativ, contab'],
        ['GESTION', 'Grados universitarios', 'grado ade, derecho, licenciado'],
        ['BECARIO', 'Practicas, formacion', 'becario, practicas, estudiante']
    ]
    tabla3 = Table(perfiles, colWidths=[3*cm, 5.5*cm, 7*cm])
    tabla3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1565C0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elementos.append(tabla3)

    elementos.append(PageBreak())

    # === SECCION 2: OFERTAS DE EMPLEO ===
    elementos.append(Paragraph("2. OFERTAS DE EMPLEO", titulo_seccion))

    elementos.append(Paragraph("Oferta LOGISTICA: Operario/a Logistica", subtitulo))
    elementos.append(Paragraph("<b>Titulo:</b> Operario/a Logistica de Almacen", normal))
    elementos.append(Paragraph(
        "<b>Descripcion:</b> Empresa del sector alimentario ubicada en la zona de Malaga busca incorporar "
        "un/a operario/a de logistica. La persona seleccionada sera responsable de: carga y descarga de "
        "mercancia, preparacion de pedidos, gestion de almacen con radiofrecuencia, control de stock.",
        normal
    ))
    elementos.append(Paragraph(
        "<b>Requisitos:</b> Carnet de conducir B. Carnet de carretillero (valorable). Experiencia en almacen. "
        "Disponibilidad horaria.",
        normal
    ))
    elementos.append(Paragraph(
        "<b>Condiciones:</b> Contrato temporal con posibilidad de indefinido. Jornada completa. "
        "Salario segun convenio.",
        normal
    ))

    elementos.append(Spacer(1, 0.5*cm))

    elementos.append(Paragraph("Oferta PESCADERIA: Dependiente/a Pescaderia", subtitulo))
    elementos.append(Paragraph("<b>Titulo:</b> Dependiente/a de Pescaderia", normal))
    elementos.append(Paragraph(
        "<b>Descripcion:</b> Empresa del sector alimentario busca dependiente/a para pescaderia. "
        "Funciones: atencion al cliente, corte y preparacion de pescado, mantenimiento del puesto, "
        "gestion de pedidos.",
        normal
    ))
    elementos.append(Paragraph(
        "<b>Requisitos:</b> Experiencia en pescaderia o carniceria. Atencion al publico. "
        "Disponibilidad para trabajar fines de semana.",
        normal
    ))
    elementos.append(Paragraph(
        "<b>Condiciones:</b> Contrato temporal. Jornada parcial o completa. Salario segun convenio.",
        normal
    ))

    elementos.append(PageBreak())

    # === SECCION 3: REPORTE SEMANAL ===
    elementos.append(Paragraph("3. REPORTE SEMANAL", titulo_seccion))

    elementos.append(Paragraph(
        "El sistema genera automaticamente un reporte PDF cada lunes a las 05:00 (hora de Espana). "
        "Este reporte se envia a las personas configuradas.",
        normal
    ))

    elementos.append(Paragraph("Contenido del Reporte", subtitulo))
    elementos.append(Paragraph(
        "<b>Seccion 1: Necesidades de Personal</b><br/>"
        "Muestra todas las peticiones de trabajador con estado ABIERTA o EN_PROCESO, incluyendo: "
        "ID, perfil, posicion, solicitante, fecha de solicitud, donde esta publicado, fechas de publicacion y estado.",
        normal
    ))

    elementos.append(Paragraph("Configuracion", subtitulo))
    elementos.append(Paragraph(
        "<b>Archivo:</b> reporte_semanal.py<br/>"
        "<b>Programacion:</b> Cron job - Lunes 05:00<br/>"
        "<b>Salida:</b> reportes/reporte_semanal_YYYYMMDD.pdf",
        normal
    ))

    elementos.append(PageBreak())

    # === SECCION 4: INTEGRACION DE BASES DE DATOS ===
    elementos.append(Paragraph("4. INTEGRACION DE BASES DE DATOS", titulo_seccion))

    elementos.append(Paragraph(
        "El sistema integra datos de tres proyectos que comparten la misma base de datos MySQL.",
        normal
    ))

    elementos.append(Paragraph("Proyectos Integrados", subtitulo))
    proyectos = [
        ['Proyecto', 'Descripcion', 'Tablas Principales'],
        ['cv-extractor', 'Extraccion y clasificacion de CVs', 'candidatos, perfiles, peticiones_trabajador'],
        ['RRHH_Flujo_Trabajadores', 'Gestion de trabajadores', 'contratos_usuario, calendario_anual'],
        ['proyecto-ia-multiagente', 'Sistema IA general', 'Varias tablas de IA']
    ]
    tabla4 = Table(proyectos, colWidths=[4*cm, 5*cm, 6.5*cm])
    tabla4.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1565C0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elementos.append(tabla4)

    elementos.append(Paragraph("Conexion Unificada", subtitulo))
    elementos.append(Paragraph(
        "<b>Base de Datos:</b> gestion.pescadoslacarihuela.es<br/>"
        "<b>Host:</b> 192.168.1.133<br/>"
        "<b>Puerto:</b> 3306<br/>"
        "<b>Usuario:</b> root",
        normal
    ))

    elementos.append(Paragraph("Tabla Compartida: calendario_anual", subtitulo))
    elementos.append(Paragraph(
        "La tabla nuevo_carihuela_jorge_calendario_anual contiene el calendario completo del ano con: "
        "numero de semana, dia de la semana, fecha, si es laboral o no, y festivos. "
        "Esta tabla se genera ejecutando el procedimiento generar_calendario_anual(AÑO).",
        normal
    ))

    elementos.append(PageBreak())

    # === SECCION 5: ESTRUCTURA DE ARCHIVOS ===
    elementos.append(Paragraph("5. ESTRUCTURA DE ARCHIVOS", titulo_seccion))

    estructura = [
        ['Archivo', 'Descripcion'],
        ['reporte_semanal.py', 'Generador de PDF semanal automatico'],
        ['setup_peticiones.py', 'Crear tablas de peticiones (ejecutar 1 vez)'],
        ['clasificador.py', 'Clasificador de candidatos por perfil'],
        ['db_loader.py', 'Cargador de datos a MySQL'],
        ['extract_cvs.py', 'Extractor de CVs desde PDF'],
        ['sql/schema_mysql.sql', 'Schema completo de base de datos'],
        ['sql/crear_peticiones.sql', 'SQL para crear tablas de peticiones'],
        ['reportes/', 'Directorio con PDFs generados'],
        ['docs/', 'Documentacion del sistema']
    ]
    tabla5 = Table(estructura, colWidths=[5*cm, 10.5*cm])
    tabla5.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1565C0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elementos.append(tabla5)

    # === PIE ===
    elementos.append(Spacer(1, 2*cm))
    elementos.append(Paragraph(
        f"Documento generado automaticamente el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}",
        nota
    ))

    # Generar PDF
    doc.build(elementos)
    print(f"Documentacion generada: {ruta_archivo}")
    return ruta_archivo


if __name__ == '__main__':
    ruta = generar_documentacion_pdf()
    print(f"Archivo: {ruta}")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Genera PDF con la tabla de Bajas de Larga Duración
"""

from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 14)
        self.cell(0, 10, 'BAJAS DE LARGA DURACION', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font('Helvetica', '', 10)
        self.cell(0, 6, f'Generado: {datetime.now().strftime("%d/%m/%Y %H:%M")}', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', align='C')

def generar_pdf():
    pdf = PDF(orientation='P', format='A4')
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Definición
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, '1. Definicion', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(60, 8, 'Tipo de Baja', border=1, fill=True)
    pdf.cell(80, 8, 'Condicion', border=1, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font('Helvetica', '', 10)
    pdf.cell(60, 7, 'Corta duracion', border=1)
    pdf.cell(80, 7, '< 30 dias naturales', border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_fill_color(255, 255, 200)
    pdf.cell(60, 7, 'Larga duracion', border=1, fill=True)
    pdf.cell(80, 7, '>= 30 dias naturales', border=1, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(3)
    pdf.set_font('Helvetica', 'I', 9)
    pdf.cell(0, 6, 'Nota: A partir del dia 30 de baja, se considera automaticamente como baja de larga duracion.', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(10)

    # Alerta automática
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, '2. Alerta Automatica (>=30 dias)', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    pdf.set_font('Helvetica', '', 9)
    pdf.cell(0, 6, 'Cuando un trabajador lleva 30 dias o mas de baja, el sistema genera una alerta automatica:', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    alerta_campos = [
        ('Condicion', 'Trabajador con >=30 dias de baja sin sustituto asignado'),
        ('Mensaje', '"El trabajador [Nombre] lleva 30 dias de baja y deberia tener un sustituto"'),
        ('Destinatario', 'Hermi (por correo electronico)'),
        ('Otros destinatarios', 'Pendiente de definir'),
        ('Frecuencia', 'Diaria hasta que se asigne sustituto'),
    ]

    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(45, 7, 'Campo', border=1, fill=True)
    pdf.cell(125, 7, 'Valor', border=1, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font('Helvetica', '', 9)
    for campo, valor in alerta_campos:
        pdf.cell(45, 6, campo, border=1)
        pdf.cell(125, 6, valor, border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(10)

    # Tabla de bajas actuales
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, '3. Bajas Larga Duracion Actuales (con sustituto)', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    # Cabecera tabla
    anchos = [15, 20, 55, 20, 55, 25]
    cabeceras = ['ID', 'Cod', 'Trabajador en Baja', 'Cod', 'Sustituto', 'Desde']

    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(50, 50, 100)
    pdf.set_text_color(255, 255, 255)
    for i, cab in enumerate(cabeceras):
        pdf.cell(anchos[i], 8, cab, border=1, fill=True, align='C')
    pdf.ln()

    # Datos actuales
    datos = [
        ('1', '097', 'Francisco Cabello', '216', 'Maria Leon', '19/09/2025'),
        ('3', '038', 'Soledad Leon', '259', 'Hugo Aguilar', '29/09/2025'),
        ('4', '005', 'Fernando Rafael Torralbo', '258', 'Angel Encinas', '13/11/2025'),
        ('2', '078', 'Monica Quesada', '255', 'Alejandro Leon', '02/01/2026'),
    ]

    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(0, 0, 0)
    for fila in datos:
        pdf.set_fill_color(245, 245, 245)
        for i, valor in enumerate(fila):
            pdf.cell(anchos[i], 7, valor, border=1, fill=True, align='C' if i in [0,1,3,5] else 'L')
        pdf.ln()

    pdf.ln(10)

    # Estructura de la tabla BD
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, '4. Estructura Tabla Base de Datos', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, 'Tabla: nuevo_carihuela_jorge_bajas_larga_duracion', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    campos = [
        ('id', 'INT', 'Identificador unico'),
        ('id_trabajador', 'INT', 'Codigo del trabajador en baja'),
        ('id_sustituto', 'INT', 'Codigo del sustituto asignado'),
        ('fecha_desde', 'DATE', 'Fecha inicio de la baja'),
        ('fecha_hasta', 'DATE NULL', 'Fecha fin (NULL si continua)'),
        ('motivo', 'VARCHAR', 'Motivo de la baja'),
        ('observaciones', 'TEXT', 'Observaciones adicionales'),
    ]

    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(40, 7, 'Campo', border=1, fill=True)
    pdf.cell(30, 7, 'Tipo', border=1, fill=True)
    pdf.cell(100, 7, 'Descripcion', border=1, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font('Helvetica', '', 9)
    for campo, tipo, desc in campos:
        pdf.cell(40, 6, campo, border=1)
        pdf.cell(30, 6, tipo, border=1)
        pdf.cell(100, 6, desc, border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(10)

    # Notas importantes
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, '5. Notas Importantes', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    pdf.set_font('Helvetica', '', 9)
    notas = [
        'Las bajas de larga duracion (>= 30 dias) requieren asignacion de sustituto.',
        'El trabajador en baja larga NO es elegible para el selector de vacaciones (Nivel 3).',
        'Al registrar una baja larga, se cancelan automaticamente las vacaciones planificadas.',
        'El sustituto debe tener un contrato de sustitucion vinculado al trabajador en baja.',
    ]

    for nota in notas:
        pdf.cell(5, 6, '-', border=0)
        pdf.multi_cell(0, 6, nota, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Guardar PDF
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f'reportes/bajas_larga_duracion_{timestamp}.pdf'
    pdf.output(output_path)
    print(f"PDF generado: {output_path}")
    return output_path

if __name__ == "__main__":
    generar_pdf()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Genera PDF con la tabla de Historial de Contratos
Incluye: Dur.Cto (Duracion Contrato) y Dur.Cond (Duracion Condicion)
"""

from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 14)
        self.cell(0, 10, 'HISTORIAL DE CONTRATOS - FORMATO VISUAL', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font('Helvetica', '', 10)
        self.cell(0, 6, f'Generado: {datetime.now().strftime("%d/%m/%Y %H:%M")}', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', align='C')

def generar_pdf():
    pdf = PDF(orientation='L', format='A4')  # Landscape para tabla ancha
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Estructura de columnas
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, '1. Estructura de Columnas', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    datos_columnas = [
        ('#', '#', 'Numero de linea secuencial', 'INT'),
        ('Contrato Desde', 'Cto Desde', 'Fecha inicio del contrato original', 'DATE'),
        ('Contrato Hasta', 'Cto Hasta', 'Fecha fin del contrato (- si indefinido)', 'DATE NULL'),
        ('Categoria', 'Cat', 'Categoria profesional (T0, T1, etc.)', 'VARCHAR'),
        ('Horas', 'Hrs', 'Horas semanales', 'INT'),
        ('Codigo', 'Cod', 'Codigo de contrato', 'VARCHAR'),
        ('Tipo', 'Tipo', 'Tipo: Temporal, Prorroga, Sustituc., Indefinido', 'VARCHAR'),
        ('Sustitucion', 'Sust', 'Nombre persona sustituida (- si no aplica)', 'VARCHAR'),
        ('Validez Desde', 'Val Desde', 'Fecha desde que aplica esta linea', 'DATE'),
        ('Validez Hasta', 'Val Hasta', 'Fecha hasta que aplica esta linea', 'DATE NULL'),
        ('Duracion Contrato', 'Dur.Cto', 'Duracion total del contrato actual', 'VARCHAR'),
        ('Duracion Condicion', 'Dur.Cond', 'Duracion de las condiciones actuales', 'VARCHAR'),
        ('Acciones', 'Acciones', 'Estado de firmas', 'VARCHAR'),
    ]

    # Cabecera tabla definicion
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(35, 7, 'Columna', border=1, fill=True)
    pdf.cell(20, 7, 'Abrev.', border=1, fill=True)
    pdf.cell(120, 7, 'Descripcion', border=1, fill=True)
    pdf.cell(25, 7, 'Tipo BD', border=1, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font('Helvetica', '', 8)
    for col, abrev, desc, tipo in datos_columnas:
        pdf.cell(35, 5, col, border=1)
        pdf.cell(20, 5, abrev, border=1)
        pdf.cell(120, 5, desc, border=1)
        pdf.cell(25, 5, tipo, border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(5)

    # Tipos de contrato
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 8, '1.1 Tipos de Contrato y Duracion', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)

    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(25, 6, 'Tipo', border=1, fill=True)
    pdf.cell(70, 6, 'Descripcion', border=1, fill=True)
    pdf.cell(55, 6, 'Dur.Cto', border=1, fill=True)
    pdf.cell(55, 6, 'Dur.Cond', border=1, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    datos_tipos = [
        ('Temporal', 'Contrato temporal inicial', 'Duracion inicial', 'Tiempo con cond. actuales'),
        ('Prorroga', 'Extension del contrato temporal', 'Suma acumulada', 'Tiempo con cond. actuales'),
        ('Sustituc.', 'Contrato por sustitucion', 'Tiempo desde inicio', 'Tiempo con cond. actuales'),
        ('Indefinido', 'Contrato indefinido', 'Tiempo desde inicio', 'Tiempo con cond. actuales'),
    ]

    pdf.set_font('Helvetica', '', 8)
    for tipo, desc, dur_cto, dur_cond in datos_tipos:
        pdf.cell(25, 5, tipo, border=1)
        pdf.cell(70, 5, desc, border=1)
        pdf.cell(55, 5, dur_cto, border=1)
        pdf.cell(55, 5, dur_cond, border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(8)

    # Tabla principal de historial
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, '2. Ejemplo Visual - Historial de Contratos', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    # Anchos de columna para la tabla principal (13 columnas)
    anchos = [8, 22, 22, 10, 10, 10, 22, 12, 22, 22, 18, 18, 22]
    cabeceras = ['#', 'Cto Desde', 'Cto Hasta', 'Cat', 'Hrs', 'Cod', 'Tipo', 'Sust', 'Val Desde', 'Val Hasta', 'Dur.Cto', 'Dur.Cond', 'Acciones']

    # Cabecera
    pdf.set_font('Helvetica', 'B', 7)
    pdf.set_fill_color(50, 50, 100)
    pdf.set_text_color(255, 255, 255)
    for i, cab in enumerate(cabeceras):
        pdf.cell(anchos[i], 8, cab, border=1, fill=True, align='C')
    pdf.ln()

    # Datos - Fecha actual ejemplo: 20/03/2027
    datos = [
        ('1', '01/12/2025', '28/02/2026', 'T0', '40', '100', 'Temporal', '-', '01/12/2025', '31/01/2026', '3m', '2m', 'H D T'),
        ('2', '01/12/2025', '28/02/2026', 'T1', '40', '100', 'Temporal', '-', '01/02/2026', '14/02/2026', '3m', '14d', 'H D T'),
        ('3', '01/12/2025', '28/02/2026', 'T1', '20', '100', 'Temporal', '-', '15/02/2026', '28/02/2026', '3m', '14d', 'H D T'),
        ('4', '01/12/2025', '31/05/2026', 'T1', '20', '100', 'Prorroga', '-', '01/03/2026', '30/04/2026', '6m', '2m 14d', 'H D T'),
        ('5', '01/12/2025', '31/05/2026', 'T1', '30', '100', 'Prorroga', '-', '01/05/2026', '31/05/2026', '6m', '1m', 'H D T'),
        ('6', '01/06/2026', '31/08/2026', 'T1', '30', '150', 'Sustituc.', 'A.Garcia', '01/06/2026', '31/08/2026', '3m', '3m', 'H D T'),
        ('7', '01/09/2026', '-', 'T1', '30', '200', 'Indefinido', '-', '01/09/2026', '19/02/2027', '5m 19d', '5m 19d', 'H D T'),
        ('8', '01/09/2026', '-', 'T3', '30', '200', 'Indefinido', '-', '20/02/2027', '-', '6m 19d', '1m', 'H D -'),
    ]

    pdf.set_font('Helvetica', '', 7)
    pdf.set_text_color(0, 0, 0)

    # Colores por tipo
    colores = {
        'Temporal': (220, 240, 220),    # Verde claro
        'Prorroga': (220, 230, 250),    # Azul claro
        'Sustituc.': (255, 240, 200),   # Amarillo claro
        'Indefinido': (240, 220, 240),  # Morado claro
    }

    for fila in datos:
        tipo = fila[6]
        color = colores.get(tipo, (255, 255, 255))
        pdf.set_fill_color(*color)
        for i, valor in enumerate(fila):
            pdf.cell(anchos[i], 7, valor, border=1, fill=True, align='C')
        pdf.ln()

    pdf.ln(8)

    # Explicacion del ejemplo
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, '3. Explicacion del Ejemplo', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    explicaciones = [
        ('1', 'Temporal', 'Contrato temporal inicial 3m, T0, 40h', '3m', '2m'),
        ('2', 'Temporal', 'Modificacion categoria T0->T1 (mismo cto)', '3m', '14d'),
        ('3', 'Temporal', 'Modificacion horas 40->20h (mismo cto)', '3m', '14d'),
        ('4', 'Prorroga', '+3m prorroga, mismas condiciones (T1, 20h)', '6m', '2m 14d'),
        ('5', 'Prorroga', 'Modificacion horas 20->30h (dentro prorroga)', '6m', '1m'),
        ('6', 'Sustituc.', 'Nuevo contrato sustitucion (reinicia Dur.Cto)', '3m', '3m'),
        ('7', 'Indefinido', 'Nuevo contrato indefinido (reinicia Dur.Cto)', '5m 19d', '5m 19d'),
        ('8', 'Indefinido', 'Modificacion categoria T1->T3 (pend. firma T)', '6m 19d', '1m'),
    ]

    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(10, 7, '#', border=1, fill=True, align='C')
    pdf.cell(25, 7, 'Tipo', border=1, fill=True)
    pdf.cell(120, 7, 'Descripcion', border=1, fill=True)
    pdf.cell(30, 7, 'Dur.Cto', border=1, fill=True)
    pdf.cell(35, 7, 'Dur.Cond', border=1, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font('Helvetica', '', 8)
    for num, tipo, desc, dur_cto, dur_cond in explicaciones:
        pdf.cell(10, 6, num, border=1, align='C')
        pdf.cell(25, 6, tipo, border=1)
        pdf.cell(120, 6, desc, border=1)
        pdf.cell(30, 6, dur_cto, border=1)
        pdf.cell(35, 6, dur_cond, border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(8)

    # Estados de acciones
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, '4. Estados de Acciones', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    estados = [
        ('H', 'Hermi ha subido el documento'),
        ('D', 'Director RRHH ha firmado'),
        ('T', 'Trabajador ha firmado'),
    ]

    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(20, 7, 'Icono', border=1, fill=True, align='C')
    pdf.cell(120, 7, 'Significado', border=1, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font('Helvetica', '', 9)
    for icono, sig in estados:
        pdf.cell(20, 6, icono, border=1, align='C')
        pdf.cell(120, 6, sig, border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(8)

    # Notas importantes
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, '5. Notas Importantes', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    pdf.set_font('Helvetica', '', 9)
    pdf.set_fill_color(255, 255, 220)
    notas = [
        'Dur.Cto: Se acumula en prorrogas (3m -> 6m -> 9m). Reinicia al cambiar modalidad (Temporal -> Sustituc. -> Indefinido)',
        'Dur.Cond: Se calcula segun el tiempo con las condiciones actuales (Cat, Hrs, Cod). Reinicia si cambian las condiciones.',
        'Prorrogas: Solo aplican a contratos Temporales. Cada prorroga genera una nueva linea.',
        'Sustitucion/Indefinido: No tienen prorrogas. La duracion se calcula desde el inicio del contrato.',
    ]

    for nota in notas:
        pdf.cell(5, 6, '-', border=0)
        pdf.multi_cell(0, 6, nota, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Guardar PDF
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f'reportes/historial_contratos_tabla_{timestamp}.pdf'
    pdf.output(output_path)
    print(f"PDF generado: {output_path}")
    return output_path

if __name__ == "__main__":
    generar_pdf()

#!/usr/bin/env python3
"""
Generador de Documentacion ModuloRRHH
Convierte archivos .md a HTML y PDF, organizados por carpeta.

Uso:
    python generar_documentacion.py

Requisitos:
    pip install markdown

Para PDF (opcional, uno de estos):
    - wkhtmltopdf instalado en el sistema + pip install pdfkit
    - pip install fpdf2 (genera PDF basico)
"""

import os
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

try:
    import markdown
except ImportError:
    print("Instalando markdown...")
    os.system("pip install markdown")
    import markdown

# Intentar importar generadores de PDF (opcionales)
PDF_ENGINE = None
WKHTMLTOPDF_PATH = None

# Rutas comunes de wkhtmltopdf en Windows
WKHTMLTOPDF_PATHS = [
    r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe",
    r"C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe",
    "wkhtmltopdf"  # Si esta en PATH
]

try:
    import pdfkit
    # Buscar wkhtmltopdf
    for path in WKHTMLTOPDF_PATHS:
        try:
            result = subprocess.run([path, '--version'],
                                  capture_output=True, timeout=5)
            if result.returncode == 0:
                WKHTMLTOPDF_PATH = path
                PDF_ENGINE = "pdfkit"
                break
        except:
            continue
except:
    pass

if PDF_ENGINE is None:
    try:
        from fpdf import FPDF
        PDF_ENGINE = "fpdf2"
    except ImportError:
        pass

if PDF_ENGINE is None:
    print("[AVISO] No se encontro generador de PDF.")
    print("        Para habilitar PDF, instale uno de estos:")
    print("        - wkhtmltopdf + pip install pdfkit")
    print("        - pip install fpdf2")
    print("")


# Configuracion
BASE_DIR = Path(__file__).parent.parent
DOCS_DIR = BASE_DIR / "docs"

# Mapeo de archivos fuente a carpetas destino
DOCUMENTOS = {
    "01_perfiles": {
        "fuente": BASE_DIR / "1_Perfiles" / "PERFILES.md",
        "nombre": "perfiles"
    },
    "02_seleccion": {
        "fuente": BASE_DIR / "2_Seleccion" / "SELECCION.md",
        "nombre": "seleccion"
    },
    "03_contratacion": {
        "fuente": BASE_DIR / "3_Contratacion" / "CONTRATACION.md",
        "nombre": "contratacion"
    },
    "04_trabajadores": {
        "fuente": BASE_DIR / "4_Trabajadores" / "TRABAJADORES.md",
        "nombre": "trabajadores"
    },
    "05_readme": {
        "fuente": BASE_DIR / "README.md",
        "nombre": "readme"
    }
}

# Estilos CSS para HTML y PDF
CSS_STYLES = """
@page {
    size: A4;
    margin: 2cm;
    @bottom-right {
        content: "Página " counter(page) " de " counter(pages);
        font-size: 9pt;
        color: #666;
    }
    @bottom-left {
        content: "ModuloRRHH - Pescados La Carihuela";
        font-size: 9pt;
        color: #666;
    }
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #333;
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
}

h1 {
    color: #1a5276;
    border-bottom: 3px solid #1a5276;
    padding-bottom: 10px;
    margin-top: 0;
}

h2 {
    color: #2874a6;
    border-bottom: 1px solid #aed6f1;
    padding-bottom: 5px;
    margin-top: 30px;
}

h3 {
    color: #3498db;
    margin-top: 25px;
}

h4 {
    color: #5dade2;
    margin-top: 20px;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 15px 0;
    font-size: 10pt;
}

th, td {
    border: 1px solid #bdc3c7;
    padding: 8px 12px;
    text-align: left;
}

th {
    background-color: #2874a6;
    color: white;
    font-weight: bold;
}

tr:nth-child(even) {
    background-color: #f8f9f9;
}

tr:hover {
    background-color: #ebf5fb;
}

code {
    background-color: #f4f6f7;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 10pt;
}

pre {
    background-color: #2c3e50;
    color: #ecf0f1;
    padding: 15px;
    border-radius: 5px;
    overflow-x: auto;
    font-size: 9pt;
    line-height: 1.4;
}

pre code {
    background-color: transparent;
    padding: 0;
    color: inherit;
}

blockquote {
    border-left: 4px solid #3498db;
    margin: 15px 0;
    padding: 10px 20px;
    background-color: #ebf5fb;
}

hr {
    border: none;
    border-top: 2px solid #eaecee;
    margin: 30px 0;
}

ul, ol {
    padding-left: 25px;
}

li {
    margin-bottom: 5px;
}

strong {
    color: #1a5276;
}

.header-info {
    background-color: #eaf2f8;
    padding: 15px;
    border-radius: 5px;
    margin-bottom: 20px;
    border-left: 4px solid #2874a6;
}

.fecha-generacion {
    text-align: right;
    color: #7f8c8d;
    font-size: 9pt;
    margin-top: 30px;
    padding-top: 10px;
    border-top: 1px solid #eee;
}
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo} - ModuloRRHH</title>
    <style>
{css}
    </style>
</head>
<body>
    <div class="header-info">
        <strong>ModuloRRHH</strong> - Pescados La Carihuela<br>
        <small>Documento: {titulo}</small>
    </div>

{contenido}

    <div class="fecha-generacion">
        Generado: {fecha}
    </div>
</body>
</html>
"""


def md_to_html(md_content: str) -> str:
    """Convierte Markdown a HTML."""
    extensions = ['tables', 'fenced_code', 'nl2br', 'sane_lists']
    html = markdown.markdown(md_content, extensions=extensions)
    return html


def generar_documento(carpeta: str, config: dict) -> dict:
    """Genera los 3 formatos para un documento."""
    resultados = {"md": False, "html": False, "pdf": False}

    fuente = config["fuente"]
    nombre = config["nombre"]
    destino = DOCS_DIR / carpeta

    # Crear carpeta si no existe
    destino.mkdir(parents=True, exist_ok=True)

    if not fuente.exists():
        print(f"  [X] Archivo fuente no encontrado: {fuente}")
        return resultados

    # Leer contenido MD
    with open(fuente, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Extraer titulo del primer H1
    titulo = nombre.upper()
    for line in md_content.split('\n'):
        if line.startswith('# '):
            titulo = line[2:].strip()
            break

    # 1. Copiar/Guardar MD
    md_path = destino / f"{nombre}.md"
    shutil.copy(fuente, md_path)
    resultados["md"] = True
    print(f"  [OK] {md_path.name}")

    # 2. Generar HTML
    html_content = md_to_html(md_content)
    html_full = HTML_TEMPLATE.format(
        titulo=titulo,
        css=CSS_STYLES,
        contenido=html_content,
        fecha=datetime.now().strftime("%d/%m/%Y %H:%M")
    )

    html_path = destino / f"{nombre}.html"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_full)
    resultados["html"] = True
    print(f"  [OK] {html_path.name}")

    # 3. Generar PDF
    pdf_path = destino / f"{nombre}.pdf"

    if PDF_ENGINE == "pdfkit":
        try:
            config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
            pdfkit.from_string(html_full, str(pdf_path), configuration=config, options={
                'encoding': 'UTF-8',
                'page-size': 'A4',
                'margin-top': '20mm',
                'margin-right': '20mm',
                'margin-bottom': '20mm',
                'margin-left': '20mm',
                'footer-center': 'Pagina [page] de [topage]',
                'footer-font-size': '8',
                'footer-line': '',
            })
            resultados["pdf"] = True
            print(f"  [OK] {pdf_path.name}")
        except Exception as e:
            print(f"  [X] Error generando PDF (pdfkit): {e}")

    elif PDF_ENGINE == "fpdf2":
        try:
            from fpdf import FPDF
            # Crear PDF basico desde el contenido MD
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", size=10)

            # Agregar titulo
            pdf.set_font("Helvetica", "B", 16)
            pdf.cell(0, 10, titulo, ln=True, align="C")
            pdf.ln(5)

            # Agregar contenido simplificado
            pdf.set_font("Helvetica", size=10)
            for line in md_content.split('\n'):
                # Limpiar markdown basico
                clean_line = line.replace('#', '').replace('*', '').replace('`', '')
                if clean_line.strip():
                    try:
                        pdf.multi_cell(0, 5, clean_line.encode('latin-1', 'replace').decode('latin-1'))
                    except:
                        pass

            pdf.output(str(pdf_path))
            resultados["pdf"] = True
            print(f"  [OK] {pdf_path.name} (basico)")
        except Exception as e:
            print(f"  [X] Error generando PDF (fpdf2): {e}")

    else:
        print(f"  [-] {pdf_path.name} (sin generador PDF)")

    return resultados


def main():
    """Funcion principal."""
    print("=" * 60)
    print("GENERADOR DE DOCUMENTACION - ModuloRRHH")
    print("=" * 60)
    print(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"Destino: {DOCS_DIR}")
    print("-" * 60)

    # Crear carpeta docs si no existe
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    total = {"md": 0, "html": 0, "pdf": 0}

    for carpeta, config in DOCUMENTOS.items():
        print(f"\n[{carpeta}] {config['nombre'].upper()}")
        resultados = generar_documento(carpeta, config)
        for fmt, ok in resultados.items():
            if ok:
                total[fmt] += 1

    print("\n" + "=" * 60)
    print("RESUMEN")
    print("-" * 60)
    print(f"  MD generados:   {total['md']}/{len(DOCUMENTOS)}")
    print(f"  HTML generados: {total['html']}/{len(DOCUMENTOS)}")
    print(f"  PDF generados:  {total['pdf']}/{len(DOCUMENTOS)}")
    print("=" * 60)

    # Mostrar estructura final
    print("\nESTRUCTURA GENERADA:")
    print("-" * 60)
    for carpeta in sorted(DOCS_DIR.iterdir()):
        if carpeta.is_dir():
            print(f"  {carpeta.name}/")
            for archivo in sorted(carpeta.iterdir()):
                print(f"    - {archivo.name}")

    print("\n[OK] Documentacion generada correctamente")


if __name__ == "__main__":
    main()

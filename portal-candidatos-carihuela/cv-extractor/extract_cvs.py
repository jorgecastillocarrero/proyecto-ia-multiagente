"""
Extractor de CVs desde PDF (formato InfoJobs)
Usa pdfplumber para extraer texto y Claude API para estructurar los datos.
"""

import json
import os
import re
from pathlib import Path

import pdfplumber
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

EXTRACTION_PROMPT = """Eres un extractor de datos de CVs. Analiza el siguiente texto extraído de un PDF que contiene múltiples CVs de InfoJobs concatenados.

IMPORTANTE:
- Los CVs están seguidos, sin separación clara entre páginas
- Cada CV nuevo empieza con: Nombre completo, puesto, ubicación, email, teléfono y "% ajuste"
- Extrae TODOS los CVs que encuentres
- Si un campo no existe, usa null
- Las fechas deben estar en formato "YYYY-MM" o "YYYY-MM-DD" cuando sea posible
- Si dice "actualmente", usa null en fecha_fin

Devuelve un JSON con esta estructura exacta (array de CVs):

[
  {{
    "datos_personales": {{
      "nombre": "string",
      "puesto_actual": "string",
      "codigo_postal": "string",
      "ciudad": "string",
      "provincia": "string",
      "email": "string",
      "telefono": "string",
      "telefono_secundario": "string o null",
      "porcentaje_ajuste": "number o null"
    }},
    "datos_candidato": {{
      "permiso_trabajo": "string o null",
      "carnet_conducir": "string o null",
      "es_autonomo": "boolean",
      "vehiculo_propio": "boolean"
    }},
    "experiencias": [
      {{
        "puesto": "string",
        "empresa": "string",
        "fecha_inicio": "YYYY-MM o null",
        "fecha_fin": "YYYY-MM o null (null si es actual)",
        "duracion_meses": "number o null",
        "tipo_contrato": "string (Empleado/a, Becario/a, Autónomo, etc.)",
        "salario_bruto_mes_min": "number o null",
        "salario_bruto_mes_max": "number o null",
        "descripcion": "string o null",
        "skills": ["array de strings"]
      }}
    ],
    "formaciones": [
      {{
        "tipo": "reglada | no_reglada | certificacion",
        "nivel": "string (ESO, Bachillerato, Grado Medio, Grado Superior, Universidad, Curso, etc.)",
        "titulo": "string",
        "centro": "string o null",
        "fecha_inicio": "YYYY-MM o null",
        "fecha_fin": "YYYY-MM o null"
      }}
    ],
    "idiomas": [
      {{
        "idioma": "string",
        "nivel": "string (Nativo, Avanzado, Intermedio, Básico)"
      }}
    ],
    "conocimientos": ["array de strings con todas las skills/conocimientos listados"]
  }}
]

TEXTO DEL PDF:
---
{pdf_text}
---

Responde SOLO con el JSON válido, sin explicaciones ni markdown."""


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extrae todo el texto de un PDF usando pdfplumber."""
    text_parts = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)

    return "\n\n--- PÁGINA ---\n\n".join(text_parts)


def parse_date_to_iso(date_str: str) -> str | None:
    """Convierte fechas en español a formato ISO (YYYY-MM)."""
    if not date_str or date_str.lower() == "actualmente":
        return None

    meses = {
        "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
        "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
        "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
    }

    # Patrón: "mes de año" o "Mes de año"
    pattern = r"(\w+)\s+de\s+(\d{4})"
    match = re.search(pattern, date_str.lower())

    if match:
        mes_nombre = match.group(1)
        año = match.group(2)
        mes_num = meses.get(mes_nombre)
        if mes_num:
            return f"{año}-{mes_num}"

    return date_str


def extract_cvs_with_claude(pdf_text: str) -> list[dict]:
    """Usa Claude API para extraer y estructurar los CVs."""

    prompt = EXTRACTION_PROMPT.format(pdf_text=pdf_text)

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response_text = message.content[0].text

    # Limpiar posibles marcadores de código
    response_text = response_text.strip()
    if response_text.startswith("```json"):
        response_text = response_text[7:]
    if response_text.startswith("```"):
        response_text = response_text[3:]
    if response_text.endswith("```"):
        response_text = response_text[:-3]

    return json.loads(response_text.strip())


def extract_cvs_from_pdf(pdf_path: str) -> list[dict]:
    """Función principal: extrae CVs de un PDF y devuelve lista de diccionarios."""

    print(f"Extrayendo texto de: {pdf_path}")
    pdf_text = extract_text_from_pdf(pdf_path)
    print(f"Texto extraído: {len(pdf_text)} caracteres")

    print("Enviando a Claude API para estructurar...")
    cvs = extract_cvs_with_claude(pdf_text)
    print(f"CVs extraídos: {len(cvs)}")

    return cvs


def main():
    """Ejemplo de uso."""
    import sys

    if len(sys.argv) < 2:
        print("Uso: python extract_cvs.py <ruta_pdf>")
        print("Ejemplo: python extract_cvs.py ./cvs.pdf")
        sys.exit(1)

    pdf_path = sys.argv[1]

    if not Path(pdf_path).exists():
        print(f"Error: No se encuentra el archivo {pdf_path}")
        sys.exit(1)

    cvs = extract_cvs_from_pdf(pdf_path)

    # Guardar resultado en JSON
    output_path = Path(pdf_path).stem + "_extracted.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cvs, f, ensure_ascii=False, indent=2)

    print(f"\nResultado guardado en: {output_path}")

    # Mostrar resumen
    print("\n" + "="*50)
    print("RESUMEN DE CVs EXTRAÍDOS")
    print("="*50)

    for i, cv in enumerate(cvs, 1):
        datos = cv.get("datos_personales", {})
        exp_count = len(cv.get("experiencias", []))
        form_count = len(cv.get("formaciones", []))

        print(f"\n{i}. {datos.get('nombre', 'Sin nombre')}")
        print(f"   Email: {datos.get('email', 'N/A')}")
        print(f"   Teléfono: {datos.get('telefono', 'N/A')}")
        print(f"   Experiencias: {exp_count} | Formaciones: {form_count}")


if __name__ == "__main__":
    main()

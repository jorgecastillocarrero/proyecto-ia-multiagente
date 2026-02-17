"""
Extractor de CVs desde PDF (formato InfoJobs) - Versión para lotes grandes
Procesa PDFs grandes dividiendo en partes.
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

EXTRACTION_PROMPT = """Eres un extractor de datos de CVs. Analiza el siguiente texto extraído de un PDF que contiene CVs de InfoJobs.

IMPORTANTE:
- Los CVs están seguidos, sin separación clara entre páginas
- Cada CV nuevo empieza con: Nombre completo, puesto, ubicación, email, teléfono y "% ajuste"
- Extrae TODOS los CVs que encuentres en este fragmento
- Si un campo no existe, usa null
- Las fechas deben estar en formato "YYYY-MM"
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
      "telefono": "string"
    }},
    "datos_candidato": {{
      "carnet_conducir": "string o null",
      "vehiculo_propio": "boolean"
    }},
    "experiencias": [
      {{
        "puesto": "string",
        "empresa": "string",
        "fecha_inicio": "YYYY-MM o null",
        "fecha_fin": "YYYY-MM o null",
        "duracion_meses": "number o null",
        "tipo_contrato": "string",
        "descripcion": "string o null"
      }}
    ],
    "formaciones": [
      {{
        "tipo": "reglada | certificacion",
        "nivel": "string",
        "titulo": "string",
        "centro": "string o null",
        "fecha_inicio": "YYYY-MM o null",
        "fecha_fin": "YYYY-MM o null"
      }}
    ],
    "idiomas": [
      {{
        "idioma": "string",
        "nivel": "string"
      }}
    ]
  }}
]

TEXTO DEL PDF:
---
{pdf_text}
---

Responde SOLO con el JSON válido, sin explicaciones ni markdown."""


def extract_text_from_pdf(pdf_path: str) -> list[str]:
    """Extrae texto de un PDF, retornando lista de páginas."""
    pages_text = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages_text.append(text)

    return pages_text


def split_into_chunks(pages: list[str], pages_per_chunk: int = 15) -> list[str]:
    """Divide las páginas en chunks procesables."""
    chunks = []
    for i in range(0, len(pages), pages_per_chunk):
        chunk_pages = pages[i:i + pages_per_chunk]
        chunk_text = "\n\n--- PÁGINA ---\n\n".join(chunk_pages)
        chunks.append(chunk_text)
    return chunks


def extract_cvs_with_claude(pdf_text: str) -> list[dict]:
    """Usa Claude API para extraer y estructurar los CVs."""

    prompt = EXTRACTION_PROMPT.format(pdf_text=pdf_text)

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=16000,
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

    try:
        return json.loads(response_text.strip())
    except json.JSONDecodeError as e:
        print(f"  Error parseando JSON: {e}")
        # Intentar arreglar JSON truncado
        response_text = response_text.strip()
        if not response_text.endswith("]"):
            # Buscar el último CV completo
            last_complete = response_text.rfind("},")
            if last_complete > 0:
                response_text = response_text[:last_complete + 1] + "]"
                try:
                    return json.loads(response_text)
                except:
                    pass
        return []


def extract_cvs_from_pdf(pdf_path: str) -> list[dict]:
    """Función principal: extrae CVs de un PDF grande en lotes."""

    print(f"Extrayendo texto de: {pdf_path}")
    pages = extract_text_from_pdf(pdf_path)
    print(f"Total páginas: {len(pages)}")

    # Dividir en chunks de 15 páginas
    chunks = split_into_chunks(pages, pages_per_chunk=15)
    print(f"Procesando en {len(chunks)} lotes...")

    all_cvs = []
    seen_emails = set()

    for i, chunk in enumerate(chunks, 1):
        print(f"\n  Lote {i}/{len(chunks)} ({len(chunk)} chars)...")
        try:
            cvs = extract_cvs_with_claude(chunk)
            # Filtrar duplicados por email
            for cv in cvs:
                email = cv.get("datos_personales", {}).get("email")
                if email and email not in seen_emails:
                    seen_emails.add(email)
                    all_cvs.append(cv)
                    print(f"    + {cv.get('datos_personales', {}).get('nombre', 'Sin nombre')}")
                elif not email:
                    all_cvs.append(cv)
                    print(f"    + {cv.get('datos_personales', {}).get('nombre', 'Sin nombre')} (sin email)")
        except Exception as e:
            print(f"    Error en lote {i}: {e}")

    print(f"\nTotal CVs extraídos: {len(all_cvs)}")
    return all_cvs


def main():
    """Ejemplo de uso."""
    import sys

    if len(sys.argv) < 2:
        print("Uso: python extract_cvs_batch.py <ruta_pdf>")
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


if __name__ == "__main__":
    main()

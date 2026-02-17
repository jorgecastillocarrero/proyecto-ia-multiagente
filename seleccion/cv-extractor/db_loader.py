"""
Cargador de CVs extraídos a PostgreSQL.
Lee archivos JSON generados por extract_cvs.py e inserta los datos en la BD.
"""

import json
import os
import re
from datetime import date
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Configuración de la base de datos
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "cvs_db"),
    "user": os.getenv("DB_USER", "cvs_user"),
    "password": os.getenv("DB_PASSWORD", "cvs_password_2024"),
}


def get_connection():
    """Crea una conexión a PostgreSQL."""
    return psycopg2.connect(**DB_CONFIG)


def parse_date(date_str: str | None) -> date | None:
    """Convierte string de fecha YYYY-MM a objeto date."""
    if not date_str:
        return None

    match = re.match(r"(\d{4})-(\d{2})", date_str)
    if match:
        year = int(match.group(1))
        month = int(match.group(2))
        return date(year, month, 1)

    return None


def insert_candidato(cur, cv_data: dict, archivo_origen: str = None) -> int:
    """Inserta un candidato y retorna su ID."""
    datos = cv_data.get("datos_personales", {})
    datos_cand = cv_data.get("datos_candidato", {})

    # Determinar carnets
    carnet = datos_cand.get("carnet_conducir", "")
    carnet_b = "B" in str(carnet).upper() if carnet else False
    carnet_c = "C" in str(carnet).upper() if carnet else False
    vehiculo = datos_cand.get("vehiculo_propio", False)

    cur.execute("""
        INSERT INTO candidatos (
            nombre, puesto_actual, codigo_postal, ciudad, provincia,
            email, telefono, vehiculo_propio, carnet_b, carnet_c, cap,
            carnet_carretillero, archivo_origen
        ) VALUES (
            %(nombre)s, %(puesto_actual)s, %(codigo_postal)s, %(ciudad)s, %(provincia)s,
            %(email)s, %(telefono)s, %(vehiculo_propio)s, %(carnet_b)s, %(carnet_c)s, FALSE,
            FALSE, %(archivo_origen)s
        )
        ON CONFLICT (email) DO UPDATE SET
            nombre = EXCLUDED.nombre,
            puesto_actual = EXCLUDED.puesto_actual,
            telefono = EXCLUDED.telefono,
            fecha_importacion = CURRENT_TIMESTAMP
        RETURNING id
    """, {
        "nombre": datos.get("nombre"),
        "puesto_actual": datos.get("puesto_actual"),
        "codigo_postal": datos.get("codigo_postal"),
        "ciudad": datos.get("ciudad"),
        "provincia": datos.get("provincia"),
        "email": datos.get("email"),
        "telefono": datos.get("telefono"),
        "vehiculo_propio": vehiculo,
        "carnet_b": carnet_b,
        "carnet_c": carnet_c,
        "archivo_origen": archivo_origen,
    })

    return cur.fetchone()[0]


def insert_experiencias(cur, candidato_id: int, experiencias: list):
    """Inserta las experiencias laborales de un candidato."""
    if not experiencias:
        return

    cur.execute("DELETE FROM experiencias WHERE candidato_id = %s", (candidato_id,))

    for exp in experiencias:
        duracion = exp.get("duracion_meses")
        duracion_anos = round(duracion / 12.0, 2) if duracion else None

        cur.execute("""
            INSERT INTO experiencias (
                candidato_id, puesto, empresa, fecha_inicio, fecha_fin,
                duracion_anos, tipo_contrato, descripcion
            ) VALUES (
                %(candidato_id)s, %(puesto)s, %(empresa)s, %(fecha_inicio)s, %(fecha_fin)s,
                %(duracion_anos)s, %(tipo_contrato)s, %(descripcion)s
            )
        """, {
            "candidato_id": candidato_id,
            "puesto": exp.get("puesto"),
            "empresa": exp.get("empresa"),
            "fecha_inicio": parse_date(exp.get("fecha_inicio")),
            "fecha_fin": parse_date(exp.get("fecha_fin")),
            "duracion_anos": duracion_anos,
            "tipo_contrato": exp.get("tipo_contrato"),
            "descripcion": exp.get("descripcion"),
        })






def update_total_experiencia(cur, candidato_id: int):
    """Actualiza el total de años de experiencia del candidato."""
    cur.execute("""
        UPDATE candidatos SET total_anos_experiencia = (
            SELECT ROUND(COALESCE(SUM(duracion_anos), 0), 2)
            FROM experiencias WHERE candidato_id = %s
        ) WHERE id = %s
    """, (candidato_id, candidato_id))


def load_cv_to_db(cv_data: dict, archivo_origen: str = None) -> int:
    """Carga un CV completo a la base de datos. Retorna el ID del candidato."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            candidato_id = insert_candidato(cur, cv_data, archivo_origen)
            insert_experiencias(cur, candidato_id, cv_data.get("experiencias", []))
            update_total_experiencia(cur, candidato_id)

            conn.commit()
            return candidato_id

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def generate_placeholder_email(nombre: str) -> str:
    """Genera un email placeholder único para candidatos sin email."""
    import hashlib
    import time
    # Crear hash único basado en nombre y timestamp
    unique_str = f"{nombre}_{time.time()}"
    hash_suffix = hashlib.md5(unique_str.encode()).hexdigest()[:8]
    return f"sin_email_{hash_suffix}@sin.email"


def load_json_file(json_path: str) -> list[int]:
    """Carga un archivo JSON con CVs a la base de datos. Retorna lista de IDs."""
    with open(json_path, "r", encoding="utf-8") as f:
        cvs = json.load(f)

    archivo_origen = Path(json_path).name
    ids = []

    for cv in cvs:
        nombre = cv.get("datos_personales", {}).get("nombre", "Desconocido")
        email = cv.get("datos_personales", {}).get("email")

        # Si no tiene email, generar uno placeholder
        if not email:
            email = generate_placeholder_email(nombre)
            cv["datos_personales"]["email"] = email
            print(f"  [SIN EMAIL] {nombre} -> asignado: {email}")

        try:
            candidato_id = load_cv_to_db(cv, archivo_origen)
            ids.append(candidato_id)
            print(f"  [OK] {nombre} -> ID: {candidato_id}")
        except Exception as e:
            print(f"  [ERROR] {nombre}: {e}")

    return ids


def main():
    """CLI para cargar CVs."""
    import sys

    if len(sys.argv) < 2:
        print("Uso:")
        print("  python db_loader.py load <archivo.json>     # Cargar CVs")
        print("  python db_loader.py load-all                # Cargar todos los JSON")
        sys.exit(1)

    command = sys.argv[1]

    if command == "load":
        if len(sys.argv) < 3:
            print("Error: Especifica el archivo JSON a cargar")
            sys.exit(1)

        json_path = sys.argv[2]
        if not Path(json_path).exists():
            print(f"Error: No se encuentra {json_path}")
            sys.exit(1)

        print(f"Cargando CVs desde: {json_path}")
        ids = load_json_file(json_path)
        print(f"\nTotal cargados: {len(ids)} candidatos")

    elif command == "load-all":
        json_files = list(Path(".").glob("*_extracted.json"))
        if not json_files:
            print("No se encontraron archivos *_extracted.json")
            sys.exit(1)

        total = 0
        for json_file in json_files:
            print(f"\nCargando: {json_file}")
            ids = load_json_file(str(json_file))
            total += len(ids)

        print(f"\n{'='*50}")
        print(f"Total cargados: {total} candidatos de {len(json_files)} archivos")

    else:
        print(f"Comando desconocido: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()

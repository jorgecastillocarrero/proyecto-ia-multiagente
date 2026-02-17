"""
Cargador de CVs extraídos a MySQL.
Lee archivos JSON generados por extract_cvs.py e inserta los datos en la BD.
"""

import json
import os
import re
from datetime import date
from pathlib import Path

import pymysql
from dotenv import load_dotenv

load_dotenv()

# Configuración de la base de datos MySQL
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "192.168.1.133"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "database": os.getenv("DB_NAME", "gestion.pescadoslacarihuela.es"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "charset": "utf8mb4",
}


def get_connection():
    """Crea una conexión a MySQL."""
    return pymysql.connect(**DB_CONFIG)


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
    carnet_b = 1 if "B" in str(carnet).upper() else 0
    carnet_c = 1 if "C" in str(carnet).upper() else 0
    vehiculo = 1 if datos_cand.get("vehiculo_propio", False) else 0

    # Separar nombre y apellidos
    nombre_completo = datos.get("nombre", "")
    partes = nombre_completo.split() if nombre_completo else []
    nombre = partes[0] if len(partes) > 0 else ""
    apellido1 = partes[1] if len(partes) > 1 else ""
    apellido2 = " ".join(partes[2:]) if len(partes) > 2 else ""

    # Verificar si existe por email
    email = datos.get("email", "")
    cur.execute("SELECT id FROM candidatos WHERE email = %s", (email,))
    existing = cur.fetchone()

    if existing:
        candidato_id = existing[0]
        cur.execute("""
            UPDATE candidatos SET
                nombre = %s,
                apellido1 = %s,
                apellido2 = %s,
                telefono = %s,
                residencia = %s,
                carnet_b = %s,
                carnet_c = %s,
                vehiculo_propio = %s,
                updated_at = NOW()
            WHERE id = %s
        """, (
            nombre,
            apellido1,
            apellido2,
            datos.get("telefono"),
            datos.get("ciudad"),
            carnet_b,
            carnet_c,
            vehiculo,
            candidato_id
        ))
    else:
        cur.execute("""
            INSERT INTO candidatos (
                nombre, apellido1, apellido2, telefono, email,
                residencia, carnet_b, carnet_c, vehiculo_propio,
                dni, categoria_id, estado_global, created_at
            ) VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, NOW()
            )
        """, (
            nombre,
            apellido1,
            apellido2,
            datos.get("telefono"),
            email,
            datos.get("ciudad"),
            carnet_b,
            carnet_c,
            vehiculo,
            "",  # dni vacío por ahora
            1,   # categoria_id default
            "NUEVO"
        ))
        candidato_id = cur.lastrowid

    return candidato_id


def insert_experiencias(cur, candidato_id: int, experiencias: list):
    """Inserta las experiencias laborales de un candidato."""
    if not experiencias:
        return

    # Verificar si existe la tabla experiencias_candidatos
    cur.execute("""
        SELECT COUNT(*) FROM information_schema.tables
        WHERE table_schema = DATABASE() AND table_name = 'experiencias_candidatos'
    """)
    if cur.fetchone()[0] == 0:
        # Crear tabla si no existe
        cur.execute("""
            CREATE TABLE experiencias_candidatos (
                id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                candidato_id BIGINT UNSIGNED NOT NULL,
                puesto VARCHAR(200),
                empresa VARCHAR(200),
                fecha_inicio DATE,
                fecha_fin DATE,
                duracion_anos DECIMAL(4,2),
                tipo_contrato VARCHAR(100),
                descripcion TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_candidato (candidato_id),
                FOREIGN KEY (candidato_id) REFERENCES candidatos(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

    # Eliminar experiencias anteriores
    cur.execute("DELETE FROM experiencias_candidatos WHERE candidato_id = %s", (candidato_id,))

    for exp in experiencias:
        duracion = exp.get("duracion_meses")
        duracion_anos = round(duracion / 12.0, 2) if duracion else None

        cur.execute("""
            INSERT INTO experiencias_candidatos (
                candidato_id, puesto, empresa, fecha_inicio, fecha_fin,
                duracion_anos, tipo_contrato, descripcion
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s
            )
        """, (
            candidato_id,
            exp.get("puesto"),
            exp.get("empresa"),
            parse_date(exp.get("fecha_inicio")),
            parse_date(exp.get("fecha_fin")),
            duracion_anos,
            exp.get("tipo_contrato"),
            exp.get("descripcion"),
        ))


def insert_conocimientos(cur, candidato_id: int, conocimientos: list):
    """Inserta los conocimientos de un candidato."""
    if not conocimientos:
        return

    # Verificar si existe la tabla
    cur.execute("""
        SELECT COUNT(*) FROM information_schema.tables
        WHERE table_schema = DATABASE() AND table_name = 'conocimientos_candidato'
    """)
    if cur.fetchone()[0] == 0:
        cur.execute("""
            CREATE TABLE conocimientos_candidato (
                id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                candidato_id BIGINT UNSIGNED NOT NULL,
                conocimiento VARCHAR(200),
                INDEX idx_candidato (candidato_id),
                FOREIGN KEY (candidato_id) REFERENCES candidatos(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

    # Eliminar conocimientos anteriores
    cur.execute("DELETE FROM conocimientos_candidato WHERE candidato_id = %s", (candidato_id,))

    for conocimiento in conocimientos:
        if conocimiento:
            cur.execute("""
                INSERT INTO conocimientos_candidato (candidato_id, conocimiento)
                VALUES (%s, %s)
            """, (candidato_id, conocimiento[:200]))


def load_cv_to_db(cv_data: dict, archivo_origen: str = None) -> int:
    """Carga un CV completo a la base de datos. Retorna el ID del candidato."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            candidato_id = insert_candidato(cur, cv_data, archivo_origen)
            insert_experiencias(cur, candidato_id, cv_data.get("experiencias", []))
            insert_conocimientos(cur, candidato_id, cv_data.get("conocimientos", []))

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


def test_connection():
    """Prueba la conexión a MySQL."""
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT VERSION()")
            version = cur.fetchone()[0]
            print(f"Conectado a MySQL: {version}")

            cur.execute("SELECT COUNT(*) FROM candidatos")
            count = cur.fetchone()[0]
            print(f"Candidatos en BD: {count}")
        conn.close()
        return True
    except Exception as e:
        print(f"Error de conexión: {e}")
        return False


def main():
    """CLI para cargar CVs."""
    import sys

    if len(sys.argv) < 2:
        print("Uso:")
        print("  python db_loader.py test                    # Probar conexión")
        print("  python db_loader.py load <archivo.json>     # Cargar CVs")
        print("  python db_loader.py load-all                # Cargar todos los JSON")
        sys.exit(1)

    command = sys.argv[1]

    if command == "test":
        test_connection()

    elif command == "load":
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

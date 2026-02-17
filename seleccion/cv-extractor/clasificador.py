"""
Clasificador de Candidatos por Perfil
Pescados La Carihuela - Sistema de Selección RRHH
"""

import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

# Configuración BD
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "192.168.1.133"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "database": os.getenv("DB_NAME", "gestion.pescadoslacarihuela.es"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "charset": "utf8mb4",
}

# Definición de perfiles y palabras clave
PERFILES = {
    "PESCADERIA": {
        "keywords": [
            "pescad", "carnicer", "charcuter", "corte", "filete",
            "marisco", "mostrador", "fresco", "despiece",
            "dependient", "tienda", "comercio"
        ],
        "requiere_carnet_c": False,
        "descripcion": "Pescadería, carnicería, comercio de frescos"
    },
    "LOGISTICA": {
        "keywords": [
            "logistic", "almacen", "almacén", "reparto", "repartidor",
            "transporte", "carretiller", "mozo", "carga", "descarga",
            "picking", "preparador pedido", "conductor", "camion", "camión",
            "furgoneta", "distribucion", "distribución"
        ],
        "requiere_carnet_c": True,  # Prioriza si tiene carnet C
        "descripcion": "Logística, almacén, reparto, transporte"
    },
    "PRODUCCION": {
        "keywords": [
            "sushi", "envase", "envasado", "produccion", "producción",
            "fabrica", "fábrica", "operario", "linea", "línea",
            "manipulador", "elaboracion", "elaboración"
        ],
        "requiere_carnet_c": False,
        "descripcion": "Producción, sushi, sala de envase"
    },
    "ADMINISTRATIVO": {
        "keywords": [
            "secretari", "administrativ", "contab", "factur",
            "oficina", "recepcion", "recepción", "auxiliar admin"
        ],
        "requiere_carnet_c": False,
        "descripcion": "Administrativo, secretariado, FP administración"
    },
    "GESTION": {
        "keywords": [
            "grado ade", "grado derecho", "licenciado", "graduado",
            "master", "mba", "universidad"
        ],
        "requiere_carnet_c": False,
        "descripcion": "Gestión, grados universitarios (ADE, Derecho, etc.)"
    }
}


def get_connection():
    """Crea conexión a MySQL."""
    return pymysql.connect(**DB_CONFIG)


def clasificar_candidato(puesto: str, carnet_c: bool = False, cap: bool = False) -> str:
    """
    Clasifica un candidato en un perfil según su puesto y requisitos.

    Args:
        puesto: Puesto actual o deseado del candidato
        carnet_c: True si tiene carnet C
        cap: True si tiene CAP

    Returns:
        Nombre del perfil o 'SIN_CLASIFICAR'
    """
    puesto_lower = (puesto or "").lower()

    # Si tiene carnet C o CAP, priorizar LOGISTICA
    if carnet_c or cap:
        return "LOGISTICA"

    # Buscar por palabras clave en orden de prioridad
    for perfil, config in PERFILES.items():
        for keyword in config["keywords"]:
            if keyword in puesto_lower:
                return perfil

    return "SIN_CLASIFICAR"


def crear_tabla_perfiles():
    """Crea la tabla de perfiles si no existe."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS perfiles (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    codigo VARCHAR(50) UNIQUE NOT NULL,
                    nombre VARCHAR(100) NOT NULL,
                    descripcion TEXT,
                    keywords TEXT,
                    activo TINYINT(1) DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)

            # Insertar perfiles predefinidos
            for codigo, config in PERFILES.items():
                cur.execute("""
                    INSERT INTO perfiles (codigo, nombre, descripcion, keywords)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        descripcion = VALUES(descripcion),
                        keywords = VALUES(keywords)
                """, (
                    codigo,
                    codigo.replace("_", " ").title(),
                    config["descripcion"],
                    ",".join(config["keywords"])
                ))

            conn.commit()
            print("Tabla 'perfiles' creada/actualizada")

    finally:
        conn.close()


def agregar_columna_perfil():
    """Agrega columna perfil_id a candidatos si no existe."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Verificar si existe la columna
            cur.execute("""
                SELECT COUNT(*) FROM information_schema.columns
                WHERE table_schema = DATABASE()
                AND table_name = 'candidatos'
                AND column_name = 'perfil_id'
            """)

            if cur.fetchone()[0] == 0:
                cur.execute("""
                    ALTER TABLE candidatos
                    ADD COLUMN perfil_id INT,
                    ADD COLUMN perfil_codigo VARCHAR(50),
                    ADD INDEX idx_perfil (perfil_id)
                """)
                conn.commit()
                print("Columnas perfil_id y perfil_codigo añadidas")
            else:
                print("Columnas de perfil ya existen")

    finally:
        conn.close()


def clasificar_todos():
    """Clasifica todos los candidatos y actualiza la BD."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Obtener todos los candidatos
            cur.execute("""
                SELECT id, puesto_actual, carnet_c
                FROM candidatos
            """)
            candidatos = cur.fetchall()

            # Obtener IDs de perfiles
            cur.execute("SELECT id, codigo FROM perfiles")
            perfiles_map = {row[1]: row[0] for row in cur.fetchall()}

            # Clasificar y actualizar
            stats = {}
            for cand_id, puesto, carnet_c in candidatos:
                perfil = clasificar_candidato(puesto, carnet_c, False)
                perfil_id = perfiles_map.get(perfil)

                cur.execute("""
                    UPDATE candidatos
                    SET perfil_id = %s, perfil_codigo = %s
                    WHERE id = %s
                """, (perfil_id, perfil, cand_id))

                stats[perfil] = stats.get(perfil, 0) + 1

            conn.commit()

            # Mostrar estadísticas
            print("\n=== CLASIFICACIÓN COMPLETADA ===\n")
            total = sum(stats.values())
            for perfil, count in sorted(stats.items(), key=lambda x: -x[1]):
                pct = (count / total) * 100
                print(f"  {perfil:20} {count:4} candidatos ({pct:.1f}%)")
            print(f"\n  {'TOTAL':20} {total:4} candidatos")

            return stats

    finally:
        conn.close()


def listar_por_perfil(perfil_codigo: str = None, limit: int = 50):
    """Lista candidatos de un perfil específico."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            if perfil_codigo:
                cur.execute("""
                    SELECT id, CONCAT(nombre, ' ', apellido1) as nombre_completo,
                           puesto_actual, residencia, anos_experiencia, carnet_c
                    FROM candidatos
                    WHERE perfil_codigo = %s
                    ORDER BY anos_experiencia DESC
                    LIMIT %s
                """, (perfil_codigo.upper(), limit))
            else:
                cur.execute("""
                    SELECT perfil_codigo, COUNT(*) as total
                    FROM candidatos
                    GROUP BY perfil_codigo
                    ORDER BY total DESC
                """)

            return cur.fetchall()

    finally:
        conn.close()


def main():
    """CLI del clasificador."""
    import sys

    if len(sys.argv) < 2:
        print("Uso:")
        print("  python clasificador.py setup       # Crear tablas y columnas")
        print("  python clasificador.py run         # Clasificar todos los candidatos")
        print("  python clasificador.py stats       # Ver estadísticas")
        print("  python clasificador.py list <PERFIL>  # Listar candidatos de un perfil")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "setup":
        print("Configurando tablas...")
        crear_tabla_perfiles()
        agregar_columna_perfil()
        print("Setup completado")

    elif cmd == "run":
        print("Clasificando candidatos...")
        clasificar_todos()

    elif cmd == "stats":
        results = listar_por_perfil()
        print("\n=== ESTADÍSTICAS POR PERFIL ===\n")
        for row in results:
            print(f"  {row[0] or 'SIN_CLASIFICAR':20} {row[1]:4} candidatos")

    elif cmd == "list":
        if len(sys.argv) < 3:
            print("Especifica el perfil: PESCADERIA, LOGISTICA, PRODUCCION, ADMINISTRATIVO, GESTION")
            sys.exit(1)

        perfil = sys.argv[2].upper()
        results = listar_por_perfil(perfil)

        print(f"\n=== {perfil} ===\n")
        print(f"{'ID':>4} | {'Nombre':25} | {'Puesto':30} | {'Ciudad':15} | {'Exp':>5} | {'C'}")
        print("-" * 95)

        for row in results:
            carnet = "[C]" if row[5] else ""
            print(f"{row[0]:>4} | {(row[1] or '')[:25]:25} | {(row[2] or '')[:30]:30} | {(row[3] or '')[:15]:15} | {row[4] or 0:>5.1f} | {carnet}")

    else:
        print(f"Comando desconocido: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()

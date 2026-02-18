import pymysql

conn = pymysql.connect(
    host='192.168.1.133',
    port=3306,
    user='root',
    password='Carihuela.Local#2026',
    database='gestion.pescadoslacarihuela.es',
    charset='utf8mb4'
)

cursor = conn.cursor(pymysql.cursors.DictCursor)

# Los permisos del usuario tienen IDs como 71, 116, 191, 319, 492, 498
# Buscar tablas con IDs en ese rango que tengan campo de descripcion

print("=== Buscando tabla con permisos ===\n")

# Primero ver todas las tablas
cursor.execute("""
    SELECT TABLE_NAME FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = 'gestion.pescadoslacarihuela.es'
""")
tablas = [r['TABLE_NAME'] for r in cursor.fetchall()]

# Buscar tablas que tengan IDs 71, 191, 319, 498 Y un campo varchar
ids_buscar = [71, 191, 319, 498]

for tabla in tablas:
    try:
        # Ver si tiene ID y varchar
        cursor.execute("""
            SELECT COLUMN_NAME FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = 'gestion.pescadoslacarihuela.es'
            AND TABLE_NAME = %s
        """, (tabla,))
        cols = [r['COLUMN_NAME'] for r in cursor.fetchall()]

        if 'id' in cols:
            # Buscar si tiene los IDs
            cursor.execute("SELECT COUNT(*) as c FROM `" + tabla + "` WHERE id IN (71, 191, 319, 498)")
            count = cursor.fetchone()['c']
            if count >= 3:
                print("*** " + tabla + " tiene " + str(count) + " de los IDs buscados ***")
                cursor.execute("SELECT * FROM `" + tabla + "` WHERE id IN (71, 72, 73, 74, 75) LIMIT 5")
                for row in cursor.fetchall():
                    print("  " + str(row))
                print()
    except Exception as e:
        pass

conn.close()

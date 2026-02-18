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

# Listar todas las tablas
cursor.execute("""
    SELECT TABLE_NAME FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = 'gestion.pescadoslacarihuela.es'
""")
tablas = [r['TABLE_NAME'] for r in cursor.fetchall()]

print(f"Total tablas: {len(tablas)}")
print("Buscando 'Acceder a usuarios'...\n")

for tabla in tablas:
    try:
        # Obtener columnas varchar
        cursor.execute(f"""
            SELECT COLUMN_NAME FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = 'gestion.pescadoslacarihuela.es'
            AND TABLE_NAME = %s AND DATA_TYPE IN ('varchar', 'text', 'char')
        """, (tabla,))
        columnas = [r['COLUMN_NAME'] for r in cursor.fetchall()]

        for col in columnas:
            try:
                cursor.execute(f"SELECT * FROM `{tabla}` WHERE `{col}` LIKE %s LIMIT 1", ('%Acceder a usuarios%',))
                rows = cursor.fetchall()
                if rows:
                    print(f"*** ENCONTRADO EN: {tabla}.{col} ***")
                    cursor.execute(f"SELECT * FROM `{tabla}` WHERE `{col}` LIKE %s LIMIT 20", ('%Acceder%',))
                    for row in cursor.fetchall():
                        print(row)
                    print("\n")
            except:
                pass
    except:
        pass

conn.close()

#!/usr/bin/env python3
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

print('=== ESTADO ACTUAL DEL SISTEMA ===')
print()

# Peticiones
cursor.execute("SELECT COUNT(*) as total, SUM(estado='ABIERTA') as abiertas FROM peticiones_trabajador")
pet = cursor.fetchone()
print(f"Peticiones: {pet['total']} total, {int(pet['abiertas'] or 0)} abiertas")

# Candidatos
cursor.execute('SELECT COUNT(*) as total FROM candidatos')
cand = cursor.fetchone()
print(f"Candidatos: {cand['total']} total")

# Candidatos por perfil
cursor.execute('SELECT perfil_codigo, COUNT(*) as c FROM candidatos WHERE perfil_codigo IS NOT NULL GROUP BY perfil_codigo ORDER BY c DESC')
print('\nCandidatos por perfil:')
for row in cursor.fetchall():
    print(f"  {row['perfil_codigo']}: {row['c']}")

# Candidatos sin perfil
cursor.execute('SELECT COUNT(*) as c FROM candidatos WHERE perfil_codigo IS NULL')
sin = cursor.fetchone()
print(f"  SIN PERFIL: {sin['c']}")

# Estados de candidatos
print('\nCandidatos por estado:')
cursor.execute('SELECT estado_seleccion, COUNT(*) as c FROM candidatos GROUP BY estado_seleccion ORDER BY c DESC')
for row in cursor.fetchall():
    estado = row['estado_seleccion'] or 'NULL'
    print(f"  {estado}: {row['c']}")

# Perfiles disponibles
print('\nPerfiles disponibles:')
try:
    cursor.execute('SELECT codigo, nombre FROM perfiles ORDER BY codigo')
    for row in cursor.fetchall():
        print(f"  {row['codigo']}: {row['nombre']}")
except:
    print("  (tabla perfiles no existe)")

conn.close()

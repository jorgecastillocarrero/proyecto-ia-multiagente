#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crear tablas de peticiones de trabajador
Ejecutar una sola vez
"""

import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', '192.168.1.133'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'Carihuela.Local#2026'),
    'database': os.getenv('DB_NAME', 'gestion.pescadoslacarihuela.es'),
    'charset': 'utf8mb4'
}

def setup():
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            # Crear tabla peticiones_trabajador
            print("Creando tabla peticiones_trabajador...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS peticiones_trabajador (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    perfil_codigo VARCHAR(50) NOT NULL,
                    posicion VARCHAR(200) NOT NULL COMMENT 'Nombre especifico del puesto',
                    solicitante_rol ENUM('GERENTE', 'DIRECTOR_RRHH') NOT NULL,
                    solicitante_nombre VARCHAR(100),
                    fecha_solicitud DATE NOT NULL,
                    publicado_en VARCHAR(100) COMMENT 'InfoJobs, LinkedIn, etc.',
                    fecha_publicacion_desde DATE,
                    fecha_publicacion_hasta DATE,
                    estado ENUM('ABIERTA', 'EN_PROCESO', 'CUBIERTA', 'CANCELADA') DEFAULT 'ABIERTA',
                    candidato_contratado_id BIGINT UNSIGNED,
                    fecha_cubierta DATE,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_perfil (perfil_codigo),
                    INDEX idx_estado (estado),
                    INDEX idx_fecha (fecha_solicitud)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            conn.commit()
            print("OK")

            # Verificar si hay datos
            cursor.execute("SELECT COUNT(*) FROM peticiones_trabajador")
            count = cursor.fetchone()[0]

            if count == 0:
                print("Insertando datos iniciales...")
                cursor.execute("""
                    INSERT INTO peticiones_trabajador
                    (perfil_codigo, posicion, solicitante_rol, solicitante_nombre, fecha_solicitud, publicado_en, fecha_publicacion_desde, fecha_publicacion_hasta, estado)
                    VALUES
                    ('LOGISTICA', 'Operario/a Logistica', 'GERENTE', 'Gerente', '2026-01-15', 'InfoJobs', '2026-01-27', '2026-03-28', 'ABIERTA'),
                    ('PESCADERIA', 'Dependiente/a Pescaderia', 'GERENTE', 'Gerente', '2026-02-13', 'InfoJobs', '2026-02-13', '2026-04-14', 'ABIERTA'),
                    ('BECARIO', 'Becario Administracion', 'GERENTE', 'Gerente', '2026-02-01', NULL, NULL, NULL, 'ABIERTA')
                """)
                conn.commit()
                print("OK - 3 peticiones insertadas")
            else:
                print(f"Ya existen {count} peticiones en la tabla")

            # Crear tabla alertas_peticion
            print("Creando tabla alertas_peticion...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alertas_peticion (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    peticion_id INT NOT NULL,
                    tipo_alerta ENUM('NUEVA_PETICION', 'PETICION_CUBIERTA', 'PETICION_CANCELADA') NOT NULL,
                    mensaje TEXT,
                    estado ENUM('PENDIENTE', 'VISTA', 'COMPLETADA') DEFAULT 'PENDIENTE',
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_peticion (peticion_id),
                    INDEX idx_estado (estado),
                    FOREIGN KEY (peticion_id) REFERENCES peticiones_trabajador(id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            conn.commit()
            print("OK")

            # Mostrar datos
            print("\nPeticiones de trabajador:")
            cursor.execute("SELECT id, perfil_codigo, posicion, estado FROM peticiones_trabajador")
            for row in cursor.fetchall():
                print(f"  {row[0]}: {row[1]} - {row[2]} ({row[3]})")

            print("\nSetup completado!")

    finally:
        conn.close()

if __name__ == '__main__':
    setup()

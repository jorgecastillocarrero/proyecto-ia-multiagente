-- Script para crear tablas de peticiones de trabajador
-- Ejecutar una sola vez

-- Tabla: peticiones_trabajador
CREATE TABLE IF NOT EXISTS peticiones_trabajador (
    id INT AUTO_INCREMENT PRIMARY KEY,
    perfil_codigo VARCHAR(50) NOT NULL,
    posicion VARCHAR(200) NOT NULL COMMENT 'Nombre especifico del puesto',
    solicitante_rol ENUM('GERENTE', 'DIRECTOR_RRHH') NOT NULL,
    solicitante_nombre VARCHAR(100),
    fecha_solicitud DATE NOT NULL,

    -- Publicacion
    publicado_en VARCHAR(100) COMMENT 'InfoJobs, LinkedIn, etc.',
    fecha_publicacion_desde DATE,
    fecha_publicacion_hasta DATE,

    -- Estado
    estado ENUM('ABIERTA', 'EN_PROCESO', 'CUBIERTA', 'CANCELADA') DEFAULT 'ABIERTA',

    -- Relacion con candidato contratado (cuando se cubre)
    candidato_contratado_id BIGINT UNSIGNED,
    fecha_cubierta DATE,

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_perfil (perfil_codigo),
    INDEX idx_estado (estado),
    INDEX idx_fecha (fecha_solicitud)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Datos iniciales: Peticiones de trabajador
INSERT INTO peticiones_trabajador (perfil_codigo, posicion, solicitante_rol, solicitante_nombre, fecha_solicitud, publicado_en, fecha_publicacion_desde, fecha_publicacion_hasta, estado) VALUES
('LOGISTICA', 'Operario/a Logistica', 'GERENTE', 'Gerente', '2026-01-15', 'InfoJobs', '2026-01-27', '2026-03-28', 'ABIERTA'),
('PESCADERIA', 'Dependiente/a Pescaderia', 'GERENTE', 'Gerente', '2026-02-13', 'InfoJobs', '2026-02-13', '2026-04-14', 'ABIERTA'),
('BECARIO', 'Becario Administracion', 'GERENTE', 'Gerente', '2026-02-01', NULL, NULL, NULL, 'ABIERTA')
ON DUPLICATE KEY UPDATE posicion = VALUES(posicion);

-- Tabla: alertas_peticion
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

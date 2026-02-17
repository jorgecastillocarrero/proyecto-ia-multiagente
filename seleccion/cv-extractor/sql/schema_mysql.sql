-- ============================================================================
-- SCHEMA MYSQL - SISTEMA DE SELECCION RRHH
-- Pescados La Carihuela
-- ============================================================================
-- Autor: Equipo RRHH
-- Fecha: 2026-02-17
-- Base de datos: gestion.pescadoslacarihuela.es
-- Servidor: 192.168.1.133:3306
-- ============================================================================

-- -----------------------------------------------------------------------------
-- NOTA: Este schema documenta las tablas creadas/modificadas para el sistema
-- de seleccion. La tabla 'candidatos' ya existia y se le añadieron columnas.
-- -----------------------------------------------------------------------------

-- =============================================================================
-- TABLA: PERFILES DE TRABAJO
-- Almacena los perfiles profesionales para clasificar candidatos
-- =============================================================================
CREATE TABLE IF NOT EXISTS perfiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL COMMENT 'Codigo unico del perfil',
    nombre VARCHAR(100) NOT NULL COMMENT 'Nombre visible del perfil',
    descripcion TEXT COMMENT 'Descripcion del perfil',
    keywords TEXT COMMENT 'Palabras clave separadas por coma para clasificacion',
    activo TINYINT(1) DEFAULT 1 COMMENT '1=Activo, 0=Inactivo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Datos iniciales de perfiles
INSERT INTO perfiles (codigo, nombre, descripcion, keywords) VALUES
('PESCADERIA', 'Pescaderia', 'Pescaderia, carniceria, comercio, dependiente de tienda',
 'pescad,carnicer,charcuter,corte,filete,marisco,mostrador,fresco,despiece,dependient,tienda,comercio'),
('LOGISTICA', 'Logistica', 'Logistica, almacen, reparto, transporte',
 'logistic,almacen,reparto,repartidor,transporte,carretiller,mozo,carga,descarga,picking,conductor,camion,furgoneta'),
('PRODUCCION', 'Produccion', 'Produccion, sushi, sala de envase',
 'sushi,envase,envasado,produccion,fabrica,operario,linea,manipulador,elaboracion'),
('ADMINISTRATIVO', 'Administrativo', 'Administrativo, secretariado, FP administracion',
 'secretari,administrativ,contab,factur,oficina,recepcion,auxiliar admin'),
('GESTION', 'Gestion', 'Gestion, grados universitarios (ADE, Derecho, etc.)',
 'grado ade,grado derecho,licenciado,graduado,master,mba,universidad')
ON DUPLICATE KEY UPDATE descripcion = VALUES(descripcion), keywords = VALUES(keywords);


-- =============================================================================
-- TABLA: MOTIVOS DE DESCARTE
-- Catalogo de motivos por los que se descarta un candidato
-- =============================================================================
CREATE TABLE IF NOT EXISTS motivos_descarte (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL COMMENT 'Codigo unico del motivo',
    descripcion VARCHAR(200) NOT NULL COMMENT 'Descripcion del motivo',
    tipo ENUM('AUTOMATICO', 'MANUAL') NOT NULL COMMENT 'Tipo de descarte',
    parametro_valor VARCHAR(50) COMMENT 'Valor configurable (ej: 1 año, 40 km)',
    activo TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Motivos predefinidos
INSERT INTO motivos_descarte (codigo, descripcion, tipo, parametro_valor) VALUES
('SIN_EXPERIENCIA', 'Experiencia menor a 1 año', 'AUTOMATICO', '1'),
('DISTANCIA_EXCEDIDA', 'Distancia mayor a 40 km', 'AUTOMATICO', '40'),
('DESCARTADO_PREVIO', 'Descartado en proceso anterior', 'AUTOMATICO', NULL),
('MALAS_REFERENCIAS', 'Malas referencias', 'MANUAL', NULL),
('NO_INTERESADO', 'Candidato no interesado', 'MANUAL', NULL),
('NO_CONTESTA', 'No contesta tras varios intentos', 'MANUAL', NULL),
('DESCARTADO_ENTREVISTA', 'Descartado tras entrevista', 'MANUAL', NULL),
('OTROS', 'Otros motivos', 'MANUAL', NULL)
ON DUPLICATE KEY UPDATE descripcion = VALUES(descripcion);


-- =============================================================================
-- TABLA: CANDIDATOS DESCARTADOS
-- Registro historico de descartes con motivo y responsable
-- =============================================================================
CREATE TABLE IF NOT EXISTS candidatos_descartados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidato_id BIGINT UNSIGNED NOT NULL COMMENT 'FK a candidatos',
    motivo_id INT NOT NULL COMMENT 'FK a motivos_descarte',
    descartado_por VARCHAR(100) COMMENT 'Nombre de quien descarto (Antonio, Carlos, Jorge)',
    fecha_descarte TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notas TEXT COMMENT 'Notas adicionales',
    proceso VARCHAR(100) COMMENT 'Proceso/oferta en el que se descarto',

    FOREIGN KEY (candidato_id) REFERENCES candidatos(id) ON DELETE CASCADE,
    FOREIGN KEY (motivo_id) REFERENCES motivos_descarte(id),
    INDEX idx_candidato (candidato_id),
    INDEX idx_motivo (motivo_id),
    INDEX idx_fecha (fecha_descarte)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================================================
-- TABLA: REGLAS DE DESCARTE
-- Reglas configurables para descarte automatico
-- =============================================================================
CREATE TABLE IF NOT EXISTS reglas_descarte (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    descripcion VARCHAR(200),
    campo VARCHAR(50) NOT NULL COMMENT 'Campo de candidatos a evaluar',
    operador ENUM('<', '>', '<=', '>=', '=', '!=') NOT NULL,
    valor VARCHAR(50) NOT NULL COMMENT 'Valor a comparar',
    motivo_id INT NOT NULL COMMENT 'FK a motivos_descarte',
    activo TINYINT(1) DEFAULT 1,
    orden INT DEFAULT 0 COMMENT 'Orden de evaluacion',

    FOREIGN KEY (motivo_id) REFERENCES motivos_descarte(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Reglas predefinidas
INSERT INTO reglas_descarte (codigo, descripcion, campo, operador, valor, motivo_id, orden)
SELECT 'REGLA_EXPERIENCIA', 'Experiencia minima 1 año', 'anos_experiencia', '<', '1', id, 1
FROM motivos_descarte WHERE codigo = 'SIN_EXPERIENCIA'
ON DUPLICATE KEY UPDATE descripcion = VALUES(descripcion);

INSERT INTO reglas_descarte (codigo, descripcion, campo, operador, valor, motivo_id, orden)
SELECT 'REGLA_DISTANCIA', 'Distancia maxima 40 km', 'distancia_km', '>', '40', id, 2
FROM motivos_descarte WHERE codigo = 'DISTANCIA_EXCEDIDA'
ON DUPLICATE KEY UPDATE descripcion = VALUES(descripcion);


-- =============================================================================
-- COLUMNAS AÑADIDAS A TABLA CANDIDATOS (ya existente)
-- =============================================================================
-- Las siguientes columnas fueron añadidas a la tabla candidatos:
--
-- ALTER TABLE candidatos ADD COLUMN provincia VARCHAR(100);
-- ALTER TABLE candidatos ADD COLUMN codigo_postal VARCHAR(10);
-- ALTER TABLE candidatos ADD COLUMN puesto_actual VARCHAR(200);
-- ALTER TABLE candidatos ADD COLUMN carnet_carretillero TINYINT(1) DEFAULT 0;
-- ALTER TABLE candidatos ADD COLUMN anos_experiencia DECIMAL(5,2);
-- ALTER TABLE candidatos ADD COLUMN archivo_origen VARCHAR(500);
-- ALTER TABLE candidatos ADD COLUMN perfil_id INT;
-- ALTER TABLE candidatos ADD COLUMN perfil_codigo VARCHAR(50);
-- ALTER TABLE candidatos ADD INDEX idx_perfil (perfil_id);


-- =============================================================================
-- VISTAS UTILES
-- =============================================================================

-- Vista: Resumen por perfil
CREATE OR REPLACE VIEW v_resumen_perfiles AS
SELECT
    COALESCE(c.perfil_codigo, 'SIN_ASIGNAR') as perfil,
    COUNT(*) as total,
    SUM(CASE WHEN c.estado_global = 'NUEVO' THEN 1 ELSE 0 END) as nuevos,
    SUM(CASE WHEN c.estado_global = 'ENTREVISTANDO' THEN 1 ELSE 0 END) as entrevistando,
    SUM(CASE WHEN c.estado_global = 'CONTRATADO' THEN 1 ELSE 0 END) as contratados,
    SUM(CASE WHEN c.estado_global = 'DESCARTADO' THEN 1 ELSE 0 END) as descartados
FROM candidatos c
GROUP BY c.perfil_codigo;


-- Vista: Candidatos con perfil
CREATE OR REPLACE VIEW v_candidatos_perfil AS
SELECT
    c.id,
    CONCAT(c.nombre, ' ', c.apellido1, ' ', COALESCE(c.apellido2, '')) as nombre_completo,
    c.email,
    c.telefono,
    c.residencia as ciudad,
    c.provincia,
    c.puesto_actual,
    c.anos_experiencia,
    c.carnet_b,
    c.carnet_c,
    c.vehiculo_propio,
    c.perfil_codigo,
    c.estado_global
FROM candidatos c;


-- =============================================================================
-- FIN DEL SCHEMA
-- =============================================================================

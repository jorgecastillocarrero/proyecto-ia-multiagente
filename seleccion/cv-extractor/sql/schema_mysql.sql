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
-- ALTER TABLE candidatos ADD COLUMN vehiculo_propio TINYINT(1) DEFAULT 0;
-- ALTER TABLE candidatos ADD COLUMN cap TINYINT(1) DEFAULT 0 COMMENT 'Certificado CAP';
-- ALTER TABLE candidatos ADD COLUMN anos_experiencia DECIMAL(5,2);
-- ALTER TABLE candidatos ADD COLUMN estudios_reglados VARCHAR(200) COMMENT 'Estudios reglados';
-- ALTER TABLE candidatos ADD COLUMN curriculum TEXT COMMENT 'CV convertido/estructurado';
-- ALTER TABLE candidatos ADD COLUMN archivo_origen VARCHAR(500);
-- ALTER TABLE candidatos ADD COLUMN perfil_id INT;
-- ALTER TABLE candidatos ADD COLUMN perfil_codigo VARCHAR(50);
-- ALTER TABLE candidatos ADD COLUMN entrevista_primera_fase ENUM('SI', 'NO', 'PENDIENTE') DEFAULT 'PENDIENTE' COMMENT 'Decision primera fase';
-- ALTER TABLE candidatos ADD COLUMN estado_seleccion ENUM('PENDIENTE_ASIGNAR', 'EN_PERFIL', 'LLAMADAS', 'ENTREVISTAS', 'CODIGOS', 'DESCARTADO', 'CONTRATADO') DEFAULT 'PENDIENTE_ASIGNAR';
-- ALTER TABLE candidatos ADD INDEX idx_perfil (perfil_id);
-- ALTER TABLE candidatos ADD INDEX idx_estado_seleccion (estado_seleccion);


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


-- Vista: Candidatos con perfil (16 campos documentados)
CREATE OR REPLACE VIEW v_candidatos_perfil AS
SELECT
    c.id,
    c.nombre,
    c.apellido1 as apellido,
    c.telefono,
    c.email,
    c.residencia as localidad,
    c.vehiculo_propio as veh,
    c.carnet_b as b,
    c.carnet_c as c_carnet,
    c.cap,
    c.carnet_carretillero as carr,
    c.perfil_codigo as puesto,
    c.anos_experiencia as exp,
    c.estudios_reglados as estudios,
    c.curriculum as cv,
    c.entrevista_primera_fase as entrevista,
    c.estado_seleccion
FROM candidatos c;


-- Vista: Candidatos para LLAMADAS (mismos 16 campos + historial)
CREATE OR REPLACE VIEW v_llamadas AS
SELECT
    c.id,
    c.nombre,
    c.apellido1 as apellido,
    c.telefono,
    c.email,
    c.residencia as localidad,
    c.vehiculo_propio as veh,
    c.carnet_b as b,
    c.carnet_c as c_carnet,
    c.cap,
    c.carnet_carretillero as carr,
    c.perfil_codigo as puesto,
    c.anos_experiencia as exp,
    c.estudios_reglados as estudios,
    c.curriculum as cv,
    al.resultado as entrevista,
    al.trabajador_id as asignado_a,
    al.fecha_asignacion,
    al.intentos,
    al.estado as estado_llamada
FROM candidatos c
INNER JOIN asignacion_llamadas al ON c.id = al.candidato_id
WHERE c.estado_seleccion = 'LLAMADAS';


-- Vista: ENTREVISTAS programadas
CREATE OR REPLACE VIEW v_entrevistas AS
SELECT
    e.id as entrevista_id,
    e.fecha_entrevista,
    DAYNAME(e.fecha_entrevista) as dia,
    TIME(e.fecha_entrevista) as hora,
    c.id as candidato_id,
    c.nombre,
    c.apellido1 as apellido,
    c.telefono,
    c.email,
    c.residencia as localidad,
    c.vehiculo_propio as veh,
    c.carnet_b as b,
    c.carnet_c as c_carnet,
    c.cap,
    c.carnet_carretillero as carr,
    c.perfil_codigo as puesto,
    c.anos_experiencia as exp,
    c.estudios_reglados as estudios,
    c.curriculum as cv,
    e.entrevistador_id,
    e.estado as estado_entrevista,
    e.resultado,
    e.valoracion
FROM entrevistas e
INNER JOIN candidatos c ON e.candidato_id = c.id
WHERE e.estado IN ('PROGRAMADA', 'REALIZADA');


-- Vista: Dashboard contador llamadas por trabajador
CREATE OR REPLACE VIEW v_dashboard_llamadas AS
SELECT
    al.trabajador_id,
    COUNT(*) as total_asignadas,
    SUM(CASE WHEN al.estado = 'COMPLETADA' THEN 1 ELSE 0 END) as completadas,
    SUM(CASE WHEN al.estado = 'PENDIENTE' THEN 1 ELSE 0 END) as pendientes
FROM asignacion_llamadas al
GROUP BY al.trabajador_id;


-- Vista: Dashboard contador entrevistas por entrevistador
CREATE OR REPLACE VIEW v_dashboard_entrevistas AS
SELECT
    e.entrevistador_id,
    COUNT(*) as total_entrevistas,
    SUM(CASE WHEN e.estado = 'REALIZADA' THEN 1 ELSE 0 END) as realizadas,
    SUM(CASE WHEN e.estado = 'PROGRAMADA' THEN 1 ELSE 0 END) as pendientes
FROM entrevistas e
GROUP BY e.entrevistador_id;


-- =============================================================================
-- TABLA: ASIGNACION DE LLAMADAS
-- Asignacion de candidatos a trabajadores para llamar
-- =============================================================================
CREATE TABLE IF NOT EXISTS asignacion_llamadas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidato_id BIGINT UNSIGNED NOT NULL COMMENT 'FK a candidatos',
    trabajador_id INT NOT NULL COMMENT 'FK a rrhh_flujo_trabajadores (nivel=4, activo=1)',
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('PENDIENTE', 'EN_PROCESO', 'COMPLETADA') DEFAULT 'PENDIENTE',
    resultado ENUM('SI', 'NO', 'DUDA') DEFAULT NULL COMMENT 'Resultado de la llamada',
    fecha_entrevista DATETIME DEFAULT NULL COMMENT 'Si resultado=SI, fecha/hora de entrevista',
    motivo_descarte_id INT DEFAULT NULL COMMENT 'Si resultado=NO, FK a motivos_descarte',
    intentos INT DEFAULT 0 COMMENT 'Numero de intentos de llamada',
    notas TEXT COMMENT 'Observaciones de la llamada',
    fecha_completada TIMESTAMP NULL,

    FOREIGN KEY (candidato_id) REFERENCES candidatos(id) ON DELETE CASCADE,
    FOREIGN KEY (motivo_descarte_id) REFERENCES motivos_descarte(id),
    INDEX idx_candidato (candidato_id),
    INDEX idx_trabajador (trabajador_id),
    INDEX idx_estado (estado),
    INDEX idx_fecha (fecha_asignacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================================================
-- TABLA: HISTORIAL DE DUDAS/COMENTARIOS
-- Historial de conversacion entre llamador y selector
-- =============================================================================
CREATE TABLE IF NOT EXISTS historial_dudas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidato_id BIGINT UNSIGNED NOT NULL COMMENT 'FK a candidatos',
    asignacion_id INT DEFAULT NULL COMMENT 'FK a asignacion_llamadas',
    usuario_id INT NOT NULL COMMENT 'FK a rrhh_flujo_trabajadores',
    rol ENUM('LLAMADOR', 'SELECTOR', 'ENTREVISTADOR') NOT NULL,
    comentario TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (candidato_id) REFERENCES candidatos(id) ON DELETE CASCADE,
    FOREIGN KEY (asignacion_id) REFERENCES asignacion_llamadas(id) ON DELETE SET NULL,
    INDEX idx_candidato (candidato_id),
    INDEX idx_fecha (fecha)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================================================
-- TABLA: ENTREVISTAS
-- Registro de entrevistas programadas y realizadas
-- =============================================================================
CREATE TABLE IF NOT EXISTS entrevistas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidato_id BIGINT UNSIGNED NOT NULL COMMENT 'FK a candidatos',
    asignacion_llamada_id INT DEFAULT NULL COMMENT 'FK a asignacion_llamadas',
    entrevistador_id INT NOT NULL COMMENT 'FK a rrhh_flujo_trabajadores',
    fecha_entrevista DATETIME NOT NULL COMMENT 'Fecha y hora programada',
    estado ENUM('PROGRAMADA', 'REALIZADA', 'NO_ASISTIO', 'CANCELADA') DEFAULT 'PROGRAMADA',
    resultado ENUM('ENTREGA_CODIGOS', 'NO') DEFAULT NULL,
    valoracion TEXT COMMENT 'Comentarios/valoracion del entrevistador',
    motivo_descarte_id INT DEFAULT NULL COMMENT 'Si resultado=NO, FK a motivos_descarte',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_realizacion TIMESTAMP NULL,

    FOREIGN KEY (candidato_id) REFERENCES candidatos(id) ON DELETE CASCADE,
    FOREIGN KEY (asignacion_llamada_id) REFERENCES asignacion_llamadas(id) ON DELETE SET NULL,
    FOREIGN KEY (motivo_descarte_id) REFERENCES motivos_descarte(id),
    INDEX idx_candidato (candidato_id),
    INDEX idx_entrevistador (entrevistador_id),
    INDEX idx_fecha (fecha_entrevista),
    INDEX idx_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================================================
-- TABLA: CANDIDATOS CON CODIGOS
-- Candidatos que han pasado entrevista y estan aprendiendo codigos
-- =============================================================================
CREATE TABLE IF NOT EXISTS candidatos_codigos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidato_id BIGINT UNSIGNED NOT NULL COMMENT 'FK a candidatos',
    entrevista_id INT NOT NULL COMMENT 'FK a entrevistas',
    email_enviado TINYINT(1) DEFAULT 0 COMMENT 'Email de registro enviado',
    fecha_email TIMESTAMP NULL,
    registrado TINYINT(1) DEFAULT 0 COMMENT 'Candidato se ha registrado',
    fecha_registro TIMESTAMP NULL,
    progreso_codigos INT DEFAULT 0 COMMENT 'Porcentaje de codigos aprendidos',
    ultimo_acceso TIMESTAMP NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (candidato_id) REFERENCES candidatos(id) ON DELETE CASCADE,
    FOREIGN KEY (entrevista_id) REFERENCES entrevistas(id) ON DELETE CASCADE,
    UNIQUE KEY uk_candidato (candidato_id),
    INDEX idx_entrevista (entrevista_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================================================
-- TABLA: CODIGOS DE ARTICULOS
-- Catalogo de codigos que los candidatos deben aprender
-- =============================================================================
CREATE TABLE IF NOT EXISTS codigos_articulos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(10) NOT NULL COMMENT 'Codigo del articulo (ej: 90)',
    nombre VARCHAR(200) NOT NULL COMMENT 'Nombre del articulo',
    categoria VARCHAR(100) COMMENT 'Categoria del producto',
    activo TINYINT(1) DEFAULT 1,

    UNIQUE KEY uk_codigo (codigo),
    INDEX idx_categoria (categoria)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================================================
-- TABLA: PROGRESO CODIGOS (Gaming)
-- Registro de respuestas del candidato en el sistema de aprendizaje
-- =============================================================================
CREATE TABLE IF NOT EXISTS progreso_codigos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidato_codigo_id INT NOT NULL COMMENT 'FK a candidatos_codigos',
    codigo_articulo_id INT NOT NULL COMMENT 'FK a codigos_articulos',
    aciertos INT DEFAULT 0,
    fallos INT DEFAULT 0,
    ultima_respuesta TIMESTAMP NULL,
    aprendido TINYINT(1) DEFAULT 0 COMMENT 'Codigo considerado aprendido',

    FOREIGN KEY (candidato_codigo_id) REFERENCES candidatos_codigos(id) ON DELETE CASCADE,
    FOREIGN KEY (codigo_articulo_id) REFERENCES codigos_articulos(id) ON DELETE CASCADE,
    UNIQUE KEY uk_candidato_codigo (candidato_codigo_id, codigo_articulo_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================================================
-- MOTIVOS DE DESCARTE ADICIONALES (para entrevistas)
-- =============================================================================
INSERT INTO motivos_descarte (codigo, descripcion, tipo) VALUES
('NO_APTO_PUESTO', 'No apto para el puesto', 'MANUAL'),
('FALTA_EXPERIENCIA', 'Falta de experiencia requerida', 'MANUAL'),
('NO_ENCAJA_EQUIPO', 'No encaja con el equipo', 'MANUAL'),
('NO_ASISTIO_ENTREVISTA', 'No asistio a la entrevista', 'MANUAL'),
('NUMERO_ERRONEO', 'Numero de telefono erroneo', 'MANUAL')
ON DUPLICATE KEY UPDATE descripcion = VALUES(descripcion);


-- =============================================================================
-- TABLA: HISTORIAL CANDIDATO (Ficha completa)
-- Registro de todas las acciones sobre un candidato
-- =============================================================================
CREATE TABLE IF NOT EXISTS historial_candidato (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidato_id BIGINT UNSIGNED NOT NULL COMMENT 'FK a candidatos',
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tipo_accion ENUM(
        'ASIGNACION_PERFIL',
        'SELECCION_ENTREVISTA',
        'LLAMADA',
        'DUDA_LLAMADA',
        'RESPUESTA_DUDA',
        'ENTREVISTA_1',
        'ENTREGA_CODIGOS',
        'LLAMADA_2A_ENTREVISTA',
        'ENTREVISTA_2',
        'CONTRATADO',
        'DESCARTADO'
    ) NOT NULL,
    usuario_id INT COMMENT 'FK a rrhh_flujo_trabajadores',
    usuario_nombre VARCHAR(100) COMMENT 'Nombre del usuario',
    descripcion TEXT COMMENT 'Descripcion de la accion',
    comentarios TEXT COMMENT 'Comentarios adicionales',
    resultado VARCHAR(50) COMMENT 'Resultado de la accion (SI/NO/DUDA/CONTRATADO/etc)',

    FOREIGN KEY (candidato_id) REFERENCES candidatos(id) ON DELETE CASCADE,
    INDEX idx_candidato (candidato_id),
    INDEX idx_fecha (fecha),
    INDEX idx_tipo (tipo_accion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================================================
-- TABLA: SEGUNDA ENTREVISTA
-- Registro de segundas entrevistas (post-codigos)
-- =============================================================================
CREATE TABLE IF NOT EXISTS segundas_entrevistas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidato_id BIGINT UNSIGNED NOT NULL COMMENT 'FK a candidatos',
    primera_entrevista_id INT NOT NULL COMMENT 'FK a entrevistas (primera)',
    entrevistador_id INT NOT NULL COMMENT 'FK a rrhh_flujo_trabajadores',
    fecha_entrevista DATETIME NOT NULL COMMENT 'Fecha y hora programada',
    estado ENUM('PROGRAMADA', 'REALIZADA', 'NO_ASISTIO', 'CANCELADA') DEFAULT 'PROGRAMADA',
    resultado ENUM('CONTRATADO', 'NO', 'DUDA') DEFAULT NULL,
    valoracion TEXT COMMENT 'Comentarios/valoracion del entrevistador',
    motivo_descarte_id INT DEFAULT NULL COMMENT 'Si resultado=NO, FK a motivos_descarte',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_realizacion TIMESTAMP NULL,

    FOREIGN KEY (candidato_id) REFERENCES candidatos(id) ON DELETE CASCADE,
    FOREIGN KEY (primera_entrevista_id) REFERENCES entrevistas(id) ON DELETE CASCADE,
    FOREIGN KEY (motivo_descarte_id) REFERENCES motivos_descarte(id),
    INDEX idx_candidato (candidato_id),
    INDEX idx_entrevistador (entrevistador_id),
    INDEX idx_fecha (fecha_entrevista),
    INDEX idx_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================================================
-- TABLA: CONTRATADOS
-- Candidatos que han completado el proceso de seleccion
-- =============================================================================
CREATE TABLE IF NOT EXISTS contratados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidato_id BIGINT UNSIGNED NOT NULL COMMENT 'FK a candidatos',
    segunda_entrevista_id INT NOT NULL COMMENT 'FK a segundas_entrevistas',
    fecha_contratacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    perfil_contratado VARCHAR(50) COMMENT 'Perfil para el que fue contratado',
    observaciones TEXT COMMENT 'Observaciones finales',

    FOREIGN KEY (candidato_id) REFERENCES candidatos(id) ON DELETE CASCADE,
    FOREIGN KEY (segunda_entrevista_id) REFERENCES segundas_entrevistas(id) ON DELETE CASCADE,
    UNIQUE KEY uk_candidato (candidato_id),
    INDEX idx_fecha (fecha_contratacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================================================
-- VISTA: Ficha completa del candidato
-- =============================================================================
CREATE OR REPLACE VIEW v_ficha_candidato AS
SELECT
    c.id,
    c.nombre,
    c.apellido1 as apellido,
    c.telefono,
    c.email,
    c.residencia as localidad,
    c.perfil_codigo as perfil,
    c.estado_seleccion,
    c.anos_experiencia as experiencia,
    (SELECT COUNT(*) FROM historial_candidato hc WHERE hc.candidato_id = c.id) as total_acciones,
    (SELECT MAX(fecha) FROM historial_candidato hc WHERE hc.candidato_id = c.id) as ultima_accion
FROM candidatos c;


-- =============================================================================
-- VISTA: Historial detallado del candidato
-- =============================================================================
CREATE OR REPLACE VIEW v_historial_detalle AS
SELECT
    hc.candidato_id,
    hc.fecha,
    hc.tipo_accion,
    hc.usuario_nombre,
    hc.descripcion,
    hc.comentarios,
    hc.resultado
FROM historial_candidato hc
ORDER BY hc.candidato_id, hc.fecha;


-- =============================================================================
-- VISTA: Dashboard segundas entrevistas
-- =============================================================================
CREATE OR REPLACE VIEW v_dashboard_segundas_entrevistas AS
SELECT
    se.entrevistador_id,
    COUNT(*) as total_entrevistas,
    SUM(CASE WHEN se.estado = 'REALIZADA' THEN 1 ELSE 0 END) as realizadas,
    SUM(CASE WHEN se.estado = 'PROGRAMADA' THEN 1 ELSE 0 END) as pendientes
FROM segundas_entrevistas se
GROUP BY se.entrevistador_id;


-- =============================================================================
-- ACTUALIZAR ESTADO CANDIDATOS
-- =============================================================================
-- ALTER TABLE candidatos MODIFY COLUMN estado_seleccion
--     ENUM('PENDIENTE_ASIGNAR', 'EN_PERFIL', 'LLAMADAS', 'ENTREVISTAS', 'CODIGOS',
--          'LLAMADA_2A', 'SEGUNDA_ENTREVISTA', 'CONTRATADO', 'DESCARTADO')
--     DEFAULT 'PENDIENTE_ASIGNAR';


-- =============================================================================
-- INTEGRACION ERP: CONTRATADO → OPERADORES
-- =============================================================================

-- Procedimiento para crear empleado en ERP cuando candidato es contratado
DELIMITER //

CREATE PROCEDURE IF NOT EXISTS sp_contratar_candidato(
    IN p_candidato_id BIGINT UNSIGNED,
    IN p_id_empresa CHAR(3),
    IN p_categoria_profesional_id INT,
    IN p_horas_semana INT,
    IN p_tcontrato INT,
    IN p_dias VARCHAR(255),
    IN p_horario VARCHAR(255),
    OUT p_operador_id INT,
    OUT p_contrato_id BIGINT
)
BEGIN
    DECLARE v_nombre VARCHAR(100);
    DECLARE v_apellido1 VARCHAR(100);
    DECLARE v_apellido2 VARCHAR(100);
    DECLARE v_email VARCHAR(255);
    DECLARE v_telefono VARCHAR(20);
    DECLARE v_dni VARCHAR(255);
    DECLARE v_residencia VARCHAR(100);
    DECLARE v_provincia VARCHAR(100);
    DECLARE v_codigo_postal VARCHAR(10);

    -- Obtener datos del candidato
    SELECT nombre, apellido1, apellido2, email, telefono, dni,
           residencia, provincia, codigo_postal
    INTO v_nombre, v_apellido1, v_apellido2, v_email, v_telefono, v_dni,
         v_residencia, v_provincia, v_codigo_postal
    FROM candidatos
    WHERE id = p_candidato_id;

    -- 1. Insertar en operadores (ERP)
    INSERT INTO operadores (
        Nombre,
        Apellido1,
        Apellido2,
        email,
        telefono,
        Nif,
        Poblacion,
        Provincia,
        Cp,
        categoria_profesional_id,
        idEmpresa,
        activo,
        borrado,
        horas_semana,
        tcontrato,
        fecha_desde,
        created_at
    ) VALUES (
        LEFT(v_nombre, 30),
        LEFT(v_apellido1, 15),
        LEFT(v_apellido2, 15),
        v_email,
        v_telefono,
        v_dni,
        LEFT(v_residencia, 50),
        LEFT(v_provincia, 50),
        LEFT(v_codigo_postal, 5),
        p_categoria_profesional_id,
        p_id_empresa,
        1,  -- activo
        0,  -- no borrado
        p_horas_semana,
        p_tcontrato,
        CURDATE(),
        NOW()
    );

    -- Obtener el ID del nuevo operador
    SET p_operador_id = LAST_INSERT_ID();

    -- 2. Insertar en contratos_usuario
    INSERT INTO contratos_usuario (
        user_id,
        categoria_profesional_id,
        horas_semana,
        tcontrato,
        dias,
        horario,
        fecha_desde,
        created_at
    ) VALUES (
        p_operador_id,
        p_categoria_profesional_id,
        p_horas_semana,
        p_tcontrato,
        p_dias,
        p_horario,
        CURDATE(),
        NOW()
    );

    -- Obtener el ID del contrato
    SET p_contrato_id = LAST_INSERT_ID();

    -- 3. Actualizar estado del candidato
    UPDATE candidatos
    SET estado_global = 'CONTRATADO',
        updated_at = NOW()
    WHERE id = p_candidato_id;

    -- 4. Registrar en historial
    INSERT INTO historial_candidato (
        candidato_id,
        tipo_accion,
        descripcion,
        resultado
    ) VALUES (
        p_candidato_id,
        'CONTRATADO',
        CONCAT('Operador ID: ', p_operador_id, ' | Contrato ID: ', p_contrato_id),
        'CONTRATADO'
    );

    -- 5. Insertar en tabla contratados (relacion)
    INSERT INTO contratados (
        candidato_id,
        segunda_entrevista_id,
        perfil_contratado,
        observaciones
    ) VALUES (
        p_candidato_id,
        (SELECT MAX(id) FROM segundas_entrevistas WHERE candidato_id = p_candidato_id),
        (SELECT perfil_codigo FROM candidatos WHERE id = p_candidato_id),
        CONCAT('Operador ID: ', p_operador_id, ' | Contrato ID: ', p_contrato_id)
    );

    -- 6. Insertar relacion candidato-operador
    INSERT INTO candidato_operador (
        candidato_id,
        operador_id
    ) VALUES (
        p_candidato_id,
        p_operador_id
    );

END //

DELIMITER ;


-- =============================================================================
-- VISTA: Candidatos listos para contratar
-- =============================================================================
CREATE OR REPLACE VIEW v_listos_contratar AS
SELECT
    c.id,
    c.nombre,
    c.apellido1,
    c.apellido2,
    c.email,
    c.telefono,
    c.dni,
    c.residencia,
    c.provincia,
    c.codigo_postal,
    c.perfil_codigo,
    se.fecha_entrevista as fecha_segunda_entrevista,
    se.resultado,
    se.valoracion
FROM candidatos c
INNER JOIN segundas_entrevistas se ON c.id = se.candidato_id
WHERE se.resultado = 'CONTRATADO'
AND c.estado_global != 'CONTRATADO';


-- =============================================================================
-- TABLA: Relacion candidato-operador
-- =============================================================================
CREATE TABLE IF NOT EXISTS candidato_operador (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidato_id BIGINT UNSIGNED NOT NULL,
    operador_id INT NOT NULL,
    fecha_contratacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (candidato_id) REFERENCES candidatos(id) ON DELETE CASCADE,
    UNIQUE KEY uk_candidato (candidato_id),
    INDEX idx_operador (operador_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================================================
-- CODIGO SQL - POST-CONTRATACION
-- Ordenado segun secuencia del flujo documentado
-- Fecha: 2026-02-18
-- =============================================================================


-- =============================================================================
-- SECUENCIA 1: PORTAL CANDIDATO (datos minimos)
-- Cuando el candidato recibe "Entrega Codigos" en la primera entrevista
-- =============================================================================
CREATE TABLE IF NOT EXISTS portal_candidato (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidato_id BIGINT UNSIGNED NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255),
    token_registro VARCHAR(100),

    -- Datos minimos (4 campos)
    nombre VARCHAR(100) NOT NULL,
    primer_apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    correo_electronico VARCHAR(255) NOT NULL,

    -- Gaming codigos
    codigos_practicados INT DEFAULT 0,
    aciertos_totales INT DEFAULT 0,
    porcentaje_aciertos DECIMAL(5,2) DEFAULT 0,

    -- Estado
    registrado TINYINT(1) DEFAULT 0,
    fecha_registro DATETIME,
    ultimo_acceso DATETIME,
    activo TINYINT(1) DEFAULT 1,

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY uk_candidato (candidato_id),
    UNIQUE KEY uk_email (email),
    FOREIGN KEY (candidato_id) REFERENCES candidatos(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================================================
-- SECUENCIA 2: CONTRATADO → PORTAL EMPLEADO
-- Cuando el candidato pasa la ultima entrevista y se marca CONTRATADO
-- Se crea automaticamente con ID siguiente al ultimo
-- =============================================================================
CREATE TABLE IF NOT EXISTS portal_empleado (
    id INT AUTO_INCREMENT PRIMARY KEY,
    operador_id INT NOT NULL,
    candidato_id BIGINT UNSIGNED,

    -- Datos transferidos automaticamente del portal candidato (4 campos)
    nombre VARCHAR(100),
    primer_apellido VARCHAR(100),
    telefono VARCHAR(20),
    correo_electronico VARCHAR(255),

    -- Datos obligatorios que completa el trabajador (9 campos)
    dni_nie VARCHAR(20),
    cuenta_bancaria VARCHAR(34) COMMENT 'IBAN',
    naf VARCHAR(20) COMMENT 'Numero Afiliacion SS',
    direccion VARCHAR(255),
    codigo_postal VARCHAR(10),
    municipio VARCHAR(100),
    fecha_nacimiento DATE,

    -- Carnets conduccion (opcionales, obligatorios si usa vehiculo empresa)
    carnet_c TINYINT(1) DEFAULT 0,
    carnet_c_caducidad DATE,
    carnet_c_documento VARCHAR(500),

    cap TINYINT(1) DEFAULT 0,
    cap_caducidad DATE,
    cap_documento VARCHAR(500),

    carnet_carretillero TINYINT(1) DEFAULT 0,
    carnet_carretillero_caducidad DATE,
    carnet_carretillero_documento VARCHAR(500),

    certificado_puntos TINYINT(1) DEFAULT 0,
    certificado_puntos_fecha DATE,
    certificado_puntos_documento VARCHAR(500),

    tacografo TINYINT(1) DEFAULT 0,
    tacografo_caducidad DATE,
    tacografo_documento VARCHAR(500),

    -- Documentos de salud
    carnet_manipulador TINYINT(1) DEFAULT 0,
    carnet_manipulador_fecha_obtencion DATE,
    carnet_manipulador_caducidad DATE COMMENT 'fecha_obtencion + 4 años',
    carnet_manipulador_documento VARCHAR(500),

    reconocimiento_medico TINYINT(1) DEFAULT 0,
    reconocimiento_medico_fecha DATE,
    reconocimiento_medico_caducidad DATE COMMENT 'fecha + 1 año',
    reconocimiento_medico_documento VARCHAR(500),

    -- Estado de completitud
    datos_completos TINYINT(1) DEFAULT 0,
    fecha_datos_completos DATETIME,

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY uk_operador (operador_id),
    INDEX idx_candidato (candidato_id),
    FOREIGN KEY (candidato_id) REFERENCES candidatos(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================================================
-- SECUENCIA 3: ALERTAS CONTRATACION
-- Sistema de alertas para el flujo de contratacion
-- =============================================================================
CREATE TABLE IF NOT EXISTS alertas_contratacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    operador_id INT NOT NULL,
    candidato_id BIGINT UNSIGNED,

    tipo_alerta ENUM(
        'ALERTA_1_DIRECTOR_NUEVO_CONTRATADO',
        'ALERTA_2_HERMI_PENDIENTE_ALTA',
        'ALERTA_3_HERMI_DATOS_COMPLETOS',
        'ALERTA_4_DIRECTOR_FIRMA_CONTRATO',
        'ALERTA_5_TRABAJADOR_FIRMA_CONTRATO',
        'ALERTA_6_CONFIRMACION_FIRMA'
    ) NOT NULL,

    destinatario_rol ENUM('DIRECTOR_RRHH', 'HERMI_SS', 'TRABAJADOR') NOT NULL,
    destinatario_email VARCHAR(255),

    asunto VARCHAR(255),
    mensaje TEXT,

    estado ENUM('PENDIENTE', 'ENVIADA', 'LEIDA') DEFAULT 'PENDIENTE',
    fecha_envio DATETIME,
    fecha_lectura DATETIME,

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_operador (operador_id),
    INDEX idx_tipo (tipo_alerta),
    INDEX idx_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================================================
-- SECUENCIA 4: FIRMA DE CONTRATOS
-- Flujo de firma con estados
-- =============================================================================
CREATE TABLE IF NOT EXISTS firma_contratos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    operador_id INT NOT NULL,
    candidato_id BIGINT UNSIGNED,

    -- Estados del contrato (segun flujo)
    estado ENUM(
        'PENDIENTE_ALTA',
        'PENDIENTE_FIRMA_EMPRESA',
        'FIRMADO_EMPRESA',
        'FIRMADO_AMBOS'
    ) DEFAULT 'PENDIENTE_ALTA',

    -- Datos que completa Director RRHH
    categoria_profesional_id INT,
    horas_semana INT,
    fecha_inicio DATE,
    fecha_fin DATE COMMENT 'NULL si indefinido',

    -- Datos que completa Hermi
    tipo_contrato VARCHAR(100),
    codigo_contrato VARCHAR(50),

    -- Alta SS
    alta_ss_realizada TINYINT(1) DEFAULT 0,
    fecha_alta_ss DATE,

    -- Firmas
    fecha_firma_empresa DATETIME,
    firmado_por_empresa VARCHAR(100),
    fecha_firma_trabajador DATETIME,

    -- Documento
    contrato_url VARCHAR(500),
    contrato_firmado_url VARCHAR(500),

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY uk_operador (operador_id),
    INDEX idx_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================================================
-- SECUENCIA 5: PROCEDIMIENTO - Al marcar CONTRATADO
-- Crea alertas 1 y 2 automaticamente
-- =============================================================================
DELIMITER //

CREATE PROCEDURE IF NOT EXISTS sp_marcar_contratado(
    IN p_candidato_id BIGINT UNSIGNED,
    IN p_operador_id INT
)
BEGIN
    DECLARE v_nombre VARCHAR(100);
    DECLARE v_perfil VARCHAR(50);

    SELECT CONCAT(nombre, ' ', apellido1), perfil_codigo
    INTO v_nombre, v_perfil
    FROM candidatos WHERE id = p_candidato_id;

    -- Crear portal empleado con datos minimos transferidos
    INSERT INTO portal_empleado (operador_id, candidato_id, nombre, primer_apellido, telefono, correo_electronico)
    SELECT p_operador_id, p_candidato_id, nombre, primer_apellido, telefono, correo_electronico
    FROM portal_candidato WHERE candidato_id = p_candidato_id;

    -- Crear registro firma contrato
    INSERT INTO firma_contratos (operador_id, candidato_id, estado)
    VALUES (p_operador_id, p_candidato_id, 'PENDIENTE_ALTA');

    -- ALERTA 1: Director RRHH
    INSERT INTO alertas_contratacion (
        operador_id, candidato_id, tipo_alerta, destinatario_rol, asunto, mensaje
    ) VALUES (
        p_operador_id, p_candidato_id,
        'ALERTA_1_DIRECTOR_NUEVO_CONTRATADO', 'DIRECTOR_RRHH',
        CONCAT('Nuevo contratado - ', v_nombre),
        CONCAT('Se ha contratado a ', v_nombre, '.\nPerfil: ', v_perfil,
               '\n\nPendiente completar datos del contrato:\n- Categoria\n- Horas\n- Comienzo contrato\n- Fin contrato')
    );

    -- ALERTA 2: Hermi (aviso previo)
    INSERT INTO alertas_contratacion (
        operador_id, candidato_id, tipo_alerta, destinatario_rol, asunto, mensaje
    ) VALUES (
        p_operador_id, p_candidato_id,
        'ALERTA_2_HERMI_PENDIENTE_ALTA', 'HERMI_SS',
        CONCAT('Pendiente alta SS - ', v_nombre),
        CONCAT('Nuevo contratado pendiente de alta en Seguridad Social.\nNombre: ', v_nombre,
               '\nPerfil: ', v_perfil, '\n\nPendiente recibir datos del contrato del Director RRHH.')
    );

END //

DELIMITER ;


-- =============================================================================
-- SECUENCIA 6: PROCEDIMIENTO - Director RRHH completa datos contrato
-- Categoria, Horas, Comienzo, Fin → Dispara ALERTA 3
-- =============================================================================
DELIMITER //

CREATE PROCEDURE IF NOT EXISTS sp_director_completa_contrato(
    IN p_operador_id INT,
    IN p_categoria_id INT,
    IN p_horas INT,
    IN p_fecha_inicio DATE,
    IN p_fecha_fin DATE
)
BEGIN
    DECLARE v_nombre VARCHAR(100);
    DECLARE v_dni VARCHAR(20);
    DECLARE v_telefono VARCHAR(20);
    DECLARE v_email VARCHAR(255);
    DECLARE v_candidato_id BIGINT;

    UPDATE firma_contratos
    SET categoria_profesional_id = p_categoria_id,
        horas_semana = p_horas,
        fecha_inicio = p_fecha_inicio,
        fecha_fin = p_fecha_fin
    WHERE operador_id = p_operador_id;

    SELECT fc.candidato_id, CONCAT(c.nombre, ' ', c.apellido1), c.dni, c.telefono, c.email
    INTO v_candidato_id, v_nombre, v_dni, v_telefono, v_email
    FROM firma_contratos fc
    JOIN candidatos c ON fc.candidato_id = c.id
    WHERE fc.operador_id = p_operador_id;

    -- ALERTA 3: Hermi - Datos completos
    INSERT INTO alertas_contratacion (
        operador_id, candidato_id, tipo_alerta, destinatario_rol, asunto, mensaje
    ) VALUES (
        p_operador_id, v_candidato_id,
        'ALERTA_3_HERMI_DATOS_COMPLETOS', 'HERMI_SS',
        CONCAT('ALTA SS - ', v_nombre, ' - DATOS COMPLETOS'),
        CONCAT('Ya puedes tramitar el alta en Seguridad Social.\n\n',
               'DATOS DEL TRABAJADOR:\n- Nombre: ', v_nombre,
               '\n- DNI: ', COALESCE(v_dni, 'Pendiente'),
               '\n- Telefono: ', COALESCE(v_telefono, 'Pendiente'),
               '\n- Email: ', COALESCE(v_email, 'Pendiente'),
               '\n\nDATOS DEL CONTRATO:\n- Categoria: ', p_categoria_id,
               '\n- Horas: ', p_horas, ' h/semana',
               '\n- Comienzo: ', p_fecha_inicio,
               '\n- Fin: ', COALESCE(p_fecha_fin, 'Indefinido'),
               '\n\nPor favor, confirmar cuando este tramitada el alta.')
    );

END //

DELIMITER ;


-- =============================================================================
-- SECUENCIA 7: PROCEDIMIENTO - Hermi completa alta SS
-- Tipo contrato, Codigo contrato → Dispara ALERTA 4
-- =============================================================================
DELIMITER //

CREATE PROCEDURE IF NOT EXISTS sp_hermi_completa_alta(
    IN p_operador_id INT,
    IN p_tipo_contrato VARCHAR(100),
    IN p_codigo_contrato VARCHAR(50),
    IN p_fecha_alta DATE
)
BEGIN
    DECLARE v_nombre VARCHAR(100);
    DECLARE v_candidato_id BIGINT;

    UPDATE firma_contratos
    SET tipo_contrato = p_tipo_contrato,
        codigo_contrato = p_codigo_contrato,
        alta_ss_realizada = 1,
        fecha_alta_ss = p_fecha_alta,
        estado = 'PENDIENTE_FIRMA_EMPRESA'
    WHERE operador_id = p_operador_id;

    SELECT fc.candidato_id, CONCAT(c.nombre, ' ', c.apellido1)
    INTO v_candidato_id, v_nombre
    FROM firma_contratos fc
    JOIN candidatos c ON fc.candidato_id = c.id
    WHERE fc.operador_id = p_operador_id;

    -- ALERTA 4: Director RRHH - Firma pendiente
    INSERT INTO alertas_contratacion (
        operador_id, candidato_id, tipo_alerta, destinatario_rol, asunto, mensaje
    ) VALUES (
        p_operador_id, v_candidato_id,
        'ALERTA_4_DIRECTOR_FIRMA_CONTRATO', 'DIRECTOR_RRHH',
        CONCAT('Contrato pendiente de firma - ', v_nombre),
        CONCAT('El trabajador ', v_nombre, ' ya esta dado de alta en SS.\n',
               'Tienes pendiente firmar su contrato.\n\n[Firmar contrato]')
    );

END //

DELIMITER ;


-- =============================================================================
-- SECUENCIA 8: PROCEDIMIENTO - Director RRHH firma contrato
-- Se desbloquea para el trabajador → Dispara ALERTA 5
-- =============================================================================
DELIMITER //

CREATE PROCEDURE IF NOT EXISTS sp_director_firma_contrato(
    IN p_operador_id INT,
    IN p_firmado_por VARCHAR(100)
)
BEGIN
    DECLARE v_nombre VARCHAR(100);
    DECLARE v_candidato_id BIGINT;
    DECLARE v_email VARCHAR(255);

    UPDATE firma_contratos
    SET estado = 'FIRMADO_EMPRESA',
        fecha_firma_empresa = NOW(),
        firmado_por_empresa = p_firmado_por
    WHERE operador_id = p_operador_id;

    SELECT fc.candidato_id, CONCAT(c.nombre, ' ', c.apellido1), c.email
    INTO v_candidato_id, v_nombre, v_email
    FROM firma_contratos fc
    JOIN candidatos c ON fc.candidato_id = c.id
    WHERE fc.operador_id = p_operador_id;

    -- ALERTA 5: Trabajador - Ya puede firmar
    INSERT INTO alertas_contratacion (
        operador_id, candidato_id, tipo_alerta, destinatario_rol,
        destinatario_email, asunto, mensaje
    ) VALUES (
        p_operador_id, v_candidato_id,
        'ALERTA_5_TRABAJADOR_FIRMA_CONTRATO', 'TRABAJADOR',
        v_email,
        'Tu contrato esta listo para firmar',
        CONCAT('Hola ', v_nombre, ',\n\n',
               'Tu contrato de trabajo esta listo para que lo firmes.\n',
               'Accede al portal para revisar y firmar el contrato.\n\n[Acceder al portal]')
    );

END //

DELIMITER ;


-- =============================================================================
-- SECUENCIA 9: PROCEDIMIENTO - Trabajador firma contrato
-- Contrato completado → Dispara ALERTA 6
-- =============================================================================
DELIMITER //

CREATE PROCEDURE IF NOT EXISTS sp_trabajador_firma_contrato(
    IN p_operador_id INT
)
BEGIN
    DECLARE v_nombre VARCHAR(100);
    DECLARE v_candidato_id BIGINT;
    DECLARE v_fecha_empresa DATETIME;

    SELECT fecha_firma_empresa INTO v_fecha_empresa
    FROM firma_contratos WHERE operador_id = p_operador_id;

    UPDATE firma_contratos
    SET estado = 'FIRMADO_AMBOS',
        fecha_firma_trabajador = NOW()
    WHERE operador_id = p_operador_id;

    SELECT fc.candidato_id, CONCAT(c.nombre, ' ', c.apellido1)
    INTO v_candidato_id, v_nombre
    FROM firma_contratos fc
    JOIN candidatos c ON fc.candidato_id = c.id
    WHERE fc.operador_id = p_operador_id;

    -- ALERTA 6: Confirmacion a Director RRHH
    INSERT INTO alertas_contratacion (
        operador_id, candidato_id, tipo_alerta, destinatario_rol, asunto, mensaje
    ) VALUES (
        p_operador_id, v_candidato_id,
        'ALERTA_6_CONFIRMACION_FIRMA', 'DIRECTOR_RRHH',
        CONCAT('Contrato firmado - ', v_nombre),
        CONCAT('El contrato de ', v_nombre, ' ha sido firmado por ambas partes.\n\n',
               'Fecha firma empresa: ', v_fecha_empresa, '\n',
               'Fecha firma trabajador: ', NOW(), '\nEstado: COMPLETADO')
    );

    -- ALERTA 6: Confirmacion a Hermi
    INSERT INTO alertas_contratacion (
        operador_id, candidato_id, tipo_alerta, destinatario_rol, asunto, mensaje
    ) VALUES (
        p_operador_id, v_candidato_id,
        'ALERTA_6_CONFIRMACION_FIRMA', 'HERMI_SS',
        CONCAT('Contrato firmado - ', v_nombre),
        CONCAT('El contrato de ', v_nombre, ' ha sido firmado por ambas partes.\n\n',
               'Fecha firma empresa: ', v_fecha_empresa, '\n',
               'Fecha firma trabajador: ', NOW(), '\nEstado: COMPLETADO')
    );

END //

DELIMITER ;


-- =============================================================================
-- SECUENCIA 10: FIRMAS INDEPENDIENTES DEL TRABAJADOR
-- Documentos que firma sin esperar al contrato
-- =============================================================================
CREATE TABLE IF NOT EXISTS firmas_documentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    operador_id INT NOT NULL,

    tipo_documento ENUM(
        'PROTECCION_DATOS',
        'USOS_IMAGENES',
        'FORMACION',
        'EPI',
        'INFORMACION',
        'POLITICA',
        'CONFIDENCIALIDAD',
        'BANCO',
        'MATERIAL',
        'PROTOCOLO_ACOSO'
    ) NOT NULL,

    estado ENUM('PENDIENTE', 'FIRMADO') DEFAULT 'PENDIENTE',
    fecha_firma DATETIME,
    documento_url VARCHAR(500),

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_operador (operador_id),
    INDEX idx_estado (estado),
    UNIQUE KEY uk_operador_documento (operador_id, tipo_documento)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================================================
-- SECUENCIA 11: RECONOCIMIENTOS MEDICOS (Dashboard)
-- =============================================================================
CREATE TABLE IF NOT EXISTS reconocimientos_medicos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    operador_id INT NOT NULL,

    estado ENUM('PENDIENTE', 'PROGRAMADO', 'REALIZADO', 'DESCARGADO') DEFAULT 'PENDIENTE',

    fecha_programado DATE,
    fecha_realizado DATE,
    fecha_caducidad DATE COMMENT 'fecha_realizado + 1 año',

    -- Documento descargado automaticamente por script
    documento_url VARCHAR(500),
    fecha_descarga DATETIME,
    descargado_automatico TINYINT(1) DEFAULT 0,

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_operador (operador_id),
    INDEX idx_estado (estado),
    INDEX idx_caducidad (fecha_caducidad)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================================================
-- SECUENCIA 12: CONFIGURACION DIAS AVISO CADUCIDAD
-- =============================================================================
CREATE TABLE IF NOT EXISTS config_dias_aviso (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo_documento VARCHAR(50) NOT NULL,
    dias_aviso INT NOT NULL,
    descripcion VARCHAR(200),

    UNIQUE KEY uk_documento (tipo_documento)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO config_dias_aviso (tipo_documento, dias_aviso, descripcion) VALUES
('CARNET_C', 30, 'Carnet de conducir tipo C'),
('CAP', 180, 'Certificado de Aptitud Profesional - 6 meses aviso'),
('CARNET_CARRETILLERO', 30, 'Carnet carretillero - obligatorio LOGISTICA'),
('CERTIFICADO_PUNTOS', 30, 'Certificado de puntos DGT'),
('TACOGRAFO', 28, 'Tarjeta de tacografo'),
('CARNET_MANIPULADOR', 60, 'Carnet manipulador alimentos - validez 4 años'),
('RECONOCIMIENTO_MEDICO', 30, 'Reconocimiento medico - validez 1 año')
ON DUPLICATE KEY UPDATE dias_aviso = VALUES(dias_aviso);


-- =============================================================================
-- SECUENCIA 13: ALERTAS CADUCIDAD DOCUMENTOS
-- =============================================================================
CREATE TABLE IF NOT EXISTS alertas_caducidad (
    id INT AUTO_INCREMENT PRIMARY KEY,
    operador_id INT NOT NULL,

    tipo_documento VARCHAR(50) NOT NULL,
    fecha_caducidad DATE NOT NULL,
    dias_restantes INT,

    estado ENUM('PENDIENTE', 'ENVIADA', 'RENOVADO', 'CADUCADO') DEFAULT 'PENDIENTE',
    fecha_alerta DATETIME,

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_operador (operador_id),
    INDEX idx_documento (tipo_documento),
    INDEX idx_caducidad (fecha_caducidad)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================================================
-- SECUENCIA 14: VISTAS DASHBOARD
-- =============================================================================

-- Vista: Reconocimientos medicos pendientes/caducados
CREATE OR REPLACE VIEW v_reconocimientos_medicos AS
SELECT
    o.id AS operador_id,
    CONCAT(o.Nombre, ' ', o.Apellido1) AS trabajador,
    rm.estado,
    rm.fecha_realizado AS ultimo_reconocimiento,
    rm.fecha_caducidad,
    DATEDIFF(rm.fecha_caducidad, CURDATE()) AS dias_restantes,
    CASE
        WHEN rm.estado = 'PENDIENTE' OR rm.id IS NULL THEN 'PENDIENTE'
        WHEN rm.fecha_caducidad < CURDATE() THEN 'CADUCADO'
        WHEN DATEDIFF(rm.fecha_caducidad, CURDATE()) <= 30 THEN 'PROXIMO_CADUCAR'
        ELSE 'OK'
    END AS estado_alerta
FROM operadores o
LEFT JOIN reconocimientos_medicos rm ON o.id = rm.operador_id
WHERE o.activo = 1 AND o.borrado = 0;


-- Vista: Documentos proximos a caducar
CREATE OR REPLACE VIEW v_documentos_proximos_caducar AS
SELECT
    pe.operador_id,
    CONCAT(o.Nombre, ' ', o.Apellido1) AS trabajador,
    'CARNET_C' AS tipo_documento,
    pe.carnet_c_caducidad AS fecha_caducidad,
    DATEDIFF(pe.carnet_c_caducidad, CURDATE()) AS dias_restantes
FROM portal_empleado pe
JOIN operadores o ON pe.operador_id = o.id
WHERE pe.carnet_c = 1 AND DATEDIFF(pe.carnet_c_caducidad, CURDATE()) <= 30

UNION ALL

SELECT pe.operador_id, CONCAT(o.Nombre, ' ', o.Apellido1), 'CAP',
    pe.cap_caducidad, DATEDIFF(pe.cap_caducidad, CURDATE())
FROM portal_empleado pe JOIN operadores o ON pe.operador_id = o.id
WHERE pe.cap = 1 AND DATEDIFF(pe.cap_caducidad, CURDATE()) <= 180

UNION ALL

SELECT pe.operador_id, CONCAT(o.Nombre, ' ', o.Apellido1), 'CARNET_CARRETILLERO',
    pe.carnet_carretillero_caducidad, DATEDIFF(pe.carnet_carretillero_caducidad, CURDATE())
FROM portal_empleado pe JOIN operadores o ON pe.operador_id = o.id
WHERE pe.carnet_carretillero = 1 AND DATEDIFF(pe.carnet_carretillero_caducidad, CURDATE()) <= 30

UNION ALL

SELECT pe.operador_id, CONCAT(o.Nombre, ' ', o.Apellido1), 'TACOGRAFO',
    pe.tacografo_caducidad, DATEDIFF(pe.tacografo_caducidad, CURDATE())
FROM portal_empleado pe JOIN operadores o ON pe.operador_id = o.id
WHERE pe.tacografo = 1 AND DATEDIFF(pe.tacografo_caducidad, CURDATE()) <= 28

UNION ALL

SELECT pe.operador_id, CONCAT(o.Nombre, ' ', o.Apellido1), 'CARNET_MANIPULADOR',
    pe.carnet_manipulador_caducidad, DATEDIFF(pe.carnet_manipulador_caducidad, CURDATE())
FROM portal_empleado pe JOIN operadores o ON pe.operador_id = o.id
WHERE pe.carnet_manipulador = 1 AND DATEDIFF(pe.carnet_manipulador_caducidad, CURDATE()) <= 60

ORDER BY dias_restantes ASC;


-- =============================================================================
-- SECUENCIA 15: SCRIPT DESCARGA CERTIFICADOS MEDICOS
-- Procedimiento llamado por script externo (cron)
-- =============================================================================
DELIMITER //

CREATE PROCEDURE IF NOT EXISTS sp_registrar_certificado_medico(
    IN p_operador_id INT,
    IN p_fecha_realizado DATE,
    IN p_documento_url VARCHAR(500)
)
BEGIN
    -- Actualizar reconocimiento medico
    UPDATE reconocimientos_medicos
    SET estado = 'DESCARGADO',
        fecha_realizado = p_fecha_realizado,
        fecha_caducidad = DATE_ADD(p_fecha_realizado, INTERVAL 1 YEAR),
        documento_url = p_documento_url,
        fecha_descarga = NOW(),
        descargado_automatico = 1
    WHERE operador_id = p_operador_id;

    -- Actualizar portal empleado
    UPDATE portal_empleado
    SET reconocimiento_medico = 1,
        reconocimiento_medico_fecha = p_fecha_realizado,
        reconocimiento_medico_caducidad = DATE_ADD(p_fecha_realizado, INTERVAL 1 YEAR),
        reconocimiento_medico_documento = p_documento_url
    WHERE operador_id = p_operador_id;

END //

DELIMITER ;


-- =============================================================================
-- SECUENCIA 16: ALERTAS VENCIMIENTO CONTRATOS
-- Sistema de alertas para contratos proximos a vencer
-- =============================================================================

-- Estados del contrato por vencer
ALTER TABLE firma_contratos
    ADD COLUMN IF NOT EXISTS estado_vencimiento ENUM(
        'ACTIVO',
        'PROXIMO_VENCER',
        'PENDIENTE_DECISION',
        'RENOVADO',
        'FINALIZADO',
        'NO_RENOVADO'
    ) DEFAULT 'ACTIVO',
    ADD COLUMN IF NOT EXISTS alertas_enviadas INT DEFAULT 0,
    ADD COLUMN IF NOT EXISTS ultima_alerta_enviada DATETIME,
    ADD COLUMN IF NOT EXISTS decision_renovacion ENUM('RENOVAR', 'FINALIZAR', 'MODIFICAR', 'PENDIENTE') DEFAULT 'PENDIENTE',
    ADD COLUMN IF NOT EXISTS fecha_decision DATETIME,
    ADD COLUMN IF NOT EXISTS decidido_por VARCHAR(100);


-- =============================================================================
-- SECUENCIA 17: TABLA ALERTAS VENCIMIENTO
-- =============================================================================
CREATE TABLE IF NOT EXISTS alertas_vencimiento_contratos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    operador_id INT NOT NULL,
    contrato_id INT NOT NULL,

    -- Datos del contrato
    fecha_fin_contrato DATE NOT NULL,
    dias_restantes INT NOT NULL,

    -- Alerta
    tipo_alerta ENUM(
        'AVISO_15_DIAS',
        'RECORDATORIO_RECURRENTE',
        'ULTIMO_DIA',
        'CONTRATO_VENCIDO'
    ) NOT NULL,

    destinatario_rol ENUM('DIRECTOR_RRHH', 'HERMI_SS') NOT NULL,
    destinatario_email VARCHAR(255),

    asunto VARCHAR(255),
    mensaje TEXT,

    -- Estado
    estado ENUM('PENDIENTE', 'ENVIADA', 'RESUELTA') DEFAULT 'PENDIENTE',
    fecha_envio DATETIME,
    resuelto TINYINT(1) DEFAULT 0,
    fecha_resolucion DATETIME,

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_operador (operador_id),
    INDEX idx_contrato (contrato_id),
    INDEX idx_fecha_fin (fecha_fin_contrato),
    INDEX idx_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================================================
-- SECUENCIA 18: CONFIGURACION ALERTAS POR ROL
-- =============================================================================
CREATE TABLE IF NOT EXISTS config_alertas_rol (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rol ENUM('DIRECTOR_RRHH', 'HERMI_SS', 'TRABAJADOR', 'PREVENCION') NOT NULL,
    tipo_alerta VARCHAR(50) NOT NULL,
    canal ENUM('DASHBOARD', 'EMAIL', 'SMS', 'LLAMADA') NOT NULL,
    frecuencia ENUM('INMEDIATA', 'DIARIA', 'CADA_2_DIAS', 'SEMANAL') NOT NULL,
    activo TINYINT(1) DEFAULT 1,
    email_destino VARCHAR(255),
    telefono_destino VARCHAR(20),

    UNIQUE KEY uk_rol_alerta_canal (rol, tipo_alerta, canal),
    INDEX idx_rol (rol),
    INDEX idx_tipo (tipo_alerta)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Configuracion por defecto
INSERT INTO config_alertas_rol (rol, tipo_alerta, canal, frecuencia) VALUES
-- Director RRHH
('DIRECTOR_RRHH', 'VENCIMIENTO_CONTRATO', 'DASHBOARD', 'INMEDIATA'),
('DIRECTOR_RRHH', 'NUEVO_CONTRATADO', 'DASHBOARD', 'INMEDIATA'),
('DIRECTOR_RRHH', 'NUEVO_CONTRATADO', 'EMAIL', 'INMEDIATA'),
('DIRECTOR_RRHH', 'FIRMA_CONTRATO', 'DASHBOARD', 'INMEDIATA'),
-- Hermi SS
('HERMI_SS', 'VENCIMIENTO_CONTRATO', 'EMAIL', 'CADA_2_DIAS'),
('HERMI_SS', 'PENDIENTE_ALTA', 'EMAIL', 'INMEDIATA'),
('HERMI_SS', 'DATOS_COMPLETOS', 'EMAIL', 'INMEDIATA'),
-- Trabajador
('TRABAJADOR', 'FIRMA_CONTRATO', 'EMAIL', 'INMEDIATA'),
('TRABAJADOR', 'DOCUMENTOS_PENDIENTES', 'EMAIL', 'SEMANAL')
ON DUPLICATE KEY UPDATE frecuencia = VALUES(frecuencia);


-- =============================================================================
-- SECUENCIA 19: VISTA CONTRATOS PROXIMOS A VENCER
-- =============================================================================
CREATE OR REPLACE VIEW v_contratos_proximos_vencer AS
SELECT
    fc.id AS contrato_id,
    fc.operador_id,
    CONCAT(o.Nombre, ' ', o.Apellido1) AS trabajador,
    fc.tipo_contrato,
    fc.fecha_inicio,
    fc.fecha_fin,
    DATEDIFF(fc.fecha_fin, CURDATE()) AS dias_restantes,
    fc.categoria_profesional_id,
    fc.horas_semana,
    fc.estado_vencimiento,
    fc.decision_renovacion,
    fc.alertas_enviadas,
    CASE
        WHEN DATEDIFF(fc.fecha_fin, CURDATE()) < 0 THEN 'VENCIDO'
        WHEN DATEDIFF(fc.fecha_fin, CURDATE()) <= 1 THEN 'ULTIMO_DIA'
        WHEN DATEDIFF(fc.fecha_fin, CURDATE()) <= 15 THEN 'URGENTE'
        WHEN DATEDIFF(fc.fecha_fin, CURDATE()) <= 30 THEN 'PROXIMO'
        ELSE 'OK'
    END AS estado_alerta
FROM firma_contratos fc
JOIN operadores o ON fc.operador_id = o.id
WHERE fc.fecha_fin IS NOT NULL
AND fc.estado = 'FIRMADO_AMBOS'
AND fc.estado_vencimiento NOT IN ('RENOVADO', 'FINALIZADO')
ORDER BY dias_restantes ASC;


-- =============================================================================
-- SECUENCIA 20: PROCEDIMIENTO - Generar alertas vencimiento
-- (Ejecutar diariamente via cron)
-- =============================================================================
DELIMITER //

CREATE PROCEDURE IF NOT EXISTS sp_generar_alertas_vencimiento()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_operador_id INT;
    DECLARE v_contrato_id INT;
    DECLARE v_nombre VARCHAR(100);
    DECLARE v_fecha_fin DATE;
    DECLARE v_dias_restantes INT;
    DECLARE v_tipo_contrato VARCHAR(100);
    DECLARE v_categoria INT;
    DECLARE v_horas INT;
    DECLARE v_ultima_alerta DATETIME;
    DECLARE v_alertas_enviadas INT;

    -- Cursor para contratos que vencen en 15 dias o menos
    DECLARE cur_contratos CURSOR FOR
        SELECT
            fc.operador_id,
            fc.id,
            CONCAT(o.Nombre, ' ', o.Apellido1),
            fc.fecha_fin,
            DATEDIFF(fc.fecha_fin, CURDATE()),
            fc.tipo_contrato,
            fc.categoria_profesional_id,
            fc.horas_semana,
            fc.ultima_alerta_enviada,
            fc.alertas_enviadas
        FROM firma_contratos fc
        JOIN operadores o ON fc.operador_id = o.id
        WHERE fc.fecha_fin IS NOT NULL
        AND fc.estado = 'FIRMADO_AMBOS'
        AND fc.estado_vencimiento NOT IN ('RENOVADO', 'FINALIZADO')
        AND DATEDIFF(fc.fecha_fin, CURDATE()) <= 15
        AND DATEDIFF(fc.fecha_fin, CURDATE()) >= 0;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur_contratos;

    read_loop: LOOP
        FETCH cur_contratos INTO v_operador_id, v_contrato_id, v_nombre, v_fecha_fin,
            v_dias_restantes, v_tipo_contrato, v_categoria, v_horas,
            v_ultima_alerta, v_alertas_enviadas;

        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Verificar si han pasado 2 dias desde la ultima alerta (para Hermi)
        IF v_ultima_alerta IS NULL OR DATEDIFF(NOW(), v_ultima_alerta) >= 2 THEN

            -- Actualizar estado del contrato
            UPDATE firma_contratos
            SET estado_vencimiento = 'PROXIMO_VENCER',
                alertas_enviadas = alertas_enviadas + 1,
                ultima_alerta_enviada = NOW()
            WHERE id = v_contrato_id;

            -- Alerta para Dashboard Director RRHH
            INSERT INTO alertas_vencimiento_contratos (
                operador_id, contrato_id, fecha_fin_contrato, dias_restantes,
                tipo_alerta, destinatario_rol, asunto, mensaje, estado
            ) VALUES (
                v_operador_id, v_contrato_id, v_fecha_fin, v_dias_restantes,
                CASE
                    WHEN v_dias_restantes <= 1 THEN 'ULTIMO_DIA'
                    ELSE 'RECORDATORIO_RECURRENTE'
                END,
                'DIRECTOR_RRHH',
                CONCAT(
                    CASE WHEN v_dias_restantes <= 1 THEN '[MUY URGENTE] ' ELSE '[URGENTE] ' END,
                    'Contrato expira - ', v_nombre, ' - ', v_fecha_fin
                ),
                CONCAT(
                    'El contrato de ', v_nombre, ' expira el ', v_fecha_fin, '.\n',
                    'Quedan ', v_dias_restantes, ' dias para la finalizacion.\n\n',
                    'DATOS DEL TRABAJADOR:\n',
                    '- Nombre: ', v_nombre, '\n',
                    '- Tipo contrato: ', COALESCE(v_tipo_contrato, 'N/A'), '\n',
                    '- Categoria: ', COALESCE(v_categoria, 'N/A'), '\n',
                    '- Horas: ', COALESCE(v_horas, 'N/A'), ' h/semana'
                ),
                'PENDIENTE'
            );

            -- Alerta EMAIL para Hermi (cada 2 dias)
            INSERT INTO alertas_vencimiento_contratos (
                operador_id, contrato_id, fecha_fin_contrato, dias_restantes,
                tipo_alerta, destinatario_rol, asunto, mensaje, estado
            ) VALUES (
                v_operador_id, v_contrato_id, v_fecha_fin, v_dias_restantes,
                CASE
                    WHEN v_dias_restantes <= 1 THEN 'ULTIMO_DIA'
                    ELSE 'RECORDATORIO_RECURRENTE'
                END,
                'HERMI_SS',
                CONCAT(
                    CASE WHEN v_dias_restantes <= 1 THEN '[MUY URGENTE] ' ELSE '[URGENTE] ' END,
                    'Contrato expira - ', v_nombre, ' - ', v_fecha_fin
                ),
                CONCAT(
                    'El contrato de ', v_nombre, ' expira el ', v_fecha_fin, '.\n',
                    'Quedan ', v_dias_restantes, ' dias para la finalizacion.\n\n',
                    'DATOS DEL TRABAJADOR:\n',
                    '- Nombre: ', v_nombre, '\n',
                    '- Tipo contrato: ', COALESCE(v_tipo_contrato, 'N/A'), '\n',
                    '- Categoria: ', COALESCE(v_categoria, 'N/A'), '\n',
                    '- Horas: ', COALESCE(v_horas, 'N/A'), ' h/semana\n\n',
                    'ACCIONES PENDIENTES:\n',
                    '[ ] Decidir renovacion o finalizacion\n',
                    '[ ] Si renovacion: preparar nuevo contrato\n',
                    '[ ] Si finalizacion: preparar baja SS\n\n',
                    'Este email se enviara cada 2 dias hasta que se resuelva.'
                ),
                'PENDIENTE'
            );

        END IF;

    END LOOP;

    CLOSE cur_contratos;

END //

DELIMITER ;


-- =============================================================================
-- SECUENCIA 21: PROCEDIMIENTO - Resolver vencimiento (renovar/finalizar)
-- =============================================================================
DELIMITER //

CREATE PROCEDURE IF NOT EXISTS sp_resolver_vencimiento(
    IN p_contrato_id INT,
    IN p_decision ENUM('RENOVAR', 'FINALIZAR', 'MODIFICAR'),
    IN p_decidido_por VARCHAR(100)
)
BEGIN
    DECLARE v_operador_id INT;
    DECLARE v_nombre VARCHAR(100);

    -- Obtener datos
    SELECT fc.operador_id, CONCAT(o.Nombre, ' ', o.Apellido1)
    INTO v_operador_id, v_nombre
    FROM firma_contratos fc
    JOIN operadores o ON fc.operador_id = o.id
    WHERE fc.id = p_contrato_id;

    -- Actualizar estado segun decision
    UPDATE firma_contratos
    SET estado_vencimiento = CASE
            WHEN p_decision = 'RENOVAR' THEN 'RENOVADO'
            WHEN p_decision = 'FINALIZAR' THEN 'NO_RENOVADO'
            WHEN p_decision = 'MODIFICAR' THEN 'PENDIENTE_DECISION'
        END,
        decision_renovacion = p_decision,
        fecha_decision = NOW(),
        decidido_por = p_decidido_por
    WHERE id = p_contrato_id;

    -- Marcar alertas como resueltas
    UPDATE alertas_vencimiento_contratos
    SET resuelto = 1,
        fecha_resolucion = NOW(),
        estado = 'RESUELTA'
    WHERE contrato_id = p_contrato_id
    AND resuelto = 0;

    -- Si es RENOVAR, crear nuevo registro de contrato (pendiente datos)
    IF p_decision = 'RENOVAR' THEN
        INSERT INTO firma_contratos (operador_id, candidato_id, estado)
        SELECT operador_id, candidato_id, 'PENDIENTE_ALTA'
        FROM firma_contratos WHERE id = p_contrato_id;
    END IF;

    -- Si es FINALIZAR, notificar a Hermi para baja SS
    IF p_decision = 'FINALIZAR' THEN
        INSERT INTO alertas_contratacion (
            operador_id, tipo_alerta, destinatario_rol, asunto, mensaje
        ) VALUES (
            v_operador_id,
            'ALERTA_3_HERMI_DATOS_COMPLETOS',
            'HERMI_SS',
            CONCAT('Baja SS pendiente - ', v_nombre),
            CONCAT('El contrato de ', v_nombre, ' NO sera renovado.\n',
                   'Por favor, tramitar la baja en Seguridad Social.\n\n',
                   'Decision tomada por: ', p_decidido_por)
        );
    END IF;

END //

DELIMITER ;


-- =============================================================================
-- SECUENCIA 22: VISTA DASHBOARD VENCIMIENTOS
-- =============================================================================
CREATE OR REPLACE VIEW v_dashboard_vencimientos AS
SELECT
    'URGENTE' AS prioridad,
    contrato_id,
    operador_id,
    trabajador,
    tipo_contrato,
    fecha_fin,
    dias_restantes,
    estado_vencimiento,
    decision_renovacion
FROM v_contratos_proximos_vencer
WHERE dias_restantes <= 15
AND dias_restantes >= 0

UNION ALL

SELECT
    'PROXIMO' AS prioridad,
    contrato_id,
    operador_id,
    trabajador,
    tipo_contrato,
    fecha_fin,
    dias_restantes,
    estado_vencimiento,
    decision_renovacion
FROM v_contratos_proximos_vencer
WHERE dias_restantes > 15
AND dias_restantes <= 30

ORDER BY dias_restantes ASC;


-- =============================================================================
-- SECUENCIA 23: HISTORIAL DE CONTRATOS (lineas)
-- Cada modificacion genera nueva linea
-- =============================================================================
CREATE TABLE IF NOT EXISTS contratos_historial (
    id INT AUTO_INCREMENT PRIMARY KEY,
    operador_id INT NOT NULL,
    numero_linea INT NOT NULL COMMENT 'Numero secuencial de linea para este trabajador',

    -- Condiciones del contrato
    tipo_contrato VARCHAR(100),
    codigo_contrato VARCHAR(50),
    categoria_profesional_id INT,
    horas_semana INT,
    fecha_desde DATE NOT NULL,
    fecha_hasta DATE COMMENT 'NULL si indefinido o activo',

    -- Estado de la linea
    estado ENUM('ACTIVO', 'CERRADO', 'PENDIENTE_FIRMA') DEFAULT 'PENDIENTE_FIRMA',

    -- Motivo del cambio (si es linea posterior a la primera)
    motivo_cambio ENUM('NUEVO_CONTRATO', 'CAMBIO_CATEGORIA', 'CAMBIO_JORNADA', 'CAMBIO_AMBOS', 'RENOVACION') DEFAULT 'NUEVO_CONTRATO',
    descripcion_cambio TEXT,

    -- Documento anexo
    documento_url VARCHAR(500),
    documento_subido_por VARCHAR(100) COMMENT 'Hermi',
    fecha_subida_documento DATETIME,

    -- Firmas
    firmado_empresa TINYINT(1) DEFAULT 0,
    fecha_firma_empresa DATETIME,
    firmado_por_empresa VARCHAR(100),
    firmado_trabajador TINYINT(1) DEFAULT 0,
    fecha_firma_trabajador DATETIME,

    -- Referencia a linea anterior (si es modificacion)
    linea_anterior_id INT,

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_operador (operador_id),
    INDEX idx_estado (estado),
    INDEX idx_fecha (fecha_desde),
    UNIQUE KEY uk_operador_linea (operador_id, numero_linea)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================================================
-- SECUENCIA 24: ALERTAS MODIFICACION CONDICIONES
-- =============================================================================
CREATE TABLE IF NOT EXISTS alertas_modificacion_contrato (
    id INT AUTO_INCREMENT PRIMARY KEY,
    operador_id INT NOT NULL,
    contrato_historial_id INT NOT NULL,

    tipo_alerta ENUM(
        'HERMI_SUBIR_DOCUMENTO',
        'DIRECTOR_FIRMAR_ANEXO',
        'TRABAJADOR_FIRMAR_ANEXO',
        'CONFIRMACION_COMPLETADO'
    ) NOT NULL,

    destinatario_rol ENUM('DIRECTOR_RRHH', 'HERMI_SS', 'TRABAJADOR') NOT NULL,
    destinatario_email VARCHAR(255),

    -- Detalle del cambio
    campo_modificado ENUM('CATEGORIA', 'JORNADA', 'AMBOS') NOT NULL,
    valor_anterior VARCHAR(100),
    valor_nuevo VARCHAR(100),

    asunto VARCHAR(255),
    mensaje TEXT,

    estado ENUM('PENDIENTE', 'ENVIADA', 'COMPLETADA') DEFAULT 'PENDIENTE',
    fecha_envio DATETIME,

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_operador (operador_id),
    INDEX idx_contrato (contrato_historial_id),
    INDEX idx_tipo (tipo_alerta),
    INDEX idx_estado (estado),
    FOREIGN KEY (contrato_historial_id) REFERENCES contratos_historial(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================================================
-- SECUENCIA 25: PROCEDIMIENTO - Modificar condiciones contrato
-- Genera nueva linea y alertas
-- =============================================================================
DELIMITER //

CREATE PROCEDURE IF NOT EXISTS sp_modificar_condiciones_contrato(
    IN p_operador_id INT,
    IN p_nueva_categoria INT,
    IN p_nuevas_horas INT,
    IN p_fecha_desde DATE,
    IN p_modificado_por VARCHAR(100)
)
BEGIN
    DECLARE v_nombre VARCHAR(100);
    DECLARE v_email VARCHAR(255);
    DECLARE v_categoria_anterior INT;
    DECLARE v_horas_anterior INT;
    DECLARE v_nueva_linea INT;
    DECLARE v_linea_anterior_id INT;
    DECLARE v_campo_modificado VARCHAR(20);
    DECLARE v_nuevo_contrato_id INT;

    -- Obtener datos actuales
    SELECT
        CONCAT(o.Nombre, ' ', o.Apellido1),
        o.email,
        ch.categoria_profesional_id,
        ch.horas_semana,
        ch.id
    INTO v_nombre, v_email, v_categoria_anterior, v_horas_anterior, v_linea_anterior_id
    FROM operadores o
    LEFT JOIN contratos_historial ch ON o.id = ch.operador_id AND ch.estado = 'ACTIVO'
    WHERE o.id = p_operador_id
    LIMIT 1;

    -- Determinar que campo se modifico
    IF p_nueva_categoria != v_categoria_anterior AND p_nuevas_horas != v_horas_anterior THEN
        SET v_campo_modificado = 'AMBOS';
    ELSEIF p_nueva_categoria != v_categoria_anterior THEN
        SET v_campo_modificado = 'CATEGORIA';
    ELSE
        SET v_campo_modificado = 'JORNADA';
    END IF;

    -- Cerrar linea anterior
    UPDATE contratos_historial
    SET estado = 'CERRADO',
        fecha_hasta = DATE_SUB(p_fecha_desde, INTERVAL 1 DAY)
    WHERE operador_id = p_operador_id AND estado = 'ACTIVO';

    -- Obtener numero de nueva linea
    SELECT COALESCE(MAX(numero_linea), 0) + 1
    INTO v_nueva_linea
    FROM contratos_historial
    WHERE operador_id = p_operador_id;

    -- Crear nueva linea
    INSERT INTO contratos_historial (
        operador_id, numero_linea, categoria_profesional_id, horas_semana,
        fecha_desde, estado, motivo_cambio, descripcion_cambio, linea_anterior_id
    ) VALUES (
        p_operador_id, v_nueva_linea, p_nueva_categoria, p_nuevas_horas,
        p_fecha_desde, 'PENDIENTE_FIRMA',
        CASE v_campo_modificado
            WHEN 'AMBOS' THEN 'CAMBIO_AMBOS'
            WHEN 'CATEGORIA' THEN 'CAMBIO_CATEGORIA'
            ELSE 'CAMBIO_JORNADA'
        END,
        CONCAT('Categoria: ', COALESCE(v_categoria_anterior, 'N/A'), ' → ', p_nueva_categoria,
               ' | Horas: ', COALESCE(v_horas_anterior, 'N/A'), ' → ', p_nuevas_horas),
        v_linea_anterior_id
    );

    SET v_nuevo_contrato_id = LAST_INSERT_ID();

    -- ALERTA 1: Hermi - Subir documento
    INSERT INTO alertas_modificacion_contrato (
        operador_id, contrato_historial_id, tipo_alerta, destinatario_rol,
        campo_modificado, valor_anterior, valor_nuevo, asunto, mensaje
    ) VALUES (
        p_operador_id, v_nuevo_contrato_id,
        'HERMI_SUBIR_DOCUMENTO', 'HERMI_SS',
        v_campo_modificado,
        CASE v_campo_modificado
            WHEN 'CATEGORIA' THEN v_categoria_anterior
            WHEN 'JORNADA' THEN v_horas_anterior
            ELSE CONCAT(v_categoria_anterior, '/', v_horas_anterior)
        END,
        CASE v_campo_modificado
            WHEN 'CATEGORIA' THEN p_nueva_categoria
            WHEN 'JORNADA' THEN p_nuevas_horas
            ELSE CONCAT(p_nueva_categoria, '/', p_nuevas_horas)
        END,
        CONCAT('Modificacion condiciones - ', v_nombre),
        CONCAT('Se ha modificado las condiciones del contrato de ', v_nombre, '.\n\n',
               'CAMBIOS:\n',
               CASE
                   WHEN v_campo_modificado = 'CATEGORIA' THEN CONCAT('- Categoria: ', v_categoria_anterior, ' → ', p_nueva_categoria)
                   WHEN v_campo_modificado = 'JORNADA' THEN CONCAT('- Jornada: ', v_horas_anterior, 'h → ', p_nuevas_horas, 'h')
                   ELSE CONCAT('- Categoria: ', v_categoria_anterior, ' → ', p_nueva_categoria, '\n- Jornada: ', v_horas_anterior, 'h → ', p_nuevas_horas, 'h')
               END,
               '\n\nACCIONES:\n[ ] Preparar anexo de modificacion\n[ ] Subir documento al sistema')
    );

END //

DELIMITER ;


-- =============================================================================
-- SECUENCIA 26: PROCEDIMIENTO - Hermi sube documento anexo
-- =============================================================================
DELIMITER //

CREATE PROCEDURE IF NOT EXISTS sp_subir_documento_anexo(
    IN p_contrato_historial_id INT,
    IN p_documento_url VARCHAR(500),
    IN p_subido_por VARCHAR(100)
)
BEGIN
    DECLARE v_operador_id INT;
    DECLARE v_nombre VARCHAR(100);
    DECLARE v_cambio TEXT;

    -- Actualizar contrato
    UPDATE contratos_historial
    SET documento_url = p_documento_url,
        documento_subido_por = p_subido_por,
        fecha_subida_documento = NOW()
    WHERE id = p_contrato_historial_id;

    -- Obtener datos
    SELECT ch.operador_id, CONCAT(o.Nombre, ' ', o.Apellido1), ch.descripcion_cambio
    INTO v_operador_id, v_nombre, v_cambio
    FROM contratos_historial ch
    JOIN operadores o ON ch.operador_id = o.id
    WHERE ch.id = p_contrato_historial_id;

    -- Marcar alerta anterior como completada
    UPDATE alertas_modificacion_contrato
    SET estado = 'COMPLETADA'
    WHERE contrato_historial_id = p_contrato_historial_id
    AND tipo_alerta = 'HERMI_SUBIR_DOCUMENTO';

    -- ALERTA 2: Director RRHH - Firmar anexo
    INSERT INTO alertas_modificacion_contrato (
        operador_id, contrato_historial_id, tipo_alerta, destinatario_rol,
        campo_modificado, asunto, mensaje
    )
    SELECT
        v_operador_id, p_contrato_historial_id,
        'DIRECTOR_FIRMAR_ANEXO', 'DIRECTOR_RRHH',
        campo_modificado,
        CONCAT('Anexo pendiente de firma - ', v_nombre),
        CONCAT('Hermi ha subido el anexo de modificacion de ', v_nombre, '.\n',
               'Tienes pendiente firmar el documento.\n\n',
               'CAMBIOS:\n', v_cambio, '\n\n[Firmar anexo]')
    FROM alertas_modificacion_contrato
    WHERE contrato_historial_id = p_contrato_historial_id
    LIMIT 1;

END //

DELIMITER ;


-- =============================================================================
-- SECUENCIA 27: PROCEDIMIENTO - Director firma anexo
-- =============================================================================
DELIMITER //

CREATE PROCEDURE IF NOT EXISTS sp_director_firma_anexo(
    IN p_contrato_historial_id INT,
    IN p_firmado_por VARCHAR(100)
)
BEGIN
    DECLARE v_operador_id INT;
    DECLARE v_nombre VARCHAR(100);
    DECLARE v_email VARCHAR(255);
    DECLARE v_cambio TEXT;

    -- Actualizar contrato
    UPDATE contratos_historial
    SET firmado_empresa = 1,
        fecha_firma_empresa = NOW(),
        firmado_por_empresa = p_firmado_por
    WHERE id = p_contrato_historial_id;

    -- Obtener datos
    SELECT ch.operador_id, CONCAT(o.Nombre, ' ', o.Apellido1), o.email, ch.descripcion_cambio
    INTO v_operador_id, v_nombre, v_email, v_cambio
    FROM contratos_historial ch
    JOIN operadores o ON ch.operador_id = o.id
    WHERE ch.id = p_contrato_historial_id;

    -- Marcar alerta anterior como completada
    UPDATE alertas_modificacion_contrato
    SET estado = 'COMPLETADA'
    WHERE contrato_historial_id = p_contrato_historial_id
    AND tipo_alerta = 'DIRECTOR_FIRMAR_ANEXO';

    -- ALERTA 3: Trabajador - Firmar anexo
    INSERT INTO alertas_modificacion_contrato (
        operador_id, contrato_historial_id, tipo_alerta, destinatario_rol,
        destinatario_email, campo_modificado, asunto, mensaje
    )
    SELECT
        v_operador_id, p_contrato_historial_id,
        'TRABAJADOR_FIRMAR_ANEXO', 'TRABAJADOR',
        v_email, campo_modificado,
        'Tienes un anexo pendiente de firmar',
        CONCAT('Hola ', v_nombre, ',\n\n',
               'Se han modificado las condiciones de tu contrato.\n',
               'Accede al portal para revisar y firmar el anexo.\n\n',
               'CAMBIOS:\n', v_cambio, '\n\n[Acceder al portal]')
    FROM alertas_modificacion_contrato
    WHERE contrato_historial_id = p_contrato_historial_id
    LIMIT 1;

END //

DELIMITER ;


-- =============================================================================
-- SECUENCIA 28: PROCEDIMIENTO - Trabajador firma anexo
-- =============================================================================
DELIMITER //

CREATE PROCEDURE IF NOT EXISTS sp_trabajador_firma_anexo(
    IN p_contrato_historial_id INT
)
BEGIN
    DECLARE v_operador_id INT;
    DECLARE v_nombre VARCHAR(100);
    DECLARE v_cambio TEXT;

    -- Actualizar contrato
    UPDATE contratos_historial
    SET firmado_trabajador = 1,
        fecha_firma_trabajador = NOW(),
        estado = 'ACTIVO'
    WHERE id = p_contrato_historial_id;

    -- Obtener datos
    SELECT ch.operador_id, CONCAT(o.Nombre, ' ', o.Apellido1), ch.descripcion_cambio
    INTO v_operador_id, v_nombre, v_cambio
    FROM contratos_historial ch
    JOIN operadores o ON ch.operador_id = o.id
    WHERE ch.id = p_contrato_historial_id;

    -- Marcar alerta anterior como completada
    UPDATE alertas_modificacion_contrato
    SET estado = 'COMPLETADA'
    WHERE contrato_historial_id = p_contrato_historial_id
    AND tipo_alerta = 'TRABAJADOR_FIRMAR_ANEXO';

    -- ALERTA 4: Confirmacion a Director RRHH y Hermi
    INSERT INTO alertas_modificacion_contrato (
        operador_id, contrato_historial_id, tipo_alerta, destinatario_rol,
        campo_modificado, asunto, mensaje
    )
    SELECT
        v_operador_id, p_contrato_historial_id,
        'CONFIRMACION_COMPLETADO', 'DIRECTOR_RRHH',
        campo_modificado,
        CONCAT('Anexo firmado - ', v_nombre),
        CONCAT('El anexo de ', v_nombre, ' ha sido firmado por ambas partes.\n\n',
               'CAMBIOS APLICADOS:\n', v_cambio, '\n\nEstado: COMPLETADO')
    FROM alertas_modificacion_contrato
    WHERE contrato_historial_id = p_contrato_historial_id
    LIMIT 1;

    INSERT INTO alertas_modificacion_contrato (
        operador_id, contrato_historial_id, tipo_alerta, destinatario_rol,
        campo_modificado, asunto, mensaje
    )
    SELECT
        v_operador_id, p_contrato_historial_id,
        'CONFIRMACION_COMPLETADO', 'HERMI_SS',
        campo_modificado,
        CONCAT('Anexo firmado - ', v_nombre),
        CONCAT('El anexo de ', v_nombre, ' ha sido firmado por ambas partes.\n\n',
               'CAMBIOS APLICADOS:\n', v_cambio, '\n\nEstado: COMPLETADO')
    FROM alertas_modificacion_contrato
    WHERE contrato_historial_id = p_contrato_historial_id
    LIMIT 1;

END //

DELIMITER ;


-- =============================================================================
-- SECUENCIA 29: VISTA HISTORIAL CONTRATOS TRABAJADOR
-- =============================================================================
CREATE OR REPLACE VIEW v_historial_contratos AS
SELECT
    ch.operador_id,
    CONCAT(o.Nombre, ' ', o.Apellido1) AS trabajador,
    ch.numero_linea,
    ch.tipo_contrato,
    ch.categoria_profesional_id AS categoria,
    ch.horas_semana AS horas,
    ch.fecha_desde,
    ch.fecha_hasta,
    ch.estado,
    ch.motivo_cambio,
    ch.descripcion_cambio,
    ch.firmado_empresa,
    ch.firmado_trabajador
FROM contratos_historial ch
JOIN operadores o ON ch.operador_id = o.id
ORDER BY ch.operador_id, ch.numero_linea;


-- =============================================================================
-- FIN DEL SCHEMA
-- =============================================================================

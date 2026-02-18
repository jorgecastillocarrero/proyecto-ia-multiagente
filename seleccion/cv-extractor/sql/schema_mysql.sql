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
-- FIN DEL SCHEMA
-- =============================================================================

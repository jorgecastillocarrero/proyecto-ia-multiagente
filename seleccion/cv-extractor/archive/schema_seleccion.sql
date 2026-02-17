-- ============================================================================
-- SCHEMA DE SELECCIÓN DE PERSONAL
-- Sistema de gestión del proceso de selección RRHH
-- ============================================================================

-- -----------------------------------------------------------------------------
-- TABLA: USUARIOS DEL SISTEMA
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    rol VARCHAR(50) NOT NULL, -- 'admin', 'revisor', 'llamador', 'entrevistador'
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- TABLA: PUESTOS DE TRABAJO
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS puestos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(300) NOT NULL,
    descripcion TEXT,
    palabras_clave TEXT[], -- Para matching con puesto_deseado
    distancia_maxima_km INTEGER DEFAULT 40,
    experiencia_minima_anos NUMERIC(4,2) DEFAULT 1.0,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_cierre TIMESTAMP,
    creado_por INTEGER REFERENCES usuarios(id)
);

-- -----------------------------------------------------------------------------
-- TABLA: MOTIVOS DE DESCARTE
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS motivos_descarte (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    descripcion VARCHAR(300) NOT NULL,
    automatico BOOLEAN DEFAULT FALSE, -- TRUE si es descarte automático del sistema
    activo BOOLEAN DEFAULT TRUE
);

-- Insertar motivos de descarte predefinidos
INSERT INTO motivos_descarte (codigo, descripcion, automatico) VALUES
    ('DESCARTADO_PREVIO', 'Descartado previamente en otro puesto', TRUE),
    ('DISTANCIA_EXCEDIDA', 'Vive a más de 40 km de Córdoba', TRUE),
    ('SIN_EXPERIENCIA', 'Sin experiencia o menos de 1 año', TRUE),
    ('PUESTO_NO_RELACIONADO', 'Puesto deseado no relacionado con el puesto', TRUE),
    ('NO_SELECCIONADO', 'No seleccionado por el revisor', FALSE),
    ('NO_INTERESADO', 'Candidato no interesado en el puesto', FALSE),
    ('NO_CONTACTADO', 'No se ha conseguido contactar', FALSE),
    ('DESCARTADO_ENTREVISTA', 'Descartado tras la entrevista', FALSE)
ON CONFLICT (codigo) DO NOTHING;

-- -----------------------------------------------------------------------------
-- TABLA: CANDIDATOS EN PUESTOS (relación candidato-puesto)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS candidatos_puestos (
    id SERIAL PRIMARY KEY,
    candidato_id INTEGER NOT NULL REFERENCES candidatos(id) ON DELETE CASCADE,
    puesto_id INTEGER NOT NULL REFERENCES puestos(id) ON DELETE CASCADE,

    -- Estado del candidato en este puesto
    estado VARCHAR(50) NOT NULL DEFAULT 'nuevo',
    -- Estados: 'nuevo', 'descartado_auto', 'primera_criba', 'descartado_manual',
    --          'seleccionado_llamar', 'llamando', 'entrevista_programada',
    --          'entrevistado', 'seleccionado_final', 'contratado'

    -- Descarte
    descartado BOOLEAN DEFAULT FALSE,
    motivo_descarte_id INTEGER REFERENCES motivos_descarte(id),
    descartado_por INTEGER REFERENCES usuarios(id),
    fecha_descarte TIMESTAMP,
    notas_descarte TEXT,

    -- Selección
    seleccionado_por INTEGER REFERENCES usuarios(id),
    fecha_seleccion TIMESTAMP,

    -- Metadatos
    fecha_entrada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uk_candidato_puesto UNIQUE (candidato_id, puesto_id)
);

CREATE INDEX idx_cand_puesto_estado ON candidatos_puestos(estado);
CREATE INDEX idx_cand_puesto_descartado ON candidatos_puestos(descartado);

-- -----------------------------------------------------------------------------
-- TABLA: LLAMADAS / INTENTOS DE CONTACTO
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS llamadas (
    id SERIAL PRIMARY KEY,
    candidato_puesto_id INTEGER NOT NULL REFERENCES candidatos_puestos(id) ON DELETE CASCADE,

    realizada_por INTEGER REFERENCES usuarios(id),
    fecha_llamada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Resultado
    contestado BOOLEAN DEFAULT FALSE,
    resultado VARCHAR(50), -- 'acepta_entrevista', 'no_interesado', 'no_contesta', 'llamar_despues'

    -- Si acepta entrevista
    fecha_entrevista_propuesta DATE,
    hora_entrevista_propuesta TIME,

    notas TEXT
);

CREATE INDEX idx_llamadas_cand_puesto ON llamadas(candidato_puesto_id);

-- -----------------------------------------------------------------------------
-- TABLA: ENTREVISTAS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS entrevistas (
    id SERIAL PRIMARY KEY,
    candidato_puesto_id INTEGER NOT NULL REFERENCES candidatos_puestos(id) ON DELETE CASCADE,

    fecha DATE NOT NULL,
    hora TIME NOT NULL,

    entrevistador_id INTEGER REFERENCES usuarios(id),

    -- Estado
    estado VARCHAR(50) DEFAULT 'programada', -- 'programada', 'realizada', 'no_asistio', 'cancelada'

    -- Resultado (tras la entrevista)
    resultado VARCHAR(50), -- 'seleccionado', 'descartado', 'pendiente'
    puntuacion INTEGER, -- 1-10
    notas TEXT,

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_entrevistas_fecha ON entrevistas(fecha, hora);
CREATE INDEX idx_entrevistas_entrevistador ON entrevistas(entrevistador_id);

-- -----------------------------------------------------------------------------
-- TABLA: CONFIGURACIÓN DEL SISTEMA
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS configuracion (
    clave VARCHAR(100) PRIMARY KEY,
    valor TEXT NOT NULL,
    descripcion VARCHAR(300)
);

INSERT INTO configuracion (clave, valor, descripcion) VALUES
    ('intentos_llamada_max', '3', 'Número máximo de intentos de llamada antes de descartar'),
    ('distancia_maxima_default', '40', 'Distancia máxima por defecto en km'),
    ('experiencia_minima_default', '1', 'Experiencia mínima por defecto en años')
ON CONFLICT (clave) DO NOTHING;

-- -----------------------------------------------------------------------------
-- TABLA: LOG DE ACCIONES (auditoría)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS log_acciones (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    accion VARCHAR(100) NOT NULL,
    tabla_afectada VARCHAR(100),
    registro_id INTEGER,
    datos_anteriores JSONB,
    datos_nuevos JSONB,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- VISTAS PARA DASHBOARDS
-- =============================================================================

-- Vista: Candidatos pendientes de primera criba
CREATE OR REPLACE VIEW v_pendientes_criba AS
SELECT
    cp.id as candidato_puesto_id,
    c.id as candidato_id,
    c.nombre,
    c.email,
    c.telefono,
    c.ciudad,
    c.total_anos_experiencia,
    c.carnet_b,
    c.carnet_c,
    c.vehiculo_propio,
    p.id as puesto_id,
    p.nombre as puesto,
    cp.fecha_entrada
FROM candidatos_puestos cp
JOIN candidatos c ON c.id = cp.candidato_id
JOIN puestos p ON p.id = cp.puesto_id
WHERE cp.estado = 'primera_criba'
AND cp.descartado = FALSE
ORDER BY cp.fecha_entrada;

-- Vista: Candidatos pendientes de llamar
CREATE OR REPLACE VIEW v_pendientes_llamar AS
SELECT
    cp.id as candidato_puesto_id,
    c.id as candidato_id,
    c.nombre,
    c.email,
    c.telefono,
    c.ciudad,
    p.nombre as puesto,
    cp.fecha_seleccion,
    COUNT(l.id) as intentos_llamada
FROM candidatos_puestos cp
JOIN candidatos c ON c.id = cp.candidato_id
JOIN puestos p ON p.id = cp.puesto_id
LEFT JOIN llamadas l ON l.candidato_puesto_id = cp.id
WHERE cp.estado = 'seleccionado_llamar'
AND cp.descartado = FALSE
GROUP BY cp.id, c.id, c.nombre, c.email, c.telefono, c.ciudad, p.nombre, cp.fecha_seleccion
ORDER BY cp.fecha_seleccion;

-- Vista: Entrevistas del día
CREATE OR REPLACE VIEW v_entrevistas_hoy AS
SELECT
    e.id as entrevista_id,
    e.fecha,
    e.hora,
    c.nombre as candidato,
    c.telefono,
    p.nombre as puesto,
    u.nombre as entrevistador,
    e.estado
FROM entrevistas e
JOIN candidatos_puestos cp ON cp.id = e.candidato_puesto_id
JOIN candidatos c ON c.id = cp.candidato_id
JOIN puestos p ON p.id = cp.puesto_id
LEFT JOIN usuarios u ON u.id = e.entrevistador_id
WHERE e.fecha = CURRENT_DATE
ORDER BY e.hora;

-- Vista: Resumen dashboard llamador
CREATE OR REPLACE VIEW v_dashboard_llamador AS
SELECT
    u.id as usuario_id,
    u.nombre as llamador,
    COUNT(CASE WHEN cp.estado = 'seleccionado_llamar' THEN 1 END) as pendientes_llamar,
    COUNT(CASE WHEN cp.estado = 'entrevista_programada' THEN 1 END) as entrevistas_programadas,
    COUNT(CASE WHEN cp.descartado AND cp.descartado_por = u.id THEN 1 END) as descartados_hoy
FROM usuarios u
LEFT JOIN candidatos_puestos cp ON cp.seleccionado_por = u.id
WHERE u.rol IN ('llamador', 'revisor')
GROUP BY u.id, u.nombre;

-- =============================================================================
-- FUNCIONES ÚTILES
-- =============================================================================

-- Función: Descartar candidato
CREATE OR REPLACE FUNCTION descartar_candidato(
    p_candidato_puesto_id INTEGER,
    p_motivo_codigo VARCHAR(50),
    p_usuario_id INTEGER,
    p_notas TEXT DEFAULT NULL
) RETURNS BOOLEAN AS $$
DECLARE
    v_motivo_id INTEGER;
BEGIN
    SELECT id INTO v_motivo_id FROM motivos_descarte WHERE codigo = p_motivo_codigo;

    IF v_motivo_id IS NULL THEN
        RETURN FALSE;
    END IF;

    UPDATE candidatos_puestos SET
        descartado = TRUE,
        motivo_descarte_id = v_motivo_id,
        descartado_por = p_usuario_id,
        fecha_descarte = CURRENT_TIMESTAMP,
        notas_descarte = p_notas,
        estado = CASE
            WHEN estado = 'nuevo' THEN 'descartado_auto'
            ELSE 'descartado_manual'
        END,
        fecha_actualizacion = CURRENT_TIMESTAMP
    WHERE id = p_candidato_puesto_id;

    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;

-- Función: Verificar si candidato fue descartado previamente
CREATE OR REPLACE FUNCTION candidato_descartado_previo(p_candidato_id INTEGER)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM candidatos_puestos
        WHERE candidato_id = p_candidato_id AND descartado = TRUE
    );
END;
$$ LANGUAGE plpgsql;

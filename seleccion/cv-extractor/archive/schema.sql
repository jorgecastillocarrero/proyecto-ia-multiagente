-- Esquema de base de datos para CVs
-- PostgreSQL 14+

-- Eliminar tablas si existen (en orden inverso por dependencias)
DROP TABLE IF EXISTS conocimientos_candidato CASCADE;
DROP TABLE IF EXISTS experiencias CASCADE;
DROP TABLE IF EXISTS candidatos CASCADE;

-- =============================================================================
-- TABLA PRINCIPAL: CANDIDATOS
-- =============================================================================
CREATE TABLE candidatos (
    id SERIAL PRIMARY KEY,

    -- Datos personales
    nombre VARCHAR(200) NOT NULL,
    puesto_actual VARCHAR(200),
    codigo_postal VARCHAR(10),
    ciudad VARCHAR(100),
    provincia VARCHAR(100),
    email VARCHAR(200),
    telefono VARCHAR(50),
    telefono_secundario VARCHAR(50),
    porcentaje_ajuste INTEGER,

    -- Datos del candidato
    permiso_trabajo VARCHAR(100),
    carnet_conducir VARCHAR(50),
    es_autonomo BOOLEAN DEFAULT FALSE,
    vehiculo_propio BOOLEAN DEFAULT FALSE,
    carnet_b BOOLEAN DEFAULT FALSE,
    carnet_c BOOLEAN DEFAULT FALSE,
    cap BOOLEAN DEFAULT FALSE,
    carnet_carretillero BOOLEAN DEFAULT FALSE,

    -- Estado general del candidato
    -- 'sin_valorar': CV pendiente de revisar
    -- 'activo': En proceso de seleccion
    -- 'descartado': Descartado del proceso
    estado VARCHAR(20) DEFAULT 'sin_valorar',

    -- Metadatos
    fecha_importacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    archivo_origen VARCHAR(500),
    total_anos_experiencia NUMERIC(4,2),

    -- Índices únicos para evitar duplicados
    CONSTRAINT uk_candidato_email UNIQUE (email)
);

-- Índice para filtrar por estado
CREATE INDEX idx_candidatos_estado ON candidatos(estado);

-- Índices para búsquedas frecuentes
CREATE INDEX idx_candidatos_ciudad ON candidatos(ciudad);
CREATE INDEX idx_candidatos_provincia ON candidatos(provincia);
CREATE INDEX idx_candidatos_carnet ON candidatos(carnet_conducir);

-- =============================================================================
-- TABLA: EXPERIENCIAS LABORALES (1:N)
-- =============================================================================
CREATE TABLE experiencias (
    id SERIAL PRIMARY KEY,
    candidato_id INTEGER NOT NULL REFERENCES candidatos(id) ON DELETE CASCADE,

    puesto VARCHAR(300) NOT NULL,
    empresa VARCHAR(300),
    fecha_inicio DATE,
    fecha_fin DATE,  -- NULL si es el trabajo actual
    duracion_meses INTEGER,
    tipo_contrato VARCHAR(100),
    salario_bruto_mes_min DECIMAL(10,2),
    salario_bruto_mes_max DECIMAL(10,2),
    descripcion TEXT,
    skills TEXT[],  -- Array de PostgreSQL para las skills

    -- Para ordenar cronológicamente
    CONSTRAINT chk_fechas CHECK (fecha_fin IS NULL OR fecha_fin >= fecha_inicio)
);

CREATE INDEX idx_experiencias_candidato ON experiencias(candidato_id);
CREATE INDEX idx_experiencias_fechas ON experiencias(fecha_inicio DESC, fecha_fin DESC);
CREATE INDEX idx_experiencias_skills ON experiencias USING GIN(skills);

-- NOTA: Tablas idiomas y formaciones eliminadas
-- Solo se usa carnet_carretillero en tabla candidatos

-- =============================================================================
-- TABLA: CONOCIMIENTOS/SKILLS (N:M simplificado como 1:N)
-- =============================================================================
CREATE TABLE conocimientos_candidato (
    id SERIAL PRIMARY KEY,
    candidato_id INTEGER NOT NULL REFERENCES candidatos(id) ON DELETE CASCADE,
    conocimiento VARCHAR(200) NOT NULL,

    CONSTRAINT uk_candidato_conocimiento UNIQUE (candidato_id, conocimiento)
);

CREATE INDEX idx_conocimientos_candidato ON conocimientos_candidato(candidato_id);
CREATE INDEX idx_conocimientos_nombre ON conocimientos_candidato(conocimiento);

-- =============================================================================
-- VISTAS ÚTILES
-- =============================================================================

-- Vista resumen de candidatos
CREATE OR REPLACE VIEW v_candidatos_resumen AS
SELECT
    c.id,
    c.nombre,
    c.email,
    c.telefono,
    c.ciudad,
    c.estado,
    c.carnet_conducir,
    c.vehiculo_propio,
    c.carnet_carretillero,
    COUNT(DISTINCT e.id) AS total_experiencias,
    COALESCE(SUM(e.duracion_meses), 0) AS meses_experiencia_total,
    ROUND(COALESCE(SUM(e.duracion_meses), 0) / 12.0, 1) AS anos_experiencia
FROM candidatos c
LEFT JOIN experiencias e ON e.candidato_id = c.id
GROUP BY c.id, c.nombre, c.email, c.telefono, c.ciudad, c.estado, c.carnet_conducir, c.vehiculo_propio, c.carnet_carretillero;

-- Vista de skills más comunes
CREATE OR REPLACE VIEW v_skills_populares AS
SELECT
    conocimiento,
    COUNT(*) AS total_candidatos
FROM conocimientos_candidato
GROUP BY conocimiento
ORDER BY total_candidatos DESC;

-- =============================================================================
-- FUNCIONES ÚTILES
-- =============================================================================

-- Función para buscar candidatos por skill
CREATE OR REPLACE FUNCTION buscar_por_skill(skill_busqueda TEXT)
RETURNS TABLE (
    candidato_id INTEGER,
    nombre VARCHAR,
    email VARCHAR,
    telefono VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT c.id, c.nombre, c.email, c.telefono
    FROM candidatos c
    JOIN conocimientos_candidato cc ON cc.candidato_id = c.id
    WHERE cc.conocimiento ILIKE '%' || skill_busqueda || '%'
    ORDER BY c.nombre;
END;
$$ LANGUAGE plpgsql;

-- Función para buscar candidatos con carnet y vehículo
CREATE OR REPLACE FUNCTION buscar_con_vehiculo(tipo_carnet TEXT DEFAULT NULL)
RETURNS TABLE (
    candidato_id INTEGER,
    nombre VARCHAR,
    email VARCHAR,
    carnet VARCHAR,
    tiene_vehiculo BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.nombre, c.email, c.carnet_conducir, c.vehiculo_propio
    FROM candidatos c
    WHERE c.vehiculo_propio = TRUE
    AND (tipo_carnet IS NULL OR c.carnet_conducir = tipo_carnet)
    ORDER BY c.nombre;
END;
$$ LANGUAGE plpgsql;

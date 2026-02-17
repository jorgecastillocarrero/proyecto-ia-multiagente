// backend/src/controllers/rrhhController.js
const { asyncHandler } = require('../middlewares/errorHandler');
const { dbPool } = require('../config/database');

const getCandidatos = asyncHandler(async (req, res) => {
    const {
        page = 1,
        limit = 50,
        estado,
        search,
        provincia,
        experienciaMin,
        carnetB,
        carnetC,
        vehiculoPropio,
        ordenarPor = 'fecha'
    } = req.query;

    let query = `
        SELECT 
            c.*,
            COUNT(DISTINCT cp.id) as total_puestos,
            COUNT(DISTINCT CASE WHEN cp.descartado = 0 THEN cp.id END) as puestos_activos,
            COUNT(DISTINCT CASE WHEN cp.estado = 'seleccionado_final' THEN cp.id END) as puestos_aceptado
        FROM candidatos c
        LEFT JOIN candidatos_puestos cp ON cp.candidato_id = c.id
        WHERE 1=1
    `;

    const params = [];

    // Filtro por estado
    if (estado && estado !== 'todos') {
        query += ' AND c.estado = ?';
        params.push(estado);
    }

    // Filtro por búsqueda (nombre, email, teléfono)
    if (search) {
        query += ' AND (c.nombre LIKE ? OR c.email LIKE ? OR c.telefono LIKE ?)';
        params.push(`%${search}%`, `%${search}%`, `%${search}%`);
    }

    // Filtro por provincia
    if (provincia) {
        query += ' AND c.provincia = ?';
        params.push(provincia);
    }

    // Filtro por experiencia mínima
    if (experienciaMin) {
        query += ' AND c.total_anos_experiencia >= ?';
        params.push(parseInt(experienciaMin));
    }

    // Filtro por Carnet B
    if (carnetB === 'true') {
        query += ' AND c.carnet_b = 1';
    }

    // Filtro por Carnet C
    if (carnetC === 'true') {
        query += ' AND c.carnet_c = 1';
    }

    // Filtro por vehículo propio
    if (vehiculoPropio === 'true') {
        query += ' AND c.vehiculo_propio = 1';
    }

    query += ' GROUP BY c.id';

    // Ordenamiento
    switch (ordenarPor) {
        case 'nombre':
            query += ' ORDER BY c.nombre ASC';
            break;
        case 'experiencia':
            query += ' ORDER BY c.total_anos_experiencia DESC';
            break;
        case 'fecha':
        default:
            query += ' ORDER BY c.fecha_importacion DESC';
            break;
    }

    // Paginación
    const offset = (page - 1) * limit;
    query += ' LIMIT ? OFFSET ?';
    params.push(parseInt(limit), offset);

    const [candidatos] = await dbPool.query(query, params);

    // Contar total con los mismos filtros
    let countQuery = 'SELECT COUNT(DISTINCT c.id) as total FROM candidatos c WHERE 1=1';
    const countParams = [];

    if (estado && estado !== 'todos') {
        countQuery += ' AND c.estado = ?';
        countParams.push(estado);
    }

    if (search) {
        countQuery += ' AND (c.nombre LIKE ? OR c.email LIKE ? OR c.telefono LIKE ?)';
        countParams.push(`%${search}%`, `%${search}%`, `%${search}%`);
    }

    if (provincia) {
        countQuery += ' AND c.provincia = ?';
        countParams.push(provincia);
    }

    if (experienciaMin) {
        countQuery += ' AND c.total_anos_experiencia >= ?';
        countParams.push(parseInt(experienciaMin));
    }

    if (carnetB === 'true') {
        countQuery += ' AND c.carnet_b = 1';
    }

    if (carnetC === 'true') {
        countQuery += ' AND c.carnet_c = 1';
    }

    if (vehiculoPropio === 'true') {
        countQuery += ' AND c.vehiculo_propio = 1';
    }

    const [countResult] = await dbPool.query(countQuery, countParams);

    res.json({
        success: true,
        data: candidatos,
        pagination: {
            page: parseInt(page),
            limit: parseInt(limit),
            total: countResult[0].total,
            totalPages: Math.ceil(countResult[0].total / limit)
        }
    });
});

const getEstadisticas = asyncHandler(async (req, res) => {
    const [stats] = await dbPool.query(`
        SELECT
            (SELECT COUNT(*) FROM candidatos WHERE estado = 'sin_valorar') as candidatos_sin_valorar,
            (SELECT COUNT(*) FROM candidatos WHERE estado = 'activo') as candidatos_activos,
            (SELECT COUNT(*) FROM candidatos WHERE estado = 'descartado') as candidatos_descartados,
            0 as pendientes_criba,
            0 as pendientes_llamar,
            0 as entrevistas_hoy,
            0 as puestos_activos,
            (SELECT COUNT(*) FROM candidatos WHERE user_id IS NOT NULL) as candidatos_con_acceso_portal
    `);

    res.json({
        success: true,
        data: stats[0]
    });
});

// Endpoints placeholder
const getCandidatoDetalle = asyncHandler(async (req, res) => {
    const { id } = req.params;

    // Datos del candidato
    const [candidatos] = await dbPool.query('SELECT * FROM candidatos WHERE id = ?', [id]);

    if (candidatos.length === 0) {
        return res.status(404).json({
            success: false,
            message: 'Candidato no encontrado'
        });
    }

    const candidato = candidatos[0];

    // Experiencias
    const [experiencias] = await dbPool.query(
        'SELECT * FROM experiencias WHERE candidato_id = ? ORDER BY fecha_inicio DESC',
        [id]
    );

    // Conocimientos
    const [conocimientos] = await dbPool.query(
        'SELECT conocimiento FROM conocimientos_candidato WHERE candidato_id = ?',
        [id]
    );

    // Puestos a los que está asignado
    const [puestos] = await dbPool.query(`
        SELECT 
            cp.*,
            p.nombre as puesto_nombre,
            p.descripcion as puesto_descripcion
        FROM candidatos_puestos cp
        JOIN puestos p ON p.id = cp.puesto_id
        WHERE cp.candidato_id = ?
        ORDER BY cp.fecha_entrada DESC
    `, [id]);

    // Si tiene user_id, traer datos del portal
    let datosPortal = null;
    if (candidato.user_id) {
        const [users] = await dbPool.query(
            'SELECT id, firstName, lastName, email, dni, documents_uploaded, form_completed, exam_completed, createdAt FROM users WHERE id = ?',
            [candidato.user_id]
        );
        if (users.length > 0) {
            datosPortal = users[0];
        }
    }

    res.json({
        success: true,
        data: {
            candidato,
            experiencias,
            conocimientos: conocimientos.map(c => c.conocimiento),
            puestos,
            datosPortal
        }
    });
});

const getPendientesCriba = asyncHandler(async (req, res) => {
    res.json({ success: true, data: [] });
});

const getPendientesLlamar = asyncHandler(async (req, res) => {
    res.json({ success: true, data: [] });
});

const getPuestos = asyncHandler(async (req, res) => {
    res.json({ success: true, data: [] });
});

const crearPuesto = asyncHandler(async (req, res) => {
    res.json({ success: true, message: 'En desarrollo' });
});

const actualizarPuesto = asyncHandler(async (req, res) => {
    res.json({ success: true, message: 'En desarrollo' });
});

const cerrarPuesto = asyncHandler(async (req, res) => {
    res.json({ success: true, message: 'En desarrollo' });
});

const getCandidatosPuesto = asyncHandler(async (req, res) => {
    res.json({ success: true, data: [] });
});

const aprobarCandidato = asyncHandler(async (req, res) => {
    res.json({ success: true, message: 'En desarrollo' });
});

const descartarCandidato = asyncHandler(async (req, res) => {
    res.json({ success: true, message: 'En desarrollo' });
});

const registrarLlamada = asyncHandler(async (req, res) => {
    res.json({ success: true, message: 'En desarrollo' });
});

const getHistorialLlamadas = asyncHandler(async (req, res) => {
    res.json({ success: true, data: [] });
});

const programarEntrevista = asyncHandler(async (req, res) => {
    res.json({ success: true, message: 'En desarrollo' });
});

const actualizarResultadoEntrevista = asyncHandler(async (req, res) => {
    res.json({ success: true, message: 'En desarrollo' });
});

const getEntrevistasHoy = asyncHandler(async (req, res) => {
    res.json({ success: true, data: [] });
});

const getEntrevistas = asyncHandler(async (req, res) => {
    res.json({ success: true, data: [] });
});

const aceptarCandidatoFinal = asyncHandler(async (req, res) => {
    res.json({ success: true, message: 'En desarrollo' });
});

const getMotivosDescarte = asyncHandler(async (req, res) => {
    res.json({ success: true, data: [] });
});

module.exports = {
    getCandidatos,
    getCandidatoDetalle,
    getPendientesCriba,
    getPendientesLlamar,
    getPuestos,
    crearPuesto,
    actualizarPuesto,
    cerrarPuesto,
    getCandidatosPuesto,
    aprobarCandidato,
    descartarCandidato,
    registrarLlamada,
    getHistorialLlamadas,
    programarEntrevista,
    actualizarResultadoEntrevista,
    getEntrevistasHoy,
    getEntrevistas,
    aceptarCandidatoFinal,
    getMotivosDescarte,
    getEstadisticas
};
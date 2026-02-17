// backend/src/routes/rrhhRoutes.js
const express = require('express');
const router = express.Router();
const rrhhController = require('../controllers/rrhhController');
const { authenticate, authorizeAdmin } = require('../middlewares/auth');

// Candidatos
router.get('/candidatos', authenticate, authorizeAdmin, rrhhController.getCandidatos);
router.get('/candidatos/:id', authenticate, authorizeAdmin, rrhhController.getCandidatoDetalle);
router.get('/pendientes/criba', authenticate, authorizeAdmin, rrhhController.getPendientesCriba);
router.get('/pendientes/llamar', authenticate, authorizeAdmin, rrhhController.getPendientesLlamar);

// Estadísticas
router.get('/estadisticas', authenticate, authorizeAdmin, rrhhController.getEstadisticas);

module.exports = router;
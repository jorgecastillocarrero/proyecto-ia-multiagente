const express = require('express');
const router = express.Router();
const adminController = require('../controllers/adminController');
const { authenticate, authorizeAdmin } = require('../middlewares/auth');
const { loginValidation } = require('../validators');

// POST /api/admin/auth/login (sin autenticación)
router.post('/auth/login', loginValidation, adminController.login);

// GET /api/admin/generate-link (requiere autenticación admin)
router.get('/generate-link', authenticate, authorizeAdmin, adminController.generateLink);

// GET /api/admin/candidates (requiere autenticación admin)
router.get('/candidates', authenticate, authorizeAdmin, adminController.getAllCandidates);

module.exports = router;
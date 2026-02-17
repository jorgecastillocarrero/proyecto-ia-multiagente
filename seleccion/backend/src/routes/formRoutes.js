// src/routes/formRoutes.js
const express = require('express');
const router = express.Router();
const formController = require('../controllers/formController');
const { authenticate } = require('../middlewares/auth');

// GET /api/form/data (requiere autenticación)
router.get('/data', authenticate, formController.getFormData);

// POST /api/form/submit (requiere autenticación)
router.post('/submit', authenticate, formController.saveFormData);

module.exports = router;
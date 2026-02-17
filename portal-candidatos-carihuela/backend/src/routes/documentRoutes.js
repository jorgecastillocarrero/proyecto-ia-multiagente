// src/routes/documentRoutes.js
const express = require('express');
const router = express.Router();
const documentController = require('../controllers/documentController');
const { authenticate } = require('../middlewares/auth');
const { uploadDocuments } = require('../middlewares/upload');

// POST /api/documents/upload (requiere autenticación)
router.post(
    '/upload',
    authenticate,
    uploadDocuments,
    documentController.uploadDocuments
);

// GET /api/documents (requiere autenticación)
router.get('/', authenticate, documentController.getUserDocuments);

module.exports = router;
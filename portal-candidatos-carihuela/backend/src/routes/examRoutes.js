const express = require('express');
const router = express.Router();
const examController = require('../controllers/examController');
const { authenticate } = require('../middlewares/auth');

// GET /api/exam/status (requiere autenticación)
router.get('/status', authenticate, examController.getExamStatus);

// POST /api/exam/submit (requiere autenticación)
router.post('/submit', authenticate, examController.submitExam);

module.exports = router;
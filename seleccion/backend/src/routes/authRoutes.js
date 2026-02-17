const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');
const { registerValidation, loginValidation } = require('../validators');

// GET /api/auth/verify-token?token=xxx
router.get('/verify-token', authController.verifyToken);

// POST /api/auth/register
router.post('/register', registerValidation, authController.register);

// POST /api/auth/login
router.post('/login', loginValidation, authController.login);

module.exports = router;
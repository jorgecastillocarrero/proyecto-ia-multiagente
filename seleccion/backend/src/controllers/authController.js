// src/controllers/authController.js
const authService = require('../services/authService');
const { asyncHandler } = require('../middlewares/errorHandler');

// POST /api/auth/register
const register = asyncHandler(async (req, res) => {
    const result = await authService.register(req.body);
    res.status(201).json(result);
});

// POST /api/auth/login
const login = asyncHandler(async (req, res) => {
    const result = await authService.login(req.body);
    res.json(result);
});

// GET /api/auth/verify-token?token=xxx
const verifyToken = asyncHandler(async (req, res) => {
    const { token } = req.query;
    const result = await authService.verifyRegistrationToken(token);
    res.json(result);
});

module.exports = {
    register,
    login,
    verifyToken
};
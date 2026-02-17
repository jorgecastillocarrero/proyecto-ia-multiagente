// src/controllers/adminController.js
const authService = require('../services/authService');
const adminService = require('../services/adminService');
const { asyncHandler } = require('../middlewares/errorHandler');

// POST /api/admin/auth/login
const login = asyncHandler(async (req, res) => {
    const result = await authService.loginAdmin(req.body);
    res.json(result);
});

// GET /api/admin/generate-link?email=xxx&frontendUrl=xxx&type=valid
const generateLink = asyncHandler(async (req, res) => {
    const { email, frontendUrl, type } = req.query;
    const result = await adminService.generateRegistrationLink(email, frontendUrl, type);
    res.json(result);
});

// GET /api/admin/candidates
const getAllCandidates = asyncHandler(async (req, res) => {
    const result = await adminService.getAllCandidates();
    res.json(result);
});

module.exports = {
    login,
    generateLink,
    getAllCandidates
};
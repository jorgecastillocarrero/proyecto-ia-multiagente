const formService = require('../services/formService');
const { asyncHandler } = require('../middlewares/errorHandler');

// GET /api/form/data
const getFormData = asyncHandler(async (req, res) => {
    const userId = req.user.id;
    const result = await formService.getFormData(userId);
    res.json(result);
});

// POST /api/form/submit
const saveFormData = asyncHandler(async (req, res) => {
    const userId = req.user.id;
    const formData = req.body;

    const result = await formService.saveFormData(userId, formData);
    res.json(result);
});

module.exports = {
    getFormData,
    saveFormData
};
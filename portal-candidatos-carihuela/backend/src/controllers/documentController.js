const documentService = require('../services/documentService');
const { asyncHandler } = require('../middlewares/errorHandler');
const { AppError } = require('../middlewares/errorHandler');
const { HTTP_STATUS } = require('../utils/constants');

// POST /api/documents/upload
const uploadDocuments = asyncHandler(async (req, res) => {
    const userId = req.user.id;
    const files = req.files;

    if (!files || Object.keys(files).length === 0) {
        throw new AppError('No files were uploaded', HTTP_STATUS.BAD_REQUEST);
    }

    const result = await documentService.uploadDocuments(userId, files);
    res.json(result);
});

// GET /api/documents
const getUserDocuments = asyncHandler(async (req, res) => {
    const userId = req.user.id;
    const result = await documentService.getUserDocuments(userId);
    res.json(result);
});

module.exports = {
    uploadDocuments,
    getUserDocuments
};
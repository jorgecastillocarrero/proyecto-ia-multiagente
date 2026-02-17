// src/middlewares/upload.js
const multer = require('multer');
const path = require('path');
const { AppError } = require('./errorHandler');
const { HTTP_STATUS } = require('../utils/constants');

// Configuración de almacenamiento
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/');
    },
    filename: (req, file, cb) => {
        // Nombre único: timestamp-random-originalname
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        const ext = path.extname(file.originalname);
        const nameWithoutExt = path.basename(file.originalname, ext);
        cb(null, `${nameWithoutExt}-${uniqueSuffix}${ext}`);
    }
});

// Filtro de archivos (solo PDF, JPG, PNG)
const fileFilter = (req, file, cb) => {
    const allowedMimes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];

    if (allowedMimes.includes(file.mimetype)) {
        cb(null, true);
    } else {
        cb(new AppError(
            `Invalid file type: ${file.mimetype}. Only PDF, JPG, and PNG are allowed`,
            HTTP_STATUS.BAD_REQUEST
        ));
    }
};

// Configuración de Multer
const upload = multer({
    storage: storage,
    fileFilter: fileFilter,
    limits: {
        fileSize: 10 * 1024 * 1024 // 10MB máximo
    }
});

// Middleware para múltiples campos
const uploadDocuments = upload.fields([
    { name: 'dniCopy', maxCount: 1 },
    { name: 'jobSeeker', maxCount: 1 },
    { name: 'degreeCopy', maxCount: 1 },
    { name: 'foodHandlerCertificate', maxCount: 1 },
    { name: 'youthGuarantee', maxCount: 1 }
]);

module.exports = {
    upload,
    uploadDocuments
};
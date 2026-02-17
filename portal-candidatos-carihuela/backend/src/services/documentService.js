// src/services/documentService.js
const documentRepository = require('../repositories/documentRepository');
const userRepository = require('../repositories/userRepository');
const { AppError } = require('../middlewares/errorHandler');
const { HTTP_STATUS } = require('../utils/constants');
const logger = require('../utils/logger');

class DocumentService {
    async uploadDocuments(userId, files) {
        logger.info('Uploading documents', { userId, fileCount: Object.keys(files).length });

        // Verificar si ya subió documentos
        const hasDocuments = await documentRepository.hasDocuments(userId);

        if (hasDocuments) {
            throw new AppError(
                'Documents have already been submitted and are under review',
                HTTP_STATUS.BAD_REQUEST
            );
        }

        // Guardar cada archivo
        const savedDocuments = [];
        for (const fieldName in files) {
            const fileArray = files[fieldName];
            if (fileArray && fileArray.length > 0) {
                const file = fileArray[0];

                const document = await documentRepository.createDocument({
                    userId,
                    type: fieldName,
                    originalName: file.originalname,
                    filePath: file.path,
                    fileSize: file.size,
                    mimeType: file.mimetype
                });

                savedDocuments.push(document);
            }
        }

        // Actualizar flag del usuario
        await userRepository.updateProgressFlags(userId, { documents_uploaded: true });

        logger.info('Documents uploaded successfully', {
            userId,
            documentsCount: savedDocuments.length
        });

        return {
            success: true,
            message: 'Documents uploaded successfully',
            documents: savedDocuments
        };
    }

    async getUserDocuments(userId) {
        const documents = await documentRepository.findByUserId(userId);

        return {
            success: true,
            documents
        };
    }
}

module.exports = new DocumentService();
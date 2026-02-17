// src/repositories/documentRepository.js
const BaseRepository = require('./BaseRepository');
const { dbPool } = require('../config/database');

class DocumentRepository extends BaseRepository {
    constructor() {
        super('user_documents');
    }

    async findByUserId(userId) {
        return await this.findAll({ user_id: userId });
    }

    async hasDocuments(userId) {
        const count = await this.count({ user_id: userId });
        return count > 0;
    }

    async createDocument(documentData) {
        return await this.create({
            user_id: documentData.userId,
            document_type: documentData.type,
            original_name: documentData.originalName,
            file_path: documentData.filePath,
            file_size: documentData.fileSize,
            mime_type: documentData.mimeType
        });
    }

    async deleteByUserId(userId) {
        const query = `DELETE FROM ${this.tableName} WHERE user_id = ?`;
        const [result] = await dbPool.query(query, [userId]);
        return result.affectedRows;
    }
}

module.exports = new DocumentRepository();
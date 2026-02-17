// src/repositories/tokenRepository.js
const BaseRepository = require('./BaseRepository');
const { dbPool } = require('../config/database');

class TokenRepository extends BaseRepository {
    constructor() {
        super('registration_tokens');
    }

    async findValidToken(token) {
        const query = `
      SELECT * FROM ${this.tableName} 
      WHERE token = ? 
      AND isUsed = FALSE 
      AND expiresAt > UTC_TIMESTAMP()
      LIMIT 1
    `;
        const [rows] = await dbPool.query(query, [token]);
        return rows[0] || null;
    }

    async markTokenAsUsed(token) {
        const query = `
      UPDATE ${this.tableName} 
      SET isUsed = TRUE, usedAt = UTC_TIMESTAMP() 
      WHERE token = ?
    `;
        const [result] = await dbPool.query(query, [token]);
        return result.affectedRows > 0;
    }

    async createToken(tokenData) {
        return await this.create({
            token: tokenData.token,
            email: tokenData.email,
            expiresAt: tokenData.expiresAt,
            isUsed: false
        });
    }
}

module.exports = new TokenRepository();
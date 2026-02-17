// src/repositories/userRepository.js
const BaseRepository = require('./BaseRepository');
const { dbPool } = require('../config/database');

class UserRepository extends BaseRepository {
    constructor() {
        super('users');
    }

    async findByEmail(email) {
        return await this.findOne({ email });
    }

    async findByDNI(dni) {
        return await this.findOne({ dni });
    }

    async findByEmailOrDNI(email, dni) {
        const query = `SELECT * FROM ${this.tableName} WHERE email = ? OR dni = ? LIMIT 1`;
        const [rows] = await dbPool.query(query, [email, dni]);
        return rows[0] || null;
    }

    async createUser(userData) {
        return await this.create({
            firstName: userData.firstName,
            lastName: userData.lastName,
            dni: userData.dni,
            email: userData.email,
            passwordHash: userData.passwordHash,
            role: userData.role || 0
        });
    }

    async getAllCandidates() {
        const query = `
      SELECT id, firstName, lastName, email, dni, 
             documents_uploaded, form_completed, exam_completed, createdAt 
      FROM ${this.tableName} 
      WHERE role = 0 
      ORDER BY createdAt DESC
    `;
        const [rows] = await dbPool.query(query);
        return rows;
    }

    async updateProgressFlags(userId, flags) {
        const allowedFlags = ['documents_uploaded', 'form_completed', 'exam_completed'];
        const updateData = {};

        for (const [key, value] of Object.entries(flags)) {
            if (allowedFlags.includes(key)) {
                updateData[key] = value ? 1 : 0;
            }
        }

        if (Object.keys(updateData).length === 0) {
            return false;
        }

        return await this.update(userId, updateData);
    }
}

module.exports = new UserRepository();
// src/repositories/BaseRepository.js
const { dbPool } = require('../config/database');
const logger = require('../utils/logger');

class BaseRepository {
    constructor(tableName) {
        this.tableName = tableName;
    }

    async findById(id) {
        const query = `SELECT * FROM ${this.tableName} WHERE id = ?`;
        const [rows] = await dbPool.query(query, [id]);
        return rows[0] || null;
    }

    async findOne(conditions) {
        const keys = Object.keys(conditions);
        const whereClause = keys.map(key => `${key} = ?`).join(' AND ');
        const values = Object.values(conditions);

        const query = `SELECT * FROM ${this.tableName} WHERE ${whereClause} LIMIT 1`;
        const [rows] = await dbPool.query(query, values);
        return rows[0] || null;
    }

    async findAll(conditions = {}) {
        let query = `SELECT * FROM ${this.tableName}`;
        let values = [];

        if (Object.keys(conditions).length > 0) {
            const keys = Object.keys(conditions);
            const whereClause = keys.map(key => `${key} = ?`).join(' AND ');
            values = Object.values(conditions);
            query += ` WHERE ${whereClause}`;
        }

        const [rows] = await dbPool.query(query, values);
        return rows;
    }

    async create(data) {
        const columns = Object.keys(data).join(', ');
        const placeholders = Object.keys(data).map(() => '?').join(', ');
        const values = Object.values(data);

        const query = `INSERT INTO ${this.tableName} (${columns}) VALUES (${placeholders})`;
        const [result] = await dbPool.query(query, values);

        return {
            id: result.insertId,
            ...data
        };
    }

    async update(id, data) {
        const setClause = Object.keys(data).map(key => `${key} = ?`).join(', ');
        const values = [...Object.values(data), id];

        const query = `UPDATE ${this.tableName} SET ${setClause} WHERE id = ?`;
        const [result] = await dbPool.query(query, values);

        return result.affectedRows > 0;
    }

    async delete(id) {
        const query = `DELETE FROM ${this.tableName} WHERE id = ?`;
        const [result] = await dbPool.query(query, [id]);
        return result.affectedRows > 0;
    }

    async count(conditions = {}) {
        let query = `SELECT COUNT(*) as total FROM ${this.tableName}`;
        let values = [];

        if (Object.keys(conditions).length > 0) {
            const keys = Object.keys(conditions);
            const whereClause = keys.map(key => `${key} = ?`).join(' AND ');
            values = Object.values(conditions);
            query += ` WHERE ${whereClause}`;
        }

        const [rows] = await dbPool.query(query, values);
        return rows[0].total;
    }
}

module.exports = BaseRepository;
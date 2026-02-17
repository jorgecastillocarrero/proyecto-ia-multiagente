const mysql = require('mysql2/promise');
const logger = require('../utils/logger');

const dbPool = mysql.createPool({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    port: process.env.DB_PORT || 3306,
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0,
    charset: 'utf8mb4'
});

const testConnection = async () => {
    try {
        const connection = await dbPool.getConnection();
        logger.info('✅ Database connected');
        connection.release();
        return true;
    } catch (error) {
        logger.error('❌ Database connection failed:', error);
        return false;
    }
};

module.exports = { dbPool, testConnection };
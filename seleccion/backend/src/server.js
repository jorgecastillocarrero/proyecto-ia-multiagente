// backend/src/server.js
const express = require('express');
const cors = require('cors');
require('dotenv').config();

const { testConnection } = require('./config/database');
const { errorHandler } = require('./middlewares/errorHandler');
const logger = require('./utils/logger');

const authRoutes = require('./routes/authRoutes');
const adminRoutes = require('./routes/adminRoutes');
const documentRoutes = require('./routes/documentRoutes');
const formRoutes = require('./routes/formRoutes');
const examRoutes = require('./routes/examRoutes');

const rrhhRoutes = require('./routes/rrhhRoutes');

const app = express();

app.use(cors({ origin: process.env.FRONTEND_URL || 'http://localhost:4200' }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use((req, res, next) => {
    logger.info(`${req.method} ${req.path}`, {
        ip: req.ip,
        userAgent: req.get('user-agent')
    });
    next();
});

app.use('/api/auth', authRoutes);
app.use('/api/admin', adminRoutes);
app.use('/api/documents', documentRoutes);
app.use('/api/form', formRoutes);
app.use('/api/exam', examRoutes);
app.use('/api/rrhh', rrhhRoutes);

app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        timestamp: new Date().toISOString(),
        env: process.env.NODE_ENV
    });
});

// Error handler (debe ir al final)
app.use(errorHandler);

// 404
app.use((req, res) => {
    res.status(404).json({
        success: false,
        message: 'Ruta no encontrada'
    });
});

const PORT = process.env.PORT || 3001;

const startServer = async () => {
    try {
        const dbConnected = await testConnection();

        if (!dbConnected) {
            logger.error('No se pudo conectar a la base de datos. Deteniendo servidor.');
            process.exit(1);
        }

        app.listen(PORT, () => {
            logger.info(`🚀 Servidor corriendo en puerto ${PORT}`);
            logger.info(`📝 Ambiente: ${process.env.NODE_ENV || 'development'}`);
            logger.info(`🗄️  Base de datos: ${process.env.DB_NAME}`);
        });
    } catch (error) {
        logger.error('Error al iniciar servidor:', error);
        process.exit(1);
    }
};

startServer();

module.exports = app;
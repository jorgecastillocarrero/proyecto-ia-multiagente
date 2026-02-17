// src/middlewares/errorHandler.js
const logger = require('../utils/logger');
const { HTTP_STATUS } = require('../utils/constants');

class AppError extends Error {
    constructor(message, statusCode) {
        super(message);
        this.statusCode = statusCode;
        this.isOperational = true;
    }
}

const errorHandler = (err, req, res, next) => {
    let error = { ...err };
    error.message = err.message;
    error.statusCode = err.statusCode || HTTP_STATUS.INTERNAL_SERVER_ERROR;

    logger.error('Error:', {
        message: error.message,
        stack: err.stack,
        url: req.url,
        method: req.method
    });

    res.status(error.statusCode).json({
        success: false,
        error: {
            message: error.message
        }
    });
};

const notFoundHandler = (req, res) => {
    res.status(HTTP_STATUS.NOT_FOUND).json({
        success: false,
        error: {
            message: `Route ${req.originalUrl} not found`
        }
    });
};

const asyncHandler = (fn) => {
    return (req, res, next) => {
        Promise.resolve(fn(req, res, next)).catch(next);
    };
};

module.exports = {
    AppError,
    errorHandler,
    notFoundHandler,
    asyncHandler
};
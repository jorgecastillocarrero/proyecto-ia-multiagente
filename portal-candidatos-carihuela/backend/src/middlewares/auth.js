// src/middlewares/auth.js
const jwt = require('jsonwebtoken');
const { AppError } = require('./errorHandler');
const { ROLES, HTTP_STATUS, ERROR_MESSAGES } = require('../utils/constants');

const authenticate = (req, res, next) => {
    try {
        const authHeader = req.headers.authorization;

        if (!authHeader || !authHeader.startsWith('Bearer ')) {
            throw new AppError(ERROR_MESSAGES.UNAUTHORIZED, HTTP_STATUS.UNAUTHORIZED);
        }

        const token = authHeader.split(' ')[1];
        const decoded = jwt.verify(token, process.env.JWT_SECRET);

        req.user = decoded;
        next();
    } catch (error) {
        if (error.name === 'TokenExpiredError') {
            next(new AppError(ERROR_MESSAGES.TOKEN_EXPIRED, HTTP_STATUS.UNAUTHORIZED));
        } else if (error.name === 'JsonWebTokenError') {
            next(new AppError(ERROR_MESSAGES.TOKEN_INVALID, HTTP_STATUS.UNAUTHORIZED));
        } else {
            next(error);
        }
    }
};

const authorizeAdmin = (req, res, next) => {
    if (req.user && req.user.role === ROLES.ADMIN) {
        next();
    } else {
        next(new AppError(ERROR_MESSAGES.FORBIDDEN, HTTP_STATUS.FORBIDDEN));
    }
};

module.exports = { authenticate, authorizeAdmin, isAdmin: authorizeAdmin };
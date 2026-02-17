// src/validators/index.js
const { body, query, validationResult } = require('express-validator');
const { AppError } = require('../middlewares/errorHandler');
const { HTTP_STATUS } = require('../utils/constants');

const handleValidationErrors = (req, res, next) => {
    const errors = validationResult(req);

    if (!errors.isEmpty()) {
        const formattedErrors = errors.array().map(error => ({
            field: error.path,
            message: error.msg
        }));

        return res.status(HTTP_STATUS.BAD_REQUEST).json({
            success: false,
            error: {
                message: 'Validation failed',
                errors: formattedErrors
            }
        });
    }

    next();
};

const registerValidation = [
    body('token').trim().notEmpty().withMessage('Token is required'),
    body('firstName').trim().notEmpty().withMessage('First name is required'),
    body('lastName').trim().notEmpty().withMessage('Last name is required'),
    body('dni').trim().notEmpty().withMessage('DNI is required'),
    body('password')
        .isLength({ min: 8 })
        .withMessage('Password must be at least 8 characters'),
    handleValidationErrors
];

const loginValidation = [
    body('email').isEmail().withMessage('Valid email is required'),
    body('password').notEmpty().withMessage('Password is required'),
    handleValidationErrors
];

module.exports = {
    registerValidation,
    loginValidation,
    handleValidationErrors
};
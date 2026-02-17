// src/utils/constants.js
const ROLES = Object.freeze({
    CANDIDATE: 0,
    ADMIN: 1
});

const JWT_CONFIG = Object.freeze({
    CANDIDATE_EXPIRY: '1d',
    ADMIN_EXPIRY: '8h'
});

const HTTP_STATUS = Object.freeze({
    OK: 200,
    CREATED: 201,
    BAD_REQUEST: 400,
    UNAUTHORIZED: 401,
    FORBIDDEN: 403,
    NOT_FOUND: 404,
    CONFLICT: 409,
    INTERNAL_SERVER_ERROR: 500
});

const ERROR_MESSAGES = Object.freeze({
    INVALID_CREDENTIALS: 'Invalid email or password',
    UNAUTHORIZED: 'Unauthorized access',
    FORBIDDEN: 'Access forbidden',
    REQUIRED_FIELDS_MISSING: 'All fields are required',
    USER_ALREADY_EXISTS: 'User already exists',
    TOKEN_EXPIRED: 'Token has expired',
    TOKEN_INVALID: 'Invalid token'
});

module.exports = {
    ROLES,
    JWT_CONFIG,
    HTTP_STATUS,
    ERROR_MESSAGES
};
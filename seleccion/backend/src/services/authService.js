// src/services/authService.js
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const userRepository = require('../repositories/userRepository');
const tokenRepository = require('../repositories/tokenRepository');
const { AppError } = require('../middlewares/errorHandler');
const { JWT_CONFIG, ROLES, HTTP_STATUS, ERROR_MESSAGES } = require('../utils/constants');
const logger = require('../utils/logger');

class AuthService {
    // Generar token JWT
    generateToken(user, expiresIn) {
        return jwt.sign(
            {
                id: user.id,
                email: user.email,
                role: user.role
            },
            process.env.JWT_SECRET,
            { expiresIn }
        );
    }

    // Hash de contraseña
    async hashPassword(password) {
        return await bcrypt.hash(password, 12);
    }

    // Comparar contraseña
    async comparePassword(plainPassword, hashedPassword) {
        return await bcrypt.compare(plainPassword, hashedPassword);
    }

    // Registrar nuevo usuario
    async register(registrationData) {
        const { token, firstName, lastName, dni, password } = registrationData;

        logger.info('Iniciando registro', { token });

        // Verificar token de registro
        const registrationToken = await tokenRepository.findValidToken(token);

        if (!registrationToken) {
            throw new AppError('Token de registro inválido o expirado', HTTP_STATUS.BAD_REQUEST);
        }

        // Verificar si usuario ya existe
        const existingUser = await userRepository.findByEmailOrDNI(
            registrationToken.email,
            dni
        );

        if (existingUser) {
            throw new AppError(ERROR_MESSAGES.USER_ALREADY_EXISTS, HTTP_STATUS.CONFLICT);
        }

        // Hash de contraseña
        const passwordHash = await this.hashPassword(password);

        // Crear usuario
        const user = await userRepository.createUser({
            firstName,
            lastName,
            dni,
            email: registrationToken.email,
            passwordHash,
            role: ROLES.CANDIDATE
        });

        // Marcar token como usado
        await tokenRepository.markTokenAsUsed(token);

        logger.info('Usuario registrado exitosamente', { userId: user.id });

        // Generar JWT
        const jwtToken = this.generateToken(user, JWT_CONFIG.CANDIDATE_EXPIRY);

        return {
            success: true,
            message: 'Registro completado exitosamente',
            token: jwtToken,
            user: {
                id: user.id,
                email: user.email,
                firstName: user.firstName,
                lastName: user.lastName,
                role: user.role
            }
        };
    }

    // Login de candidato
    async login(credentials) {
        const { email, password } = credentials;

        logger.info('Intento de login de candidato', { email });

        // Buscar usuario
        const user = await userRepository.findByEmail(email);

        if (!user) {
            throw new AppError(ERROR_MESSAGES.INVALID_CREDENTIALS, HTTP_STATUS.UNAUTHORIZED);
        }

        // Verificar que es candidato
        if (user.role !== ROLES.CANDIDATE) {
            throw new AppError(
                'Acceso denegado: Esta cuenta requiere el portal de administrador',
                HTTP_STATUS.FORBIDDEN
            );
        }

        // Verificar contraseña
        const isPasswordValid = await this.comparePassword(password, user.passwordHash);

        if (!isPasswordValid) {
            throw new AppError(ERROR_MESSAGES.INVALID_CREDENTIALS, HTTP_STATUS.UNAUTHORIZED);
        }

        logger.info('Login exitoso', { userId: user.id });

        // Generar JWT
        const token = this.generateToken(user, JWT_CONFIG.CANDIDATE_EXPIRY);

        return {
            success: true,
            message: 'Login exitoso',
            token,
            user: {
                id: user.id,
                email: user.email,
                firstName: user.firstName,
                lastName: user.lastName,
                role: user.role
            }
        };
    }

    // Login de administrador
    async loginAdmin(credentials) {
        const { email, password } = credentials;

        logger.info('Intento de login de administrador', { email });

        const user = await userRepository.findByEmail(email);

        if (!user || user.role !== ROLES.ADMIN) {
            throw new AppError(
                'El usuario no existe o no tiene permisos de administrador',
                HTTP_STATUS.UNAUTHORIZED
            );
        }

        const isPasswordValid = await this.comparePassword(password, user.passwordHash);

        if (!isPasswordValid) {
            throw new AppError('Contraseña incorrecta', HTTP_STATUS.UNAUTHORIZED);
        }

        logger.info('Login de administrador exitoso', { userId: user.id });

        const token = this.generateToken(user, JWT_CONFIG.ADMIN_EXPIRY);

        return {
            success: true,
            message: 'Login de administrador exitoso',
            token,
            user: {
                id: user.id,
                email: user.email,
                firstName: user.firstName,
                lastName: user.lastName,
                role: user.role
            }
        };
    }

    // Verificar token de registro
    async verifyRegistrationToken(token) {
        const registrationToken = await tokenRepository.findValidToken(token);

        if (!registrationToken) {
            return {
                valid: false,
                email: null
            };
        }

        return {
            valid: true,
            email: registrationToken.email
        };
    }

    // Generar token de registro
    async generateRegistrationToken(email, type = 'valid') {
        logger.info('Generando token de registro', { email, type });

        // Verificar si el email ya tiene usuario
        const existingUser = await userRepository.findByEmail(email);

        if (existingUser) {
            throw new AppError('Ya existe un usuario con este correo electrónico', HTTP_STATUS.CONFLICT);
        }

        // Generar token aleatorio
        const token = crypto.randomBytes(32).toString('hex');

        // Calcular fecha de expiración
        const expiresAt = new Date();
        if (type === 'valid') {
            expiresAt.setHours(expiresAt.getHours() + 24); // 24 horas
        } else {
            expiresAt.setHours(expiresAt.getHours() - 1); // Expirado (para testing)
        }

        // Guardar token
        await tokenRepository.createToken({
            token,
            email,
            expiresAt
        });

        logger.info('Token de registro generado', { email, token });

        return token;
    }
}

module.exports = new AuthService();
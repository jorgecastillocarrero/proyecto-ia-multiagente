// src/services/adminService.js
const userRepository = require('../repositories/userRepository');
const authService = require('./authService');
const logger = require('../utils/logger');

class AdminService {
    async getAllCandidates() {
        logger.info('Getting all candidates');

        const candidates = await userRepository.getAllCandidates();

        return {
            success: true,
            data: candidates
        };
    }

    async generateRegistrationLink(email, frontendUrl, type = 'valid') {
        logger.info('Generating registration link', { email, type });

        const token = await authService.generateRegistrationToken(email, type);
        const link = `${frontendUrl}#/register?token=${token}`;

        return {
            success: true,
            link,
            token
        };
    }
}

module.exports = new AdminService();
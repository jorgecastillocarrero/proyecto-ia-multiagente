// src/services/formService.js
const formRepository = require('../repositories/formRepository');
const userRepository = require('../repositories/userRepository');
const { AppError } = require('../middlewares/errorHandler');
const { HTTP_STATUS } = require('../utils/constants');
const logger = require('../utils/logger');

class FormService {
    async getFormData(userId) {
        logger.info('Getting form data', { userId });

        const formData = await formRepository.findByUserId(userId);

        if (!formData) {
            return {
                success: true,
                data: null
            };
        }

        return {
            success: true,
            data: {
                phone: formData.phone,
                address: formData.address,
                city: formData.city,
                postalCode: formData.postal_code,
                hasCar: !!formData.has_car,
                canTravel: !!formData.can_travel,
                previousWorkExp: !!formData.previous_work_exp,
                retailExp: !!formData.retail_exp,
                experienceSummary: formData.experience_summary
            }
        };
    }

    async saveFormData(userId, formData) {
        logger.info('Saving form data', { userId });

        // Validar campos obligatorios
        const { phone, address, city, experienceSummary } = formData;

        if (!phone || !address || !city || !experienceSummary) {
            throw new AppError('Missing required fields', HTTP_STATUS.BAD_REQUEST);
        }

        // Guardar o actualizar datos
        await formRepository.createOrUpdateForm(userId, {
            phone,
            address,
            city,
            postalCode: formData.postalCode,
            hasCar: formData.hasCar,
            canTravel: formData.canTravel,
            previousWorkExp: formData.previousWorkExp,
            retailExp: formData.retailExp,
            experienceSummary
        });

        // Actualizar flag del usuario
        await userRepository.updateProgressFlags(userId, { form_completed: true });

        logger.info('Form data saved successfully', { userId });

        return {
            success: true,
            message: 'Form saved successfully'
        };
    }
}

module.exports = new FormService();
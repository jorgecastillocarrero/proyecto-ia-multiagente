// src/repositories/formRepository.js
const BaseRepository = require('./BaseRepository');
const { dbPool } = require('../config/database');

class FormRepository extends BaseRepository {
    constructor() {
        super('user_form_data');
    }

    async findByUserId(userId) {
        return await this.findOne({ user_id: userId });
    }

    async hasForm(userId) {
        const form = await this.findByUserId(userId);
        return form !== null;
    }

    async createOrUpdateForm(userId, formData) {
        const existing = await this.findByUserId(userId);

        if (existing) {
            // Update
            const query = `
        UPDATE ${this.tableName} 
        SET phone = ?, address = ?, city = ?, postal_code = ?,
            has_car = ?, can_travel = ?, previous_work_exp = ?, 
            retail_exp = ?, experience_summary = ?,
            updatedAt = CURRENT_TIMESTAMP
        WHERE user_id = ?
      `;
            const [result] = await dbPool.query(query, [
                formData.phone,
                formData.address,
                formData.city,
                formData.postalCode || null,
                formData.hasCar ? 1 : 0,
                formData.canTravel ? 1 : 0,
                formData.previousWorkExp ? 1 : 0,
                formData.retailExp ? 1 : 0,
                formData.experienceSummary,
                userId
            ]);
            return result.affectedRows > 0;
        } else {
            // Create
            return await this.create({
                user_id: userId,
                phone: formData.phone,
                address: formData.address,
                city: formData.city,
                postal_code: formData.postalCode || null,
                has_car: formData.hasCar ? 1 : 0,
                can_travel: formData.canTravel ? 1 : 0,
                previous_work_exp: formData.previousWorkExp ? 1 : 0,
                retail_exp: formData.retailExp ? 1 : 0,
                experience_summary: formData.experienceSummary
            });
        }
    }
}

module.exports = new FormRepository();
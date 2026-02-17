// src/repositories/examRepository.js
const BaseRepository = require('./BaseRepository');
const { dbPool } = require('../config/database');

class ExamRepository extends BaseRepository {
    constructor() {
        super('exams');
    }

    async findByUserId(userId) {
        const query = `
      SELECT * FROM ${this.tableName} 
      WHERE user_id = ? 
      ORDER BY created_at DESC 
      LIMIT 1
    `;
        const [rows] = await dbPool.query(query, [userId]);
        return rows[0] || null;
    }

    async hasExam(userId) {
        const count = await this.count({ user_id: userId });
        return count > 0;
    }

    async createExam(examData) {
        const percentage = (examData.score / examData.total) * 100;

        return await this.create({
            user_id: examData.userId,
            score: examData.score,
            total_questions: examData.total,
            passed: examData.passed,
            percentage: percentage.toFixed(2),
            time_taken: examData.timeTaken || null
        });
    }
}

module.exports = new ExamRepository();
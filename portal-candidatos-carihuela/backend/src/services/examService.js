// src/services/examService.js
const examRepository = require('../repositories/examRepository');
const documentRepository = require('../repositories/documentRepository');
const formRepository = require('../repositories/formRepository');
const userRepository = require('../repositories/userRepository');
const logger = require('../utils/logger');

class ExamService {
    async getExamStatus(userId) {
        logger.info('Getting exam status', { userId });

        // Verificar estado del examen
        const exam = await examRepository.findByUserId(userId);

        // Verificar documentos
        const hasDocuments = await documentRepository.hasDocuments(userId);

        // Verificar formulario
        const hasForm = await formRepository.hasForm(userId);

        let examStatus = 'not_taken';
        if (exam) {
            examStatus = exam.passed ? 'passed' : 'failed';
        }

        return {
            status: examStatus,
            documentsUploaded: hasDocuments,
            formCompleted: hasForm,
            examData: exam || null
        };
    }

    async submitExam(userId, examData) {
        const { score, total, passed, timeTaken } = examData;

        logger.info('Submitting exam', { userId, score, total, passed });

        // Crear registro del examen
        const exam = await examRepository.createExam({
            userId,
            score,
            total,
            passed,
            timeTaken
        });

        // Actualizar flag del usuario
        await userRepository.updateProgressFlags(userId, { exam_completed: true });

        logger.info('Exam submitted successfully', { userId, examId: exam.id });

        return {
            success: true,
            message: 'Exam submitted successfully',
            exam
        };
    }
}

module.exports = new ExamService();
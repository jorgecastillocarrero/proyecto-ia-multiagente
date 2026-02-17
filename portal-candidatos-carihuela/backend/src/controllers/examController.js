const examService = require('../services/examService');
const { asyncHandler } = require('../middlewares/errorHandler');

// GET /api/exam/status
const getExamStatus = asyncHandler(async (req, res) => {
    const userId = req.user.id;
    const result = await examService.getExamStatus(userId);
    res.json(result);
});

// POST /api/exam/submit
const submitExam = asyncHandler(async (req, res) => {
    const userId = req.user.id;
    const { score, total, passed, timeTaken } = req.body;

    const result = await examService.submitExam(userId, {
        score,
        total,
        passed,
        timeTaken
    });

    res.status(201).json(result);
});

module.exports = {
    getExamStatus,
    submitExam
};
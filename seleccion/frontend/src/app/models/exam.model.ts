// src/app/models/exam.model.ts
export interface Question {
    id: number;
    text: string;
    options: string[];
    correctAnswer: number;
}

export interface ExamStatus {
    status: 'not_taken' | 'passed' | 'failed';
    documentsUploaded: boolean;
    formCompleted: boolean;
    examData?: {
        score: number;
        total_questions: number;
        passed: boolean;
        percentage: number;
    };
}

export interface ExamSubmission {
    score: number;
    total: number;
    passed: boolean;
    timeTaken?: number;
}
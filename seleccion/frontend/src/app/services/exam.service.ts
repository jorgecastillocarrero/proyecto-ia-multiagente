// src/app/services/exam.service.ts
import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export type ExamStatus = 'passed' | 'failed' | 'not_taken';

export interface ExamResult {
    score: number;
    total: number;
    passed: boolean;
}

export interface ExamStatusResponse {
    status: ExamStatus;
    documentsUploaded?: boolean;
    formCompleted?: boolean;
}

const API_URL = environment.API_URL;

@Injectable({
    providedIn: 'root',
})
export class ExamService {
    private http = inject(HttpClient);

    // Método principal que usa documents
    getExamStatus(): Observable<ExamStatusResponse> {
        return this.http.get<ExamStatusResponse>(`${API_URL}/exam/status`);
    }

    // Método alternativo (mantener compatibilidad)
    getExamStatusFromServer(): Observable<ExamStatusResponse> {
        return this.getExamStatus();
    }

    submitExam(result: ExamResult): Observable<{ success: boolean }> {
        return this.http.post<{ success: boolean }>(`${API_URL}/exam/submit`, result);
    }

    /**
     * Defines the passing score for the exam.
     * @param totalQuestions The total number of questions in the exam.
     * @returns The minimum number of correct answers to pass.
     */
    getPassingScore(totalQuestions: number): number {
        // Passing threshold is 60%
        return Math.ceil(totalQuestions * 0.6);
    }
}
// src/app/components/exam/exam.component.ts
import { ChangeDetectionStrategy, Component, computed, inject, OnDestroy, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { LanguageService } from '../../services/language.service';
import { ALL_QUESTIONS, Question } from '../../data/questions';
import { ExamService, ExamResult } from '../../services/exam.service';
import { LoadingSpinnerComponent } from '../loading-spinner/loading-spinner.component';

type ExamComponentState = 'loading' | 'not_started' | 'in_progress' | 'finished' | 'already_passed';

interface Answer {
    questionId: number;
    selectedAnswer: string;
    correctAnswer: string;
    isCorrect: boolean;
}

const EXAM_QUESTION_COUNT = 5;
const SECONDS_PER_QUESTION = 10;

@Component({
    selector: 'app-exam',
    standalone: true,
    imports: [CommonModule, LoadingSpinnerComponent],
    templateUrl: './exam.component.html',
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ExamComponent implements OnInit, OnDestroy {
    languageService = inject(LanguageService);
    examService = inject(ExamService);
    router = inject(Router);
    t = this.languageService.translations;

    examState = signal<ExamComponentState>('loading');
    questions = signal<Question[]>([]);
    answers = signal<Answer[]>([]);
    currentQuestionIndex = signal(0);
    examResult = signal<ExamResult | null>(null);

    timer = signal(SECONDS_PER_QUESTION);
    private timerInterval: any;

    currentQuestion = computed(() => this.questions()[this.currentQuestionIndex()]);

    progress = computed(() => ((this.currentQuestionIndex() + 1) / this.questions().length) * 100);

    examConstants = {
        count: EXAM_QUESTION_COUNT,
        seconds: SECONDS_PER_QUESTION,
    };

    ngOnInit(): void {
        this.examService.getExamStatus().subscribe({
            next: ({ status }) => {
                if (status === 'passed') {
                    this.examState.set('already_passed');
                } else {
                    this.examState.set('not_started');
                }
            },
            error: () => {
                this.examState.set('not_started');
            }
        });
    }

    ngOnDestroy(): void {
        clearInterval(this.timerInterval);
    }

    startExam(): void {
        this.questions.set(this.getRandomQuestions());
        this.answers.set([]);
        this.currentQuestionIndex.set(0);
        this.examResult.set(null);
        this.examState.set('in_progress');
        this.startTimer();
    }

    private getRandomQuestions(): Question[] {
        const shuffled = [...ALL_QUESTIONS].sort(() => 0.5 - Math.random());
        return shuffled.slice(0, EXAM_QUESTION_COUNT);
    }

    selectAnswer(selectedOption: string): void {
        if (this.timerInterval === null) return;

        clearInterval(this.timerInterval);
        this.timerInterval = null;

        const currentQ = this.currentQuestion();
        const answer: Answer = {
            questionId: currentQ.id,
            selectedAnswer: selectedOption,
            correctAnswer: currentQ.correctAnswer,
            isCorrect: selectedOption === currentQ.correctAnswer,
        };
        this.answers.update(answers => [...answers, answer]);

        setTimeout(() => this.nextQuestion(), 500);
    }

    private nextQuestion(): void {
        if (this.currentQuestionIndex() < this.questions().length - 1) {
            this.currentQuestionIndex.update(i => i + 1);
            this.startTimer();
        } else {
            this.finishExam();
        }
    }

    private finishExam(): void {
        const finalScore = this.answers().filter(a => a.isCorrect).length;
        const totalQuestions = this.questions().length;
        const passingScore = this.examService.getPassingScore(totalQuestions);
        const passed = finalScore >= passingScore;

        const result: ExamResult = {
            score: finalScore,
            total: totalQuestions,
            passed: passed,
        };

        this.examResult.set(result);
        this.examState.set('loading');

        this.examService.submitExam(result).subscribe({
            next: () => {
                this.examState.set('finished');
            },
            error: () => {
                this.examState.set('finished');
            }
        });
    }

    private startTimer(): void {
        this.timer.set(SECONDS_PER_QUESTION);
        clearInterval(this.timerInterval);
        this.timerInterval = setInterval(() => {
            this.timer.update(t => t - 1);
            if (this.timer() === 0) {
                this.selectAnswer('');
            }
        }, 1000);
    }

    navigateToDocuments(): void {
        this.router.navigate(['/documents']);
    }
}
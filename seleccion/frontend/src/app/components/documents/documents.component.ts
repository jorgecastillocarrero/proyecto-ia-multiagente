// src/app/components/documents/documents.component.ts
import { ChangeDetectionStrategy, Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { LanguageService } from '../../services/language.service';
import { LoadingSpinnerComponent } from '../loading-spinner/loading-spinner.component';
import { FileInputComponent } from '../file-input/file-input.component';
import { ProfileDropdownComponent } from '../profile-dropdown/profile-dropdown.component';
import { ExamService } from '../../services/exam.service';
import { DocumentService } from '../../services/document.service';

// Tipo para el estado del examen
export type ExamStatus = 'not_taken' | 'passed' | 'failed';

@Component({
    selector: 'app-documents',
    standalone: true,
    imports: [
        CommonModule,
        ReactiveFormsModule,
        RouterLink,
        LoadingSpinnerComponent,
        FileInputComponent,
        ProfileDropdownComponent
    ],
    templateUrl: './documents.component.html',
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DocumentsComponent implements OnInit {
    private fb = inject(FormBuilder);
    private router = inject(Router);
    private authService = inject(AuthService);
    private examService = inject(ExamService);
    private documentService = inject(DocumentService);
    languageService = inject(LanguageService);

    // Signals - TODOS los que necesita el HTML
    isLoading = signal(true);
    examStatus = signal<ExamStatus>('not_taken');
    documentsUploaded = signal(false);
    formCompleted = signal(false);

    t = this.languageService.translations;
    documentsForm: FormGroup;

    constructor() {
        this.documentsForm = this.fb.group({
            dniCopy: [null, Validators.required],
            youthGuarantee: [null],
            jobSeeker: [null, Validators.required],
            degreeCopy: [null, Validators.required],
            foodHandlerCertificate: [null, Validators.required],
        });
    }

    ngOnInit(): void {
        this.checkStatus();
    }

    private checkStatus(): void {
        this.isLoading.set(true);
        this.examService.getExamStatus().subscribe({
            next: (res: any) => {
                // Asignar estados
                this.examStatus.set(res.status || 'not_taken');
                this.documentsUploaded.set(!!res.documentsUploaded);
                this.formCompleted.set(!!res.formCompleted);

                // Habilitar/Deshabilitar formulario
                if (this.documentsUploaded() || this.examStatus() !== 'passed') {
                    this.documentsForm.disable();
                } else {
                    this.documentsForm.enable();
                }
                this.isLoading.set(false);
            },
            error: () => this.isLoading.set(false)
        });
    }

    // Métodos de navegación - TODOS los que necesita el HTML
    navigateToForm(): void {
        this.router.navigate(['/form']);
    }

    navigateToExam(): void {
        if (this.examStatus() !== 'passed') {
            this.router.navigate(['/exam']);
        }
    }

    navigateToPrivacyPolicy(): void {
        this.router.navigate(['/privacy-policy']);
    }

    logout(): void {
        this.authService.logout();
        this.router.navigate(['/login']);
    }

    // Getters para los form controls - TODOS los que necesita el HTML
    get dniCopy() {
        return this.documentsForm.get('dniCopy');
    }

    get jobSeeker() {
        return this.documentsForm.get('jobSeeker');
    }

    get degreeCopy() {
        return this.documentsForm.get('degreeCopy');
    }

    get foodHandlerCertificate() {
        return this.documentsForm.get('foodHandlerCertificate');
    }

    // Método para enviar documentos
    // En documents.component.ts
    // REEMPLAZAR el método onSubmit()

    onSubmit() {
        if (this.documentsForm.invalid) {
            this.documentsForm.markAllAsTouched();
            return;
        }

        this.isLoading.set(true);
        const formData = new FormData();

        const allowedFields = [
            'dniCopy',
            'jobSeeker',
            'degreeCopy',
            'foodHandlerCertificate',
            'youthGuarantee'
        ];

        allowedFields.forEach(fieldName => {
            const file = this.documentsForm.get(fieldName)?.value;
            if (file) {
                formData.append(fieldName, file);
            }
        });

        this.authService.uploadDocuments(formData).subscribe({
            next: (res) => {
                if (res.success) {
                    this.documentsUploaded.set(true);
                    this.documentsForm.disable();
                }
                this.isLoading.set(false);
            },
            error: (err) => {
                console.error('Error uploading documents:', err);
                this.isLoading.set(false);
            }
        });
    }
}
// src/app/components/form/form.component.ts
import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { LanguageService } from '../../services/language.service';
import { LoadingSpinnerComponent } from '../loading-spinner/loading-spinner.component';

@Component({
    selector: 'app-form',
    standalone: true,
    imports: [CommonModule, ReactiveFormsModule, LoadingSpinnerComponent],
    templateUrl: './form.component.html'
})
export class FormComponent implements OnInit {
    private fb = inject(FormBuilder);
    private router = inject(Router);
    private authService = inject(AuthService);
    private languageService = inject(LanguageService);

    isLoading = signal(true);
    isSubmitting = signal(false);
    errorMessage = signal<string | null>(null);

    t = this.languageService.translations;
    registrationForm: FormGroup;

    get f() { return this.registrationForm.controls; }

    constructor() {
        this.registrationForm = this.fb.group({
            // Campos de Texto (Obligatorios)
            phone: ['', [Validators.required, Validators.pattern(/^[6789]{1}[0-9]{8}$/)]],
            city: ['', [Validators.required]],
            address: ['', [Validators.required, Validators.minLength(5)]],
            experience_summary: ['', [Validators.required, Validators.minLength(20)]],

            // Campos Booleanos (Radio Buttons o Checkbox)
            has_car: [false, Validators.required],
            can_travel: [false, Validators.required],
            previous_work_exp: [false, Validators.required],
            retail_exp: [false, Validators.required],
            termsAccepted: [false, Validators.requiredTrue]
        });
    }

    ngOnInit(): void {
        this.loadExistingData();
    }

    private loadExistingData(): void {
        this.isLoading.set(true);
        this.authService.getFormData().subscribe({
            next: (data: any) => {
                if (data) {
                    this.registrationForm.patchValue({
                        phone: data.phone,
                        city: data.city,
                        address: data.address,
                        experience_summary: data.experienceSummary,
                        has_car: !!data.hasCar,
                        can_travel: !!data.canTravel,
                        previous_work_exp: !!data.previousWorkExp,
                        retail_exp: !!data.retailExp,
                        termsAccepted: true
                    });
                }
                this.isLoading.set(false);
            },
            error: (err: any) => {
                console.log('No hay datos previos', err);
                this.isLoading.set(false);
            }
        });
    }

    onSubmit(): void {
        if (this.registrationForm.invalid) {
            this.registrationForm.markAllAsTouched();
            this.errorMessage.set('Por favor, completa todos los campos obligatorios.');
            return;
        }

        this.isSubmitting.set(true);

        const formValue = this.registrationForm.value;

        const formData = {
            phone: formValue.phone,
            address: formValue.address,
            city: formValue.city,
            experienceSummary: formValue.experience_summary, 
            hasCar: formValue.has_car,                        
            canTravel: formValue.can_travel,
            previousWorkExp: formValue.previous_work_exp,
            retailExp: formValue.retail_exp    
        };

        this.authService.saveFormData(formData).subscribe({
            next: () => {
                this.isSubmitting.set(false);
                this.router.navigate(['/documents']);
            },
            error: (err: any) => {
                this.isSubmitting.set(false);
                this.errorMessage.set('Error al guardar. Inténtalo de nuevo.');
                console.error(err);
            }
        });
    }

    goBack(): void {
        this.router.navigate(['/documents']);
    }
}
// src/app/components/register/register.component.ts
import { Component, inject, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators, AbstractControl } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { LanguageService } from '../../services/language.service';
import { LoadingSpinnerComponent } from '../loading-spinner/loading-spinner.component';
import { LanguageSwitcherComponent } from '../language-switcher/language-switcher.component';
import { CustomValidators } from '../../utils/validators';

@Component({
    selector: 'app-register',
    standalone: true,
    imports: [
        CommonModule,
        ReactiveFormsModule,
        LoadingSpinnerComponent,
        LanguageSwitcherComponent
    ],
    templateUrl: './register.component.html'
})
export class RegisterComponent implements OnInit {
    private fb = inject(FormBuilder);
    private router = inject(Router);
    private route = inject(ActivatedRoute);
    private authService = inject(AuthService);
    languageService = inject(LanguageService);

    isLoading = signal(false);
    errorMessage = signal<string | null>(null);
    t = this.languageService.translations;

    registrationForm: FormGroup;
    token: string = '';
    email: string = '';
    candidatoData: any = null; // ← AÑADIDO: Datos del candidato RRHH si existe

    constructor() {
        this.registrationForm = this.fb.group({
            firstName: ['', [Validators.required, Validators.minLength(2)]],
            lastName: ['', [Validators.required, Validators.minLength(2)]],
            dni: ['', [Validators.required, CustomValidators.dni()]],
            email: [{ value: '', disabled: true }],
            password: ['', [Validators.required, CustomValidators.strongPassword()]],
            confirmPassword: ['', [Validators.required]],
            privacyPolicy: [false, [Validators.requiredTrue]]
        }, {
            validators: this.passwordMatchValidator
        });
    }

    ngOnInit() {
        // Obtener token de query params
        this.route.queryParams.subscribe(params => {
            this.token = params['token'] || '';
        });

        // Obtener datos del resolver (tokenData y candidateData)
        this.route.data.subscribe(data => {
            const tokenData = data['tokenData'];
            const candidateData = data['candidateData'];

            // Verificar token válido
            if (tokenData && tokenData.valid && tokenData.email) {
                this.email = tokenData.email;

                // Establecer el email en el formulario
                this.registrationForm.patchValue({
                    email: tokenData.email
                });

                // ← AÑADIDO: Si existe candidato RRHH, pre-rellenar datos
                if (candidateData) {
                    this.candidatoData = candidateData;

                    // Pre-rellenar nombre y apellidos del CV
                    this.registrationForm.patchValue({
                        firstName: candidateData.firstName || '',
                        lastName: candidateData.lastName || ''
                    });

                    // Deshabilitar campos pre-rellenados
                    if (candidateData.firstName) {
                        this.registrationForm.get('firstName')?.disable();
                    }
                    if (candidateData.lastName) {
                        this.registrationForm.get('lastName')?.disable();
                    }
                }
            } else {
                console.error('No valid email in token data');
                this.router.navigate(['/login']);
            }
        });
    }

    passwordMatchValidator(control: AbstractControl) {
        const password = control.get('password');
        const confirmPassword = control.get('confirmPassword');

        if (!password || !confirmPassword) {
            return null;
        }

        return password.value === confirmPassword.value ? null : { passwordMismatch: true };
    }

    // Getters para el HTML
    get firstName() { return this.registrationForm.get('firstName'); }
    get lastName() { return this.registrationForm.get('lastName'); }
    get dni() { return this.registrationForm.get('dni'); }
    get password() { return this.registrationForm.get('password'); }
    get confirmPassword() { return this.registrationForm.get('confirmPassword'); }
    get privacyPolicy() { return this.registrationForm.get('privacyPolicy'); }

    onSubmit(): void {
        if (this.registrationForm.invalid) {
            this.registrationForm.markAllAsTouched();
            return;
        }

        this.isLoading.set(true);
        this.errorMessage.set(null);

        // ← MODIFICADO: Usar getRawValue() para incluir campos deshabilitados
        const formValue = this.registrationForm.getRawValue();

        const registrationData = {
            token: this.token,
            firstName: formValue.firstName,
            lastName: formValue.lastName,
            dni: formValue.dni,
            password: formValue.password
        };

        this.authService.completeRegistration(registrationData).subscribe({
            next: (response) => {
                if (response.success) {
                    this.router.navigate(['/success']);
                } else {
                    this.errorMessage.set(this.t().register.errors.generic);
                }
                this.isLoading.set(false);
            },
            error: (err) => {
                this.isLoading.set(false);
                console.error('Registration error:', err);

                if (err.status === 409) {
                    this.errorMessage.set('Ya existe un usuario con este email o DNI');
                } else if (err.status === 400) {
                    this.errorMessage.set(this.t().register.errors.generic);
                } else {
                    this.errorMessage.set(this.t().register.errors.generic);
                }
            }
        });
    }
}
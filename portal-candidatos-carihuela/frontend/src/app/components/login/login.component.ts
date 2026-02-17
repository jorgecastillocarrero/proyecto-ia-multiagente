// src/app/components/login/login.component.ts
import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { LanguageService } from '../../services/language.service';
import { LoadingSpinnerComponent } from '../loading-spinner/loading-spinner.component';
import { LanguageSwitcherComponent } from '../language-switcher/language-switcher.component';

@Component({
    selector: 'app-login',
    standalone: true,
    imports: [
        CommonModule,
        ReactiveFormsModule,
        LoadingSpinnerComponent,
        LanguageSwitcherComponent
    ],
    templateUrl: './login.component.html'
})
export class LoginComponent {
    private fb = inject(FormBuilder);
    private router = inject(Router);
    private authService = inject(AuthService);
    languageService = inject(LanguageService);

    isLoading = signal(false);
    errorMessage = signal<string | null>(null);
    t = this.languageService.translations;

    loginForm: FormGroup;

    constructor() {
        this.loginForm = this.fb.group({
            email: ['', [Validators.required, Validators.email]],
            password: ['', [Validators.required]]
        });
    }

    get email() {
        return this.loginForm.get('email');
    }

    get password() {
        return this.loginForm.get('password');
    }

    onSubmit(): void {
        if (this.loginForm.invalid) {
            this.loginForm.markAllAsTouched();
            return;
        }

        this.isLoading.set(true);
        this.errorMessage.set(null);

        this.authService.login(this.loginForm.value).subscribe({
            next: (response) => {
                if (response.success) {
                    this.router.navigate(['/documents']);
                } else {
                    this.errorMessage.set(this.t().login.errors.generic);
                }
                this.isLoading.set(false);
            },
            error: (err) => {
                this.isLoading.set(false);

                if (err.status === 403) {
                    const serverMsg = err.error?.error?.message || 'Acceso denegado: Use el portal de administración.';
                    this.router.navigate(['/access-denied'], {
                        state: { errorMsg: serverMsg }
                    });
                } else if (err.status === 401) {
                    this.errorMessage.set(this.t().login.errors.invalidCredentials);
                } else {
                    this.errorMessage.set(this.t().login.errors.generic);
                }
            }
        });
    }
}
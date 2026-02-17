// src/app/components/admin-auth/admin-auth.component.ts
import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AdminAuthService } from '../../services/admin-auth.service';
import { LanguageService } from '../../services/language.service';
import { LoadingSpinnerComponent } from '../loading-spinner/loading-spinner.component';
import { LanguageSwitcherComponent } from '../language-switcher/language-switcher.component';

@Component({
  selector: 'app-admin-auth',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    LoadingSpinnerComponent,
    LanguageSwitcherComponent,
  ],
  templateUrl: './admin-auth.component.html',

})
export class AdminAuthComponent {
  private fb = inject(FormBuilder);
  private router = inject(Router);
  private adminAuthService = inject(AdminAuthService);
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

  // Getters para los controles del formulario
  get emailControl() {
    return this.loginForm.get('email');
  }

  get passwordControl() {
    return this.loginForm.get('password');
  }

  onSubmit() {
    if (this.loginForm.invalid) return;

    this.isLoading.set(true);
    this.errorMessage.set(null);

    this.adminAuthService.login(this.loginForm.value).subscribe({
      next: (response) => {
        if (response.success) {
          this.router.navigate(['/admin']);
        }
        this.isLoading.set(false);
      },
      error: (err) => {
        this.isLoading.set(false);
        this.errorMessage.set(err.error?.error?.message || this.t().adminAuth.errors.generic);
      }
    });
  }
}
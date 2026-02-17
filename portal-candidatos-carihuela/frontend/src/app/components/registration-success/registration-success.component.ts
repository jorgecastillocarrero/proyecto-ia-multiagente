// src/app/components/registration-success/registration-success.component.ts
import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
    selector: 'app-registration-success',
    standalone: true,
    imports: [CommonModule],
    template: `
    <div class="flex items-center justify-center min-h-screen bg-slate-100 p-4">
      <div class="w-full max-w-md bg-white p-12 rounded-lg shadow-xl text-center">
        <div class="mb-6">
          <svg class="mx-auto h-24 w-24 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>

        <h1 class="text-3xl font-bold text-slate-800 mb-4">¡Registro Completado!</h1>
        
        <p class="text-slate-600 mb-8">
          Tu cuenta ha sido creada exitosamente. Ya puedes comenzar con el proceso de candidatura.
        </p>

        <button
          (click)="goToDashboard()"
          class="w-full px-6 py-3 bg-carihuela-blue text-white rounded-md hover:bg-carihuela-dark transition-colors font-medium">
          Ir al Panel
        </button>
      </div>
    </div>
  `
})
export class RegistrationSuccessComponent {
    private router = inject(Router);

    goToDashboard() {
        this.router.navigate(['/documents']);
    }
}
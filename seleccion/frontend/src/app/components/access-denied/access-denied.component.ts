import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { LanguageService } from '../../services/language.service';


@Component({
    selector: 'app-access-denied',
    standalone: true,
    imports: [CommonModule],
    template: `
    <div class="flex items-center justify-center min-h-screen bg-slate-100 p-4">
      <div class="w-full max-w-md text-center bg-white p-8 rounded-lg shadow-lg border-t-4 border-red-600">
        <img src="/assets/img/logo-carihuela.png" alt="Logo" class="h-16 w-auto mx-auto mb-4">

        <h1 class="text-3xl font-bold text-slate-800">
          {{ t().accessDenied.title }}
        </h1>

        <p class="text-slate-600 mt-4 text-lg">
          {{ errorMessage }}
        </p>

        <p class="text-slate-500 mt-2 italic">
          {{ t().accessDenied.contact }}
        </p>

        <button (click)="goBack()"
          class="mt-6 px-6 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors uppercase font-bold text-sm">
          Volver al inicio
        </button>
      </div>
    </div>
    `
})
export class AccessDeniedComponent {
    private router = inject(Router);
    errorMessage: string = '';
  languageService = inject(LanguageService);


  t = this.languageService.translations;


    constructor() {
        const navigation = this.router.getCurrentNavigation();
        this.errorMessage = navigation?.extras?.state?.['serverError'] || '';
    }

    goBack() {
        this.router.navigate(['/login']);
    }
}
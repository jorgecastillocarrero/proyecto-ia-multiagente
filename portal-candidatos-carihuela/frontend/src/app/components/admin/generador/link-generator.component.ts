// src/app/components/admin/generador/link-generator.component.ts
import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { catchError, of } from 'rxjs';
import { environment } from '../../../../environments/environment';

const API_URL = environment.API_URL;

@Component({
    selector: 'app-link-generator',
    standalone: true,
    imports: [CommonModule, ReactiveFormsModule],
    template: `
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6 md:p-8 max-w-2xl">
            <h2 class="text-xl md:text-2xl font-bold text-slate-900 mb-6">Generar Enlace de Registro</h2>

            <form [formGroup]="generatorForm" (ngSubmit)="generateLink()">
                <div class="mb-6">
                    <label class="block text-sm font-semibold text-slate-700 mb-2">
                        Email del Candidato
                    </label>
                    <input type="email" 
                        formControlName="email" 
                        placeholder="candidato@ejemplo.com"
                        class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-[#003366] focus:border-transparent">
                    
                    @if (generatorForm.get('email')?.invalid && generatorForm.get('email')?.touched) {
                    <p class="mt-2 text-sm text-red-600">
                        Por favor, introduce un email válido
                    </p>
                    }
                </div>

                <div class="flex gap-3">
                    <button type="submit" 
                        [disabled]="generatorForm.invalid || isGenerating()"
                        class="px-6 py-2.5 bg-[#003366] text-white rounded-lg hover:bg-[#002244] transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2">
                        @if (isGenerating()) {
                        <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        <span>Generando...</span>
                        } @else {
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1">
                            </path>
                        </svg>
                        <span>Generar Enlace</span>
                        }
                    </button>

                    @if (generatedLink()) {
                    <button type="button"
                        (click)="resetForm()"
                        class="px-4 py-2.5 text-slate-700 bg-slate-100 rounded-lg hover:bg-slate-200 transition-colors font-medium">
                        Nuevo
                    </button>
                    }
                </div>
            </form>

            <!-- Link Generado -->
            @if (generatedLink()) {
            <div class="mt-6 p-4 bg-emerald-50 border border-emerald-200 rounded-lg">
                <p class="text-sm font-semibold text-emerald-900 mb-3 flex items-center gap-2">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    Enlace generado correctamente
                </p>
                <div class="flex flex-col sm:flex-row gap-2">
                    <input type="text" 
                        [value]="generatedLink()" 
                        readonly
                        class="flex-1 px-3 py-2 bg-white border border-emerald-300 rounded-lg text-sm text-slate-700 font-mono">
                    <button (click)="copyToClipboard()"
                        [class.bg-emerald-700]="!copied()"
                        [class.bg-emerald-600]="copied()"
                        class="px-4 py-2 text-white rounded-lg hover:bg-emerald-700 transition-colors font-medium flex items-center justify-center gap-2 whitespace-nowrap">
                        @if (copied()) {
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M5 13l4 4L19 7"></path>
                        </svg>
                        <span>Copiado</span>
                        } @else {
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z">
                            </path>
                        </svg>
                        <span>Copiar</span>
                        }
                    </button>
                </div>
            </div>
            }

            <!-- Error -->
            @if (error()) {
            <div class="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                <p class="text-sm font-semibold text-red-900 mb-1 flex items-center gap-2">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    Error al generar el enlace
                </p>
                <p class="text-sm text-red-700">{{ error() }}</p>
            </div>
            }

            <!-- Información adicional -->
            <div class="mt-6 pt-6 border-t border-slate-200">
                <h3 class="text-sm font-semibold text-slate-700 mb-2">Información</h3>
                <ul class="text-sm text-slate-600 space-y-1">
                    <li class="flex items-start gap-2">
                        <svg class="w-4 h-4 text-slate-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        <span>El enlace es válido durante 7 días</span>
                    </li>
                    <li class="flex items-start gap-2">
                        <svg class="w-4 h-4 text-slate-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        <span>El candidato recibirá un email con el enlace de registro</span>
                    </li>
                    <li class="flex items-start gap-2">
                        <svg class="w-4 h-4 text-slate-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        <span>Cada enlace es de un solo uso</span>
                    </li>
                </ul>
            </div>
        </div>
    `
})
export class LinkGeneratorComponent {
    fb = inject(FormBuilder);
    http = inject(HttpClient);

    generatorForm: FormGroup;
    generatedLink = signal<string | null>(null);
    error = signal<string | null>(null);
    isGenerating = signal(false);
    copied = signal(false);

    private mockApiKey = 'n8n-secret-key-for-demo';

    constructor() {
        this.generatorForm = this.fb.group({
            email: ['', [Validators.required, Validators.email]]
        });
    }

    private getFrontendBaseUrl(): string {
        const { protocol, host } = window.location;
        return `${protocol}//${host}/`;
    }

    generateLink(): void {
        if (this.generatorForm.invalid) {
            this.generatorForm.markAllAsTouched();
            return;
        }

        this.isGenerating.set(true);
        this.error.set(null);
        this.generatedLink.set(null);
        this.copied.set(false);

        const email = this.generatorForm.get('email')?.value;
        const type = 'valid';

        this.http.get<{ success: boolean, link?: string, error?: string }>(
            `${API_URL}/admin/generate-link`,
            {
                params: {
                    email,
                    type,
                    apiKey: this.mockApiKey,
                    frontendUrl: this.getFrontendBaseUrl()
                }
            }
        ).pipe(
            catchError((err: HttpErrorResponse) => {
                let errorMessage = 'Ha ocurrido un error inesperado. Por favor, inténtalo de nuevo.';
                if (err.message.includes('Http failure during parsing')) {
                    errorMessage = 'Error al procesar la respuesta del servidor.';
                } else if (err.error?.error) {
                    errorMessage = err.error.error;
                } else if (err.status === 0) {
                    errorMessage = 'No se pudo conectar con el servidor.';
                } else if (err.status === 404) {
                    errorMessage = 'Servicio no disponible.';
                } else if (err.status === 500) {
                    errorMessage = 'Error interno del servidor.';
                }
                return of({ success: false as const, error: errorMessage });
            })
        ).subscribe(result => {
            this.isGenerating.set(false);

            if (result.success && result.link) {
                this.generatedLink.set(result.link);
            } else {
                this.error.set(result.error || 'Error desconocido');
            }
        });
    }

    copyToClipboard(): void {
        const link = this.generatedLink();
        if (!link) return;

        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(link).then(() => {
                this.copied.set(true);
                setTimeout(() => this.copied.set(false), 2000);
            }).catch(err => {
                console.error('Error al copiar:', err);
                this.fallbackCopy(link);
            });
        } else {
            this.fallbackCopy(link);
        }
    }

    private fallbackCopy(text: string): void {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.left = '-999999px';
        document.body.appendChild(textarea);
        textarea.select();
        try {
            document.execCommand('copy');
            this.copied.set(true);
            setTimeout(() => this.copied.set(false), 2000);
        } catch (err) {
            console.error('Error al copiar (método alternativo):', err);
            this.error.set('No se pudo copiar el enlace. Por favor, cópialo manualmente.');
        }
        document.body.removeChild(textarea);
    }

    resetForm(): void {
        this.generatorForm.reset();
        this.generatedLink.set(null);
        this.error.set(null);
        this.copied.set(false);
    }
}
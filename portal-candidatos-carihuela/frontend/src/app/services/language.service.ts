// src/app/services/language.service.ts
import { Injectable, signal, computed } from '@angular/core';
import { es } from '../../i18n/es';
import { en } from '../../i18n/en';

export type Language = 'es' | 'en'; 
type Translations = typeof es;

@Injectable({
    providedIn: 'root'
})
export class LanguageService {
    private currentLanguage = signal<Language>('es');

    // Computed signal con las traducciones actuales
    translations = computed<Translations>(() => {
        return this.currentLanguage() === 'es' ? es : en;
    });

    constructor() {
        // Cargar idioma del localStorage
        const savedLang = localStorage.getItem('language') as Language;
        if (savedLang) {
            this.currentLanguage.set(savedLang);
        }
    }

    setLanguage(lang: Language) {
        this.currentLanguage.set(lang);
        localStorage.setItem('language', lang);
    }

    getCurrentLanguage() {
        return this.currentLanguage();
    }

    toggleLanguage() {
        const newLang = this.currentLanguage() === 'es' ? 'en' : 'es';
        this.setLanguage(newLang);
    }
}
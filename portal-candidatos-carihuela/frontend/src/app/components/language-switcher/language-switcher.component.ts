// src/app/components/language-switcher/language-switcher.component.ts
import { Component, inject, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LanguageService, Language } from '../../services/language.service';

@Component({
  selector: 'app-language-switcher',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './language-switcher.component.html'
})
export class LanguageSwitcherComponent {
  languageService = inject(LanguageService);
  t = this.languageService.translations;

  currentLanguage = computed(() => this.languageService.getCurrentLanguage());

  setLanguage(lang: Language): void {
    this.languageService.setLanguage(lang);
  }
}
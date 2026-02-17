import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Location } from '@angular/common';
import { LanguageService } from '../../services/language.service';

@Component({
  selector: 'app-privacy-policy',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './privacy-policy.component.html',
})
export class PrivacyPolicyComponent {
  private location = inject(Location);
  languageService = inject(LanguageService);

  t = this.languageService.translations;

  goBack(): void {
    this.location.back();
  }
}
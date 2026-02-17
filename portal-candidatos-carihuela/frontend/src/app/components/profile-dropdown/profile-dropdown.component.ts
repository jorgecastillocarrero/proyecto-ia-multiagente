import { Component, inject, signal, output, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { LanguageService, Language } from '../../services/language.service';

@Component({
    selector: 'app-profile-dropdown',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './profile-dropdown.component.html',
})
export class ProfileDropdownComponent {
    private authService = inject(AuthService);
    private router = inject(Router);
    languageService = inject(LanguageService);

    isOpen = signal(false);
    t = this.languageService.translations;

    // ✅ COMPUTED SIGNAL - ahora se puede llamar con ()
    currentLanguage = computed(() => this.languageService.getCurrentLanguage());

    // Outputs para eventos
    logoutClicked = output<void>();
    privacyPolicyClicked = output<void>();

    toggleDropdown() {
        this.isOpen.set(!this.isOpen());
    }

    closeDropdown() {
        this.isOpen.set(false);
    }

    getUserName(): string {
        const user = this.authService.currentUser();
        return user ? `${user.firstName} ${user.lastName}` : 'Usuario';
    }

    getUserEmail(): string {
        const user = this.authService.currentUser();
        return user?.email || '';
    }

    getInitials(): string {
        const user = this.authService.currentUser();
        if (!user) return 'U';
        return `${user.firstName.charAt(0)}${user.lastName.charAt(0)}`.toUpperCase();
    }

    onLogout() {
        this.closeDropdown();
        this.logoutClicked.emit();
    }

    onPrivacyPolicy() {
        this.closeDropdown();
        this.privacyPolicyClicked.emit();
    }

    setLanguage(lang: Language): void {
        this.languageService.setLanguage(lang);
    }
}
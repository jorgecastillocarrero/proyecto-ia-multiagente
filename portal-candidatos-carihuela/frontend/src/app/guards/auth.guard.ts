// src/app/guards/auth.guard.ts
import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { AdminAuthService } from '../services/admin-auth.service';

export const authGuard: CanActivateFn = () => {
    const authService = inject(AuthService);
    const adminAuthService = inject(AdminAuthService);
    const router = inject(Router);

    if (authService.isAuthenticated()) {
        return true;
    }

    if (adminAuthService.isAuthenticated()) {
        return router.parseUrl('/admin');
    }

    return router.parseUrl('/login');
};
// src/app/guards/guest.guard.ts
import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { AdminAuthService } from '../services/admin-auth.service';

export const guestGuard: CanActivateFn = (route) => {
    const authService = inject(AuthService);
    const adminAuthService = inject(AdminAuthService);
    const router = inject(Router);

    // Si es ruta de admin (/admin/auth)
    if (route.routeConfig?.path?.includes('admin')) {
        // Solo bloquea si está logueado como admin
        if (adminAuthService.isAuthenticated()) {
            return router.parseUrl('/admin');
        }
        return true;
    }
    
    // Si es ruta de candidato (/login, /register)
    // Bloquea AMBOS: candidatos Y admins logueados
    if (authService.isAuthenticated()) {
        return router.parseUrl('/documents');
    }
    
    if (adminAuthService.isAuthenticated()) {
        return router.parseUrl('/admin');
    }

    return true;
};
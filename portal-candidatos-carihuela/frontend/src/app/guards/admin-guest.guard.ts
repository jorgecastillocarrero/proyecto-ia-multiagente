// src/app/guards/admin-guest.guard.ts
import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AdminAuthService } from '../services/admin-auth.service';
import { AuthService } from '../services/auth.service';

/**
 * Guard para el login de admin
 * - Si ya está logueado como admin → redirige a /admin
 * - Si está logueado como candidato → redirige a /documents
 * - Si no está logueado → permite acceso al login de admin
 */
export const adminGuestGuard: CanActivateFn = () => {
    const adminAuthService = inject(AdminAuthService);
    const authService = inject(AuthService);
    const router = inject(Router);

    // Si está autenticado como admin, redirigir al panel de admin
    if (adminAuthService.isAuthenticated()) {
        console.warn('Ya estás logueado como admin. Redirigiendo a /admin');
        return router.parseUrl('/admin');
    }

    // Si está autenticado como candidato, redirigir a documentos
    if (authService.isAuthenticated()) {
        console.warn('Ya estás logueado como candidato. Redirigiendo a /documents');
        return router.parseUrl('/documents');
    }

    // Si no está autenticado, permitir acceso al login de admin
    return true;
};
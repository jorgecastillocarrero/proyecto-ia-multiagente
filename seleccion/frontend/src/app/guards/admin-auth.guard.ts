import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AdminAuthService } from '../services/admin-auth.service';

export const adminAuthGuard: CanActivateFn = () => {
    const adminAuthService = inject(AdminAuthService);
    const router = inject(Router);

    if (adminAuthService.isAuthenticated()) {
        return true;
    }

    // Redirigir al login de admin si no está autenticado
    return router.parseUrl('/admin/auth');
};
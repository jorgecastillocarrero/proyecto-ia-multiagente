import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, throwError } from 'rxjs';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { AdminAuthService } from '../services/admin-auth.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
    const authService = inject(AuthService);
    const adminAuthService = inject(AdminAuthService);
    const router = inject(Router);

    // Determinar si es petición de admin
    const isAdminRequest = req.url.includes('/api/admin') || req.url.includes('/api/rrhh');

    // Obtener el token apropiado
    const token = isAdminRequest
        ? adminAuthService.getToken()
        : authService.getToken();

    // Clonar request y añadir token si existe
    let authReq = req;
    if (token) {
        authReq = req.clone({
            setHeaders: {
                Authorization: `Bearer ${token}`
            }
        });
    }

    // Manejar la respuesta
    return next(authReq).pipe(
        catchError((error: HttpErrorResponse) => {
            // 401: No autorizado (token expirado o inválido)
            if (error.status === 401) {
                // Evitar redireccionar si el error viene del login
                if (!req.url.includes('/auth/login')) {
                    if (isAdminRequest) {
                        adminAuthService.logout();
                        router.navigate(['/admin/auth']);
                    } else {
                        authService.logout();
                        router.navigate(['/login']);
                    }
                }
            }

            // 403: Prohibido (rol incorrecto)
            if (error.status === 403) {
                router.navigate(['/access-denied'], {
                    state: { serverError: error.error?.error }
                });
            }

            return throwError(() => error);
        })
    );
};
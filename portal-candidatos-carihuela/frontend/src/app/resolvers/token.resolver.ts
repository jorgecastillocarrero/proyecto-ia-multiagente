// src/app/resolvers/token.resolver.ts
import { inject } from '@angular/core';
import { ResolveFn, Router, ActivatedRouteSnapshot } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { catchError, map, of } from 'rxjs';

export const tokenResolver: ResolveFn<any> = (route: ActivatedRouteSnapshot) => {
    const authService = inject(AuthService);
    const router = inject(Router);

    const token = route.queryParams['token'];

    if (!token) {
        router.navigate(['/login']);
        return of(null);
    }

    return authService.verifyToken(token).pipe(
        map(response => {
            if (!response.valid) {
                router.navigate(['/login']);
                return null;
            }
            return response;
        }),
        catchError(() => {
            router.navigate(['/login']);
            return of(null);
        })
    );
};
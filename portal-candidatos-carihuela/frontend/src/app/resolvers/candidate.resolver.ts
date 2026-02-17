// src/app/resolvers/candidate.resolver.ts
import { inject } from '@angular/core';
import { ResolveFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { catchError, map, of } from 'rxjs';

export const candidateResolver: ResolveFn<any> = (route, state) => {
    const authService = inject(AuthService);
    const router = inject(Router);

    const token = route.queryParamMap.get('token');

    if (!token) {
        router.navigate(['/access-denied']);
        return of({ valid: false });
    }

    return authService.verifyToken(token).pipe(
        map(response => {
            if (response.valid && response.email) {
                return {
                    valid: true,
                    email: response.email,
                    token: token
                };
            } else {
                router.navigate(['/access-denied']);
                return { valid: false };
            }
        }),
        catchError(() => {
            router.navigate(['/access-denied']);
            return of({ valid: false });
        })
    );
};
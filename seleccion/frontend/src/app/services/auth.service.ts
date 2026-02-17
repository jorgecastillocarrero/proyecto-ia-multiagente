import { inject, Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { environment } from '../../environments/environment';

const JWT_TOKEN_KEY = 'auth_jwt_token';
const API_URL = environment.API_URL;

interface User {
    firstName: string;
    lastName: string;
    email: string;
    dni: string;
}

interface TokenValidationResponse {
    valid: boolean;
    email?: string;
    token?: string;
}

@Injectable({
    providedIn: 'root',
})
export class AuthService {
    private http = inject(HttpClient);

    // Signal para saber si está logueado
    isAuthenticated = signal<boolean>(!!this.getToken());

    // Signal para el usuario actual
    currentUser = signal<User | null>(null);

    // --- GESTIÓN DE TOKEN ---
    private setToken(token: string): void {
        localStorage.setItem(JWT_TOKEN_KEY, token);
        this.isAuthenticated.set(true);
    }

    getToken(): string | null {
        return localStorage.getItem(JWT_TOKEN_KEY);
    }

    logout(): void {
        localStorage.removeItem(JWT_TOKEN_KEY);
        this.isAuthenticated.set(false);
        this.currentUser.set(null);
    }

    // --- AUTHENTICATION ---
    verifyToken(token: string): Observable<TokenValidationResponse> {
        return this.http.get<TokenValidationResponse>(`${API_URL}/auth/verify-token`, {
            params: { token },
        });
    }

    completeRegistration(data: {
        token: string;
        firstName: string;
        lastName: string;
        dni: string;
        password: string;
    }): Observable<{ success: boolean; token: string; }> {
        return this.http.post<{ success: boolean; token: string; }>(`${API_URL}/auth/register`, data).pipe(
            tap(response => {
                if (response.success && response.token) {
                    this.setToken(response.token);
                    // Establecer usuario actual
                    this.currentUser.set({
                        firstName: data.firstName,
                        lastName: data.lastName,
                        email: '', // Se puede obtener del backend si es necesario
                        dni: data.dni
                    });
                }
            })
        );
    }

    // Alias para compatibilidad
    register = this.completeRegistration.bind(this);

    login(credentials: { email: string; password: string }): Observable<{ success: boolean; token: string; }> {
        return this.http.post<{ success: boolean; token: string; }>(`${API_URL}/auth/login`, credentials).pipe(
            tap(response => {
                if (response.success && response.token) {
                    this.setToken(response.token);
                }
            }),
            catchError(err => {
                this.logout();
                return throwError(() => err);
            })
        );
    }

    // --- DOCUMENTOS ---
    uploadDocuments(data: FormData): Observable<{ success: boolean; files: any }> {
        return this.http.post<{ success: boolean; files: any }>(`${API_URL}/documents/upload`, data);
    }

    // --- FORMULARIO ---
    getFormData(): Observable<any> {
        return this.http.get<any>(`${API_URL}/form/data`);
    }

    saveFormData(data: any): Observable<{ success: boolean; message: string }> {
        return this.http.post<{ success: boolean; message: string }>(`${API_URL}/form/submit`, data);
    }
}
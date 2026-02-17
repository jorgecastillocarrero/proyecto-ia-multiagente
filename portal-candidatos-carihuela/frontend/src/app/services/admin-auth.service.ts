// src/app/services/admin-auth.service.ts
import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap, catchError, throwError } from 'rxjs';
import { environment } from '../../environments/environment';
import { AuthResponse, User } from '../models/user.model';

@Injectable({
    providedIn: 'root'
})
export class AdminAuthService {
    private readonly ADMIN_TOKEN_KEY = 'admin_jwt_token';
    private readonly API_URL = environment.API_URL;

    isAuthenticated = signal<boolean>(!!this.getToken());
    currentAdmin = signal<User | null>(null);

    constructor(private http: HttpClient) {
        const token = this.getToken();
        if (token) {
            this.loadAdminFromToken(token);
        }
    }

    private loadAdminFromToken(token: string) {
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            this.currentAdmin.set({
                id: payload.id,
                email: payload.email,
                firstName: payload.firstName || '',
                lastName: payload.lastName || '',
                role: payload.role
            });
        } catch (error) {
            console.error('Error decoding admin token:', error);
            this.logout();
        }
    }

    private setToken(token: string): void {
        localStorage.setItem(this.ADMIN_TOKEN_KEY, token);
        this.isAuthenticated.set(true);
        this.loadAdminFromToken(token);
    }

    getToken(): string | null {
        return localStorage.getItem(this.ADMIN_TOKEN_KEY);
    }

    logout(): void {
        localStorage.removeItem(this.ADMIN_TOKEN_KEY);
        this.isAuthenticated.set(false);
        this.currentAdmin.set(null);
    }

    login(credentials: { email: string; password: string }): Observable<AuthResponse> {
        return this.http.post<AuthResponse>(`${this.API_URL}/admin/auth/login`, credentials).pipe(
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

    generateRegistrationLink(email: string, frontendUrl: string): Observable<any> {
        return this.http.get(`${this.API_URL}/admin/generate-link`, {
            params: { email, frontendUrl }
        });
    }

    getAllCandidates(): Observable<any> {
        return this.http.get(`${this.API_URL}/admin/candidates`);
    }
}
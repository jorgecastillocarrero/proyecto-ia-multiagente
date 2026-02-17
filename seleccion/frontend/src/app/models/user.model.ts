// src/app/models/user.model.ts
export interface User {
    id: number;
    email: string;
    firstName: string;
    lastName: string;
    role: number;
}

export interface AuthResponse {
    success: boolean;
    message: string;
    token: string;
    user: User;
}

export interface TokenValidationResponse {
    valid: boolean;
    email: string | null;
}
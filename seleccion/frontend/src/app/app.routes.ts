// src/app/app.routes.ts
import { Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { DocumentsComponent } from './components/documents/documents.component';
import { FormComponent } from './components/form/form.component';
import { ExamComponent } from './components/exam/exam.component';
import { AdminComponent } from './components/admin/admin.component';
import { AdminAuthComponent } from './components/admin-auth/admin-auth.component';
import { AccessDeniedComponent } from './components/access-denied/access-denied.component';
import { RegistrationSuccessComponent } from './components/registration-success/registration-success.component';
import { PrivacyPolicyComponent } from './components/privacy-policy/privacy-policy.component';

import { authGuard } from './guards/auth.guard';
import { guestGuard } from './guards/guest.guard';
import { adminAuthGuard } from './guards/admin-auth.guard';
import { adminGuestGuard } from './guards/admin-guest.guard';
import { tokenResolver } from './resolvers/token.resolver';
import { candidateResolver } from './resolvers/candidate.resolver';

export const routes: Routes = [
    {
        path: '',
        redirectTo: '/login',
        pathMatch: 'full'
    },
    {
        path: 'login',
        component: LoginComponent,
        canActivate: [guestGuard]
    },
    {
        path: 'register',
        component: RegisterComponent,
        resolve: { tokenData: tokenResolver, candidateData: candidateResolver}
    },
    {
        path: 'documents',
        component: DocumentsComponent,
        canActivate: [authGuard]
    },
    {
        path: 'form',
        component: FormComponent,
        canActivate: [authGuard]
    },
    {
        path: 'exam',
        component: ExamComponent,
        canActivate: [authGuard]
    },
    {
        path: 'admin/auth',
        component: AdminAuthComponent,
        canActivate: [adminGuestGuard]
    },
    {
        path: 'admin',
        component: AdminComponent,
        canActivate: [adminAuthGuard]
    },
    {
        path: 'access-denied',
        component: AccessDeniedComponent
    },
    {
        path: 'success',
        component: RegistrationSuccessComponent
    },
    {
        path: 'privacy-policy',
        component: PrivacyPolicyComponent
    },
    {
        path: '**',
        redirectTo: '/login'
    }
];
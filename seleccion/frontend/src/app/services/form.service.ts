import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { FormData } from '../models/form.model';

@Injectable({
    providedIn: 'root'
})
export class FormService {
    private readonly API_URL = environment.API_URL;

    constructor(private http: HttpClient) { }

    getFormData(): Observable<{ success: boolean; data: FormData | null }> {
        return this.http.get<{ success: boolean; data: FormData | null }>(`${this.API_URL}/form/data`);
    }

    saveFormData(data: FormData): Observable<any> {
        return this.http.post(`${this.API_URL}/form/submit`, data);
    }
}
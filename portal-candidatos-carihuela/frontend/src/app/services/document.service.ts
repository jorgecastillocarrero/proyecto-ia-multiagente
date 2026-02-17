// src/app/services/document.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
    providedIn: 'root'
})
export class DocumentService {
    private readonly API_URL = environment.API_URL;

    constructor(private http: HttpClient) { }

    uploadDocuments(formData: FormData): Observable<any> {
        return this.http.post(`${this.API_URL}/documents/upload`, formData);
    }

    getUserDocuments(): Observable<any> {
        return this.http.get(`${this.API_URL}/documents`);
    }
}
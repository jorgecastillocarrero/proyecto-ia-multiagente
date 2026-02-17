// src/app/models/form.model.ts
export interface FormData {
    phone: string;
    address: string;
    city: string;
    postalCode?: string;
    hasCar: boolean;
    canTravel: boolean;
    previousWorkExp: boolean;
    retailExp: boolean;
    experienceSummary: string;
}
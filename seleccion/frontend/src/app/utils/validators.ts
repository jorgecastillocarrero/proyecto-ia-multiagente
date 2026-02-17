// src/app/utils/validators.ts
import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

export class CustomValidators {
    static dni(): ValidatorFn {
        return (control: AbstractControl): ValidationErrors | null => {
            if (!control.value) {
                return null;
            }

            const dniPattern = /^[0-9]{8}[A-Za-z]$/;
            const valid = dniPattern.test(control.value);

            return valid ? null : { invalidDni: true };
        };
    }

    static phone(): ValidatorFn {
        return (control: AbstractControl): ValidationErrors | null => {
            if (!control.value) {
                return null;
            }

            const phonePattern = /^[0-9]{9}$/;
            const valid = phonePattern.test(control.value.replace(/\s/g, ''));

            return valid ? null : { invalidPhone: true };
        };
    }

    static strongPassword(): ValidatorFn {
        return (control: AbstractControl): ValidationErrors | null => {
            if (!control.value) {
                return null;
            }

            const hasUpperCase = /[A-Z]/.test(control.value);
            const hasLowerCase = /[a-z]/.test(control.value);
            const hasNumber = /[0-9]/.test(control.value);
            const minLength = control.value.length >= 8;

            const valid = hasUpperCase && hasLowerCase && hasNumber && minLength;

            return valid ? null : { weakPassword: true };
        };
    }
}
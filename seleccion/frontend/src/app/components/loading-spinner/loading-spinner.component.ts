import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-loading-spinner',
    standalone: true,
    imports: [CommonModule],
    template: `
    <div [class]="getSpinnerClass()"></div>
  `,
    styles: [`
    .spinner-sm {
      width: 20px;
      height: 20px;
      border: 2px solid #f3f3f3;
      border-top: 2px solid #003366;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }

    .spinner-md {
      width: 40px;
      height: 40px;
      border: 3px solid #f3f3f3;
      border-top: 3px solid #003366;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }

    .spinner-lg {
      width: 60px;
      height: 60px;
      border: 4px solid #f3f3f3;
      border-top: 4px solid #003366;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }

    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
  `]
})
export class LoadingSpinnerComponent {
    @Input() size: 'sm' | 'md' | 'lg' = 'md';

    getSpinnerClass(): string {
        return `spinner-${this.size}`;
    }
}
import { ChangeDetectionStrategy, Component, output, signal, input, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LanguageService } from '../../services/language.service';

@Component({
  selector: 'app-file-input',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './file-input.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class FileInputComponent {
  languageService = inject(LanguageService);
  t = this.languageService.translations;

  label = input.required<string>();
  controlId = input<string>('file-upload');
  hasError = input<boolean>(false);

  fileChanged = output<File | null>();
  fileName = signal<string | null>(null);

  errorMessage = signal<string | null>(null);

  private readonly allowedTypes = ['application/pdf', 'image/png', 'image/jpeg'];

  onFileSelected(event: Event | DragEvent): void {
    let file: File | null = null;
    this.errorMessage.set(null);

    if (event instanceof DragEvent) {
      file = event.dataTransfer?.files?.[0] ?? null;
    } else {
      const input = event.target as HTMLInputElement;
      file = input.files?.[0] ?? null;
    }

    if (!file) return;

    if (this.allowedTypes.includes(file.type)) {
      this.fileName.set(file.name);
      this.fileChanged.emit(file);
    } else {
      this.errorMessage.set('Formato no permitido. Solo se aceptan PDF, PNG o JPG.');
      this.clearFile();
    }

    if (!(event instanceof DragEvent)) {
      (event.target as HTMLInputElement).value = '';
    }
  }

  clearFile(): void {
    this.fileName.set(null);
    this.fileChanged.emit(null);
  }
}
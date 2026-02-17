// src/app/components/admin/candidatos/candidato-detail-modal.component.ts
import { Component, input, output } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface DetalleCompleto {
    candidato: any;
    experiencias: any[];
    conocimientos: string[];
    puestos: any[];
    datosPortal?: any;
}

@Component({
    selector: 'app-candidato-detail-modal',
    standalone: true,
    imports: [CommonModule],
    template: `
        @if (isOpen()) {
        <div class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-fadeIn"
            (click)="onClose.emit()">
            <div class="bg-white rounded-2xl shadow-2xl w-full max-w-3xl max-h-[90vh] flex flex-col animate-slideUp"
                (click)="$event.stopPropagation()">

                <!-- Header -->
                <div class="px-4 md:px-6 py-4 border-b border-slate-200 flex items-center justify-between flex-shrink-0">
                    <div class="flex-1 min-w-0 mr-4">
                        <h3 class="text-lg md:text-xl font-bold text-slate-900 truncate">
                            {{ detalle()?.candidato?.nombre || 'Candidato' }}
                        </h3>
                        @if (detalle()?.candidato?.puesto_deseado) {
                        <p class="text-xs md:text-sm text-slate-500 mt-0.5 truncate">
                            {{ detalle()!.candidato.puesto_deseado }}
                        </p>
                        }
                    </div>
                    <button (click)="onClose.emit()" 
                        class="p-2 hover:bg-slate-100 rounded-lg transition-colors flex-shrink-0">
                        <svg class="w-5 h-5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12">
                            </path>
                        </svg>
                    </button>
                </div>

                <!-- Contenido Scrolleable -->
                <div class="overflow-y-auto flex-1 p-4 md:p-6">
                    @if (loading()) {
                    <div class="flex items-center justify-center py-12">
                        <div class="inline-block w-8 h-8 border-3 border-slate-200 border-t-[#003366] rounded-full animate-spin">
                        </div>
                    </div>
                    } @else if (detalle()) {
                    <div class="space-y-4 md:space-y-6">

                        <!-- Info Básica en Grid -->
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div class="space-y-3">
                                <div>
                                    <label class="text-xs font-medium text-slate-500 uppercase">Email</label>
                                    <p class="text-sm text-slate-900 mt-1 break-words">
                                        {{ detalle()!.candidato.email }}
                                    </p>
                                </div>
                                <div>
                                    <label class="text-xs font-medium text-slate-500 uppercase">Teléfono</label>
                                    <p class="text-sm text-slate-900 mt-1">
                                        {{ detalle()!.candidato.telefono }}
                                    </p>
                                </div>
                            </div>
                            <div class="space-y-3">
                                <div>
                                    <label class="text-xs font-medium text-slate-500 uppercase">Ubicación</label>
                                    <p class="text-sm text-slate-900 mt-1">
                                        {{ detalle()!.candidato.ciudad }}, {{ detalle()!.candidato.provincia }}
                                    </p>
                                </div>
                                <div>
                                    <label class="text-xs font-medium text-slate-500 uppercase">Experiencia</label>
                                    <p class="text-sm text-slate-900 mt-1">
                                        {{ detalle()!.candidato.total_anos_experiencia || 0 }} años
                                    </p>
                                </div>
                            </div>
                        </div>

                        <!-- Carnets y Permisos -->
                        <div>
                            <label class="text-xs font-medium text-slate-500 uppercase mb-2 block">
                                Carnets y Permisos
                            </label>
                            <div class="flex flex-wrap gap-2">
                                @if (detalle()!.candidato.carnet_b) {
                                <span class="px-3 py-1.5 bg-blue-50 text-blue-700 text-sm font-medium rounded-lg border border-blue-200">
                                    Carnet B
                                </span>
                                }
                                @if (detalle()!.candidato.carnet_c) {
                                <span class="px-3 py-1.5 bg-blue-50 text-blue-700 text-sm font-medium rounded-lg border border-blue-200">
                                    Carnet C
                                </span>
                                }
                                @if (detalle()!.candidato.vehiculo_propio) {
                                <span class="px-3 py-1.5 bg-emerald-50 text-emerald-700 text-sm font-medium rounded-lg border border-emerald-200">
                                    Vehículo Propio
                                </span>
                                }
                                @if (detalle()!.candidato.cap) {
                                <span class="px-3 py-1.5 bg-purple-50 text-purple-700 text-sm font-medium rounded-lg border border-purple-200">
                                    CAP
                                </span>
                                }
                                @if (detalle()!.candidato.carnet_carretillero) {
                                <span class="px-3 py-1.5 bg-orange-50 text-orange-700 text-sm font-medium rounded-lg border border-orange-200">
                                    Carretillero
                                </span>
                                }
                                @if (!detalle()!.candidato.carnet_b && !detalle()!.candidato.carnet_c && 
                                     !detalle()!.candidato.vehiculo_propio && !detalle()!.candidato.cap &&
                                     !detalle()!.candidato.carnet_carretillero) {
                                <span class="text-sm text-slate-500">Sin información de carnets</span>
                                }
                            </div>
                        </div>

                        <!-- Experiencia Laboral -->
                        @if (detalle()!.experiencias && detalle()!.experiencias.length > 0) {
                        <div>
                            <label class="text-xs font-medium text-slate-500 uppercase mb-3 block">
                                Experiencia Laboral
                            </label>
                            <div class="space-y-3">
                                @for (exp of detalle()!.experiencias; track exp.id) {
                                <div class="bg-slate-50 rounded-lg p-4 border border-slate-200">
                                    <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-2 mb-2">
                                        <div class="flex-1 min-w-0">
                                            <h4 class="font-semibold text-slate-900">{{ exp.puesto }}</h4>
                                            @if (exp.empresa) {
                                            <p class="text-sm text-slate-600 mt-1">{{ exp.empresa }}</p>
                                            }
                                        </div>
                                        @if (exp.duracion_meses) {
                                        <span class="text-xs bg-white text-slate-600 px-2 py-1 rounded border border-slate-200 self-start">
                                            {{ exp.duracion_meses }} meses
                                        </span>
                                        }
                                    </div>
                                    @if (exp.descripcion) {
                                    <p class="text-sm text-slate-600 mt-2">{{ exp.descripcion }}</p>
                                    }
                                </div>
                                }
                            </div>
                        </div>
                        }

                        <!-- Conocimientos -->
                        @if (detalle()!.conocimientos && detalle()!.conocimientos.length > 0) {
                        <div>
                            <label class="text-xs font-medium text-slate-500 uppercase mb-2 block">Conocimientos</label>
                            <div class="flex flex-wrap gap-2">
                                @for (conocimiento of detalle()!.conocimientos; track conocimiento) {
                                <span class="px-3 py-1 bg-slate-100 text-slate-700 text-sm rounded-full">
                                    {{ conocimiento }}
                                </span>
                                }
                            </div>
                        </div>
                        }

                        <!-- Estado en Portal -->
                        @if (detalle()!.datosPortal) {
                        <div class="bg-emerald-50 border border-emerald-200 rounded-lg p-4">
                            <div class="flex items-start gap-3">
                                <svg class="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                                <div>
                                    <p class="text-sm font-semibold text-emerald-900">Registrado en el Portal</p>
                                    <p class="text-sm text-emerald-700 mt-1">
                                        Este candidato tiene acceso al portal desde el 
                                        {{ detalle()!.datosPortal.createdAt | date:'dd/MM/yyyy' }}
                                    </p>
                                </div>
                            </div>
                        </div>
                        } @else {
                        <div class="bg-amber-50 border border-amber-200 rounded-lg p-4">
                            <div class="flex items-start gap-3">
                                <svg class="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z">
                                    </path>
                                </svg>
                                <div>
                                    <p class="text-sm font-semibold text-amber-900">Sin Acceso al Portal</p>
                                    <p class="text-sm text-amber-700 mt-1">
                                        Este candidato aún no se ha registrado en el portal
                                    </p>
                                </div>
                            </div>
                        </div>
                        }

                    </div>
                    }
                </div>

                <!-- Footer -->
                <div class="px-4 md:px-6 py-4 border-t border-slate-200 flex justify-end gap-3 flex-shrink-0">
                    <button (click)="onClose.emit()"
                        class="px-4 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors">
                        Cerrar
                    </button>
                </div>

            </div>
        </div>
        }
    `
})
export class CandidatoDetailModalComponent {
    isOpen = input.required<boolean>();
    loading = input<boolean>(false);
    detalle = input<DetalleCompleto | null>(null);

    onClose = output<void>();
}
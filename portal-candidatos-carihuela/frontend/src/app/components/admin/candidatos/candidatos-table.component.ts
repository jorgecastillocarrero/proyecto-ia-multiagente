// src/app/components/admin/candidatos/candidatos-table.component.ts
import { Component, input, output } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface Candidato {
    id: number;
    nombre: string;
    email: string;
    telefono: string;
    ciudad: string;
    provincia: string;
    estado: string;
    total_anos_experiencia: number;
    carnet_b: boolean;
    carnet_c: boolean;
    vehiculo_propio: boolean;
    fecha_importacion: string;
    puesto_deseado: string;
}

export interface Paginacion {
    actual: number;
    total: number;
    totalCandidatos: number;
    mostrados: number;
}

@Component({
    selector: 'app-candidatos-table',
    standalone: true,
    imports: [CommonModule],
    template: `
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
            @if (loading()) {
            <div class="p-12 text-center">
                <div class="inline-block w-8 h-8 border-3 border-slate-200 border-t-[#003366] rounded-full animate-spin">
                </div>
                <p class="mt-4 text-slate-500">Cargando candidatos...</p>
            </div>
            } @else if (candidatos().length === 0) {
            <div class="p-12 text-center">
                <svg class="mx-auto w-12 h-12 text-slate-300 mb-4" fill="none" stroke="currentColor"
                    viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4">
                    </path>
                </svg>
                <p class="text-slate-500 font-medium">No se encontraron candidatos</p>
                <p class="text-slate-400 text-sm mt-2">Prueba ajustando los filtros de búsqueda</p>
            </div>
            } @else {
            
            <!-- Vista Desktop -->
            <div class="hidden lg:block overflow-x-auto">
                <table class="w-full">
                    <thead>
                        <tr class="border-b border-slate-200 bg-slate-50">
                            <th class="px-6 py-4 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">
                                Candidato</th>
                            <th class="px-6 py-4 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">
                                Contacto</th>
                            <th class="px-6 py-4 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">
                                Ubicación</th>
                            <th class="px-6 py-4 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">
                                Estado</th>
                            <th class="px-6 py-4 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">
                                Experiencia</th>
                            <th class="px-6 py-4 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">
                                Carnets</th>
                            <th class="px-6 py-4 text-center text-xs font-semibold text-slate-600 uppercase tracking-wider">
                                Acciones</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100">
                        @for (candidato of candidatos(); track candidato.id) {
                        <tr class="hover:bg-slate-50 transition-colors">
                            <td class="px-6 py-4">
                                <div class="flex items-center gap-3">
                                    <div class="w-10 h-10 rounded-full bg-[#003366] text-white flex items-center justify-center font-semibold flex-shrink-0">
                                        {{ candidato.nombre.charAt(0) }}
                                    </div>
                                    <div class="min-w-0">
                                        <div class="font-medium text-slate-900 truncate">{{ candidato.nombre }}</div>
                                        @if (candidato.puesto_deseado) {
                                        <div class="text-xs text-slate-500 truncate">{{ candidato.puesto_deseado }}</div>
                                        }
                                    </div>
                                </div>
                            </td>
                            <td class="px-6 py-4">
                                <div class="text-sm text-slate-600 truncate">{{ candidato.email }}</div>
                                <div class="text-sm text-slate-500 flex items-center gap-1 mt-1">
                                    <svg class="w-3 h-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z">
                                        </path>
                                    </svg>
                                    {{ candidato.telefono }}
                                </div>
                            </td>
                            <td class="px-6 py-4">
                                <div class="text-sm text-slate-700 font-medium">{{ candidato.ciudad }}</div>
                                <div class="text-xs text-slate-500">{{ candidato.provincia }}</div>
                            </td>
                            <td class="px-6 py-4">
                                <span [class]="getEstadoClasses(candidato.estado)">
                                    {{ getEstadoLabel(candidato.estado) }}
                                </span>
                            </td>
                            <td class="px-6 py-4">
                                <div class="text-sm font-medium text-slate-700">
                                    {{ candidato.total_anos_experiencia || 0 }} años
                                </div>
                            </td>
                            <td class="px-6 py-4">
                                <div class="flex gap-1.5 flex-wrap">
                                    @if (candidato.carnet_b) {
                                    <span class="px-2 py-0.5 bg-blue-50 text-blue-700 text-xs font-medium rounded border border-blue-200">B</span>
                                    }
                                    @if (candidato.carnet_c) {
                                    <span class="px-2 py-0.5 bg-blue-50 text-blue-700 text-xs font-medium rounded border border-blue-200">C</span>
                                    }
                                    @if (candidato.vehiculo_propio) {
                                    <span class="text-lg">🚗</span>
                                    }
                                </div>
                            </td>
                            <td class="px-6 py-4 text-center">
                                <button (click)="onVerDetalle.emit(candidato)"
                                    class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-[#003366] text-white text-sm font-medium rounded-lg hover:bg-[#002244] transition-colors">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z">
                                        </path>
                                    </svg>
                                    Ver Detalle
                                </button>
                            </td>
                        </tr>
                        }
                    </tbody>
                </table>
            </div>

            <!-- Vista Mobile/Tablet - Cards -->
            <div class="lg:hidden divide-y divide-slate-100">
                @for (candidato of candidatos(); track candidato.id) {
                <div class="p-4 hover:bg-slate-50 transition-colors">
                    <div class="flex items-start gap-3 mb-3">
                        <div class="w-12 h-12 rounded-full bg-[#003366] text-white flex items-center justify-center font-semibold text-lg flex-shrink-0">
                            {{ candidato.nombre.charAt(0) }}
                        </div>
                        <div class="flex-1 min-w-0">
                            <h3 class="font-semibold text-slate-900 text-base mb-1">{{ candidato.nombre }}</h3>
                            @if (candidato.puesto_deseado) {
                            <p class="text-sm text-slate-500 mb-2">{{ candidato.puesto_deseado }}</p>
                            }
                            <span [class]="getEstadoClasses(candidato.estado)">
                                {{ getEstadoLabel(candidato.estado) }}
                            </span>
                        </div>
                    </div>

                    <div class="space-y-2 text-sm mb-3">
                        <div class="flex items-center gap-2 text-slate-600">
                            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z">
                                </path>
                            </svg>
                            <span class="truncate">{{ candidato.email }}</span>
                        </div>
                        <div class="flex items-center gap-2 text-slate-600">
                            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z">
                                </path>
                            </svg>
                            <span>{{ candidato.telefono }}</span>
                        </div>
                        <div class="flex items-center gap-2 text-slate-600">
                            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z">
                                </path>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                            </svg>
                            <span>{{ candidato.ciudad }}, {{ candidato.provincia }}</span>
                        </div>
                    </div>

                    <div class="flex items-center justify-between pt-3 border-t border-slate-100">
                        <div class="flex items-center gap-2">
                            <span class="text-xs text-slate-500">Exp:</span>
                            <span class="text-sm font-medium text-slate-700">
                                {{ candidato.total_anos_experiencia || 0 }} años
                            </span>
                            @if (candidato.carnet_b || candidato.carnet_c || candidato.vehiculo_propio) {
                            <div class="flex gap-1 ml-2">
                                @if (candidato.carnet_b) {
                                <span class="px-1.5 py-0.5 bg-blue-50 text-blue-700 text-xs font-medium rounded">B</span>
                                }
                                @if (candidato.carnet_c) {
                                <span class="px-1.5 py-0.5 bg-blue-50 text-blue-700 text-xs font-medium rounded">C</span>
                                }
                                @if (candidato.vehiculo_propio) {
                                <span class="text-base">🚗</span>
                                }
                            </div>
                            }
                        </div>
                        <button (click)="onVerDetalle.emit(candidato)"
                            class="flex items-center gap-1.5 px-3 py-1.5 bg-[#003366] text-white text-sm font-medium rounded-lg hover:bg-[#002244] transition-colors">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z">
                                </path>
                            </svg>
                            Ver
                        </button>
                    </div>
                </div>
                }
            </div>

            <!-- Paginación -->
            <div class="bg-slate-50 px-4 md:px-6 py-4 flex flex-col sm:flex-row items-center justify-between gap-3 border-t border-slate-200">
                <div class="text-xs md:text-sm text-slate-600 text-center sm:text-left">
                    Mostrando <span class="font-medium text-slate-900">{{ paginacion().mostrados }}</span> de 
                    <span class="font-medium text-slate-900">{{ paginacion().totalCandidatos }}</span> candidatos
                </div>
                <div class="flex items-center gap-2">
                    <button [disabled]="paginacion().actual === 1" 
                        (click)="onCambiarPagina.emit(paginacion().actual - 1)"
                        class="px-3 py-1.5 text-xs md:text-sm border border-slate-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-white transition-colors">
                        Anterior
                    </button>
                    <span class="px-2 md:px-3 py-1.5 text-xs md:text-sm text-slate-700">
                        Página <span class="font-medium">{{ paginacion().actual }}</span> de 
                        <span class="font-medium">{{ paginacion().total }}</span>
                    </span>
                    <button [disabled]="paginacion().actual === paginacion().total"
                        (click)="onCambiarPagina.emit(paginacion().actual + 1)"
                        class="px-3 py-1.5 text-xs md:text-sm border border-slate-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-white transition-colors">
                        Siguiente
                    </button>
                </div>
            </div>
            }
        </div>
    `
})
export class CandidatosTableComponent {
    candidatos = input.required<Candidato[]>();
    loading = input<boolean>(false);
    paginacion = input.required<Paginacion>();

    onVerDetalle = output<Candidato>();
    onCambiarPagina = output<number>();

    getEstadoClasses(estado: string): string {
        const baseClasses = 'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium ';
        switch (estado) {
            case 'sin_valorar':
                return baseClasses + 'bg-amber-50 text-amber-700 border border-amber-200';
            case 'activo':
                return baseClasses + 'bg-emerald-50 text-emerald-700 border border-emerald-200';
            case 'descartado':
                return baseClasses + 'bg-slate-100 text-slate-700 border border-slate-200';
            case 'en_proceso':
                return baseClasses + 'bg-blue-50 text-blue-700 border border-blue-200';
            default:
                return baseClasses + 'bg-slate-100 text-slate-700 border border-slate-200';
        }
    }

    getEstadoLabel(estado: string): string {
        switch (estado) {
            case 'sin_valorar': return 'Sin valorar';
            case 'activo': return 'Activo';
            case 'descartado': return 'Descartado';
            case 'en_proceso': return 'En proceso';
            default: return estado;
        }
    }
}
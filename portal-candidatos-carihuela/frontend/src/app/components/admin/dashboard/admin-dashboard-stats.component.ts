// src/app/components/admin/dashboard/admin-dashboard-stats.component.ts
import { Component, input, output } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface Estadisticas {
    candidatos_sin_valorar: number;
    candidatos_activos: number;
    candidatos_descartados: number;
    pendientes_criba: number;
    pendientes_llamar: number;
    entrevistas_hoy: number;
    puestos_activos: number;
}

@Component({
    selector: 'app-admin-dashboard-stats',
    standalone: true,
    imports: [CommonModule],
    template: `
        <!-- Tarjetas de Estadísticas -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
            <!-- Sin Valorar -->
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 md:p-6 hover:shadow-md transition-shadow cursor-pointer"
                (click)="onFilterClick.emit('sin_valorar')">
                <div class="flex items-start justify-between">
                    <div class="flex-1 min-w-0">
                        <p class="text-xs md:text-sm font-medium text-slate-500 mb-1">Sin Valorar</p>
                        <p class="text-2xl md:text-3xl font-bold text-slate-900 truncate">
                            {{ stats().candidatos_sin_valorar }}
                        </p>
                    </div>
                    <div class="p-2 md:p-3 bg-amber-50 rounded-lg flex-shrink-0">
                        <svg class="w-5 h-5 md:w-6 md:h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                    </div>
                </div>
            </div>

            <!-- Activos -->
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 md:p-6 hover:shadow-md transition-shadow cursor-pointer"
                (click)="onFilterClick.emit('activo')">
                <div class="flex items-start justify-between">
                    <div class="flex-1 min-w-0">
                        <p class="text-xs md:text-sm font-medium text-slate-500 mb-1">Activos</p>
                        <p class="text-2xl md:text-3xl font-bold text-slate-900 truncate">
                            {{ stats().candidatos_activos }}
                        </p>
                    </div>
                    <div class="p-2 md:p-3 bg-emerald-50 rounded-lg flex-shrink-0">
                        <svg class="w-5 h-5 md:w-6 md:h-6 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                    </div>
                </div>
            </div>

            <!-- Pendientes Criba -->
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 md:p-6 hover:shadow-md transition-shadow">
                <div class="flex items-start justify-between">
                    <div class="flex-1 min-w-0">
                        <p class="text-xs md:text-sm font-medium text-slate-500 mb-1">Pendientes Criba</p>
                        <p class="text-2xl md:text-3xl font-bold text-slate-900 truncate">
                            {{ stats().pendientes_criba }}
                        </p>
                    </div>
                    <div class="p-2 md:p-3 bg-blue-50 rounded-lg flex-shrink-0">
                        <svg class="w-5 h-5 md:w-6 md:h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4">
                            </path>
                        </svg>
                    </div>
                </div>
            </div>

            <!-- Descartados -->
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 md:p-6 hover:shadow-md transition-shadow cursor-pointer"
                (click)="onFilterClick.emit('descartado')">
                <div class="flex items-start justify-between">
                    <div class="flex-1 min-w-0">
                        <p class="text-xs md:text-sm font-medium text-slate-500 mb-1">Descartados</p>
                        <p class="text-2xl md:text-3xl font-bold text-slate-900 truncate">
                            {{ stats().candidatos_descartados }}
                        </p>
                    </div>
                    <div class="p-2 md:p-3 bg-slate-100 rounded-lg flex-shrink-0">
                        <svg class="w-5 h-5 md:w-6 md:h-6 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636">
                            </path>
                        </svg>
                    </div>
                </div>
            </div>
        </div>

        <!-- Acciones Rápidas y Resumen -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 md:gap-6 mt-6">
            <!-- Acciones Rápidas -->
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 md:p-6">
                <h3 class="text-base md:text-lg font-semibold text-slate-900 mb-4">Acciones Rápidas</h3>
                <div class="space-y-2">
                    <button (click)="onViewCandidates.emit()"
                        class="w-full flex items-center justify-between px-4 py-3 text-left bg-slate-50 hover:bg-slate-100 rounded-lg transition-colors group">
                        <span class="text-sm md:text-base text-slate-700 group-hover:text-slate-900 font-medium">
                            Ver todos los candidatos
                        </span>
                        <svg class="w-5 h-5 text-slate-400 group-hover:text-slate-600" fill="none"
                            stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7">
                            </path>
                        </svg>
                    </button>
                    <button (click)="onGenerateLink.emit()"
                        class="w-full flex items-center justify-between px-4 py-3 text-left bg-slate-50 hover:bg-slate-100 rounded-lg transition-colors group">
                        <span class="text-sm md:text-base text-slate-700 group-hover:text-slate-900 font-medium">
                            Generar enlace de registro
                        </span>
                        <svg class="w-5 h-5 text-slate-400 group-hover:text-slate-600" fill="none"
                            stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7">
                            </path>
                        </svg>
                    </button>
                </div>
            </div>

            <!-- Resumen Hoy -->
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 md:p-6">
                <h3 class="text-base md:text-lg font-semibold text-slate-900 mb-4">Resumen Hoy</h3>
                <div class="space-y-3">
                    <div class="flex items-center justify-between py-2 border-b border-slate-100">
                        <span class="text-xs md:text-sm text-slate-600">Pendientes de llamar</span>
                        <span class="text-xs md:text-sm font-semibold text-slate-900">
                            {{ stats().pendientes_llamar }}
                        </span>
                    </div>
                    <div class="flex items-center justify-between py-2 border-b border-slate-100">
                        <span class="text-xs md:text-sm text-slate-600">Entrevistas programadas</span>
                        <span class="text-xs md:text-sm font-semibold text-slate-900">
                            {{ stats().entrevistas_hoy }}
                        </span>
                    </div>
                    <div class="flex items-center justify-between py-2">
                        <span class="text-xs md:text-sm text-slate-600">Puestos activos</span>
                        <span class="text-xs md:text-sm font-semibold text-slate-900">
                            {{ stats().puestos_activos }}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    `
})
export class AdminDashboardStatsComponent {
    stats = input.required<Estadisticas>();
    onFilterClick = output<string>();
    onViewCandidates = output<void>();
    onGenerateLink = output<void>();
}
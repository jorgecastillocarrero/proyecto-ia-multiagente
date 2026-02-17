// src/app/components/admin/candidatos/candidatos-filters.component.ts
import { Component, input, output, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface FiltrosCandidatos {
    estado: string;
    busqueda: string;
    provincia?: string;
    experienciaMin?: number;
    experienciaMax?: number;
    carnetB?: boolean;
    carnetC?: boolean;
    vehiculoPropio?: boolean;
    ordenarPor?: 'nombre' | 'fecha' | 'experiencia';
}

@Component({
    selector: 'app-candidatos-filters',
    standalone: true,
    imports: [CommonModule],
    styles: [`
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .animate-slideDown {
            animation: slideDown 0.3s ease-out;
        }

        /* Custom select dropdown arrow */
        select {
            background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%23475569' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
            background-position: right 0.75rem center;
            background-repeat: no-repeat;
            background-size: 1.5em 1.5em;
            padding-right: 2.5rem;
            -webkit-appearance: none;
            -moz-appearance: none;
            appearance: none;
        }

        /* Checkbox styles */
        input[type="checkbox"]:checked {
            background-color: #1e293b;
            border-color: #1e293b;
        }

        input[type="checkbox"]:focus {
            ring-color: #64748b;
        }
    `],
    template: `
        <div class="bg-white rounded-2xl shadow-lg border border-slate-200 overflow-hidden mb-5">
            <div class="bg-white border-b border-slate-200 p-4 md:p-5">
                <div class="flex flex-col lg:flex-row gap-3 md:gap-4">
                    <div class="flex-1">
                        <div class="relative group">
                            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                <svg class="w-5 h-5 text-slate-400 group-focus-within:text-slate-600 transition-colors" fill="none"
                                    stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                                </svg>
                            </div>
                            <input type="text" 
                                [value]="filtros().busqueda"
                                (input)="handleBusquedaChange($event)"
                                placeholder="Buscar por nombre, email o teléfono..."
                                class="w-full pl-12 pr-4 py-3 bg-slate-50 border-2 border-slate-200 rounded-xl text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-300 focus:border-slate-400 focus:bg-white transition-all text-sm md:text-base">
                        </div>
                    </div>

                    <div class="flex gap-2">
                        <button (click)="toggleFiltrosAvanzados()"
                            [class]="mostrarFiltrosAvanzados() 
                                ? 'bg-slate-100 text-slate-900 border-slate-300' 
                                : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'"
                            class="px-4 py-3 rounded-xl border-2 transition-all duration-200 font-medium flex items-center gap-2 text-sm md:text-base whitespace-nowrap">
                            <svg class="w-4 h-4 transition-transform duration-200" 
                                [class.rotate-180]="mostrarFiltrosAvanzados()"
                                fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z">
                                </path>
                            </svg>
                            <span class="hidden sm:inline">{{ mostrarFiltrosAvanzados() ? 'Ocultar filtros' : 'Más filtros' }}</span>
                        </button>

                        <button (click)="onActualizar.emit()"
                            class="px-4 md:px-6 py-3 bg-slate-900 text-white rounded-xl hover:bg-slate-800 transition-all duration-200 font-semibold flex items-center gap-2 text-sm md:text-base whitespace-nowrap shadow-sm hover:shadow-md">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15">
                                </path>
                            </svg>
                            <span class="hidden sm:inline">Actualizar</span>
                        </button>
                    </div>
                </div>
            </div>

            @if (mostrarFiltrosAvanzados()) {
            <div class="p-4 md:p-6 bg-slate-50/50 border-t border-slate-200 animate-slideDown">
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 mb-2 uppercase tracking-wider">
                            Estado
                        </label>
                        <select [value]="filtros().estado" 
                            (change)="handleEstadoChange($any($event.target).value)"
                            class="w-full px-4 py-2.5 bg-white border-2 border-slate-200 rounded-lg text-slate-700 focus:outline-none focus:ring-2 focus:ring-slate-300 focus:border-slate-400 transition-all text-sm hover:border-slate-300 cursor-pointer shadow-sm">
                            <option value="todos">Todos</option>
                            <option value="sin_valorar">Sin valorar</option>
                            <option value="activo">Activos</option>
                            <option value="descartado">Descartados</option>
                            <option value="en_proceso">En proceso</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-semibold text-slate-700 mb-2 uppercase tracking-wider">
                            Provincia
                        </label>
                        <select [value]="filtros().provincia || ''"
                            (change)="handleProvinciaChange($any($event.target).value)"
                            class="w-full px-4 py-2.5 bg-white border-2 border-slate-200 rounded-lg text-slate-700 focus:outline-none focus:ring-2 focus:ring-slate-300 focus:border-slate-400 transition-all text-sm hover:border-slate-300 cursor-pointer shadow-sm">
                            <option value="">Todas</option>
                            <option value="Málaga">Málaga</option>
                            <option value="Sevilla">Sevilla</option>
                            <option value="Granada">Granada</option>
                            <option value="Cádiz">Cádiz</option>
                            <option value="Córdoba">Córdoba</option>
                            <option value="Almería">Almería</option>
                            <option value="Huelva">Huelva</option>
                            <option value="Jaén">Jaén</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-semibold text-slate-700 mb-2 uppercase tracking-wider">
                            Experiencia Mínima
                        </label>
                        <select [value]="filtros().experienciaMin || ''"
                            (change)="handleExperienciaMinChange($any($event.target).value)"
                            class="w-full px-4 py-2.5 bg-white border-2 border-slate-200 rounded-lg text-slate-700 focus:outline-none focus:ring-2 focus:ring-slate-300 focus:border-slate-400 transition-all text-sm hover:border-slate-300 cursor-pointer shadow-sm">
                            <option value="">Sin mínimo</option>
                            <option value="1">1+ años</option>
                            <option value="2">2+ años</option>
                            <option value="3">3+ años</option>
                            <option value="5">5+ años</option>
                            <option value="10">10+ años</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-semibold text-slate-700 mb-2 uppercase tracking-wider">
                            Ordenar por
                        </label>
                        <select [value]="filtros().ordenarPor || 'fecha'"
                            (change)="handleOrdenarPorChange($any($event.target).value)"
                            class="w-full px-4 py-2.5 bg-white border-2 border-slate-200 rounded-lg text-slate-700 focus:outline-none focus:ring-2 focus:ring-slate-300 focus:border-slate-400 transition-all text-sm hover:border-slate-300 cursor-pointer shadow-sm">
                            <option value="fecha">Más recientes</option>
                            <option value="nombre">Nombre (A-Z)</option>
                            <option value="experiencia">Mayor experiencia</option>
                        </select>
                    </div>

                    <div class="sm:col-span-2 lg:col-span-3 xl:col-span-4">
                        <label class="block text-xs font-semibold text-slate-700 mb-3 uppercase tracking-wider">
                            Carnets y Permisos
                        </label>
                        <div class="flex flex-wrap gap-3">
                            <label class="flex items-center gap-2.5 px-4 py-2.5 bg-white border-2 border-slate-200 rounded-lg hover:border-slate-400 hover:bg-slate-50 transition-all cursor-pointer shadow-sm">
                                <input type="checkbox" 
                                    [checked]="filtros().carnetB || false"
                                    (change)="handleCarnetBChange($any($event.target).checked)"
                                    class="w-4 h-4 text-slate-900 bg-white border-slate-300 rounded focus:ring-slate-400 focus:ring-2 cursor-pointer">
                                <span class="text-sm font-medium text-slate-700">Carnet B</span>
                            </label>
                            <label class="flex items-center gap-2.5 px-4 py-2.5 bg-white border-2 border-slate-200 rounded-lg hover:border-slate-400 hover:bg-slate-50 transition-all cursor-pointer shadow-sm">
                                <input type="checkbox" 
                                    [checked]="filtros().carnetC || false"
                                    (change)="handleCarnetCChange($any($event.target).checked)"
                                    class="w-4 h-4 text-slate-900 bg-white border-slate-300 rounded focus:ring-slate-400 focus:ring-2 cursor-pointer">
                                <span class="text-sm font-medium text-slate-700">Carnet C</span>
                            </label>
                            <label class="flex items-center gap-2.5 px-4 py-2.5 bg-white border-2 border-slate-200 rounded-lg hover:border-slate-400 hover:bg-slate-50 transition-all cursor-pointer shadow-sm">
                                <input type="checkbox" 
                                    [checked]="filtros().vehiculoPropio || false"
                                    (change)="handleVehiculoPropioChange($any($event.target).checked)"
                                    class="w-4 h-4 text-slate-900 bg-white border-slate-300 rounded focus:ring-slate-400 focus:ring-2 cursor-pointer">
                                <span class="text-sm font-medium text-slate-700">Vehículo Propio</span>
                            </label>
                        </div>
                    </div>

                    <div class="sm:col-span-2 lg:col-span-3 xl:col-span-4 flex justify-end pt-2">
                        <button (click)="onLimpiarFiltros.emit()"
                            class="px-5 py-2.5 text-sm text-slate-600 hover:text-slate-900 hover:bg-white rounded-lg transition-all font-semibold border-2 border-slate-200 hover:border-slate-300 shadow-sm">
                            Limpiar filtros
                        </button>
                    </div>
                </div>
            </div>
            }

            @if (tienesFiltrosActivos()) {
            <div class="px-4 md:px-6 pb-4 bg-white border-t border-slate-200">
                <div class="flex flex-wrap items-center gap-2 pt-4">
                    <span class="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                        Filtros activos:
                    </span>
                    @if (filtros().estado !== 'todos') {
                    <span class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-slate-100 text-slate-700 text-xs font-medium rounded-lg border border-slate-200 hover:bg-slate-200 transition-all">
                        <span>{{ getEstadoLabel(filtros().estado) }}</span>
                        <button (click)="handleEstadoChange('todos')" class="hover:bg-slate-300 rounded-full p-0.5 transition-colors">
                            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                        </button>
                    </span>
                    }
                    @if (filtros().provincia) {
                    <span class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-slate-100 text-slate-700 text-xs font-medium rounded-lg border border-slate-200 hover:bg-slate-200 transition-all">
                        <span>{{ filtros().provincia }}</span>
                        <button (click)="handleProvinciaChange('')" class="hover:bg-slate-300 rounded-full p-0.5 transition-colors">
                            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                        </button>
                    </span>
                    }
                    @if (filtros().experienciaMin) {
                    <span class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-slate-100 text-slate-700 text-xs font-medium rounded-lg border border-slate-200 hover:bg-slate-200 transition-all">
                        <span>{{ filtros().experienciaMin }}+ años exp.</span>
                        <button (click)="handleExperienciaMinChange('')" class="hover:bg-slate-300 rounded-full p-0.5 transition-colors">
                            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                        </button>
                    </span>
                    }
                    @if (filtros().carnetB) {
                    <span class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-slate-100 text-slate-700 text-xs font-medium rounded-lg border border-slate-200 hover:bg-slate-200 transition-all">
                        <span>Carnet B</span>
                        <button (click)="handleCarnetBChange(false)" class="hover:bg-slate-300 rounded-full p-0.5 transition-colors">
                            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                        </button>
                    </span>
                    }
                    @if (filtros().carnetC) {
                    <span class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-slate-100 text-slate-700 text-xs font-medium rounded-lg border border-slate-200 hover:bg-slate-200 transition-all">
                        <span>Carnet C</span>
                        <button (click)="handleCarnetCChange(false)" class="hover:bg-slate-300 rounded-full p-0.5 transition-colors">
                            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                        </button>
                    </span>
                    }
                    @if (filtros().vehiculoPropio) {
                    <span class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-slate-100 text-slate-700 text-xs font-medium rounded-lg border border-slate-200 hover:bg-slate-200 transition-all">
                        <span>Vehículo Propio</span>
                        <button (click)="handleVehiculoPropioChange(false)" class="hover:bg-slate-300 rounded-full p-0.5 transition-colors">
                            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                        </button>
                    </span>
                    }
                </div>
            </div>
            }
        </div>
    `
})
export class CandidatosFiltersComponent {
    filtros = input.required<FiltrosCandidatos>();

    onBusquedaChange = output<string>();
    onEstadoChange = output<string>();
    onProvinciaChange = output<string>();
    onExperienciaMinChange = output<string>();
    onOrdenarPorChange = output<string>();
    onCarnetBChange = output<boolean>();
    onCarnetCChange = output<boolean>();
    onVehiculoPropioChange = output<boolean>();
    onActualizar = output<void>();
    onLimpiarFiltros = output<void>();

    mostrarFiltrosAvanzados = signal(false);

    toggleFiltrosAvanzados(): void {
        this.mostrarFiltrosAvanzados.update(v => !v);
    }

    tienesFiltrosActivos(): boolean {
        const f = this.filtros();
        return f.estado !== 'todos' ||
            !!f.provincia ||
            !!f.experienciaMin ||
            !!f.carnetB ||
            !!f.carnetC ||
            !!f.vehiculoPropio;
    }

    // Métodos handler internos que emiten los eventos
    handleBusquedaChange(event: Event): void {
        const input = event.target as HTMLInputElement;
        this.onBusquedaChange.emit(input.value);
    }

    handleEstadoChange(value: string): void {
        this.onEstadoChange.emit(value);
    }

    handleProvinciaChange(value: string): void {
        this.onProvinciaChange.emit(value);
    }

    handleExperienciaMinChange(value: string): void {
        this.onExperienciaMinChange.emit(value);
    }

    handleOrdenarPorChange(value: string): void {
        this.onOrdenarPorChange.emit(value);
    }

    handleCarnetBChange(value: boolean): void {
        this.onCarnetBChange.emit(value);
    }

    handleCarnetCChange(value: boolean): void {
        this.onCarnetCChange.emit(value);
    }

    handleVehiculoPropioChange(value: boolean): void {
        this.onVehiculoPropioChange.emit(value);
    }

    getEstadoLabel(estado: string): string {
        const labels: Record<string, string> = {
            'sin_valorar': 'Sin valorar',
            'activo': 'Activo',
            'descartado': 'Descartado',
            'en_proceso': 'En proceso'
        };
        return labels[estado] || estado;
    }
}
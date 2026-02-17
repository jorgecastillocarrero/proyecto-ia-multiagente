// src/app/components/admin/admin.component.ts
import { ChangeDetectionStrategy, Component, signal, inject, computed, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LanguageService } from '../../services/language.service';
import { AdminAuthService } from '../../services/admin-auth.service';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { catchError, of, Subject, debounceTime, distinctUntilChanged } from 'rxjs';
import { environment } from '../../../environments/environment';

// Importar componentes
import { AdminDashboardStatsComponent, Estadisticas } from './dashboard/admin-dashboard-stats.component';
import { CandidatosFiltersComponent, FiltrosCandidatos } from './candidatos/candidatos-filters.component';
import { CandidatosTableComponent, Candidato, Paginacion } from './candidatos/candidatos-table.component';
import { CandidatoDetailModalComponent, DetalleCompleto } from './candidatos/candidato-detail-modal.component';
import { LinkGeneratorComponent } from './generador/link-generator.component';

const API_URL = environment.API_URL;

@Component({
    selector: 'app-admin',
    standalone: true,
    imports: [
        CommonModule,
        AdminDashboardStatsComponent,
        CandidatosFiltersComponent,
        CandidatosTableComponent,
        CandidatoDetailModalComponent,
        LinkGeneratorComponent
    ],
    templateUrl: './admin.component.html',
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AdminComponent {
    languageService = inject(LanguageService);
    adminAuthService = inject(AdminAuthService);
    router = inject(Router);
    http = inject(HttpClient);
    t = this.languageService.translations;

    // Estado de la vista actual
    vistaActual = signal<'inicio' | 'candidatos' | 'generador'>('inicio');

    // Datos de candidatos
    candidatos = signal<Candidato[]>([]);
    candidatosLoading = signal(false);

    // Modal de detalle
    modalAbierto = signal(false);
    detalleLoading = signal(false);
    candidatoSeleccionado = signal<DetalleCompleto | null>(null);

    // Filtros
    filtros = signal<FiltrosCandidatos>({
        estado: 'todos',
        busqueda: '',
        provincia: undefined,
        experienciaMin: undefined,
        experienciaMax: undefined,
        carnetB: undefined,
        carnetC: undefined,
        vehiculoPropio: undefined,
        ordenarPor: 'fecha'
    });

    // Paginación
    paginaActual = signal(1);
    totalPaginas = signal(1);
    totalCandidatos = signal(0);

    paginacion = computed<Paginacion>(() => ({
        actual: this.paginaActual(),
        total: this.totalPaginas(),
        totalCandidatos: this.totalCandidatos(),
        mostrados: this.candidatos().length
    }));

    // Estadísticas
    estadisticas = signal<Estadisticas>({
        candidatos_sin_valorar: 0,
        candidatos_activos: 0,
        candidatos_descartados: 0,
        pendientes_criba: 0,
        pendientes_llamar: 0,
        entrevistas_hoy: 0,
        puestos_activos: 0
    });

    // Subject para debounce de búsqueda
    private busquedaSubject = new Subject<string>();

    constructor() {
        // Configurar debounce para búsqueda
        this.busquedaSubject.pipe(
            debounceTime(500),
            distinctUntilChanged()
        ).subscribe(busqueda => {
            this.filtros.update(f => ({ ...f, busqueda }));
            this.paginaActual.set(1);
            this.cargarCandidatos();
        });

        this.cargarEstadisticas();
        this.cargarCandidatos();
    }

    // =========================================================================
    // NAVEGACIÓN
    // =========================================================================

    cambiarVista(vista: 'inicio' | 'candidatos' | 'generador'): void {
        this.vistaActual.set(vista);

        if (vista === 'candidatos') {
            this.cargarCandidatos();
        } else if (vista === 'inicio') {
            this.cargarEstadisticas();
        }
    }

    // =========================================================================
    // CANDIDATOS
    // =========================================================================

    cargarCandidatos(): void {
        this.candidatosLoading.set(true);

        const params: any = {
            page: this.paginaActual(),
            limit: 50
        };

        const f = this.filtros();

        // Debug: mostrar filtros activos
        console.log('🔍 Filtros actuales:', f);

        if (f.estado !== 'todos') {
            params.estado = f.estado;
        }

        if (f.busqueda) {
            params.search = f.busqueda;
        }

        if (f.provincia) {
            params.provincia = f.provincia;
        }

        if (f.experienciaMin) {
            params.experienciaMin = f.experienciaMin;
        }

        if (f.carnetB) {
            params.carnetB = 'true';
        }

        if (f.carnetC) {
            params.carnetC = 'true';
        }

        if (f.vehiculoPropio) {
            params.vehiculoPropio = 'true';
        }

        if (f.ordenarPor) {
            params.ordenarPor = f.ordenarPor;
        }

        // Debug: mostrar parámetros enviados al backend
        console.log('📤 Parámetros enviados al backend:', params);

        this.http.get<any>(`${API_URL}/rrhh/candidatos`, { params }).pipe(
            catchError(err => {
                console.error('❌ Error cargando candidatos:', err);
                this.candidatosLoading.set(false);
                return of({ success: false, data: [], pagination: { total: 0, totalPages: 0 } });
            })
        ).subscribe(result => {
            console.log('✅ Respuesta del backend:', result);
            if (result.success) {
                this.candidatos.set(result.data || []);
                this.totalCandidatos.set(result.pagination?.total || 0);
                this.totalPaginas.set(result.pagination?.totalPages || 1);
                console.log(`📊 Candidatos cargados: ${result.data?.length || 0} de ${result.pagination?.total || 0}`);
            }
            this.candidatosLoading.set(false);
        });
    }

    // Handlers de filtros
    onBusquedaChange(busqueda: string): void {
        // Usar el Subject para aplicar debounce
        this.busquedaSubject.next(busqueda);
    }

    onEstadoChange(estado: string): void {
        this.filtros.update(f => ({ ...f, estado }));
        this.paginaActual.set(1);
        this.cargarCandidatos();
    }

    onProvinciaChange(provincia: string): void {
        this.filtros.update(f => ({ ...f, provincia: provincia || undefined }));
        this.paginaActual.set(1);
        this.cargarCandidatos();
    }

    onExperienciaMinChange(valor: string): void {
        const experienciaMin = valor ? parseInt(valor) : undefined;
        this.filtros.update(f => ({ ...f, experienciaMin }));
        this.paginaActual.set(1);
        this.cargarCandidatos();
    }

    onOrdenarPorChange(ordenarPor: string): void {
        this.filtros.update(f => ({ ...f, ordenarPor: ordenarPor as any }));
        this.paginaActual.set(1);
        this.cargarCandidatos();
    }

    onCarnetBChange(carnetB: boolean): void {
        this.filtros.update(f => ({ ...f, carnetB: carnetB || undefined }));
        this.paginaActual.set(1);
        this.cargarCandidatos();
    }

    onCarnetCChange(carnetC: boolean): void {
        this.filtros.update(f => ({ ...f, carnetC: carnetC || undefined }));
        this.paginaActual.set(1);
        this.cargarCandidatos();
    }

    onVehiculoPropioChange(vehiculoPropio: boolean): void {
        this.filtros.update(f => ({ ...f, vehiculoPropio: vehiculoPropio || undefined }));
        this.paginaActual.set(1);
        this.cargarCandidatos();
    }

    onLimpiarFiltros(): void {
        this.filtros.set({
            estado: 'todos',
            busqueda: '',
            provincia: undefined,
            experienciaMin: undefined,
            experienciaMax: undefined,
            carnetB: undefined,
            carnetC: undefined,
            vehiculoPropio: undefined,
            ordenarPor: 'fecha'
        });
        this.paginaActual.set(1);
        this.cargarCandidatos();
    }

    cambiarPagina(pagina: number): void {
        this.paginaActual.set(pagina);
        this.cargarCandidatos();
    }

    verDetalleCandidato(candidato: Candidato): void {
        this.detalleLoading.set(true);
        this.modalAbierto.set(true);

        this.http.get<any>(`${API_URL}/rrhh/candidatos/${candidato.id}`).pipe(
            catchError(err => {
                console.error('Error cargando detalle:', err);
                this.detalleLoading.set(false);
                return of({ success: false, data: null });
            })
        ).subscribe(result => {
            if (result.success && result.data) {
                this.candidatoSeleccionado.set(result.data);
            }
            this.detalleLoading.set(false);
        });
    }

    cerrarModal(): void {
        this.modalAbierto.set(false);
        this.candidatoSeleccionado.set(null);
    }

    cargarEstadisticas(): void {
        this.http.get<any>(`${API_URL}/rrhh/estadisticas`).subscribe(result => {
            if (result.success) {
                this.estadisticas.set(result.data);
            }
        });
    }

    // Handler para clicks en estadísticas
    onFilterClick(estado: string): void {
        this.filtros.update(f => ({ ...f, estado }));
        this.cambiarVista('candidatos');
    }

    logout(): void {
        this.adminAuthService.logout();
        this.router.navigate(['/admin/auth']);
    }
}
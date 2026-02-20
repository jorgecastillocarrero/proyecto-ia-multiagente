# REPORTE SEMANAL RRHH

## Estructura del Reporte

El reporte semanal incluye las siguientes secciones:

### 1. OFERTAS ACTIVAS
Ordenadas por prioridad (MUY ALTA, ALTA, MEDIA, BAJA, MUY BAJA).

| Campo | Descripcion |
|-------|-------------|
| Prioridad | Nivel de urgencia |
| Perfil | Tipo de puesto |
| Posicion | Nombre del puesto |
| Plazas | Numero de vacantes |
| Portal | Donde se publico |
| Desde | Fecha inicio publicacion |
| Hasta | Fecha fin publicacion |
| Estado | ACTIVA / INACTIVA |

### 2. CANDIDATOS
Resumen por perfil.

| Campo | Descripcion |
|-------|-------------|
| Perfil | Tipo de puesto |
| Total | Candidatos totales |
| Sin Validar | Pendientes de clasificar |
| Con Duda | Con dudas pendientes |

### 3. ENTREVISTAS
Entrevistas programadas de la semana.

| Campo | Descripcion |
|-------|-------------|
| Dia | Fecha de la entrevista |
| Hora | Hora programada |
| Nombre | Nombre del candidato |
| Apellido | Apellido del candidato |
| Perfil | Tipo de puesto |
| Tipo | 1a Entrevista / 2a Entrevista |

### 4. CANDIDATOS EN CODIGOS
Candidatos aprendiendo codigos de productos.

| Campo | Descripcion |
|-------|-------------|
| Candidato | Nombre y apellido |
| Perfil | Tipo de puesto |
| Fecha 1a Entrev | Fecha de la primera entrevista |
| Codigos | Progreso (ej: 45/120) |
| Aciertos | Porcentaje de aciertos |
| Estado | En Progreso / LLAMAR |

**Estados:**
- **En Progreso**: Candidato aprendiendo codigos
- **LLAMAR**: Candidato listo para llamar y decidir 2a entrevista

### 5. CARNETS Y PERMISOS
Resumen de carnets disponibles en la bolsa de candidatos.

| Campo | Descripcion |
|-------|-------------|
| Tipo | Carnet B, Carnet C, CAP, Carretillero |
| Candidatos | Numero de candidatos con ese carnet |

---

## Ejemplo de Datos

### Candidatos en Codigos

| Candidato | Perfil | Fecha 1a Entrev | Codigos | Aciertos | Estado |
|-----------|--------|-----------------|---------|----------|--------|
| Manuel Perez | PESCADERIA | 10/02/2026 | 120/120 | 88% | LLAMAR |
| Adela Ruano | PESCADERIA | 15/02/2026 | 45/120 | 90% | En Progreso |
| Angel Garcia | LOGISTICA | 12/02/2026 | 80/120 | 75% | En Progreso |

---

*Documento: reporte_semanal.md*
*Fuente: tabla `peticiones_trabajador`, `candidatos`, `entrevistas`, `codigos_progreso`*

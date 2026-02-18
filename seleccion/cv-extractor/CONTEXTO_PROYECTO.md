# CONTEXTO PROYECTO - Sistema Seleccion RRHH
## Pescados La Carihuela
**Fecha:** 2026-02-18
**Para continuar en otro ordenador**

---

## 1. UBICACION DEL PROYECTO

```
C:\Users\usuario\seleccion\cv-extractor\
```

## 2. BASE DE DATOS

```
Host: 192.168.1.133
Puerto: 3306
Base de datos: gestion.pescadoslacarihuela.es
Usuario: root
Contraseña: Carihuela.Local#2026
```

## 3. TABLAS NUEVAS CREADAS

| Tabla | Descripcion |
|-------|-------------|
| `peticiones_trabajador` | Peticiones de nuevo personal (3 registros) |
| `alertas_peticion` | Alertas automaticas |
| `perfiles` | Perfiles profesionales |

## 4. TABLAS EXISTENTES USADAS

| Tabla | Uso |
|-------|-----|
| `candidatos` | 208 candidatos extraidos de CVs |
| `operadores` | Usuarios/trabajadores (roles ROLE_ADMIN, ROLE_USER) |
| `nuevo_carihuela_jorge_calendario_anual` | Semanas del año (Semana 7 actual) |

## 5. ARCHIVOS CREADOS

### Scripts Python
- `reporte_semanal.py` - Genera PDF semanal (Lunes 05:00)
- `setup_peticiones.py` - Crear tablas (ejecutar 1 vez)
- `generar_documentacion_pdf.py` - Genera PDF documentacion
- `estado_sistema.py` - Ver estado actual

### SQL
- `sql/crear_peticiones.sql` - SQL para crear tablas

### Reportes HTML (para validar)
- `reportes/reporte_semanal_RRHH.html` - Reporte semanal
- `reportes/documentacion_sistema.html` - Documentacion del sistema

## 6. ESTADO ACTUAL DEL REPORTE SEMANAL

Secciones completadas:
1. ✅ Necesidades de Personal (3 peticiones abiertas)
2. ✅ Candidatos por Perfil (LOGISTICA: 67, PRODUCCION: 18, PESCADERIA: 7, ADMINISTRATIVO: 4, SIN_CLASIFICAR: 112)
3. ✅ Estado de Candidatos (NUEVO: 183, ENTREVISTANDO: 25)
4. ✅ Carnets y Permisos (B: 141, C: 22)

Secciones pendientes:
- Candidatos por provincia
- Candidatos con vehiculo propio
- Valoraciones
- (otras que el usuario indique)

## 7. DOCUMENTACION DEL SISTEMA

Secciones:
1. ✅ Base de Datos (tablas nuevas y existentes)
2. ✅ Roles y Permisos (ROLE_ADMIN: 4, ROLE_USER: 193)
3. ✅ Peticion de Trabajador
4. ✅ Perfiles Profesionales
5. ✅ Archivos del Sistema

Notas:
- Lista de permisos: TABLA NO ENCONTRADA (estan en codigo Laravel, no en BD)
- Permiso nuevo a crear: "Buscar Nuevos Perfiles"

## 8. PETICIONES DE TRABAJADOR ACTUALES

| ID | Perfil | Posicion | Publicado | Estado |
|----|--------|----------|-----------|--------|
| 1 | LOGISTICA | Operario/a Logistica | InfoJobs 27/01-28/03 | ABIERTA |
| 2 | PESCADERIA | Dependiente/a Pescaderia | InfoJobs 13/02-14/04 | ABIERTA |
| 3 | BECARIO | Becario Administracion | - | ABIERTA |

## 9. PERFILES DISPONIBLES

- PESCADERIA
- LOGISTICA
- PRODUCCION
- ADMINISTRATIVO
- GESTION
- BECARIO

## 10. PROYECTOS RELACIONADOS

Los 3 proyectos comparten la misma BD:
1. `cv-extractor` - Extraccion y clasificacion de CVs (este proyecto)
2. `RRHH_Flujo_Trabajadores` - Gestion de trabajadores con contrato
3. `proyecto-ia-multiagente` - Sistema IA general

Documentacion relacionada:
- `C:\Users\usuario\RRHH_Flujo_Trabajadores_Contrato.md`

## 11. PARA CONTINUAR

1. Abrir Claude Code en el ordenador del trabajo
2. Navegar a: `C:\Users\usuario\seleccion\cv-extractor\`
3. Leer este archivo: `CONTEXTO_PROYECTO.md`
4. Continuar con el reporte semanal (secciones pendientes)

---

*Generado: 2026-02-18*

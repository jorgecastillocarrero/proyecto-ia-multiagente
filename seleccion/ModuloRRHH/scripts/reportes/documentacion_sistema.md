# DOCUMENTACION SISTEMA RRHH

**Pescados La Carihuela**

---

## 1. BASE DE DATOS

### Conexion

| Campo | Valor |
|-------|-------|
| Host | 192.168.1.133 |
| Puerto | 3306 |
| Base de datos | gestion.pescadoslacarihuela.es |
| Usuario | root |

### Tablas NUEVAS

| Tabla | Descripcion | Campos principales |
|-------|-------------|-------------------|
| `peticiones_trabajador` | Peticiones de nuevo personal | id, perfil_codigo, posicion, solicitante_rol, fecha_solicitud, publicado_en, estado |
| `alertas_peticion` | Alertas automaticas de peticiones | id, peticion_id, tipo_alerta, mensaje, estado |
| `perfiles` | Perfiles profesionales | id, codigo, nombre, descripcion, keywords, oferta_titulo, oferta_descripcion |

### Tablas EXISTENTES utilizadas

| Tabla | Descripcion | Uso en el sistema |
|-------|-------------|-------------------|
| `operadores` | Usuarios/Trabajadores | Datos de usuarios, roles (ROLE_ADMIN, ROLE_USER) |
| `nuevo_carihuela_jorge_calendario_anual` | Calendario anual | Obtener numero de semana, dias laborables |
| `candidatos` | Candidatos extraidos de CVs | Datos de candidatos para seleccion |

---

## 2. ROLES Y PERMISOS

### Roles en operadores

| Rol | Cantidad | Descripcion |
|-----|----------|-------------|
| `ROLE_ADMIN` | 4 | Administradores del sistema |
| `ROLE_USER` | 193 | Trabajadores normales |

### Administradores (ROLE_ADMIN)

| Nombre | Email |
|--------|-------|
| Antonio Manuel | - |
| Jorge | jorge@pescadoslacarihuela.es |
| Oficina | - |
| Servicio Tecnico | - |

### Modulos de Gestion

| ID | Modulo | Usuarios asignados |
|----|--------|-------------------|
| 1 | Gestion Vehiculos | CARLOS |
| 2 | Gestion Proveedores | CARLOS |
| 3 | Gestion Usuarios | CARLOS |
| 4 | Gestion Docu. Trabajadores | CARLOS |
| 5 | Gestion Articulos | CARLOS, JORGE LUIS |

### Permisos NUEVOS a crear

> **ACCION REQUERIDA:** Crear el siguiente permiso en la aplicacion y asignarlo a los roles correspondientes.

| Permiso | Descripcion | Roles sugeridos |
|---------|-------------|-----------------|
| **Buscar Nuevos Perfiles** | Acceso al modulo de seleccion RRHH para buscar y gestionar candidatos | ROLE_ADMIN, Director RRHH, Gerente |

---

## 3. PETICION DE TRABAJADOR

El proceso de seleccion comienza cuando el **Gerente** o el **Director de RRHH** solicita un nuevo trabajador.

### Datos de la Peticion

| Campo | Descripcion | Obligatorio |
|-------|-------------|-------------|
| ID | Identificador unico | Auto |
| Perfil | PESCADERIA, LOGISTICA, PRODUCCION, ADMINISTRATIVO, GESTION, BECARIO | SI |
| Posicion | Nombre especifico del puesto | SI |
| Solicitante | Gerente o Director RRHH | Auto |
| Fecha Solicitud | Fecha de creacion | SI |
| Publicado en | Donde se ha publicado (InfoJobs, etc.) | NO |
| Desde/Hasta | Periodo de publicacion | NO |
| Estado | ABIERTA, EN_PROCESO, CUBIERTA, CANCELADA | Auto |

### Peticiones Actuales

| ID | Perfil | Posicion | Fecha Sol. | Publicado | Desde | Hasta | Estado |
|----|--------|----------|------------|-----------|-------|-------|--------|
| 1 | LOGISTICA | Operario/a Logistica | 15/01/2026 | InfoJobs | 27/01/2026 | 28/03/2026 | ABIERTA |
| 2 | PESCADERIA | Dependiente/a Pescaderia | 13/02/2026 | InfoJobs | 13/02/2026 | 14/04/2026 | ABIERTA |
| 3 | BECARIO | Becario Administracion | 01/02/2026 | - | - | - | ABIERTA |

---

## 4. PERFILES PROFESIONALES

| Codigo | Descripcion |
|--------|-------------|
| PESCADERIA | Pescaderia, carniceria, comercio |
| LOGISTICA | Almacen, reparto, transporte |
| PRODUCCION | Fabrica, envasado, sushi |
| ADMINISTRATIVO | Oficina, secretariado |
| GESTION | Grados universitarios |
| BECARIO | Practicas, formacion |

---

## 5. ARCHIVOS DEL SISTEMA

### Scripts Python

| Archivo | Descripcion |
|---------|-------------|
| `reporte_semanal.py` | Genera PDF semanal automatico (Lunes 05:00) |
| `setup_peticiones.py` | Crear tablas de peticiones (ejecutar 1 vez) |
| `generar_documentacion_pdf.py` | Genera PDF de documentacion |

### Scripts SQL

| Archivo | Descripcion |
|---------|-------------|
| `sql/crear_peticiones.sql` | SQL para crear tablas peticiones_trabajador y alertas_peticion |

### Directorios

| Directorio | Contenido |
|------------|-----------|
| `reportes/` | PDFs y HTMLs generados |
| `sql/` | Scripts SQL |
| `docs/` | Documentacion markdown |

---

**Leyenda:**
- **NUEVO** = Tabla/archivo creado nuevo
- **MODIFICADA** = Tabla existente con cambios

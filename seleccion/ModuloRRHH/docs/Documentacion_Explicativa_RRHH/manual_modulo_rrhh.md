# MANUAL DEL MODULO RRHH - ERP La Carihuela

**Pescados La Carihuela**
**Fecha:** Febrero 2026
**Version:** 1.3

---

## INTRODUCCION

Este manual describe el funcionamiento del Modulo de Recursos Humanos (RRHH) en el sistema ERP de Pescados La Carihuela. El modulo gestiona todo el proceso desde la solicitud de personal hasta la contratacion.

---

## 1. PERFILES PROFESIONALES

### 1.1 Que son los Perfiles

Los perfiles son las categorias profesionales que utiliza la empresa para clasificar las ofertas de empleo y los candidatos que se reciben.

### 1.2 Perfiles Disponibles

| Codigo | Nombre | Puesto Tipico | Uso |
|--------|--------|---------------|-----|
| PESCADERIA | Pescaderia | Dependiente/a de Pescaderia | Personal de tienda, mostrador, corte y atencion al cliente |
| LOGISTICA | Logistica | Operario/a de Logistica | Almacen, reparto, conductores, carga/descarga |
| PRODUCCION | Produccion | Operario/a de Produccion | Sushi, sala de envase, linea de produccion |
| ADMINISTRATIVO | Administrativo | Administrativo/a | Oficina, secretariado, contabilidad |
| GESTION | Gestion | Responsable de Area | Titulados universitarios, puestos de responsabilidad |
| BECARIO | Becario | Becario/a en Practicas | Estudiantes en practicas |

---

## 2. PETICIONES DE TRABAJADOR

### 2.1 Que es una Peticion

Cuando un Gerente o Director de RRHH necesita contratar personal, crea una **Peticion de Trabajador** en el sistema.

### 2.2 Como Crear una Peticion

1. Acceder al modulo RRHH
2. Seleccionar "Nueva Peticion"
3. Elegir el **Perfil** (PESCADERIA, LOGISTICA, etc.)
4. Indicar la **Posicion** (nombre del puesto)
5. Indicar el numero de **Plazas**
6. Guardar

### 2.3 Campos de la Peticion

| Campo | Descripcion | Obligatorio |
|-------|-------------|-------------|
| Perfil | Categoria profesional | SI |
| Posicion | Nombre especifico del puesto | SI |
| Plazas | Numero de vacantes | SI |
| Prioridad | Urgencia de la peticion | SI |
| Solicitante | Quien hace la peticion (automatico) | AUTO |
| Fecha Solicitud | Fecha de creacion (automatico) | AUTO |
| Portal | Donde se publica (InfoJobs, LinkedIn, etc.) | NO |
| Desde | Fecha inicio publicacion | NO |
| Hasta | Fecha fin publicacion | NO |
| Estado | ACTIVA o INACTIVA | AUTO |

### 2.4 Prioridades

| Prioridad | Uso |
|-----------|-----|
| MUY_ALTA | Urgente, cubrir inmediatamente |
| ALTA | Prioritario |
| MEDIA | Normal (por defecto) |
| BAJA | Puede esperar |
| MUY_BAJA | Sin urgencia |

### 2.5 Estados de la Peticion

| Estado | Significado |
|--------|-------------|
| ACTIVA | El anuncio esta publicado en internet |
| INACTIVA | El anuncio no esta visible |

### 2.5 Vista en el ERP

**Pantalla: Peticiones de Trabajador**

| ID | Perfil | Posicion | Plazas | Solicitante | Fecha Sol. | Portal | Desde | Hasta | Estado |
|----|--------|----------|--------|-------------|------------|--------|-------|-------|--------|
| 1 | LOGISTICA | Operario/a Logistica | 2 | Gerente | 15/01/2026 | InfoJobs | 27/01/2026 | 28/03/2026 | ACTIVA |
| 2 | PESCADERIA | Dependiente/a Pescaderia | 2 | Gerente | 13/02/2026 | InfoJobs | 13/02/2026 | 14/04/2026 | ACTIVA |
| 3 | BECARIO | Becario Administracion | 1 | Gerente | 01/02/2026 | - | - | - | ACTIVA |

---

## 3. ENTRADA DE CVs Y CANDIDATOS

### 3.1 Como Llegan los CVs

Los CVs llegan automaticamente desde los portales de empleo donde se publican las ofertas (InfoJobs, LinkedIn, etc.).

### 3.2 Vista de Candidatos por Perfil

| Perfil | Total | Sin Validar | Con Duda |
|--------|-------|-------------|----------|
| LOGISTICA | 67 | 65 | 2 |
| PRODUCCION | 18 | 17 | 1 |
| PESCADERIA | 7 | 4 | 3 |
| ADMINISTRATIVO | 4 | 4 | 0 |
| SIN CLASIFICAR | 216 | 216 | 0 |
| **TOTAL** | **312** | **306** | **6** |

### 3.3 Candidatos Pendientes de Clasificar

Los candidatos sin perfil asignado aparecen en esta vista:

| ID | Nombre | Apellido | Telefono | Localidad | Veh | B | C | CAP | Car | Exp | CV | Asignar |
|----|--------|----------|----------|-----------|-----|---|---|-----|-----|-----|-----|---------|
| 1 | ADAMA | FOFANA | 633 171 068 | - | N | N | N | N | N | 12.1 | [+] | [ v ] |

**Desplegable Asignar:**
- PESCADERIA, LOGISTICA, PRODUCCION, ADMINISTRATIVO, GESTION, BECARIO → Asigna perfil
- NO → Va a DESCARTADOS

### 3.4 Candidatos con Perfil - Sin Validar

Los candidatos con perfil pero sin validar aparecen en su listado correspondiente:

| ID | Nombre | Apellido | Telefono | Localidad | Veh | B | C | CAP | Car | Exp | CV | Entrevista |
|----|--------|----------|----------|-----------|-----|---|---|-----|-----|-----|-----|------------|
| 65 | Adela | Ruano | 675 942 449 | Cordoba | S | S | N | N | N | 20.3 | [+] | Pendiente |

**Desplegable Entrevista:**
- Pendiente → Esperando decision
- Si → Pasa a llamadas para entrevistas
- No → Va a DESCARTADOS

### 3.5 Candidatos con Perfil - Con Duda

Los candidatos que tienen una duda pendiente de resolver:

| ID | Nombre | Apellido | Telefono | Duda | Respuesta | Accion |
|----|--------|----------|----------|------|-----------|--------|
| 72 | Carmen | Lopez | 654 123 456 | Solo quiere tienda Barraquer | [ ] | [ v ] |

**Desplegable Accion:**
- Si → Escribe respuesta para el Llamador → Vuelve a Llamadas
- No → Descartado con Motivo = la Duda

---

## 4. TIPOS DE DESCARTE

### 4.1 Descartes Automaticos

El sistema descarta automaticamente candidatos segun reglas configurables:

| Regla | Condicion | Motivo |
|-------|-----------|--------|
| REGLA_EXPERIENCIA | Experiencia < 1 ano | Experiencia menor a 1 ano |
| REGLA_DISTANCIA | Distancia > 40 km | Distancia mayor a 40 km |

### 4.2 Descartes Manuales

El usuario puede descartar candidatos seleccionando un motivo:

| Motivo | Descripcion |
|--------|-------------|
| MALAS_REFERENCIAS | Malas referencias |
| NO_INTERESADO | Candidato no interesado |
| NO_CONTESTA | No contesta tras varios intentos |
| DESCARTADO_ENTREVISTA | Descartado tras entrevista |
| OTROS | Otros motivos |

### 4.3 Acceso en el ERP

**Menu:** RRHH > Configuracion > Descartes

- **Motivos de Descarte**: Configurar motivos automaticos y manuales
- **Reglas Automaticas**: Configurar condiciones para descarte automatico
- **Candidatos Descartados**: Ver historial de candidatos descartados

---

## 5. LLAMADAS PARA ENTREVISTAS

### 5.1 Que es

Cuando un candidato se marca como "Entrevista = Si", pasa a la fase de llamadas donde el Llamador contacta al candidato para concertar una cita de entrevista.

### 5.2 Vista en el ERP

**Menu:** RRHH > Llamadas > Llamadas para Entrevistas

| ID | Nombre | Apellido | Telefono | Localidad | Veh | B | C | CAP | Car | Exp | CV | Estado | Intentos | Notas | Dia | Hora |
|----|--------|----------|----------|-----------|-----|---|---|-----|-----|-----|-----|--------|----------|-------|-----|------|
| 65 | [Adela] | [Ruano] | [675 942 449] | [Cordoba] | [S] | [S] | [N] | [N] | [N] | [20.3] | [+] | Si | 1 | interesada | 21/02 | 10:00 |

**Nota:** Los campos entre corchetes son editables para corregir errores de extraccion del CV.

### 5.3 Campos de la Vista

| Campo | Descripcion |
|-------|-------------|
| Estado | Si / No / Duda |
| Intentos | 1, 2, 3, 4, 5 (descarte automatico configurable) |
| Notas | Comentarios de la llamada |
| Dia | Fecha de la entrevista (solo si Estado = Si) |
| Hora | Hora de la entrevista (solo si Estado = Si) |

### 5.4 Opciones de Estado

| Estado | Que pasa |
|--------|----------|
| **Si** | Aparecen campos Dia y Hora. El candidato pasa a ENTREVISTAS |
| **No** | El candidato pasa a DESCARTADOS |
| **Duda** | El candidato vuelve a PERFILES (pestana Con Duda) para que el Evaluador decida |

### 5.5 Flujo de Dudas

1. **Llamador** marca "Duda" con comentario: "Solo quiere trabajar en tienda Barraquer"
2. El candidato aparece en **PERFILES > Con Duda**
3. **Evaluador** ve la duda y decide:
   - **Si es No**: Descartado con Motivo = la Duda
   - **Si es Si**: Escribe nota para el Llamador y vuelve a Llamadas
4. **Llamador** ve la nota, llama de nuevo y marca Si/No

### 5.6 Ejemplos de Notas

| Estado | Ejemplo de Nota |
|--------|-----------------|
| Si | "Interesada en el sector, tiene experiencia" |
| No | "Trabajando actualmente, pero buena impresion para el futuro" |
| Duda | "Quiere saber cuales son los turnos de trabajo" |

---

## 6. OFERTAS DE EMPLEO

### 6.1 Ofertas por Perfil

Cada perfil tiene una plantilla de oferta de empleo lista para publicar:

| Perfil | Titulo Oferta | Estado |
|--------|---------------|--------|
| PESCADERIA | Dependiente/a de Pescaderia | Documentada |
| LOGISTICA | Operario/a de Logistica de Almacen | Documentada |
| PRODUCCION | Operario/a de Produccion | Pendiente |
| ADMINISTRATIVO | Administrativo/a | Pendiente |
| GESTION | Responsable de Area | Pendiente |
| BECARIO | Becario/a en Practicas | Pendiente |

### 6.2 Vista Dashboard - Ofertas por Perfil

| Perfil | Titulo | Plazas | Creacion | Portal | Publicada | Desde | Hasta |
|--------|--------|--------|----------|--------|-----------|-------|-------|
| LOGISTICA | Operario/a Logistica | 2 | 15/01/2026 | InfoJobs | Si | 27/01/2026 | 28/03/2026 |
| PESCADERIA | Dependiente/a Pescaderia | 2 | 13/02/2026 | InfoJobs | Si | 13/02/2026 | 14/04/2026 |
| PRODUCCION | Operario/a Produccion | 0 | - | - | No | - | - |
| ADMINISTRAT. | Administrativo/a | 0 | - | - | No | - | - |
| GESTION | Responsable de Area | 0 | - | - | No | - | - |
| BECARIO | Becario Administracion | 1 | 01/02/2026 | - | No | - | - |

---

## 7. ROLES Y PERMISOS

### 7.1 Roles en el Modulo RRHH

| Rol | Responsabilidades |
|-----|-------------------|
| Director RRHH | Completar datos contrato, firmar documentos |
| Gerente | Crear peticiones de trabajador |
| Llamador | Llamar candidatos, concertar entrevistas |
| Evaluador | Revisar perfiles, resolver dudas, decidir si/no |
| Entrevistador | Realizar entrevistas, evaluar candidatos |

---

## 8. DASHBOARD RRHH

### 8.1 Que es

El Dashboard RRHH es la pantalla principal donde los roles de Evaluador, Entrevistador, Director RRHH y Gerente ven el resumen del proceso de seleccion.

**Acceso:** Menu RRHH > Dashboard

### 8.2 Secciones del Dashboard

#### 1. OFERTAS ACTIVAS

Muestra las ofertas de empleo publicadas actualmente, ordenadas por prioridad.

| Prioridad | Perfil | Posicion | Plazas | Portal | Desde | Hasta | Estado |
|-----------|--------|----------|--------|--------|-------|-------|--------|
| MUY_ALTA | PESCADERIA | Dependiente/a Pescaderia | 2 | InfoJobs | 13/02/2026 | 14/04/2026 | ACTIVA |
| ALTA | LOGISTICA | Operario/a Logistica | 2 | InfoJobs | 27/01/2026 | 28/03/2026 | ACTIVA |

#### 2. CANDIDATOS

Resumen de candidatos por perfil con su estado de validacion.

| Perfil | Total | Sin Validar | Con Duda |
|--------|-------|-------------|----------|
| LOGISTICA | 67 | 65 | 2 |
| PESCADERIA | 7 | 4 | 3 |
| PRODUCCION | 18 | 17 | 1 |
| **TOTAL** | **312** | **306** | **6** |

#### 3. ENTREVISTAS

Lista de entrevistas programadas ordenadas por dia y hora.

| Dia | Hora | Nombre | Apellido | Perfil | Tipo |
|-----|------|--------|----------|--------|------|
| 19/02/2026 | 10:00 | Adela | Ruano | PESCADERIA | 1a Entrevista |
| 20/02/2026 | 09:00 | Carmen | Lopez | PESCADERIA | 2a Entrevista |

### 8.3 Reporte Semanal

Estas mismas 3 secciones se incluyen en el Reporte Semanal RRHH que se genera automaticamente.

---

## 9. DASHBOARD LLAMADOR

### 9.1 Que es

El Dashboard Llamador tiene 2 pantallas para gestionar las llamadas a candidatos.

### 9.2 Pantalla 1: Panel Principal

**Acceso:** Menu RRHH > Mi Panel

Resumen de llamadas pendientes ordenadas por prioridad + entrevistas del dia.

```
+--------------------------------------------------+
|  LLAMADAS PARA ENTREVISTAS                       |
+--------------------------------------------------+
|                                                  |
|  [!] MUY ALTA                                    |
|      Dependiente/a de Pescaderia .......... 15   |
|                                                  |
|  [!] ALTA                                        |
|      Operario/a Logistico ................. 6    |
|                                                  |
|  [ ] MEDIA                                       |
|      Becario Administracion ............... 3    |
|                                                  |
+--------------------------------------------------+

+--------------------------------------------------+
|  ENTREVISTAS DE HOY                              |
+--------------------------------------------------+
|                                                  |
|  10:00  Adela Ruano - PESCADERIA - 1a Entrev.    |
|  11:30  Angel Garcia - LOGISTICA - 1a Entrev.    |
|  16:00  Carmen Lopez - PESCADERIA - 2a Entrev.   |
|                                                  |
+--------------------------------------------------+
```

- Clic en Llamadas → abre Pantalla 2 (Llamadas por Perfil)
- Entrevistas de Hoy → para gestionar con el Entrevistador cuando llegue el candidato

### 9.3 Pantalla 2: Llamadas por Perfil

**Acceso:** Clic en perfil desde Panel Principal

| ID | Nombre | Apellido | Telefono | Perfil | Veh | B | C | CAP | Car | Exp | CV | Estado | Intentos | Notas |
|----|--------|----------|----------|--------|-----|---|---|-----|-----|-----|-----|--------|----------|-------|
| 65 | [Adela] | [Ruano] | [675 942 449] | PESCADERIA | [S] | [S] | [N] | [N] | [N] | [20.3] | [+] | [ v ] | [ v ] | [ ] |

**Campos editables** (entre corchetes): para corregir errores del CV

**Si Estado = Si:** aparecen columnas Dia y Hora

| ID | Nombre | Apellido | Telefono | Estado | Intentos | Notas | Dia | Hora |
|----|--------|----------|----------|--------|----------|-------|-----|------|
| 65 | [Adela] | [Ruano] | [675 942 449] | Si | 1 | interesada | [21/02] | [10:00] |

### 9.4 Funcionamiento

| Accion | Resultado |
|--------|-----------|
| Marca **Si** | Candidato sale de la lista, contador -1, aparecen campos Dia/Hora |
| Marca **No** | Candidato sale de la lista, va a Descartados |
| Marca **Duda** | Candidato sale de la lista, va a Perfiles (Con Duda) |

### 9.5 Entrevistas de Hoy - Desplegable

Cada entrevista del dia tiene un desplegable:

| Opcion | Que pasa |
|--------|----------|
| **Presentado** | El candidato ha llegado, pasa a la pantalla de Entrevista |
| **No Presentado** | El candidato va a DESCARTADOS (motivo: NO_ASISTIO, sin email) |

### 9.6 Pantalla: Realizar Entrevista

Cuando se marca "Presentado", el Entrevistador ve esta pantalla:

| Campo | Descripcion |
|-------|-------------|
| Candidato | Nombre y apellido |
| Perfil | Perfil asignado |
| Tipo | 1a o 2a Entrevista |
| CV | Enlace al CV completo |
| Notas llamada | Lo que anoto el Llamador |
| Notas entrevista | Campo para escribir observaciones |
| Resultado | Desplegable: Entrega Codigos / Duda / No |

**Opciones de Resultado:**

| Resultado | Que pasa |
|-----------|----------|
| **Entrega Codigos** | Email automatico + acceso al Sistema de Codigos |
| **Duda** | Se queda en Entrevistas con notas |
| **No** | Descartados + Email automatico de rechazo |

---

## 10. EMAILS AUTOMATICOS

### 10.1 Que son

El sistema envia emails automaticos a los candidatos en ciertos momentos del proceso de seleccion.

### 10.2 Email de Entrega de Codigos

**Cuando se envia:** Cuando el Entrevistador marca "Entrega Codigos" en la entrevista (candidato seleccionado).

**Contenido:**
- Saludo y agradecimiento por participar en el proceso
- Confirmacion de que ha superado la entrevista
- Enlace al sistema de aprendizaje de codigos
- Datos de contacto para dudas

### 10.3 Email de Rechazo tras Entrevista

**Cuando se envia:** Cuando el Entrevistador marca "No" en la 1a o 2a entrevista **y el candidato se presento**.

**Contenido:**
- Saludo y agradecimiento por participar
- Comunicacion de que no continua en el proceso
- Invitacion a seguir futuras ofertas
- Datos de contacto

**Nota:** Este email solo se envia cuando el candidato ha realizado una entrevista (1a o 2a). No se envia en rechazos previos (clasificacion, llamadas, etc.).

### 10.4 Candidato No Presentado

**Cuando ocurre:** El Llamador marca "No Presentado" en las Entrevistas de Hoy.

**Que pasa:**
- El candidato va directamente a DESCARTADOS
- Motivo de descarte: NO_ASISTIO
- **NO se envia email** de rechazo

---

## 11. UBICACION DE DATOS

### 10.1 Tablas en Base de Datos

| Tabla | Descripcion |
|-------|-------------|
| perfiles | Perfiles profesionales + ofertas de empleo |
| peticiones_trabajador | Peticiones de personal |
| candidatos | Candidatos en proceso |
| asignacion_llamadas | Llamadas para concertar entrevistas |
| entrevistas | Entrevistas programadas y realizadas |
| motivos_descarte | Catalogo de motivos de descarte |
| reglas_descarte | Reglas automaticas de descarte |
| candidatos_descartados | Historial de descartados |

### 10.2 Servidor

- **IP:** 192.168.1.133
- **Base de datos:** gestion.pescadoslacarihuela.es

---

## 11. DOCUMENTOS GENERADOS

El sistema genera documentacion en tres formatos:

| Formato | Extension | Uso |
|---------|-----------|-----|
| Markdown | .md | Edicion y control de versiones |
| HTML | .html | Visualizacion en navegador |
| PDF | .pdf | Impresion y distribucion |

---

*Manual del Modulo RRHH - Pescados La Carihuela - Version 1.3*

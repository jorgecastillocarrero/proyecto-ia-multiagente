# Flujo de Trabajo RRHH - Sistema de Seleccion

## Resumen del Sistema

Sistema de gestion de candidatos para el proceso de seleccion de personal. Los candidatos pueden entrar por dos vias:
1. **InfoJobs**: Se descargan CVs de ofertas publicadas (15-20 por lote)
2. **Email directo**: CVs que llegan a empleo@pescadoslacarihuela.es

**Todos los CVs pasan por los mismos filtros automaticos**, independientemente de su origen.

---

## Estados del Candidato (campo `estado` en tabla candidatos)

| Estado | Descripcion |
|--------|-------------|
| `sin_valorar` | CV recien llegado, pendiente de revisar |
| `activo` | Candidato en proceso de seleccion (incluye todas las fases) |
| `descartado` | Candidato que no cumple requisitos o fue rechazado |

> **IMPORTANTE**: El estado `activo` incluye todas las fases del proceso: primera criba, llamadas, entrevistas, stand_by, segunda entrevista, etc. El detalle de cada fase se gestiona en la tabla `candidatos_puestos`.

---

## 1. Entrada de CVs

### Via InfoJobs
1. Se publica puesto en **InfoJobs** (ej: "Operario de Logistica")
2. El responsable asignado entra a InfoJobs
3. Selecciona 15-20 CVs
4. Los descarga como PDF
5. Los carga en el sistema

### Via Email Directo (Automatizado)
1. CV llega a **empleo@pescadoslacarihuela.es**
2. El sistema detecta el nuevo email con CV adjunto
3. Extrae el CV automaticamente (PDF -> datos estructurados)
4. Sube el candidato al sistema
5. Aplica las reglas automaticas de descarte
6. El email se mueve a la carpeta **"CVs_Procesados"**
7. Borrado manual de la carpeta cada ~1 mes

---

## 2. Descarte Automatico (Primera Criba)

El sistema descarta automaticamente candidatos que cumplan **CUALQUIERA** de estos criterios:

| # | Codigo | Motivo de Descarte | Descripcion |
|---|--------|-------------------|-------------|
| 1 | `DESCARTADO_PREVIO` | **Descartado previamente** | Ha sido descartado en cualquier puesto anterior |
| 2 | `DISTANCIA_EXCEDIDA` | **Distancia > 40km** | Vive a mas de 40 km en coche de Cordoba |
| 3 | `SIN_EXPERIENCIA` | **Sin experiencia** | No tiene experiencia o tiene menos de 1 ano |
| 4 | `PUESTO_NO_RELACIONADO` | **Puesto no relacionado** | Su puesto deseado no tiene relacion con el puesto publicado |

> **NOTA**: Los criterios de descarte son configurables por puesto.

---

## 3. Revision Manual (Segunda Criba)

Tras el descarte automatico, el responsable (Antonio, Carlos, Jorge...) revisa los CVs desde su **dashboard**.

### Dashboard del Revisor
Antonio, Carlos o Jorge acceden al dashboard donde ven la lista de candidatos pendientes de revisar. Desde ahi pueden ver el CV completo y decidir si el candidato pasa a la siguiente fase o es descartado.

### Si NO interesa:
- Pasa a **DESCARTADOS**
- Se registra motivo: `NO_SELECCIONADO` - "No seleccionado por [nombre]"
- Queda en base de datos de descartados

### Si INTERESA:
- Se marca como **SELECCIONADO PARA LLAMAR**
- Se genera automaticamente **orden de trabajo**
- La orden aparece en el dashboard de la persona encargada de llamar

---

## 4. Fase de Llamadas

El responsable de llamadas ve en su dashboard:

```
+----------------------------------+
|  Llamar para entrevistas: 0/20   |
+----------------------------------+
```

### Proceso de llamada:
1. Se verifican los datos del candidato (nombre, direccion, disponibilidad)
2. Se confirma que los datos del CV son correctos
3. Se verifica el interes mutuo:
   - El candidato sigue interesado en el puesto
   - La empresa confirma interes en el candidato
4. Si hay interes mutuo, se programa la entrevista

### Resultados posibles:

| Resultado | Codigo | Accion |
|-----------|--------|--------|
| **Contesta + Verifica + Interes mutuo** | - | Se programa entrevista |
| **Contesta + No interesado** | `NO_INTERESADO` | Pasa a DESCARTADOS |
| **Contesta + Datos incorrectos** | - | Se actualiza CV o descarta |
| **No contesta** | (se reintenta) | Se reintenta hasta X veces |
| **No contesta (max intentos)** | `NO_CONTACTADO` | Pasa a DESCARTADOS |

---

## 5. Primera Entrevista

El entrevistador ve en su dashboard:

```
+---------------------------------------------+
|  ENTREVISTAS HOY - 12/02/2026               |
+---------------------------------------------+
|  09:00 - Juan Garcia - Operario Logistica   |
|  10:30 - Maria Lopez - Operario Logistica   |
|  12:00 - Pedro Ruiz - Operario Logistica    |
+---------------------------------------------+
```

### Resultado de la Primera Entrevista:

| Resultado | Codigo | Accion |
|-----------|--------|--------|
| **Pasa la entrevista** | - | Se entregan codigos -> STAND_BY |
| **Descartado** | `DESCARTADO_ENTREVISTA` | Pasa a DESCARTADOS con notas |
| **No asistio** | `NO_ASISTIO` | DESCARTADO: No ha venido a la entrevista |

---

## 6. STAND_BY (Post Primera Entrevista)

Cuando el candidato pasa la primera entrevista, se le entregan los codigos y queda en estado **STAND_BY**.

### Tareas Pendientes en STAND_BY:

| Tarea | Descripcion |
|-------|-------------|
| 1. Segunda entrevista | Llamar para concertar segunda entrevista |
| 2. Preguntar codigos | Llamar para verificar que tiene los codigos |

### Llamada para Segunda Entrevista:
- Si **PUEDE** en la fecha/hora propuesta -> Se confirma segunda entrevista
- Si **NO PUEDE** -> El candidato indica cuando puede el
- Se registra todo en el campo **NOTAS**

Ejemplo de NOTAS:
```
15/02 - Propuesto 17/02 a las 10:00
15/02 - No puede, dice que puede el 19/02 manana
16/02 - Confirmado: 19/02 a las 09:30
```

### Si el candidato ya no esta interesado:
- Pasa a DESCARTADO con motivo `NO_INTERESADO_POST_ENTREV`

---

## 7. Segunda Entrevista

Una vez confirmada la fecha y hora, el candidato pasa a estado **SEGUNDA_ENTREVISTA_PROGRAMADA**.

### Resultado de la Segunda Entrevista:

| Resultado | Codigo | Accion |
|-----------|--------|--------|
| **Pasa la entrevista** | - | SELECCIONADO_FINAL -> Contratacion |
| **Descartado** | `DESCARTADO_ENTREVISTA` | Pasa a DESCARTADOS con notas |
| **No asistio** | `NO_ASISTIO` | DESCARTADO: No ha venido a la entrevista |

---

## 8. Diagrama de Flujo

```
                    +---------------+
                    |  ENTRADA CV   |
                    +-------+-------+
                            |
                            v
              +---------------------------+
              | Cumple criterios descarte?|
              +---------------------------+
                SI /           \ NO
                  /             \
                 v               v
    +------------------+    +------------------+
    | DESCARTADO_AUTO  |    |  PRIMERA_CRIBA   |
    +------------------+    +--------+---------+
                                     |
                                     v
                       +------------------------+
                       |   Interesa a RRHH?     |
                       +------------------------+
                         NO /           \ SI
                           /             \
                          v               v
           +------------------+    +------------------+
           |DESCARTADO_MANUAL |    | SELEC_LLAMAR     |
           +------------------+    +--------+---------+
                                            |
                                            v
                              +------------------------+
                              |  Contesta telefono?    |
                              +------------------------+
                              NO(3x) /         \ SI
                                   /           \
                                  v             v
                   +---------------+    +------------------+
                   | NO_CONTACTADO |    | Interes mutuo?   |
                   +---------------+    +------------------+
                                          NO /       \ SI
                                            /         \
                                           v           v
                            +---------------+    +------------------+
                            | NO_INTERESADO |    | ENTREV_PROGRAMADA|
                            +---------------+    +--------+---------+
                                                          |
                                                          v
                                            +------------------------+
                                            | Asiste a entrevista?   |
                                            +------------------------+
                                              NO /           \ SI
                                                /             \
                                               v               v
                                 +------------+    +---------------------+
                                 | NO_ASISTIO |    | Pasa 1a entrevista? |
                                 +------------+    +---------------------+
                                                     NO /         \ SI
                                                       /           \
                                                      v             v
                                    +------------------+    +------------------+
                                    |DESCARTADO_ENTREV |    | STAND_BY+CODIGOS |
                                    +------------------+    +--------+---------+
                                                                     |
                                                                     v
                                                      +------------------------+
                                                      |   Sigue interesado?    |
                                                      +------------------------+
                                                        NO /           \ SI
                                                          /             \
                                                         v               v
                                       +---------------------+    +------------------+
                                       |NO_INTERES_POST_ENTR |    |2a ENTREV PROGRAM |
                                       +---------------------+    +--------+---------+
                                                                           |
                                                                           v
                                                            +------------------------+
                                                            | Pasa 2a entrevista?    |
                                                            +------------------------+
                                                              NO /           \ SI
                                                                /             \
                                                               v               v
                                                  +------------+    +------------------+
                                                  | DESCARTADO |    |SELECCIONADO FINAL|
                                                  +------------+    +------------------+
```

---

## 9. Regla de Reactivacion

Un candidato DESCARTADO puede volver a ser ACTIVO si:
- Envia nuevo CV con datos actualizados
- El motivo de descarte ya no aplica

**Ejemplos:**
- Estaba descartado por vivir a +40km -> Ahora envia CV con direccion en Cordoba
- Estaba descartado por poca experiencia -> Ahora tiene mas experiencia

El sistema debe detectar estos cambios y notificar al revisor.

---

## 10. Roles del Sistema

| Rol | Funciones |
|-----|-----------|
| **Admin** | Configura puestos, motivos, asignaciones |
| **Cargador** | Sube PDFs al sistema |
| **Revisor** | Hace la segunda criba manual |
| **Llamador** | Contacta candidatos seleccionados |
| **Entrevistador** | Realiza entrevistas |

---

## 11. Motivos de Descarte

### Automaticos (Sistema)
| Codigo | Descripcion |
|--------|-------------|
| `DESCARTADO_PREVIO` | Descartado previamente en otro puesto |
| `DISTANCIA_EXCEDIDA` | Vive a mas de 40 km de Cordoba |
| `SIN_EXPERIENCIA` | Sin experiencia o menos de 1 ano |
| `PUESTO_NO_RELACIONADO` | Puesto deseado no relacionado |

### Manuales (Usuario)
| Codigo | Descripcion |
|--------|-------------|
| `NO_SELECCIONADO` | No seleccionado por el revisor |
| `NO_INTERESADO` | Candidato no interesado en el puesto |
| `NO_CONTACTADO` | No se ha conseguido contactar |
| `DESCARTADO_ENTREVISTA` | Descartado tras la entrevista |
| `NO_ASISTIO` | No ha venido a la entrevista |
| `NO_INTERESADO_POST_ENTREV` | No interesado despues de 1a entrevista |

---

## 12. Configuracion del Sistema

| Parametro | Valor por defecto | Descripcion |
|-----------|-------------------|-------------|
| `intentos_llamada_max` | 3 | Intentos antes de descartar por no contactar |
| `distancia_maxima_default` | 40 km | Distancia maxima desde Cordoba |
| `experiencia_minima_default` | 1 ano | Experiencia minima requerida |

---

## 13. Automatizacion de Recepcion por Email

### Flujo Automatico:
1. Llega CV a **empleo@pescadoslacarihuela.es**
2. El sistema detecta el nuevo email con CV adjunto
3. Extrae el CV automaticamente
4. Sube el candidato al sistema
5. Aplica las reglas automaticas de descarte
6. El email se mueve a la carpeta **"CVs_Procesados"**

### Gestion de Emails Procesados:
| Accion | Descripcion |
|--------|-------------|
| Mover a carpeta | El email desaparece de bandeja principal -> CVs_Procesados |
| Retencion | Los emails se mantienen en la carpeta ~1 mes |
| Borrado manual | El equipo decide cuando vaciar la carpeta |

---

## 14. Estructura de la Base de Datos

### Campo `estado` en tabla candidatos

| Valor | Descripcion |
|-------|-------------|
| `sin_valorar` | CV pendiente de revisar (estado inicial) |
| `activo` | En proceso de seleccion (todas las fases) |
| `descartado` | Descartado del proceso |

### Tablas Principales

| Tabla | Descripcion |
|-------|-------------|
| `candidatos` | Datos personales, carnets, contacto + campo ESTADO |
| `experiencias` | Historial laboral de cada candidato |
| `puestos` | Puestos de trabajo publicados con requisitos |
| `candidatos_puestos` | Relacion candidato-puesto con estado del flujo |
| `motivos_descarte` | Catalogo de motivos de descarte |
| `usuarios` | Usuarios del sistema (revisores, llamadores, etc.) |
| `llamadas` | Registro de intentos de contacto |
| `entrevistas` | Entrevistas programadas y realizadas |
| `configuracion` | Parametros del sistema |
| `log_acciones` | Auditoria de acciones realizadas |

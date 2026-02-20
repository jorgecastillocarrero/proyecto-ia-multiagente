# MODULO RRHH - SELECCION

---

## PANTALLAS DEL ERP - SELECCION

### Resumen de Pantallas

| # | Pantalla | Funcion | Accion Principal |
|---|----------|---------|------------------|
| 1 | Candidatos | Clasificar y validar | Asignar perfil / Si / No / Duda |
| 2 | Llamadas | Concertar citas | Si (+ Dia/Hora) / No / Duda |
| 3 | Entrevistas | Realizar entrevistas | Entrega Codigos / No / Duda |
| 4 | Codigos | Aprendizaje productos | Completado / Pendiente |
| 5 | Contratado | Fin del proceso | Documentacion |

### Permisos por Rol

| Pantalla | Seleccionador | Llamador | Entrevistador | Director RRHH | Gerente |
|----------|---------------|----------|---------------|---------------|---------|
| 1. Candidatos | Editar | Ver | Ver | Editar | Ver |
| 2. Llamadas | Editar | Editar | Ver | Editar | Ver |
| 3. Entrevistas | Editar | Ver | Editar | Editar | Ver |
| 4. Codigos | Editar | Ver | Ver | Editar | Ver |
| 5. Contratado | Editar | Ver | Ver | Editar | Editar |

**Leyenda:**
- **Editar:** Puede modificar campos y realizar acciones
- **Ver:** Solo lectura, puede consultar la informacion

### Dashboard por Rol

| Rol | Pasos en Dashboard |
|-----|-------------------|
| Seleccionador | 1. Candidatos, 2. Llamadas, 3. Entrevistas, 4. Codigos, 5. Contratado |
| Director RRHH | 1. Candidatos, 2. Llamadas, 3. Entrevistas, 4. Codigos, 5. Contratado |
| Gerente | 1. Candidatos, 2. Llamadas, 3. Entrevistas, 4. Codigos, 5. Contratado |
| Entrevistador | 1. Candidatos, 2. Llamadas, 3. Entrevistas, 4. Codigos, 5. Contratado |
| Llamador | 2. Llamadas, 3. Entrevistas, 4. Codigos, 5. Contratado |

```
DASHBOARD - Seleccionador / Director RRHH / Gerente / Entrevistador (5 pasos)
+------------------------------------------------------------------+
| 1.CANDIDATOS | 2.LLAMADAS | 3.ENTREVISTAS | 4.CODIGOS | 5.CONTRAT |
+------------------------------------------------------------------+

DASHBOARD - Llamador (4 pasos)
+------------------------------------------------------------------+
| 2.LLAMADAS | 3.ENTREVISTAS | 4.CODIGOS | 5.CONTRATADO            |
+------------------------------------------------------------------+
```

### Flujo entre Pantallas

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ 1. CANDIDATOS   │ --> │ 2. LLAMADAS     │ --> │ 3. ENTREVISTAS  │
│    Si           │     │    Si + Dia/Hora│     │    Entrega Cod. │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                         │
                                                         v
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ 5. CONTRATADO   │ <-- │ 3. ENTREVISTAS  │ <-- │ 4. CODIGOS      │
│    (Fin)        │     │    (2a) Contrat.│     │    Completado   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

## PANTALLA 1: CANDIDATOS

### 1.1 Descripcion

Pantalla para clasificar candidatos nuevos y resolver dudas pendientes.

### 1.2 Pestanas

| Pestana | Contenido |
|---------|-----------|
| Sin Clasificar | CVs nuevos sin perfil asignado |
| Con Duda | Candidatos con dudas pendientes de resolver |

### 1.3 Campos - Sin Clasificar

| Campo | Editable | Descripcion |
|-------|----------|-------------|
| ID | No | Identificador unico |
| Nombre | Si | Nombre del candidato |
| Apellido | Si | Apellido del candidato |
| Telefono | Si | Telefono de contacto |
| Email | Si | Correo electronico |
| Localidad | Si | Ciudad de residencia |
| Veh | Si | Vehiculo propio (S/N) |
| B | Si | Carnet B (S/N) |
| C | Si | Carnet C (S/N) |
| CAP | Si | Certificado CAP (S/N) |
| Carr | Si | Carnet Carretillero (S/N) |
| Exp | Si | Anos de experiencia |
| Estudios | Si | Formacion academica |
| CV | No | Enlace al CV completo [+] |
| **Asignar** | Si | Desplegable de accion |

### 1.4 Desplegable: Asignar

| Opcion | Resultado |
|--------|-----------|
| PESCADERIA | Va a Candidatos PESCADERIA |
| LOGISTICA | Va a Candidatos LOGISTICA |
| PRODUCCION | Va a Candidatos PRODUCCION |
| ADMINISTRATIVO | Va a Candidatos ADMINISTRATIVO |
| GESTION | Va a Candidatos GESTION |
| BECARIO | Va a Candidatos BECARIO |
| NO | Va a DESCARTADOS |

### 1.5 Campos - Con Duda

| Campo | Editable | Descripcion |
|-------|----------|-------------|
| (todos los anteriores) | Si | Datos del candidato |
| Duda | No | Texto de la duda del Llamador |
| Respuesta | Si | Nota para el Llamador |
| **Accion** | Si | Desplegable de decision |

### 1.6 Desplegable: Accion (Con Duda)

| Opcion | Resultado |
|--------|-----------|
| SI | Escribe Respuesta → Vuelve a LLAMADAS |
| NO | Va a DESCARTADOS (motivo = la duda) |

### 1.7 Dashboard - Contador

```
CANDIDATOS
├── Sin Clasificar: 216
└── Con Duda: 6
```

---

## PANTALLA 2: LLAMADAS

### 2.1 Descripcion

Pantalla para llamar a candidatos validados y concertar citas de entrevista.

### 2.2 Pestanas

| Pestana | Contenido |
|---------|-----------|
| Por Perfil | Candidatos agrupados por perfil, ordenados por prioridad |
| Entrevistas Hoy | Citas del dia para gestionar llegadas |

### 2.3 Campos - Llamadas por Perfil

| Campo | Editable | Descripcion |
|-------|----------|-------------|
| ID | No | Identificador unico |
| Nombre | Si | Nombre del candidato |
| Apellido | Si | Apellido del candidato |
| Telefono | Si | Telefono de contacto |
| Localidad | Si | Ciudad de residencia |
| Veh | Si | Vehiculo propio (S/N) |
| B | Si | Carnet B (S/N) |
| C | Si | Carnet C (S/N) |
| CAP | Si | Certificado CAP (S/N) |
| Carr | Si | Carnet Carretillero (S/N) |
| Exp | Si | Anos de experiencia |
| CV | No | Enlace al CV completo [+] |
| **Estado** | Si | Desplegable de resultado |
| **Intentos** | Si | Desplegable 1-5 |
| **Notas** | Si | Observaciones de la llamada |
| Dia | Si | Fecha entrevista (si Estado=Si) |
| Hora | Si | Hora entrevista (si Estado=Si) |

### 2.4 Desplegable: Estado

| Opcion | Campos Extra | Resultado |
|--------|--------------|-----------|
| SI | Dia, Hora | Va a ENTREVISTAS |
| NO | - | Va a DESCARTADOS |
| DUDA | - | Vuelve a CANDIDATOS (Con Duda) |

### 2.5 Campos - Entrevistas Hoy

| Campo | Editable | Descripcion |
|-------|----------|-------------|
| Hora | No | Hora de la cita |
| Nombre | No | Nombre del candidato |
| Apellido | No | Apellido del candidato |
| Perfil | No | Perfil del puesto |
| Tipo | No | 1a Entrevista / 2a Entrevista |
| **Asistencia** | Si | Desplegable |

### 2.6 Desplegable: Asistencia

| Opcion | Resultado |
|--------|-----------|
| PRESENTADO | Pasa a pantalla REALIZAR ENTREVISTA |
| NO PRESENTADO | Va a DESCARTADOS (NO_ASISTIO, sin email) |

### 2.7 Dashboard - Contador (ordenado por prioridad)

```
LLAMADAS PARA ENTREVISTAS
├── [!] MUY ALTA
│   └── Dependiente/a Pescaderia: 15
├── [!] ALTA
│   └── Operario/a Logistica: 6
└── [ ] MEDIA
    └── Becario Administracion: 3

ENTREVISTAS DE HOY
├── 10:00 Adela Ruano - PESCADERIA - 1a
├── 11:30 Angel Garcia - LOGISTICA - 1a
└── 16:00 Carmen Lopez - PESCADERIA - 2a
```

---

## PANTALLA 3: ENTREVISTAS

### 3.1 Descripcion

Pantalla para realizar entrevistas y registrar resultados.

### 3.2 Pestanas

| Pestana | Contenido |
|---------|-----------|
| 1a Entrevista | Candidatos en primera entrevista |
| 2a Entrevista | Candidatos en segunda entrevista |
| Con Duda | Candidatos pendientes de decision |

### 3.3 Campos - Realizar Entrevista

| Campo | Editable | Descripcion |
|-------|----------|-------------|
| Candidato | No | Nombre y apellido |
| Perfil | No | Perfil del puesto |
| Tipo | No | 1a Entrevista / 2a Entrevista |
| Telefono | No | Telefono de contacto |
| Email | No | Correo electronico |
| CV | No | Enlace al CV completo [+] |
| Notas llamada | No | Observaciones del Llamador |
| **Notas entrevista** | Si | Observaciones del Entrevistador |
| **Resultado** | Si | Desplegable de decision |

### 3.4 Desplegable: Resultado (1a Entrevista)

| Opcion | Resultado |
|--------|-----------|
| ENTREGA CODIGOS | Email automatico → Va a CODIGOS |
| DUDA | Se queda en ENTREVISTAS (Con Duda) |
| NO | Email rechazo → Va a DESCARTADOS |

### 3.5 Desplegable: Resultado (2a Entrevista)

| Opcion | Resultado |
|--------|-----------|
| CONTRATADO | Email bienvenida → Va a CONTRATADO |
| DUDA | Se queda en ENTREVISTAS (Con Duda) |
| NO | Email rechazo → Va a DESCARTADOS |

### 3.6 Dashboard - Contador

```
ENTREVISTAS
├── 1a Entrevista: 8
├── 2a Entrevista: 3
└── Con Duda: 2
```

---

## PANTALLA 4: CODIGOS

### 4.1 Descripcion

Pantalla del sistema gaming para aprender codigos de productos. Muestra informacion de la 1a entrevista y estadisticas de progreso.

### 4.2 Campos - Lista de Candidatos en Codigos

| Campo | Editable | Descripcion |
|-------|----------|-------------|
| Candidato | No | Nombre y apellido |
| Perfil | No | Perfil del puesto |
| Fecha 1a entrevista | No | Fecha de la primera entrevista |
| Notas entrevista | No | Comentarios del entrevistador |
| Codigos hechos | No | Numero de codigos completados (ej: 45/120) |
| Aciertos | No | Porcentaje de aciertos |
| **Comentario** | Si | Indicaciones para el llamador |
| **Estado** | Si | En Progreso / Llamar |

### 4.3 Desplegable: Estado

| Opcion | Resultado |
|--------|-----------|
| EN PROGRESO | Se queda en CODIGOS |
| LLAMAR | Aparece en Dashboard Llamador para llamar y decidir 2a entrevista |

### 4.4 Cuando Estado = Llamar

Aparece campo adicional:

| Campo | Editable | Descripcion |
|-------|----------|-------------|
| **Resultado** | Si | Desplegable de decision final |

### 4.5 Desplegable: Resultado (cuando Estado = Llamar)

| Opcion | Resultado |
|--------|-----------|
| SI | Pasa a LLAMADAS (2a Entrevista) |
| NO | Va a DESCARTADOS |

### 4.6 Vista Ejemplo - Candidatos en Codigos

| Candidato | Perfil | Fecha 1a | Notas Entrevista | Codigos | Aciertos | Comentario | Estado |
|-----------|--------|----------|------------------|---------|----------|------------|--------|
| Manuel Perez | PESCADERIA | 10/02/2026 | Muy motivado | 120/120 | 88% | Intenta quedar miercoles 12:30 | Llamar |
| Adela Ruano | PESCADERIA | 15/02/2026 | Experiencia 20 años | 45/120 | 90% | | En Progreso |
| Angel Garcia | LOGISTICA | 12/02/2026 | Disponibilidad inmediata | 80/120 | 75% | | En Progreso |

### 4.7 Dashboard - Contador

```
CODIGOS
├── En Progreso: 2
└── Llamar: 1
```

---

## PANTALLA 5: CONTRATADO

### 5.1 Descripcion

Pantalla final del proceso de seleccion. Candidatos que pasan a contratacion.

### 5.2 Campos

| Campo | Editable | Descripcion |
|-------|----------|-------------|
| Candidato | No | Nombre y apellido |
| Perfil | No | Perfil del puesto |
| Telefono | No | Telefono de contacto |
| Email | No | Correo electronico |
| Fecha 1a entrevista | No | Fecha de la primera entrevista |
| Fecha 2a entrevista | No | Fecha de la segunda entrevista |
| Fecha contratacion | Si | Fecha prevista de incorporacion |
| **Estado** | Si | Desplegable |
| Notas | Si | Observaciones finales |

### 5.3 Desplegable: Estado

| Opcion | Resultado |
|--------|-----------|
| PENDIENTE DOC | Esperando documentacion |
| DOCUMENTADO | Documentacion completa |
| INCORPORADO | Ya trabaja en la empresa |

### 5.4 Dashboard - Contador

```
CONTRATADOS
├── Pendiente documentacion: 1
├── Documentados: 2
└── Incorporados este mes: 3
```

---

## DASHBOARD COMPLETO - SELECCION

```
+------------------------------------------------------------------+
|  DASHBOARD SELECCION                                              |
+------------------------------------------------------------------+
|                                                                  |
|  1. CANDIDATOS                    2. LLAMADAS                    |
|  ┌────────────────────────┐       ┌────────────────────────┐     |
|  │ Sin Clasificar: 216   │       │ [!] Pescaderia: 15     │     |
|  │ Con Duda: 6           │       │ [!] Logistica: 6       │     |
|  └────────────────────────┘       │ [ ] Becario: 3         │     |
|                                   ├────────────────────────┤     |
|                                   │ Entrevistas Hoy: 4     │     |
|                                   └────────────────────────┘     |
|                                                                  |
|  3. ENTREVISTAS                   4. CODIGOS                     |
|  ┌────────────────────────┐       ┌────────────────────────┐     |
|  │ 1a Entrevista: 8      │       │ En progreso: 5         │     |
|  │ 2a Entrevista: 3      │       │ Completados: 2         │     |
|  │ Con Duda: 2           │       └────────────────────────┘     |
|  └────────────────────────┘                                      |
|                                   5. CONTRATADOS                 |
|                                   ┌────────────────────────┐     |
|                                   │ Pendiente doc: 1       │     |
|                                   │ Documentados: 2        │     |
|                                   │ Incorporados: 3        │     |
|                                   └────────────────────────┘     |
|                                                                  |
+------------------------------------------------------------------+
```

---

## FLUJO DE CANDIDATOS (version anterior)

### Flujo Detallado

```
+=============================================================================+
|  FLUJO DE CANDIDATOS - PROCESO DE SELECCION                                 |
+=============================================================================+

ESTADO 1: CANDIDATOS
+--------------------------------------------------+
|  Pantalla: Candidatos por Perfil                 |
|  Accion: Validar candidato                       |
|  Desplegable: [ Pendiente / Si / No ]            |
+--------------------------------------------------+
         |
    +----+----+
    |         |
   SI        NO -----------------> DESCARTADOS
    |
    v

ESTADO 2: LLAMADAS
+--------------------------------------------------+
|  Pantalla: Llamadas para Entrevistas             |
|  Accion: Llamar y concertar cita                 |
|  Desplegable: [ Si / No / Duda ]                 |
|  Si marca Si: aparecen Dia y Hora                |
+--------------------------------------------------+
         |
    +----+----+----+
    |    |        |
   SI   NO       DUDA --> Vuelve a CANDIDATOS (Con Duda)
    |    |
    |    v
    |  DESCARTADOS
    v

ESTADO 3: 1a ENTREVISTA
+--------------------------------------------------+
|  Pantalla: Entrevistas de Hoy                    |
|  Accion: Marcar Presentado / No Presentado       |
+--------------------------------------------------+
         |
    +----+----+
    |         |
PRESENTADO   NO PRESENTADO --> DESCARTADOS (sin email)
    |
    v
+--------------------------------------------------+
|  Pantalla: Realizar Entrevista                   |
|  Desplegable: [ Entrega Codigos / Duda / No ]    |
+--------------------------------------------------+
         |
    +----+----+----+
    |    |        |
CODIGOS  NO      DUDA --> Se queda en ENTREVISTAS
    |    |
    |    v
    |  DESCARTADOS + Email rechazo
    v

ESTADO 4: CODIGOS (GAMING)
+--------------------------------------------------+
|  Pantalla: Sistema de Codigos                    |
|  Email automatico con enlace                     |
|  Candidato practica codigos de productos         |
+--------------------------------------------------+
         |
         v

ESTADO 5: 2a ENTREVISTA
+--------------------------------------------------+
|  Pantalla: Llamadas 2a Entrevista                |
|  Desplegable: [ Si / No / Duda ]                 |
+--------------------------------------------------+
         |
    +----+----+----+
    |    |        |
   SI   NO       DUDA --> Vuelve a CANDIDATOS (Con Duda)
    |    |
    |    v
    |  DESCARTADOS
    v
+--------------------------------------------------+
|  Pantalla: Entrevistas de Hoy                    |
|  Accion: Marcar Presentado / No Presentado       |
+--------------------------------------------------+
         |
    +----+----+
    |         |
PRESENTADO   NO PRESENTADO --> DESCARTADOS (sin email)
    |
    v
+--------------------------------------------------+
|  Pantalla: Realizar 2a Entrevista                |
|  Desplegable: [ Contratado / Duda / No ]         |
+--------------------------------------------------+
         |
    +----+----+----+
    |    |        |
CONTRAT  NO      DUDA --> Se queda en ENTREVISTAS
    |    |
    |    v
    |  DESCARTADOS + Email rechazo
    v

ESTADO 6: CONTRATADO
+--------------------------------------------------+
|  FIN DEL PROCESO DE SELECCION                    |
|  Pasa a MODULO CONTRATACION                      |
+--------------------------------------------------+
```

### Resumen de Transiciones

| Estado | Pantalla | Si | No | Duda |
|--------|----------|----|----|------|
| 1. CANDIDATOS | Candidatos por Perfil | → LLAMADAS | → DESCARTADOS | - |
| 2. LLAMADAS | Llamadas para Entrevistas | → 1a ENTREVISTA | → DESCARTADOS | → CANDIDATOS |
| 3. 1a ENTREVISTA | Realizar Entrevista | → CODIGOS | → DESCARTADOS + email | → ENTREVISTAS |
| 4. CODIGOS | Sistema Gaming | → 2a ENTREVISTA | - | - |
| 5. 2a ENTREVISTA | Realizar 2a Entrevista | → CONTRATADO | → DESCARTADOS + email | → ENTREVISTAS |
| 6. CONTRATADO | Contratados | FIN | - | - |

---

## 1. Entrada de CVs

### 1.1 Descripcion

El proceso de seleccion comienza cuando llegan los CVs de las ofertas publicadas en el modulo de **Perfiles**.

### 1.2 Flujo

```
+---------------------------+
| MODULO PERFILES           |
| Oferta publicada          |
| (InfoJobs, LinkedIn, etc) |
+---------------------------+
         |
         v
+---------------------------+
| Llegan CVs                |
+---------------------------+
         |
         v
+---------------------------+
| MODULO SELECCION          |
| Procesar candidatos       |
+---------------------------+
```

### 1.3 Vista en el programa ERP Carihuela

| Perfil | Candidatos | Descartados |
|--------|------------|-------------|
| SIN CLASIFICAR | 216 | 0 |
| LOGISTICA | 67 | 0 |
| PRODUCCION | 18 | 0 |
| PESCADERIA | 7 | 0 |
| ADMINISTRATIVO | 4 | 0 |
| **TOTAL** | **312** | **0** |

---

## 2. Candidatos - Primera Fase

### 2.1 Campos del Listado

| # | Campo | Descripcion | Tipo BD |
|---|-------|-------------|---------|
| 1 | ID | Identificador unico | INT |
| 2 | Nombre | Nombre del candidato | VARCHAR |
| 3 | Apellido | Solo apellido 1 (sin apellido 2) | VARCHAR |
| 4 | Telefono | Telefono de contacto | VARCHAR |
| 5 | Email | Correo electronico | VARCHAR |
| 6 | Localidad | Ciudad/Residencia | VARCHAR |
| 7 | Veh | Vehiculo propio (S/N) | TINYINT |
| 8 | B | Carnet B (S/N) | TINYINT |
| 9 | C | Carnet C (S/N) | TINYINT |
| 10 | CAP | Certificado CAP (S/N) | TINYINT |
| 11 | Carr | Carnet Carretillero (S/N) | TINYINT |
| 12 | Puesto | Perfil asignado segun keywords | VARCHAR |
| 13 | Exp | Anos de experiencia total | DECIMAL |
| 14 | Estudios | Estudios reglados | VARCHAR |
| 15 | CV | Enlace al curriculum detallado | TEXT |
| 16 | Entrevista/Asignar | Desplegable segun estado | ENUM |

### 2.2 Vista en el programa ERP Carihuela

#### 2.2.1 Candidatos PENDIENTES DE CLASIFICAR (216)

| ID | Nombre | Apellido | Telefono | Localidad | Veh | B | C | CAP | Car | Exp | CV | Asignar |
|----|--------|----------|----------|-----------|-----|---|---|-----|-----|-----|-----|---------|
| 1 | ADAMA | FOFANA | 633 171 068 | - | N | N | N | N | N | 12.1 | [+] | [ v ] |
| 4 | Carmelo | Aguilar | 615 168 410 | Aguilar | N | S | N | N | N | 0.0 | [+] | [ v ] |
| 5 | Alexandre | Gustems | 689 465 624 | Almodovar | S | S | N | N | N | 8.6 | [+] | [ v ] |

**Desplegable Asignar:**
- PESCADERIA → Va a listado PESCADERIA
- LOGISTICA → Va a listado LOGISTICA
- PRODUCCION → Va a listado PRODUCCION
- ADMINISTRATIVO → Va a listado ADMINISTRATIVO
- GESTION → Va a listado GESTION
- BECARIO → Va a listado BECARIO
- NO → Va a DESCARTADOS

#### 2.2.2 Candidatos POR PERFIL (ya clasificados)

**PESCADERIA (7)**

| ID | Nombre | Apellido | Telefono | Localidad | Veh | B | C | CAP | Car | Exp | CV | Entrevista |
|----|--------|----------|----------|-----------|-----|---|---|-----|-----|-----|-----|------------|
| 65 | Adela | Ruano | 675 942 449 | Cordoba | S | S | N | N | N | 20.3 | [+] | Pendiente |
| 103 | Angela | Navarro | 622-52-80-94 | Cordoba | N | N | N | N | N | 5.3 | [+] | Pendiente |

**LOGISTICA (67)**

| ID | Nombre | Apellido | Telefono | Localidad | Veh | B | C | CAP | Car | Exp | CV | Entrevista |
|----|--------|----------|----------|-----------|-----|---|---|-----|-----|-----|-----|------------|
| 2 | Angel | Garcia | 677 538 930 | Adamuz | S | S | S | N | N | 8.3 | [+] | Pendiente |
| 3 | Borja | Mendez | 692 977 443 | Adamuz | S | S | S | N | N | 5.5 | [+] | Pendiente |

**Desplegable Entrevista:**
- Pendiente → Esperando decision
- Si → Pasa a entrevistas
- No → Va a DESCARTADOS

### 2.3 Logica de Asignacion

| Accion | Resultado |
|--------|-----------|
| Asignar perfil (ej: PESCADERIA) | Candidato va al listado del perfil |
| Asignar NO | Candidato va a DESCARTADOS |
| Entrevista = Si | Candidato pasa a fase entrevistas |
| Entrevista = No | Candidato va a DESCARTADOS |

---

## 3. Tipos de Descarte

### 3.1 Descartes AUTOMATICOS (reglas configurables)

| Regla | Campo | Condicion | Valor | Motivo Mostrado |
|-------|-------|-----------|-------|-----------------|
| REGLA_EXPERIENCIA | anos_experiencia | < | 1 | Experiencia menor a 1 ano |
| REGLA_DISTANCIA | distancia_km | > | 40 | Distancia mayor a 40 km |
| DESCARTADO_PREVIO | - | Si aplica | - | Descartado en proceso anterior |

### 3.2 Descartes MANUALES (decision del usuario)

| Motivo | Descripcion |
|--------|-------------|
| MALAS_REFERENCIAS | Malas referencias |
| NO_INTERESADO | Candidato no interesado |
| NO_CONTESTA | No contesta tras varios intentos |
| DESCARTADO_ENTREVISTA | Descartado tras entrevista |
| OTROS | Otros motivos (especificar en notas) |

### 3.3 Vista en el programa ERP Carihuela

**Acceso:** Menu RRHH > Configuracion > Descartes

#### Pantalla: Configuracion de Motivos de Descarte

| Codigo | Descripcion | Tipo |
|--------|-------------|------|
| SIN_EXPERIENCIA | Experiencia menor a 1 ano | AUTOMATICO |
| DISTANCIA_EXCEDIDA | Distancia mayor a 40 km | AUTOMATICO |
| DESCARTADO_PREVIO | Descartado en proceso anterior | AUTOMATICO |
| MALAS_REFERENCIAS | Malas referencias | MANUAL |
| NO_INTERESADO | Candidato no interesado | MANUAL |
| NO_CONTESTA | No contesta tras varios intentos | MANUAL |
| DESCARTADO_ENTREVISTA | Descartado tras entrevista | MANUAL |
| NO_ASISTIO | No se presento a la entrevista | AUTOMATICO |
| OTROS | Otros motivos | MANUAL |

#### Pantalla: Configuracion de Reglas Automaticas

| Regla | Campo | Operador | Valor | Motivo Asociado |
|-------|-------|----------|-------|-----------------|
| REGLA_EXPERIENCIA | anos_experiencia | < | 1 | SIN_EXPERIENCIA |
| REGLA_DISTANCIA | distancia_km | > | 40 | DISTANCIA_EXCEDIDA |

#### Pantalla: Candidatos Descartados

| ID | Nombre | Apellido | Perfil | Motivo | Fecha | Descartado por | Notas |
|----|--------|----------|--------|--------|-------|----------------|-------|
| - | - | - | - | - | - | - | - |

### 3.4 Ubicacion de Datos

| Tabla | Descripcion |
|-------|-------------|
| `motivos_descarte` | Catalogo de motivos (8 registros) |
| `reglas_descarte` | Reglas automaticas configurables (2 activas) |
| `candidatos_descartados` | Historial de descartados |

---

## 4. Segunda Fase: ENTREVISTAS

### 4.1 Descripcion

Cuando un candidato se marca como **Entrevista = Si**, pasa a la fase de llamadas para concertar cita de entrevista.

### 4.2 Vista en el programa ERP Carihuela - PERFILES

**Acceso:** Menu RRHH > Perfiles > [Seleccionar Perfil]

#### Estadisticas por Perfil

| Perfil | Sin Validar | Con Duda |
|--------|-------------|----------|
| PESCADERIA | 66 | 3 |
| LOGISTICA | 45 | 2 |
| PRODUCCION | 15 | 1 |
| ADMINISTRATIVO | 4 | 0 |
| **TOTAL** | **130** | **6** |

#### Pestana: PESCADERIA - Sin Validar (66)

| ID | Nombre | Apellido | Telefono | Localidad | Veh | B | C | CAP | Car | Exp | CV | Entrevista |
|----|--------|----------|----------|-----------|-----|---|---|-----|-----|-----|-----|------------|
| 65 | Adela | Ruano | 675 942 449 | Cordoba | S | S | N | N | N | 20.3 | [+] | Pendiente |

**Desplegable Entrevista:** Pendiente / Si / No

#### Pestana: PESCADERIA - Con Duda (3)

| ID | Nombre | Apellido | Telefono | Localidad | Veh | B | C | CAP | Car | Exp | CV | Duda | Respuesta | Accion |
|----|--------|----------|----------|-----------|-----|---|---|-----|-----|-----|-----|------|-----------|--------|
| 72 | Carmen | Lopez | 654 123 456 | Malaga | S | S | N | N | N | 5.1 | [+] | Solo quiere tienda Barraquer | [ ] | [ v ] |

**Desplegable Accion:**
- **Si** → Campo Respuesta (nota para Llamador) → Vuelve a Llamadas
- **No** → Descartado con Motivo = la Duda

### 4.3 Vista en el programa ERP Carihuela - LLAMADAS PARA ENTREVISTAS

**Acceso:** Menu RRHH > Llamadas > Llamadas para Entrevistas

| ID | Nombre | Apellido | Telefono | Localidad | Veh | B | C | CAP | Car | Exp | CV | Estado | Intentos | Notas | Dia | Hora |
|----|--------|----------|----------|-----------|-----|---|---|-----|-----|-----|-----|--------|----------|-------|-----|------|
| 65 | [Adela] | [Ruano] | [675 942 449] | [Cordoba] | [S] | [S] | [N] | [N] | [N] | [20.3] | [+] | Si | 1 | interesada sector | 21/02 | 10:00 |
| 103 | [Angela] | [Navarro] | [622-52-80-94] | [Cordoba] | [N] | [N] | [N] | [N] | [N] | [5.3] | [+] | Duda | 2 | quiere saber turnos | | |
| 107 | [Pedro] | [Lopez] | [654 321 987] | [Sevilla] | [S] | [S] | [N] | [N] | [N] | [3.2] | [+] | No | 1 | trabajando, buena impresion | | |

**Campos editables** (entre corchetes): Permite corregir errores de extraccion del CV

**Desplegable Estado:**
- **Si** → Aparecen columnas **Dia** y **Hora** → Pasa a ENTREVISTAS
- **No** → Pasa a DESCARTADOS
- **Duda** → Vuelve a PERFILES (pestana Con Duda)

**Desplegable Intentos:** 1, 2, 3, 4, 5 (descarte automatico configurable a partir de N intentos)

**Campo Notas:**
- Si: "interesada en el sector"
- No: "trabajando actualmente, buena impresion"
- Duda: "quiere saber cuales son los turnos"

### 4.4 Flujo de DUDAS

```
LLAMADOR marca DUDA
"Solo quiere trabajar en la tienda Barraquer"
         |
         v
+---------------------------+
| Vuelve a su PERFIL        |
| Pestana: Con Duda         |
+---------------------------+
         |
         v
+---------------------------+
| EVALUADOR ve la duda      |
| y decide                  |
+---------------------------+
         |
    +----+----+
    |         |
   NO        SI
    |         |
    v         v
+----------------+  +--------------------------------+
| DESCARTADO     |  | Anade nota para el Llamador    |
| Descartado por:|  | "Llamala y dile que no podemos |
| Jorge Perez    |  | ofrecerle puesto fijo porque   |
| Motivo:        |  | el equipo esta cubierto"       |
| Solo quiere    |  +--------------------------------+
| tienda fija    |           |
+----------------+           v
              +---------------------------+
              | Vuelve a LLAMADAS         |
              | con la nota del Evaluador |
              +---------------------------+
                         |
                         v
              +---------------------------+
              | LLAMADOR llama de nuevo   |
              | y marca SI / NO           |
              +---------------------------+
```

### 4.5 Flujo de Asignacion de Llamadas

```
+---------------------------+
| Entrevista = Si           |
+---------------------------+
           |
           v
+---------------------------+
| VERIFICAR DISPONIBILIDAD  |
| del trabajador asignado   |
+---------------------------+
           |
     +-----+-----+
     |           |
 DISPONIBLE  NO DISPONIBLE
  (Nivel 4)      |
     |           v
     |    +---------------------------+
     |    | Comprobar nivel del       |
     |    | trabajador asignado       |
     |    +---------------------------+
     |           |
     |     +-----+-----+
     |     |           |
     |  NIVEL 3     NIVEL 1/2 o
     |  (temporal)  NO EN EMPRESA
     |     |           |
     |     v           v
     |  +------------+ +----------------+
     |  | Asignar    | | Asignar        |
     |  | MOMENTANEA | | DEFINITIVA     |
     |  | a otro     | | a otro         |
     |  | trabajador | | trabajador     |
     |  +------------+ +----------------+
     |
     v
+-----------+
| Asignar   |
| llamada   |
+-----------+
```

### 4.6 Tipos de Reasignacion

| Nivel Trabajador | Estado | Tipo Asignacion | Descripcion |
|------------------|--------|-----------------|-------------|
| Nivel 4 | Disponible | Normal | Trabajador disponible en cuadrante |
| Nivel 3 | No disponible temporal | MOMENTANEA | Vacaciones, baja corta, permiso. Vuelve a su tarea al reincorporarse |
| Nivel 2 | No disponible | DEFINITIVA | Baja larga duracion. Se reasigna permanentemente |
| Nivel 1 | No disponible | DEFINITIVA | Excedencia. Se reasigna permanentemente |
| No en empresa | - | DEFINITIVA | Ya no trabaja. Se reasigna permanentemente |

### 4.7 Tabla: asignacion_llamadas

| Campo | Descripcion | Tipo BD |
|-------|-------------|---------|
| id | Identificador | INT |
| candidato_id | FK a candidatos | BIGINT UNSIGNED |
| trabajador_id | FK a operadores | INT |
| fecha_asignacion | Timestamp automatico | TIMESTAMP |
| estado | SI / NO / DUDA | ENUM |
| intentos | Numero de intentos de llamada (1-5) | INT |
| notas | Observaciones de la llamada | TEXT |
| dia_entrevista | Fecha entrevista (si estado=SI) | DATE |
| hora_entrevista | Hora entrevista (si estado=SI) | TIME |

### 4.8 Tabla: entrevistas

| Campo | Descripcion | Tipo BD |
|-------|-------------|---------|
| id | Identificador | INT |
| candidato_id | FK a candidatos | BIGINT UNSIGNED |
| llamada_id | FK a asignacion_llamadas | INT |
| fecha_entrevista | Fecha y hora programada | DATETIME |
| entrevistador_id | FK a operadores | INT |
| estado | PROGRAMADA / REALIZADA / NO_ASISTIO | ENUM |
| resultado | PASA / DESCARTADO | ENUM |
| notas | Observaciones de la entrevista | TEXT |

### 4.9 Resultados de la Entrevista

| Opcion | Accion |
|--------|--------|
| **Entrega Codigos** | Pasa la entrevista → email automatico → sistema gaming |
| **No** | Descartado → abre campo motivo |

### 4.10 Flujo Completo de Entrevistas

```
+--------------------------------------------------+
|  DASHBOARD LLAMADOR - ENTREVISTAS DE HOY         |
+--------------------------------------------------+
|                                                  |
|  10:00  Adela Ruano - PESCADERIA - 1a  [ v ]     |
|  11:30  Angel Garcia - LOGISTICA - 1a  [ v ]     |
|                                                  |
+--------------------------------------------------+
                    |
        +-----------+-----------+
        |                       |
   PRESENTADO              NO PRESENTADO
        |                       |
        v                       v
+------------------+    +------------------------+
|  PANTALLA:       |    |  DESCARTADOS           |
|  ENTREVISTA      |    |  Motivo: NO_ASISTIO    |
+------------------+    |  (sin email)           |
        |               +------------------------+
        v
+--------------------------------------------------+
|  PANTALLA: REALIZAR ENTREVISTA                   |
+--------------------------------------------------+
|                                                  |
|  Candidato: Adela Ruano                          |
|  Perfil: PESCADERIA                              |
|  Tipo: 1a Entrevista                             |
|                                                  |
|  CV: [Ver CV completo]                           |
|                                                  |
|  Notas de llamada: "Interesada en el sector"     |
|                                                  |
|  +-----------------------------------------+     |
|  | NOTAS DE LA ENTREVISTA                  |     |
|  | [                                    ]  |     |
|  +-----------------------------------------+     |
|                                                  |
|  RESULTADO: [ v ]                                |
|                                                  |
+--------------------------------------------------+
                    |
        +-----------+-----------+-----------+
        |           |                       |
   ENTREGA      DUDA                       NO
   CODIGOS        |                         |
        |         v                         v
        |  +------------------+    +------------------------+
        |  |  SE QUEDA EN     |    |  DESCARTADOS           |
        |  |  ENTREVISTAS     |    |  + EMAIL RECHAZO       |
        |  |  con comentarios |    |  automatico            |
        |  +------------------+    +------------------------+
        v
+--------------------------------------------------+
|  EMAIL AUTOMATICO                                |
|  Bienvenido + enlace sistema codigos             |
+--------------------------------------------------+
        |
        v
+--------------------------------------------------+
|  SISTEMA GAMING - CODIGOS                        |
+--------------------------------------------------+
```

### 4.11 Pantalla: Realizar Entrevista

**Acceso:** Desde Dashboard Llamador > Entrevistas de Hoy > Presentado

| Campo | Descripcion | Editable |
|-------|-------------|----------|
| Candidato | Nombre y apellido | NO |
| Perfil | Perfil asignado | NO |
| Tipo | 1a Entrevista / 2a Entrevista | NO |
| CV | Enlace al CV completo | NO |
| Notas llamada | Notas del Llamador | NO |
| Notas entrevista | Observaciones del Entrevistador | SI |
| Resultado | Entrega Codigos / Duda / No | SI |

**Desplegable Resultado:**

| Opcion | Accion |
|--------|--------|
| **Entrega Codigos** | Email automatico + Sistema Gaming |
| **Duda** | Se queda en Entrevistas con notas |
| **No** | Descartados + Email automatico de rechazo |

### 4.12 Pantalla: Candidato No Presentado

**Acceso:** Desde Dashboard Llamador > Entrevistas de Hoy > No Presentado

| Campo | Valor |
|-------|-------|
| Estado | NO_ASISTIO |
| Destino | DESCARTADOS |
| Email | NO se envia |
| Motivo descarte | NO_ASISTIO |

---

## 5. Sistema de Codigos (Gaming)

### 5.1 Flujo de Acceso

```
Entrega Codigos (1a entrevista)
         |
         v
+------------------------------------------+
|  SISTEMA GENERA ID CANDIDATO             |
|  Ej: CAND-12345                          |
+------------------------------------------+
         |
         v
+------------------------------------------+
|  EMAIL AUTOMATICO AL CANDIDATO           |
|  - ID Candidato                          |
|  - Enlace al sistema                     |
|  - Instrucciones                         |
+------------------------------------------+
         |
         v
+------------------------------------------+
|  PANTALLA: REGISTRO                      |
|  - Introduce ID Candidato                |
|  - Completa datos personales             |
|  - Crea contraseña                       |
+------------------------------------------+
         |
         v
+------------------------------------------+
|  PANTALLA: LOGIN                         |
|  - ID o Email + Contraseña               |
|  - Recuperar contraseña (via email)      |
+------------------------------------------+
         |
         v
+------------------------------------------+
|  SISTEMA GAMING - APRENDER CODIGOS       |
|  Por familias de productos               |
+------------------------------------------+
```

### 5.2 Campos de Registro del Candidato

| Campo | Obligatorio | Descripcion |
|-------|-------------|-------------|
| ID Candidato | Si | El que recibe en el email |
| Nombre | Si | Nombre |
| Apellido 1 | Si | Primer apellido |
| Apellido 2 | Si | Segundo apellido |
| Email | Si | Para recuperar contraseña |
| Telefono | Si | Contacto |
| Contraseña | Si | Minimo 6 caracteres |
| Repetir contraseña | Si | Confirmacion |

### 5.3 Recuperacion de Contraseña

| Paso | Accion |
|------|--------|
| 1 | Candidato pulsa "Olvide mi contraseña" |
| 2 | Introduce su email |
| 3 | Sistema envia enlace de recuperacion |
| 4 | Candidato crea nueva contraseña |

### 5.4 Emails Automaticos del Proceso de Entrevistas

#### 5.4.1 Email: Entrega de Codigos (Candidato Seleccionado)

**Trigger:** Entrevistador marca "Entrega Codigos" en la entrevista

**Plantilla:**

```
Asunto: Bienvenido al equipo - Acceso al Sistema de Codigos

Estimado/a Sr/a [APELLIDO]:

Gracias por participar en el proceso de seleccion para el puesto de
[POSICION] en La Carihuela Gestion de Pescaderias SL.

Nos complace informarle que ha superado la entrevista y le damos
la bienvenida a nuestro equipo.

Su ID de candidato es: [ID_CANDIDATO]

A continuacion le facilitamos el enlace para acceder al sistema
de aprendizaje de codigos de productos:

[ENLACE_SISTEMA_CODIGOS]

Este sistema le ayudara a familiarizarse con los codigos de los
productos que manejamos en nuestras pescaderias.

Si tiene alguna duda, contacte por correo electronico a:
seleccion@pescadoslacarihuela.es o por telefono al 957 XXX XXX.

Atentamente,
Departamento de Recursos Humanos
La Carihuela Gestion de Pescaderias SL
```

#### 5.4.2 Email: Rechazo tras Entrevista

**Trigger:** Entrevistador marca "No" en la 1a o 2a entrevista

**Condicion:** Solo se envia si el candidato se presento a la entrevista (Presentado = Si)

**NO se envia si:** Candidato marcado como "No Presentado" (va a Descartados sin email)

**Plantilla:**

```
Asunto: Resultado del proceso de seleccion

Estimado/a Sr/a [APELLIDO]:

Gracias por participar en el proceso de seleccion para el puesto de
[POSICION] en La Carihuela Gestion de Pescaderias SL.

Lamentamos comunicarle que, tras evaluar su candidatura, hemos
decidido continuar el proceso con otros candidatos cuyo perfil
se ajusta mejor a las necesidades actuales del puesto.

Le agradecemos el tiempo dedicado y le animamos a seguir nuestras
ofertas de empleo para futuras oportunidades.

Si tiene alguna duda, contacte por correo electronico a:
seleccion@pescadoslacarihuela.es

Atentamente,
Departamento de Recursos Humanos
La Carihuela Gestion de Pescaderias SL
```

### 5.5 Tareas de Programacion

| ID | Tarea | Trigger | Condicion | Descripcion | Estado |
|----|-------|---------|-----------|-------------|--------|
| AUTO_001 | Importacion CVs email | Email a empleo@pescadoslacarihuela.es | - | Importar CVs automaticamente a candidatos | PENDIENTE |
| EMAIL_001 | Email Entrega Codigos | Entrevista = "Entrega Codigos" | - | Enviar email con enlace al sistema de codigos | PENDIENTE |
| EMAIL_002 | Email Rechazo Entrevista | Entrevista (1a o 2a) = "No" | Presentado = Si | Enviar email de rechazo al candidato | PENDIENTE |
| EMAIL_003 | Email Bienvenida Contratacion | 2a Entrevista = "Contratado" | - | Enviar email de bienvenida al nuevo empleado | PENDIENTE |
| DESC_001 | Descarte No Presentado | Entrevista = "No Presentado" | - | Descartar candidato con motivo NO_ASISTIO (sin email) | PENDIENTE |
| DESC_002 | Descarte Intentos Excedidos | Intentos = MAX_INTENTOS | - | Descartar candidato con motivo NO_CONTESTA | PENDIENTE |

**Documento completo:** Ver `docs/TAREAS_AUTOMATIZACION.md`

### 5.6 Variables de Plantilla

| Variable | Descripcion | Origen |
|----------|-------------|--------|
| [APELLIDO] | Apellido del candidato | candidatos.apellido |
| [POSICION] | Titulo del puesto | peticiones_trabajador.posicion |
| [ID_CANDIDATO] | ID unico del candidato | Sistema genera automaticamente |
| [ENLACE_SISTEMA_CODIGOS] | URL del sistema gaming | Configuracion sistema |

### 5.7 Pantalla del Juego - Practica por Familias

```
+============================================+
|  CODIGOS - Adela Ruano                    |
+============================================+
|                                            |
|  PROGRESO POR FAMILIAS                     |
|  ├── CHICO ENTERO ........ 85% [ ]        |
|  ├── CHICO LIMPIO ........ 92% [✓]        |
|  ├── MARISCO CRUDO ....... 90% [✓]        |
|  ├── PLANOS .............. 78% [ ]        |
|  └── CEFALOPODO .......... 95% [✓]        |
|                                            |
|  [✓] = Verde (>= 90%)                      |
|  [ ] = Gris (< 90%)                        |
|                                            |
+============================================+
|                                            |
|  MODO PRACTICA - CHICO ENTERO              |
|                                            |
|  Codigo: 16                                |
|                                            |
|  Cual es?                                  |
|                                            |
|  [ ] Acedias                               |
|  [x] Boquerones  -> Correcto!              |
|  [ ] Sardinas                              |
|                                            |
|  Racha: 5 seguidas                         |
|  Aciertos familia: 45/53 (85%)             |
|                                            |
+============================================+
```

### 5.8 Progreso y Prueba Final

#### 5.8.1 Requisitos para Prueba Final

| Requisito | Valor |
|-----------|-------|
| Progreso minimo por familia | 90% de aciertos |
| Condicion para activar prueba | TODAS las familias en verde (>= 90%) |

#### 5.8.2 Prueba Final

| Elemento | Valor |
|----------|-------|
| Numero de preguntas | 10 codigos aleatorios |
| Minimo para aprobar | 7 aciertos (70%) |
| Resultado APROBADO | Estado = "Codigos Completado" |
| Resultado SUSPENDIDO | Vuelve a practicar |

#### 5.8.3 Flujo Completo del Sistema Gaming

```
PRACTICA POR FAMILIAS
         |
         v
+---------------------------+
| ¿Todas familias >= 90%?   |
+---------------------------+
         |
    NO --+-- SI
    |        |
    v        v
 Seguir   PRUEBA FINAL
practicar (10 codigos)
             |
        +----+----+
        |         |
     >= 7       < 7
    APROBADO  SUSPENDIDO
        |         |
        v         v
  "CODIGOS      Vuelve a
  COMPLETADO"   practicar
        |
        v
  Pendiente llamar
  para 2a Entrevista
```

#### 5.8.4 Estados en Pantalla CODIGOS (ERP)

| Estado | Significado | Color |
|--------|-------------|-------|
| En Progreso | Practicando familias | - |
| Prueba Disponible | Todas familias >= 90%, puede hacer prueba | - |
| Codigos Completado | Aprobo prueba, pendiente decision | Verde |

#### 5.8.5 Alerta Automatica - Codigos Completado

**Trigger:** Candidato aprueba examen de codigos (>= 7/10)

**Destinatarios:**
- Entrevistador
- Director RRHH

**Mensaje de alerta:**
```
[NOMBRE APELLIDO] se sabe los codigos
```

**Ejemplo:**
```
Manuel Perez se sabe los codigos
```

#### 5.8.6 Accion Post-Examen en Pantalla CODIGOS

Cuando el candidato aprueba el examen, se desbloquea la accion Si/No:

**Vista en Pantalla CODIGOS:**

| Candidato | Codigos | Aciertos | Estado | Accion | Nota |
|-----------|---------|----------|--------|--------|------|
| Manuel Perez | 120/120 | 88% | Codigos Completado | [ v ] | [ ] |

**Desplegable Accion:**

| Opcion | Resultado |
|--------|-----------|
| SI | Llamar para 2a Entrevista/Contratacion + Campo Nota |
| NO | Va a DESCARTADOS |

**Campo Nota (cuando marca Si):**

Indicaciones para la cita, ejemplo:
```
queda mañana martes 12/02 a las 10:30
```

#### 5.8.7 Flujo Completo Post-Examen

```
CANDIDATO APRUEBA EXAMEN (>= 7/10)
         |
         +--------> ALERTA AUTOMATICA
         |          Para: Entrevistador + Director RRHH
         |          "Manuel Perez se sabe los codigos"
         |
         v
PANTALLA CODIGOS (ERP)
Estado: "Codigos Completado"
Accion: [ Si / No ] (desbloqueado)
         |
         v
SELECCIONADOR marca "Si" + Nota
"queda mañana martes 12/02 a las 10:30"
         |
         v
MENU: Segunda Entrevista / Contratacion
         |
         v
2a ENTREVISTA + CONTRATACION
```

### 5.9 Fuente de Datos - Servidor ERP

**Servidor:** gestion.pescadoslacarihuela.es

#### 5.9.1 Tablas del Servidor

| Tabla | Uso | Campos Clave |
|-------|-----|--------------|
| `articulos` | Productos | codigo, nombre, familia_id |
| `familias` | Familias de productos | id, nombre |
| `v2_facturas_tickets_lineas` | Ventas | IdArticulo, created_at |

#### 5.9.2 Familias de Productos

| ID | Familia |
|----|---------|
| 13 | CHICO ENTERO |
| 14 | CHICO LIMPIO |
| 18 | MARISCO CRUDO |
| 19 | MARISCO COCIDO |
| 21 | CEFALOPODO |
| 24 | BACALAO |
| 29 | MERLUZA |
| 31 | PLANOS |
| 32 | RAPE |

#### 5.9.3 Ejemplos de Articulos

| Codigo | Nombre | Familia |
|--------|--------|---------|
| 1 | ACEDIAS | CHICO ENTERO |
| 16 | BOQUERONES | CHICO ENTERO |
| 60 | LENGUADO | PLANOS |
| 120 | LENGUADOS | PLANOS |
| 160 | URTA | RESTO HORNO |

#### 5.9.4 Filtro de Productos Activos (Ultimos 3 Meses)

Solo se muestran en el juego los articulos que han tenido ventas en los ultimos 3 meses.

**Consulta SQL:**

```sql
SELECT DISTINCT a.codigo, a.nombre, f.nombre as familia
FROM articulos a
JOIN familias f ON a.familia_id = f.id
JOIN v2_facturas_tickets_lineas v ON v.IdArticulo = a.id
WHERE v.created_at >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)
ORDER BY f.nombre, a.nombre
```

**Logica:**

| Condicion | Resultado |
|-----------|-----------|
| Articulo vendido en ultimos 3 meses | Aparece en el sistema gaming |
| Articulo sin ventas en 3 meses | No aparece (producto inactivo) |

---

## 6. Tercera Fase: SEGUNDA ENTREVISTA / CONTRATACION

### 6.1 Acceso

**Menu:** Segunda Entrevista / Contratacion

### 6.2 Resultados

| Opcion | Email Automatico | Destino |
|--------|------------------|---------|
| SI (Contratado) | Email Bienvenida + acceso sistema | CONTRATADOS |
| DUDA | - | Se queda en ENTREVISTAS |
| NO | Email Agradecimiento | DESCARTADOS |

### 6.3 Email Automatico - SI (Contratado)

**Trigger:** 2a Entrevista marca "Si"

**Plantilla:**

```
Asunto: Bienvenido a La Carihuela

Estimado/a [NOMBRE] [APELLIDO]:

Bienvenido a La Carihuela. Estamos muy felices de que puedas
formar parte de nuestra empresa.

Para acceder al sistema, utilice los siguientes datos:

Usuario: [ID_CANDIDATO]
Contraseña: Puede establecerla en el siguiente enlace:
[ENLACE_CREAR_CONTRASEÑA]

Introduzca su nueva contraseña dos veces para confirmarla.

Si tiene alguna duda, contacte con nosotros en:
seleccion@pescadoslacarihuela.es

Atentamente,
Departamento de Recursos Humanos
La Carihuela Gestion de Pescaderias SL
```

### 6.4 Email Automatico - NO (No Contratado)

**Trigger:** 2a Entrevista marca "No"

**Plantilla:**

```
Asunto: Agradecimiento por su participacion

Estimado/a [NOMBRE] [APELLIDO]:

Queremos agradecerle sinceramente su participacion en nuestro
proceso de seleccion para el puesto de [POSICION].

Lamentamos comunicarle que en esta ocasion no ha sido posible
contar con usted para incorporarse a nuestro equipo.

Le animamos a seguir atento a nuestras futuras ofertas de empleo.

Gracias por su tiempo e interes en La Carihuela.

Atentamente,
Departamento de Recursos Humanos
La Carihuela Gestion de Pescaderias SL
```

### 6.5 Flujo 2a Entrevista / Contratacion

```
MENU: Segunda Entrevista / Contratacion
         |
         v
+---------------------------+
|    RESULTADO 2a ENTREV    |
+---------------------------+
         |
    +----+----+----+
    |    |        |
   SI   DUDA      NO
    |    |        |
    v    v        v
+-------+ +------+ +------------------+
| EMAIL | | QUEDA| | EMAIL            |
| BIENV.| | ENTR.| | AGRADECIMIENTO   |
+-------+ +------+ +------------------+
    |              |
    v              v
CONTRATADOS    DESCARTADOS
    |
    v
Acceso sistema:
- Usuario: ID_CANDIDATO
- Crear contraseña
```

### 6.6 Variables de Plantilla - 2a Entrevista

| Variable | Descripcion | Origen |
|----------|-------------|--------|
| [NOMBRE] | Nombre del candidato | candidatos.nombre |
| [APELLIDO] | Apellido del candidato | candidatos.apellido |
| [ID_CANDIDATO] | ID unico del candidato | Sistema |
| [POSICION] | Titulo del puesto | peticiones_trabajador.posicion |
| [ENLACE_CREAR_CONTRASEÑA] | URL para crear contraseña | Configuracion sistema |

### 6.7 Alta en Sistema - Tabla operadores

Cuando el candidato es contratado (2a Entrevista = Si), se da de alta en el portal de trabajadores.

#### 6.7.1 Portal de Trabajadores

**Tabla:** `operadores`
**Servidor:** gestion.pescadoslacarihuela.es

#### 6.7.2 Asignacion de ID

El sistema asigna automaticamente el primer ID libre desde 1:

```
Buscar primer ID libre desde 1
         |
         v
Ejemplo: IDs [_,2,_,_,5,6,...]
         |
         v
Asigna ID = 1 (primer hueco libre)
         |
         v
Insertar en tabla operadores
```

**Regla:** Si hay huecos en la numeracion, se reutilizan (ej: si entre 10 y 12 falta el 11, se asigna 11)

#### 6.7.3 Campos Principales - Tabla operadores

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| id | int | ID unico del trabajador (asignado automaticamente) |
| Nombre | char(30) | Nombre |
| Apellido1 | char(15) | Primer apellido |
| Apellido2 | char(15) | Segundo apellido |
| Nif | varchar(255) | DNI/NIE |
| email | varchar(255) | Correo electronico |
| telefono | varchar(255) | Telefono |
| login | varchar(255) | Usuario de acceso |
| password_laravel | varchar(255) | Contraseña encriptada |
| Direccion | varchar(100) | Direccion |
| Poblacion | varchar(50) | Ciudad |
| Provincia | varchar(50) | Provincia |
| Cp | char(5) | Codigo postal |
| fecha_nacimiento | date | Fecha de nacimiento |
| NAF | char(12) | Numero Afiliacion SS |
| categoria_profesional_id | int | FK categoria profesional |
| idtienda | int | Tienda asignada |
| activo | int | Estado activo/inactivo |
| created_at | timestamp | Fecha de alta |

#### 6.7.4 Flujo Completo de Alta

```
2a ENTREVISTA = SI (Contratado)
         |
         v
+----------------------------------+
| 1. Buscar primer ID libre >= 1   |
+----------------------------------+
         |
         v
+----------------------------------+
| 2. Crear registro en operadores  |
|    - Datos personales            |
|    - Login = ID                  |
|    - Contraseña pendiente        |
+----------------------------------+
         |
         v
+----------------------------------+
| 3. Enviar EMAIL BIENVENIDA       |
|    - Usuario: ID                 |
|    - Enlace crear contraseña     |
+----------------------------------+
         |
         v
+----------------------------------+
| 4. Trabajador accede al portal   |
|    - Crea su contraseña          |
|    - Acceso completo             |
+----------------------------------+
```

#### 6.7.5 Ejemplos de Trabajadores

| ID | Nombre | Apellido |
|----|--------|----------|
| 175 | Dolores | Morales |
| 189 | Jesus Javier | Raya |
| 194 | Virginia | Jimenez |
| 597 | Haydee Lucia | Maltez |

#### 6.7.6 Alerta Automatica - Contratacion Completada

**Trigger:** Se asigna ID al nuevo trabajador

**Destinatarios:**
- Gerente
- Director RRHH
- (Otros configurables)

**Contenido de la alerta:**
```
[NOMBRE APELLIDO] ha concluido el proceso de seleccion

Notas de las entrevistas:
- 1a Entrevista: [NOTAS_1A_ENTREVISTA]
- 2a Entrevista: [NOTAS_2A_ENTREVISTA]

Curriculum adjunto: [CV.pdf]
```

### 6.8 Primer Acceso - Datos Obligatorios

Cuando el trabajador accede por primera vez al portal, debe completar los siguientes datos:

#### 6.8.1 Campos Obligatorios

| Campo | Tipo | Validacion |
|-------|------|------------|
| Nombre | texto | Obligatorio |
| Apellido 1 | texto | Obligatorio |
| Apellido 2 | texto | Obligatorio |
| Fecha de nacimiento | fecha | Obligatorio |
| Telefono | texto | Obligatorio |
| Email | email | Obligatorio, formato valido |
| Direccion | texto | Obligatorio |
| Codigo postal | texto | Obligatorio, 5 digitos |
| Ciudad | texto | Obligatorio |
| DNI | texto | Obligatorio, formato valido |
| Numero afiliacion SS | texto | Obligatorio |
| Numero cuenta bancaria | IBAN | Obligatorio, **verificacion especial** |

#### 6.8.2 Verificacion Cuenta Bancaria - Proteccion Anti-Fraude

Para evitar fraude, la cuenta bancaria requiere doble verificacion:

**Paso 1 - Trabajador:**
```
+----------------------------------+
| Campo: Numero de cuenta (IBAN)   |
| ES12 3456 7890 1234 5678 9012    |
+----------------------------------+
         |
         v
+----------------------------------+
| Subir PDF del banco              |
| (extracto, certificado bancario) |
| [documento_banco.pdf]            |
+----------------------------------+
```

**Paso 2 - Persona que paga nominas:**
```
+----------------------------------+
| Ver PDF adjunto                  |
| Comparar numero cuenta           |
| [✓] Verificado                   |
+----------------------------------+
```

#### 6.8.3 Estados de Verificacion Cuenta

| Estado | Significado |
|--------|-------------|
| Pendiente | PDF subido, esperando verificacion |
| Verificado | Numero coincide con documento (check marcado) |
| Rechazado | No coincide, trabajador debe corregir |

#### 6.8.4 Flujo Completo - Primer Acceso

```
EMAIL BIENVENIDA (Usuario + Enlace)
         |
         v
Trabajador crea contraseña
         |
         v
Completa datos obligatorios:
- Nombre, Apellidos
- Fecha nacimiento
- Telefono, Email
- Direccion, CP, Ciudad
- DNI, Nº Afiliacion SS
         |
         v
Introduce cuenta bancaria (IBAN)
         |
         v
Sube PDF del banco
         |
         v
PERSONA QUE PAGA NOMINAS
         |
         v
Verifica PDF vs Numero cuenta
         |
         v
[✓] Check = CUENTA VALIDADA
```

---

## 7. Tablas SQL

### 8.1 peticiones_trabajador

```sql
CREATE TABLE IF NOT EXISTS peticiones_trabajador (
    id INT AUTO_INCREMENT PRIMARY KEY,
    perfil_codigo VARCHAR(50) NOT NULL,
    solicitante_rol ENUM('GERENTE', 'DIRECTOR_RRHH') NOT NULL,
    solicitante_nombre VARCHAR(100),
    publicado_en VARCHAR(100),
    fecha_publicacion_desde DATE,
    fecha_publicacion_hasta DATE,
    estado ENUM('ABIERTA', 'EN_PROCESO', 'CUBIERTA', 'CANCELADA') DEFAULT 'ABIERTA',
    candidato_contratado_id BIGINT UNSIGNED,
    fecha_cubierta DATE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_perfil (perfil_codigo),
    INDEX idx_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 8.2 alertas_peticion

```sql
CREATE TABLE IF NOT EXISTS alertas_peticion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    peticion_id INT NOT NULL,
    tipo_alerta ENUM('NUEVA_PETICION', 'PETICION_CUBIERTA', 'PETICION_CANCELADA') NOT NULL,
    mensaje TEXT,
    estado ENUM('PENDIENTE', 'VISTA', 'COMPLETADA') DEFAULT 'PENDIENTE',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_peticion (peticion_id),
    INDEX idx_estado (estado),
    FOREIGN KEY (peticion_id) REFERENCES peticiones_trabajador(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 8. Dashboard RRHH

**Roles:** Evaluador, Entrevistador, Director RRHH, Gerente (pueden ser la misma persona)

**Acceso:** Menu RRHH > Dashboard

### 9.1 OFERTAS ACTIVAS

Ordenadas por prioridad.

| Prioridad | Perfil | Posicion | Plazas | Portal | Desde | Hasta | Estado |
|-----------|--------|----------|--------|--------|-------|-------|--------|
| MUY_ALTA | PESCADERIA | Dependiente/a Pescaderia | 2 | InfoJobs | 13/02/2026 | 14/04/2026 | ACTIVA |
| ALTA | LOGISTICA | Operario/a Logistica | 2 | InfoJobs | 27/01/2026 | 28/03/2026 | ACTIVA |
| MEDIA | BECARIO | Becario Administracion | 1 | - | - | - | ACTIVA |

### 9.1.1 Prioridades Disponibles

| Prioridad | Orden | Uso |
|-----------|-------|-----|
| MUY_ALTA | 1 | Urgente, cubrir inmediatamente |
| ALTA | 2 | Prioritario |
| MEDIA | 3 | Normal |
| BAJA | 4 | Puede esperar |
| MUY_BAJA | 5 | Sin urgencia |

### 9.2 CANDIDATOS

| Perfil | Total | Sin Validar | Con Duda |
|--------|-------|-------------|----------|
| LOGISTICA | 67 | 65 | 2 |
| PESCADERIA | 7 | 4 | 3 |
| PRODUCCION | 18 | 17 | 1 |
| ADMINISTRATIVO | 4 | 4 | 0 |
| SIN CLASIFICAR | 216 | 216 | 0 |
| **TOTAL** | **312** | **306** | **6** |

### 9.3 ENTREVISTAS

Ordenadas por dia y hora.

| Dia | Hora | Nombre | Apellido | Perfil | Tipo |
|-----|------|--------|----------|--------|------|
| 19/02/2026 | 10:00 | Adela | Ruano | PESCADERIA | 1a Entrevista |
| 19/02/2026 | 11:30 | Angel | Garcia | LOGISTICA | 1a Entrevista |
| 20/02/2026 | 09:00 | Carmen | Lopez | PESCADERIA | 2a Entrevista |
| 21/02/2026 | 10:00 | Borja | Mendez | LOGISTICA | 1a Entrevista |

---

## 9. Dashboard LLAMADOR

**Rol:** Llamador (persona que realiza las llamadas telefonicas)

**Acceso:** Menu RRHH > Mi Panel

### 10.1 Pantalla 1: Panel Principal

Resumen de tareas pendientes **ordenadas por urgencia** (mas urgente primero).

```
+--------------------------------------------------+
|  PENDIENTE LLAMAR CONTRATADO                     |
+--------------------------------------------------+
|  Carmen Lopez - PESCADERIA                       |
+--------------------------------------------------+

+--------------------------------------------------+
|  PENDIENTE LLAMAR CODIGOS Y 2a ENTREVISTA        |
+--------------------------------------------------+
|  Manuel Perez - PESCADERIA                       |
+--------------------------------------------------+

+--------------------------------------------------+
|  ENTREVISTAS DE HOY                              |
+--------------------------------------------------+
|  10:00  Adela Ruano - PESCADERIA - 1a  [ v ]     |
|  11:30  Angel Garcia - LOGISTICA - 1a  [ v ]     |
|  16:00  Pedro Gomez - PESCADERIA - 2a  [ v ]     |
+--------------------------------------------------+

+--------------------------------------------------+
|  LLAMADAS PARA ENTREVISTAS                       |
+--------------------------------------------------+
|  [!] MUY ALTA                                    |
|      Dependiente/a de Pescaderia .......... 15   |
|                                                  |
|  [!] ALTA                                        |
|      Operario/a Logistico ................. 6    |
|                                                  |
|  [ ] MEDIA                                       |
|      Becario Administracion ............... 3    |
+--------------------------------------------------+
```

**Orden de urgencia (de mas a menos):**
1. Contratado - cerrar incorporacion
2. Codigos y 2a Entrevista - candidatos listos para avanzar
3. Entrevistas de Hoy - gestionar llegadas
4. Llamadas para Entrevistas - concertar citas nuevas

**Desplegable en Entrevistas de Hoy:**
- **Presentado** → El candidato ha llegado, pasa al Entrevistador
- **No Presentado** → El candidato va a DESCARTADOS (motivo: NO_ASISTIO, sin email)

### 10.2 Vista Detallada de Llamadas

**Acceso:** Menu RRHH > Llamadas > Llamadas para Entrevistas

| ID | Nombre | Apellido | Telefono | Perfil | Veh | B | C | CAP | Car | Exp | CV | Estado | Intentos | Notas |
|----|--------|----------|----------|--------|-----|---|---|-----|-----|-----|-----|--------|----------|-------|
| 65 | [Adela] | [Ruano] | [675 942 449] | PESCADERIA | [S] | [S] | [N] | [N] | [N] | [20.3] | [+] | [ v ] | [ v ] | [ ] |

**Campos editables** (entre corchetes): para corregir errores del CV

**Al marcar Estado = Si:** aparecen columnas Dia y Hora

| ID | Nombre | Apellido | Telefono | Perfil | Estado | Intentos | Notas | Dia | Hora |
|----|--------|----------|----------|--------|--------|----------|-------|-----|------|
| 65 | [Adela] | [Ruano] | [675 942 449] | PESCADERIA | Si | 1 | interesada | [21/02] | [10:00] |

### 10.3 Funcionamiento

| Accion | Resultado |
|--------|-----------|
| Marca **Si** | Candidato sale de la lista, contador -1 |
| Marca **No** | Candidato sale de la lista, va a Descartados |
| Marca **Duda** | Candidato sale de la lista, va a Perfiles (Con Duda) |

---

## 10. Roles en Seleccion

| Rol | Dashboard | Funcion |
|-----|-----------|---------|
| Evaluador | Dashboard RRHH | Revisar perfiles, resolver dudas, decidir si/no |
| Entrevistador | Dashboard RRHH | Realizar entrevistas, evaluar candidatos |
| Director RRHH | Dashboard RRHH | Supervisar proceso, firmar contratos |
| Gerente | Dashboard RRHH | Crear peticiones de trabajador |
| Llamador | Dashboard LLAMADOR | Llamar candidatos, concertar entrevistas |

---

*Documento generado: ModuloRRHH v1.1*

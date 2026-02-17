# Estructura: CVs por Perfiles (Primera Fase)

## 1. Campos del Listado

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
| 16 | Entrevista | Desplegable Si/No | ENUM |

---

## 2. Ejemplo Visual

```
PESCADERIA (7)
ID |Nombre   |Apellido|Telefono   |Email               |Localid|Veh|B|C|CAP|Car|Puesto  |Exp |Est|CV |Entr
---|---------|--------|-----------|--------------------| ------|---|–|–|---|---|--------|----| –-|---|----
 65|Adela    |Ruano   |675 942 449|adelaruano1269@gmai |Cordoba|S  |S|N|N  |N  |PESCADE |20.3|-  |[+]|[ v]
180|Mari     |Carmen  |654 728 707|mc_gar@yahoo.es     |Lucena |N  |S|N|N  |N  |PESCADE |13.0|-  |[+]|[ v]
103|Angela   |Navarro |622-52-80-9|angelanavex@gmail.c |Cordoba|S  |N|N|N  |N  |PESCADE | 5.3|-  |[+]|[ v]
```

---

## 3. Perfiles Disponibles

| Perfil | Keywords | Candidatos |
|--------|----------|------------|
| PESCADERIA | pescad, carnicer, dependient, tienda, comercio | 7 |
| LOGISTICA | logistic, almacen, reparto, conductor, carnet C | 67 |
| PRODUCCION | sushi, envase, produccion, operario, fabrica | 18 |
| ADMINISTRATIVO | secretari, administrativ, contab, oficina | 4 |
| GESTION | grado ade, derecho, universidad, master | 0 |

**NOTA IMPORTANTE**: Esta estructura de campos y flujo aplica a los 5 perfiles anteriores.

### Candidatos PENDIENTES ASIGNAR (112)

Los candidatos sin perfil asignado tienen los **mismos 15 campos**, pero:

| Campo 15 en Perfiles | Campo 15 en Pendientes |
|----------------------|------------------------|
| Entrevista (Si/No)   | Asignar (desplegable)  |

**Ejemplo Visual**:
```
PENDIENTES ASIGNAR (112)
ID |Nombre   |Apellido|Telefono   |Email               |Localid|Veh|B|C|CAP|Car|Puesto|Exp |Est|CV |Asignar
---|---------|--------|-----------|--------------------| ------|---|–|–|---|---|------|----|-–-|---|--------
 12|Pedro    |Lopez   |666 123 456|pedrolopez@gmail.com|Montill|S  |S|N|N  |N  |  -   | 3.2|ESO|[+]|[    v ]
 45|Carmen   |Jimenez |654 987 321|cjimenez@hotmail.es |Cordoba|N  |S|N|N  |N  |  -   | 5.0|FP |[+]|[    v ]
 78|Francisco|Moreno  |622 555 888|fmoreno@yahoo.es    |Lucena |S  |S|S|S  |N  |  -   | 8.1|BAC|[+]|[    v ]
```

**Desplegable Asignar**: PESCADERIA, LOGISTICA, PRODUCCION, ADMINISTRATIVO, GESTION, DESCARTADO

**Flujo**:
1. Se aplican los filtros automaticos (experiencia < 1 año, distancia > 40 km)
2. Si NO pasan → Van a Descartados con motivo automatico
3. Si PASAN → Se quedan en "Pendientes Asignar"
4. Al seleccionar perfil en "Asignar" → Pasa al listado de ese perfil (con campo Entrevista)
5. Al seleccionar "DESCARTADO" → Va a Descartados (registra usuario que descarto)

---

## 4. Campo Entrevista (Logica)

El campo **Entrevista** es un desplegable con dos opciones:

### Si se selecciona "Si":
- El candidato pasa a la **Segunda Fase: Entrevistas**
- Se programa fecha de entrevista

### Si se selecciona "No":
- El candidato pasa a **Descartados**
- Se registra automaticamente:
  - Usuario que descarto (Jorge, Antonio, Carlos, etc.)
  - Fecha de descarte
  - Motivo: DESCARTE_MANUAL

---

## 5. Tipos de Descarte

### Descartes AUTOMATICOS (reglas configurables)

| Regla | Campo | Condicion | Valor | Motivo Mostrado |
|-------|-------|-----------|-------|-----------------|
| SIN_EXPERIENCIA | anos_experiencia | < | 1 ano | "Experiencia menor a 1 año" |
| DISTANCIA_EXCEDIDA | distancia_km | > | 40 km | "Vive a más de 40 km en coche de Córdoba" |
| DESCARTADO_PREVIO | - | Si aplica regla anterior | - | "Descartado en proceso anterior" |

**Nota**: La distancia se calcula en coche desde Córdoba (sede principal).

### Descartes MANUALES (decision del usuario)

| Motivo | Descripcion |
|--------|-------------|
| MALAS_REFERENCIAS | Descartado por malas referencias |
| NO_INTERESADO | Candidato no interesado |
| NO_CONTESTA | No contesta tras varios intentos |
| OTROS | Otros motivos (especificar en notas) |

Registro de descarte manual:
- descartado_por: "Jorge" / "Antonio" / "Carlos"
- fecha_descarte: timestamp automatico
- motivo_id: FK a motivos_descarte

---

## 6. Flujo de la Primera Fase

```
+----------------------------------+
|     CVs POR PERFILES             |
|     (Primera Fase)               |
+----------------------------------+
            |
            v
+----------------------------------+
|   Revisar candidato              |
|   - Ver datos                    |
|   - Ver CV detallado             |
+----------------------------------+
            |
            v
+----------------------------------+
|   Seleccionar Entrevista         |
|   [Si]  o  [No]                  |
+----------------------------------+
            |
      +-----+-----+
      |           |
     Si          No
      |           |
      v           v
+-----------+ +------------------+
|ENTREVISTAS| |   DESCARTADOS    |
|(2a Fase)  | |"Descartado por X"|
+-----------+ +------------------+
```

---

## 7. Tabla de Descartados

### Campos del Listado

| # | Campo | Descripcion | Tipo BD |
|---|-------|-------------|---------|
| 1 | ID | Identificador | INT |
| 2 | Nombre | Nombre candidato | VARCHAR |
| 3 | Apellido | Apellido 1 | VARCHAR |
| 4 | Telefono | Contacto | VARCHAR |
| 5 | Email | Correo | VARCHAR |
| 6 | Localidad | Ciudad | VARCHAR |
| 7 | Perfil | Perfil donde estaba (o PENDIENTE) | VARCHAR |
| 8 | Descartado por | AUTOMATICO o usuario (Jorge/Antonio/Carlos) | VARCHAR |
| 9 | Motivo | Razon del descarte | VARCHAR |
| 10 | Notas | Documentacion de entrevista (opcional) | TEXT |
| 11 | Fecha | Timestamp automatico (dia + hora) | TIMESTAMP |

### Ejemplo Visual

```
DESCARTADOS
ID |Nombre   |Apellido|Telefono   |Email               |Localid|Perfil    |Descartado por|Motivo                              |Notas         |Fecha
---|---------|--------|-----------|--------------------| ------|----------|--------------|------------------------------------|--------------|-----------
 23|Luis     |Ramirez |655 111 222|lramirez@gmail.com  |Jaen   |PENDIENTE |AUTOMATICO    |Vive a más de 40 km en coche        |-             |2026-02-17 14:35
 89|Maria    |Torres  |677 333 444|mtorres@hotmail.es  |Cordoba|LOGISTICA |Antonio       |Descartado en entrevista            |No encaja     |2026-02-16 10:20
 34|Jose     |Ruiz    |622 555 666|jruiz@yahoo.es      |Priego |PESCADERIA|Jorge         |No contesta tras varios intentos    |-             |2026-02-15 09:45
112|Elena    |Sanchez |666 777 888|esanchez@gmail.com  |Montoro|PENDIENTE |AUTOMATICO    |Experiencia menor a 1 año           |-             |2026-02-14 16:10
 56|Pedro    |Gomez   |644 222 111|pgomez@gmail.com    |Cordoba|PRODUCCION|Carlos        |Descartado en entrevista            |Poca actitud  |2026-02-13 11:30
```

**Nota**: La fecha se registra automaticamente con timestamp cuando se guarda el descarte.

---

## 8. Segunda Fase: ENTREVISTAS

### 8.1 Flujo de Asignacion de Llamadas

Cuando un candidato pasa a Entrevista (Entrevista = Si), se genera automaticamente una asignacion de llamada.

```
+---------------------------+
| Entrevista = Si           |
+---------------------------+
           |
           v
+---------------------------+
| VERIFICAR DISPONIBILIDAD  |
| Consultar:                |
| - rrhh_flujo_trabajadores |
|   (nivel = 4, activo = 1) |
| - Cuadrante semanal       |
+---------------------------+
           |
     +-----+-----+
     |           |
    SI          NO
     |           |
     v           v
+-----------+ +------------------+
| Asignar   | | ERROR:           |
| llamada a | | "No hay personal |
| trabajador| | disponible en    |
+-----------+ | nivel 4 o no     |
     |        | está en cuadrante"|
     v        +------------------+
+-----------+
| Trabajador|
| llama y   |
| concierta |
| entrevista|
+-----------+
```

**Condiciones para asignar llamada**:
1. El trabajador debe estar en `rrhh_flujo_trabajadores` con `nivel = 4`
2. El trabajador debe tener `activo = 1`
3. El trabajador debe aparecer en el **cuadrante semanal** del día

### 8.2 Tabla: asignacion_llamadas

| Campo | Descripcion | Tipo BD |
|-------|-------------|---------|
| id | Identificador | INT |
| candidato_id | FK a candidatos | INT |
| trabajador_id | FK a rrhh_flujo_trabajadores | INT |
| fecha_asignacion | Timestamp automatico | TIMESTAMP |
| estado | PENDIENTE / REALIZADA / NO_CONTESTA | ENUM |
| intentos | Numero de intentos de llamada | INT |
| notas | Observaciones de la llamada | TEXT |

### 8.3 Tabla: entrevistas

| Campo | Descripcion | Tipo BD |
|-------|-------------|---------|
| id | Identificador | INT |
| candidato_id | FK a candidatos | INT |
| llamada_id | FK a asignacion_llamadas | INT |
| fecha_entrevista | Fecha y hora programada | DATETIME |
| entrevistador_id | FK a rrhh_flujo_trabajadores | INT |
| estado | PROGRAMADA / REALIZADA / NO_ASISTIO | ENUM |
| resultado | PASA / DESCARTADO | ENUM |
| notas | Observaciones de la entrevista | TEXT |

### 8.4 Tabla: LLAMADAS

La tabla Llamadas tiene los **mismos 16 campos que Perfiles**, pero el campo 16 (Entrevista) tiene opciones diferentes.

**Campos 1-15**: Iguales que Perfiles (ID, Nombre, Apellido, Telefono, Email, Localidad, Veh, B, C, CAP, Carr, Puesto, Exp, Estudios, CV)

**Campo 16**: Entrevista (Si / No / Duda)

**Ejemplo Visual**:
```
LLAMADAS
ID |Nombre   |Apellido|Telefono   |Email               |Localid|Veh|B|C|CAP|Car|Puesto  |Exp |Est|CV |Entrevista
---|---------|--------|-----------|--------------------| ------|---|–|–|---|---|--------|----| –-|---|----------
 65|Adela    |Ruano   |675 942 449|adelaruano1269@gmai |Cordoba|S  |S|N|N  |N  |PESCADE |20.3|-  |[+]|[    v   ]
103|Angela   |Navarro |622-52-80-9|angelanavex@gmail.c |Cordoba|S  |N|N|N  |N  |PESCADE | 5.3|-  |[+]|[    v   ]
 78|Francisco|Moreno  |622 555 888|fmoreno@yahoo.es    |Lucena |S  |S|S|S  |N  |LOGIST  | 8.1|BAC|[+]|[    v   ]
```

### 8.5 Campo Entrevista en Llamadas (Logica)

| Opcion | Accion |
|--------|--------|
| **Si** | Abre campos Dia/Hora → pasa a ENTREVISTAS |
| **No** | Abre campo Motivo → pasa a DESCARTADOS |
| **Duda** | Abre campo Comentario → vuelve a PERFILES |

#### Si Entrevista = Si
```
+------------------+     +------------------+
| Entrevista: [Si] | --> | Dia:  [19/02/26] |
+------------------+     | Hora: [10:00   ] |
                         +------------------+
                                 |
                                 v
                         Guarda como DATETIME
                         2026-02-19 10:00:00
                                 |
                                 v
                         Pasa a ENTREVISTAS
```

#### Si Entrevista = No
```
+------------------+     +----------------------+
| Entrevista: [No] | --> | Motivo: [    v     ] |
+------------------+     +----------------------+
                                 |
                         - No interesado
                         - No contesta (3 intentos)
                         - Numero erroneo
                         - Otros
                                 |
                                 v
                         DESCARTADOS
                         (registra usuario + motivo + fecha)
```

#### Si Entrevista = Duda
```
+--------------------+     +-------------------------+
| Entrevista: [Duda] | --> | Comentario/Duda:        |
+--------------------+     | [____________________]  |
                           +-------------------------+
                                      |
                                      v
                           Vuelve a PERFILES con marca DUDA
```

**Nota**: El campo Duda permite multiples comentarios (historial de conversacion):
```
+------------------------------------------+
| HISTORIAL DE DUDAS - Candidato #65       |
+------------------------------------------+
| 17/02 10:30 - Maria (Llamador):          |
| "Pregunta si puede trabajar solo mañanas"|
+------------------------------------------+
| 17/02 11:15 - Jorge (Selector):          |
| "Si, turno de mañana disponible"         |
+------------------------------------------+
| 17/02 14:00 - Maria (Llamador):          |
| "Tambien pregunta por el sueldo"         |
+------------------------------------------+
| 17/02 14:30 - Jorge (Selector):          |
| "Segun convenio, se explica en entrev."  |
+------------------------------------------+
```

### 8.6 Flujo de DUDAS

**Ejemplo con Maria (Llamador) y Jorge (Selector)**:

```
1. MARIA (Llamador) llama a candidato
   Candidato pregunta: "¿Puedo trabajar solo mañanas?"
   Maria no sabe → marca DUDA + escribe pregunta
         |
         v
2. JORGE (Selector) ve la duda en Perfiles
   Lee: "Pregunta si puede trabajar solo mañanas"
   Jorge decide:
         |
    +----+----+
    |         |
   SI        NO
    |         |
    v         v
3a. JORGE marca Si        3b. JORGE marca No
    + escribe respuesta       → DESCARTADO
    "Si, turno manana
    disponible"
         |
         v
4. MARIA ve respuesta en Llamadas
   Lee: "Si, turno manana disponible"
         |
         v
5. MARIA llama de nuevo al candidato
   Le dice: "Si, puede trabajar solo mananas"
         |
         v
6. MARIA marca Si/No/Duda segun respuesta del candidato
```

**Resumen flujo DUDA**:

| Paso | Persona | Rol | Accion |
|------|---------|-----|--------|
| 1 | Maria | Llamador | Marca Duda + escribe comentario/pregunta |
| 2 | Jorge | Selector | Ve duda en Perfiles |
| 3a | Jorge | Selector | Si marca SI → escribe respuesta → vuelve a Llamadas |
| 3b | Jorge | Selector | Si marca NO → candidato a Descartados |
| 4 | Maria | Llamador | Ve respuesta del selector |
| 5 | Maria | Llamador | Llama de nuevo con la informacion |
| 6 | Maria | Llamador | Marca Si/No/Duda segun nueva respuesta |

### 8.7 Dashboard LLAMADOR

```
+============================================+
|  DASHBOARD LLAMADOR - Maria               |
+============================================+
|  +------------------------------------+   |
|  |  LLAMADAS PARA ENTREVISTAS         |   |
|  |           0/20                      |   |
|  +------------------------------------+   |
+============================================+
```

El contador se actualiza automaticamente al marcar Si, No o Duda (0/20 → 1/20 → 2/20...)

### 8.8 Dashboard ENTREVISTADOR

```
+============================================+
|  DASHBOARD ENTREVISTADOR - Jorge          |
+============================================+
|  +------------------------------------+   |
|  |  ENTREVISTAS              0/20     |   |
|  +------------------------------------+   |
|                                            |
|  Fecha      |Dia |Hora |Nombre   |Apellido|CV |
|  -----------|----|-----|---------|--------|---|
|  19/02/2026 |Mie |10:00|Adela    |Ruano   |[+]|
|  19/02/2026 |Mie |11:30|Angela   |Navarro |[+]|
|  20/02/2026 |Jue |09:00|Francisco|Moreno  |[+]|
|  20/02/2026 |Jue |12:00|Carmen   |Jimenez |[+]|
|                                            |
+============================================+
```

El contador se actualiza automaticamente al marcar Si, No o Duda.

**Campo Resultado en Entrevistas**:
| Opcion | Accion |
|--------|--------|
| Si | Se mantiene en ENTREVISTAS |
| No | DESCARTADOS (con motivo) |
| Duda | PERFILES con marca duda (historial comentarios) |

### 8.9 Vista CV (click en [+])

Al hacer click en [CV] se abre el curriculum con los campos estructurados:

```
+============================================+
|  CV CANDIDATO - Adela Ruano               |
+============================================+
|  ID: 65                                    |
|  Nombre: Adela                             |
|  Apellido: Ruano                           |
|  Telefono: 675 942 449                     |
|  Email: adelaruano1269@gmail.com           |
|  Localidad: Cordoba                        |
|  Vehiculo propio: Si                       |
|  Carnet B: Si                              |
|  Carnet C: No                              |
|  CAP: No                                   |
|  Carretillero: No                          |
|  Puesto: PESCADERIA                        |
|  Experiencia: 20.3 anos                    |
|  Estudios: -                               |
|                                            |
|  EXPERIENCIAS DETALLADAS:                  |
|  - Pescaderia Lopez (2015-2024) 9 anos    |
|  - Carniceria Martinez (2010-2015) 5 anos |
|  - Supermercado Dia (2004-2010) 6 anos    |
+============================================+
```

### 8.10 Vista Completa Entrevista (Dia de la entrevista)

El entrevistador ve toda la informacion del candidato:

```
+============================================================================+
|  ENTREVISTAS - Jorge                                                  0/20 |
+============================================================================+

+----------------------------------------------------------------------------+
|  CANDIDATO: Adela Ruano                                    Fecha: 19/02/26 |
|  Entrevista: Miercoles 10:00                               Dia: Mie        |
+----------------------------------------------------------------------------+
|  ID: 65 | Telefono: 675 942 449 | Email: adelaruano@gmail.com              |
|  Localidad: Cordoba | Veh: S | B: S | C: N | CAP: N | Carr: N              |
|  Puesto: PESCADERIA | Exp: 20.3 anos | Estudios: -                         |
+----------------------------------------------------------------------------+
|  CV: [+]                                                                   |
+----------------------------------------------------------------------------+
|  HISTORIAL COMENTARIOS/DUDAS:                                              |
|  17/02 10:30 - Maria (Llamador): "Pregunta si puede trabajar solo mananas" |
|  17/02 11:15 - Jorge (Selector): "Si, turno de manana disponible"          |
+----------------------------------------------------------------------------+
|  Resultado: [    v    ]                                                    |
+----------------------------------------------------------------------------+
```

**Campos visibles**:
- Todos los datos del candidato (16 campos)
- Fecha, Dia, Hora de entrevista
- CV completo [+]
- Historial de comentarios/dudas previas
- Resultado (desplegable)

### 8.11 Resultados de la Entrevista

| Opcion | Accion |
|--------|--------|
| **Entrega Codigos** | Pasa la entrevista → abre comentarios → siguiente filtro |
| **No** | Descartado → abre campo motivo |

#### Si Resultado = Entrega Codigos
```
+--------------------+     +---------------------------+
| Entrega Codigos    | --> | Comentarios/Valoracion:   |
+--------------------+     | [________________________]|
                           | [________________________]|
                           +---------------------------+
                                      |
                                      v
                           +---------------------------+
                           | 1. Guarda valoracion      |
                           | 2. Email auto al candidato|
                           | 3. Pasa a siguiente filtro|
                           +---------------------------+
```

**Registro guardado**:
- fecha_entrevista: DATETIME
- entrevistador_id: FK a rrhh_flujo_trabajadores
- resultado: 'ENTREGA_CODIGOS'
- valoracion: TEXT (comentarios del entrevistador)
- fecha_registro: TIMESTAMP automatico

#### Si Resultado = No
```
+------------------+     +----------------------+
| Resultado: [No]  | --> | Motivo: [    v     ] |
+------------------+     +----------------------+
                                 |
                         - No apto para el puesto
                         - Falta de experiencia
                         - No encaja con el equipo
                         - Otros (especificar)
                                 |
                                 v
                         DESCARTADOS
                         (registra entrevistador + motivo + fecha)
```

### 8.12 Sistema de Codigos (Gaming)

Cuando el candidato recibe "Entrega Codigos", se activa el sistema de aprendizaje:

**Flujo automatico**:
```
Entrega Codigos (entrevista)
         |
         v
+------------------------------------------+
|  EMAIL AUTOMATICO AL CANDIDATO           |
|                                          |
|  Para: adelaruano@gmail.com              |
|  Asunto: Registro Pescados La Carihuela  |
|                                          |
|  Enlace para registrarse y acceder       |
|  al sistema de codigos                   |
+------------------------------------------+
         |
         v
+------------------------------------------+
|  CANDIDATO SE REGISTRA                   |
|  - Introduce sus datos                   |
|  - Accede al sistema de codigos          |
+------------------------------------------+
         |
         v
+------------------------------------------+
|  SISTEMA GAMING - APRENDER CODIGOS       |
+------------------------------------------+
```

**Pantalla del juego**:
```
+============================================+
|  CODIGOS - Adela Ruano                    |
+============================================+
|                                            |
|  MODO PRACTICA                             |
|                                            |
|  Codigo: 90                                |
|                                            |
|  Cual es?                                  |
|                                            |
|  [ ] Lomo de Salmon                        |
|  [x] Rodajas de Salmon  -> Correcto!       |
|  [ ] Boquerones                            |
|                                            |
|  Racha: 5 seguidas                         |
|  Aciertos hoy: 45/50 (90%)                 |
|                                            |
+============================================+
```

**Caracteristicas del sistema**:
- Preguntas tipo test con codigo y opciones
- Practica ilimitada (gaming)
- Registro de progreso y aciertos
- El candidato practica hasta aprender los codigos

### 8.13 Roles en Segunda Fase

| Rol | Dashboard | Condicion | Funcion |
|-----|-----------|-----------|---------|
| Llamador | Llamadas para Entrevistas | nivel=4, activo=1, en cuadrante | Llama y concierta cita |
| Entrevistador | Entrevistas | (por definir) | Realiza la entrevista |

**Nota**: El llamador y el entrevistador pueden ser personas diferentes.

---

## 9. Tercera Fase: SEGUNDA ENTREVISTA

### 9.1 Flujo Post-Codigos

Despues de que el candidato practica los codigos (gaming), se le llama para concertar segunda entrevista.

```
GAMING CODIGOS (candidato practica)
         |
         v
+---------------------------+
| LLAMADA PARA              |
| SEGUNDA ENTREVISTA        |
| (misma persona u otra)    |
+---------------------------+
         |
    +----+----+----+
    |    |        |
   SI   NO      DUDA
    |    |        |
    v    v        v
+----+ +----+ +--------+
|2a  | |DESC| |PERFILES|
|ENTR| |    | |(duda)  |
+----+ +----+ +--------+
```

### 9.2 Segunda Entrevista - Resultados

```
SEGUNDA ENTREVISTA
         |
    +----+----+----+
    |    |        |
CONTRAT DUDA     NO
    |    |        |
    v    v        v
+----+ +------+ +----+
|CONT| |QUEDA | |DESC|
|RAT | |ENTREV| |    |
|ADO | |(com.)| +----+
+----+ +------+
```

**Resultados**:
| Opcion | Accion |
|--------|--------|
| Contratado | Pasa a CONTRATADOS (fin proceso) |
| Duda | Se queda en ENTREVISTAS con comentarios |
| No | Descartado con motivo |

### 9.3 DUDA en Entrevistas vs Llamadas

| Fase | Si es DUDA |
|------|------------|
| Llamadas | Vuelve a PERFILES (flujo Maria/Jorge) |
| Entrevistas | Se queda en ENTREVISTAS con comentarios |

### 9.4 Ficha del Candidato

Todos los comentarios se guardan en la ficha del candidato:

```
+============================================+
|  FICHA CANDIDATO - Adela Ruano            |
+============================================+
|  DATOS PERSONALES                          |
|  ID: 65 | Perfil: PESCADERIA               |
|  Telefono: 675 942 449                     |
|  Email: adelaruano@gmail.com               |
+--------------------------------------------+
|  HISTORIAL COMPLETO                        |
+--------------------------------------------+
|  15/02 - Asignada a perfil PESCADERIA      |
|  16/02 - Seleccionada para entrevista (Si) |
|  16/02 - Llamada por Maria                 |
|  16/02 - Duda: "Pregunta turno mananas"    |
|  16/02 - Jorge: "Si, turno disponible"     |
|  17/02 - Llamada OK, cita 19/02 10:00      |
|  19/02 - 1a Entrevista: Entrega Codigos    |
|  19/02 - Valoracion: "Buena actitud"       |
|  22/02 - Llamada 2a entrevista: 25/02      |
|  25/02 - 2a Entrevista: CONTRATADO         |
+--------------------------------------------+
|  RESULTADO FINAL: CONTRATADO               |
|  Fecha: 25/02/2026                         |
+============================================+
```

**Queda registrado**:
- Todos los comentarios de llamadas
- Todas las dudas y respuestas
- Valoraciones de entrevistas
- Resultado final (Contratado o Descartado)

---

## 10. FLUJO COMPLETO

```
+------------------+
|  ENTRADA CVs     |
|  (InfoJobs/Email)|
+------------------+
         |
         v
+------------------+
|  FILTROS AUTO    |
|  - Exp < 1 ano   |
|  - Dist > 40 km  |
+------------------+
         |
    +----+----+
    |         |
   PASA      NO --> DESCARTADOS (auto)
    |
    v
+------------------+
|  PENDIENTES      |
|  ASIGNAR         |
+------------------+
         |
         v (Asignar perfil)
+------------------+
|  CVs POR PERFIL  |
|  Entrevista      |
|  Si/No           |
+------------------+
         |
    +----+----+
    |         |
   SI        NO --> DESCARTADOS (manual)
    |
    v
+------------------+
|  LLAMADAS PARA   |
|  ENTREVISTAS     |
|  Si/No/Duda      |
+------------------+
         |
    +----+----+----+
    |    |        |
   SI   NO      DUDA --> PERFILES
    |    |
    |    v
    |  DESCARTADOS
    v
+------------------+
|  1a ENTREVISTA   |
|  Codigos/No/Duda |
+------------------+
         |
    +----+----+----+
    |    |        |
 CODIGOS NO     DUDA --> QUEDA ENTREVISTAS
    |    |
    |    v
    |  DESCARTADOS
    v
+------------------+
|  GAMING CODIGOS  |
|  (practica)      |
+------------------+
         |
         v
+------------------+
|  LLAMADA 2a      |
|  ENTREVISTA      |
|  Si/No/Duda      |
+------------------+
         |
    +----+----+----+
    |    |        |
   SI   NO      DUDA --> PERFILES
    |    |
    |    v
    |  DESCARTADOS
    v
+------------------+
|  2a ENTREVISTA   |
|  Contrat/No/Duda |
+------------------+
         |
    +----+----+----+
    |    |        |
CONTRAT NO      DUDA --> QUEDA ENTREVISTAS
    |    |
    |    v
    |  DESCARTADOS
    v
+------------------+
|  CONTRATADO      |
|  (fin proceso)   |
+------------------+
```

---

## 11. Integracion ERP: CONTRATADO → OPERADORES

### 11.1 Flujo de Contratacion

Cuando un candidato pasa a CONTRATADO, se crea automaticamente un registro en la tabla `operadores` del ERP.

```
CONTRATADO (seleccion)
         |
         v
+---------------------------+
| Crear registro en         |
| tabla OPERADORES (ERP)    |
| ID automatico             |
+---------------------------+
         |
         v
+---------------------------+
| Candidato ahora es        |
| EMPLEADO en el sistema    |
+---------------------------+
```

### 11.2 Mapeo de Campos: candidatos → operadores

| Campo CANDIDATOS | Campo OPERADORES | Tipo |
|------------------|------------------|------|
| nombre | Nombre | char(30) |
| apellido1 | Apellido1 | char(15) |
| apellido2 | Apellido2 | char(15) |
| email | email | varchar(255) |
| telefono | telefono | varchar(255) |
| dni | Nif | varchar(255) |
| residencia | Poblacion | varchar(50) |
| provincia | Provincia | varchar(50) |
| codigo_postal | Cp | char(5) |
| perfil_codigo | categoria_profesional_id | int (FK) |
| - | activo | 1 (nuevo empleado) |
| - | idEmpresa | (config) |
| - | fecha_desde | fecha contratacion |
| - | created_at | timestamp auto |

### 11.3 Campos que se generan automaticamente

| Campo OPERADORES | Valor |
|------------------|-------|
| id | AUTO_INCREMENT |
| activo | 1 |
| borrado | 0 |
| created_at | CURRENT_TIMESTAMP |
| fecha_desde | Fecha de contratacion |
| idEmpresa | Segun configuracion |

### 11.4 Flujo Completo de Contratacion

```
CONTRATADO
    |
    v
+---------------------------+
| 1. Crear OPERADORES       |
|    ID automatico          |
|    Datos del candidato    |
+---------------------------+
    |
    v
+---------------------------+
| 2. Crear CONTRATOS_USUARIO|
|    ID = ultimo + 1        |
|    user_id = operador.id  |
+---------------------------+
    |
    v
+---------------------------+
| 3. Actualizar CANDIDATOS  |
|    estado = CONTRATADO    |
+---------------------------+
    |
    v
+---------------------------+
| 4. Registrar HISTORIAL    |
+---------------------------+
    |
    v
+---------------------------+
| 5. Crear relacion         |
|    candidato_operador     |
+---------------------------+
```

### 11.5 Procedimiento SQL

```sql
CALL sp_contratar_candidato(
    p_candidato_id,           -- ID del candidato
    p_id_empresa,             -- Empresa (ej: '001')
    p_categoria_profesional_id, -- Categoria
    p_horas_semana,           -- Horas/semana
    p_tcontrato,              -- Tipo contrato
    p_dias,                   -- Dias trabajo
    p_horario,                -- Horario
    @operador_id,             -- OUT: ID operador creado
    @contrato_id              -- OUT: ID contrato creado
);
```

### 11.6 Campos adicionales a completar

Estos campos se completan despues de la contratacion:

| Campo | Descripcion |
|-------|-------------|
| login | Usuario para acceso al sistema |
| Password | Contraseña inicial |
| fecha_nacimiento | Fecha nacimiento |
| NAF | Numero Afiliacion SS |

---

*Documento generado: 2026-02-17*

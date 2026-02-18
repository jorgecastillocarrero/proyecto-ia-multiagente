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

## 12. PORTAL CANDIDATO → PORTAL EMPLEADO

### 12.1 Flujo Completo Portal Candidato

```
1. PRIMERA ENTREVISTA
   Resultado: Entrega Codigos
         |
         v
2. EMAIL AUTOMATICO
   "Registrate en el portal para practicar los codigos"
         |
         v
3. PORTAL CANDIDATO
   - Candidato se registra
   - Completa sus datos personales
   - Practica codigos (gaming)
         |
         v
4. LLAMADA ULTIMA ENTREVISTA
   Se le llama para concertar cita
         |
         v
5. ULTIMA ENTREVISTA
   - Se comprueban los codigos
   - Se resuelven dudas finales
         |
    +----+----+
    |         |
 SABE       NO SABE
 CODIGOS    CODIGOS
    |         |
    v         v
CONTRATADO  DUDA/DESCARTADO
    |
    v
6. PORTAL EMPLEADO
   - Se crea ID automatico (siguiente al ultimo)
   - Datos transferidos del portal candidato
   - Director RRHH completa datos contrato
```

### 12.2 Transferencia de Datos Automatica

Cuando el candidato es marcado como CONTRATADO:

1. Se crea automaticamente usuario en **Portal Empleado**
2. El ID es el **siguiente al ultimo ID existente**
3. Los datos del portal candidato se transfieren automaticamente

```
PORTAL CANDIDATO                 PORTAL EMPLEADO
(practica codigos)               (trabajador)
       |                                |
       |  CONTRATADO                    |
       +--------------->----------------+
       |                                |
   Datos completados:              Se crea usuario:
   - Nombre                        - ID: 248 (auto)
   - Apellidos                     - Nombre
   - DNI                           - Apellidos
   - Email                         - DNI
   - Telefono                      - Email
   - Direccion                     - Telefono
   - Cuenta bancaria               - Direccion
                                   - Cuenta bancaria
                                   |
                                   v
                              Director RRHH completa:
                              - Horas
                              - Tipo horario
                              - Categoria profesional
                              - Fecha desde
                              - Fecha hasta
```

### 12.3 Datos Minimos Portal Candidato

El candidato completa estos datos minimos en el portal de candidatos:

| # | Campo | Obligatorio |
|---|-------|-------------|
| 1 | Nombre | Si |
| 2 | Primer apellido | Si |
| 3 | Telefono | Si |
| 4 | Correo electronico | Si |

**Estos 4 datos minimos se transfieren automaticamente al Portal Empleado.**

### 12.4 Portal Empleado: Verificacion de Documentos

Una vez creado el usuario en Portal Empleado, el **nuevo empleado** verifica y completa todos los documentos requeridos:

| Documento | Accion |
|-----------|--------|
| DNI/NIE | Subir escaneado |
| Cuenta bancaria | Introducir IBAN |
| Direccion completa | Completar datos |
| Carnet manipulador alimentos | Subir |
| Permiso conduccion (si aplica) | Subir |
| Politica proteccion datos | Firmar |
| Confidencialidad | Firmar |
| Derechos de imagen | Firmar |

---

## 13. Documentacion del EMPLEADO

### 13.1 Documentos requeridos por el Trabajador

Basado en la tabla `documentacion_trabajadores` del ERP:

#### CONDUCCION (si aplica al puesto)

| ID | Codigo | Documento | Aviso | Tipo |
|----|--------|-----------|-------|------|
| 80 | 021 | Permiso de conduccion | 1 dia | Manual |
| 81 | 022 | Carnet carretillero | 1500 dias | Manual |
| 83 | 023 | CAP Curso | 180 dias | Manual |
| 93 | 026 | Solicitud puntos carnet | - | Manual |
| 78 | 025 | Tacografo | 28 dias | Manual |

#### PROTECCION DE DATOS

| ID | Codigo | Documento | Tipo |
|----|--------|-----------|------|
| 82 | 006 | Politica proteccion de datos | Automatico |
| 84 | 011 | Confidencialidad | Automatico |
| 89 | 014 | Cuenta bancaria | Automatico |
| 90 | 015 | Derechos de imagen | Automatico |
| 91 | 016 | Material empresa | Automatico |

#### PROTOCOLOS

| ID | Codigo | Documento | Tipo |
|----|--------|-----------|------|
| 88 | 013 | Identificacion y actuacion acoso | Automatico |

#### RIESGOS LABORALES

| ID | Codigo | Documento | Aviso | Tipo |
|----|--------|-----------|-------|------|
| 75 | 003 | Formacion | 1095 dias (3 anos) | Automatico |
| 76 | 004 | Equipos proteccion individual | - | Automatico |
| 77 | 005 | Informacion | - | Automatico |

#### SALUD

| ID | Codigo | Documento | Aviso | Tipo |
|----|--------|-----------|-------|------|
| 73 | 001 | Carnet manipulador de alimentos | 1460 dias (4 anos) | Automatico |
| 74 | 002 | Reconocimiento medico | 365 dias (1 ano) | Automatico |

### 13.2 Flujo de Documentacion Empleado

```
CONTRATADO
    |
    v
+---------------------------+
| Director RRHH recibe      |
| aviso "Pendiente Datos    |
| Manuel Perez"             |
+---------------------------+
    |
    v
+---------------------------+
| Solicitar documentos al   |
| nuevo empleado:           |
| - DNI                     |
| - Cuenta bancaria         |
| - Permisos conduccion     |
| - Etc.                    |
+---------------------------+
    |
    v
+---------------------------+
| Empleado aporta docs      |
| Subir a sistema           |
+---------------------------+
    |
    v
+---------------------------+
| Verificar y validar       |
| Marcar como completado    |
+---------------------------+
```

### 13.3 Dashboard Director RRHH

```
+============================================================================+
|  DASHBOARD DIRECTOR RRHH                                                    |
+============================================================================+

+------------------------------------------+
|  PENDIENTES DATOS TRABAJADORES           |
+------------------------------------------+
|  [!] Manuel Perez     - 5 docs pendiente |
|  [!] Carmen Rodriguez - 3 docs pendiente |
|  [ ] Luis Sanchez     - Completado       |
+------------------------------------------+

+------------------------------------------+
|  DOCUMENTOS POR CADUCAR (30 dias)        |
+------------------------------------------+
|  [!] Juan Lopez - Reconocimiento medico  |
|      Caduca: 15/03/2026                  |
|  [!] Ana Garcia - CAP Curso              |
|      Caduca: 20/03/2026                  |
+------------------------------------------+

+------------------------------------------+
|  ALTAS PENDIENTES SEGURIDAD SOCIAL       |
+------------------------------------------+
|  [ ] Manuel Perez - Esperando datos      |
|  [ ] Carmen Rodriguez - Datos completos  |
+------------------------------------------+
```

---

## 14. Documentacion de la EMPRESA

### 14.1 Documentos que genera la Empresa

| Documento | Responsable | Cuando |
|-----------|-------------|--------|
| Contrato de trabajo | Director RRHH | Al contratar |
| Alta Seguridad Social | Resp. SS | Antes inicio |
| Entrega EPI | Prevencion | Primer dia |
| Formacion PRL | Prevencion | Primera semana |
| Politica proteccion datos | RRHH | Firma contrato |
| Clausula confidencialidad | RRHH | Firma contrato |
| Protocolo acoso | RRHH | Firma contrato |

### 14.2 Ficha del Nuevo Empleado (Director RRHH)

Cuando el candidato es CONTRATADO:
1. Se crea automaticamente la ficha con sus datos personales
2. Se asigna automaticamente el siguiente ID disponible
3. El Director RRHH entra en la ficha y completa:

```
+============================================================================+
|  FICHA EMPLEADO - Manuel Perez                           ID: 247 (auto)    |
+============================================================================+
|                                                                             |
|  DATOS PERSONALES (automaticos del portal candidato)                        |
|  +-----------+---------------------------+                                  |
|  | Nombre    | Manuel                    |                                  |
|  | Apellidos | Perez Garcia              |                                  |
|  | DNI       | 12345678X                 |                                  |
|  | Email     | mperez@gmail.com          |                                  |
|  | Telefono  | 654 321 987               |                                  |
|  | Direccion | C/ Principal 15, Cordoba  |                                  |
|  +-----------+---------------------------+                                  |
|                                                                             |
|  DATOS CONTRATO (a rellenar por Director RRHH)                              |
|  +-------------------------+---------------------------+                    |
|  | Horas                   | [    v    ] horas/semana  |  <- Rellenar       |
|  | Tipo de horario         | [    v    ]               |  <- Rellenar       |
|  | Categoria profesional   | [    v    ]               |  <- Rellenar       |
|  | Fecha desde             | [  /  /    ]              |  <- Rellenar       |
|  | Fecha hasta             | [  /  /    ]              |  <- Rellenar       |
|  +-------------------------+---------------------------+                    |
|                                                                             |
|  [ Guardar ]                                                                |
|                                                                             |
+============================================================================+
```

### 14.3 Campos que completa el Director RRHH

| # | Campo | Descripcion | Tipo | Ejemplo |
|---|-------|-------------|------|---------|
| 1 | Horas | Horas semanales de trabajo | INT | 40, 35, 20 |
| 2 | Tipo de horario | Tipo de jornada/turno | ENUM | Mañana, Tarde, Partido, Rotativo |
| 3 | Categoria profesional | Categoria segun convenio | FK | Oficial 1a, Peon, Administrativo |
| 4 | Fecha desde | Fecha inicio del contrato | DATE | 01/03/2026 |
| 5 | Fecha hasta | Fecha fin del contrato (si temporal) | DATE | 01/09/2026 o NULL (indefinido) |

### 14.4 Opciones de Tipo de Horario

| Codigo | Descripcion |
|--------|-------------|
| MANANA | Turno de mañana |
| TARDE | Turno de tarde |
| PARTIDO | Jornada partida |
| ROTATIVO | Turnos rotativos |
| NOCHE | Turno de noche |
| FLEXIBLE | Horario flexible |

### 14.5 Flujo Director RRHH

```
CANDIDATO CONTRATADO
         |
         v
+---------------------------+
| Sistema crea ficha auto   |
| - Datos personales        |
| - ID siguiente disponible |
+---------------------------+
         |
         v
+---------------------------+
| Dashboard Director RRHH   |
| "Pendiente Datos:         |
|  Manuel Perez"            |
+---------------------------+
         |
         v
+---------------------------+
| Director abre ficha       |
| Completa:                 |
| - Horas                   |
| - Tipo horario            |
| - Categoria profesional   |
| - Fecha desde             |
| - Fecha hasta             |
+---------------------------+
         |
         v
+---------------------------+
| Guardar                   |
| → Notifica a Resp. SS     |
|   para tramitar alta      |
+---------------------------+
```

---

## 15. Acciones CONJUNTAS

### 15.1 Firma de Contrato

```
+---------------------------+     +---------------------------+
|     EMPRESA               |     |     EMPLEADO              |
+---------------------------+     +---------------------------+
|                           |     |                           |
| 1. Generar contrato       |     |                           |
|    con datos              |     |                           |
|                           |     |                           |
| 2. Enviar por email       |---->| 3. Recibir contrato       |
|    o presencial           |     |                           |
|                           |     | 4. Revisar y firmar       |
|                           |<----| 5. Devolver firmado       |
|                           |     |                           |
| 6. Archivar contrato      |     |                           |
|    firmado                |     |                           |
+---------------------------+     +---------------------------+
```

### 15.2 Alta Seguridad Social

```
DATOS EMPLEADO COMPLETOS
         |
         v
+---------------------------+
| Responsable SS recibe     |
| notificacion automatica   |
+---------------------------+
         |
         v
+---------------------------+
| Tramitar alta en TGSS     |
| Antes de fecha inicio     |
+---------------------------+
         |
         v
+---------------------------+
| Registrar NAF en sistema  |
| (Numero Afiliacion SS)    |
+---------------------------+
```

### 15.3 Checklist Pre-Incorporacion

| # | Tarea | Responsable | Estado |
|---|-------|-------------|--------|
| 1 | Datos personales completos | Empleado | [ ] |
| 2 | DNI escaneado | Empleado | [ ] |
| 3 | Cuenta bancaria | Empleado | [ ] |
| 4 | Contrato generado | Director RRHH | [ ] |
| 5 | Contrato firmado | Ambos | [ ] |
| 6 | Alta Seguridad Social | Resp. SS | [ ] |
| 7 | NAF registrado | Resp. SS | [ ] |
| 8 | EPI preparados | Prevencion | [ ] |
| 9 | Formacion PRL programada | Prevencion | [ ] |

---

## 16. Automatizaciones y ALERTAS

### 16.1 Notificaciones al CONTRATAR

Cuando un candidato pasa a CONTRATADO se disparan DOS alertas:

```
ULTIMA ENTREVISTA
         |
    CONTRATADO
         |
    +----+----+
    |         |
    v         v
ALERTA 1   ALERTA 2
Director   Hermi (SS)
RRHH       "Pendiente"
```

#### ALERTA 1: Director RRHH
```
Para: Director RRHH
Asunto: Nuevo contratado - Manuel Perez

Mensaje:
"Se ha contratado a Manuel Perez.
Perfil: LOGISTICA
Pendiente completar datos del contrato."
```

#### ALERTA 2: Hermi (Asesor SS) - AVISO PREVIO
```
Para: Hermi (Asesor SS)
Asunto: Pendiente alta SS - Manuel Perez

Mensaje:
"Nuevo contratado pendiente de alta en Seguridad Social.
Nombre: Manuel Perez
Perfil: LOGISTICA

Pendiente recibir datos del contrato del Director RRHH."
```

**Nota**: Esta alerta es solo para que Hermi sepa que tiene que estar pendiente. Todavia NO tiene los datos para tramitar el alta.

### 16.2 Quien completa cada dato

#### Director RRHH completa:

| # | Campo | Descripcion |
|---|-------|-------------|
| 1 | Categoria | Categoria profesional |
| 2 | Horas | Horas semanales |
| 3 | Comienzo contrato | Fecha inicio |
| 4 | Fin contrato | Fecha fin (si temporal) |

#### Hermi (Asesor SS) completa:

| # | Campo | Descripcion |
|---|-------|-------------|
| 1 | Tipo de contrato | Temporal, indefinido, etc. |
| 2 | Codigo de contrato | Codigo oficial del contrato |

#### Trabajador aporta (en Portal Empleado):

**Datos obligatorios para TODOS:**

| # | Campo | Descripcion |
|---|-------|-------------|
| 1 | DNI/NIE | Documento escaneado |
| 2 | Cuenta bancaria | IBAN |
| 3 | Numero de afiliacion (NAF) | Seguridad Social |
| 4 | Direccion | Domicilio completo |
| 5 | Telefono | Movil de contacto |
| 6 | Email | Correo electronico |
| 7 | Fecha de nacimiento | DD/MM/AAAA |
| 8 | Codigo postal | CP |
| 9 | Municipio | Localidad |

**Carnets/Permisos (segun perfil):**

| # | Campo | Obligatorio | Condicion | Validez |
|---|-------|-------------|-----------|---------|
| 10 | Carnet C (camion) | No | Opcional | Si |
| 11 | CAP | No | Opcional (si tiene carnet C) | Si |
| 12 | Carnet carretillero | **SI** | **Obligatorio si perfil = LOGISTICA** | Si |
| 13 | Certificado de puntos | **SI** | **Obligatorio si usa vehiculo empresa** | Si |
| 14 | Tacografo | **SI** | **Obligatorio si usa vehiculo empresa** | Si |

**Notas importantes**:
- El carnet carretillero es **obligatorio** para todos los trabajadores del departamento de LOGISTICA
- El certificado de puntos y tacografo son **obligatorios** para trabajadores que usen vehiculos de la empresa para repartir (logistica)
- Todos los permisos de conduccion tienen **fecha de validez/caducidad**

### 16.2.1 Alertas de Seguimiento - Permisos de Conduccion

Se crea un sistema de alertas para **TODOS los trabajadores de la empresa** cuando sus permisos estan proximos a caducar.

```
+============================================================================+
|  ALERTAS CADUCIDAD PERMISOS - Director RRHH                                |
+============================================================================+
|                                                                             |
|  [!] PROXIMOS A CADUCAR (30 dias)                                          |
|  +------------------------------------------+------------------+---------+ |
|  | Trabajador        | Documento            | Caduca           | Dias    | |
|  +------------------------------------------+------------------+---------+ |
|  | Juan Lopez        | Carnet C             | 15/03/2026       | 25      | |
|  | Pedro Garcia      | CAP                  | 20/03/2026       | 30      | |
|  | Ana Martinez      | Tacografo            | 18/03/2026       | 28      | |
|  | Luis Sanchez      | Certificado puntos   | 22/03/2026       | 32      | |
|  +------------------------------------------+------------------+---------+ |
|                                                                             |
|  [X] CADUCADOS                                                             |
|  +------------------------------------------+------------------+---------+ |
|  | Carlos Ruiz       | Carnet carretillero  | 10/02/2026       | -8      | |
|  +------------------------------------------+------------------+---------+ |
|                                                                             |
+============================================================================+
```

#### Dias de aviso por documento:

| Documento | Dias aviso antes de caducar |
|-----------|----------------------------|
| Carnet C | 30 dias |
| CAP | 180 dias (6 meses) |
| Carnet carretillero | 30 dias |
| Certificado de puntos | 30 dias |
| Tacografo | 28 dias |

### 16.2.2 Documentos de SALUD

| # | Documento | Obligatorio | Validez | Dias aviso |
|---|-----------|-------------|---------|------------|
| 15 | Carnet Manipulador de Alimentos | **SI** | 4 años (desde fecha diploma) | 60 dias |
| 16 | Reconocimiento Medico | **SI** | 1 año (desde fecha realizacion) | 30 dias |

**Notas**:
- El carnet de manipulador es **obligatorio para TODOS** - validez **4 años**
- El reconocimiento medico es **obligatorio para TODOS** - validez **1 año**

### 16.2.3 Dashboard Reconocimientos Medicos Pendientes

El reconocimiento medico aparece en el dashboard como tarea pendiente:

```
+============================================================================+
|  RECONOCIMIENTOS MEDICOS - Director RRHH                                   |
+============================================================================+
|                                                                             |
|  [!] PENDIENTES DE REALIZAR                                                |
|  +------------------------------------------+------------------+---------+ |
|  | Trabajador        | Ultimo reconocimiento| Caduca           | Estado  | |
|  +------------------------------------------+------------------+---------+ |
|  | Manuel Perez      | (nuevo empleado)     | -                | PENDIENTE| |
|  | Carmen Rodriguez  | (nuevo empleado)     | -                | PENDIENTE| |
|  +------------------------------------------+------------------+---------+ |
|                                                                             |
|  [!] PROXIMOS A CADUCAR (30 dias)                                          |
|  +------------------------------------------+------------------+---------+ |
|  | Juan Lopez        | 20/03/2025           | 20/03/2026       | 30 dias | |
|  | Ana Martinez      | 25/03/2025           | 25/03/2026       | 35 dias | |
|  +------------------------------------------+------------------+---------+ |
|                                                                             |
|  [X] CADUCADOS                                                             |
|  +------------------------------------------+------------------+---------+ |
|  | Pedro Garcia      | 10/02/2025           | 10/02/2026       | -8 dias | |
|  +------------------------------------------+------------------+---------+ |
|                                                                             |
|  [Programar reconocimientos]  [Exportar listado]                           |
+============================================================================+
```

### 16.2.4 Automatizacion Certificados Medicos

Una vez realizado el reconocimiento medico, un **script automatico** descarga los certificados:

```
RECONOCIMIENTO MEDICO REALIZADO
         |
         v
+---------------------------+
| SCRIPT AUTOMATICO         |
| (ejecucion programada)    |
+---------------------------+
         |
         v
+---------------------------+
| 1. Accede a web empresa   |
|    servicio prevencion    |
+---------------------------+
         |
         v
+---------------------------+
| 2. Descarga certificados  |
|    medicos nuevos         |
+---------------------------+
         |
         v
+---------------------------+
| 3. Asocia certificado     |
|    a ficha del trabajador |
+---------------------------+
         |
         v
+---------------------------+
| 4. Actualiza fecha        |
|    reconocimiento y       |
|    fecha caducidad (+1año)|
+---------------------------+
         |
         v
+---------------------------+
| 5. Marca como COMPLETADO  |
|    en el dashboard        |
+---------------------------+
```

**Configuracion del script:**

| Parametro | Valor |
|-----------|-------|
| Frecuencia | Diaria / Semanal (configurable) |
| URL | Web servicio prevencion |
| Credenciales | Almacenadas en config segura |
| Destino | Ficha trabajador (documentos) |
| Formato | PDF |

### 16.2.5 Resumen Documentos con Validez

| Documento | Validez | Dias aviso | Obligatorio |
|-----------|---------|------------|-------------|
| Carnet C | Variable | 30 dias | Si usa vehiculo |
| CAP | 5 años | 180 dias | Si tiene Carnet C |
| Carnet carretillero | Variable | 30 dias | LOGISTICA |
| Certificado puntos | Anual | 30 dias | Si usa vehiculo empresa |
| Tacografo | Variable | 28 dias | Si usa vehiculo empresa |
| Carnet Manipulador | 4 años | 60 dias | TODOS |
| Reconocimiento Medico | 1 año | 30 dias | TODOS |

#### Flujo de alertas caducidad:

```
SISTEMA comprueba diariamente
         |
         v
+---------------------------+
| Documento proximo a       |
| caducar (segun dias aviso)|
+---------------------------+
         |
         v
+---------------------------+
| ALERTA a Director RRHH    |
| "Documento X de Y caduca  |
|  en Z dias"               |
+---------------------------+
         |
         v
+---------------------------+
| ALERTA al Trabajador      |
| "Tu documento X caduca    |
|  en Z dias, renovar"      |
+---------------------------+
         |
         v
+---------------------------+
| Trabajador renueva y      |
| sube nuevo documento      |
+---------------------------+
         |
         v
+---------------------------+
| Director RRHH valida      |
| Se actualiza fecha        |
| caducidad                 |
+---------------------------+
```

### 16.3 ALERTA 3: Hermi - Datos Completos

Cuando el Director RRHH completa los 4 campos y guarda:

```
Director RRHH completa datos
         |
         v
    ALERTA 3
    Hermi (SS)
    "Datos completos"
```

```
Para: Hermi (Asesor SS)
Asunto: ALTA SS - Manuel Perez - DATOS COMPLETOS

Mensaje:
"Ya puedes tramitar el alta en Seguridad Social.

DATOS DEL TRABAJADOR:
- Nombre: Manuel Perez
- DNI: 12345678X
- Telefono: 654 321 987
- Email: mperez@gmail.com

DATOS DEL CONTRATO:
- Categoria: Oficial 1a
- Horas: 40 h/semana
- Comienzo: 01/03/2026
- Fin: (indefinido)

Por favor, confirmar cuando este tramitada el alta."
```

### 16.4 Flujo Completo de Alertas

```
CONTRATADO
    |
    +---> ALERTA 1: Director RRHH
    |     "Nuevo contratado, completar datos"
    |
    +---> ALERTA 2: Hermi
          "Pendiente alta, esperar datos"
              |
              v
    Director RRHH completa:
    - Categoria
    - Horas
    - Comienzo contrato
    - Fin contrato
              |
              v
         ALERTA 3: Hermi
         "Datos completos, tramitar alta"
              |
              v
         Hermi tramita alta SS
         + completa tipo/codigo contrato
              |
              v
         FLUJO FIRMA CONTRATO
         (ver seccion 17)
```

---

## 17. FIRMA DE CONTRATO

### 17.1 Flujo de Firma

El contrato se firma mediante una **aplicacion web de firma de contratos**.

```
HERMI da de alta al trabajador en SS
         |
         v
+---------------------------+
| ALERTA 4: Director RRHH   |
| "Contrato pendiente de    |
|  firma: Manuel Perez"     |
+---------------------------+
         |
         v
+---------------------------+
| Director RRHH firma       |
| (app web firma contratos) |
| Estado: FIRMADO_EMPRESA   |
+---------------------------+
         |
         v
+---------------------------+
| Se DESBLOQUEA firma       |
| para el trabajador        |
+---------------------------+
         |
         v
+---------------------------+
| ALERTA 5: Trabajador      |
| "Tienes un contrato       |
|  pendiente de firmar"     |
+---------------------------+
         |
         v
+---------------------------+
| Trabajador firma          |
| (app web firma contratos) |
| Estado: FIRMADO_AMBOS     |
+---------------------------+
         |
         v
+---------------------------+
| CONTRATO COMPLETADO       |
| Notifica a Director RRHH  |
| y a Hermi                 |
+---------------------------+
```

### 17.2 Estados del Contrato

| Estado | Descripcion |
|--------|-------------|
| PENDIENTE_ALTA | Esperando alta en SS por Hermi |
| PENDIENTE_FIRMA_EMPRESA | Alta realizada, pendiente firma Director RRHH |
| FIRMADO_EMPRESA | Director RRHH ha firmado, pendiente trabajador |
| FIRMADO_AMBOS | Contrato completado |

### 17.3 Alertas de Firma

#### ALERTA 4: Director RRHH - Firma pendiente
```
Para: Director RRHH
Asunto: Contrato pendiente de firma - Manuel Perez

Mensaje:
"El trabajador Manuel Perez ya esta dado de alta en SS.
Tienes pendiente firmar su contrato.

[Firmar contrato]"
```

#### ALERTA 5: Trabajador - Firma desbloqueada
```
Para: Manuel Perez (trabajador)
Asunto: Tu contrato esta listo para firmar

Mensaje:
"Tu contrato de trabajo esta listo para que lo firmes.
Accede al portal para revisar y firmar el contrato.

[Acceder al portal]"
```

#### ALERTA 6: Confirmacion firma completada
```
Para: Director RRHH, Hermi
Asunto: Contrato firmado - Manuel Perez

Mensaje:
"El contrato de Manuel Perez ha sido firmado
por ambas partes.

Fecha firma empresa: 28/02/2026
Fecha firma trabajador: 01/03/2026
Estado: COMPLETADO"
```

### 17.4 Aplicacion Web Firma Contratos

| Caracteristica | Descripcion |
|----------------|-------------|
| Acceso | Via navegador web |
| Usuarios | Director RRHH, Trabajadores |
| Funciones | Ver contrato, Firmar digitalmente |
| Notificaciones | Email, Dashboard |
| Bloqueo | Trabajador no puede firmar hasta que firme Director RRHH |

---

## 18. OTRAS FIRMAS Y DOCUMENTOS DEL TRABAJADOR

### 18.1 Documentos Independientes del Contrato

El trabajador firma estos documentos **sin necesidad de haber firmado el contrato**. Son independientes y se pueden firmar en cualquier momento desde el Portal Empleado.

| # | Documento | Tipo |
|---|-----------|------|
| 1 | Proteccion de Datos | Firma |
| 2 | Usos de Imagenes | Firma |
| 3 | Formacion | Firma |
| 4 | EPI (Equipos Proteccion Individual) | Firma |
| 5 | Informacion | Firma |
| 6 | Politica | Firma |
| 7 | Confidencialidad | Firma |
| 8 | Banco | Firma |
| 9 | Material | Firma |
| 10 | Protocolo Acoso | Firma |

### 18.2 Portal Empleado - Mis Documentos

```
PORTAL EMPLEADO - Manuel Perez
+============================================================================+
|  MIS DOCUMENTOS                                                            |
+============================================================================+
|                                                                             |
|  CONTRATO DE TRABAJO                                                        |
|  +------------------------------------------+--------+------------------+   |
|  | Contrato de trabajo                      | [!]    | Bloqueado        |   |
|  +------------------------------------------+--------+------------------+   |
|                                                                             |
|  DOCUMENTOS A FIRMAR (independientes)                                       |
|  +------------------------------------------+--------+------------------+   |
|  | Proteccion de Datos                      | [!]    | [Firmar]         |   |
|  | Usos de Imagenes                         | [!]    | [Firmar]         |   |
|  | Formacion                                | [!]    | [Firmar]         |   |
|  | EPI                                      | [!]    | [Firmar]         |   |
|  | Informacion                              | [!]    | [Firmar]         |   |
|  | Politica                                 | [!]    | [Firmar]         |   |
|  | Confidencialidad                         | [!]    | [Firmar]         |   |
|  | Banco                                    | [!]    | [Firmar]         |   |
|  | Material                                 | [!]    | [Firmar]         |   |
|  | Protocolo Acoso                          | [!]    | [Firmar]         |   |
|  +------------------------------------------+--------+------------------+   |
|                                                                             |
|  DATOS A COMPLETAR                                                          |
|  +------------------------------------------+--------+------------------+   |
|  | DNI/NIE                                  | [!]    | [Subir]          |   |
|  | Cuenta bancaria                          | [!]    | [Introducir]     |   |
|  | NAF                                      | [!]    | [Introducir]     |   |
|  | Direccion, CP, Municipio                 | [!]    | [Completar]      |   |
|  | Telefono, Email                          | [ok]   | Verificado       |   |
|  | Fecha nacimiento                         | [!]    | [Introducir]     |   |
|  | Carnet C (opcional)                      | [ ]    | [Subir]          |   |
|  | CAP (opcional)                           | [ ]    | [Subir]          |   |
|  | Carnet carretillero                      | [!]    | [Subir] *        |   |
|  +------------------------------------------+--------+------------------+   |
|  * Obligatorio si perfil = LOGISTICA                                       |
|                                                                             |
+============================================================================+
```

### 18.3 Flujo de Firmas Independientes

```
TRABAJADOR accede a Portal Empleado
         |
         v
+---------------------------+
| Ve lista de documentos    |
| pendientes de firmar      |
+---------------------------+
         |
         v
+---------------------------+
| Puede firmar en cualquier |
| orden, sin esperar        |
| el contrato               |
+---------------------------+
         |
         v
+---------------------------+
| Al firmar cada documento  |
| se marca como [ok]        |
+---------------------------+
         |
         v
+---------------------------+
| Cuando TODOS firmados     |
| → Notifica a Director RRHH|
+---------------------------+
```

### 18.4 Estados de Documentos

| Icono | Estado | Descripcion |
|-------|--------|-------------|
| [!] | Pendiente | Documento pendiente de firmar/subir |
| [~] | En proceso | Subido, pendiente validacion |
| [ok] | Completado | Firmado/validado |
| [ ] | Opcional | No obligatorio para este perfil |

### 16.5 Tabla: notificaciones_contratacion

```sql
CREATE TABLE IF NOT EXISTS notificaciones_contratacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidato_id BIGINT UNSIGNED NOT NULL,
    operador_id INT NOT NULL,
    tipo_notificacion ENUM('EMAIL', 'SMS', 'LLAMADA') NOT NULL,
    destinatario_rol ENUM('DIRECTOR_RRHH', 'RESPONSABLE_SS', 'PREVENCION') NOT NULL,
    destinatario_email VARCHAR(255),
    destinatario_telefono VARCHAR(20),
    asunto VARCHAR(255),
    mensaje TEXT,
    estado ENUM('PENDIENTE', 'ENVIADA', 'ERROR') DEFAULT 'PENDIENTE',
    fecha_envio DATETIME,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (candidato_id) REFERENCES candidatos(id),
    FOREIGN KEY (operador_id) REFERENCES operadores(id)
);
```

### 16.3 Configuracion de Alertas

```sql
CREATE TABLE IF NOT EXISTS config_alertas_rrhh (
    id INT AUTO_INCREMENT PRIMARY KEY,
    evento ENUM('CONTRATADO', 'DOCUMENTO_CADUCA', 'DATOS_PENDIENTES') NOT NULL,
    rol_destino ENUM('DIRECTOR_RRHH', 'RESPONSABLE_SS', 'PREVENCION') NOT NULL,
    tipo_notificacion ENUM('EMAIL', 'SMS', 'LLAMADA') NOT NULL,
    activo TINYINT(1) DEFAULT 1,
    email_destino VARCHAR(255),
    telefono_destino VARCHAR(20),
    dias_antelacion INT DEFAULT 0 COMMENT 'Para alertas de caducidad',
    plantilla_asunto VARCHAR(255),
    plantilla_mensaje TEXT,
    idEmpresa CHAR(3),

    INDEX idx_evento (evento),
    INDEX idx_rol (rol_destino)
);
```

### 16.4 Alertas de Documentos por Caducar

```sql
-- Vista para documentos proximos a caducar
CREATE OR REPLACE VIEW v_documentos_por_caducar AS
SELECT
    dt.iddocumento,
    dt.nombre AS documento,
    dt.dias_aviso,
    dtr.idtrabajador,
    o.Nombre,
    o.Apellido1,
    dtr.fecha_caducidad,
    DATEDIFF(dtr.fecha_caducidad, CURDATE()) AS dias_restantes
FROM documentacion_trabajadores dt
JOIN documentacion_trabajadores_registro dtr ON dt.iddocumento = dtr.iddocumento
JOIN operadores o ON dtr.idtrabajador = o.id
WHERE dt.borrado = 0
AND dtr.borrado = 0
AND dtr.fecha_caducidad IS NOT NULL
AND DATEDIFF(dtr.fecha_caducidad, CURDATE()) <= dt.dias_aviso
AND DATEDIFF(dtr.fecha_caducidad, CURDATE()) >= 0
ORDER BY dias_restantes ASC;
```

### 16.5 Dashboard Alertas Director RRHH

```
+============================================================================+
|  ALERTAS - Director RRHH                                     Hoy: 18/02/26 |
+============================================================================+

+------------------------------------------+
|  [!] URGENTE - NUEVOS CONTRATADOS        |
+------------------------------------------+
|  Manuel Perez                             |
|  Fecha inicio: 01/03/2026 (11 dias)       |
|  Pendiente: Contrato, Datos, Alta SS      |
|  [Ver detalle]                            |
+------------------------------------------+

+------------------------------------------+
|  [!] DOCUMENTOS POR CADUCAR              |
+------------------------------------------+
|  Juan Lopez - Reconoc. medico            |
|  Caduca: 15/03/2026 (25 dias)            |
|  [Programar renovacion]                   |
|                                           |
|  Ana Garcia - CAP Curso                   |
|  Caduca: 20/03/2026 (30 dias)            |
|  [Programar renovacion]                   |
+------------------------------------------+

+------------------------------------------+
|  [ ] DATOS PENDIENTES EMPLEADOS          |
+------------------------------------------+
|  Carmen Rodriguez - 3 documentos          |
|  Cuenta bancaria, DNI, Carnet             |
|  [Enviar recordatorio]                    |
+------------------------------------------+
```

### 16.6 Procedimiento: Enviar Notificacion Contratacion

```sql
CREATE PROCEDURE IF NOT EXISTS sp_notificar_contratacion(
    IN p_candidato_id BIGINT UNSIGNED,
    IN p_operador_id INT
)
BEGIN
    DECLARE v_nombre VARCHAR(100);
    DECLARE v_perfil VARCHAR(50);
    DECLARE v_fecha_inicio DATE;
    DECLARE v_dni VARCHAR(20);

    -- Obtener datos del candidato
    SELECT
        CONCAT(nombre, ' ', apellido1),
        perfil_codigo
    INTO v_nombre, v_perfil
    FROM candidatos
    WHERE id = p_candidato_id;

    -- Obtener fecha inicio del contrato
    SELECT fecha_desde, Nif
    INTO v_fecha_inicio, v_dni
    FROM operadores
    WHERE id = p_operador_id;

    -- Insertar notificacion para Director RRHH
    INSERT INTO notificaciones_contratacion (
        candidato_id, operador_id, tipo_notificacion,
        destinatario_rol, asunto, mensaje, estado
    )
    SELECT
        p_candidato_id, p_operador_id, tipo_notificacion,
        'DIRECTOR_RRHH',
        CONCAT('Nuevo contratado: ', v_nombre),
        CONCAT('Se ha contratado a ', v_nombre, '\n',
               'Perfil: ', v_perfil, '\n',
               'Fecha inicio: ', v_fecha_inicio),
        'PENDIENTE'
    FROM config_alertas_rrhh
    WHERE evento = 'CONTRATADO'
    AND rol_destino = 'DIRECTOR_RRHH'
    AND activo = 1;

    -- Insertar notificacion para Responsable SS
    INSERT INTO notificaciones_contratacion (
        candidato_id, operador_id, tipo_notificacion,
        destinatario_rol, asunto, mensaje, estado
    )
    SELECT
        p_candidato_id, p_operador_id, tipo_notificacion,
        'RESPONSABLE_SS',
        CONCAT('Alta pendiente SS: ', v_nombre),
        CONCAT('Tramitar alta en Seguridad Social:\n',
               'Nombre: ', v_nombre, '\n',
               'DNI: ', v_dni, '\n',
               'Fecha inicio: ', v_fecha_inicio),
        'PENDIENTE'
    FROM config_alertas_rrhh
    WHERE evento = 'CONTRATADO'
    AND rol_destino = 'RESPONSABLE_SS'
    AND activo = 1;

END;
```

### 16.7 Trigger: Auto-notificar al Contratar

```sql
CREATE TRIGGER IF NOT EXISTS tr_notificar_contratacion
AFTER INSERT ON candidato_operador
FOR EACH ROW
BEGIN
    CALL sp_notificar_contratacion(NEW.candidato_id, NEW.operador_id);
END;
```

---

## 17. Tablas SQL Completas

### 17.1 Tabla: documentacion_trabajadores_requerida

```sql
-- Vista para ver documentos pendientes de un trabajador
CREATE OR REPLACE VIEW v_documentos_pendientes_trabajador AS
SELECT
    o.id AS trabajador_id,
    CONCAT(o.Nombre, ' ', o.Apellido1) AS trabajador,
    dt.iddocumento,
    dt.codigo,
    dt.nombre AS documento,
    dt.grupo,
    CASE
        WHEN dtr.idregistro IS NULL THEN 'PENDIENTE'
        WHEN dtr.fecha_caducidad < CURDATE() THEN 'CADUCADO'
        ELSE 'OK'
    END AS estado,
    dtr.fecha_caducidad
FROM operadores o
CROSS JOIN documentacion_trabajadores dt
LEFT JOIN documentacion_trabajadores_registro dtr
    ON o.id = dtr.idtrabajador
    AND dt.iddocumento = dtr.iddocumento
    AND dtr.borrado = 0
WHERE o.activo = 1
AND o.borrado = 0
AND dt.borrado = 0
ORDER BY o.id, dt.grupo, dt.orden;
```

### 17.2 Tabla: portal_candidato

```sql
CREATE TABLE IF NOT EXISTS portal_candidato (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidato_id BIGINT UNSIGNED NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    token_registro VARCHAR(100),
    fecha_registro DATETIME,
    ultimo_acceso DATETIME,
    activo TINYINT(1) DEFAULT 1,

    -- Datos personales completados por el candidato
    nombre VARCHAR(100),
    apellido1 VARCHAR(100),
    apellido2 VARCHAR(100),
    dni VARCHAR(20),
    fecha_nacimiento DATE,
    direccion VARCHAR(255),
    codigo_postal VARCHAR(10),
    localidad VARCHAR(100),
    provincia VARCHAR(100),
    telefono VARCHAR(20),
    cuenta_bancaria VARCHAR(34) COMMENT 'IBAN',
    datos_completos TINYINT(1) DEFAULT 0,
    fecha_datos_completos DATETIME,

    -- Gaming codigos
    codigos_practicados INT DEFAULT 0,
    aciertos_totales INT DEFAULT 0,
    porcentaje_aciertos DECIMAL(5,2) DEFAULT 0,

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY uk_candidato (candidato_id),
    UNIQUE KEY uk_email (email),
    FOREIGN KEY (candidato_id) REFERENCES candidatos(id)
);
```

### 17.3 Procedimiento: Transferir Datos a Operador

```sql
CREATE PROCEDURE IF NOT EXISTS sp_transferir_portal_a_operador(
    IN p_candidato_id BIGINT UNSIGNED,
    OUT p_operador_id INT
)
BEGIN
    DECLARE v_existe INT DEFAULT 0;

    -- Verificar que el candidato tiene datos completos en portal
    SELECT COUNT(*) INTO v_existe
    FROM portal_candidato
    WHERE candidato_id = p_candidato_id
    AND datos_completos = 1;

    IF v_existe = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El candidato no tiene datos completos en el portal';
    END IF;

    -- Crear operador con datos del portal
    INSERT INTO operadores (
        Nombre, Apellido1, Apellido2, Nif,
        Poblacion, Provincia, Cp, telefono, email,
        activo, borrado, created_at
    )
    SELECT
        pc.nombre, pc.apellido1, pc.apellido2, pc.dni,
        pc.localidad, pc.provincia, pc.codigo_postal,
        pc.telefono, pc.email,
        1, 0, NOW()
    FROM portal_candidato pc
    WHERE pc.candidato_id = p_candidato_id;

    SET p_operador_id = LAST_INSERT_ID();

    -- Actualizar cuenta bancaria en operador
    UPDATE operadores o
    JOIN portal_candidato pc ON pc.candidato_id = p_candidato_id
    SET o.cuenta_bancaria = pc.cuenta_bancaria
    WHERE o.id = p_operador_id;

END;
```

---

---

## 19. ALERTAS VENCIMIENTO DE CONTRATOS

### 19.1 Sistema de Alertas por Vencimiento

Cuando un contrato temporal esta proximo a vencer, se genera un sistema de alertas automaticas.

**Ejemplo**:
- Trabajador: Manuel Manuel
- Contrato: 3 meses
- Categoria: T0
- Horas: 40 h/semana
- Fecha fin: 28/02/2026

### 19.2 Flujo de Alertas Vencimiento

```
CONTRATO TEMPORAL
Fecha fin: 28/02/2026
         |
         v
15 DIAS ANTES (13/02/2026)
         |
    +----+----+
    |         |
    v         v
DASHBOARD   ALERTA EMAIL
Director    Hermi
RRHH
         |
         v
"Manuel Manuel expira el
 contrato el dia 28/02/2026"
         |
         v
+---------------------------+
| ALERTAS RECURRENTES       |
| Cada 2 dias a Hermi       |
| hasta que se resuelva     |
+---------------------------+
         |
    13/02 - Email 1
    15/02 - Email 2
    17/02 - Email 3
    19/02 - Email 4
    21/02 - Email 5
    23/02 - Email 6
    25/02 - Email 7
    27/02 - Email 8 (ultimo)
         |
         v
+---------------------------+
| SI nuevo contrato firmado |
| → Se detienen alertas     |
| → Se marca como RESUELTO  |
+---------------------------+
```

### 19.3 Dashboards que muestran Vencimientos

| Dashboard | Rol | Muestra |
|-----------|-----|---------|
| Director RRHH | DIRECTOR_RRHH | Contratos proximos a vencer |
| Hermi | HERMI_SS | Contratos pendientes renovar |
| (Configurable) | Otros roles | Segun configuracion |

### 19.4 Vista Dashboard Vencimientos

```
+============================================================================+
|  CONTRATOS PROXIMOS A VENCER - Director RRHH                               |
+============================================================================+
|                                                                             |
|  [!] VENCEN EN MENOS DE 15 DIAS                                            |
|  +------------------------------------------+------------+--------+------+ |
|  | Trabajador        | Tipo    | Fin        | Dias      | Estado | Accion| |
|  +------------------------------------------+------------+--------+------+ |
|  | Manuel Manuel     | 3 meses | 28/02/2026 | 10 dias   | [!]    | [Renovar]|
|  | Carmen Garcia     | 6 meses | 05/03/2026 | 15 dias   | [!]    | [Renovar]|
|  +------------------------------------------+------------+--------+------+ |
|                                                                             |
|  [ ] VENCEN EN 15-30 DIAS                                                  |
|  +------------------------------------------+------------+--------+------+ |
|  | Pedro Lopez       | 1 año   | 20/03/2026 | 30 dias   | [ ]    | [Ver]  |
|  +------------------------------------------+------------+--------+------+ |
|                                                                             |
+============================================================================+
```

### 19.5 Alertas Email a Hermi

**Frecuencia**: Cada 2 dias durante los ultimos 15 dias

**Email ejemplo (dia 13/02)**:
```
Para: Hermi (Asesor SS)
Asunto: [URGENTE] Contrato expira - Manuel Manuel - 28/02/2026

Mensaje:
"El contrato de Manuel Manuel expira el 28/02/2026.
Quedan 15 dias para la finalizacion.

DATOS DEL TRABAJADOR:
- Nombre: Manuel Manuel
- Categoria: T0
- Horas: 40 h/semana
- Tipo contrato: Temporal 3 meses
- Fecha inicio: 01/12/2025
- Fecha fin: 28/02/2026

ACCIONES PENDIENTES:
[ ] Decidir renovacion o finalizacion
[ ] Si renovacion: preparar nuevo contrato
[ ] Si finalizacion: preparar baja SS

Este email se enviara cada 2 dias hasta que se resuelva.

[Acceder al sistema]"
```

**Email ejemplo (dia 27/02 - ultimo)**:
```
Para: Hermi (Asesor SS)
Asunto: [MUY URGENTE] Contrato expira MAÑANA - Manuel Manuel - 28/02/2026

Mensaje:
"ATENCION: El contrato de Manuel Manuel expira MAÑANA 28/02/2026.
Queda 1 dia para la finalizacion.

Si no se ha tomado una decision, el contrato finalizara automaticamente.

[Acceder al sistema]"
```

### 19.6 Estados del Contrato por Vencer

| Estado | Descripcion |
|--------|-------------|
| ACTIVO | Contrato vigente, sin alertas |
| PROXIMO_VENCER | Menos de 15 dias, alertas activas |
| PENDIENTE_DECISION | Alerta enviada, esperando accion |
| RENOVADO | Nuevo contrato firmado, alertas detenidas |
| FINALIZADO | Contrato terminado, baja SS tramitada |
| NO_RENOVADO | Decision de no renovar, baja SS pendiente |

### 19.7 Acciones Posibles

| Accion | Descripcion | Resultado |
|--------|-------------|-----------|
| **Renovar** | Crear nuevo contrato | Nuevo flujo de firma, alertas detenidas |
| **Finalizar** | No renovar contrato | Tramitar baja SS, alertas detenidas |
| **Modificar** | Cambiar condiciones | Nuevo contrato con cambios |

### 19.8 Condiciones que generan Alertas

Si se modifican estas condiciones en el contrato activo:

| Condicion | Alerta |
|-----------|--------|
| Fecha fin proxima (< 15 dias) | Alerta vencimiento |
| Cambio de categoria | Alerta modificacion |
| Cambio de horas | Alerta modificacion |
| Cambio de tipo contrato | Alerta modificacion |

---

## 20. CONFIGURACION ALERTAS POR ROL

### 20.1 Tabla Configuracion Alertas

| Rol | Tipo Alerta | Canal | Frecuencia |
|-----|-------------|-------|------------|
| DIRECTOR_RRHH | Vencimiento contrato | Dashboard | Tiempo real |
| DIRECTOR_RRHH | Nuevo contratado | Dashboard + Email | Inmediata |
| HERMI_SS | Vencimiento contrato | Email | Cada 2 dias |
| HERMI_SS | Pendiente alta | Email | Inmediata |
| HERMI_SS | Datos completos | Email | Inmediata |
| TRABAJADOR | Firma contrato | Email | Inmediata |
| TRABAJADOR | Documentos pendientes | Email | Semanal |

### 20.2 Canales de Notificacion

| Canal | Descripcion |
|-------|-------------|
| Dashboard | Aparece en el panel del usuario |
| Email | Correo electronico |
| SMS | Mensaje de texto (opcional) |
| Llamada | Llamada telefonica (opcional) |

---

---

## 21. MODIFICACION DE CONDICIONES DEL CONTRATO

### 21.1 Condiciones que generan nuevo contrato/anexo

Si un trabajador sufre una modificacion de alguna de estas condiciones, se genera **una nueva linea en los contratos del trabajador**:

| Condicion | Genera nuevo contrato |
|-----------|----------------------|
| Cambio de categoria | SI |
| Cambio de jornada (horas) | SI |

**Nota**: Basta con que se modifique UNA de estas condiciones para generar el nuevo contrato.

### 21.2 Flujo Modificacion de Condiciones

```
TRABAJADOR CON CONTRATO ACTIVO
(3 meses, indefinido, etc.)
         |
         v
+---------------------------+
| Se modifica condicion:    |
| - Cambio categoria        |
| - Cambio jornada          |
+---------------------------+
         |
         v
+---------------------------+
| Se genera NUEVA LINEA     |
| en contratos del trabajador|
| (Anexo/Novacion)          |
+---------------------------+
         |
         v
+---------------------------+
| HERMI sube el documento   |
| del nuevo contrato/anexo  |
+---------------------------+
         |
         v
+---------------------------+
| ALERTA: Director RRHH     |
| "Nuevo anexo pendiente    |
|  de firma: Manuel Manuel" |
+---------------------------+
         |
         v
+---------------------------+
| Director RRHH FIRMA       |
| (primero)                 |
+---------------------------+
         |
         v
+---------------------------+
| Se DESBLOQUEA para        |
| el trabajador             |
+---------------------------+
         |
         v
+---------------------------+
| ALERTA: Trabajador        |
| "Tienes un anexo/contrato |
|  pendiente de firmar"     |
+---------------------------+
         |
         v
+---------------------------+
| Trabajador FIRMA          |
| (segundo)                 |
+---------------------------+
         |
         v
+---------------------------+
| ANEXO COMPLETADO          |
| Nueva linea activa        |
| Anterior linea cerrada    |
+---------------------------+
```

### 21.3 Historial de Contratos del Trabajador

Cada modificacion genera una nueva linea, manteniendo el historial completo:

```
+============================================================================+
|  CONTRATOS - Manuel Manuel (ID: 248)                                       |
+============================================================================+
|                                                                             |
|  # | Tipo        | Categoria | Horas | Desde      | Hasta      | Estado    |
|  --|-------------|-----------|-------|------------|------------|-----------|
|  1 | Temporal    | T0        | 40    | 01/12/2025 | 28/02/2026 | CERRADO   |
|  2 | Indefinido  | T1        | 40    | 01/03/2026 | -          | CERRADO   |
|  3 | Indefinido  | T1        | 35    | 15/04/2026 | -          | ACTIVO    |
|                                                                             |
|  Cambios realizados:                                                        |
|  - 01/03/2026: Paso de temporal a indefinido, cambio categoria T0 → T1     |
|  - 15/04/2026: Reduccion de jornada 40h → 35h                              |
|                                                                             |
+============================================================================+
```

### 21.4 Ejemplo Practico

**Situacion inicial**:
- Trabajador: Manuel Manuel
- Contrato: Temporal 3 meses
- Categoria: T0
- Jornada: 40 horas

**Modificacion**: Cambio de jornada a 35 horas

```
1. Director RRHH modifica jornada en el sistema
   40h → 35h
         |
         v
2. Sistema genera nueva linea de contrato
   Contrato #2: Categoria T0, 35h
         |
         v
3. ALERTA a Hermi
   "Modificacion de condiciones - Manuel Manuel
    Cambio de jornada: 40h → 35h
    Subir documento del anexo"
         |
         v
4. Hermi sube documento anexo
         |
         v
5. ALERTA a Director RRHH
   "Anexo pendiente de firma - Manuel Manuel"
         |
         v
6. Director RRHH firma
         |
         v
7. ALERTA a Trabajador
   "Tienes un anexo pendiente de firmar"
         |
         v
8. Trabajador firma
         |
         v
9. COMPLETADO
   - Contrato #1: CERRADO (40h)
   - Contrato #2: ACTIVO (35h)
```

### 21.5 Tipos de Documentos por Modificacion

| Modificacion | Documento |
|--------------|-----------|
| Cambio categoria | Anexo de novacion |
| Cambio jornada | Anexo de modificacion de jornada |
| Ambos | Anexo de novacion con modificacion de jornada |

### 21.6 Alertas de Modificacion

#### ALERTA a Hermi (subir documento)
```
Para: Hermi (Asesor SS)
Asunto: Modificacion condiciones - Manuel Manuel

Mensaje:
"Se ha modificado las condiciones del contrato de Manuel Manuel.

CAMBIOS:
- Jornada: 40h → 35h

ACCIONES:
[ ] Preparar anexo de modificacion
[ ] Subir documento al sistema

[Acceder al sistema]"
```

#### ALERTA a Director RRHH (firmar)
```
Para: Director RRHH
Asunto: Anexo pendiente de firma - Manuel Manuel

Mensaje:
"Hermi ha subido el anexo de modificacion de Manuel Manuel.
Tienes pendiente firmar el documento.

CAMBIOS:
- Jornada: 40h → 35h

[Firmar anexo]"
```

#### ALERTA a Trabajador (firmar)
```
Para: Manuel Manuel
Asunto: Tienes un anexo pendiente de firmar

Mensaje:
"Hola Manuel,

Se han modificado las condiciones de tu contrato.
Accede al portal para revisar y firmar el anexo.

CAMBIOS:
- Jornada: 40h → 35h

[Acceder al portal]"
```

---

## 22. HISTORIAL DE CONTRATOS - FORMATO VISUAL FINAL

### 22.1 Estructura de Columnas

| Columna | Descripcion | Tipo BD |
|---------|-------------|---------|
| # | Numero de linea secuencial | INT |
| Contrato Desde | Fecha inicio del contrato original | DATE |
| Contrato Hasta | Fecha fin del contrato (- si indefinido) | DATE NULL |
| Cat | Categoria profesional (T0, T1, etc.) | VARCHAR |
| Horas | Horas semanales | INT |
| Codigo | Codigo de contrato | VARCHAR |
| Tipo | Tipo de contrato (Temporal 3m, Indefinido, etc.) | VARCHAR |
| Sustit | Si es sustitucion (SI/NO) | TINYINT |
| Validez Desde | Fecha desde que aplica esta linea | DATE |
| Validez Hasta | Fecha hasta que aplica esta linea | DATE NULL |
| Acciones | Estado de firmas | VARCHAR |

### 22.2 Formato Visual Historial

```
┌─────┬────────────────┬────────────────┬─────┬───────┬────────┬─────────────┬────────┬───────────────┬───────────────┬────────────┐
│  #  │ Contrato Desde │ Contrato Hasta │ Cat │ Horas │ Codigo │    Tipo     │ Sustit │ Validez Desde │ Validez Hasta │  Acciones  │
├─────┼────────────────┼────────────────┼─────┼───────┼────────┼─────────────┼────────┼───────────────┼───────────────┼────────────┤
│ 1   │ 01/12/2025     │ 28/02/2026     │ T0  │ 40    │ 100    │ Temporal 3m │ NO     │ 01/12/2025    │ 02/02/2026    │ ✓H ✓Dir ✓T │
├─────┼────────────────┼────────────────┼─────┼───────┼────────┼─────────────┼────────┼───────────────┼───────────────┼────────────┤
│ 2   │ 01/12/2025     │ 28/02/2026     │ T1  │ 40    │ 100    │ Temporal 3m │ NO     │ 03/02/2026    │ 09/02/2026    │ ✓H ✓Dir ✓T │
├─────┼────────────────┼────────────────┼─────┼───────┼────────┼─────────────┼────────┼───────────────┼───────────────┼────────────┤
│ 3   │ 01/12/2025     │ 28/02/2026     │ T1  │ 20    │ 100    │ Temporal 3m │ NO     │ 10/02/2026    │ 28/02/2026    │ ✓H ✓Dir ✓T │
├─────┼────────────────┼────────────────┼─────┼───────┼────────┼─────────────┼────────┼───────────────┼───────────────┼────────────┤
│ 4   │ 01/03/2026     │ -              │ T1  │ 20    │ 200    │ Indefinido  │ NO     │ 01/03/2026    │ 14/03/2026    │ ✓H ✓Dir ✓T │
├─────┼────────────────┼────────────────┼─────┼───────┼────────┼─────────────┼────────┼───────────────┼───────────────┼────────────┤
│ 5   │ 01/03/2026     │ -              │ T1  │ 40    │ 200    │ Indefinido  │ NO     │ 15/03/2026    │ -             │ □H □Dir □T │
└─────┴────────────────┴────────────────┴─────┴───────┴────────┴─────────────┴────────┴───────────────┴───────────────┴────────────┘
```

### 22.3 Explicacion del Ejemplo

| Linea | Descripcion del cambio |
|-------|------------------------|
| 1 | Contrato original: Temporal 3 meses, categoria T0, 40 horas |
| 2 | Cambio de categoria: T0 → T1 (validez desde 03/02/2026) |
| 3 | Cambio de horas: 40h → 20h (validez desde 10/02/2026) |
| 4 | Transformacion a Indefinido: nuevo contrato desde 01/03/2026 |
| 5 | Cambio de horas: 20h → 40h (pendiente de firmas) |

### 22.4 Estados de Acciones

| Icono | Significado |
|-------|-------------|
| ✓H | Hermi ha subido el documento |
| ✓Dir | Director RRHH ha firmado |
| ✓T | Trabajador ha firmado |
| □H | Pendiente subir documento (Hermi) |
| □Dir | Pendiente firma Director RRHH |
| □T | Pendiente firma Trabajador |

### 22.5 Diferencia entre Contrato y Validez

| Campo | Descripcion |
|-------|-------------|
| **Contrato Desde/Hasta** | Fechas del contrato "padre" (el original firmado) |
| **Validez Desde/Hasta** | Fechas en que aplican las condiciones de ESA linea |

**Ejemplo**:
- Un trabajador firma un contrato temporal de 3 meses (01/12/2025 - 28/02/2026)
- Si le cambian la categoria el 03/02/2026, se crea una nueva linea
- El "Contrato" sigue siendo el mismo (01/12/2025 - 28/02/2026)
- Pero la "Validez" de la linea 1 termina el 02/02/2026
- Y la "Validez" de la linea 2 empieza el 03/02/2026

### 22.6 Cuando cambia "Contrato Desde/Hasta"

Solo cambia cuando hay un **nuevo contrato** (no modificacion):
- Transformacion de temporal a indefinido
- Finalizacion y nuevo contrato
- Renovacion con nuevas fechas

---

*Documento generado: 2026-02-17*
*Ultima actualizacion: 2026-02-18*

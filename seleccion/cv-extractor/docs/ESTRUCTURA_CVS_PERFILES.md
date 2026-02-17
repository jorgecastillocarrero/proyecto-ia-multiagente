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

```
LLAMADOR                              SELECTOR (Perfiles)
+--------------------+
| Entrevista: [Duda] |
| Comentario: [____] |
+--------------------+
         |
         v
+--------------------+                +----------------------+
| Vuelve a PERFILES  | -------------> | Ve candidato + DUDA  |
| con marca DUDA     |                | Comentario llamador  |
+--------------------+                +----------------------+
                                               |
                                      +--------+--------+
                                      |                 |
                                     SI                NO
                                      |                 |
                                      v                 v
                              +----------------+  +------------------+
                              | Abre campo     |  | DESCARTADO       |
                              | comentario     |  | (automatico)     |
                              | para responder |  +------------------+
                              +----------------+
                                      |
                                      v
+--------------------+        +----------------+
| Vuelve a LLAMADAS  | <----- | Respuesta del  |
| con respuesta      |        | selector       |
+--------------------+        +----------------+
         |
         v
+--------------------+
| Llamador vuelve a  |
| llamar con la info |
+--------------------+
```

### 8.7 Roles en Segunda Fase

| Rol | Tabla | Condicion | Funcion |
|-----|-------|-----------|---------|
| Llamador | rrhh_flujo_trabajadores | nivel=4, activo=1, en cuadrante | Llama y concierta cita |
| Entrevistador | rrhh_flujo_trabajadores | (por definir) | Realiza la entrevista |

**Nota**: El llamador y el entrevistador pueden ser personas diferentes.

---

*Documento generado: 2026-02-17*

# MODULO RRHH - SELECCION

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

### 5.3 Pantalla del Juego - Practica por Familias

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
|  Aciertos familia: 45/53 (85%)             |
|                                            |
+============================================+
```

### 5.4 Progreso y Prueba Final

#### Requisitos para Prueba Final

| Requisito | Valor |
|-----------|-------|
| Progreso minimo por familia | 90% de aciertos |
| Condicion para activar prueba | TODAS las familias en verde (>= 90%) |

#### Prueba Final

| Elemento | Valor |
|----------|-------|
| Numero de preguntas | 10 codigos aleatorios |
| Minimo para aprobar | 7 aciertos (70%) |
| Resultado APROBADO | Estado = "Codigos Completado" |
| Resultado SUSPENDIDO | Vuelve a practicar |

#### Flujo del Sistema Gaming

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
 Seguir   PRUEBA FINAL (10 codigos)
practicar    |
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
  Pendiente llamar 2a Entrevista
```

#### Estados en Pantalla CODIGOS (ERP)

| Estado | Significado |
|--------|-------------|
| En Progreso | Practicando familias |
| Prueba Disponible | Todas familias >= 90% |
| Codigos Completado | Aprobo prueba, pendiente decision |

#### Alerta Automatica - Codigos Completado

**Trigger:** Candidato aprueba examen (>= 7/10)

**Destinatarios:** Entrevistador, Director RRHH

**Mensaje:**
```
Manuel Perez se sabe los codigos
```

#### Accion Post-Examen

Cuando aprueba, se desbloquea accion Si/No:

| Candidato | Estado | Accion | Nota |
|-----------|--------|--------|------|
| Manuel Perez | Codigos Completado | [ Si / No ] | queda martes 12/02 a las 10:30 |

| Opcion | Resultado |
|--------|-----------|
| SI | Llamar para 2a Entrevista/Contratacion |
| NO | Va a DESCARTADOS |

#### Flujo Post-Examen

```
APRUEBA EXAMEN (>= 7/10)
         |
         +---> ALERTA: "Manuel Perez se sabe los codigos"
         |
         v
PANTALLA CODIGOS: Accion [ Si / No ]
         |
         v (Si + Nota)
MENU: Segunda Entrevista / Contratacion
```

### 5.5 Pantalla ERP - Lista de Candidatos en Codigos

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

### 5.6 Desplegable: Estado

| Opcion | Resultado |
|--------|-----------|
| EN PROGRESO | Se queda en CODIGOS |
| LLAMAR | Aparece en Dashboard Llamador para llamar y decidir 2a entrevista |

### 5.7 Cuando Estado = Llamar

| Campo | Editable | Descripcion |
|-------|----------|-------------|
| **Resultado** | Si | Desplegable: Si (pasa a 2a entrevista) / No (descartado) |

### 5.8 Vista Ejemplo

| Candidato | Perfil | Fecha 1a | Notas Entrevista | Codigos | Aciertos | Comentario | Estado |
|-----------|--------|----------|------------------|---------|----------|------------|--------|
| Manuel Perez | PESCADERIA | 10/02/2026 | Muy motivado | 120/120 | 88% | Intenta quedar miercoles 12:30 | Llamar |
| Adela Ruano | PESCADERIA | 15/02/2026 | Experiencia 20 años | 45/120 | 90% | | En Progreso |

### 5.9 Fuente de Datos - Servidor ERP

**Servidor:** gestion.pescadoslacarihuela.es

#### Tablas del Servidor

| Tabla | Uso | Campos Clave |
|-------|-----|--------------|
| `articulos` | Productos | codigo, nombre, familia_id |
| `familias` | Familias de productos | id, nombre |
| `v2_facturas_tickets_lineas` | Ventas | IdArticulo, created_at |

#### Familias de Productos

| ID | Familia |
|----|---------|
| 13 | CHICO ENTERO |
| 14 | CHICO LIMPIO |
| 18 | MARISCO CRUDO |
| 19 | MARISCO COCIDO |
| 21 | CEFALOPODO |
| 29 | MERLUZA |
| 31 | PLANOS |
| 32 | RAPE |

#### Ejemplos de Articulos

| Codigo | Nombre | Familia |
|--------|--------|---------|
| 1 | ACEDIAS | CHICO ENTERO |
| 16 | BOQUERONES | CHICO ENTERO |
| 60 | LENGUADO | PLANOS |
| 120 | LENGUADOS | PLANOS |
| 160 | URTA | RESTO HORNO |

#### Filtro de Productos Activos (Ultimos 3 Meses)

Solo se muestran los articulos con ventas en los ultimos 3 meses.

```sql
SELECT DISTINCT a.codigo, a.nombre, f.nombre as familia
FROM articulos a
JOIN familias f ON a.familia_id = f.id
JOIN v2_facturas_tickets_lineas v ON v.IdArticulo = a.id
WHERE v.created_at >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)
```

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

### 6.3 Email SI (Contratado)

```
Asunto: Bienvenido a La Carihuela

Bienvenido a La Carihuela. Estamos muy felices de que puedas
formar parte de nuestra empresa.

Usuario: [ID_CANDIDATO]
Contraseña: [ENLACE_CREAR_CONTRASEÑA]
```

### 6.4 Email NO (No Contratado)

```
Asunto: Agradecimiento por su participacion

Queremos agradecerle sinceramente su participacion...
Lamentamos comunicarle que en esta ocasion no ha sido posible
contar con usted para incorporarse a nuestro equipo.
```

### 6.5 Flujo 2a Entrevista

```
2a ENTREVISTA
     |
     +-- SI --> EMAIL BIENVENIDA --> CONTRATADOS
     |          (Usuario + Contraseña)
     |
     +-- DUDA --> QUEDA EN ENTREVISTAS
     |
     +-- NO --> EMAIL AGRADECIMIENTO --> DESCARTADOS
```

### 6.6 Alta en Portal de Trabajadores

Cuando el candidato es contratado, se da de alta en la tabla `operadores`.

**Asignacion de ID:**
- Se busca el primer ID libre desde 1
- Si hay huecos, se reutilizan
- Ejemplo: IDs [1,2,_,4] → Asigna 3

**Flujo:**
```
CONTRATADO
     |
     v
Buscar primer ID libre >= 1
     |
     v
Crear registro en operadores
     |
     v
EMAIL: Usuario = ID + Enlace crear contraseña
     |
     v
Trabajador accede al portal
```

---

## 7. FLUJO COMPLETO

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

## 8. Tablas SQL

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

## 9. Dashboard RRHH

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

## 10. Dashboard LLAMADOR

**Rol:** Llamador (persona que realiza las llamadas telefonicas)

**Acceso:** Menu RRHH > Mi Panel

### 10.1 Pantalla 1: Panel Principal

Resumen de tareas pendientes ordenadas por prioridad + entrevistas del dia.

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

## 11. Roles en Seleccion

| Rol | Dashboard | Funcion |
|-----|-----------|---------|
| Evaluador | Dashboard RRHH | Revisar perfiles, resolver dudas, decidir si/no |
| Entrevistador | Dashboard RRHH | Realizar entrevistas, evaluar candidatos |
| Director RRHH | Dashboard RRHH | Supervisar proceso, firmar contratos |
| Gerente | Dashboard RRHH | Crear peticiones de trabajador |
| Llamador | Dashboard LLAMADOR | Llamar candidatos, concertar entrevistas |

---

*Documento generado: ModuloRRHH v1.1*

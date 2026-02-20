# MODULO RRHH - CONTRATACION

## 1. Integracion ERP: CONTRATADO → OPERADORES

### 1.1 Flujo de Contratacion

Cuando un candidato pasa a CONTRATADO (2a Entrevista = Si), se crea automaticamente un registro en la tabla `operadores` del ERP.

```
2a ENTREVISTA = SI (Contratado)
         |
         v
+----------------------------------+
| 1. Buscar primer ID libre >= 1   |
|    (reutiliza huecos)            |
+----------------------------------+
         |
         v
+----------------------------------+
| 2. Crear registro en operadores  |
|    - Datos del candidato         |
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
|    - Portal de trabajadores      |
+----------------------------------+
```

### 1.2 Asignacion de ID de Trabajador

**Tabla:** `operadores`
**Servidor:** gestion.pescadoslacarihuela.es

**Regla de asignacion:**
- Se busca el primer ID libre desde 1
- Si hay huecos en la numeracion, se reutilizan
- Ejemplo: Si IDs [1,2,_,4,5] → Asigna 3

```
Buscar primer ID libre desde 1
         |
         v
Ejemplo: IDs [_,2,_,_,5,6,...]
         |
         v
Asigna ID = 1 (primer hueco libre)
```

**Ejemplos de trabajadores:**

| ID | Nombre | Apellido |
|----|--------|----------|
| 175 | Dolores | Morales |
| 189 | Jesus Javier | Raya |
| 194 | Virginia | Jimenez |
| 597 | Haydee Lucia | Maltez |

### 1.3 Primer Acceso del Trabajador

Cuando el trabajador recibe el email de bienvenida con su ID, debe acceder al portal y completar información obligatoria.

#### 1.3.1 Datos Obligatorios Primer Acceso

| # | Campo | Descripcion | Tipo | Obligatorio |
|---|-------|-------------|------|-------------|
| 1 | Nombre | Nombre del trabajador | VARCHAR | SI |
| 2 | Apellido 1 | Primer apellido | VARCHAR | SI |
| 3 | Apellido 2 | Segundo apellido | VARCHAR | SI |
| 4 | Fecha de nacimiento | DD/MM/AAAA | DATE | SI |
| 5 | Telefono | Movil de contacto | VARCHAR | SI |
| 6 | Email | Correo electronico | VARCHAR | SI |
| 7 | Direccion | Domicilio completo | VARCHAR | SI |
| 8 | Codigo postal | CP | CHAR(5) | SI |
| 9 | Ciudad | Municipio/Localidad | VARCHAR | SI |
| 10 | DNI/NIE | Documento de identidad | VARCHAR | SI |
| 11 | Numero Afiliacion SS | NAF Seguridad Social | VARCHAR | SI |
| 12 | Cuenta bancaria | IBAN para nominas | VARCHAR | SI |

#### 1.3.2 Verificacion Cuenta Bancaria (Anti-Fraude)

Para evitar fraudes, la cuenta bancaria requiere verificacion manual:

```
TRABAJADOR INTRODUCE CUENTA BANCARIA
         |
         v
+----------------------------------+
| 1. Repetir numero de cuenta      |
|    (doble entrada)               |
+----------------------------------+
         |
         v
+----------------------------------+
| 2. Subir PDF del banco           |
|    (extracto o certificado       |
|     que muestre titular + IBAN)  |
+----------------------------------+
         |
         v
+----------------------------------+
| 3. Estado: PENDIENTE VERIFICAR   |
+----------------------------------+
         |
         v
+----------------------------------+
| 4. Persona de nominas revisa     |
|    - Comprueba PDF               |
|    - Verifica titular = trabajador|
|    - Verifica IBAN coincide      |
+----------------------------------+
         |
         v
+----------------------------------+
| 5. CHECK de verificacion         |
|    Estado: CUENTA VERIFICADA     |
+----------------------------------+
```

**Responsable verificacion:** Persona que gestiona las nominas

**Campos en BD:**
| Campo | Descripcion |
|-------|-------------|
| cuenta_iban | IBAN introducido |
| cuenta_pdf | Ruta al PDF subido |
| cuenta_verificada | BOOLEAN (0/1) |
| cuenta_verificada_por | ID usuario que verifico |
| cuenta_verificada_fecha | Timestamp verificacion |

#### 1.3.3 Alerta Contratacion Completada

Cuando se asigna el ID al trabajador, se envia automaticamente una alerta:

```
ASIGNACION ID TRABAJADOR
         |
         v
+----------------------------------+
| ALERTA AUTOMATICA                |
| Destinatarios:                   |
| - Gerente                        |
| - Director RRHH                  |
+----------------------------------+
         |
         v
+----------------------------------+
| Contenido:                       |
| "Manuel Lopez ha concluido el    |
|  proceso de seleccion"           |
|                                  |
| + Notas de la entrevista         |
| + CV adjunto                     |
+----------------------------------+
```

**Codigo alerta:** `ALERT_002`

---

### 1.4 Mapeo de Campos: candidatos → operadores

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

---

## 2. Datos del Contrato

### 2.1 Campos que completa el Director RRHH / Gerente

Cuando el Director RRHH o Gerente recibe la alerta de contratacion completada, entra en la ficha del trabajador y debe completar los siguientes campos:

| # | Campo | Abrev. | Descripcion | Tipo | Obligatorio |
|---|-------|--------|-------------|------|-------------|
| 1 | Contrato Desde | Cto Desde | Fecha inicio del contrato | DATE | SI |
| 2 | Contrato Hasta | Cto Hasta | Fecha fin (- si indefinido) | DATE | NO |
| 3 | Categoria | Cat | Categoria profesional (T0, T1, T2, T3) | FK | SI |
| 4 | Horas | Hrs | Horas semanales | INT | SI |
| 5 | Codigo | Cod | Codigo de contrato | VARCHAR | SI |
| 6 | Tipo | Tipo | Temporal, Prorroga, Sustituc., Indefinido | ENUM | SI |
| 7 | Sustitucion | Sust | Persona sustituida (- si no aplica) | FK | Solo si Tipo=Sustituc. |
| 8 | Validez Desde | Val Desde | Fecha desde que aplica esta linea | DATE | SI |
| 9 | Validez Hasta | Val Hasta | Fecha hasta que aplica (- si indefinido) | DATE | NO |

**Campos calculados automaticamente:**
| Campo | Abrev. | Descripcion |
|-------|--------|-------------|
| Duracion Contrato | Dur.Cto | Duracion total del contrato actual |
| Duracion Condicion | Dur.Cond | Duracion de las condiciones actuales |
| Acciones | Acciones | Estado de firmas (H D T) |

#### 2.1.1 Ejemplo Visual - Ficha Contrato (Sustitucion A.Garcia)

```
+============================================================================+
|  FICHA CONTRATO - DATOS A COMPLETAR                                        |
+============================================================================+
|                                                                             |
|  Contrato Desde:   [01/06/2026]                                             |
|                                                                             |
|  Contrato Hasta:   [31/08/2026]                                             |
|                                                                             |
|  Categoria:        [T1                      v]                              |
|                                                                             |
|  Horas semanales:  [30]                                                     |
|                                                                             |
|  Codigo:           [150]                                                    |
|                                                                             |
|  Tipo:             [Sustituc.               v]                              |
|                                                                             |
|  Sustitucion:      [A.Garcia                v]                              |
|                                                                             |
|  Validez Desde:    [01/06/2026]                                             |
|                                                                             |
|  Validez Hasta:    [31/08/2026]                                             |
|                                                                             |
|  -----------------------------------------------------------------------    |
|  CAMPOS CALCULADOS:                                                         |
|  Dur.Cto:          3m                                                       |
|  Dur.Cond:         3m                                                       |
|  Acciones:         H D T                                                    |
|  -----------------------------------------------------------------------    |
|                                                                             |
|  [GUARDAR]                                                                  |
|                                                                             |
+============================================================================+
```

#### 2.1.2 Resultado en Historial de Contratos

```
┌───┬────────────┬────────────┬─────┬─────┬─────┬────────────┬───────────┬────────────┬────────────┬─────────┬──────────┬──────────┐
│ # │ Cto Desde  │ Cto Hasta  │ Cat │ Hrs │ Cod │    Tipo    │   Sust    │ Val Desde  │ Val Hasta  │ Dur.Cto │ Dur.Cond │ Acciones │
├───┼────────────┼────────────┼─────┼─────┼─────┼────────────┼───────────┼────────────┼────────────┼─────────┼──────────┼──────────┤
│ 6 │ 01/06/2026 │ 31/08/2026 │ T1  │ 30  │ 150 │ Sustituc.  │ A.Garcia  │ 01/06/2026 │ 31/08/2026 │ 3m      │ 3m       │ H D T    │
└───┴────────────┴────────────┴─────┴─────┴─────┴────────────┴───────────┴────────────┴────────────┴─────────┴──────────┴──────────┘
```

#### 2.1.3 Flujo tras Guardar - Comunicaciones Automaticas

```
DIRECTOR RRHH / GERENTE guarda datos
         |
         v
+------------------------------------------+
| ALERTA 1: HERMI (Asesor SS)              |
| "Tienes informacion para un nuevo        |
|  contrato a nombre Manuel Lopez"         |
|                                          |
| + Cto Desde: 01/06/2026                  |
| + Cto Hasta: 31/08/2026                  |
| + Categoria: T1                          |
| + Horas: 30                              |
| + Codigo: 150                            |
| + Tipo: Sustituc.                        |
| + Sustituye a: A.Garcia                  |
+------------------------------------------+
         |
         v
+------------------------------------------+
| COMUNICACION 2: CARLOS + SUPERVISORES    |
| "Manuel Lopez ha sido contratado"        |
|                                          |
| + Experiencia: 3 años pescaderia         |
| + Telefono: 657 XXX XXX                  |
| + Fecha comienzo: 01/06/2026             |
| + Categoria: T1                          |
| + Horas: 30                              |
| + Tipo: Sustitucion de A.Garcia          |
|                                          |
| NOTAS ENTREVISTAS:                       |
| Candidato con buena actitud. Conoce      |
| bien el producto. Disponibilidad         |
| inmediata.                               |
+------------------------------------------+
```

**Destinatarios Comunicacion 2:**
| Destinatario | Rol |
|--------------|-----|
| Carlos | Supervisor general |
| Supervisores de tienda | Responsables de cada punto de venta |

**Codigo alertas:**
- ALERT_003: Alerta Hermi nuevo contrato
- ALERT_004: Comunicacion nuevo empleado (Carlos + Supervisores)

### 2.2 Campos que completa Hermi (Asesor SS)

| # | Campo | Descripcion |
|---|-------|-------------|
| 1 | Tipo de contrato | Temporal, indefinido, etc. |
| 2 | Codigo de contrato | Codigo oficial del contrato |

### 2.3 Opciones de Tipo de Horario

| Codigo | Descripcion |
|--------|-------------|
| MANANA | Turno de mañana |
| TARDE | Turno de tarde |
| PARTIDO | Jornada partida |
| ROTATIVO | Turnos rotativos |
| NOCHE | Turno de noche |
| FLEXIBLE | Horario flexible |

---

## 3. Flujo de Alertas de Contratacion

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
```

---

## 4. Firma de Contrato

### 4.1 Flujo de Firma

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

### 4.2 Estados del Contrato

| Estado | Descripcion |
|--------|-------------|
| PENDIENTE_ALTA | Esperando alta en SS por Hermi |
| PENDIENTE_FIRMA_EMPRESA | Alta realizada, pendiente firma Director RRHH |
| FIRMADO_EMPRESA | Director RRHH ha firmado, pendiente trabajador |
| FIRMADO_AMBOS | Contrato completado |

---

## 5. Modificacion de Condiciones

### 5.1 Condiciones que generan nuevo contrato/anexo

| Condicion | Genera nuevo contrato |
|-----------|----------------------|
| Cambio de categoria | SI |
| Cambio de jornada (horas) | SI |

### 5.2 Flujo Modificacion

```
TRABAJADOR CON CONTRATO ACTIVO
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

---

## 6. Historial de Contratos - Formato Visual

### 6.1 Estructura de Columnas

| Columna | Abrev. | Descripcion | Tipo BD |
|---------|--------|-------------|---------|
| # | # | Numero de linea secuencial | INT |
| Contrato Desde | Cto Desde | Fecha inicio del contrato original | DATE |
| Contrato Hasta | Cto Hasta | Fecha fin del contrato (- si indefinido) | DATE NULL |
| Categoria | Cat | Categoria profesional (T0, T1, etc.) | VARCHAR |
| Horas | Hrs | Horas semanales | INT |
| Codigo | Cod | Codigo de contrato | VARCHAR |
| Tipo | Tipo | Tipo: Temporal, Prorroga, Sustituc., Indefinido | VARCHAR |
| Sustitucion | Sust | Nombre persona sustituida (- si no aplica) | VARCHAR |
| Validez Desde | Val Desde | Fecha desde que aplica esta linea | DATE |
| Validez Hasta | Val Hasta | Fecha hasta que aplica esta linea | DATE NULL |
| Duracion Contrato | Dur.Cto | Duracion total del contrato actual | VARCHAR |
| Duracion Condicion | Dur.Cond | Duracion de las condiciones actuales | VARCHAR |
| Acciones | Acciones | Estado de firmas | VARCHAR |

### 6.2 Tipos de Contrato y Duracion

| Tipo | Descripcion | Dur.Cto | Dur.Cond |
|------|-------------|---------|----------|
| **Temporal** | Contrato temporal inicial | Duracion inicial | Tiempo con cond. actuales |
| **Prorroga** | Extension del contrato temporal | Suma acumulada | Tiempo con cond. actuales |
| **Sustituc.** | Contrato por sustitucion | Tiempo desde inicio | Tiempo con cond. actuales |
| **Indefinido** | Contrato indefinido | Tiempo desde inicio | Tiempo con cond. actuales |

### 6.3 Ejemplo Visual (Fecha actual: 20/03/2027)

```
┌───┬────────────┬────────────┬─────┬─────┬─────┬────────────┬───────────┬────────────┬────────────┬─────────┬──────────┬──────────┐
│ # │ Cto Desde  │ Cto Hasta  │ Cat │ Hrs │ Cod │    Tipo    │   Sust    │ Val Desde  │ Val Hasta  │ Dur.Cto │ Dur.Cond │ Acciones │
├───┼────────────┼────────────┼─────┼─────┼─────┼────────────┼───────────┼────────────┼────────────┼─────────┼──────────┼──────────┤
│ 1 │ 01/12/2025 │ 28/02/2026 │ T0  │ 40  │ 100 │ Temporal   │ -         │ 01/12/2025 │ 31/01/2026 │ 3m      │ 2m       │ H D T    │
│ 2 │ 01/12/2025 │ 28/02/2026 │ T1  │ 40  │ 100 │ Temporal   │ -         │ 01/02/2026 │ 14/02/2026 │ 3m      │ 14d      │ H D T    │
│ 3 │ 01/12/2025 │ 28/02/2026 │ T1  │ 20  │ 100 │ Temporal   │ -         │ 15/02/2026 │ 28/02/2026 │ 3m      │ 14d      │ H D T    │
│ 4 │ 01/12/2025 │ 31/05/2026 │ T1  │ 20  │ 100 │ Prorroga   │ -         │ 01/03/2026 │ 30/04/2026 │ 6m      │ 2m 14d   │ H D T    │
│ 5 │ 01/12/2025 │ 31/05/2026 │ T1  │ 30  │ 100 │ Prorroga   │ -         │ 01/05/2026 │ 31/05/2026 │ 6m      │ 1m       │ H D T    │
│ 6 │ 01/06/2026 │ 31/08/2026 │ T1  │ 30  │ 150 │ Sustituc.  │ A.Garcia  │ 01/06/2026 │ 31/08/2026 │ 3m      │ 3m       │ H D T    │
│ 7 │ 01/09/2026 │ -          │ T1  │ 30  │ 200 │ Indefinido │ -         │ 01/09/2026 │ 19/02/2027 │ 5m 19d  │ 5m 19d   │ H D T    │
│ 8 │ 01/09/2026 │ -          │ T3  │ 30  │ 200 │ Indefinido │ -         │ 20/02/2027 │ -          │ 6m 19d  │ 1m       │ H D -    │
└───┴────────────┴────────────┴─────┴─────┴─────┴────────────┴───────────┴────────────┴────────────┴─────────┴──────────┴──────────┘
```

### 6.4 Explicacion del Ejemplo

| # | Tipo | Descripcion | Dur.Cto | Dur.Cond |
|---|------|-------------|---------|----------|
| 1 | Temporal | Contrato temporal inicial 3m, T0, 40h | 3m | 2m |
| 2 | Temporal | Modificacion categoria T0→T1 (mismo cto) | 3m | 14d |
| 3 | Temporal | Modificacion horas 40→20h (mismo cto) | 3m | 14d |
| 4 | Prorroga | +3m prorroga, mismas condiciones (T1, 20h) | 6m | 2m 14d |
| 5 | Prorroga | Modificacion horas 20→30h (dentro prorroga) | 6m | 1m |
| 6 | Sustituc. | Nuevo contrato sustitucion (reinicia Dur.Cto) | 3m | 3m |
| 7 | Indefinido | Nuevo contrato indefinido (reinicia Dur.Cto) | 5m 19d | 5m 19d |
| 8 | Indefinido | Modificacion categoria T1→T3 (pend. firma T) | 6m 19d | 1m |

### 6.5 Estados de Acciones

| Icono | Significado |
|-------|-------------|
| H | Hermi ha subido el documento |
| D | Director RRHH ha firmado |
| T | Trabajador ha firmado |
| - | Pendiente |

### 6.6 Notas Importantes

- **Dur.Cto**: Se acumula en prorrogas (3m → 6m → 9m). Reinicia al cambiar modalidad (Temporal → Sustituc. → Indefinido)
- **Dur.Cond**: Se calcula segun el tiempo con las condiciones actuales (Cat, Hrs, Cod). Reinicia si cambian
- **Prorrogas**: Solo aplican a contratos Temporales. Cada prorroga genera una nueva linea
- **Sustitucion/Indefinido**: No tienen prorrogas. La duracion se calcula desde el inicio del contrato

---

## 7. Alertas de Vencimiento de Contratos

### 7.1 Flujo de Alertas

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
```

### 7.2 Estados del Contrato por Vencer

| Estado | Descripcion |
|--------|-------------|
| ACTIVO | Contrato vigente, sin alertas |
| PROXIMO_VENCER | Menos de 15 dias, alertas activas |
| PENDIENTE_DECISION | Alerta enviada, esperando accion |
| RENOVADO | Nuevo contrato firmado, alertas detenidas |
| FINALIZADO | Contrato terminado, baja SS tramitada |
| NO_RENOVADO | Decision de no renovar, baja SS pendiente |

### 7.3 Acciones Posibles

| Accion | Descripcion | Resultado |
|--------|-------------|-----------|
| **Renovar** | Crear nuevo contrato | Nuevo flujo de firma, alertas detenidas |
| **Finalizar** | No renovar contrato | Tramitar baja SS, alertas detenidas |
| **Modificar** | Cambiar condiciones | Nuevo contrato con cambios |

---

## 8. Documentacion del Empleado

### 8.1 Documentos Obligatorios para TODOS

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

### 8.2 Carnets/Permisos (segun perfil)

| # | Campo | Obligatorio | Condicion | Validez |
|---|-------|-------------|-----------|---------|
| 10 | Carnet C (camion) | No | Opcional | Si |
| 11 | CAP | No | Opcional (si tiene carnet C) | Si |
| 12 | Carnet carretillero | **SI** | **Obligatorio si perfil = LOGISTICA** | Si |
| 13 | Certificado de puntos | **SI** | **Obligatorio si usa vehiculo empresa** | Si |
| 14 | Tacografo | **SI** | **Obligatorio si usa vehiculo empresa** | Si |

### 8.3 Documentos de SALUD

| # | Documento | Obligatorio | Validez | Dias aviso |
|---|-----------|-------------|---------|------------|
| 15 | Carnet Manipulador de Alimentos | **SI** | 4 años | 60 dias |
| 16 | Reconocimiento Medico | **SI** | 1 año | 30 dias |

### 8.4 Documentos a Firmar (independientes del contrato)

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

---

## 9. Alertas de Caducidad de Documentos

### 9.1 Dias de aviso por documento

| Documento | Dias aviso antes de caducar |
|-----------|----------------------------|
| Carnet C | 30 dias |
| CAP | 180 dias (6 meses) |
| Carnet carretillero | 30 dias |
| Certificado de puntos | 30 dias |
| Tacografo | 28 dias |
| Carnet Manipulador | 60 dias |
| Reconocimiento Medico | 30 dias |

### 9.2 Dashboard Alertas

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
|  +------------------------------------------+------------------+---------+ |
|                                                                             |
|  [X] CADUCADOS                                                             |
|  +------------------------------------------+------------------+---------+ |
|  | Carlos Ruiz       | Carnet carretillero  | 10/02/2026       | -8      | |
|  +------------------------------------------+------------------+---------+ |
|                                                                             |
+============================================================================+
```

---

## 10. Procedimiento SQL: Contratar Candidato

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

---

## 11. Portal del Trabajador

El Portal del Trabajador es un espacio personal accesible desde cualquier lugar (no requiere estar fisicamente en la empresa). El trabajador solo ve informacion que le afecta directamente, no relacionada con la tienda.

### 11.1 Menu Principal

```
+============================================+
|  PORTAL DEL TRABAJADOR                     |
+============================================+
|                                            |
|  1. Dashboard - Tareas Pendientes          |
|  2. Documentos                             |
|  3. Contratos                              |
|  4. Horario                                |
|  5. Pedidos                                |
|                                            |
+============================================+
```

### 11.2 Estructura de Documentos

```
2. DOCUMENTOS
   |
   +-- 2.1 Documentos Personales
   |       (DNI, cuenta bancaria, NAF, direccion...)
   |
   +-- 2.2 Documentos Empresa
   |       |
   |       +-- Riesgos Laborales
   |       |       - EPI
   |       |       - Formacion
   |       |       - Informacion
   |       |
   |       +-- Proteccion de Datos
   |       |       - Politica
   |       |       - Confidencialidad
   |       |       - Banco
   |       |       - Imagen
   |       |       - Material
   |       |
   |       +-- Protocolos
   |               - Identi. Acoso
   |
   +-- 2.3 Carnets / Habilitaciones
   |       |
   |       +-- Para TODOS:
   |       |       - Carnet Manipulador
   |       |       - Reconocimiento Medico
   |       |
   |       +-- Solo LOGISTICA (L0, L1):
   |               - Carnet B
   |               - Carnet C
   |               - CAP
   |               - Carretillero
   |
   +-- 2.4 Formacion
           (Formacion especifica del puesto)
```

### 11.3 Contratos

El trabajador puede ver su historial de contratos con todas las lineas (temporales, prorrogas, modificaciones, etc.)

### 11.4 Horario

El trabajador puede consultar su horario asignado.

### 11.5 Pedidos

El trabajador puede realizar solicitudes a traves de esta seccion.

#### 11.5.1 Tablas Base de Datos

**Tabla: `nuevo_carihuela_jorge_preferencia_turno`**

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| id | INT AUTO_INCREMENT | ID unico |
| id_trabajador | INT | Codigo trabajador |
| fecha_desde | DATE | Fecha inicio |
| fecha_hasta | DATE | Fecha fin |
| horario_preferido | ENUM('MAÑANAS','TARDES') | Turno solicitado |
| motivo | TEXT | Motivo de la solicitud |
| documento | VARCHAR(255) NULL | Ruta documento (opcional) |
| estado | ENUM('PENDIENTE','APROBADA','RECHAZADA') | Estado |
| created_at | DATETIME | Fecha creacion |

**Tabla: `nuevo_carihuela_jorge_permiso_puntual`**

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| id | INT AUTO_INCREMENT | ID unico |
| id_trabajador | INT | Codigo trabajador |
| fecha | DATE | Fecha del permiso |
| hora_desde | TIME | Hora salida |
| hora_hasta | TIME NULL | Hora regreso (NULL = fin jornada) |
| motivo | TEXT | Motivo |
| documento | VARCHAR(255) | Ruta documento (obligatorio) |
| estado | ENUM('PENDIENTE','APROBADA','RECHAZADA') | Estado |
| created_at | DATETIME | Fecha creacion |

#### 11.5.2 Tipos de Pedidos

| Tipo | Descripcion | Documento |
|------|-------------|-----------|
| Permiso puntual | Salir antes, llegar tarde, cita medica... | **Obligatorio** |
| Preferencia de turno | Solicitar horario especifico por periodo | Opcional |
| Representacion sindical | Horas sindicales (solo representantes) | **Obligatorio** |

#### 11.5.2 Formulario Permiso Puntual

```
+============================================================+
|  PERMISO PUNTUAL                                           |
+============================================================+
|                                                            |
|  Fecha:              [27/02/2026]                          |
|                                                            |
|  Horario desde:      [12:00]                               |
|                                                            |
|  Horario hasta:      [14:00] (o fin jornada)               |
|                                                            |
|  Motivo:             [Cita medica            v]            |
|                                                            |
|  Documento:          [Seleccionar archivo...] *Obligatorio |
|                                                            |
|  [ENVIAR SOLICITUD]                                        |
|                                                            |
+============================================================+
```

#### 11.5.3 Formulario Preferencia de Turno

```
+============================================================+
|  PREFERENCIA DE TURNO                                      |
+============================================================+
|                                                            |
|  Fecha desde:        [01/03/2026]                          |
|                                                            |
|  Fecha hasta:        [06/03/2026]                          |
|                                                            |
|  Horario preferido:  [Mañanas                v]            |
|                                                            |
|  Motivo:             [________________________]            |
|                      [________________________]            |
|                                                            |
|  Documento:          [Seleccionar archivo...] (Opcional)   |
|                                                            |
|  [ENVIAR SOLICITUD]                                        |
|                                                            |
+============================================================+
```

#### 11.5.4 Formulario Representacion Sindical

```
+============================================================+
|  PERMISO REPRESENTACION SINDICAL                           |
+============================================================+
|                                                            |
|  Dias solicitados:                                         |
|  +------------------------------------------------------+  |
|  | Fecha        | Hora desde | Hora hasta |    Accion   |  |
|  +------------------------------------------------------+  |
|  | 01/03/2026   | 09:00      | 14:00      |    [x]      |  |
|  | 02/03/2026   | 11:00      | 15:00      |    [x]      |  |
|  |              |            |            |    [+]      |  |
|  +------------------------------------------------------+  |
|                                                            |
|  Documento:          [Seleccionar archivo...] *Obligatorio |
|                                                            |
|  [ENVIAR SOLICITUD]                                        |
|                                                            |
+============================================================+
```

### 11.6 Vacaciones

#### 11.6.1 Informacion General

| Campo | Valor |
|-------|-------|
| **Tabla BD** | `nuevo_carihuela_jorge_vacaciones` |
| **Codigo incidencia** | ID 65 = Vacaciones (Vac) |
| **Total anual** | 30 dias/año |
| **Periodos** | Invierno (15 dias) + Verano (15 dias) |

#### 11.6.2 Estados de Vacaciones

| Estado | Descripcion |
|--------|-------------|
| ASIGNADAS | Vacaciones ya confirmadas, muestra periodo |
| PERIODO_ABIERTO | Periodo de solicitud abierto, muestra formulario |
| PENDIENTE | Solicitud enviada, esperando aprobacion |
| APROBADA | Vacaciones aprobadas |
| RECHAZADA | Solicitud rechazada |
| CANCELADA | Vacaciones canceladas |

#### 11.6.3 Reglas de Solicitud

**Regla principal:** Las vacaciones empiezan en **LUNES**

**Excepciones:**
| Excepcion | Descripcion |
|-----------|-------------|
| Semana 0 | Primera semana del año (puede empezar cualquier dia) |
| Lunes festivo | Empieza el siguiente dia laborable |

#### 11.6.4 Posibilidades de Solicitud (por periodo de 15 dias)

| Posibilidad | Descripcion | Ejemplo |
|-------------|-------------|---------|
| **Posibilidad 1** | 1 periodo de 15 dias | 23/02 al 09/03 (15 dias) |
| **Posibilidad 2** | 2 periodos (8 + 7 dias) | 16/02 al 23/02 (8 dias) + otro (7 dias) |

#### 11.6.5 Ejemplos Verificados

```
┌─────┬────────────────────────────────┬────────────┬────────────┬──────┬─────────────┐
│ ID  │ Trabajador                     │ Desde      │ Hasta      │ Dias │ Dia semana  │
├─────┼────────────────────────────────┼────────────┼────────────┼──────┼─────────────┤
│ 111 │ Moraleda Cerrato, Cristina     │ 16/02/2026 │ 23/02/2026 │ 8    │ LUNES ✓     │
│ 213 │ Castro Rodriguez, Nicolas      │ 23/02/2026 │ 09/03/2026 │ 15   │ LUNES ✓     │
└─────┴────────────────────────────────┴────────────┴────────────┴──────┴─────────────┘
```

#### 11.6.6 Formulario Solicitud Vacaciones (Posibilidad 1)

```
+============================================================+
|  SOLICITUD VACACIONES - VERANO 2026                        |
+============================================================+
|                                                            |
|  Periodo disponible: 15 dias                               |
|                                                            |
|  Seleccione modalidad:                                     |
|  (x) Posibilidad 1: 1 periodo de 15 dias                   |
|  ( ) Posibilidad 2: 2 periodos (8 + 7 dias)                |
|                                                            |
|  --------------------------------------------------------  |
|  PERIODO 1:                                                |
|  Fecha inicio:  [23/02/2026] (Lunes)                       |
|  Fecha fin:     [09/03/2026] (auto-calculado)              |
|  Dias:          15                                         |
|  --------------------------------------------------------  |
|                                                            |
|  [ENVIAR SOLICITUD]                                        |
|                                                            |
+============================================================+
```

#### 11.6.7 Formulario Posibilidad 2 (8 + 7 dias)

```
+============================================================+
|  SOLICITUD VACACIONES - VERANO 2026                        |
+============================================================+
|                                                            |
|  Seleccione modalidad:                                     |
|  ( ) Posibilidad 1: 1 periodo de 15 dias                   |
|  (x) Posibilidad 2: 2 periodos (8 + 7 dias)                |
|                                                            |
|  --------------------------------------------------------  |
|  PERIODO 1 (8 dias):                                       |
|  Fecha inicio:  [16/02/2026] (Lunes)                       |
|  Fecha fin:     [23/02/2026] (auto-calculado)              |
|  --------------------------------------------------------  |
|  PERIODO 2 (7 dias):                                       |
|  Fecha inicio:  [__/__/____] (Debe ser Lunes)              |
|  Fecha fin:     [__/__/____] (auto-calculado)              |
|  --------------------------------------------------------  |
|                                                            |
|  [ENVIAR SOLICITUD]                                        |
|                                                            |
+============================================================+
```

#### 11.6.8 Vista Vacaciones Asignadas

```
+============================================================+
|  MIS VACACIONES 2026                                       |
+============================================================+
|                                                            |
|  INVIERNO:                                                 |
|  +------------------------------------------------------+  |
|  | Periodo          | Dias | Estado                     |  |
|  +------------------------------------------------------+  |
|  | 16/02 - 23/02    | 8    | APROBADA                   |  |
|  | 02/03 - 08/03    | 7    | APROBADA                   |  |
|  +------------------------------------------------------+  |
|                                                            |
|  VERANO:                                                   |
|  +------------------------------------------------------+  |
|  | Periodo          | Dias | Estado                     |  |
|  +------------------------------------------------------+  |
|  | 01/06 - 15/06    | 15   | PENDIENTE                  |  |
|  +------------------------------------------------------+  |
|                                                            |
|  RESUMEN ANUAL:                                            |
|  - Dias correspondientes: 30                               |
|  - Dias solicitados:      30                               |
|  - Dias pendientes:       0                                |
|                                                            |
+============================================================+
```

### 11.7 Ausencias

El trabajador puede comunicar ausencias previstas o imprevistas a traves de esta seccion.

#### 11.7.1 Tabla de Permisos Retribuidos (Art. 37 ET)

| Motivo | Dias | Documento |
|--------|------|-----------|
| Matrimonio / Pareja de hecho | 15 | Certificado matrimonio/registro |
| Fallecimiento familiar (hasta 2º grado) | 5 | Certificado defuncion |
| Enfermedad grave familiar | 5 | Informe medico |
| Hospitalizacion familiar | 5 | Justificante hospital |
| Intervencion quirurgica sin hospitalizacion | 5 | Justificante medico |
| Accidente familiar grave | 5 | Parte accidente/informe medico |
| Fuerza mayor familiar (urgencias) | 4 dias/año | Justificante situacion |
| Lactancia | 1h/dia hasta 9 meses | Libro familia |
| Permiso climatico (DANA, etc.) | Hasta 4 | Declaracion autoridades |
| Donacion de organos | Tiempo indispensable | Citacion medica |

**Nota:** Los 5 dias se cuentan en dias laborables (no incluyen fines de semana ni festivos).

#### 11.7.2 Formulario Comunicacion de Ausencia

```
+============================================================+
|  COMUNICACION DE AUSENCIA                                  |
+============================================================+
|                                                            |
|  Motivo:             [Enfermedad grave familiar    v]      |
|                                                            |
|  Fecha desde:        [20/02/2026]                          |
|                                                            |
|  Fecha hasta:        [26/02/2026]                          |
|                                                            |
|  Dias solicitados:   5 dias laborables                     |
|                                                            |
|  Observaciones:      [________________________]            |
|                      [________________________]            |
|                                                            |
|  Documento:          [Seleccionar archivo...] *Obligatorio |
|                                                            |
|  [ENVIAR COMUNICACION]                                     |
|                                                            |
+============================================================+
```

#### 11.7.3 Flujo de Ausencia

```
TRABAJADOR COMUNICA AUSENCIA
         |
         v
+---------------------------+
| Selecciona motivo         |
| (segun tabla Art. 37 ET)  |
+---------------------------+
         |
         v
+---------------------------+
| Sistema muestra dias      |
| correspondientes al motivo|
+---------------------------+
         |
         v
+---------------------------+
| Trabajador adjunta        |
| documento justificativo   |
+---------------------------+
         |
         v
+---------------------------+
| Notifica a Supervisor     |
| y Director RRHH           |
+---------------------------+
         |
         v
+---------------------------+
| Registro en Control       |
| Presencia                 |
+---------------------------+
```

#### 11.7.4 Estados de Ausencia

| Estado | Descripcion |
|--------|-------------|
| COMUNICADA | Ausencia registrada, pendiente de revision |
| JUSTIFICADA | Ausencia con documento validado |
| PENDIENTE_DOCUMENTO | Falta adjuntar justificante |
| RECHAZADA | Documento no valido o motivo no procede |

---

*Documento generado: ModuloRRHH v1.0*

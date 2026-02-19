# MODULO RRHH - CONTRATACION

## 1. Integracion ERP: CONTRATADO → OPERADORES

### 1.1 Flujo de Contratacion

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

### 1.2 Mapeo de Campos: candidatos → operadores

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

### 2.1 Campos que completa el Director RRHH

| # | Campo | Descripcion | Tipo | Ejemplo |
|---|-------|-------------|------|---------|
| 1 | Horas | Horas semanales de trabajo | INT | 40, 35, 20 |
| 2 | Tipo de horario | Tipo de jornada/turno | ENUM | Mañana, Tarde, Partido, Rotativo |
| 3 | Categoria profesional | Categoria segun convenio | FK | Oficial 1a, Peon, Administrativo |
| 4 | Fecha desde | Fecha inicio del contrato | DATE | 01/03/2026 |
| 5 | Fecha hasta | Fecha fin del contrato (si temporal) | DATE | 01/09/2026 o NULL (indefinido) |

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

*Documento generado: ModuloRRHH v1.0*

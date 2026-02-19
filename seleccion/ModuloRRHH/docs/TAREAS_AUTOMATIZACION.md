# TAREAS DE AUTOMATIZACION - MODULO RRHH

**Pescados La Carihuela**
**Fecha:** Febrero 2026
**Version:** 1.0

---

## RESUMEN

Este documento lista todas las tareas de automatizacion pendientes de programar para el Modulo RRHH, ordenadas segun el flujo cronologico del proceso de seleccion.

---

## FLUJO CRONOLOGICO DE AUTOMATIZACIONES

```
ENTRADA CVs ──────────────────────────────────────────────────────────────────
     │
     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  AUTO_001: Importacion automatica CVs por email                             │
│  Email: empleo@pescadoslacarihuela.es → Agente IA (Ollama+Mistral) → BD     │
└─────────────────────────────────────────────────────────────────────────────┘
     │
     ▼
LLAMADAS ─────────────────────────────────────────────────────────────────────
     │
     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  DESC_002: Descarte automatico por intentos excedidos                       │
│  Si intentos >= MAX_INTENTOS → Descartado (NO_CONTESTA)                     │
└─────────────────────────────────────────────────────────────────────────────┘
     │
     ▼
1a ENTREVISTA ────────────────────────────────────────────────────────────────
     │
     ├── No Presentado ─────────────────────────────────────────────────────┐
     │                                                                       │
     │   ┌───────────────────────────────────────────────────────────────┐   │
     │   │  DESC_001: Descarte automatico No Presentado                  │   │
     │   │  → Descartado (NO_ASISTIO) sin email                          │   │
     │   └───────────────────────────────────────────────────────────────┘   │
     │                                                                       │
     ├── No (Rechazado) ────────────────────────────────────────────────────┤
     │                                                                       │
     │   ┌───────────────────────────────────────────────────────────────┐   │
     │   │  EMAIL_002: Email Rechazo tras 1a Entrevista                  │   │
     │   │  Solo si Presentado = Si                                      │   │
     │   └───────────────────────────────────────────────────────────────┘   │
     │                                                                       │
     └── Entrega Codigos ───────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  EMAIL_001: Email Entrega de Codigos                                        │
│  Enlace al sistema gaming                                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                │
                ▼
CODIGOS (GAMING) ─────────────────────────────────────────────────────────────
                │
                ▼
2a ENTREVISTA ────────────────────────────────────────────────────────────────
     │
     ├── No Presentado ─────────────────────────────────────────────────────┐
     │                                                                       │
     │   ┌───────────────────────────────────────────────────────────────┐   │
     │   │  DESC_001: Descarte automatico No Presentado                  │   │
     │   │  → Descartado (NO_ASISTIO) sin email                          │   │
     │   └───────────────────────────────────────────────────────────────┘   │
     │                                                                       │
     ├── No (Rechazado) ────────────────────────────────────────────────────┤
     │                                                                       │
     │   ┌───────────────────────────────────────────────────────────────┐   │
     │   │  EMAIL_002: Email Rechazo tras 2a Entrevista                  │   │
     │   │  Solo si Presentado = Si                                      │   │
     │   └───────────────────────────────────────────────────────────────┘   │
     │                                                                       │
     └── Contratado ────────────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  EMAIL_003: Email Bienvenida Contratacion                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                │
                ▼
CONTRATADO (FIN) ─────────────────────────────────────────────────────────────
```

---

## 1. ENTRADA DE CVs

### AUTO_001: Importacion automatica de CVs por email

| Campo | Valor |
|-------|-------|
| **ID** | AUTO_001 |
| **Momento** | Entrada de CVs |
| **Nombre** | Importacion automatica de CVs |
| **Prioridad** | ALTA |
| **Estado** | PENDIENTE |

**Descripcion:**
Los CVs que llegan al email empleo@pescadoslacarihuela.es deben integrarse automaticamente en la tabla de candidatos.

**Flujo:**
```
Email recibido en empleo@pescadoslacarihuela.es
         │
         ▼
┌──────────────────────────────────────────┐
│  Leer adjuntos (PDF, DOC, DOCX)          │
└──────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│  AGENTE IA - EXTRACTOR DE CVs            │
│  Tecnologia: Ollama + Mistral (local)    │
│  Cumple: LOPD y RGPD                     │
├──────────────────────────────────────────┤
│  Extraer datos del CV:                   │
│  - Nombre, Apellido                      │
│  - Telefono, Email                       │
│  - Localidad                             │
│  - Experiencia (anos)                    │
│  - Carnets (B, C, CAP, Carretillero)     │
│  - Vehiculo propio                       │
│  - Estudios                              │
└──────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│  Insertar en tabla candidatos            │
│  Estado: SIN_CLASIFICAR                  │
└──────────────────────────────────────────┘
```

**Tecnologia:**
| Componente | Valor |
|------------|-------|
| Motor IA | Ollama (local) |
| Modelo | Mistral |
| Privacidad | Cumple LOPD y RGPD (procesamiento local) |

**Origen:** Email empleo@pescadoslacarihuela.es
**Destino:** Tabla `candidatos`
**Frecuencia:** Continuo (cada email recibido)

---

## 2. LLAMADAS

### DESC_002: Descarte por Intentos Excedidos

| Campo | Valor |
|-------|-------|
| **ID** | DESC_002 |
| **Momento** | Llamadas para Entrevistas |
| **Nombre** | Descarte automatico por intentos |
| **Prioridad** | BAJA |
| **Estado** | PENDIENTE |

**Trigger:** Campo `intentos` alcanza el limite configurado (ej: 5)

**Accion:**
- Insertar en `candidatos_descartados`
- Motivo: NO_CONTESTA
- NO enviar email

---

## 3. 1a ENTREVISTA

### DESC_001: Descarte por No Presentado

| Campo | Valor |
|-------|-------|
| **ID** | DESC_001 |
| **Momento** | 1a/2a Entrevista - Candidato no se presenta |
| **Nombre** | Descarte automatico No Presentado |
| **Prioridad** | BAJA |
| **Estado** | PENDIENTE |

**Trigger:** Llamador marca "No Presentado" en Entrevistas de Hoy

**Accion:**
- Insertar en `candidatos_descartados`
- Motivo: NO_ASISTIO
- NO enviar email

---

### EMAIL_002: Email Rechazo tras 1a Entrevista

| Campo | Valor |
|-------|-------|
| **ID** | EMAIL_002 |
| **Momento** | 1a Entrevista = No (Rechazado) |
| **Nombre** | Email Rechazo tras Entrevista |
| **Prioridad** | MEDIA |
| **Estado** | PENDIENTE |

**Trigger:** Entrevistador marca "No" en la 1a entrevista

**Condicion:** Solo se envia si el candidato se presento (Presentado = Si)

**NO se envia si:** Candidato marcado como "No Presentado"

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

---

### EMAIL_001: Email Entrega de Codigos

| Campo | Valor |
|-------|-------|
| **ID** | EMAIL_001 |
| **Momento** | 1a Entrevista = Entrega Codigos |
| **Nombre** | Email Entrega de Codigos |
| **Prioridad** | MEDIA |
| **Estado** | PENDIENTE |

**Trigger:** Entrevistador marca "Entrega Codigos" en la 1a entrevista

**Plantilla:**
```
Asunto: Bienvenido al equipo - Acceso al Sistema de Codigos

Estimado/a Sr/a [APELLIDO]:

Gracias por participar en el proceso de seleccion para el puesto de
[POSICION] en La Carihuela Gestion de Pescaderias SL.

Nos complace informarle que ha superado la entrevista y le damos
la bienvenida a nuestro equipo.

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

---

## 4. 2a ENTREVISTA

### EMAIL_002: Email Rechazo tras 2a Entrevista

(Misma plantilla que EMAIL_002 en 1a Entrevista)

| Campo | Valor |
|-------|-------|
| **ID** | EMAIL_002 |
| **Momento** | 2a Entrevista = No (Rechazado) |
| **Condicion** | Solo si Presentado = Si |

---

### EMAIL_003: Email Bienvenida Contratacion

| Campo | Valor |
|-------|-------|
| **ID** | EMAIL_003 |
| **Momento** | 2a Entrevista = Contratado |
| **Nombre** | Email Bienvenida Contratacion |
| **Prioridad** | MEDIA |
| **Estado** | PENDIENTE |

**Trigger:** Entrevistador marca "Contratado" en la 2a entrevista

**Plantilla:** Por definir

---

## 5. AGENTE IA - EXTRACTOR DE CVs

### Descripcion

El sistema utiliza un agente de Inteligencia Artificial local para extraer la informacion de los CVs recibidos.

### Tecnologia

| Componente | Descripcion |
|------------|-------------|
| **Plataforma** | Ollama (ejecucion local) |
| **Modelo** | Mistral |
| **Privacidad** | Cumple LOPD y RGPD |
| **Ubicacion** | Servidor interno (sin envio de datos a terceros) |

### Ventajas de Procesamiento Local

- **Cumplimiento LOPD:** Los datos personales no salen del servidor
- **Cumplimiento RGPD:** No hay transferencia a terceros
- **Velocidad:** Procesamiento rapido sin latencia de red
- **Coste:** Sin costes por API externa
- **Control:** Total control sobre el modelo y los datos

### Campos Extraidos

| Campo | Descripcion | Destino BD |
|-------|-------------|------------|
| Nombre | Nombre del candidato | candidatos.nombre |
| Apellido | Apellido del candidato | candidatos.apellido |
| Telefono | Telefono de contacto | candidatos.telefono |
| Email | Correo electronico | candidatos.email |
| Localidad | Ciudad de residencia | candidatos.localidad |
| Experiencia | Anos de experiencia | candidatos.anos_experiencia |
| Vehiculo | Vehiculo propio (S/N) | candidatos.vehiculo_propio |
| Carnet B | Carnet de conducir B | candidatos.carnet_b |
| Carnet C | Carnet de conducir C | candidatos.carnet_c |
| CAP | Certificado CAP | candidatos.cap |
| Carretillero | Carnet carretillero | candidatos.carretillero |
| Estudios | Formacion academica | candidatos.estudios |

---

## 6. RESUMEN DE TAREAS (Orden Cronologico)

| Orden | ID | Momento en Flujo | Nombre | Tipo | Estado |
|-------|-----|------------------|--------|------|--------|
| 1 | AUTO_001 | Entrada CVs | Importacion automatica CVs por email | IA + Integracion | PENDIENTE |
| 2 | DESC_002 | Llamadas | Descarte por intentos excedidos | Descarte | PENDIENTE |
| 3 | DESC_001 | 1a/2a Entrevista | Descarte No Presentado | Descarte | PENDIENTE |
| 4 | EMAIL_002 | 1a Entrevista = No | Email Rechazo | Email | PENDIENTE |
| 5 | EMAIL_001 | 1a Entrevista = Codigos | Email Entrega de Codigos | Email | PENDIENTE |
| 6 | EMAIL_002 | 2a Entrevista = No | Email Rechazo | Email | PENDIENTE |
| 7 | EMAIL_003 | 2a Entrevista = Contratado | Email Bienvenida Contratacion | Email | PENDIENTE |

---

## 7. DATOS DE CONFIGURACION

### 7.1 Emails del Sistema

| Email | Uso |
|-------|-----|
| empleo@pescadoslacarihuela.es | Recepcion de CVs |
| seleccion@pescadoslacarihuela.es | Envio de emails a candidatos |

### 7.2 Parametros Configurables

| Parametro | Valor por defecto | Descripcion |
|-----------|-------------------|-------------|
| MAX_INTENTOS_LLAMADA | 5 | Intentos antes de descarte automatico |
| ENLACE_SISTEMA_CODIGOS | (por definir) | URL del sistema gaming |

### 7.3 Variables de Plantilla

| Variable | Descripcion | Origen |
|----------|-------------|--------|
| [APELLIDO] | Apellido del candidato | candidatos.apellido |
| [POSICION] | Titulo del puesto | peticiones_trabajador.posicion |
| [ENLACE_SISTEMA_CODIGOS] | URL del sistema gaming | Configuracion sistema |

---

*Documento de Tareas de Automatizacion - ModuloRRHH v1.0*

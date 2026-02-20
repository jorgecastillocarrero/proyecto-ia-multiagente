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
┌─────────────────────────────────────────────────────────────────────────────┐
│  ALERT_001: Alerta Codigos Completado                                       │
│  Candidato aprueba examen → Alerta a Entrevistador + Director RRHH          │
└─────────────────────────────────────────────────────────────────────────────┘
                │
                ▼
2a ENTREVISTA / CONTRATACION ─────────────────────────────────────────────────
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
┌─────────────────────────────────────────────────────────────────────────────┐
│  ALERT_002: Alerta Contratacion Completada                                  │
│  Asignacion ID → Alerta a Gerente + Director RRHH (con notas + CV)          │
└─────────────────────────────────────────────────────────────────────────────┘
                │
                ▼
DIRECTOR RRHH / GERENTE completa datos contrato
                │
                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  ALERT_003: Alerta Hermi Nuevo Contrato                                     │
│  "Tienes informacion para un nuevo contrato a nombre [Nombre]"              │
└─────────────────────────────────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  ALERT_004: Comunicacion Nuevo Empleado                                     │
│  Carlos + Supervisores: "[Nombre] ha sido contratado" + info                │
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

---

## 4. CODIGOS (GAMING)

### ALERT_001: Alerta Codigos Completado

| Campo | Valor |
|-------|-------|
| **ID** | ALERT_001 |
| **Momento** | Candidato aprueba examen de codigos (>= 7/10) |
| **Nombre** | Alerta Codigos Completado |
| **Prioridad** | ALTA |
| **Estado** | PENDIENTE |

**Trigger:** Candidato aprueba examen de codigos (>= 7 de 10 aciertos)

**Destinatarios:**
- Entrevistador
- Director RRHH

**Mensaje:**
```
[NOMBRE] [APELLIDO] se sabe los codigos
```

**Ejemplo:**
```
Manuel Perez se sabe los codigos
```

### ALERT_002: Alerta Contratacion Completada

| Campo | Valor |
|-------|-------|
| **ID** | ALERT_002 |
| **Momento** | Asignacion de ID de trabajador (contratacion completada) |
| **Nombre** | Alerta Contratacion Completada |
| **Prioridad** | ALTA |
| **Estado** | PENDIENTE |

**Trigger:** Se asigna ID al nuevo trabajador en tabla `operadores`

**Destinatarios:**
- Gerente
- Director RRHH

**Mensaje:**
```
[NOMBRE] [APELLIDO] ha concluido el proceso de seleccion
```

**Adjuntos:**
- Notas de la entrevista
- CV del candidato

**Ejemplo:**
```
Manuel Lopez ha concluido el proceso de seleccion

[Adjunto: Notas entrevista]
[Adjunto: CV_Manuel_Lopez.pdf]
```

### ALERT_003: Alerta Hermi Nuevo Contrato

| Campo | Valor |
|-------|-------|
| **ID** | ALERT_003 |
| **Momento** | Director RRHH/Gerente guarda datos del contrato |
| **Nombre** | Alerta Hermi Nuevo Contrato |
| **Prioridad** | ALTA |
| **Estado** | PENDIENTE |

**Trigger:** Director RRHH o Gerente completa y guarda los datos del contrato

**Destinatarios:**
- Hermi (Asesor SS)

**Mensaje:**
```
Tienes informacion para un nuevo contrato a nombre [NOMBRE] [APELLIDO]

+ Contrato Desde: [CTO_DESDE]
+ Contrato Hasta: [CTO_HASTA]
+ Categoria: [CATEGORIA]
+ Horas: [HORAS]
+ Codigo: [CODIGO]
+ Tipo: [TIPO]
+ Sustituye a: [SUSTITUCION] (si aplica)
```

**Ejemplo:**
```
Tienes informacion para un nuevo contrato a nombre Manuel Lopez

+ Contrato Desde: 01/06/2026
+ Contrato Hasta: 31/08/2026
+ Categoria: T1
+ Horas: 30
+ Codigo: 150
+ Tipo: Sustituc.
+ Sustituye a: A.Garcia
```

### ALERT_004: Comunicacion Nuevo Empleado

| Campo | Valor |
|-------|-------|
| **ID** | ALERT_004 |
| **Momento** | Director RRHH/Gerente guarda datos del contrato |
| **Nombre** | Comunicacion Nuevo Empleado |
| **Prioridad** | MEDIA |
| **Estado** | PENDIENTE |

**Trigger:** Director RRHH o Gerente completa y guarda los datos del contrato (simultaneo con ALERT_003)

**Destinatarios:**
- Carlos (Supervisor general)
- Supervisores de tienda

**Mensaje:**
```
[NOMBRE] [APELLIDO] ha sido contratado

+ Experiencia: [EXPERIENCIA]
+ Telefono: [TELEFONO]
+ Fecha comienzo: [FECHA_INICIO]
+ Categoria: [CATEGORIA]
+ Horas: [HORAS]
+ Tipo: [TIPO]
+ Sustituye a: [SUSTITUCION] (si aplica)

NOTAS ENTREVISTAS:
[NOTAS_ENTREVISTA]
```

**Ejemplo:**
```
Manuel Lopez ha sido contratado

+ Experiencia: 3 años pescaderia
+ Telefono: 657 XXX XXX
+ Fecha comienzo: 01/06/2026
+ Categoria: T1
+ Horas: 30
+ Tipo: Sustitucion de A.Garcia

NOTAS ENTREVISTAS:
Candidato con buena actitud. Conoce bien el producto.
Experiencia previa en Pescaderias Pepe. Disponibilidad inmediata.
```

---

## 5. 2a ENTREVISTA / CONTRATACION

### EMAIL_003: Email Bienvenida Contratacion

| Campo | Valor |
|-------|-------|
| **ID** | EMAIL_003 |
| **Momento** | 2a Entrevista = Si (Contratado) |
| **Nombre** | Email Bienvenida Contratacion |
| **Prioridad** | ALTA |
| **Estado** | PENDIENTE |

**Trigger:** 2a Entrevista marca "Si" (Contratado)

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

---

### EMAIL_004: Email Agradecimiento No Contratado

| Campo | Valor |
|-------|-------|
| **ID** | EMAIL_004 |
| **Momento** | 2a Entrevista = No |
| **Nombre** | Email Agradecimiento No Contratado |
| **Prioridad** | MEDIA |
| **Estado** | PENDIENTE |

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

---

## 6. AGENTE IA - EXTRACTOR DE CVs

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

## 7. RESUMEN DE TAREAS (Orden Cronologico)

| Orden | ID | Momento en Flujo | Nombre | Tipo | Estado |
|-------|-----|------------------|--------|------|--------|
| 1 | AUTO_001 | Entrada CVs | Importacion automatica CVs por email | IA + Integracion | PENDIENTE |
| 2 | DESC_002 | Llamadas | Descarte por intentos excedidos | Descarte | PENDIENTE |
| 3 | DESC_001 | 1a/2a Entrevista | Descarte No Presentado | Descarte | PENDIENTE |
| 4 | EMAIL_002 | 1a Entrevista = No | Email Rechazo | Email | PENDIENTE |
| 5 | EMAIL_001 | 1a Entrevista = Codigos | Email Entrega de Codigos + ID | Email | PENDIENTE |
| 6 | ALERT_001 | Codigos = Aprobado | Alerta Codigos Completado | Alerta | PENDIENTE |
| 7 | EMAIL_003 | 2a Entrevista = Si | Email Bienvenida Contratacion | Email | PENDIENTE |
| 8 | EMAIL_004 | 2a Entrevista = No | Email Agradecimiento No Contratado | Email | PENDIENTE |
| 9 | ALERT_002 | Asignacion ID | Alerta Contratacion Completada | Alerta | PENDIENTE |
| 10 | ALERT_003 | Datos contrato guardados | Alerta Hermi Nuevo Contrato | Alerta | PENDIENTE |
| 11 | ALERT_004 | Datos contrato guardados | Comunicacion Nuevo Empleado + Notas | Alerta | PENDIENTE |

---

## 8. DATOS DE CONFIGURACION

### 8.1 Emails del Sistema

| Email | Uso |
|-------|-----|
| empleo@pescadoslacarihuela.es | Recepcion de CVs |
| seleccion@pescadoslacarihuela.es | Envio de emails a candidatos |

### 8.2 Parametros Configurables

| Parametro | Valor por defecto | Descripcion |
|-----------|-------------------|-------------|
| MAX_INTENTOS_LLAMADA | 5 | Intentos antes de descarte automatico |
| MIN_ACIERTOS_EXAMEN | 7 | Minimo aciertos para aprobar examen codigos |
| ENLACE_SISTEMA_CODIGOS | (por definir) | URL del sistema gaming |
| ENLACE_CREAR_CONTRASEÑA | (por definir) | URL para crear contraseña nuevo empleado |

### 8.3 Variables de Plantilla

| Variable | Descripcion | Origen |
|----------|-------------|--------|
| [NOMBRE] | Nombre del candidato | candidatos.nombre |
| [APELLIDO] | Apellido del candidato | candidatos.apellido |
| [ID_CANDIDATO] | ID unico del candidato | Sistema (generado) |
| [POSICION] | Titulo del puesto | peticiones_trabajador.posicion |
| [ENLACE_SISTEMA_CODIGOS] | URL del sistema gaming | Configuracion sistema |
| [ENLACE_CREAR_CONTRASEÑA] | URL para crear contraseña | Configuracion sistema |

---

*Documento de Tareas de Automatizacion - ModuloRRHH v1.0*

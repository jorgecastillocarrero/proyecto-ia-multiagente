# RESUMEN DEL PROYECTO: Sistema de Seleccion RRHH

**Empresa**: Pescados La Carihuela
**Fecha**: 17 de Febrero de 2026
**Modulo**: Seleccion de Personal (Modulo 1 de RRHH)

---

## 1. QUE ES ESTE PROYECTO

Este proyecto es un **sistema para gestionar la seleccion de personal**. Permite:

1. Recibir CVs de candidatos (principalmente de InfoJobs)
2. Extraer automaticamente los datos de los CVs
3. Clasificar candidatos segun el perfil profesional que buscamos
4. Gestionar el proceso de seleccion (entrevistas, descartes, contrataciones)

---

## 2. QUE SE HA HECHO HASTA AHORA

### 2.1 Base de Datos

Se ha configurado la base de datos MySQL en el servidor de la empresa:
- **Servidor**: 192.168.1.133
- **Base de datos**: gestion.pescadoslacarihuela.es
- **Candidatos cargados**: 208

### 2.2 Perfiles de Trabajo

Se han definido **5 perfiles profesionales** para clasificar candidatos:

| Perfil | Para que sirve | Palabras clave |
|--------|----------------|----------------|
| **PESCADERIA** | Dependientes de tienda, pescaderia, carniceria | tienda, comercio, dependiente, pescad, carnicer |
| **LOGISTICA** | Conductores, repartidores, mozos de almacen | logistica, almacen, reparto, carnet C, CAP |
| **PRODUCCION** | Operarios de fabrica, envasado, sushi | produccion, operario, fabrica, envase, sushi |
| **ADMINISTRATIVO** | Secretariado, contabilidad, oficina | administrativo, secretaria, contable, oficina |
| **GESTION** | Titulados universitarios | grado ADE, derecho, universidad, master |

### 2.3 Clasificacion Automatica

Se ha creado un programa que clasifica automaticamente los candidatos:

**Resultado actual:**
```
LOGISTICA:       67 candidatos (32%)
PRODUCCION:      18 candidatos (9%)
PESCADERIA:       7 candidatos (3%)
ADMINISTRATIVO:   4 candidatos (2%)
GESTION:          0 candidatos (0%)
SIN CLASIFICAR: 112 candidatos (54%)
```

### 2.4 Reglas de Descarte

Se han definido reglas para descartar candidatos automaticamente:

| Regla | Descripcion | Valor |
|-------|-------------|-------|
| Experiencia minima | Descartar si tiene menos de X años | 1 año |
| Distancia maxima | Descartar si vive a mas de X km | 40 km |
| Descartado previo | Si ya fue descartado antes por la misma razon | Automatico |
| Malas referencias | Descartado por decision de Antonio, Carlos o Jorge | Manual |

---

## 3. QUE FALTA POR HACER

### 3.1 Dashboard (Pantalla Principal)

Crear una pantalla visual que muestre:

```
+---------------------------+  +---------------------------+  +---------------------------+
|        PESCADERIA         |  |         LOGISTICA         |  |        PRODUCCION         |
|        7 candidatos       |  |       67 candidatos       |  |       18 candidatos       |
|        6 nuevos           |  |       49 nuevos           |  |       18 nuevos           |
+---------------------------+  +---------------------------+  +---------------------------+
```

**Especificacion completa en**: `docs/ESPECIFICACION_DASHBOARD.md`

### 3.2 Funcionalidades Pendientes

1. **Panel de descartes**: Aplicar reglas de descarte a candidatos
2. **Gestion de entrevistas**: Programar y registrar entrevistas
3. **Cambio de estado**: Mover candidatos entre estados (nuevo -> entrevista -> contratado)
4. **Exportar datos**: Generar Excel con candidatos filtrados

---

## 4. COMO FUNCIONA EL FLUJO

```
PASO 1: Llegan CVs de InfoJobs (archivo PDF)
           |
           v
PASO 2: Se extraen los datos del PDF automaticamente
           |
           v
PASO 3: Se guardan en la base de datos (MySQL)
           |
           v
PASO 4: Se clasifican automaticamente por perfil
           |
           v
PASO 5: El personal de RRHH revisa y gestiona
           |
           v
PASO 6: Se descartan o se contratan
```

---

## 5. ARCHIVOS DEL PROYECTO

```
seleccion/cv-extractor/
│
├── README.md                      # Documentacion tecnica
├── requirements.txt               # Dependencias de Python
├── .env                           # Configuracion (credenciales BD)
│
├── clasificador.py                # Programa que clasifica candidatos
├── db_loader.py                   # Programa que carga datos a MySQL
├── extract_cvs.py                 # Programa que extrae datos de PDFs
│
├── sql/
│   └── schema_mysql.sql           # Estructura de la base de datos
│
├── docs/
│   ├── RESUMEN_PROYECTO.md        # Este documento
│   ├── ESPECIFICACION_DASHBOARD.md # Especificacion del dashboard
│   ├── FLUJO_SELECCION.md         # Flujo de seleccion
│   └── FLUJO_RRHH.md              # Documentacion general RRHH
│
└── archive/                       # Archivos antiguos (PostgreSQL)
```

---

## 6. DATOS TECNICOS

### Base de Datos
- **Motor**: MySQL 8.0
- **Servidor**: 192.168.1.133
- **Puerto**: 3306
- **Base de datos**: gestion.pescadoslacarihuela.es

### Tablas Principales
| Tabla | Descripcion |
|-------|-------------|
| candidatos | Datos de los 208 candidatos |
| perfiles | Los 5 perfiles de trabajo |
| motivos_descarte | Motivos para descartar |
| candidatos_descartados | Historial de descartes |
| reglas_descarte | Reglas configurables |

### Tecnologias
- **Backend**: Node.js + Express (existente)
- **Frontend**: Angular (existente)
- **Base de datos**: MySQL
- **Extraccion CVs**: Python + Claude API

---

## 7. PROXIMO PASO

1. **Aprobar este documento** para confirmar que el enfoque es correcto
2. **Desarrollar el dashboard** siguiendo la especificacion
3. **Implementar los descartes** con las reglas definidas
4. **Probar el sistema** con datos reales

---

## 8. CONTACTO

- **Repositorio Git**: https://github.com/jorgecastillocarrero/proyecto-ia-multiagente
- **Rama**: master

---

*Documento preparado para revision y aprobacion*

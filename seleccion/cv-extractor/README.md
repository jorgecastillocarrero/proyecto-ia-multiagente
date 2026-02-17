# CV-Extractor - Sistema de Seleccion RRHH

**Pescados La Carihuela**

Sistema de extraccion y clasificacion de CVs para el proceso de seleccion de personal.

---

## Indice

1. [Descripcion General](#descripcion-general)
2. [Arquitectura](#arquitectura)
3. [Requisitos](#requisitos)
4. [Instalacion](#instalacion)
5. [Uso](#uso)
6. [Perfiles de Trabajo](#perfiles-de-trabajo)
7. [Reglas de Descarte](#reglas-de-descarte)
8. [Estructura de Archivos](#estructura-de-archivos)
9. [Base de Datos](#base-de-datos)

---

## Descripcion General

El sistema permite:

1. **Extraer CVs** de PDFs descargados de InfoJobs
2. **Clasificar candidatos** automaticamente por perfil profesional
3. **Visualizar dashboard** con estadisticas por perfil
4. **Gestionar descartes** con motivos configurables

---

## Arquitectura

```
+------------------+     +------------------+     +------------------+
|   PDF InfoJobs   | --> |  extract_cvs.py  | --> |   JSON datos     |
+------------------+     +------------------+     +------------------+
                                                          |
                                                          v
+------------------+     +------------------+     +------------------+
|    dashboard.py  | <-- | clasificador.py  | <-- |  db_loader.py    |
+------------------+     +------------------+     +------------------+
        |                        |                        |
        v                        v                        v
+------------------------------------------------------------------+
|                     MySQL (192.168.1.133)                        |
|                 gestion.pescadoslacarihuela.es                   |
+------------------------------------------------------------------+
```

---

## Requisitos

### Software
- Python 3.10+
- MySQL 8.0+
- Acceso a red local (192.168.1.133)

### Dependencias Python
```
pdfplumber==0.11.0
anthropic==0.40.0
pymysql==1.1.0
python-dotenv==1.0.1
```

---

## Instalacion

1. **Clonar repositorio**
```bash
git clone https://github.com/jorgecastillocarrero/proyecto-ia-multiagente.git
cd seleccion/cv-extractor
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con credenciales de BD
```

4. **Verificar conexion**
```bash
python db_loader.py test
```

---

## Uso

### Clasificar candidatos
```bash
python clasificador.py setup   # Crear tablas (solo primera vez)
python clasificador.py run     # Clasificar todos los candidatos
python clasificador.py stats   # Ver estadisticas
```

### Cargar CVs desde JSON
```bash
python db_loader.py load archivo.json
python db_loader.py load-all   # Cargar todos los *_extracted.json
```

### Extraer CVs de PDF
```bash
python extract_cvs.py archivo.pdf
```

---

## Perfiles de Trabajo

| Codigo | Descripcion | Keywords |
|--------|-------------|----------|
| PESCADERIA | Pescaderia, carniceria, comercio | pescad, carnicer, dependient, tienda, comercio |
| LOGISTICA | Almacen, reparto, transporte | logistic, almacen, repartidor, mozo, conductor |
| PRODUCCION | Fabrica, envasado, sushi | sushi, envase, produccion, operario, fabrica |
| ADMINISTRATIVO | Oficina, secretariado | secretari, administrativ, contab, oficina |
| GESTION | Grados universitarios | grado ade, derecho, licenciado, universidad |

### Criterios de Clasificacion

1. **LOGISTICA**: Prioridad si tiene Carnet C o CAP
2. **PESCADERIA**: Si el puesto contiene "tienda", "comercio", "dependiente"
3. **PRODUCCION**: Si el puesto contiene "operario", "fabrica", "envase"
4. **ADMINISTRATIVO**: Si el puesto contiene "administrativo", "secretaria"
5. **GESTION**: Solo con grado universitario

---

## Reglas de Descarte

### Automaticas (configurables)

| Regla | Campo | Condicion | Valor |
|-------|-------|-----------|-------|
| REGLA_EXPERIENCIA | anos_experiencia | < | 1 año |
| REGLA_DISTANCIA | distancia_km | > | 40 km |

### Manuales

| Codigo | Descripcion |
|--------|-------------|
| MALAS_REFERENCIAS | Descartado por Antonio/Carlos/Jorge |
| NO_INTERESADO | Candidato no interesado |
| NO_CONTESTA | No contesta tras varios intentos |
| DESCARTADO_ENTREVISTA | Descartado tras entrevista |

---

## Estructura de Archivos

```
cv-extractor/
├── README.md                  # Este documento
├── requirements.txt           # Dependencias Python
├── .env                       # Configuracion (NO commitear)
├── .env.example               # Plantilla de configuracion
│
├── clasificador.py            # Clasificador de candidatos
├── db_loader.py               # Cargador de datos a MySQL
├── extract_cvs.py             # Extractor de PDFs
├── extract_cvs_batch.py       # Extractor en lote
│
├── sql/
│   └── schema_mysql.sql       # Schema de base de datos
│
├── docs/
│   ├── RESUMEN_PROYECTO.md        # Resumen para direccion
│   ├── ESPECIFICACION_DASHBOARD.md # Especificacion del dashboard
│   ├── FLUJO_SELECCION.md         # Documentacion del flujo
│   └── FLUJO_RRHH.md              # Documentacion RRHH
│
└── archive/                   # Archivos obsoletos (PostgreSQL)
    ├── schema.sql
    ├── schema_seleccion.sql
    └── docker-compose.yml
```

---

## Base de Datos

### Conexion
- **Host**: 192.168.1.133
- **Puerto**: 3306
- **Base de datos**: gestion.pescadoslacarihuela.es
- **Usuario**: root

### Tablas Principales

| Tabla | Descripcion |
|-------|-------------|
| candidatos | Datos de candidatos (existente, modificada) |
| perfiles | Catalogo de perfiles profesionales |
| motivos_descarte | Catalogo de motivos de descarte |
| candidatos_descartados | Historial de descartes |
| reglas_descarte | Reglas configurables |

### Columnas Añadidas a Candidatos

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| provincia | VARCHAR(100) | Provincia del candidato |
| codigo_postal | VARCHAR(10) | Codigo postal |
| puesto_actual | VARCHAR(200) | Puesto actual/deseado |
| carnet_carretillero | TINYINT(1) | Tiene carnet carretillero |
| anos_experiencia | DECIMAL(5,2) | Años de experiencia total |
| archivo_origen | VARCHAR(500) | Archivo PDF de origen |
| perfil_id | INT | FK a tabla perfiles |
| perfil_codigo | VARCHAR(50) | Codigo del perfil asignado |

---

## Datos Actuales

| Metrica | Valor |
|---------|-------|
| Total candidatos | 208 |
| LOGISTICA | 67 |
| PRODUCCION | 18 |
| PESCADERIA | 7 |
| ADMINISTRATIVO | 4 |
| Sin clasificar | 112 |

---

## Contacto

- **Repositorio**: https://github.com/jorgecastillocarrero/proyecto-ia-multiagente
- **Equipo**: RRHH Pescados La Carihuela

---

*Ultima actualizacion: 2026-02-17*

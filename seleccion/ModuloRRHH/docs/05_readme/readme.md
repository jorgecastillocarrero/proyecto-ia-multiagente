# MODULO RRHH - Pescados La Carihuela

**Fecha:** 2026-02-18
**Version:** 1.0

---

## Estructura del Modulo

```
ModuloRRHH/
├── README.md                    # Este archivo
├── 1_Perfiles/
│   └── PERFILES.md             # Perfiles profesionales y ofertas de empleo
├── 2_Seleccion/
│   └── SELECCION.md            # Proceso de seleccion de candidatos
├── 3_Contratacion/
│   └── CONTRATACION.md         # Proceso de contratacion e historial
├── 4_Trabajadores/
│   └── TRABAJADORES.md         # Gestion de trabajadores y ausencias
├── docs/                        # Documentacion en multiples formatos
│   ├── 01_perfiles/
│   │   ├── perfiles.md
│   │   ├── perfiles.html
│   │   └── perfiles.pdf
│   ├── 02_seleccion/
│   │   ├── seleccion.md
│   │   ├── seleccion.html
│   │   └── seleccion.pdf
│   ├── 03_contratacion/
│   │   ├── contratacion.md
│   │   ├── contratacion.html
│   │   └── contratacion.pdf
│   ├── 04_trabajadores/
│   │   ├── trabajadores.md
│   │   ├── trabajadores.html
│   │   └── trabajadores.pdf
│   └── 05_readme/
│       ├── readme.md
│       ├── readme.html
│       └── readme.pdf
└── scripts/
    ├── generar_documentacion.py        # Genera docs en MD, HTML y PDF
    ├── generar_tabla_contratos_pdf.py  # Genera PDF historial contratos
    └── generar_bajas_larga_duracion_pdf.py # Genera PDF bajas larga duracion
```

---

## Contenido por Seccion

### 1. Perfiles (1_Perfiles/)

- Definicion de los 6 perfiles profesionales
- Keywords para clasificacion automatica
- Ofertas de empleo por perfil (InfoJobs)
- Estructura de la tabla SQL `perfiles`

**Perfiles disponibles:**
- PESCADERIA
- LOGISTICA
- PRODUCCION
- ADMINISTRATIVO
- GESTION
- BECARIO

### 2. Seleccion (2_Seleccion/)

- Proceso de peticion de trabajador
- Gestion de candidatos (primera fase)
- Filtros automaticos y manuales
- Sistema de entrevistas (segunda fase)
- Sistema de codigos (gaming)
- Flujo completo de seleccion

### 3. Contratacion (3_Contratacion/)

- Integracion con ERP (candidato → operador)
- Datos del contrato
- Flujo de alertas de contratacion
- Sistema de firma de contratos
- Modificacion de condiciones
- Historial de contratos (formato visual)
- Alertas de vencimiento
- Documentacion del empleado

### 4. Trabajadores (4_Trabajadores/)

- Clasificacion de trabajadores (4 niveles)
- Gestion de ausencias
- Bajas de larga duracion (>=30 dias)
- Bajas de corta duracion (<30 dias)
- Excedencias
- Paternidad/Maternidad
- Lactancia
- Vacaciones
- Representantes sindicales

---

## Scripts Disponibles

### generar_documentacion.py

Genera toda la documentacion en 3 formatos (MD, HTML, PDF) organizados por carpeta.

```bash
cd ModuloRRHH/scripts
py generar_documentacion.py
```

**Salida:** `docs/01_perfiles/`, `docs/02_seleccion/`, etc.

**Formatos generados:**
- `.md` - Markdown original
- `.html` - HTML con estilos profesionales
- `.pdf` - PDF (requiere fpdf2 o wkhtmltopdf)

---

### generar_tabla_contratos_pdf.py

Genera un PDF con el historial de contratos en formato visual.

```bash
cd ModuloRRHH/scripts
python generar_tabla_contratos_pdf.py
```

**Salida:** `reportes/historial_contratos_tabla_YYYYMMDD_HHMMSS.pdf`

### generar_bajas_larga_duracion_pdf.py

Genera un PDF con la documentacion de bajas de larga duracion.

```bash
cd ModuloRRHH/scripts
python generar_bajas_larga_duracion_pdf.py
```

**Salida:** `reportes/bajas_larga_duracion_YYYYMMDD_HHMMSS.pdf`

---

## Base de Datos

**Servidor:** 192.168.1.133

### Tablas principales

| Tabla | Descripcion |
|-------|-------------|
| perfiles | Perfiles profesionales + ofertas |
| peticiones_trabajador | Peticiones de personal |
| candidatos | Candidatos en proceso |
| operadores | Trabajadores contratados |
| contratos_usuario | Historial de contratos |
| nuevo_carihuela_jorge_bajas_larga_duracion | Bajas >= 30 dias |
| nuevo_carihuela_jorge_excedencia | Excedencias |
| nuevo_carihuela_jorge_vacaciones | Vacaciones |

---

## Roles Principales

| Rol | Responsabilidades |
|-----|-------------------|
| Director RRHH | Completar datos contrato, firmar documentos |
| Hermi (Asesor SS) | Alta SS, subir documentos, tipo contrato |
| Llamador | Llamar candidatos, concertar entrevistas |
| Entrevistador | Realizar entrevistas, evaluar candidatos |
| Trabajador | Firmar documentos, completar datos personales |

---

*ModuloRRHH v1.0 - Pescados La Carihuela*

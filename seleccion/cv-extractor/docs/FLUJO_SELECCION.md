# Flujo de Selección de Personal - Pescados La Carihuela

## 1. Perfiles de Trabajo

| # | Perfil | Palabras Clave / Requisitos |
|---|--------|----------------------------|
| 1 | **PESCADERÍA** | pescadería, carnicería, comercio, corte, fileteado, marisco |
| 2 | **LOGÍSTICA** | carnet C, CAP, logística, reparto, almacén, transporte |
| 3 | **PRODUCCIÓN** | sushi, sala de envase, producción, envasado |
| 4 | **ADMINISTRATIVO** | secretariado, administrativo, FP/ciclo superior en administración |
| 5 | **GESTIÓN** | Grados universitarios (ADE, Derecho, etc.) |

---

## 2. Flujo de Trabajo

```
┌─────────────────┐
│  PDF InfoJobs   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  extract_cvs.py │  ← Extrae texto con pdfplumber
│  + Claude API   │  ← Estructura datos con IA
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  clasificador.py│  ← Clasifica por perfil
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    MySQL BD     │  ← candidatos + perfil_id
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────┐
│              CLASIFICACIÓN AUTOMÁTICA            │
├─────────┬─────────┬─────────┬─────────┬─────────┤
│PESCADERÍA│LOGÍSTICA│PRODUCCIÓN│ADMIN   │GESTIÓN  │
│    6    │   67    │   18    │   4    │   3     │
└─────────┴─────────┴─────────┴─────────┴─────────┘
         │
         ▼
┌─────────────────┐
│ SIN_CLASIFICAR  │  ← 110 candidatos para revisión
│   (Otros)       │
└─────────────────┘
```

---

## 3. Criterios de Clasificación

### PESCADERÍA
- Experiencia en: pescadería, carnicería, charcutería
- Habilidades: corte, fileteado, despiece, marisco
- Atención al cliente en mostrador de frescos

### LOGÍSTICA
- **Obligatorio**: Carnet C o CAP
- Experiencia en: almacén, reparto, transporte
- Puestos: carretillero, mozo, repartidor, conductor

### PRODUCCIÓN
- Experiencia en: fábrica, línea de producción
- Puestos: operario, envasador, manipulador
- Específico: sushi, sala de envase

### ADMINISTRATIVO
- Formación: FP/Ciclo Superior en Administración
- Experiencia: secretariado, contabilidad, facturación
- Puestos: auxiliar administrativo, recepcionista

### GESTIÓN
- Formación: Grado universitario (ADE, Derecho, etc.)
- Experiencia en puestos de responsabilidad
- Puestos: encargado, responsable, supervisor, jefe

---

## 4. Estados del Candidato

```
NUEVO → CLASIFICADO → EN_REVISION → SELECCIONADO → ENTREVISTA → CONTRATADO
                  ↓
              DESCARTADO
```

---

## 5. Resultado Clasificación Actual (208 candidatos)

| Perfil | Cantidad | % |
|--------|----------|---|
| LOGÍSTICA | 67 | 32% |
| PRODUCCIÓN | 18 | 9% |
| PESCADERÍA | 6 | 3% |
| ADMINISTRATIVO | 4 | 2% |
| GESTIÓN | 3 | 1% |
| SIN_CLASIFICAR | 110 | 53% |

---

## 6. Archivos del Sistema

```
cv-extractor/
├── extract_cvs.py       # Extractor de PDFs
├── clasificador.py      # Clasificador por perfiles
├── db_loader.py         # Cargador a MySQL
├── requirements.txt     # Dependencias Python
├── .env                 # Configuración BD
└── docs/
    └── FLUJO_SELECCION.md  # Este documento
```

---

*Última actualización: 2026-02-17*

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
| 7 | B | Carnet B (S/N) | TINYINT |
| 8 | C | Carnet C (S/N) | TINYINT |
| 9 | CAP | Certificado CAP (S/N) | TINYINT |
| 10 | Carr | Carnet Carretillero (S/N) | TINYINT |
| 11 | Puesto | Perfil asignado segun keywords | VARCHAR |
| 12 | Exp | Anos de experiencia total | DECIMAL |
| 13 | Estudios | Estudios reglados | VARCHAR |
| 14 | CV | Enlace al curriculum detallado | TEXT |
| 15 | Entrevista | Desplegable Si/No | ENUM |

---

## 2. Ejemplo Visual

```
PESCADERIA (7)
ID |Nombre   |Apellido|Telefono   |Email               |Localid|B|C|CAP|Car|Puesto  |Exp |Est|CV |Entr
---|---------|--------|-----------|--------------------| ------|–|–|---|---|--------|----| –-|---|----
 65|Adela    |Ruano   |675 942 449|adelaruano1269@gmai |Cordoba|S|N|N  |N  |PESCADE |20.3|-  |[+]|[ v]
180|Mari     |Carmen  |654 728 707|mc_gar@yahoo.es     |Lucena |S|N|N  |N  |PESCADE |13.0|-  |[+]|[ v]
103|Angela   |Navarro |622-52-80-9|angelanavex@gmail.c |Cordoba|N|N|N  |N  |PESCADE | 5.3|-  |[+]|[ v]
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

Los candidatos sin perfil asignado siguen este proceso:

1. **Se aplican los filtros automaticos** (experiencia < 1 año, distancia > 40 km)
2. **Si NO pasan** → Van a Descartados con motivo automatico
3. **Si PASAN** → Se quedan en "Pendientes Asignar" hasta ser clasificados manualmente

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

*Documento generado: 2026-02-17*

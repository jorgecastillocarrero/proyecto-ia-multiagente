# Especificacion Tecnica: Dashboard de Seleccion RRHH

**Pescados La Carihuela**
**Fecha**: 2026-02-17
**Estado**: Pendiente de desarrollo
**Responsable desarrollo**: Por asignar

---

## 1. Objetivo

Crear un panel visual (dashboard) que muestre el estado de los candidatos organizados por perfil profesional, permitiendo una vision rapida del proceso de seleccion.

---

## 2. Diseño Visual del Dashboard

### 2.1 Vista Principal - Cuadros por Perfil

```
+============================================================================+
|              DASHBOARD SELECCION RRHH - PESCADOS LA CARIHUELA              |
+============================================================================+

+---------------------------+  +---------------------------+  +---------------------------+
|        PESCADERIA         |  |         LOGISTICA         |  |        PRODUCCION         |
+---------------------------+  +---------------------------+  +---------------------------+
|  Total:              7    |  |  Total:             67    |  |  Total:             18    |
|  Nuevos:             6    |  |  Nuevos:            49    |  |  Nuevos:            18    |
|  Entrevistando:      1    |  |  Entrevistando:     18    |  |  Entrevistando:      0    |
|  Contratados:        0    |  |  Contratados:        0    |  |  Contratados:        0    |
|  Descartados:        0    |  |  Descartados:        0    |  |  Descartados:        0    |
+---------------------------+  +---------------------------+  +---------------------------+

+---------------------------+  +---------------------------+  +---------------------------+
|      ADMINISTRATIVO       |  |          GESTION          |  |    PENDIENTES ASIGNAR     |
+---------------------------+  +---------------------------+  +---------------------------+
|  Total:              4    |  |  Total:              0    |  |  Total:            112    |
|  Nuevos:             4    |  |  Nuevos:             0    |  |  Nuevos:           106    |
|  Entrevistando:      0    |  |  Entrevistando:      0    |  |  Entrevistando:      6    |
|  Contratados:        0    |  |  Contratados:        0    |  |  Contratados:        0    |
|  Descartados:        0    |  |  Descartados:        0    |  |  Descartados:        0    |
+---------------------------+  +---------------------------+  +---------------------------+

+============================================================================+
|  TOTAL CANDIDATOS EN SISTEMA: 208                                          |
+============================================================================+
```

### 2.2 Colores Sugeridos

| Perfil | Color de fondo | Color texto |
|--------|----------------|-------------|
| PESCADERIA | Azul claro (#E3F2FD) | Azul (#1565C0) |
| LOGISTICA | Naranja claro (#FFF3E0) | Naranja (#E65100) |
| PRODUCCION | Verde claro (#E8F5E9) | Verde (#2E7D32) |
| ADMINISTRATIVO | Morado claro (#F3E5F5) | Morado (#7B1FA2) |
| GESTION | Gris claro (#ECEFF1) | Gris (#455A64) |
| PENDIENTES | Rojo claro (#FFEBEE) | Rojo (#C62828) |

---

## 3. Funcionalidades Requeridas

### 3.1 Vista Dashboard (Pantalla Principal)

| Funcionalidad | Descripcion | Prioridad |
|---------------|-------------|-----------|
| Mostrar cuadros | Un cuadro por cada perfil con estadisticas | Alta |
| Actualizar en tiempo real | Refrescar datos cada 30 segundos | Media |
| Click en cuadro | Navegar al detalle del perfil | Alta |
| Total general | Mostrar total de candidatos al final | Alta |

### 3.2 Vista Detalle de Perfil (al hacer click en cuadro)

```
+============================================================================+
|  PERFIL: PESCADERIA                                                        |
+============================================================================+
|  Descripcion: Pescaderia, carniceria, comercio, dependiente de tienda      |
|  Keywords: pescad, carnicer, dependient, tienda, comercio                  |
+----------------------------------------------------------------------------+
|  Total: 7  |  Nuevos: 6  |  Entrevistando: 1  |  Contratados: 0            |
+============================================================================+

+------+---------------------------+---------------------------+-------+--------+
|  ID  | Nombre                    | Puesto                    |  Exp  | Estado |
+------+---------------------------+---------------------------+-------+--------+
|  65  | Adela Ruano               | Dependiente/a de tienda   | 20.3  | NUEVO  |
| 180  | Mari Carmen               | Dependiente/a de tienda   | 13.0  | NUEVO  |
| 103  | Angela Navarro            | RESPONSABLE DE TIENDA     |  5.3  | ENTRV  |
|  43  | Manuel david              | Repartidor y dependiente  |  2.1  | NUEVO  |
|  87  | Juan jesus                | Dependiente/a de tienda   |  1.8  | NUEVO  |
| 183  | Maria Del                 | Dependiente/a de tienda   |  1.1  | NUEVO  |
| 122  | Rafael Morales            | Responsable de tienda     |  0.0  | NUEVO  |
+------+---------------------------+---------------------------+-------+--------+

[ Volver al Dashboard ]  [ Exportar Excel ]  [ Filtrar ]
```

### 3.3 Acciones por Candidato

| Accion | Descripcion |
|--------|-------------|
| Ver detalle | Abrir ficha completa del candidato |
| Cambiar perfil | Reasignar a otro perfil |
| Cambiar estado | NUEVO -> ENTREVISTANDO -> CONTRATADO/DESCARTADO |
| Descartar | Abrir dialogo para seleccionar motivo de descarte |

---

## 4. Consultas SQL Necesarias

### 4.1 Obtener datos para cuadros del dashboard

```sql
SELECT
    COALESCE(perfil_codigo, 'SIN_ASIGNAR') as perfil,
    COUNT(*) as total,
    SUM(CASE WHEN estado_global = 'NUEVO' THEN 1 ELSE 0 END) as nuevos,
    SUM(CASE WHEN estado_global = 'ENTREVISTANDO' THEN 1 ELSE 0 END) as entrevistando,
    SUM(CASE WHEN estado_global = 'CONTRATADO' THEN 1 ELSE 0 END) as contratados,
    SUM(CASE WHEN estado_global = 'DESCARTADO' THEN 1 ELSE 0 END) as descartados
FROM candidatos
GROUP BY perfil_codigo
ORDER BY total DESC;
```

### 4.2 Obtener candidatos de un perfil

```sql
SELECT
    id,
    CONCAT(nombre, ' ', apellido1) as nombre_completo,
    puesto_actual,
    anos_experiencia,
    estado_global
FROM candidatos
WHERE perfil_codigo = 'PESCADERIA'
ORDER BY anos_experiencia DESC;
```

### 4.3 Obtener datos de un perfil

```sql
SELECT id, codigo, nombre, descripcion, keywords
FROM perfiles
WHERE codigo = 'PESCADERIA';
```

---

## 5. Endpoints API Requeridos (Backend)

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | /api/dashboard/resumen | Obtener datos para todos los cuadros |
| GET | /api/perfiles | Listar todos los perfiles |
| GET | /api/perfiles/:codigo | Detalle de un perfil con candidatos |
| GET | /api/candidatos/:id | Detalle de un candidato |
| PUT | /api/candidatos/:id/perfil | Cambiar perfil de un candidato |
| PUT | /api/candidatos/:id/estado | Cambiar estado de un candidato |
| POST | /api/candidatos/:id/descartar | Descartar candidato con motivo |

### 5.1 Ejemplo respuesta GET /api/dashboard/resumen

```json
{
  "perfiles": [
    {
      "codigo": "PESCADERIA",
      "nombre": "Pescaderia",
      "total": 7,
      "nuevos": 6,
      "entrevistando": 1,
      "contratados": 0,
      "descartados": 0
    },
    {
      "codigo": "LOGISTICA",
      "nombre": "Logistica",
      "total": 67,
      "nuevos": 49,
      "entrevistando": 18,
      "contratados": 0,
      "descartados": 0
    }
  ],
  "total_candidatos": 208,
  "pendientes_asignar": 112
}
```

---

## 6. Tecnologias Sugeridas

| Componente | Tecnologia |
|------------|------------|
| Frontend | Angular (existente en el proyecto) |
| Backend | Node.js + Express (existente) |
| Base de datos | MySQL 8.0 |
| Estilos | Angular Material / Bootstrap |

---

## 7. Criterios de Aceptacion

- [ ] Dashboard muestra 6 cuadros (5 perfiles + pendientes)
- [ ] Cada cuadro muestra: total, nuevos, entrevistando, contratados, descartados
- [ ] Click en cuadro navega al detalle del perfil
- [ ] Detalle muestra lista de candidatos ordenados por experiencia
- [ ] Se puede cambiar el estado de un candidato
- [ ] Se puede descartar un candidato con motivo
- [ ] Datos se actualizan sin recargar pagina

---

## 8. Datos de Prueba Actuales

| Perfil | Total | Nuevos | Entrevistando |
|--------|-------|--------|---------------|
| LOGISTICA | 67 | 49 | 18 |
| PRODUCCION | 18 | 18 | 0 |
| PESCADERIA | 7 | 6 | 1 |
| ADMINISTRATIVO | 4 | 4 | 0 |
| GESTION | 0 | 0 | 0 |
| PENDIENTES | 112 | 106 | 6 |
| **TOTAL** | **208** | | |

---

*Documento preparado para aprobacion*

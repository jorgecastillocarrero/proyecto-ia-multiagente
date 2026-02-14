# Proyecto IA Multi-Agente - Pescados La Carihuela

## Resumen del Proyecto

Sistema de inteligencia artificial multi-agente para empresa de retail/comercio del sector pesquero. Integra con ERP existente en Laravel para automatizar procesos, generar alertas inteligentes y proporcionar asistencia conversacional.

---

## Arquitectura General

### Stack Tecnologico

| Capa | Tecnologia | Funcion |
|------|------------|---------|
| **Frontend Existente** | Blade + jQuery | ERP actual para operarios |
| **Frontend Nuevo** | Vue.js 3 + Inertia.js | 11 apps especificas por departamento |
| **Backend ERP** | Laravel 11 | API REST, CRUD, autenticacion |
| **Backend IA** | FastAPI (Python) | Gateway de agentes, ML |
| **LLM Local** | Ollama + Mistral 7B | Procesamiento lenguaje natural |
| **BD Operativa** | MySQL | Datos ERP (ventas, stock, empleados) |
| **BD Analitica** | PostgreSQL | Datos IA (metricas, alertas, candidatos) |
| **BD Vectorial** | ChromaDB | Embeddings de documentos |
| **Cache/Mensajes** | Redis | Alertas tiempo real, colas |
| **Notificaciones** | Laravel Echo + WebSocket | Push en tiempo real |

### Agentes IA

1. **Agente Asistente**: Chat conversacional, consultas en lenguaje natural
2. **Agente Alertas**: Monitoreo proactivo, notificaciones inteligentes
3. **Agente Automatizacion**: Workflows, acciones automaticas
4. **Agente Predictivo**: ML, prediccion demanda, tendencias
5. **Agente Documentos**: Extraccion texto, OCR, embeddings

---

## 11 Frontends por Departamento

| # | Frontend | Ruta | Funciones Principales |
|---|----------|------|----------------------|
| 1 | RRHH | /rrhh/* | CVs, entrevistas, nominas |
| 2 | Administrativo | /admin/* | Facturas, pagos, cobros |
| 3 | Tiendas | /tiendas/* | Ventas, stock, pedidos |
| 4 | Logistica | /logistica/* | Rutas, entregas, tracking |
| 5 | Compras | /compras/* | Proveedores, ordenes |
| 6 | Comercial | /comercial/* | Clientes, ofertas, visitas |
| 7 | Calidad | /calidad/* | Controles, incidencias |
| 8 | Almacen | /almacen/* | Entradas, salidas, inventario |
| 9 | Contabilidad | /contabilidad/* | Asientos, balances |
| 10 | Produccion | /produccion/* | Elaborados, recetas, costes |
| 11 | Gerencia | /gerencia/* | Dashboards, KPIs, predicciones |

---

## Bases de Datos

### MySQL (ERP Existente)
- trabajadores
- trabajadores_antiguos
- registro_horario
- nominas
- vacantes
- ventas
- productos
- clientes
- facturas
- stock

### PostgreSQL (Sistema IA Nuevo)
- candidatos
- cvs_documentos
- proceso_seleccion
- llamadas
- entrevistas
- alertas
- metricas
- predicciones

### ChromaDB (Vectores)
- Embeddings de CVs
- Embeddings de documentos
- Busqueda semantica

### Redis (Cache)
- Sesiones
- Alertas tiempo real
- Colas de mensajes

---

## Flujo RRHH Detallado (Seccion 18 del PDF)

### Fases del Proceso de Seleccion

| Fase | Descripcion | Automatizacion | BD Principal |
|------|-------------|----------------|--------------|
| 1. Entrada CVs | Recepcion por email/web/API | 100% automatica | PostgreSQL |
| 2. Primera Criba | Filtro por criterios minimos | 100% automatica | MySQL + PG |
| 3. Segunda Criba | Revision manual con ayuda IA | Semi-automatica | MySQL + PG |
| 4. Llamadas | Contacto con candidatos | Manual + alertas | PostgreSQL |
| 5. Entrevistas | Evaluacion y decision | Manual | MySQL + PG |
| 6. Reactivacion | Recuperar candidatos del pool | 70% automatica | MySQL + PG |

### Integracion MySQL en RRHH

- **Verificar empleado**: Consulta si candidato ya trabaja o trabajo antes
- **Consultar salarios**: Para preparar oferta economica
- **Crear empleado**: INSERT en trabajadores al contratar
- **Crear nomina**: INSERT en nominas al contratar
- **Detectar vacantes**: Trigger desde tabla vacantes del ERP

---

## Archivos del Proyecto

| Archivo | Descripcion |
|---------|-------------|
| `generar_pdf_agentes.py` | Script Python para generar PDF de documentacion |
| `Proyecto_IA_MultiAgente_v6.pdf` | Documentacion completa (18 secciones) |
| `PROYECTO_IA_MULTIAGENTE.md` | Este archivo de contexto |

---

## Secciones del PDF v6

1. Vision General de la Arquitectura
2. Agente Asistente
3. Agente de Alertas
4. Agente de Automatizaciones
5. Agente Predictivo
6. Integracion con ERP Laravel
7. Stack Tecnologico Recomendado
8. Roadmap de Implementacion
9. Tipos de Agentes IA (Guia General)
10. Matriz de Recomendaciones
11. Cuadro: Usuarios, Frontend y Backend
12. Cuadro: Eventos, Acciones y Bases de Datos
13. Cuadro: Agentes IA y Tipos de Busqueda
14. Ejemplos Practicos de Alertas
15. Frontends Especificos por Departamento
16. Compatibilidad Movil (PWA)
17. Flujos de Trabajo y Comunicacion
18. Analisis Flujo RRHH - Sistema de Seleccion
    - 18.1 Vision General del Proceso
    - 18.2 Fase 1: Entrada de CVs
    - 18.3 Fase 2: Primera Criba
    - 18.4 Fase 3: Segunda Criba
    - 18.5 Fase 4: Llamadas
    - 18.6 Fase 5: Entrevistas
    - 18.7 Fase 6: Reactivacion
    - 18.8 Integracion MySQL y PostgreSQL
    - 18.9 Resumen Stack por Fase
    - 18.10 Metricas y KPIs
    - 18.11 Pantallas del Frontend RRHH
    - 18.12 Detalle de Cada Pantalla
    - 18.13 Widgets Comunes
    - 18.14 Actividades por Trabajador
    - 18.15 Resumen por Rol

---

## Como Continuar

Para retomar el proyecto, indica a Claude:

```
Lee el archivo PROYECTO_IA_MULTIAGENTE.md y el script generar_pdf_agentes.py
para continuar con el proyecto de IA Multi-Agente.
```

### Proximos Pasos Sugeridos

1. **Disenar otro flujo de trabajo** (ej: Compras, Logistica, Ventas)
2. **Crear mockups** de las pantallas Vue.js
3. **Definir API endpoints** de Laravel y FastAPI
4. **Crear esquema de base de datos** detallado
5. **Implementar primer agente** (Asistente o Alertas)

---

## Notas Tecnicas

- **PWA**: Todos los frontends seran compatibles con movil via PWA
- **Sincronizacion**: MySQL -> PostgreSQL via eventos Laravel
- **Alertas**: Persistentes hasta resolucion, con progreso X/Y
- **LLM Local**: Mistral 7B en Ollama para privacidad de datos

---

*Documento generado con asistencia de Claude AI - Febrero 2025*

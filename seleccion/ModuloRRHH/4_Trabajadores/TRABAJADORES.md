# MODULO RRHH - TRABAJADORES

## 1. Clasificacion de Trabajadores (4 Niveles)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ NIVEL 1: TRABAJADORES CON CONTRATO                                         │
│ Todos con contrato en vigor (incluidos excedencia)                          │
└─────────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼ (menos excedencias)
┌─────────────────────────────────────────────────────────────────────────────┐
│ NIVEL 2: TRABAJADORES ACTUALES                                              │
│ Sin excedencia                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼ (menos baja larga duracion)
┌─────────────────────────────────────────────────────────────────────────────┐
│ NIVEL 3: ELEGIBLES VACACIONES                                               │
│ Sin baja larga duracion → Selector de vacaciones                            │
│ (Paternidad/maternidad SI son elegibles)                                    │
└─────────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼ (menos paternidad/mat. + vacaciones + baja corta + permisos)
┌─────────────────────────────────────────────────────────────────────────────┐
│ NIVEL 4: CUADRANTE / CONTROL DE PRESENCIA                                   │
│ Disponibles para trabajar el dia seleccionado                               │
│ (PENDIENTE DE DESARROLLO)                                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

| Nivel | Nombre | Excluye | Uso |
|-------|--------|---------|-----|
| 1 | Trabajadores con Contrato | - | Base |
| 2 | Trabajadores Actuales | Excedencia | General |
| 3 | Elegibles Vacaciones | Baja larga | Selector vacaciones |
| 4 | Cuadrante/Control Presencia | Patern/matern, vacaciones, baja corta, permisos | Horarios |

---

## 2. Definicion de Trabajador Activo

Un trabajador se considera "dado de alta" o "con contrato en vigor" cuando tiene un registro activo en la tabla `contratos_usuario` que cumple:

- El contrato no ha sido eliminado (`deleted_at IS NULL`)
- La fecha de fin es nula (contrato indefinido) o es igual o posterior a la fecha actual (`fecha_fin IS NULL OR fecha_fin >= CURDATE()`)

---

## 3. Gestion de Ausencias

### 3.1 Tablas de Ausencias

| Tabla | Descripcion |
|-------|-------------|
| `nuevo_carihuela_jorge_excedencia` | Excedencias voluntarias |
| `nuevo_carihuela_jorge_bajas_larga_duracion` | Bajas con sustituto asignado |
| `nuevo_carihuela_jorge_paternidad_maternidad` | Permisos paternidad/maternidad |
| `nuevo_carihuela_jorge_lactancia` | Permisos de lactancia |

---

## 4. Bajas de Larga Duracion

### 4.1 Definicion

| Tipo de Baja | Condicion |
|--------------|-----------|
| **Corta duracion** | < 30 dias naturales |
| **Larga duracion** | >= 30 dias naturales |

**Nota:** A partir del dia 30 de baja, se considera automaticamente como baja de larga duracion.

### 4.2 Alerta Automatica (>=30 dias)

Cuando un trabajador lleva **30 dias o mas de baja**, el sistema genera una **alerta automatica**:

| Campo | Valor |
|-------|-------|
| **Condicion** | Trabajador con >=30 dias de baja sin sustituto asignado |
| **Mensaje** | "El trabajador [Nombre] lleva 30 dias de baja y deberia tener un sustituto" |
| **Destinatario** | Hermi (por correo electronico) |
| **Otros destinatarios** | Pendiente de definir |
| **Frecuencia** | Diaria hasta que se asigne sustituto |

```
+============================================================================+
|  [!] ALERTA - BAJA LARGA DURACION SIN SUSTITUTO                            |
+============================================================================+
|                                                                             |
|  El trabajador Francisco Cabello (097) lleva 30 dias de baja.              |
|  Fecha inicio baja: 19/09/2025                                              |
|  Dias de baja: 30                                                           |
|                                                                             |
|  ACCION REQUERIDA: Asignar sustituto                                        |
|                                                                             |
|  [Asignar sustituto]  [Ver detalle]                                         |
|                                                                             |
+============================================================================+
```

### 4.3 Tabla de Bajas Larga Duracion Actuales

```
┌────┬─────┬──────────────────────────┬─────┬──────────────────────────┬────────────┐
│ ID │ Cod │ Trabajador en Baja       │ Cod │ Sustituto                │ Desde      │
├────┼─────┼──────────────────────────┼─────┼──────────────────────────┼────────────┤
│ 1  │ 097 │ Francisco Cabello        │ 216 │ Maria Leon               │ 19/09/2025 │
├────┼─────┼──────────────────────────┼─────┼──────────────────────────┼────────────┤
│ 3  │ 038 │ Soledad Leon             │ 259 │ Hugo Aguilar             │ 29/09/2025 │
├────┼─────┼──────────────────────────┼─────┼──────────────────────────┼────────────┤
│ 4  │ 005 │ Fernando Rafael Torralbo │ 258 │ Angel Encinas            │ 13/11/2025 │
├────┼─────┼──────────────────────────┼─────┼──────────────────────────┼────────────┤
│ 2  │ 078 │ Monica Quesada           │ 255 │ Alejandro Leon           │ 02/01/2026 │
└────┴─────┴──────────────────────────┴─────┴──────────────────────────┴────────────┘
```

### 4.4 Estructura Tabla Base de Datos

Tabla: `nuevo_carihuela_jorge_bajas_larga_duracion`

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| id | INT | Identificador unico |
| id_trabajador | INT | Codigo del trabajador en baja |
| id_sustituto | INT | Codigo del sustituto asignado |
| fecha_desde | DATE | Fecha inicio de la baja |
| fecha_hasta | DATE NULL | Fecha fin (NULL si continua) |
| motivo | VARCHAR | Motivo de la baja |
| observaciones | TEXT | Observaciones adicionales |

### 4.5 Notas Importantes

- Las bajas de larga duracion (>= 30 dias) requieren asignacion de sustituto
- El trabajador en baja larga NO es elegible para el selector de vacaciones (Nivel 3)
- Al registrar una baja larga, se cancelan automaticamente las vacaciones planificadas
- El sustituto debe tener un contrato de sustitucion vinculado al trabajador en baja

---

## 5. Bajas Corta Duracion

Las bajas de corta duracion se gestionan a traves del **Control de Presencia** en la tabla `eventos_incidencias_colores`:

| ID | Nombre | Iniciales |
|----|--------|-----------|
| 66 | Baja | Baj |
| 68 | Baja S/Justificar | Bsj |
| 67 | Trabajado (Sin Ticada) | Tst |
| 65 | Vacaciones | Vac |

**Nota:** "Baja" (id 66) corresponde a **Baja Corta Duracion**.

---

## 6. Excedencias

### 6.1 Excedencias Actuales

```
┌─────┬─────────────────────────────┬────────────┬────────────┬───────────────────────┐
│ Cod │ Nombre Completo             │ Desde      │ Hasta      │ Tipo                  │
├─────┼─────────────────────────────┼────────────┼────────────┼───────────────────────┤
│ 280 │ Pedro Moya Moya             │ 25/03/2025 │ 25/03/2026 │ Excedencia voluntaria │
├─────┼─────────────────────────────┼────────────┼────────────┼───────────────────────┤
│ 077 │ Pablo Javier Nunez Fierro   │ 31/05/2025 │ 31/05/2026 │ Excedencia voluntaria │
├─────┼─────────────────────────────┼────────────┼────────────┼───────────────────────┤
│ 011 │ Jose Maria Aguilar Serrano  │ 03/09/2025 │ 03/09/2026 │ Excedencia voluntaria │
├─────┼─────────────────────────────┼────────────┼────────────┼───────────────────────┤
│ 050 │ Francisco Luz Romero        │ 31/10/2025 │ 31/10/2026 │ Excedencia voluntaria │
└─────┴─────────────────────────────┴────────────┴────────────┴───────────────────────┘
```

---

## 7. Paternidad/Maternidad

### 7.1 Estructura

- Fecha de nacimiento del hijo
- Periodo obligatorio: 6 semanas desde nacimiento
- Periodo optativo: 13 semanas (a disfrutar antes de que el hijo cumpla 1 año)
- Total: 19 semanas

---

## 8. Lactancia

### 8.1 Tipos disponibles

| Tipo | Descripcion |
|------|-------------|
| AUSENCIA_1_HORA | Ausencia de 1 hora diaria |
| REDUCCION_JORNADA | Reduccion de jornada |
| ACUMULACION_DIAS | Acumulacion de dias completos |

---

## 9. Vacaciones

### 9.1 Tipos

| Tipo | Descripcion |
|------|-------------|
| INVIERNO | Vacaciones periodo invernal |
| VERANO | Vacaciones periodo estival |

### 9.2 Estados

| Estado | Descripcion |
|--------|-------------|
| PENDIENTE | Solicitud enviada, pendiente de aprobacion |
| APROBADA | Vacaciones aprobadas |
| RECHAZADA | Solicitud rechazada |
| CANCELADA | Vacaciones canceladas |

### 9.3 Balance Anual

- Dias correspondientes: 30 dias/año
- Dias invierno: Segun solicitud
- Dias verano: Segun solicitud
- Dias pendientes: Calculado automaticamente

---

## 10. Representantes Sindicales

### 10.1 Representantes Actuales

| Codigo | Nombre | Sindicato |
|--------|--------|-----------|
| 110 | Alejandro Moreno | UGT |
| 019 | Silvia Sierra | UGT |
| 164 | Clara Munoz | CCOO |
| 094 | Rafael Espejo | INDEPENDIENTE |
| 160 | Carlos Fernandez | INDEPENDIENTE |

### 10.2 Horas Sindicales

Los representantes sindicales tienen derecho a horas de credito horario sindical que se registran mensualmente.

---

## 11. Jornada Laboral

### 11.1 Distribucion

| Horas/semana | Trabajadores |
|--------------|-------------|
| 40 horas | 67 |
| 28 horas | 3 |
| 24 horas | 1 |

---

## 12. Categorias Profesionales

### 12.1 Distribucion por grupos

| Grupo | Categoria | Total |
|-------|-----------|-------|
| I | Directores/as y Responsables Tecnicos | 5 |
| II | Administrativos (A-1, A-2) | 3 |
| III | Logistica (L-1, L-2, L-3) | 4 |
| IV | Pescaderia (P-2, P-3) | 7 |
| V | Tecnicos (T-0, T-1, T-2, T-3, Lider) | 52 |

---

*Documento generado: ModuloRRHH v1.0*

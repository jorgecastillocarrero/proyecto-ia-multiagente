# FLUJO DE TRABAJADORES CON CONTRATO EN VIGOR
## Módulo RRHH - Pescados La Carihuela

**Fecha:** 2026-02-17
**Elaborado por:** Jorge Castillo

---

## RESUMEN: Clasificación de Trabajadores (4 Niveles)

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
                              ▼ (menos baja larga duración)
┌─────────────────────────────────────────────────────────────────────────────┐
│ NIVEL 3: ELEGIBLES VACACIONES                                               │
│ Sin baja larga duración → Selector de vacaciones                            │
│ (Paternidad/maternidad SÍ son elegibles)                                    │
└─────────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼ (menos paternidad/mat. + vacaciones + baja corta + permisos + horas rep.)
┌─────────────────────────────────────────────────────────────────────────────┐
│ NIVEL 4: CUADRANTE / CONTROL DE PRESENCIA                                   │
│ Disponibles para trabajar el día seleccionado                               │
│ (PENDIENTE DE DESARROLLO)                                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

| Nivel | Nombre | Excluye | Uso |
|-------|--------|---------|-----|
| 1 | Trabajadores con Contrato | - | Base |
| 2 | Trabajadores Actuales | Excedencia | General |
| 3 | Elegibles Vacaciones | Baja larga | Selector vacaciones |
| 4 | Cuadrante/Control Presencia | Patern/matern, vacaciones, baja corta, permisos, horas rep. | Horarios (PENDIENTE) |

---

## Paso 1: Definición

Un trabajador se considera "dado de alta" o "con contrato en vigor" cuando tiene un registro activo en la tabla `contratos_usuario` que cumple las siguientes condiciones:

- El contrato no ha sido eliminado (`deleted_at IS NULL`)
- La fecha de fin es nula (contrato indefinido) o es igual o posterior a la fecha actual (`fecha_fin IS NULL OR fecha_fin >= CURDATE()`)

---

## Paso 2: Trabajadores con Contrato en Vigor

A continuación se muestra el listado completo de trabajadores que actualmente tienen contrato en vigor en la empresa.

---

## Paso 3: Tabla Principal de Trabajadores

```
┌─────┬──────────────────────────────┬────────────┬────────────┬─────┬─────┬─────────────────────────────────────┬─────────────────────────────┐
│ Cod │ Nombre                       │ Inicio     │ Fin        │ C.C │ Hrs │ Categoría                           │ Sustituye a                 │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 110 │ Alejandro Moreno             │ 01/08/2019 │ -          │ 100 │ 40  │ V.a.2. T-3                          │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 255 │ ALEJANDRO LEÓN               │ 02/01/2026 │ -          │ 410 │ 40  │ V.d T-0                             │ Mónica Quesada              │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 095 │ Alfredo David Ruiz           │ 10/01/2019 │ -          │ 189 │ 40  │ V.a.1. T3-Líder                     │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 236 │ ÁLVARO MUÑIZ                 │ 01/08/2024 │ -          │ 289 │ 24  │ V.a.2. T-3                          │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 063 │ Ana Belén Pérez              │ 22/08/2017 │ -          │ 189 │ 40  │ IV.A. P-3                           │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 181 │ ANA CRISTINA LEÓN            │ 31/05/2022 │ -          │ 100 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 258 │ ÁNGEL ENCINAS                │ 13/11/2025 │ -          │ 410 │ 40  │ V.c. T-1                            │ Fernando R. Torralbo        │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 122 │ ANGELICA ELISABEHT           │ 04/05/2020 │ -          │ 189 │ 40  │ IV.b P-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 217 │ ANTONIO ROMÁN                │ 17/07/2023 │ -          │ 100 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 074 │ Antonio Jose Carmona         │ 22/11/2017 │ -          │ 189 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 049 │ Antonio José Porras          │ 16/10/2018 │ -          │ 189 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 160 │ CARLOS FERNANDEZ             │ 07/09/2021 │ -          │ 189 │ 40  │ I.1.d. Director/a de Operaciones    │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 164 │ CLARA MUÑOZ                  │ 14/02/2022 │ -          │ 100 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 111 │ Cristina Moraleda            │ 08/05/2023 │ -          │ 100 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 182 │ DANIEL SOPEÑA                │ 26/09/2022 │ -          │ 100 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 002 │ Dolores Morales              │ 09/08/2007 │ -          │ 189 │ 40  │ I.2.d. Resp. Técnico Pescadería     │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 211 │ EMILIANA PATILLA             │ 08/11/2023 │ -          │ 100 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 033 │ Eva Serrano                  │ 10/04/2018 │ -          │ 100 │ 40  │ V.a.2. T-3                          │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 012 │ Eva María García             │ 02/09/2011 │ -          │ 100 │ 40  │ V.a.1. T3-Líder                     │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 005 │ Fernando Rafael Torralbo     │ 23/09/2006 │ -          │ 100 │ 40  │ V.a.2. T-3                          │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 097 │ Francisco Cabello            │ 11/02/2019 │ -          │ 189 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 050 │ Francisco Luz                │ 27/03/2017 │ -          │ 100 │ 40  │ I.2.b. Resp. Técnico Logística      │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 059 │ Francisco Soto               │ 11/07/2017 │ -          │ 189 │ 40  │ V.a.1. T3-Líder                     │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 176 │ FRANCISCO JAVIER ROMÁN       │ 03/01/2022 │ -          │ 100 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 042 │ Francisco José Boyer         │ 15/09/2016 │ -          │ 189 │ 40  │ III.a.1. L-3.1                      │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 272 │ Haydeé Lucia Maltez          │ 02/01/2026 │ 31/03/2026 │ 502 │ 28  │ V.d T-0                             │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 259 │ HUGO AGUILAR                 │ 29/09/2025 │ -          │ 410 │ 40  │ V.c. T-1                            │ Soledad León                │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 052 │ Inmaculada Pérez             │ 15/06/2018 │ -          │ 189 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 209 │ ISAAC MARCOS                 │ 01/08/2024 │ -          │ 189 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 227 │ JAVIER CARMONA               │ 08/09/2024 │ -          │ 189 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 106 │ Jessica Ramírez              │ 01/07/2019 │ -          │ 139 │ 40  │ V.c. T-1                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 219 │ JESUS GOMEZ                  │ 07/02/2023 │ -          │ 100 │ 40  │ 3.4. Operario de Logística          │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 559 │ JESÚS BERRAL                 │ 02/01/2026 │ 31/03/2026 │ 402 │ 40  │ III.b.2. L-2                        │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 016 │ Jesús Javier Raya            │ 10/05/2011 │ -          │ 189 │ 40  │ V.a.2. T-3                          │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 150 │ Jorge Castillo               │ 11/02/2026 │ -          │ 289 │ 40  │ I.1. Directores/as Técnicos         │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 257 │ JOSÉ ANTONIO VELASCO         │ 13/01/2026 │ 12/04/2026 │ 402 │ 40  │ V.c. T-1                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 011 │ José María Aguilar           │ 14/06/2010 │ -          │ 189 │ 40  │ III.a.2. L-3.2                      │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 084 │ Josefa Bellido               │ 26/06/2018 │ -          │ 189 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 028 │ Juan David Molero            │ 01/12/2014 │ -          │ 100 │ 40  │ V.a.1. T3-Líder                     │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 055 │ Juan José Torres             │ 27/06/2017 │ -          │ 189 │ 40  │ V.a.2. T-3                          │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 104 │ Juan Manuel Cervantes        │ 17/06/2019 │ -          │ 189 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 041 │ Laura Flores                 │ 11/06/2016 │ -          │ 189 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 029 │ Manuel Solar                 │ 25/02/2016 │ -          │ 100 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 216 │ MARIA LEÓN                   │ 19/09/2025 │ -          │ 410 │ 40  │ IV.b P-2                            │ Francisco Cabello           │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 021 │ María Ángeles Medina         │ 18/09/2012 │ -          │ 189 │ 40  │ V.a.1. T3-Líder                     │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 030 │ María Ángeles Muñoz          │ 22/02/2016 │ -          │ 100 │ 40  │ V.a.2. T-3                          │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 079 │ María Cristina Martínez      │ 03/05/2018 │ -          │ 189 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 071 │ María del Puerto Navarro     │ 01/12/2017 │ -          │ 189 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 0   │ María José Castillo          │ 22/10/2013 │ -          │ 189 │ 40  │ V.a.1. T3-Líder                     │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 184 │ MARIA JOSE BERNIER           │ 09/06/2022 │ -          │ 100 │ 40  │ IV.b P-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 020 │ Miguel Ángel Ruiz            │ 01/07/2014 │ -          │ 200 │ 28  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 009 │ Miguel Ángel Heredia         │ 02/01/2009 │ -          │ 189 │ 40  │ V.a.2. T-3                          │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 078 │ Mónica Quesada               │ 02/05/2018 │ -          │ 189 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 234 │ NATIVIDAD FERNÁNDEZ          │ 02/01/2026 │ 30/06/2026 │ 402 │ 40  │ II.c. A-1                           │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 213 │ NICOLAS CASTRO               │ 12/06/2023 │ -          │ 189 │ 40  │ V.a.2. T-3                          │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 077 │ Pablo Javier Nuñez           │ 01/06/2020 │ -          │ 189 │ 40  │ V.a.2. T-3                          │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 010 │ Pedro Molina                 │ 21/01/2009 │ -          │ 189 │ 40  │ I.2.d. Resp. Técnico Pescadería     │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 280 │ Pedro Moya                   │ 01/01/2020 │ -          │ 189 │ 40  │ V.a.2. T-3                          │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 126 │ RAFAEL DUARTE                │ 10/08/2020 │ -          │ 189 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 094 │ Rafael Espejo                │ 20/11/2018 │ -          │ 189 │ 40  │ V.a.2. T-3                          │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 250 │ RAFAEL UCLES                 │ 02/01/2025 │ -          │ 100 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 162 │ ROCIO ISABEL GARCIA          │ 16/06/2022 │ -          │ 100 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 047 │ Rosario López                │ 03/05/2018 │ -          │ 189 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 019 │ Silvia Sierra                │ 19/11/2014 │ -          │ 200 │ 28  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 038 │ Soledad León                 │ 17/09/2018 │ -          │ 100 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 224 │ SONIA GATA                   │ 03/07/2024 │ -          │ 189 │ 40  │ II.b. A-2                           │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 266 │ TOMÁS CABANILLAS             │ 02/01/2026 │ 31/03/2026 │ 402 │ 40  │ III.c. L-1                          │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 024 │ Virginia Jiménez             │ 01/01/2017 │ -          │ 189 │ 40  │ V.b. T-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 064 │ Virtudes Osuna               │ 01/09/2017 │ -          │ 139 │ 40  │ IV.b P-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 062 │ Yesica Muñoz                 │ 03/08/2017 │ -          │ 189 │ 40  │ IV.b P-2                            │                             │
├─────┼──────────────────────────────┼────────────┼────────────┼─────┼─────┼─────────────────────────────────────┼─────────────────────────────┤
│ 247 │ YOLANDA DEL FRESNO           │ 18/11/2024 │ -          │ 189 │ 40  │ V.b. T-2                            │                             │
└─────┴──────────────────────────────┴────────────┴────────────┴─────┴─────┴─────────────────────────────────────┴─────────────────────────────┘

Total: 71 trabajadores con contrato en vigor
```

---

## Paso 4: Trabajadores en Excedencia

Los siguientes trabajadores se encuentran actualmente en situación de excedencia voluntaria:

```
┌─────┬─────────────────────────────┬────────────┬────────────┬───────────────────────┐
│ Cod │ Nombre Completo             │ Desde      │ Hasta      │ Tipo                  │
├─────┼─────────────────────────────┼────────────┼────────────┼───────────────────────┤
│ 280 │ Pedro Moya Moya             │ 25/03/2025 │ 25/03/2026 │ Excedencia voluntaria │
├─────┼─────────────────────────────┼────────────┼────────────┼───────────────────────┤
│ 077 │ Pablo Javier Nuñez Fierro   │ 31/05/2025 │ 31/05/2026 │ Excedencia voluntaria │
├─────┼─────────────────────────────┼────────────┼────────────┼───────────────────────┤
│ 011 │ José María Aguilar Serrano  │ 03/09/2025 │ 03/09/2026 │ Excedencia voluntaria │
├─────┼─────────────────────────────┼────────────┼────────────┼───────────────────────┤
│ 050 │ Francisco Luz Romero        │ 31/10/2025 │ 31/10/2026 │ Excedencia voluntaria │
└─────┴─────────────────────────────┴────────────┴────────────┴───────────────────────┘

Total: 4 trabajadores en excedencia
```

---

## Paso 5: Jornada Laboral

**Jornadas parciales:**

```
┌─────┬─────────────────────────────┬───────┐
│ Cod │ Nombre                      │ Horas │
├─────┼─────────────────────────────┼───────┤
│ 236 │ ÁLVARO MUÑIZ CASTILLO       │ 24    │
├─────┼─────────────────────────────┼───────┤
│ 272 │ Haydeé Lucia Maltez         │ 28    │
├─────┼─────────────────────────────┼───────┤
│ 019 │ Silvia Sierra Sánchez       │ 28    │
├─────┼─────────────────────────────┼───────┤
│ 020 │ Miguel Ángel Ruiz Díaz      │ 28    │
└─────┴─────────────────────────────┴───────┘
```

**Resumen:**
- 40 horas/semana: 67 trabajadores
- 28 horas/semana: 3 trabajadores
- 24 horas/semana: 1 trabajador

---

## Paso 6: Categorías Profesionales

**Distribución por grupos:**

| Grupo | Categoría | Total |
|-------|-----------|-------|
| I | Directores/as y Responsables Técnicos | 5 |
| II | Administrativos (A-1, A-2) | 3 |
| III | Logística (L-1, L-2, L-3) | 4 |
| IV | Pescadería (P-2, P-3) | 7 |
| V | Técnicos (T-0, T-1, T-2, T-3, Líder) | 52 |

---

## Paso 7: Gestión de Ausencias

### 7.1 Tablas Creadas

| Tabla | Descripción | Registros |
|-------|-------------|-----------|
| `nuevo_carihuela_jorge_excedencia` | Excedencias voluntarias | 4 |
| `nuevo_carihuela_jorge_bajas_larga_duracion` | Bajas con sustituto asignado | 4 |
| `nuevo_carihuela_jorge_paternidad_maternidad` | Permisos paternidad/maternidad | 0 |
| `nuevo_carihuela_jorge_lactancia` | Permisos de lactancia | 0 |

### 7.1.1 Modificación tabla operadores

**Añadir campo nombre_corto:**
```sql
-- Añadir columna nombre_corto a la tabla operadores
ALTER TABLE operadores
ADD COLUMN nombre_corto VARCHAR(15) NULL
COMMENT 'Nombre abreviado para vacaciones y cuadrante (ej: A. Moreno)';

-- Actualizar nombre_corto para todos los trabajadores existentes
-- Formato: Primera inicial + Primer apellido
UPDATE operadores
SET nombre_corto = CONCAT(
    LEFT(nombre, 1), '. ',
    SUBSTRING_INDEX(apellidos, ' ', 1)
)
WHERE nombre_corto IS NULL;

-- Verificar resultados
SELECT codigo, nombre, apellidos, nombre_corto
FROM operadores
ORDER BY apellidos;
```

**Ejemplos de nombre_corto:**

| Código | Nombre | Apellidos | NomCorto |
|--------|--------|-----------|----------|
| 110 | Alejandro | Moreno Blanes | A. Moreno |
| 111 | Cristina | Moraleda Cerrato | C. Moraleda |
| 038 | Soledad | León Fernández | S. León |
| 097 | Francisco | Cabello Sánchez | F. Cabello |

### 7.2 Bajas Larga Duración (con sustituto)

```
┌────┬─────┬──────────────────────────┬─────┬──────────────────────────┬────────────┐
│ ID │ Cod │ Trabajador en Baja       │ Cod │ Sustituto                │ Desde      │
├────┼─────┼──────────────────────────┼─────┼──────────────────────────┼────────────┤
│ 1  │ 097 │ Francisco Cabello        │ 216 │ María León               │ 19/09/2025 │
├────┼─────┼──────────────────────────┼─────┼──────────────────────────┼────────────┤
│ 3  │ 038 │ Soledad León             │ 259 │ Hugo Aguilar             │ 29/09/2025 │
├────┼─────┼──────────────────────────┼─────┼──────────────────────────┼────────────┤
│ 4  │ 005 │ Fernando Rafael Torralbo │ 258 │ Ángel Encinas            │ 13/11/2025 │
├────┼─────┼──────────────────────────┼─────┼──────────────────────────┼────────────┤
│ 2  │ 078 │ Mónica Quesada           │ 255 │ Alejandro León           │ 02/01/2026 │
└────┴─────┴──────────────────────────┴─────┴──────────────────────────┴────────────┘
```

### 7.3 Paternidad/Maternidad

**Estructura de la tabla:**
- Fecha de nacimiento del hijo
- Periodo obligatorio: 6 semanas desde nacimiento
- Periodo optativo: 13 semanas (a disfrutar antes de que el hijo cumpla 1 año)
- Total: 19 semanas

**Estado:** Sin registros actuales

### 7.4 Lactancia

**Tipos disponibles:**
- AUSENCIA_1_HORA: Ausencia de 1 hora diaria
- REDUCCION_JORNADA: Reducción de jornada
- ACUMULACION_DIAS: Acumulación de días completos

**Estado:** Sin registros actuales

### 7.5 Bajas Corta Duración

Las bajas de corta duración se gestionan a través del **Control de Presencia** en la tabla `eventos_incidencias_colores`:

```
┌────┬───────────────────────┬───────────┐
│ ID │ Nombre                │ Iniciales │
├────┼───────────────────────┼───────────┤
│ 66 │ Baja                  │ Baj       │
│ 68 │ Baja S/Justificar     │ Bsj       │
│ 67 │ Trabajado (Sin Ticada)│ Tst       │
│ 65 │ Vacaciones            │ Vac       │
└────┴───────────────────────┴───────────┘
```

**Nota:** "Baja" (id 66) corresponde a **Baja Corta Duración**.

### 7.6 Pendiente de Desarrollo

**PENDIENTE PARA JEFE DE PROGRAMACIÓN:**

Relacionar la tabla `eventos_incidencias_colores` con las tablas de ausencias:
- Vincular con `nuevo_carihuela_jorge_bajas_larga_duracion`
- Vincular con `nuevo_carihuela_jorge_paternidad_maternidad`
- Vincular con `nuevo_carihuela_jorge_lactancia`
- Vincular con `nuevo_carihuela_jorge_excedencia`

---

## Paso 8: Representantes Sindicales

### 8.1 Representantes Actuales

| Código | Nombre | Sindicato |
|--------|--------|-----------|
| 110 | Alejandro Moreno | UGT |
| 019 | Silvia Sierra | UGT |
| 164 | Clara Muñoz | CCOO |
| 094 | Rafael Espejo | INDEPENDIENTE |
| 160 | Carlos Fernández | INDEPENDIENTE |

### 8.2 Horas Sindicales Consumidas

| Representante | Enero 2026 | Febrero 2026 |
|---------------|------------|--------------|
| Alejandro Moreno (UGT) | 14h | 7h |
| Clara Muñoz (CCOO) | 15h | 15h |
| Silvia Sierra (UGT) | 10h 20min | 10h 20min |
| Rafael Espejo (IND) | - | - |
| Carlos Fernández (IND) | - | - |

### 8.3 Automatización Pendiente

**PENDIENTE:** Automatizar la solicitud de crédito horario sindical mediante registro de email por cada sindicato:
- Email UGT → Registro automático para Alejandro Moreno y Silvia Sierra
- Email CCOO → Registro automático para Clara Muñoz
- Email representantes independientes → Registro automático para Rafael Espejo y Carlos Fernández

---

## Paso 9: Vacaciones

### 9.1 Estructura

**Tabla principal de vacaciones:**
```sql
CREATE TABLE nuevo_carihuela_jorge_vacaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    operador_id INT NOT NULL,
    tipo ENUM('INVIERNO', 'VERANO') NOT NULL,
    fecha_desde DATE NOT NULL,
    fecha_hasta DATE NOT NULL,
    dias INT NOT NULL COMMENT 'Calculado automáticamente',
    estado ENUM('PENDIENTE', 'APROBADA', 'RECHAZADA', 'CANCELADA') DEFAULT 'PENDIENTE',
    observaciones TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (operador_id) REFERENCES operadores(id),
    INDEX idx_operador (operador_id),
    INDEX idx_tipo (tipo),
    INDEX idx_fechas (fecha_desde, fecha_hasta),
    INDEX idx_estado (estado)
);

-- Trigger para calcular días automáticamente
DELIMITER //
CREATE TRIGGER trg_calcular_dias_vacaciones
BEFORE INSERT ON nuevo_carihuela_jorge_vacaciones
FOR EACH ROW
BEGIN
    SET NEW.dias = DATEDIFF(NEW.fecha_hasta, NEW.fecha_desde) + 1;
END //
DELIMITER ;
```

**Tabla de balance anual:**
```sql
CREATE TABLE nuevo_carihuela_jorge_vacaciones_balance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    operador_id INT NOT NULL,
    anio INT NOT NULL,
    dias_correspondientes INT NOT NULL DEFAULT 30,
    dias_invierno INT NOT NULL DEFAULT 0,
    dias_verano INT NOT NULL DEFAULT 0,
    dias_consumidos INT GENERATED ALWAYS AS (dias_invierno + dias_verano) STORED,
    dias_pendientes INT GENERATED ALWAYS AS (dias_correspondientes - dias_invierno - dias_verano) STORED,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (operador_id) REFERENCES operadores(id),
    UNIQUE KEY uk_operador_anio (operador_id, anio)
);
```

### 9.2 Reglas de Cálculo

**Reglas generales:**
- Trabajadores indefinidos: 30 días naturales por año
- Trabajadores temporales: proporcional al tiempo de contrato
- Las vacaciones siempre comienzan en día laboral (nunca en festivo)
- Redondeo: a partir de 0.5 se redondea al alza

**Exclusiones del calendario de vacaciones:**
- Los trabajadores en **excedencia activa** en la fecha de gestión NO aparecen en el calendario de vacaciones
- Los trabajadores en excedencia recuperan sus derechos cuando se reincorporen, **a partir de la fecha de incorporación** (el periodo de derecho comienza desde esa fecha, no desde el 01/01)

**Cancelación de vacaciones por incidencias:**

Si un trabajador tiene vacaciones asignadas y durante ese periodo se produce alguna de las siguientes situaciones, las vacaciones se cancelan y quedan **pendientes de reasignar**:

| Incidencia | Efecto |
|------------|--------|
| Baja larga duración | Vacaciones canceladas → Pendiente reasignar |
| Baja corta duración | Vacaciones canceladas → Pendiente reasignar |
| Paternidad/Maternidad | Vacaciones canceladas → Pendiente reasignar |
| Lactancia | Vacaciones canceladas → Pendiente reasignar |
| Otros permisos | Vacaciones canceladas → Pendiente reasignar |

**Excepciones - Esta regla NO aplica a:**
- **Representantes sindicales**: Sus horas sindicales son independientes de las vacaciones
- **Trabajadores en excedencia**: Ya están excluidos del calendario (no están en la empresa)

Tabla: `nuevo_carihuela_jorge_vacaciones_canceladas`
- Registra vacaciones canceladas por incidencias
- Estados: PENDIENTE_REASIGNAR, REASIGNADO, COMPENSADO
- Vincula con la incidencia que causó la cancelación

**Estructura de la tabla:**
```sql
CREATE TABLE nuevo_carihuela_jorge_vacaciones_canceladas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vacacion_original_id INT NOT NULL,
    operador_id INT NOT NULL,
    fecha_desde_original DATE NOT NULL,
    fecha_hasta_original DATE NOT NULL,
    dias_cancelados INT NOT NULL,
    motivo_cancelacion ENUM('BAJA_LARGA', 'BAJA_CORTA', 'PATERNIDAD_MATERNIDAD', 'PERMISO', 'OTRO') NOT NULL,
    incidencia_id INT NULL COMMENT 'ID de la incidencia que causó la cancelación',
    estado ENUM('PENDIENTE_REASIGNAR', 'REASIGNADO', 'COMPENSADO') DEFAULT 'PENDIENTE_REASIGNAR',
    fecha_cancelacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_reasignacion TIMESTAMP NULL,
    nueva_fecha_desde DATE NULL,
    nueva_fecha_hasta DATE NULL,
    observaciones TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (operador_id) REFERENCES operadores(id),
    INDEX idx_operador (operador_id),
    INDEX idx_estado (estado)
);
```

**Trigger para cancelación automática por baja larga:**
```sql
DELIMITER //

CREATE TRIGGER trg_cancelar_vacaciones_baja_larga
AFTER INSERT ON nuevo_carihuela_jorge_bajas_larga_duracion
FOR EACH ROW
BEGIN
    -- Registrar vacaciones canceladas
    INSERT INTO nuevo_carihuela_jorge_vacaciones_canceladas
        (vacacion_original_id, operador_id, fecha_desde_original, fecha_hasta_original,
         dias_cancelados, motivo_cancelacion, incidencia_id, estado)
    SELECT
        v.id, v.operador_id, v.fecha_desde, v.fecha_hasta,
        v.dias, 'BAJA_LARGA', NEW.id, 'PENDIENTE_REASIGNAR'
    FROM nuevo_carihuela_jorge_vacaciones v
    WHERE v.operador_id = NEW.operador_id
    AND v.fecha_desde >= NEW.fecha_desde
    AND v.estado = 'APROBADA';

    -- Actualizar estado de vacaciones originales a CANCELADA
    UPDATE nuevo_carihuela_jorge_vacaciones
    SET estado = 'CANCELADA',
        observaciones = CONCAT('Cancelada por baja larga desde ', DATE_FORMAT(NEW.fecha_desde, '%d/%m/%Y'))
    WHERE operador_id = NEW.operador_id
    AND fecha_desde >= NEW.fecha_desde
    AND estado = 'APROBADA';
END //

DELIMITER ;
```

**Cálculo proporcional:**
- Periodo de derecho: 01/01/2026 o fecha de inicio del contrato (si es posterior)
- Días devengados = (Días transcurridos desde periodo de derecho / 365) × 30 días

### 9.3 Trabajadores en Excedencia (Excluidos del Calendario)

| Código | Nombre | Excedencia Hasta |
|--------|--------|------------------|
| 011 | José María Aguilar | 03/09/2026 |
| 050 | Francisco Luz | 31/10/2026 |
| 077 | Pablo Javier Nuñez | 31/05/2026 |
| 280 | Pedro Moya | 25/03/2026 |

### 9.4 Tabla de Vacaciones 2026 (Fecha: 17/02/2026)

**Total trabajadores activos:** 66 (excluidos 4 en excedencia)

```
+-----+--------------------+-----------------------+------------+---------+--------+----------+--------+--------+
| Cod | Nombre             | Apellidos             | Periodo    | Corresp | Deveng | Invierno | Verano | Consum |
+-----+--------------------+-----------------------+------------+---------+--------+----------+--------+--------+
| 0   | María José         | Castillo Carrero      | 01/01/2026 |      30 |      4 |       14 |      0 |     14 |
| 002 | Dolores            | Morales Torres        | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 005 | Fernando Rafael    | Torralbo Acuña        | 01/01/2026 |      30 |      4 |        0 |      0 |      0 |
| 009 | Miguel Ángel       | Heredia Yañez         | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 010 | Pedro              | Molina Fuentes        | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 012 | Eva María          | García Álvarez        | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 016 | Jesús Javier       | Raya Lozano           | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 019 | Silvia             | Sierra Sánchez        | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 020 | Miguel Ángel       | Ruiz Díaz             | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 021 | María Ángeles      | Medina Caballero      | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 024 | Virginia           | Jiménez Montalbán     | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 028 | Juan David         | Molero Sánchez        | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 029 | Manuel             | Solar Jordán          | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 030 | María Ángeles      | Muñoz Jiménez         | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 033 | Eva                | Serrano Juárez        | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 038 | Soledad            | León Fernández        | 01/01/2026 |      30 |      4 |        0 |      0 |      0 |
| 041 | Laura              | Flores Moyano         | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 042 | Francisco José     | Boyer García          | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 047 | Rosario            | López Reina           | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 049 | Antonio José       | Porras López          | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 052 | Inmaculada         | Pérez Nogareda        | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 055 | Juan José          | Torres García         | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 059 | Francisco          | Soto Alcolea          | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 062 | Yesica             | Muñoz Oña             | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 063 | Ana Belén          | Pérez Mármol          | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 064 | Virtudes           | Osuna Roda            | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 071 | María del Puerto   | Navarro Otero         | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 074 | Antonio Jose       | Carmona Leal          | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 078 | Mónica             | Quesada Lucena        | 01/01/2026 |      30 |      4 |        0 |      0 |      0 |
| 079 | María Cristina     | Martínez Tejada       | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 084 | Josefa             | Bellido Garrido       | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 094 | Rafael             | Espejo González       | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 095 | Alfredo David      | Ruiz Moral            | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 097 | Francisco          | Cabello Sánchez       | 01/01/2026 |      30 |      4 |        0 |      0 |      0 |
| 104 | Juan Manuel        | Cervantes Carrasco    | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 106 | Jessica            | Ramírez Rasero        | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 110 | Alejandro          | Moreno Blanes         | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 111 | Cristina           | Moraleda Cerrato      | 01/01/2026 |      30 |      4 |        8 |      0 |      8 |
| 122 | ANGELICA ELISABEHT | ALEJANDRO FARIAS      | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 126 | RAFAEL             | DUARTE CERRILLO       | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 150 | Jorge              | Castillo Carrero      | 01/01/2026 |      30 |      4 |        0 |      0 |      0 |
| 160 | CARLOS             | FERNANDEZ HERNANDEZ   | 01/01/2026 |      30 |      4 |        0 |      0 |      0 |
| 162 | ROCIO ISABEL       | GARCIA SANCHEZ        | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 164 | CLARA              | MUÑOZ HERRERA         | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 176 | FRANCISCO JAVIER   | ROMÁN CALER           | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 181 | ANA CRISTINA       | LEÓN JIMENEZ          | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 182 | DANIEL             | SOPEÑA COSSIO         | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 184 | MARIA JOSE         | BERNIER AFÁN          | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 209 | ISAAC              | MARCOS GONZÁLEZ       | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 211 | EMILIANA           | PATILLA CONSUEGRA     | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 213 | NICOLAS            | CASTRO RODRIGUEZ      | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 216 | MARIA              | LEÓN PEÑA             | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 217 | ANTONIO            | ROMÁN NAVARRO         | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 219 | JESUS              | GOMEZ BEJARANO        | 01/01/2026 |      30 |      4 |        0 |      0 |      0 |
| 224 | SONIA              | GATA GARCIA           | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 227 | JAVIER             | CARMONA DUQUE         | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 234 | NATIVIDAD          | FERNÁNDEZ EXPOSITO    | 02/01/2026 |      30 |      4 |        0 |      0 |      0 |
| 236 | ÁLVARO             | MUÑIZ CASTILLO        | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 247 | YOLANDA            | DEL FRESNO RODRÍGUEZ  | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 250 | RAFAEL             | UCLES OSUNA           | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 255 | ALEJANDRO          | LEÓN JIMÉNEZ          | 02/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 257 | JOSÉ ANTONIO       | VELASCO MADRID        | 13/01/2026 |      29 |      3 |       15 |      0 |     15 |
| 258 | ÁNGEL              | ENCINAS MURILLO       | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 259 | HUGO               | AGUILAR PEÑA          | 01/01/2026 |      30 |      4 |       15 |      0 |     15 |
| 266 | TOMÁS              | CABANILLAS SERRANO    | 02/01/2026 |      30 |      4 |        0 |      0 |      0 |
| 272 | Haydeé Lucia       | Maltez Contreras      | 02/01/2026 |      30 |      4 |        0 |      0 |      0 |
| 559 | JESÚS              | BERRAL VILLÉN         | 02/01/2026 |      30 |      4 |        0 |      0 |      0 |
+-----+--------------------+-----------------------+------------+---------+--------+----------+--------+--------+
```

**Leyenda:**
- **Periodo**: Fecha desde la que computa el derecho a vacaciones
- **Corresp**: Días de vacaciones que corresponden en el año
- **Deveng**: Días devengados hasta la fecha (17/02/2026)
- **Invierno/Verano**: Días asignados por periodo
- **Consum**: Total días consumidos

### 9.5 Resumen de Estado

| Estado | Trabajadores |
|--------|--------------|
| Vacaciones invierno completas (15 días) | 52 |
| Vacaciones invierno parciales | 2 (María José 14, Cristina 8) |
| Sin vacaciones asignadas (bajas/pendientes) | 12 |
| Temporales sin asignar | 4 |

### 9.6 Trabajadores con Segundo Periodo Pendiente

| Código | Nombre | Consumidos | Pendientes |
|--------|--------|------------|------------|
| 111 | Cristina Moraleda | 8 | 22 |
| 0 | María José Castillo | 14 | 16 |

### 9.7 Trabajadores Temporales

| Código | Nombre | Periodo Derecho | Corresp | Fin Contrato |
|--------|--------|-----------------|---------|--------------|
| 234 | Natividad Fernández | 02/01/2026 | 30 | 30/06/2026 |
| 257 | José Antonio Velasco | 13/01/2026 | 29 | 12/04/2026 |
| 266 | Tomás Cabanillas | 02/01/2026 | 30 | 31/03/2026 |
| 272 | Haydeé Lucia Maltez | 02/01/2026 | 30 | 31/03/2026 |
| 559 | Jesús Berral | 02/01/2026 | 30 | 31/03/2026 |

### 9.8 Reglas de Adjudicación de Vacaciones (Página de Usuario)

**Reglas para solicitud de vacaciones por el trabajador:**

| Regla | Descripción |
|-------|-------------|
| Inicio de vacaciones | **Siempre en LUNES** de cada semana |
| Excepción semana 0 | Si las vacaciones empiezan en semana 0 (1-5 enero), pueden empezar otro día |
| Excepción festivo | Si el lunes es festivo, las vacaciones empiezan el siguiente día laboral |
| Máximo simultáneo | 5 trabajadores de vacaciones por día |
| Periodos | Invierno (enero-mayo) + Otoño (octubre-diciembre) |
| Verano | Junio-septiembre (pendiente asignar) |
| Bloques | Vacaciones en días consecutivos (7-15 días típico) |

**Proceso de solicitud:**
1. El trabajador accede a su página de usuario
2. Selecciona la semana de inicio de vacaciones (el sistema muestra solo lunes disponibles)
3. Selecciona duración (7 o 15 días)
4. El sistema verifica que no se supere el máximo de 5 trabajadores simultáneos
5. Si hay disponibilidad, se registra la solicitud
6. RRHH aprueba/rechaza la solicitud

**Tablas relacionadas:**

| Tabla | Descripción |
|-------|-------------|
| `diasfestivos` | Festivos nacionales y locales |
| `nuevo_carihuela_jorge_semanas_anuales` | Semanas del año con fecha inicio vacaciones |
| `nuevo_carihuela_jorge_vacaciones_calendario` | Calendario diario con slots |

**Tipos de festivos en `diasfestivos`:**

| Tipo | Año en BD | Descripción |
|------|-----------|-------------|
| Recursivo | 9999 | Se repite cada año (ej: Navidad 25/12) |
| Específico | Año real | Solo ese año (ej: Semana Santa) |

**Festivos recursivos configurados:**
- 01/01 - Año Nuevo
- 06/01 - Reyes
- 28/02 - Día de Andalucía
- 01/05 - Día del Trabajo
- 12/10 - Día de la Hispanidad
- 24/10 - San Rafael (local)
- 01/11 - Todos los Santos
- 06/12 - Día de la Constitución
- 08/12 - Inmaculada Concepción
- 25/12 - Navidad
- 31/12 - Fin de Año

**Festivos específicos (añadir cada año):**
- Semana Santa (Jueves y Viernes Santo)
- Traslados de festivos que caen en domingo

**Procedimiento automático: `generar_calendario_anual(año)`**

Este procedimiento genera automáticamente el calendario completo del año consultando la tabla `diasfestivos`:

```sql
CALL generar_calendario_anual(2026);
```

**Lógica del procedimiento:**
1. Genera los 365 días del año (una fila por día)
2. Calcula la semana correspondiente (semana 0 = días antes del primer lunes)
3. Verifica si es festivo (recursivo o específico)
4. Marca como no laboral: domingos y festivos
5. Guarda en `nuevo_carihuela_jorge_calendario_anual`

**Código del procedimiento almacenado:**

```sql
DELIMITER //

CREATE PROCEDURE generar_calendario_anual(IN p_anio INT)
BEGIN
    DECLARE v_fecha DATE;
    DECLARE v_fecha_fin DATE;
    DECLARE v_semana INT;
    DECLARE v_dia_semana VARCHAR(10);
    DECLARE v_laboral TINYINT;
    DECLARE v_festivo VARCHAR(100);
    DECLARE v_primer_lunes DATE;

    -- Limpiar calendario existente del año
    DELETE FROM nuevo_carihuela_jorge_calendario_anual WHERE YEAR(fecha) = p_anio;

    -- Establecer fechas de inicio y fin
    SET v_fecha = CONCAT(p_anio, '-01-01');
    SET v_fecha_fin = CONCAT(p_anio, '-12-31');

    -- Encontrar el primer lunes del año
    SET v_primer_lunes = v_fecha;
    WHILE DAYOFWEEK(v_primer_lunes) != 2 DO
        SET v_primer_lunes = DATE_ADD(v_primer_lunes, INTERVAL 1 DAY);
    END WHILE;

    -- Generar cada día del año
    WHILE v_fecha <= v_fecha_fin DO

        -- Calcular semana (0 para días antes del primer lunes)
        IF v_fecha < v_primer_lunes THEN
            SET v_semana = 0;
        ELSE
            SET v_semana = FLOOR(DATEDIFF(v_fecha, v_primer_lunes) / 7) + 1;
        END IF;

        -- Obtener día de la semana en formato España (1=Lunes, 7=Domingo)
        -- WEEKDAY() devuelve 0=Lunes, 6=Domingo, sumamos 1 para formato España
        SET v_dia_semana = CASE WEEKDAY(v_fecha)
            WHEN 0 THEN 'Lunes'     -- 1
            WHEN 1 THEN 'Martes'    -- 2
            WHEN 2 THEN 'Miércoles' -- 3
            WHEN 3 THEN 'Jueves'    -- 4
            WHEN 4 THEN 'Viernes'   -- 5
            WHEN 5 THEN 'Sábado'    -- 6
            WHEN 6 THEN 'Domingo'   -- 7
        END;

        -- Verificar si es festivo (recursivo año 9999 o específico del año)
        SELECT nombre INTO v_festivo
        FROM diasfestivos
        WHERE (YEAR(fecha) = 9999 AND MONTH(fecha) = MONTH(v_fecha) AND DAY(fecha) = DAY(v_fecha))
           OR (fecha = v_fecha)
        LIMIT 1;

        -- Determinar si es laboral
        -- PENDIENTE DE CONFIRMAR: Domingos y festivos laborables se deciden desde tabla de configuración
        -- Por ahora se marca según configuración pendiente
        SET v_laboral = 1; -- Por defecto laboral, se ajusta según tabla de configuración

        -- TODO: Consultar tabla de configuración para determinar si domingos/festivos son laborables
        -- IF (SELECT domingos_laborables FROM configuracion_calendario WHERE anio = p_anio) = 0 AND WEEKDAY(v_fecha) = 6 THEN
        --     SET v_laboral = 0;
        -- END IF;
        -- IF (SELECT festivos_laborables FROM configuracion_calendario WHERE anio = p_anio) = 0 AND v_festivo IS NOT NULL THEN
        --     SET v_laboral = 0;
        -- END IF;

        -- Insertar en el calendario
        INSERT INTO nuevo_carihuela_jorge_calendario_anual (semana, dia_semana, fecha, laboral, festivo)
        VALUES (v_semana, v_dia_semana, v_fecha, v_laboral, v_festivo);

        -- Limpiar variable festivo
        SET v_festivo = NULL;

        -- Siguiente día
        SET v_fecha = DATE_ADD(v_fecha, INTERVAL 1 DAY);

    END WHILE;

    -- Mostrar resumen
    SELECT
        COUNT(*) AS dias_totales,
        SUM(laboral) AS dias_laborables,
        COUNT(*) - SUM(laboral) AS dias_no_laborables,
        SUM(CASE WHEN festivo IS NOT NULL THEN 1 ELSE 0 END) AS festivos
    FROM nuevo_carihuela_jorge_calendario_anual
    WHERE YEAR(fecha) = p_anio;

END //

DELIMITER ;

-- Ejecutar para generar calendario 2026
CALL generar_calendario_anual(2026);
```

**Tabla: `nuevo_carihuela_jorge_calendario_anual`**

| Campo | Descripción |
|-------|-------------|
| semana | Número de semana (0-52) |
| dia_semana | Lunes, Martes, ..., Domingo |
| dia_semana_num | 1=Lunes, 7=Domingo (formato España) |
| fecha | Fecha completa |
| laboral | 1=Laboral, 0=No laboral (PENDIENTE CONFIGURAR) |
| festivo | Nombre del festivo (si aplica) |

**Estructura SQL:**
```sql
CREATE TABLE nuevo_carihuela_jorge_calendario_anual (
    id INT AUTO_INCREMENT PRIMARY KEY,
    semana INT NOT NULL COMMENT '0=antes del primer lunes, 1-52 semanas',
    dia_semana VARCHAR(10) NOT NULL COMMENT 'Lunes-Domingo',
    dia_semana_num TINYINT NOT NULL COMMENT 'Formato España: 1=Lunes, 7=Domingo',
    fecha DATE NOT NULL,
    laboral TINYINT(1) NOT NULL DEFAULT 1 COMMENT 'PENDIENTE: Configurar desde tabla',
    festivo VARCHAR(100) NULL,
    INDEX idx_fecha (fecha),
    INDEX idx_semana (semana),
    INDEX idx_laboral (laboral),
    UNIQUE KEY uk_fecha (fecha)
);
```

**Tabla de configuración de días laborables (PENDIENTE DECIDIR):**
```sql
-- PENDIENTE DE CONFIRMAR
CREATE TABLE nuevo_carihuela_jorge_configuracion_calendario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    anio INT NOT NULL,
    domingos_laborables TINYINT(1) NOT NULL DEFAULT 0 COMMENT '0=No, 1=Sí',
    festivos_laborables TINYINT(1) NOT NULL DEFAULT 0 COMMENT '0=No, 1=Sí',
    observaciones TEXT NULL,
    UNIQUE KEY uk_anio (anio)
);

-- Insertar configuración 2026 (VALORES PENDIENTES DE CONFIRMAR)
INSERT INTO nuevo_carihuela_jorge_configuracion_calendario (anio, domingos_laborables, festivos_laborables)
VALUES (2026, 0, 0); -- Por defecto: domingos y festivos NO laborables
```

**Resumen 2026:**
- 365 días totales
- 301 días laborables
- 64 días no laborables
- 14 festivos

### 9.8.1 Módulo ERP - Selección de Vacaciones

**PENDIENTE PROGRAMACIÓN**

**Requisito previo - Trabajadores elegibles:**

> El selector de vacaciones muestra trabajadores del **Nivel 3: Elegibles Vacaciones**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ FILTRO DE TRABAJADORES PARA SELECTOR DE VACACIONES                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Trabajadores con Contrato (Nivel 1)                                       │
│           │                                                                 │
│           ▼ menos excedencias                                               │
│  Trabajadores Actuales (Nivel 2)                                            │
│           │                                                                 │
│           ▼ menos baja larga duración                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ ELEGIBLES VACACIONES (Nivel 3) ◄── SELECTOR DE VACACIONES          │   │
│  │ (Paternidad/maternidad SÍ son elegibles)                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Excluidos del selector:                                                    │
│  - En excedencia                                                            │
│  - En baja de larga duración                                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

El módulo de selección de vacaciones en el ERP tendrá las siguientes características:

**Estructura de pestañas:**

| Pestaña | Periodo | Meses |
|---------|---------|-------|
| **Vacaciones Invierno** | Periodo Invierno/Otoño | Enero-Mayo + Octubre-Diciembre |
| **Vacaciones Verano** | Periodo Verano | Junio-Septiembre |

> **NOTA:** Las reglas de VERANO son las mismas que las de INVIERNO:
> - Solicitud con Opción 1 y Opción 2
> - Inicio solo en lunes (excepto semana 0 o lunes festivo)
> - Máximo 5 trabajadores simultáneos por día
> - Periodos de 15 días completos o 7-8 días
> - Misma interfaz de usuario y pantalla RRHH

**Visualización de vacaciones asignadas y año anterior:**

> **⚠️ PENDIENTE DE DESARROLLO** - Definir cómo se programará esta funcionalidad

- Ver trabajadores con fechas asignadas del año actual
- Ver histórico de vacaciones del año anterior
- Selector de año para comparar

**Interfaz de usuario - PESTAÑA INVIERNO (estilo Horarios):**

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ VACACIONES INVIERNO 2026                                                                                        │
├───────────────────────────┬─────────────────────────────────────────────────────────────────────────────────────┤
│ SELECTOR TRABAJADOR       │ CALENDARIO DE VACACIONES                                                           │
├───────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
│                           │                                                                                     │
│ [Buscar trabajador...]    │ Rango: Desde [05/01/2026▼] Hasta [31/01/2026▼]                                     │
│                           │                                                                                     │
│ ▼ Clara Muñoz             │ | S | Día | Fecha | Obs.  | 1           | 2          | 3        | 4     | 5      | │
│   Corresp: 30 días        │ |---|-----|-------|-------|-------------|------------|----------|-------|--------| │
│   2025: 06/01 - 20/01     │ | 1 | L   | 05-01 |       | Clara Muñoz | Jesús Raya | Jessica  | Emi   |        | │
│                           │ | 1 | M   | 06-01 | Reyes | Clara Muñoz | Jesús Raya | Jessica  | Emi   |        | │
│ ○ Jesús Raya              │ | 1 | X   | 07-01 |       | Clara Muñoz | Jesús Raya | Jessica  | Emi   | ██TÚ██ | │
│   Corresp: 30 días        │ | 1 | J   | 08-01 |       | Clara Muñoz | Jesús Raya | Jessica  | Emi   | ██TÚ██ | │
│   2025: 13/01 - 27/01     │ | 1 | V   | 09-01 |       |             | Jesús Raya | Jessica  |       | ██TÚ██ | │
│                           │ | 1 | S   | 10-01 |       |             | Jesús Raya | Jessica  |       | ██TÚ██ | │
│ ○ Jessica Ramírez         │ | 1 | D   | 11-01 |       |             | Jesús Raya | Jessica  |       | ██TÚ██ | │
│   Corresp: 30 días        │ | 2 | L   | 12-01 |       | Mª Á.Medina | Jesús Raya | Jessica  | Virtu | ██TÚ██ | │
│   2025: 03/02 - 17/02     │ | 2 | M   | 13-01 |       | Mª Á.Medina | Jesús Raya | Jessica  | Virtu |        | │
│                           │ | ...                                                                              | │
│ ○ José Antonio Velasco    │                                                                                     │
│   Corresp: 29 días        │ Leyenda: ██TÚ██ = Solicitud del trabajador seleccionado                            │
│   2025: (nuevo)           │                                                                                     │
│                           ├─────────────────────────────────────────────────────────────────────────────────────┤
│ ○ Hugo Aguilar            │ OPCIONES DE SOLICITUD                                                               │
│   Corresp: 30 días        │                                                                                     │
│   2025: 24/02 - 10/03     │ OPCIÓN 1 (Preferida):   Desde: [07/01/2026] Hasta: [21/01/2026] = 15 días          │
│                           │ OPCIÓN 2 (Alternativa): Desde: [02/02/2026] Hasta: [16/02/2026] = 15 días          │
│ ○ Pedro Molina            │                                                                                     │
│   Corresp: 30 días        │ [ENVIAR SOLICITUD]    [CANCELAR]                                                    │
│   2025: 03/03 - 17/03     │                                                                                     │
│                           │                                                                                     │
└───────────────────────────┴─────────────────────────────────────────────────────────────────────────────────────┘
```

**Elementos del selector de trabajador (columna izquierda):**

| Elemento | Descripción |
|----------|-------------|
| Nombre trabajador | Solo trabajadores elegibles (Nivel 4) |
| Corresp: XX días | Días de vacaciones que le corresponden según contrato |
| Año anterior (2025) | Periodo(s) de vacaciones del año anterior |
| (nuevo) | Si el trabajador no tiene histórico del año anterior |
| ▼ Seleccionado | Trabajador actualmente seleccionado |
| ○ No seleccionado | Otros trabajadores disponibles |
| Buscador | Campo para filtrar por nombre |

**Cálculo de días correspondientes:**

| Tipo contrato | Cálculo |
|---------------|---------|
| Indefinido | 30 días naturales (año completo) |
| Temporal | Proporcional según duración contrato |

**Ejemplo:** José Antonio Velasco (contrato 13/01/2026 - 12/04/2026) = 29 días correspondientes

**Días pendientes vs planificados:**

> Al adjudicar vacaciones de un periodo, se muestran los días **PENDIENTES** descontando los ya **PLANIFICADOS** en otros periodos (aunque no estén disfrutados).

**Ejemplo - Francisco Soto:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ PESTAÑA VERANO - Selector de trabajador                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ ○ Francisco Soto                                                            │
│   Corresp: 30 días                                                          │
│   Planif. Invierno: 15 días (06/04 - 20/04)                                │
│   Pendientes Verano: 15 días  ◄── Disponibles para adjudicar               │
│   2025: 10/04 - 24/04                                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Fórmula:**
```
Días Pendientes = Días Correspondientes - Días Planificados (otros periodos)
```

| Campo | Valor Francisco Soto |
|-------|---------------------|
| Corresp | 30 días |
| Planif. Invierno | 15 días (06/04 - 20/04) |
| Pendientes Verano | 30 - 15 = **15 días** |

> **NOTA:** Los días planificados se restan aunque NO estén disfrutados todavía. Lo importante es que ya están asignados a un periodo.

**Cancelación automática por ausencia:**

> Si un trabajador con vacaciones planificadas entra en situación de ausencia (baja, paternidad/maternidad, etc.), las vacaciones planificadas se **ELIMINAN AUTOMÁTICAMENTE** y los días vuelven a estar como **PENDIENTES**.

**Ejemplo - Trabajador con baja durante vacaciones planificadas:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ANTES DE LA BAJA                                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ ○ María García                                                              │
│   Corresp: 30 días                                                          │
│   Planif. Invierno: 15 días (02/03 - 16/03)                                │
│   Pendientes: 15 días                                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼ Se produce BAJA el 01/03/2026
┌─────────────────────────────────────────────────────────────────────────────┐
│ DESPUÉS DE LA BAJA (automático)                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ ○ María García                                                              │
│   Corresp: 30 días                                                          │
│   Planif. Invierno: CANCELADO (baja)                                       │
│   Pendientes: 30 días  ◄── Vuelven a estar disponibles                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Motivos de cancelación automática:**

| Motivo | Acción |
|--------|--------|
| Baja larga duración | Cancela vacaciones planificadas |
| Baja corta duración | Cancela vacaciones planificadas |
| Paternidad/Maternidad | Cancela vacaciones planificadas |
| Otros permisos | Cancela vacaciones planificadas |

**Registro en base de datos:**

Las vacaciones canceladas se registran en `nuevo_carihuela_jorge_vacaciones_canceladas` con el motivo de la cancelación.

**Sistema de opciones de solicitud:**

| Concepto | Descripción |
|----------|-------------|
| **Opción 1** | Periodo preferido por el trabajador |
| **Opción 2** | Periodo alternativo (por si Opción 1 no disponible) |
| **Motivo 2 opciones** | Alta demanda en ciertos periodos, no todos pueden coincidir |

**Modalidades de duración:**

| Modalidad | Días | Descripción |
|-----------|------|-------------|
| Periodo completo | 15 días | De lunes a domingo de la semana siguiente (14 noches) |
| Periodo parcial | 7-8 días | Una semana (lunes a domingo) |
| Combinación | 7+8 o 8+7 | Dos periodos parciales que suman 15 días |

**Restricciones de inicio de vacaciones:**

| Regla | El programa... |
|-------|----------------|
| Solo lunes | Solo muestra lunes en el dropdown de selección |
| Semana 0 | Excepción: permite iniciar en día distinto (01-05 enero) |
| Lunes festivo | Excepción: permite iniciar el siguiente día laboral |
| Bloqueo | NO permite seleccionar ningún otro día de inicio |

**Reglas de validación:**

| # | Regla | Descripción |
|---|-------|-------------|
| 1 | Elegibilidad | Solo trabajadores con contrato en vigor y sin excedencia |
| 2 | Días disponibles | No puede solicitar más días de los que tiene pendientes |
| 3 | Inicio lunes | Las vacaciones solo pueden empezar en lunes (excepto semana 0) |
| 4 | Festivo lunes | Si el lunes es festivo, empiezan el siguiente día laboral |
| 5 | Máximo 5 | No puede haber más de 5 trabajadores de vacaciones el mismo día |
| 6 | Periodo correcto | Pestaña Invierno: solo fechas Ene-May/Oct-Dic. Pestaña Verano: Jun-Sep |
| 7 | Días consecutivos | Las vacaciones se asignan en bloques consecutivos |

**Flujo de aprobación:**

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Trabajador  │───►│  Solicitud  │───►│   RRHH      │───►│  Aprobado/  │
│  solicita   │    │  Pendiente  │    │  Revisa     │    │  Rechazado  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

### 9.8.2 Pantalla RRHH - Gestión de Vacaciones (similar a Horario de Adrián)

**Funcionalidad:**
- Visualiza automáticamente todas las solicitudes de vacaciones enviadas por los trabajadores
- Permite aprobar/rechazar solicitudes
- Muestra si el trabajador tiene Opción 2 disponible
- Máximo 5 trabajadores por día → si hay más solicitudes, RRHH selecciona cuáles aprobar

**Interfaz RRHH - Gestión Vacaciones Invierno:**

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ GESTIÓN VACACIONES INVIERNO 2026 - RRHH                                                           [Estilo Horario]     │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                         │
│  Filtrar periodo:  Desde: [05/01/2026 ▼]   Hasta: [31/01/2026 ▼]    [APLICAR FILTRO]                                   │
│                                                                                                                         │
│  ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════   │
│  CALENDARIO CON SOLICITUDES PENDIENTES                                                                                  │
│  ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                                                         │
│  | S | Día | Fecha  | Obs.  | 1 (Aprobado)    | 2 (Aprobado)    | 3 (Aprobado)    | 4 (Aprobado)    | 5 (Aprobado)  | │
│  |---|-----|--------|-------|-----------------|-----------------|-----------------|-----------------|---------------| │
│  | 1 | L   | 05-01  |       | ✓ Clara Muñoz   | ✓ Jesús Raya    | ✓ Jessica       | ✓ Emi           |               | │
│  | 1 | M   | 06-01  | Reyes | ✓ Clara Muñoz   | ✓ Jesús Raya    | ✓ Jessica       | ✓ Emi           |               | │
│  | 1 | X   | 07-01  |       | ✓ Clara Muñoz   | ✓ Jesús Raya    | ✓ Jessica       | ✓ Emi           | ✓ Carlos      | │
│  | 1 | J   | 08-01  |       | ✓ Clara Muñoz   | ✓ Jesús Raya    | ✓ Jessica       | ✓ Emi           | ✓ Carlos      | │
│  | 1 | V   | 09-01  |       |                 | ✓ Jesús Raya    | ✓ Jessica       |                 | ✓ Carlos      | │
│  | ... |   |        |       |                 |                 |                 |                 |               | │
│                                                                                                                         │
│  ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════   │
│  SOLICITUDES PENDIENTES DE ASIGNAR (8 solicitudes para este periodo - máximo 5 slots)                                  │
│  ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                                                         │
│  | ☐ | Trabajador          | Opción | Fecha Inicio | Fecha Fin  | Días | Tiene Op.2 | Fechas Op.2          | Acción  | │
│  |---|---------------------|--------|--------------|------------|------|------------|----------------------|---------| │
│  | ☑ | Clara Muñoz         | Op.1   | 05/01/2026   | 19/01/2026 | 15   | Sí         | 02/02 - 16/02        | APROBAR | │
│  | ☑ | Jesús Raya          | Op.1   | 05/01/2026   | 19/01/2026 | 15   | No         | -                    | APROBAR | │
│  | ☑ | Jessica Ramírez     | Op.1   | 05/01/2026   | 19/01/2026 | 15   | Sí         | 09/02 - 23/02        | APROBAR | │
│  | ☑ | Emiliana Patilla    | Op.1   | 05/01/2026   | 19/01/2026 | 15   | Sí         | 16/02 - 02/03        | APROBAR | │
│  | ☐ | Miguel Ruiz         | Op.1   | 05/01/2026   | 19/01/2026 | 15   | Sí ⚠️      | 23/02 - 09/03        | REASIGN | │
│  | ☐ | Antonio Porras      | Op.1   | 05/01/2026   | 19/01/2026 | 15   | Sí ⚠️      | 02/03 - 16/03        | REASIGN | │
│  | ☐ | Virginia Jiménez    | Op.1   | 05/01/2026   | 19/01/2026 | 15   | No ❌      | -                    | REASIGN | │
│  | ☐ | Puerto Navarro      | Op.1   | 05/01/2026   | 19/01/2026 | 15   | Sí ⚠️      | 09/03 - 23/03        | REASIGN | │
│                                                                                                                         │
│  ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════   │
│  ACCIONES                                                                                                               │
│  ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                                                         │
│  Seleccionados para APROBAR: 4 trabajadores                                                                            │
│  Pendientes de REASIGNAR: 4 trabajadores (3 con Op.2 disponible, 1 sin Op.2)                                           │
│                                                                                                                         │
│  [APROBAR SELECCIONADOS]   [USAR OPCIÓN 2 PARA NO SELECCIONADOS]   [SOLICITAR NUEVAS FECHAS]                           │
│                                                                                                                         │
│  ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────   │
│  ⚠️ = Tiene Opción 2 disponible → Se puede asignar automáticamente a su periodo alternativo                            │
│  ❌ = No tiene Opción 2 → Debe volver a solicitar nuevas fechas                                                         │
│                                                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Acciones disponibles para RRHH:**

| Acción | Descripción |
|--------|-------------|
| **APROBAR SELECCIONADOS** | Aprueba las vacaciones de los trabajadores marcados con ☑ |
| **USAR OPCIÓN 2** | Asigna automáticamente la Opción 2 a los trabajadores no seleccionados que la tengan |
| **SOLICITAR NUEVAS FECHAS** | Notifica a los trabajadores sin Opción 2 para que envíen nueva solicitud |

**Lógica de gestión:**

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                        8 SOLICITUDES PARA MISMO PERIODO                        │
│                              (máximo 5 slots)                                  │
├────────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│   RRHH selecciona 4-5 trabajadores  ──────►  ✓ APROBADOS (pasan al calendario)│
│                                                                                │
│   Trabajadores NO seleccionados:                                               │
│   ├── Tiene Opción 2 ──────────────────────►  ⚠️ Asignar a Opción 2           │
│   │                                              automáticamente               │
│   │                                                                            │
│   └── NO tiene Opción 2 ───────────────────►  ❌ Notificar para que            │
│                                                  solicite nuevas fechas        │
│                                                                                │
└────────────────────────────────────────────────────────────────────────────────┘
```

**Indicadores visuales:**

| Icono | Significado |
|-------|-------------|
| ✓ | Vacaciones aprobadas |
| ☑ | Seleccionado para aprobar |
| ☐ | No seleccionado (pendiente reasignar) |
| ⚠️ | Tiene Opción 2 disponible |
| ❌ | No tiene Opción 2, debe solicitar nuevas fechas |
| 🔄 | **Lunes de transición** - Solapamiento de trabajadores |

### 9.8.3 Solapamiento de Lunes (Transición entre trabajadores)

**Situación:** Cuando un trabajador ACABA sus vacaciones un domingo y otro EMPIEZA el lunes siguiente, ese lunes hay un solapamiento que debe resaltarse.

**Ejemplo visual en el calendario:**

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ CALENDARIO - DETECCIÓN DE SOLAPAMIENTOS                                                             │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                     │
│  | S  | Día | Fecha  | 1                 | 2                 | 3             | 4         | 5       │
│  |----|-----|--------|-------------------|-------------------|---------------|-----------|---------|
│  | 2  | S   | 17-01  | Mª Ángeles Medina |                   |               | Virtu     |         │
│  | 2  | D   | 18-01  | Mª Ángeles Medina |                   |               | Virtu     |         │ ← Acaba Mª Ángeles
│  |----|-----|--------|-------------------|-------------------|---------------|-----------|---------|
│  | 3  | L   | 19-01  | 🔄 Hugo Aguilar   | Álvaro Muñiz      | Ana B. Pérez  | Juanjo    |         │ ← LUNES TRANSICIÓN
│  |    |     |        | ↑ SOLAPAMIENTO    |                   |               |           |         │
│  |    |     |        | Mª Ángeles → Hugo |                   |               |           |         │
│  |----|-----|--------|-------------------|-------------------|---------------|-----------|---------|
│  | 3  | M   | 20-01  | Hugo Aguilar      | Álvaro Muñiz      | Ana B. Pérez  | Juanjo    |         │
│                                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Panel de información de solapamiento:**

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 🔄 SOLAPAMIENTOS DETECTADOS - Lunes 19/01/2026                                                      │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                     │
│  | Slot | Trabajador que ACABA (Dom 18/01) | Trabajador que EMPIEZA (Lun 19/01) | Estado          │
│  |------|----------------------------------|-------------------------------------|-----------------|
│  | 1    | Mª Ángeles Medina                | Hugo Aguilar                        | 🔄 SOLAPAMIENTO │
│  | 4    | Virtu Osuna                      | Juanjo Torres                       | 🔄 SOLAPAMIENTO │
│                                                                                                     │
│  ⚠️ ATENCIÓN: El lunes 19/01/2026 NO estarán disponibles:                                          │
│     - Mª Ángeles Medina (último día de vacaciones)                                                  │
│     - Hugo Aguilar (primer día de vacaciones)                                                       │
│     - Virtu Osuna (último día de vacaciones)                                                        │
│     - Juanjo Torres (primer día de vacaciones)                                                      │
│                                                                                                     │
│  Total trabajadores ausentes por solapamiento: 4                                                    │
│                                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Lógica de detección:**

| Condición | Resultado |
|-----------|-----------|
| Trabajador A termina domingo | Último día = domingo |
| Trabajador B empieza lunes siguiente | Primer día = lunes |
| Mismo slot | 🔄 Marcar como SOLAPAMIENTO |
| El lunes | Ambos trabajadores ausentes (A termina, B empieza) |

**Regla de negocio:**

> En un lunes de transición, el slot muestra al trabajador que EMPIEZA (ya que el que acaba terminó el domingo), pero el sistema resalta visualmente que hubo una transición para que RRHH sepa que ese lunes:
> - El trabajador que ACABA ya no está trabajando (vacaciones hasta domingo incluido)
> - El trabajador que EMPIEZA tampoco está trabajando (vacaciones desde lunes)

### 9.8.4 Solapamiento entre Periodos Invierno/Verano

**Regla:** Las fechas de vacaciones de INVIERNO y VERANO pueden coincidir en los días límite de cada periodo.

**Ejemplo:** Lunes 01/06/2026 (transición Invierno → Verano)

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ SOLAPAMIENTO ENTRE PERIODOS - Junio 2026                                                            │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                     │
│  | S  | Día | Fecha  | Periodo  | 1                 | 2                 | 3             | 4       | │
│  |----|-----|--------|----------|-------------------|-------------------|---------------|---------|│
│  | 21 | S   | 30-05  | INVIERNO | Eva Serrano       | Cristina Martínez |               |         | │
│  | 21 | D   | 31-05  | INVIERNO | Eva Serrano       | Cristina Martínez |               |         | │ ← Último día INVIERNO
│  |----|-----|--------|----------|-------------------|-------------------|---------------|---------|│
│  | 22 | L   | 01-06  | 🔀 MIXTO | 🔄 Pedro Molina   | 🔄 Juan David     | Eva Serrano   | Cris M. | │ ← Primer día VERANO
│  |    |     |        |          | (VERANO empieza)  | (VERANO empieza)  | (INV. acaba)  | (acaba) | │
│  |----|-----|--------|----------|-------------------|-------------------|---------------|---------|│
│  | 22 | M   | 02-06  | VERANO   | Pedro Molina      | Juan David        |               |         | │
│                                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Detalle del día de transición (01/06/2026):**

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 🔀 DÍA MIXTO - Lunes 01/06/2026                                                                     │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                     │
│  TRABAJADORES QUE ACABAN (Periodo INVIERNO):                                                        │
│  ├── Slot 3: Eva Serrano (último día de vacaciones invierno)                                        │
│  └── Slot 4: Cristina Martínez (último día de vacaciones invierno)                                  │
│                                                                                                     │
│  TRABAJADORES QUE EMPIEZAN (Periodo VERANO):                                                        │
│  ├── Slot 1: Pedro Molina (primer día de vacaciones verano)                                         │
│  └── Slot 2: Juan David (primer día de vacaciones verano)                                           │
│                                                                                                     │
│  ⚠️ TOTAL AUSENTES ESTE DÍA: 4 trabajadores                                                         │
│     - 2 terminando vacaciones de INVIERNO                                                           │
│     - 2 empezando vacaciones de VERANO                                                              │
│                                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Rangos de fechas por periodo:**

| Periodo | Tramos | Meses |
|---------|--------|-------|
| **INVIERNO** | Tramo 1 | Enero - Mayo |
|              | Tramo 2 | Octubre - Diciembre |
| **VERANO** | Único | Junio - Septiembre |

**Solapamientos posibles entre periodos:**

| Transición | Fecha límite | Ejemplo |
|------------|--------------|---------|
| INVIERNO → VERANO | Finales Mayo / Inicio Junio | Lunes 01/06/2026: Trabajador INVIERNO acaba, trabajador VERANO empieza |
| VERANO → INVIERNO | Finales Septiembre / Inicio Octubre | Lunes 05/10/2026: Trabajador VERANO acaba, trabajador INVIERNO empieza |

**Ejemplo transición INVIERNO → VERANO (Lunes 01/06/2026):**

```
| S  | Día | Fecha  | Periodo  | 1               | 2             | 3           | 4         |
|----|-----|--------|----------|-----------------|---------------|-------------|-----------|
| 21 | D   | 31-05  | INVIERNO | Eva Serrano     | Cristina M.   |             |           | ← Último día INVIERNO
| 22 | L   | 01-06  | 🔀 MIXTO | 🔄 Pedro Molina | 🔄 Juan David | Eva (acaba) | Cris (ac) | ← Primer día VERANO
| 22 | M   | 02-06  | VERANO   | Pedro Molina    | Juan David    |             |           |
```

**Ejemplo transición VERANO → INVIERNO (Lunes 05/10/2026):**

```
| S  | Día | Fecha  | Periodo  | 1               | 2             | 3           | 4         |
|----|-----|--------|----------|-----------------|---------------|-------------|-----------|
| 40 | D   | 04-10  | VERANO   | Alfredo         | Rosario       |             |           | ← Último día VERANO
| 41 | L   | 05-10  | 🔀 MIXTO | 🔄 Solar        | 🔄 Miguel Ruiz| Alfredo(ac) | Rosa (ac) | ← Primer día INVIERNO (tramo 2)
| 41 | M   | 06-10  | INVIERNO | Solar           | Miguel Ruiz   |             |           |
```

**Indicadores visuales para días mixtos:**

| Icono | Significado |
|-------|-------------|
| 🔀 | Día MIXTO (coinciden trabajadores de ambos periodos) |
| (INV.) | Trabajador con vacaciones de periodo INVIERNO |
| (VER.) | Trabajador con vacaciones de periodo VERANO |

**Regla de validación:**

> El sistema PERMITE que las vacaciones de un trabajador de INVIERNO terminen el mismo día que empiezan las vacaciones de VERANO de otro trabajador. Ambos se contabilizan en los 5 slots máximos del día.

**Estados de la solicitud:**

| Estado | Descripción |
|--------|-------------|
| PENDIENTE | Solicitud enviada, esperando revisión RRHH |
| APROBADA | Vacaciones confirmadas |
| RECHAZADA | Vacaciones denegadas (con motivo) |
| CANCELADA | Cancelada por el trabajador o por incidencia (baja, etc.) |

**Tabla de base de datos: `nuevo_carihuela_jorge_vacaciones_solicitudes`**

```sql
CREATE TABLE nuevo_carihuela_jorge_vacaciones_solicitudes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    operador_id INT NOT NULL,
    tipo_periodo ENUM('INVIERNO', 'VERANO') NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    dias_solicitados INT NOT NULL,
    estado ENUM('PENDIENTE', 'APROBADA', 'RECHAZADA', 'CANCELADA') DEFAULT 'PENDIENTE',
    motivo_rechazo VARCHAR(255) NULL,
    fecha_solicitud TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_resolucion TIMESTAMP NULL,
    resuelto_por INT NULL,
    observaciones TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (operador_id) REFERENCES operadores(id),
    INDEX idx_operador (operador_id),
    INDEX idx_estado (estado),
    INDEX idx_periodo (tipo_periodo),
    INDEX idx_fechas (fecha_inicio, fecha_fin)
);
```

**Festivos 2026:**

| S | Día | Fecha | Festivo |
|---|-----|-------|---------|
| 0 | Jueves | 01/01 | Año Nuevo |
| 1 | Martes | 06/01 | Reyes |
| 8 | Sábado | 28/02 | Día de Andalucía |
| 13 | Jueves | 02/04 | Jueves Santo |
| 13 | Viernes | 03/04 | Viernes Santo |
| 17 | Viernes | 01/05 | Día del Trabajo |
| 41 | Lunes | 12/10 | Hispanidad |
| 42 | Sábado | 24/10 | San Rafael (Local) |
| 43 | Domingo | 01/11 | Todos los Santos |
| 44 | Lunes | 02/11 | Todos los Santos (traslado) |
| 48 | Domingo | 06/12 | Constitución |
| 49 | Martes | 08/12 | Inmaculada |
| 51 | Viernes | 25/12 | Navidad |
| 52 | Jueves | 31/12 | Fin de Año |

**PENDIENTE PROGRAMACIÓN:**
1. Interfaz de usuario para solicitud de vacaciones
2. Validar máximo 5 trabajadores simultáneos
3. Ejecutar `CALL generar_calendario_anual(AÑO)` cada año nuevo

**Consultas SQL útiles para vacaciones:**

```sql
-- Verificar disponibilidad de slots para una fecha
SELECT
    DATE_FORMAT(c.fecha, '%d/%m/%Y') AS Fecha,
    DAYNAME(c.fecha) AS DiaSemana,
    c.semana AS Semana,
    COUNT(v.id) AS SlotsOcupados,
    5 - COUNT(v.id) AS SlotsLibres,
    CASE
        WHEN COUNT(v.id) >= 5 THEN 'COMPLETO'
        ELSE 'DISPONIBLE'
    END AS Estado
FROM nuevo_carihuela_jorge_calendario_anual c
LEFT JOIN nuevo_carihuela_jorge_vacaciones v
    ON c.fecha BETWEEN v.fecha_desde AND v.fecha_hasta
WHERE c.fecha BETWEEN '2026-02-01' AND '2026-02-28'
GROUP BY c.fecha, c.semana
ORDER BY c.fecha;

-- Obtener trabajadores de vacaciones en una fecha específica
SELECT
    o.nombre_corto AS Trabajador,
    v.tipo AS Periodo,
    DATE_FORMAT(v.fecha_desde, '%d/%m') AS Desde,
    DATE_FORMAT(v.fecha_hasta, '%d/%m') AS Hasta,
    v.dias AS Dias
FROM nuevo_carihuela_jorge_vacaciones v
JOIN operadores o ON v.operador_id = o.id
WHERE '2026-02-10' BETWEEN v.fecha_desde AND v.fecha_hasta
ORDER BY v.fecha_desde;

-- Vista resumen anual de vacaciones por trabajador
SELECT
    cu.codigo AS Cod,
    o.nombre AS Nombre,
    o.apellidos AS Apellidos,
    COALESCE(SUM(CASE WHEN v.tipo = 'INVIERNO' THEN v.dias ELSE 0 END), 0) AS DiasInvierno,
    COALESCE(SUM(CASE WHEN v.tipo = 'VERANO' THEN v.dias ELSE 0 END), 0) AS DiasVerano,
    COALESCE(SUM(v.dias), 0) AS DiasTotal,
    CASE
        WHEN cu.fecha_fin IS NULL THEN 30
        ELSE ROUND(DATEDIFF(LEAST(cu.fecha_fin, '2026-12-31'), GREATEST(cu.fecha_inicio, '2026-01-01')) / 365 * 30)
    END AS DiasCorresponde,
    CASE
        WHEN cu.fecha_fin IS NULL THEN 30
        ELSE ROUND(DATEDIFF(LEAST(cu.fecha_fin, '2026-12-31'), GREATEST(cu.fecha_inicio, '2026-01-01')) / 365 * 30)
    END - COALESCE(SUM(v.dias), 0) AS DiasPendientes
FROM contratos_usuario cu
JOIN operadores o ON cu.operador_id = o.id
LEFT JOIN nuevo_carihuela_jorge_vacaciones v
    ON v.operador_id = o.id AND YEAR(v.fecha_desde) = 2026
WHERE cu.deleted_at IS NULL
AND (cu.fecha_fin IS NULL OR cu.fecha_fin >= '2026-01-01')
GROUP BY cu.codigo, o.nombre, o.apellidos, cu.fecha_inicio, cu.fecha_fin
ORDER BY o.apellidos, o.nombre;
```

**Estructura del calendario:**
- Semana (S): Número de semana del año
- Día: L, M, X, J, V, S, D
- Fecha: Fecha corta (DD-MM)
- Observaciones: Festivos u otras notas
- Slots 1-5: Trabajadores asignados (máximo 5 simultáneos)

### 9.9 Calendario de Vacaciones 2026 - Periodo Invierno/Otoño

**PENDIENTE DE PROGRAMAR:** Implementar tabla `nuevo_carihuela_jorge_vacaciones_calendario` con la siguiente estructura:

```
| S  | Día | Fecha  | Observaciones              | Slot 1              | Slot 2              | Slot 3              | Slot 4              | Slot 5          |
|----|-----|--------|----------------------------|---------------------|---------------------|---------------------|---------------------|-----------------|
| 0  | V   | 02-01  |                            | Clara Muñoz         | Jesús Raya          | Jessica             | Emi                 |                 |
| 0  | S   | 03-01  |                            | Clara Muñoz         | Jesús Raya          | Jessica             | Emi                 |                 |
| 0  | D   | 04-01  |                            | Clara Muñoz         | Jesús Raya          | Jessica             | Emi                 |                 |
| 1  | L   | 05-01  |                            | Clara Muñoz         | Jesús Raya          | Jessica             | Emi                 |                 |
| 1  | M   | 06-01  | Reyes                      | Clara Muñoz         | Jesús Raya          | Jessica             | Emi                 |                 |
| 1  | X   | 07-01  |                            | Clara Muñoz         | Jesús Raya          | Jessica             | Emi                 | Carlos          |
| 1  | J   | 08-01  |                            | Clara Muñoz         | Jesús Raya          | Jessica             | Emi                 | Carlos          |
| 1  | V   | 09-01  |                            |                     | Jesús Raya          | Jessica             |                     | Carlos          |
| 1  | S   | 10-01  |                            |                     | Jesús Raya          | Jessica             |                     | Carlos          |
| 1  | D   | 11-01  |                            |                     | Jesús Raya          | Jessica             |                     | Carlos          |
| 2  | L   | 12-01  |                            | Mª Ángeles Medina   | Jesús Raya          | Jessica             | Virtu               | Carlos          |
| 2  | M   | 13-01  |                            | Mª Ángeles Medina   | Jesús Raya          | Jessica             | Virtu               |                 |
| 2  | X   | 14-01  |                            | Mª Ángeles Medina   | Jesús Raya          | Jessica             | Virtu               |                 |
| 2  | J   | 15-01  |                            | Mª Ángeles Medina   | Jesús Raya          | Jessica             | Virtu               |                 |
| 2  | V   | 16-01  |                            | Mª Ángeles Medina   | Jesús Raya          | Jessica             | Virtu               |                 |
| 2  | S   | 17-01  |                            | Mª Ángeles Medina   |                     |                     | Virtu               |                 |
| 2  | D   | 18-01  |                            | Mª Ángeles Medina   |                     |                     | Virtu               |                 |
| 3  | L   | 19-01  |                            | M. Medina/Hugo      | Álvaro Muñiz        | Ana B. Pérez        | Juanjo              |                 |
| 3  | M   | 20-01  |                            | Hugo Aguilar        | Álvaro Muñiz        | Ana B. Pérez        | Juanjo              |                 |
| 3  | X   | 21-01  |                            | Hugo Aguilar        | Álvaro Muñiz        | Ana B. Pérez        | Juanjo              |                 |
| 3  | J   | 22-01  |                            | Hugo Aguilar        | Álvaro Muñiz        | Ana B. Pérez        | Juanjo              |                 |
| 3  | V   | 23-01  |                            | Hugo Aguilar        | Álvaro Muñiz        | Ana B. Pérez        | Juanjo              |                 |
| 3  | S   | 24-01  |                            | Hugo Aguilar        | Álvaro Muñiz        | Ana B. Pérez        | Juanjo              |                 |
| 3  | D   | 25-01  |                            | Hugo Aguilar        | Álvaro Muñiz        | Ana B. Pérez        | Juanjo              |                 |
| 4  | L   | 26-01  |                            | Pedro Molina        | Jose Antonio        | Ángelica            | Juanjo              |                 |
| 4  | M   | 27-01  |                            | Pedro Molina        | Jose Antonio        | Ángelica            | Juanjo              |                 |
| 4  | X   | 28-01  |                            | Pedro Molina        | Jose Antonio        | Ángelica            | Juanjo              |                 |
| 4  | J   | 29-01  |                            | Pedro Molina        | Jose Antonio        | Ángelica            | Juanjo              |                 |
| 4  | V   | 30-01  |                            | Pedro Molina        | Jose Antonio        | Ángelica            | Juanjo              |                 |
| 4  | S   | 31-01  |                            | Pedro Molina        | Jose Antonio        | Ángelica            | Juanjo              |                 |
| 4  | D   | 01-02  |                            | Pedro Molina        | Jose Antonio        | Ángelica            | Juanjo              |                 |
| 5  | L   | 02-02  |                            | Alfredo             | Alejandro León      | Ángelica            |                     |                 |
| 5  | M   | 03-02  |                            | Alfredo             | Alejandro León      | Ángelica            |                     |                 |
| 5  | X   | 04-02  |                            | Alfredo             | Alejandro León      | Ángelica            |                     |                 |
| 5  | J   | 05-02  |                            | Alfredo             | Alejandro León      | Ángelica            |                     |                 |
| 5  | V   | 06-02  |                            | Alfredo             | Alejandro León      | Ángelica            |                     |                 |
| 5  | S   | 07-02  |                            | Alfredo             | Alejandro León      | Ángelica            |                     |                 |
| 5  | D   | 08-02  |                            | Alfredo             | Alejandro León      | Ángelica            |                     |                 |
| 6  | L   | 09-02  |                            | Alfredo             | A. Porras           | Sonia Gata          |                     |                 |
| 6  | M   | 10-02  |                            | Alfredo             | A. Porras           | Sonia Gata          |                     |                 |
| 6  | X   | 11-02  |                            | Alfredo             | A. Porras           | Sonia Gata          |                     |                 |
| 6  | J   | 12-02  |                            | Alfredo             | A. Porras           | Sonia Gata          |                     |                 |
| 6  | V   | 13-02  |                            | Alfredo             | A. Porras           | Sonia Gata          |                     |                 |
| 6  | S   | 14-02  |                            | Alfredo             | A. Porras           | Sonia Gata          |                     |                 |
| 6  | D   | 15-02  |                            | Alfredo             | A. Porras           | Sonia Gata          |                     |                 |
| 7  | L   | 16-02  |                            | Alejandro Moreno    | A. Porras           | Fran Román          | Cristina Moraleda   |                 |
| 7  | M   | 17-02  |                            | Alejandro Moreno    | A. Porras           | Fran Román          | Cristina Moraleda   |                 |
| 7  | X   | 18-02  |                            | Alejandro Moreno    | A. Porras           | Fran Román          | Cristina Moraleda   |                 |
| 7  | J   | 19-02  |                            | Alejandro Moreno    | A. Porras           | Fran Román          | Cristina Moraleda   |                 |
| 7  | V   | 20-02  |                            | Alejandro Moreno    | A. Porras           | Fran Román          | Cristina Moraleda   |                 |
| 7  | S   | 21-02  |                            | Alejandro Moreno    | A. Porras           | Fran Román          | Cristina Moraleda   |                 |
| 7  | D   | 22-02  |                            | Alejandro Moreno    | A. Porras           | Fran Román          | Cristina Moraleda   |                 |
| 8  | L   | 23-02  |                            | Alejandro Moreno    | Nico                | Fran Román          | Miguel Ruiz         |                 |
| 8  | M   | 24-02  |                            | Alejandro Moreno    | Nico                | Fran Román          | Miguel Ruiz         |                 |
| 8  | X   | 25-02  |                            | Alejandro Moreno    | Nico                | Fran Román          | Miguel Ruiz         |                 |
| 8  | J   | 26-02  |                            | Alejandro Moreno    | Nico                | Fran Román          | Miguel Ruiz         |                 |
| 8  | V   | 27-02  |                            | Alejandro Moreno    | Nico                | Fran Román          | Miguel Ruiz         |                 |
| 8  | S   | 28-02  | Día de Andalucía           | Alejandro Moreno    | Nico                | Fran Román          | Miguel Ruiz         |                 |
| 8  | D   | 01-03  |                            | Alejandro Moreno    | Nico                | Fran Román          | Miguel Ruiz         |                 |
| 9  | L   | 02-03  |                            | Juan David          | Nico                | Fran Román          |                     |                 |
| 9  | M   | 03-03  |                            | Juan David          | Nico                | Yessica Muñoz       |                     |                 |
| 9  | X   | 04-03  |                            | Juan David          | Nico                | Yessica Muñoz       |                     |                 |
| 9  | J   | 05-03  |                            | Juan David          | Nico                | Yessica Muñoz       |                     |                 |
| 9  | V   | 06-03  |                            | Juan David          | Nico                | Yessica Muñoz       |                     |                 |
| 9  | S   | 07-03  |                            | Juan David          | Nico                | Yessica Muñoz       |                     |                 |
| 9  | D   | 08-03  |                            | Juan David          | Nico                | Yessica Muñoz       |                     |                 |
| 10 | L   | 09-03  |                            | Josefa              | Mª José Castillo    | Yessica Muñoz       | Inma                |                 |
| 10 | M   | 10-03  |                            | Josefa              | Mª José Castillo    | Yessica Muñoz       | Inma                |                 |
| 10 | X   | 11-03  |                            | Josefa              | Mª José Castillo    | Yessica Muñoz       | Inma                |                 |
| 10 | J   | 12-03  |                            | Josefa              | Mª José Castillo    | Yessica Muñoz       | Inma                |                 |
| 10 | V   | 13-03  |                            | Josefa              | Mª José Castillo    | Yessica Muñoz       | Inma                |                 |
| 10 | S   | 14-03  |                            | Josefa              | Mª José Castillo    | Yessica Muñoz       | Inma                |                 |
| 10 | D   | 15-03  |                            | Josefa              | Mª José Castillo    | Yessica Muñoz       | Inma                |                 |
| 11 | L   | 16-03  |                            | Josefa              | Puerto              | Laura Flores        | Carmona             |                 |
| 11 | M   | 17-03  |                            | Josefa              | Puerto              | Laura Flores        | Carmona             |                 |
| 11 | X   | 18-03  |                            | Josefa              | Puerto              | Laura Flores        | Carmona             |                 |
| 11 | J   | 19-03  |                            | Josefa              | Puerto              | Laura Flores        | Carmona             |                 |
| 11 | V   | 20-03  |                            | Josefa              | Puerto              | Laura Flores        | Carmona             |                 |
| 11 | S   | 21-03  |                            | Josefa              | Puerto              | Laura Flores        | Carmona             |                 |
| 11 | D   | 22-03  |                            | Josefa              | Puerto              | Laura Flores        | Carmona             |                 |
| 12 | L   | 23-03  |                            | Miguel Á. Heredia   | Clara Muñoz         | Laura Flores        | Carmona             |                 |
| 12 | M   | 24-03  |                            | Miguel Á. Heredia   | Clara Muñoz         | Laura Flores        | Carmona             |                 |
| 12 | X   | 25-03  |                            | Miguel Á. Heredia   | Clara Muñoz         | Laura Flores        | Carmona             |                 |
| 12 | J   | 26-03  |                            | Miguel Á. Heredia   | Clara Muñoz         | Laura Flores        | Carmona             |                 |
| 12 | V   | 27-03  |                            | Miguel Á. Heredia   | Clara Muñoz         | Laura Flores        | Carmona             |                 |
| 12 | S   | 28-03  |                            | Miguel Á. Heredia   | Clara Muñoz         | Laura Flores        | Carmona             |                 |
| 12 | D   | 29-03  |                            | Miguel Á. Heredia   | Clara Muñoz         | Laura Flores        | Carmona             |                 |
| 13 | L   | 30-03  |                            | Miguel Á. Heredia   | Eva García          | Ana Cristina/Mª José Bernier | Hugo Aguilar/Clara Muñoz |    |
| 13 | M   | 31-03  |                            | Miguel Á. Heredia   | Eva García          | Ana Cristina        | Hugo Aguilar        |                 |
| 13 | X   | 01-04  |                            | Miguel Á. Heredia   | Eva García          | Ana Cristina        | Hugo Aguilar        |                 |
| 13 | J   | 02-04  | Jueves Santo               | Miguel Á. Heredia   | Eva García          | Ana Cristina        | Hugo Aguilar        |                 |
| 13 | V   | 03-04  | Viernes Santo              | Miguel Á. Heredia   | Eva García          | Ana Cristina        | Hugo Aguilar        |                 |
| 13 | S   | 04-04  |                            | Miguel Á. Heredia   | Eva García          | Ana Cristina        | Hugo Aguilar        |                 |
| 13 | D   | 05-04  |                            | Miguel Á. Heredia   | Eva García          | Ana Cristina        | Hugo Aguilar        |                 |
| 14 | L   | 06-04  |                            | Francisco Soto/     | Eva García          | Mª José Bernier     |                     |                 |
| 14 | M   | 07-04  |                            | Francisco Soto      | Eva García          | Mª José Bernier     |                     |                 |
| 14 | X   | 08-04  |                            | Francisco Soto      | Eva García          | Mª José Bernier     |                     |                 |
| 14 | J   | 09-04  |                            | Francisco Soto      | Eva García          | Mª José Bernier     |                     |                 |
| 14 | V   | 10-04  |                            | Francisco Soto      | Eva García          | Mª José Bernier     |                     |                 |
| 14 | S   | 11-04  |                            | Francisco Soto      | Eva García          | Mª José Bernier     |                     |                 |
| 14 | D   | 12-04  |                            | Francisco Soto      | Eva García          | Mª José Bernier     |                     |                 |
| 15 | L   | 13-04  |                            | Francisco Soto      | Rocío García        | Mª José Bernier     |                     |                 |
| 15 | M   | 14-04  |                            | Francisco Soto      | Rocío García        | Mª José Bernier     |                     |                 |
| 15 | X   | 15-04  |                            | Francisco Soto      | Rocío García        | Mª José Bernier     |                     |                 |
| 15 | J   | 16-04  |                            | Francisco Soto      | Rocío García        | Mª José Bernier     |                     |                 |
| 15 | V   | 17-04  |                            | Francisco Soto      | Rocío García        | Mª José Bernier     |                     |                 |
| 15 | S   | 18-04  |                            | Francisco Soto      | Rocío García        | Mª José Bernier     |                     |                 |
| 15 | D   | 19-04  |                            | Francisco Soto      | Rocío García        | Mª José Bernier     |                     |                 |
| 16 | L   | 20-04  |                            | Cervantes           | Rocío García        | Rafael Espejo       | Virginia Jiménez    |                 |
| 16 | M   | 21-04  |                            | Cervantes           | Rocío García        | Rafael Espejo       | Virginia Jiménez    |                 |
| 16 | X   | 22-04  |                            | Cervantes           | Rocío García        | Rafael Espejo       | Virginia Jiménez    |                 |
| 16 | J   | 23-04  |                            | Cervantes           | Rocío García        | Rafael Espejo       | Virginia Jiménez    |                 |
| 16 | V   | 24-04  |                            | Cervantes           | Rocío García        | Rafael Espejo       | Virginia Jiménez    |                 |
| 16 | S   | 25-04  |                            | Cervantes           | Rocío García        | Rafael Espejo       | Virginia Jiménez    |                 |
| 16 | D   | 26-04  |                            | Cervantes           | Rocío García        | Rafael Espejo       | Virginia Jiménez    |                 |
| 17 | L   | 27-04  |                            | Cervantes           | Yolanda del Fresno  |                     | Virginia Jiménez    |                 |
| 17 | M   | 28-04  |                            | Cervantes           | Yolanda del Fresno  | Morales             | Virginia Jiménez    |                 |
| 17 | X   | 29-04  |                            | Cervantes           | Yolanda del Fresno  | Morales             | Virginia Jiménez    |                 |
| 17 | J   | 30-04  |                            | Cervantes           | Yolanda del Fresno  | Morales             | Virginia Jiménez    |                 |
| 17 | V   | 01-05  | Día del Trabajo            | Cervantes           | Yolanda del Fresno  | Morales             | Virginia Jiménez    |                 |
| 17 | S   | 02-05  |                            | Cervantes           | Yolanda del Fresno  | Morales             | Virginia Jiménez    |                 |
| 17 | D   | 03-05  |                            | Cervantes           | Yolanda del Fresno  | Morales             | Virginia Jiménez    |                 |
| 18 | L   | 04-05  |                            | Mª León             | Yolanda del Fresno  | Rosario López       | Silvia Sánchez      |                 |
| 18 | M   | 05-05  |                            | Mª León             | Yolanda del Fresno  | Rosario López       | Silvia Sánchez      |                 |
| 18 | X   | 06-05  |                            | Mª León             | Yolanda del Fresno  | Rosario López       | Silvia Sánchez      |                 |
| 18 | J   | 07-05  |                            | Mª León             | Yolanda del Fresno  | Rosario López       | Silvia Sánchez      |                 |
| 18 | V   | 08-05  |                            | Mª León             | Yolanda del Fresno  | Rosario López       | Silvia Sánchez      |                 |
| 18 | S   | 09-05  |                            | Mª León             | Yolanda del Fresno  | Rosario López       | Silvia Sánchez      |                 |
| 18 | D   | 10-05  |                            | Mª León             | Yolanda del Fresno  | Rosario López       | Silvia Sánchez      |                 |
| 19 | L   | 11-05  |                            | Mª León             | Mª Ángeles Muñoz    | Rosario López       | Silvia Sánchez      |                 |
| 19 | M   | 12-05  |                            | Mª León             | Mª Ángeles Muñoz    | Rosario López       | Silvia Sánchez      |                 |
| 19 | X   | 13-05  |                            | Mª León             | Mª Ángeles Muñoz    | Rosario López       | Silvia Sánchez      |                 |
| 19 | J   | 14-05  |                            | Mª León             | Mª Ángeles Muñoz    | Rosario López       | Silvia Sánchez      |                 |
| 19 | V   | 15-05  |                            | Mª León             | Mª Ángeles Muñoz    | Rosario López       | Silvia Sánchez      |                 |
| 19 | S   | 16-05  |                            | Mª León             | Mª Ángeles Muñoz    | Rosario López       | Silvia Sánchez      |                 |
| 19 | D   | 17-05  |                            | Mª León             | Mª Ángeles Muñoz    | Rosario López       | Silvia Sánchez      |                 |
| 20 | L   | 18-05  |                            | Mª León             | Mª Ángeles Muñoz    | Rosario López       | Silvia Sánchez      |                 |
| 20 | M   | 19-05  |                            | Ángel               | Mª Ángeles Muñoz    | Antonio Román       | Sopeña              |                 |
| 20 | X   | 20-05  |                            | Ángel               | Mª Ángeles Muñoz    | Antonio Román       | Sopeña              |                 |
| 20 | J   | 21-05  |                            | Ángel               | Mª Ángeles Muñoz    | Antonio Román       | Sopeña              |                 |
| 20 | V   | 22-05  |                            | Ángel               | Mª Ángeles Muñoz    | Antonio Román       | Sopeña              |                 |
| 20 | S   | 23-05  |                            | Ángel               | Mª Ángeles Muñoz    | Antonio Román       | Sopeña              |                 |
| 20 | D   | 24-05  |                            | Ángel               | Mª Ángeles Muñoz    | Antonio Román       | Sopeña              |                 |
| 21 | L   | 25-05  |                            | Ángel               | Eva Serrano         | Cristina Martínez   |                     |                 |
| 21 | M   | 26-05  |                            | Mª Ángeles Medina   | Eva Serrano         | Cristina Martínez   |                     |                 |
| 21 | X   | 27-05  |                            | Mª Ángeles Medina   | Eva Serrano         | Cristina Martínez   |                     |                 |
| 21 | J   | 28-05  |                            | Mª Ángeles Medina   | Eva Serrano         | Cristina Martínez   |                     |                 |
| 21 | V   | 29-05  |                            | Mª Ángeles Medina   | Eva Serrano         | Cristina Martínez   |                     |                 |
| 21 | S   | 30-05  |                            | Mª Ángeles Medina   | Eva Serrano         | Cristina Martínez   |                     |                 |
| 21 | D   | 31-05  |                            | Mª Ángeles Medina   | Eva Serrano         | Cristina Martínez   |                     |                 |
```

**PERIODO OTOÑO (Octubre - Diciembre):**

```
| S  | Día | Fecha  | Observaciones              | Slot 1              | Slot 2              | Slot 3              | Slot 4              | Slot 5          |
|----|-----|--------|----------------------------|---------------------|---------------------|---------------------|---------------------|-----------------|
| 22 | L   | 05-10  |                            | Solar               | Miguel Ruiz         | Virtu               | Boyer               |                 |
| 22 | M   | 06-10  |                            | Solar               | Miguel Ruiz         | Virtu               | Boyer               |                 |
| 22 | X   | 07-10  |                            | Solar               | Miguel Ruiz         | Virtu               | Boyer               |                 |
| 22 | J   | 08-10  |                            | Solar               | Miguel Ruiz         | Virtu               | Boyer               |                 |
| 22 | V   | 09-10  |                            | Solar               | Miguel Ruiz         | Virtu               | Boyer               |                 |
| 22 | S   | 10-10  |                            | Solar               | Miguel Ruiz         | Virtu               | Boyer               |                 |
| 22 | D   | 11-10  |                            | Solar               | Miguel Ruiz         | Virtu               | Boyer               |                 |
| 23 | L   | 12-10  | Fiesta Nacional            | Solar               | Miguel Ruiz         | Virtu               | Boyer               |                 |
| 23 | M   | 13-10  |                            | Solar               | Maria José Castillo | Emi                 | Boyer               |                 |
| 23 | X   | 14-10  |                            | Solar               | Maria José Castillo | Emi                 | Boyer               |                 |
| 23 | J   | 15-10  |                            | Solar               | Maria José Castillo | Emi                 | Boyer               |                 |
| 23 | V   | 16-10  |                            | Solar               | Maria José Castillo | Emi                 | Boyer               |                 |
| 23 | S   | 17-10  |                            | Solar               | Maria José Castillo | Emi                 | Boyer               |                 |
| 23 | D   | 18-10  |                            | Solar               | Maria José Castillo | Emi                 | Boyer               |                 |
| 24 | L   | 19-10  |                            | Duarte              | Maria José Castillo | Sopeña              | Morales             |                 |
| 24 | M   | 20-10  |                            | Duarte              | Antonio Román       | Sopeña              | Morales             |                 |
| 24 | X   | 21-10  |                            | Duarte              | Antonio Román       | Sopeña              | Morales             |                 |
| 24 | J   | 22-10  |                            | Duarte              | Antonio Román       | Sopeña              | Morales             | Carlos Fernández|
| 24 | V   | 23-10  |                            | Duarte              | Antonio Román       | Sopeña              | Morales             | Carlos Fernández|
| 24 | S   | 24-10  | San Rafael                 | Duarte              | Antonio Román       | Sopeña              | Morales             | Carlos Fernández|
| 24 | D   | 25-10  |                            | Duarte              | Antonio Román       | Sopeña              | Morales             | Carlos Fernández|
| 25 | L   | 26-10  |                            | Duarte              | Álvaro Muñiz        | Ana B. Pérez        | Eva Serrano         | Carlos Fernández|
| 25 | M   | 27-10  |                            | Duarte              | Álvaro Muñiz        | Ana B. Pérez        | Eva Serrano         | Carlos Fernández|
| 25 | X   | 28-10  |                            | Duarte              | Álvaro Muñiz        | Ana B. Pérez        | Eva Serrano         | Carlos Fernández|
| 25 | J   | 29-10  |                            | Duarte              | Álvaro Muñiz        | Ana B. Pérez        | Eva Serrano         |                 |
| 25 | V   | 30-10  |                            | Duarte              | Álvaro Muñiz        | Ana B. Pérez        | Eva Serrano         |                 |
| 25 | S   | 31-10  |                            | Duarte              | Álvaro Muñiz        | Ana B. Pérez        | Eva Serrano         |                 |
| 25 | D   | 01-11  |                            | Duarte              | Álvaro Muñiz        | Ana B. Pérez        | Eva Serrano         |                 |
| 26 | L   | 02-11  | Todos los Santos (traslado)| Duarte              | Álvaro Muñiz        | Ana B. Pérez        | Eva Serrano         |                 |
| 26 | M   | 03-11  |                            | Jose Antonio        | Puerto              | Cristina Martínez   |                     | Duarte          |
| 26 | X   | 04-11  |                            | Jose Antonio        | Puerto              | Cristina Martínez   |                     | Duarte          |
| 26 | J   | 05-11  |                            | Jose Antonio        | Puerto              | Cristina Martínez   |                     | Duarte          |
| 26 | V   | 06-11  |                            | Jose Antonio        | Puerto              | Cristina Martínez   |                     | Duarte          |
| 26 | S   | 07-11  |                            | Jose Antonio        | Puerto              | Cristina Martínez   |                     | Duarte          |
| 26 | D   | 08-11  |                            | Jose Antonio        | Puerto              | Cristina Martínez   |                     | Duarte          |
| 27 | L   | 09-11  |                            | Juan David          | Puerto              | Isaac Marcos        |                     | Duarte          |
| 27 | M   | 10-11  |                            | Juan David          | Ana Cristina        | Isaac Marcos        |                     | Duarte          |
| 27 | X   | 11-11  |                            | Juan David          | Ana Cristina        | Isaac Marcos        |                     | Duarte          |
| 27 | J   | 12-11  |                            | Juan David          | Ana Cristina        | Isaac Marcos        |                     | Duarte          |
| 27 | V   | 13-11  |                            | Juan David          | Ana Cristina        | Isaac Marcos        |                     | Duarte          |
| 27 | S   | 14-11  |                            | Juan David          | Ana Cristina        | Isaac Marcos        |                     | Duarte          |
| 27 | D   | 15-11  |                            | Juan David          | Ana Cristina        | Isaac Marcos        |                     | Duarte          |
| 28 | L   | 16-11  |                            | Inma                | Javier Carmona      | Isaac Marcos        | Pedro Molina        |                 |
| 28 | M   | 17-11  |                            | Inma                | Javier Carmona      | Isaac Marcos        | Pedro Molina        |                 |
| 28 | X   | 18-11  |                            | Inma                | Javier Carmona      | Isaac Marcos        | Pedro Molina        |                 |
| 28 | J   | 19-11  |                            | Inma                | Javier Carmona      | Isaac Marcos        | Pedro Molina        |                 |
| 28 | V   | 20-11  |                            | Inma                | Javier Carmona      | Isaac Marcos        | Pedro Molina        |                 |
| 28 | S   | 21-11  |                            | Inma                | Javier Carmona      | Isaac Marcos        | Pedro Molina        |                 |
| 28 | D   | 22-11  |                            | Inma                | Javier Carmona      | Isaac Marcos        | Sonia Gata          |                 |
| 29 | L   | 23-11  |                            | Alejandro León      | Javier Carmona      | Espejo              | Sonia Gata          |                 |
| 29 | M   | 24-11  |                            | Alejandro León      | Javier Carmona      | Espejo              | Sonia Gata          |                 |
| 29 | X   | 25-11  |                            | Alejandro León      | Javier Carmona      | Espejo              | Sonia Gata          |                 |
| 29 | J   | 26-11  |                            | Alejandro León      | Javier Carmona      | Espejo              | Sonia Gata          |                 |
| 29 | V   | 27-11  |                            | Alejandro León      | Javier Carmona      | Espejo              | Sonia Gata          |                 |
| 29 | S   | 28-11  |                            | Alejandro León      | Javier Carmona      | Espejo              | Sonia Gata          |                 |
| 29 | D   | 29-11  |                            | Alejandro León      | Javier Carmona      | Espejo              | Sonia Gata          |                 |
| 30 | L   | 30-11  |                            | Uclés               |                     |                     |                     |                 |
| 30 | M   | 01-12  |                            | Uclés               |                     |                     |                     |                 |
| 30 | X   | 02-12  |                            | Uclés               |                     |                     |                     |                 |
| 30 | J   | 03-12  |                            | Uclés               |                     |                     |                     |                 |
| 30 | V   | 04-12  |                            | Uclés               |                     |                     |                     |                 |
| 30 | S   | 05-12  |                            | Uclés               |                     |                     |                     |                 |
| 30 | D   | 06-12  |                            | Uclés               |                     |                     |                     |                 |
| 31 | L   | 07-12  |                            | Uclés               |                     |                     |                     |                 |
| 31 | M   | 08-12  |                            | Uclés               |                     |                     |                     |                 |
| 31 | X   | 09-12  |                            | Uclés               |                     |                     |                     |                 |
| 31 | J   | 10-12  |                            | Uclés               |                     |                     |                     |                 |
| 31 | V   | 11-12  |                            | Uclés               |                     |                     |                     |                 |
| 31 | S   | 12-12  |                            | Uclés               |                     |                     |                     |                 |
| 31 | D   | 13-12  |                            | Uclés               |                     |                     |                     |                 |
```

### 9.10 Festivos 2026

| Fecha | Festivo |
|-------|---------|
| 06/01 | Reyes |
| 28/02 | Día de Andalucía |
| 02/04 | Jueves Santo |
| 03/04 | Viernes Santo |
| 01/05 | Día del Trabajo |
| 12/10 | Fiesta Nacional |
| 24/10 | San Rafael (local) |
| 02/11 | Todos los Santos (traslado) |

---

## Paso 10: Clasificación de Trabajadores (Flujo Jerárquico)

### 10.1 Estructura de Filtros Progresivos

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                         FLUJO JERÁRQUICO DE TRABAJADORES (4 NIVELES)                               │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐   │
│  │ NIVEL 1: TRABAJADORES CON CONTRATO                                                          │   │
│  │ Todos los trabajadores con contrato en vigor (incluidos los que tienen excedencia)         │   │
│  └─────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                           │                                                         │
│                                           ▼ (menos excedencias)                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐   │
│  │ NIVEL 2: TRABAJADORES ACTUALES                                                              │   │
│  │ Todos menos aquellos que están de excedencia                                                │   │
│  └─────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                           │                                                         │
│                                           ▼ (menos baja larga duración)                             │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐   │
│  │ NIVEL 3: ELEGIBLES VACACIONES                                                               │   │
│  │ Los anteriores menos bajas de larga duración                                                │   │
│  │ → Paternidad/maternidad SÍ son elegibles para vacaciones                                   │   │
│  │ → Estos aparecen en el selector de vacaciones                                               │   │
│  └─────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                           │                                                         │
│                                           ▼ (menos patern/mat + vacaciones + baja corta + permisos)│
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐   │
│  │ NIVEL 4: CUADRANTE / CONTROL DE PRESENCIA                                                   │   │
│  │ Los anteriores que durante el día seleccionado de la semana de trabajo:                     │   │
│  │ - No estén de paternidad/maternidad                                                         │   │
│  │ - No estén de vacaciones                                                                    │   │
│  │ - No estén de baja de corta duración                                                        │   │
│  │ - No tengan permisos                                                                        │   │
│  │ - No tengan horas de representación                                                         │   │
│  │ (PENDIENTE DE DESARROLLO)                                                                   │   │
│  └─────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 10.2 NIVEL 1: Trabajadores con Contrato

**Definición:** Todos los trabajadores que tienen contrato en vigor en la empresa.

| Incluye | Tabla |
|---------|-------|
| Todos con contrato activo | `contratos_usuario` |
| Incluye trabajadores en excedencia | `nuevo_carihuela_jorge_excedencia` |

**Consulta SQL completa:**
```sql
-- NIVEL 1: Obtener todos los trabajadores con contrato en vigor
SELECT
    cu.codigo AS Cod,
    o.nombre AS Nombre,
    o.apellidos AS Apellidos,
    o.nombre_corto AS NomCorto,
    cu.horas_semanales AS Horas,
    DATE_FORMAT(cu.fecha_inicio, '%d/%m/%Y') AS F_Inicio,
    CASE
        WHEN cu.fecha_fin IS NULL THEN 'Indefinido'
        ELSE DATE_FORMAT(cu.fecha_fin, '%d/%m/%Y')
    END AS F_Fin,
    cu.centro_coste AS CodContr,
    CASE
        WHEN cu.fecha_fin IS NULL THEN 'Indefinido'
        ELSE 'Temporal'
    END AS TipoContr,
    COALESCE(
        (SELECT 'Excedencia' FROM nuevo_carihuela_jorge_excedencia e
         WHERE e.operador_id = o.id AND CURDATE() BETWEEN e.fecha_desde AND e.fecha_hasta),
        (SELECT 'Baja larga' FROM nuevo_carihuela_jorge_bajas_larga_duracion b
         WHERE b.operador_id = o.id AND b.fecha_hasta IS NULL),
        (SELECT 'Patern/Mat' FROM nuevo_carihuela_jorge_paternidad_maternidad p
         WHERE p.operador_id = o.id AND CURDATE() BETWEEN p.fecha_desde AND p.fecha_hasta),
        'Activo'
    ) AS Estado
FROM contratos_usuario cu
JOIN operadores o ON cu.operador_id = o.id
WHERE cu.deleted_at IS NULL
AND (cu.fecha_fin IS NULL OR cu.fecha_fin >= CURDATE())
ORDER BY o.apellidos, o.nombre;
```

### 10.3 NIVEL 2: Trabajadores Actuales

**Definición:** Todos los trabajadores con contrato **MENOS** los que están en excedencia.

| Excluye | Tabla |
|---------|-------|
| Excedencia voluntaria | `nuevo_carihuela_jorge_excedencia` |

**Consulta SQL completa:**
```sql
-- NIVEL 2: Trabajadores Actuales (sin excedencias)
SELECT
    cu.codigo AS Cod,
    o.nombre AS Nombre,
    o.apellidos AS Apellidos,
    o.nombre_corto AS NomCorto,
    cu.horas_semanales AS Horas,
    DATE_FORMAT(cu.fecha_inicio, '%d/%m/%Y') AS F_Inicio,
    CASE
        WHEN cu.fecha_fin IS NULL THEN 'Indefinido'
        ELSE DATE_FORMAT(cu.fecha_fin, '%d/%m/%Y')
    END AS F_Fin,
    COALESCE(
        (SELECT 'Baja larga' FROM nuevo_carihuela_jorge_bajas_larga_duracion b
         WHERE b.operador_id = o.id AND b.fecha_hasta IS NULL),
        (SELECT 'Patern/Mat' FROM nuevo_carihuela_jorge_paternidad_maternidad p
         WHERE p.operador_id = o.id AND CURDATE() BETWEEN p.fecha_desde AND p.fecha_hasta),
        'Activo'
    ) AS Estado
FROM contratos_usuario cu
JOIN operadores o ON cu.operador_id = o.id
WHERE cu.deleted_at IS NULL
AND (cu.fecha_fin IS NULL OR cu.fecha_fin >= CURDATE())
-- FILTRO NIVEL 2: Excluir trabajadores en excedencia
AND o.id NOT IN (
    SELECT e.operador_id
    FROM nuevo_carihuela_jorge_excedencia e
    WHERE CURDATE() BETWEEN e.fecha_desde AND e.fecha_hasta
)
ORDER BY o.apellidos, o.nombre;
```

### 10.4 NIVEL 3: Elegibles Vacaciones

**Definición:** Trabajadores Actuales **MENOS** bajas de larga duración.

| Excluye | Tabla |
|---------|-------|
| Baja larga duración | `nuevo_carihuela_jorge_bajas_larga_duracion` |

> **NOTA:** Los trabajadores en **paternidad/maternidad SÍ son elegibles** para seleccionar vacaciones.

**Consulta SQL completa:**
```sql
-- NIVEL 3: Elegibles Vacaciones (sin excedencias ni bajas largas)
-- IMPORTANTE: Paternidad/maternidad SÍ son elegibles
SELECT
    cu.codigo AS Cod,
    o.nombre AS Nombre,
    o.apellidos AS Apellidos,
    o.nombre_corto AS NomCorto,
    cu.horas_semanales AS Horas,
    -- Días de vacaciones correspondientes
    CASE
        WHEN cu.fecha_fin IS NULL THEN 30
        ELSE ROUND(DATEDIFF(cu.fecha_fin, cu.fecha_inicio) / 365 * 30)
    END AS DiasCorresp,
    -- Días ya planificados
    COALESCE(
        (SELECT SUM(v.dias) FROM nuevo_carihuela_jorge_vacaciones v
         WHERE v.operador_id = o.id AND YEAR(v.fecha_desde) = YEAR(CURDATE())),
        0
    ) AS DiasPlanif,
    -- Días pendientes
    CASE
        WHEN cu.fecha_fin IS NULL THEN 30
        ELSE ROUND(DATEDIFF(cu.fecha_fin, cu.fecha_inicio) / 365 * 30)
    END - COALESCE(
        (SELECT SUM(v.dias) FROM nuevo_carihuela_jorge_vacaciones v
         WHERE v.operador_id = o.id AND YEAR(v.fecha_desde) = YEAR(CURDATE())),
        0
    ) AS DiasPendientes
FROM contratos_usuario cu
JOIN operadores o ON cu.operador_id = o.id
WHERE cu.deleted_at IS NULL
AND (cu.fecha_fin IS NULL OR cu.fecha_fin >= CURDATE())
-- FILTRO NIVEL 2: Excluir excedencias
AND o.id NOT IN (
    SELECT e.operador_id
    FROM nuevo_carihuela_jorge_excedencia e
    WHERE CURDATE() BETWEEN e.fecha_desde AND e.fecha_hasta
)
-- FILTRO NIVEL 3: Excluir bajas largas
AND o.id NOT IN (
    SELECT b.operador_id
    FROM nuevo_carihuela_jorge_bajas_larga_duracion b
    WHERE b.fecha_hasta IS NULL  -- Baja sin fecha de fin = activa
)
ORDER BY o.apellidos, o.nombre;
```

**Uso:** Estos trabajadores aparecen en el **selector de vacaciones** del módulo ERP.

### 10.5 NIVEL 4: Cuadrante / Control de Presencia

**Definición:** Elegibles Vacaciones que durante el **día seleccionado** de la semana de trabajo están disponibles para trabajar.

| Excluye (ese día) | Tabla | Exclusión |
|-------------------|-------|-----------|
| Paternidad/Maternidad | `nuevo_carihuela_jorge_paternidad_maternidad` | Día completo |
| Vacaciones | `nuevo_carihuela_jorge_vacaciones` | Día completo |
| Baja corta duración | `eventos_incidencias_colores` (id=66) | Día completo |
| Permisos | Varias tablas | Día completo o parcial |
| Horas de representación | `nuevo_carihuela_jorge_representantes_horas` | Solo esas horas |
| Lactancia | `nuevo_carihuela_jorge_lactancia` | Según tipo |

**Consulta SQL (PENDIENTE DE DESARROLLO):**
```sql
-- NIVEL 4: Cuadrante / Control de Presencia para fecha específica
-- Parámetro: @fecha_consulta = fecha del día a consultar

SET @fecha_consulta = '2026-02-17';

SELECT
    cu.codigo AS Cod,
    o.nombre AS Nombre,
    o.apellidos AS Apellidos,
    o.nombre_corto AS NomCorto,
    cu.horas_semanales AS HorasContrato,
    'DISPONIBLE' AS Estado
FROM contratos_usuario cu
JOIN operadores o ON cu.operador_id = o.id
WHERE cu.deleted_at IS NULL
AND (cu.fecha_fin IS NULL OR cu.fecha_fin >= @fecha_consulta)
-- FILTRO NIVEL 2: Sin excedencias
AND o.id NOT IN (
    SELECT e.operador_id
    FROM nuevo_carihuela_jorge_excedencia e
    WHERE @fecha_consulta BETWEEN e.fecha_desde AND e.fecha_hasta
)
-- FILTRO NIVEL 3: Sin bajas largas
AND o.id NOT IN (
    SELECT b.operador_id
    FROM nuevo_carihuela_jorge_bajas_larga_duracion b
    WHERE b.fecha_hasta IS NULL
)
-- FILTRO NIVEL 4: Sin paternidad/maternidad ese día
AND o.id NOT IN (
    SELECT p.operador_id
    FROM nuevo_carihuela_jorge_paternidad_maternidad p
    WHERE @fecha_consulta BETWEEN p.fecha_desde AND p.fecha_hasta
)
-- FILTRO NIVEL 4: Sin vacaciones ese día
AND o.id NOT IN (
    SELECT v.operador_id
    FROM nuevo_carihuela_jorge_vacaciones v
    WHERE @fecha_consulta BETWEEN v.fecha_desde AND v.fecha_hasta
)
-- FILTRO NIVEL 4: Sin baja corta ese día (PENDIENTE: vincular con eventos_incidencias_colores)
-- FILTRO NIVEL 4: Sin permisos ese día (PENDIENTE)
-- FILTRO NIVEL 4: Descontar horas de representación (PENDIENTE)
ORDER BY o.apellidos, o.nombre;
```

**Estado:** PENDIENTE DE DESARROLLO

### 10.6 Resumen Visual

| Nivel | Nombre | Excluye | Uso |
|-------|--------|---------|-----|
| 1 | Trabajadores con Contrato | - | Base |
| 2 | Trabajadores Actuales | Excedencia | General |
| 3 | Elegibles Vacaciones | Baja larga | Selector vacaciones |
| 4 | Cuadrante/Control Presencia | Patern/mat + Vacaciones + Baja corta + Permisos + Horas rep | Horarios (PENDIENTE) |

---

## Paso 11: Vistas ERP por Niveles

### 11.1 VISTA NIVEL 1: Trabajadores con Contrato

**Descripción:** Formulario para gestionar todos los trabajadores con contrato en vigor (incluidos los que están en excedencia).

**Interfaz ERP - Formulario editable:**

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ NIVEL 1: TRABAJADORES CON CONTRATO                                                                             │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                 │
│ [+ NUEVO TRABAJADOR]                                                                                            │
│                                                                                                                 │
│ ┌───────┬───────────┬─────────────────┬──────────┬───────┬──────────┬──────────┬────────┬──────────┬──────────┬──────────┬──────────┐
│ │Cód ▲▼ │ Nombre ▲▼ │ Apellidos ▲▼    │NomCorto▲▼│Horas▲▼│ F.Inicio │ F.Fin ▲▼ │CódContr│TipoContr▲│ Estado ▲▼│ Desde ▲▼ │ Hasta    │
│ ├───────┼───────────┼─────────────────┼──────────┼───────┼──────────┼──────────┼────────┼──────────┼──────────┼──────────┼──────────┤
│ │ 110   │ Alejandro │ Moreno Blanes   │A. Moreno │ 40    │01/08/2019│Indefinido│ 100    │Indefinido│ Activo   │          │          │
│ │ 111   │ Cristina  │ Moraleda Cerrato│C. Morale.│ 40    │15/03/2020│Indefinido│ 100    │Indefinido│ Activo   │          │          │
│ │ 038   │ Soledad   │ León Fernández  │S. León   │ 40    │01/01/2015│Indefinido│ 100    │Indefinido│Excedencia│01/02/2026│01/08/2026│
│ │ 097   │ Francisco │ Cabello Sánchez │F. Cabello│ 40    │01/06/2018│Indefinido│ 100    │Indefinido│Baja larga│15/01/2026│          │
│ │ 257   │ José Ant. │ Velasco Madrid  │J. Velasco│ 40    │13/01/2026│12/04/2026│ 200    │ Temporal │ Activo   │          │          │
│ │ ...   │ ...       │ ...             │ ...      │ ...   │ ...      │ ...      │ ...    │ ...      │ ...      │ ...      │ ...      │
│ └───────┴───────────┴─────────────────┴──────────┴───────┴──────────┴──────────┴────────┴──────────┴──────────┴──────────┴──────────┘
│                                                                                                                 │
│ ═══════════════════════════════════════════════════════════════════════════════════════════════════════════   │
│ FORMULARIO DE EDICIÓN (al pulsar fila o [+ NUEVO])                                                              │
│ ═══════════════════════════════════════════════════════════════════════════════════════════════════════════   │
│ DATOS DEL CONTRATO                                                                                              │
│ ───────────────────────────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                                                 │
│ Código:              [110        ]                                                                              │
│                                                                                                                 │
│ Nombre:              [Alejandro                 ]                                                               │
│                                                                                                                 │
│ Apellidos:           [Moreno Blanes             ]                                                               │
│                                                                                                                 │
│ Nombre corto:        [A. Moreno     ]  (para vacaciones y cuadrante)                                            │
│                                                                                                                 │
│ Fecha inicio:        [01/08/2019  📅]                                                                           │
│                                                                                                                 │
│ Fecha fin:           [            📅]  ☐ Indefinido                                                            │
│                                                                                                                 │
│ Centro de coste:     [100 - Producción          ▼]                                                             │
│                                                                                                                 │
│ Horas semanales:     [40         ]                                                                              │
│                                                                                                                 │
│ Categoría:           [V.a.2. T-3                ▼]                                                             │
│                                                                                                                 │
│ Tipo contrato:       [Indefinido                ▼]                                                             │
│                                                                                                                 │
│ ═══════════════════════════════════════════════════════════════════════════════════════════════════════════   │
│ SITUACIÓN ACTUAL                                                                                                │
│ ───────────────────────────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                                                 │
│ ☐ Excedencia         Desde: [          📅]  Hasta: [          📅]                                              │
│                                                                                                                 │
│ ☐ Baja larga         Desde: [          📅]  Sustituto: [                    ▼]                                 │
│                                                                                                                 │
│ ☐ Paternidad/Matern  Desde: [          📅]  Hasta: [          📅]                                              │
│                                                                                                                 │
│ ═══════════════════════════════════════════════════════════════════════════════════════════════════════════   │
│                                                                                                                 │
│ [GUARDAR]    [CANCELAR]    [ELIMINAR]                                                                           │
│                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Campos editables:**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| Código | Texto | Código del trabajador |
| Nombre | Texto | Nombre del trabajador |
| Apellidos | Texto | Apellidos del trabajador |
| Nombre corto | Texto | Nombre abreviado para vacaciones y cuadrante |
| Fecha inicio | Fecha | Fecha inicio contrato actual |
| Fecha fin | Fecha | Fecha fin contrato (vacío si indefinido) |
| Indefinido | Checkbox | Marcar si contrato indefinido |
| Centro de coste | Dropdown | Selector de centro de coste |
| Horas semanales | Número | Horas de jornada semanal |
| Categoría | Dropdown | Categoría profesional |
| Tipo contrato | Dropdown | Indefinido / Temporal |

**Casillas de situación (Estado):**

| Estado | Campos | Descripción |
|--------|--------|-------------|
| ☐ Excedencia | Desde, Hasta | Periodo de excedencia voluntaria |
| ☐ Baja larga | Desde, Sustituto | Baja de larga duración (sin fecha fin) con sustituto asignado |
| ☐ Paternidad/Maternidad | Desde, Hasta | Permiso por nacimiento/adopción |

> **NOTA:** Al marcar una casilla de estado, se habilitan los campos Desde/Hasta correspondientes y el trabajador pasa a ese estado.

**Acciones:**

| Botón | Acción |
|-------|--------|
| GUARDAR | Guarda los cambios del formulario |
| CANCELAR | Descarta los cambios |
| ELIMINAR | Elimina el registro (baja del trabajador) |
| + NUEVO | Crear nuevo trabajador |

---

### 11.2 VISTA NIVEL 2: Trabajadores Actuales

**Descripción:** Misma vista que Nivel 1 con filtro `Estado != 'Excedencia'`

No aparecen los trabajadores en excedencia.

---

### 11.3 VISTA NIVEL 3: Elegibles Vacaciones

**Descripción:** Nivel 2 menos los de baja larga. Paternidad/maternidad SÍ son elegibles.

**Filtro:** `Estado != 'Baja larga'`

**Tres vistas disponibles:**

#### 11.3.1 Vista: Vacaciones 2026 (Resumen anual)

Datos automáticos desde la pestaña Elegibles Vacaciones.

```
┌─────┬───────────┬─────────────────┬──────────┬──────────┬─────┬──────────┬──────────┬─────┬──────────┬──────────┬─────┬──────────┬──────────┬─────┬───────┬────────┬───────┐
│     │           │                 │      INVIERNO P1    │Tot  │      INVIERNO P2    │Tot  │       VERANO P1     │Tot  │       VERANO P2     │Tot  │ Días  │ Días   │       │
│ID▲▼ │ Nombre ▲▼ │ Apellidos ▲▼    │ Desde    │ Hasta    │ P1  │ Desde    │ Hasta    │ P2  │ Desde    │ Hasta    │ P1  │ Desde    │ Hasta    │ P2  │Totales│Corresp │ Difer │
├─────┼───────────┼─────────────────┼──────────┼──────────┼─────┼──────────┼──────────┼─────┼──────────┼──────────┼─────┼──────────┼──────────┼─────┼───────┼────────┼───────┤
│ 110 │ Alejandro │ Moreno Blanes   │02/02/2026│16/02/2026│ 15  │          │          │  0  │          │          │  0  │          │          │  0  │  15   │   30   │  -15  │
│ 059 │ Francisco │ Soto Alcolea    │02/02/2026│16/02/2026│ 15  │          │          │  0  │03/08/2026│17/08/2026│ 15  │          │          │  0  │  30   │   30   │   0   │
│ 111 │ Cristina  │ Moraleda Cerrato│10/02/2026│17/02/2026│  8  │10/03/2026│17/03/2026│  8  │03/08/2026│10/08/2026│  8  │17/08/2026│22/08/2026│  6  │  30   │   30   │   0   │
│ 005 │ Fernando  │ Torralbo Acuña  │          │          │  0  │          │          │  0  │          │          │  0  │          │          │  0  │   0   │   30   │  -30  │
│ ... │ ...       │ ...             │ ...      │ ...      │ ... │ ...      │ ...      │ ... │ ...      │ ...      │ ... │ ...      │ ...      │ ... │  ...  │  ...   │  ...  │
└─────┴───────────┴─────────────────┴──────────┴──────────┴─────┴──────────┴──────────┴─────┴──────────┴──────────┴─────┴──────────┴──────────┴─────┴───────┴────────┴───────┘
```

> **NOTA:** Puede haber más periodos (P3, P4...) según necesidades del trabajador.

#### 11.3.2 Vista: Vacaciones Invierno 2026

*Misma estructura que la definida en sección 9.8*

#### 11.3.3 Vista: Vacaciones Verano 2026

*Misma estructura que la definida en sección 9.8*

---

### 11.4 VISTA NIVEL 4: Cuadrante / Control de Presencia

*PENDIENTE DE DESARROLLO*

---

### 10.7 Disponibilidad Parcial (por horas)

**Importante:** En el NIVEL 4, la disponibilidad se calcula por **día Y hora**, no solo por día completo.

**Ejemplo:** Clara solicita permiso de 2 horas (08:00-10:00)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ DISPONIBILIDAD - Clara Muñoz - Lunes 17/02/2026                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Jornada: 08:00 - 16:00 (8 horas)                                          │
│                                                                             │
│  | Hora        | Estado           | Observación                  |         │
│  |-------------|------------------|------------------------------|         │
│  | 08:00-10:00 | ❌ NO DISPONIBLE | Permiso solicitado (2 horas) |         │
│  | 10:00-16:00 | ✅ DISPONIBLE    | Resto de jornada             |         │
│                                                                             │
│  Total disponible: 6 horas de 8                                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Regla de vacaciones:**

> El trabajador está **NO DISPONIBLE** solo durante los días de disfrute. El día siguiente al último día de vacaciones **YA está disponible**.

**Ejemplo:**
```
VACACIONES Clara: 02/02/2026 - 16/02/2026

| Fecha      | Día    | Estado         |
|------------|--------|----------------|
| 16/02/2026 | Lunes  | ❌ VACACIONES  | ← Último día
| 17/02/2026 | Martes | ✅ DISPONIBLE  | ← Ya disponible
```

### 10.8 Periodo del Cuadrante Horario

| Campo | Valor |
|-------|-------|
| Días habituales | Lunes a Sábado |
| Domingo | Normalmente no se trabaja (excepto excepciones) |

---

## RESUMEN DE PENDIENTES PARA PRODUCCIÓN

### Pendientes de Desarrollo

| # | Módulo | Descripción | Prioridad |
|---|--------|-------------|-----------|
| 1 | Calendario | Confirmar si domingos y festivos son laborables | ALTA |
| 2 | Nivel 4 | Desarrollar vista Cuadrante/Control de Presencia | ALTA |
| 3 | Vacaciones | Interfaz de usuario para solicitud de vacaciones | ALTA |
| 4 | Vacaciones | Validar máximo 5 trabajadores simultáneos | ALTA |
| 5 | Vacaciones | Comparación con año anterior | MEDIA |
| 6 | Ausencias | Vincular `eventos_incidencias_colores` con tablas de ausencias | MEDIA |
| 7 | Sindicales | Automatizar solicitud de crédito horario por email | BAJA |

### Tablas a Crear

```sql
-- Ejecutar en orden:
1. nuevo_carihuela_jorge_configuracion_calendario
2. nuevo_carihuela_jorge_calendario_anual
3. nuevo_carihuela_jorge_semanas_anuales
4. nuevo_carihuela_jorge_vacaciones (si no existe)
5. nuevo_carihuela_jorge_vacaciones_balance
6. nuevo_carihuela_jorge_vacaciones_solicitudes
7. nuevo_carihuela_jorge_vacaciones_canceladas
```

### Procedimientos a Ejecutar

```sql
-- Ejecutar cada año nuevo:
CALL generar_calendario_anual(2026);
CALL generar_semanas_anuales(2026);
```

### Configuración Inicial

1. Definir días laborables en `nuevo_carihuela_jorge_configuracion_calendario`
2. Añadir festivos específicos del año en `diasfestivos`
3. Asignar `nombre_corto` a todos los trabajadores en `operadores`

---

*Documento generado: 2026-02-17*
*Última actualización: 2026-02-17*
*Versión: PRODUCCIÓN*

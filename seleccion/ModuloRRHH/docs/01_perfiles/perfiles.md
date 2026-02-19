# MODULO RRHH - PERFILES

## 1. Perfiles Disponibles

| Codigo | Nombre | Oferta Titulo | Keywords |
|--------|--------|---------------|----------|
| PESCADERIA | Pescaderia | Dependiente/a de Pescaderia | pescad, carnicer, dependient, tienda, comercio |
| LOGISTICA | Logistica | Operario/a de Logistica de Almacen | logistic, almacen, reparto, conductor, carnet C |
| PRODUCCION | Produccion | Operario/a de Produccion | sushi, envase, produccion, operario, fabrica |
| ADMINISTRATIVO | Administrativo | Administrativo/a | secretari, administrativ, contab, oficina |
| GESTION | Gestion | Responsable de Area | grado ade, derecho, universidad, master |
| BECARIO | Becario | Becario/a en Practicas | becario, practicas, estudiante, formacion |

---

## 2. Tabla SQL: perfiles

```sql
CREATE TABLE IF NOT EXISTS perfiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL COMMENT 'Codigo unico del perfil',
    nombre VARCHAR(100) NOT NULL COMMENT 'Nombre visible del perfil',
    descripcion TEXT COMMENT 'Descripcion del perfil y oferta de empleo',
    keywords TEXT COMMENT 'Palabras clave separadas por coma para clasificacion',
    activo TINYINT(1) DEFAULT 1 COMMENT '1=Activo, 0=Inactivo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 3. Peticion de Trabajador

### 3.1 Descripcion

El proceso comienza cuando el **Gerente** o el **Director de RRHH** solicita un nuevo trabajador.

### 3.2 Flujo

```
GERENTE / DIRECTOR RRHH
         |
         v
+---------------------------+
| Crear peticion de         |
| trabajador                |
+---------------------------+
         |
         v
+---------------------------+
| Seleccionar PERFIL        |
+---------------------------+
         |
         v
+---------------------------+
| Peticion CREADA           |
| Estado: ABIERTA           |
+---------------------------+
         |
         v
+---------------------------+
| Publicar oferta en        |
| portal (InfoJobs, etc.)   |
+---------------------------+
```

### 3.3 Datos de la Peticion

| Campo | Descripcion | Obligatorio |
|-------|-------------|-------------|
| ID | Identificador unico | Auto |
| Perfil | PESCADERIA, LOGISTICA, PRODUCCION, ADMINISTRATIVO, GESTION, BECARIO | SI |
| Posicion | Nombre especifico del puesto | SI |
| Plazas | Numero de vacantes | SI |
| Prioridad | MUY_ALTA, ALTA, MEDIA, BAJA, MUY_BAJA | SI |
| Solicitante | Gerente o Director RRHH | Auto |
| Fecha Solicitud | Fecha de creacion | Auto |
| Portal | Donde se publica (InfoJobs, LinkedIn, etc.) | NO |
| Desde | Fecha inicio publicacion | NO |
| Hasta | Fecha fin publicacion | NO |
| Estado | ACTIVA, INACTIVA | Auto |

### 3.4 Prioridades

| Prioridad | Orden | Uso |
|-----------|-------|-----|
| MUY_ALTA | 1 | Urgente, cubrir inmediatamente |
| ALTA | 2 | Prioritario |
| MEDIA | 3 | Normal (por defecto) |
| BAJA | 4 | Puede esperar |
| MUY_BAJA | 5 | Sin urgencia |

### 3.5 Estados de la Oferta

| Estado | Descripcion |
|--------|-------------|
| ACTIVA | Anuncio publicado en internet con fechas desde/hasta |
| INACTIVA | Anuncio no visible |

**Nota:** Las fechas **Desde** y **Hasta** determinan el periodo de publicacion de la oferta.

---

## 4. Ofertas de Empleo por Perfil

### 4.1 LOGISTICA - Operario/a de Logistica de Almacen

```
DESCRIPCION:
EMPRESA DEL SECTOR DE PESCADOS Y MARISCOS, UBICADA EN MERCACORDOBA,
BUSCA INCORPORAR UNA PERSONA PARA JORNADA COMPLETA.

FUNCIONES PRINCIPALES:
- Descarga y recepcion de mercancia
- Preparacion de pedidos
- Almacenaje y organizacion de productos
- Carga de mercancia para clientes

OTRAS FUNCIONES:
- Limpieza y orden del area de trabajo
- Transporte interno de mercancia
- Apoyo en corte y fileteado cuando sea necesario

REQUISITOS IMPRESCINDIBLES:
- Carnet y manejo de carretilla elevadora
- Carnet de conducir
- Disponibilidad para trabajar en horario de madrugada (a partir de las 2:00h)
- Buena disposicion fisica para tareas de carga/descarga

REQUISITOS VALORABLES:
- Carnet C+CAP
- Experiencia previa en almacen, logistica o puestos similares

FORMACION/APRENDIZAJE:
- No es necesario conocimiento previo de pescados y mariscos, pero si
  capacidad y disposicion para aprender

SE OFRECE:
- Contrato a jornada completa
- Horario de lunes a sabado (entrada a partir de las 2:00h)
- Salario segun convenio y experiencia (17.000-23.000 EUR bruto/ano)
- Posibilidad de promocion interna
- Otros beneficios
```

### 4.2 PESCADERIA - Dependiente/a de Pescaderia

```
DESCRIPCION:
Nos encontramos en la busqueda de Dependientes/as de Pescaderia que se
encarguen de la venta, preparacion y manipulacion de una amplia variedad
de productos del mar en una pescaderia de referencia.

RESPONSABILIDADES Y FUNCIONES:
- Atencion al cliente y asesoramiento sobre la seleccion y preparacion
  de los productos del mar
- Manipulacion y corte de pescado y mariscos
- Ordenamiento, rotacion y almacenamiento de existencias
- Recepcion y verificacion de la mercancia en el obrador
- Colaboracion en la preparacion y presentacion de los productos
- Mantenimiento de la limpieza y orden del area de trabajo

REQUISITOS:
- Experiencia previa en el sector de industria alimentaria, preferiblemente
  en pescaderia o venta al detalle de alimentos
- Dominio de las tecnicas de pescado, manipulacion de cuchillo, carniceria
  y almacenamiento de existencias
- Habilidades de atencion al cliente
- Compromiso con la calidad, la higiene y la seguridad
- Flexibilidad para adaptarse a los horarios

SE OFRECE:
- Oportunidad de formar parte de un equipo comprometido y en constante crecimiento
- Desarrollo de habilidades profesionales
- Posibilidad de contribuir al exito de nuestra pescaderia
```

### 4.3 Vista en el programa ERP Carihuela

| Perfil | Titulo Oferta | Contenido | Estado |
|--------|---------------|-----------|--------|
| PESCADERIA | Dependiente/a de Pescaderia | Funciones, requisitos, condiciones | Documentada |
| LOGISTICA | Operario/a de Logistica de Almacen | Funciones, requisitos, salario | Documentada |
| PRODUCCION | Operario/a de Produccion | - | Pendiente |
| ADMINISTRATIVO | Administrativo/a | - | Pendiente |
| GESTION | Responsable de Area | - | Pendiente |
| BECARIO | Becario/a en Practicas | - | Pendiente |

---

## 5. Vista Dashboard - Ofertas por Perfil

Ordenadas por prioridad.

```
+=========================================================================================================================+
|  OFERTAS DE EMPLEO POR PERFIL (ordenadas por prioridad)                                                                 |
+=========================================================================================================================+
|                                                                                                                         |
|  +-----------+--------------+----------------------------+--------+----------+-----------+-----------+----------+------+
|  | Prioridad | Perfil       | Titulo                     | Plazas | Creacion | Portal    | Publicada | Desde    | Hasta|
|  +-----------+--------------+----------------------------+--------+----------+-----------+-----------+----------+------+
|  | MUY_ALTA  | PESCADERIA   | Dependiente/a Pescaderia   |   2    |13/02/2026| InfoJobs  | [x]       |13/02/2026|14/04 |
|  | ALTA      | LOGISTICA    | Operario/a Logistica       |   2    |15/01/2026| InfoJobs  | [x]       |27/01/2026|28/03 |
|  | MEDIA     | BECARIO      | Becario Administracion     |   1    |01/02/2026|    -      | [ ]       |    -     |  -   |
|  | -         | PRODUCCION   | Operario/a Produccion      |   0    |    -     |    -      | [ ]       |    -     |  -   |
|  | -         | ADMINISTRAT. | Administrativo/a           |   0    |    -     |    -      | [ ]       |    -     |  -   ||
|  | GESTION      | Responsable de Area        |   0    |    -     |    -      | [ ]       |    -     |    -     ||
|  | BECARIO      | Becario Administracion     |   1    |01/02/2026|    -      | [ ]       |    -     |    -     ||
|  +--------------+----------------------------+--------+----------+-----------+-----------+----------+----------++
|                                                                                                                  |
+==================================================================================================================+
```

---

## 6. Ubicacion de Datos

| Tabla | Ubicacion | Descripcion |
|-------|-----------|-------------|
| `perfiles` | BD: 192.168.1.133 | Perfiles + ofertas de empleo |
| `peticiones_trabajador` | BD: 192.168.1.133 | Peticiones de personal |

---

*Documento generado: ModuloRRHH v1.0*

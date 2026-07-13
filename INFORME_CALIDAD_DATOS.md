# Informe de calidad de datos

## Resumen ejecutivo

El archivo `datos_congreso.xlsx` contiene una base administrativa ya trabajada, con una hoja principal de gestion (`HOJA MAESTRA`), copias de origen, vistas automaticas, controles de integridad y un respaldo textual del CSV original.

La estructura es suficiente para importar personas, autorias, modalidades, areas, estados, incidencias, responsables, acciones pendientes y asignaciones futuras a paneles/sesiones. Sin embargo, no contiene campos visibles para titulos de comunicaciones, resumenes, palabras clave como texto ni datos completos de simposios. Esos datos deberan incorporarse posteriormente desde otra fuente.

## Controles de integridad

Valores que deben conservarse y verificarse en la importacion:

- `ORDEN LLEGADA`: 173 filas, incluyendo cabecera y 172 propuestas.
- `HOJA MAESTRA`: 173 filas.
- `POR PANELES`: 161 filas activas segun `COMPROBACION`, incluyendo cabecera y 160 registros.
- `ORDEN LLEGADA`: 28 columnas originales (`A:AB`).
- `POR PANELES`: la comprobacion indica 22 columnas originales (`A:V`), aunque la hoja visible contiene 23 columnas con `NOTIFICADO` en `W`; requiere confirmacion.
- Hash `ORDEN`: `d50276d8fce9c0b3dd0a889597c512ae15015da6da7520bfc27c1a9c63e51e5e`.
- Hash `POR PANELES`: `ba8a44b49a2a74da16a3239727d54fd69a674fb3011f8080d0879263ee0ea7f8`.
- `CSV_ORIGEN_RAW`: 174 lineas, cabecera interna mas 173 lineas de CSV original.

## Distribucion principal

- Modalidades originales: 162 `Comunicación`, 8 `Simposio`, 1 `Taller`, 1 `COMUNICACION`.
- Modalidades normalizadas: 163 `Comunicación`, 8 `Simposio`, 1 `Taller`.
- Estados cientificos: 160 `Aceptado`, 7 `Duplicado`, 4 `Pendiente`, 1 `Duda`.
- Estados formales: 138 `Correcto`, 34 `Subsanar`.
- Estados de notificacion: 150 `Notificado`, 21 `No notificado`, 1 `Duplicado`.
- Estados generales: 119 `Cerrado`, 53 `Pendiente`.
- Acciones pendientes: 112 `Sin acción`, 32 `Pedir subsanación`, 20 `Notificar`, 7 `Revisar duplicado`, 1 `Revisar decisión`.
- Responsables: 172 `Pendiente asignar`.
- Asistencia confirmada: 172 `Pendiente`.

## Problemas detectados

### Variantes de nombres

Hay 306 entradas de autoria y 229 nombres normalizados unicos. Se detectan 62 grupos de nombres repetidos. Muchos son coautorias legitimas o personas con varias propuestas, pero deben revisarse para conflictos de agenda y posibles duplicados.

Ejemplos:

- `PLASENCIA CARBALLO, ZEUS` / `Plasencia Carballo, Zeus`.
- `Barros Gonzalez, Oscar` / `Barros Gonzalez, Óscar`.
- Personas con varias propuestas: Natalia Barranco Izquierdo, Maria Perez Hernandez, Mario Ferreras Listan, Natalia Suarez Rubio, Celia Morales Rando.

### Instituciones escritas de forma diferente

Hay 304 entradas de institucion, 90 variantes literales y al menos 7 grupos con variantes normalizables.

Ejemplos:

- `Universitat de València`, `UNIVERSITAT DE VALÈNCIA`, `Universitat de Valencia`.
- `Universidad de La Laguna`, `Universidad de la Laguna`.
- `Universidad de Málaga`, `UNIVERSIDAD DE MÁLAGA`.
- `Universidad de Castilla-La Mancha`, `UNIVERSIDAD DE CASTILLA-LA MANCHA`.
- `Universidad Andres Bello`, `Universidad Andrés Bello`.
- Abreviaturas como `UCM`, `UAM` o `UTAMED` conviven con nombres completos.

### Correos repetidos

Hay 305 correos de autoria, 217 correos normalizados unicos y 65 grupos repetidos. No todos son errores: muchos indican una misma persona en varias propuestas o coautorias compartidas.

Ejemplos de repeticion:

- `natalia.barranco@uva.es`: 4 apariciones.
- `mperez57@us.es`: 4 apariciones.
- `coralhuntg@us.es`: 4 apariciones.
- `mferreras@us.es`: 4 apariciones.
- `nsuaru@ull.edu.es`: 4 apariciones.
- `cmorales@ull.edu.es`: 4 apariciones.
- Caso con variante de tilde en correo: `monica.ruiz@ua.es` / `mónica.ruiz@ua.es`.

### Posibles propuestas duplicadas

La columna `Posible duplicado` marca 64 filas con `Sí`, mientras que `Estado científico` marca 7 como `Duplicado`. La aplicacion debe diferenciar:

- Duplicado confirmado.
- Posible duplicado pendiente de revision.
- Repeticion legitima de persona en varias propuestas.

Ejemplos de combinaciones repetidas de primera autoria/correo:

- `SIDLL26-040`, `SIDLL26-041`, `SIDLL26-045`, `SIDLL26-106`.
- `SIDLL26-015`, `SIDLL26-016`, `SIDLL26-020`.
- `SIDLL26-013`, `SIDLL26-018`.
- `SIDLL26-023`, `SIDLL26-024`.
- `SIDLL26-140`, `SIDLL26-141`, `SIDLL26-167`, `SIDLL26-168` aparecen relacionados por correos compartidos.

### Valores vacios

Vacios relevantes en `HOJA MAESTRA`:

- `VISTO BUENO`: 2 vacios.
- `NOTIFICADO`: 20 vacios.
- `Subpanel`, `Sesión`, `Orden intervención`: 172 vacios cada uno, por tanto la programacion todavia no esta asignada en esa hoja.
- `Observación interna`: 172 vacios.
- `Fecha revisión`, `Fecha notificación`, `Fecha última actualización`, `Motivo reubicación`: 172 vacios.
- `Observación comunicable`: 113 vacios.
- Campos de autoria 2, 3 y 4 tienen muchos vacios, esperables porque no todas las propuestas tienen cuatro autorias.

### Formulas con errores

La columna `Autoría breve` (`BC`) muestra 172 errores `#NAME?`. La formula usa `_xludf.TEXTJOIN`, lo que indica una funcion no reconocida en el entorno de lectura o compatibilidad.

La aplicacion no debe depender del valor calculado de esa columna; debe recalcular la autoria breve internamente a partir de los bloques de autoria.

### Valores no normalizados

- Modalidad: existe `COMUNICACION`, normalizable a `Comunicación`.
- Area: existe `2.Interculturalidad`, normalizable a `2. Interculturalidad`.
- Area: existe `Derivado a Panel 6 (Educación Literaria)`, que no pertenece a las siete areas controladas y requiere decision: area definitiva, motivo de reubicacion o incidencia.

### Columnas originales sin encabezado claro

`ORDEN LLEGADA` contiene seis columnas originales sin encabezado (`W:AB`). En `HOJA MAESTRA` aparecen como `ORIG_COL_23` a `ORIG_COL_28`.

Tienen algunos valores no vacios:

- `ORIG_COL_23`: 6 valores.
- `ORIG_COL_24`: 3 valores.
- `ORIG_COL_25`: 3 valores.
- `ORIG_COL_26`: 2 valores.
- `ORIG_COL_27`: 2 valores.
- `ORIG_COL_28`: 1 valor.

No deben descartarse. Deben conservarse con nombre tecnico estable y origen completo.

## Carencias de contenido

No se han encontrado columnas visibles para:

- Titulos de comunicaciones.
- Resumenes.
- Palabras clave como lista o texto; solo existe el indicador `Falta palabras clave`.
- Datos completos de simposios, como titulo del simposio, coordinacion, descripcion, comunicaciones internas o estructura propia.
- Aulas, dias o franjas definitivas de programa.

Consecuencia: la primera importacion puede cargar la base administrativa y las autorias, pero la aplicacion debe permitir incorporar despues esos campos desde otro Excel, CSV o formulario.

## Restricciones desde `excepciones.docx`

Se detectan dos restricciones:

| Persona | Restriccion | Estructura propuesta |
| --- | --- | --- |
| Gerardo Fernandez San Emeterio | Debe programarse el viernes por la mañana por circunstancias docentes. | `must_schedule`, viernes, mañana, prioridad alta, preferente u obligatoria pendiente de confirmacion. |
| Boris Vazquez | No puede el miercoles por la tarde. | `cannot_schedule`, miercoles, tarde, prioridad alta, obligatoria. |

Estas restricciones deben cruzarse con personas normalizadas. Si la persona no esta en la base importada con coincidencia exacta, debe quedar como restriccion pendiente de vincular.

## Recomendaciones de importacion

Normalizar para busqueda, comparacion y validacion:

- Nombres y apellidos.
- Correos.
- Instituciones.
- Modalidades.
- Areas.
- Estados.
- Acciones pendientes.
- Indicadores si/no.

Conservar literalmente:

- Texto original de cada celda.
- Columnas sin encabezado.
- Observaciones originales e internas.
- Correos tal como llegaron, incluso si contienen tildes.
- Hashes y CSV original.
- Valores calculados importados y formulas detectadas, aunque se recalculen.

## Decisiones que requieren confirmacion

- Si `HOJA MAESTRA` debe fusionarse con `ORDEN LLEGADA` para recuperar `Fecha y hora`.
- Como interpretar las seis columnas originales sin encabezado.
- Si `Derivado a Panel 6 (Educación Literaria)` debe convertirse en area 6 o en motivo de reubicacion.
- Que criterio usar para confirmar duplicados frente a personas con varias propuestas.
- Como incorporar titulos, resumenes, palabras clave y datos completos de simposios.
- Si la restriccion de Gerardo Fernandez San Emeterio es obligatoria o preferente.
- Si la comprobacion de `POR PANELES` debe considerar 22 columnas originales como dice `COMPROBACION` o 23 columnas visibles como muestra la hoja.

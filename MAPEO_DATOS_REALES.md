# Mapeo de datos reales

## Archivos analizados

- `datos_congreso.xlsx`
- `excepciones.docx`
- `congreso_varios/PETICIONES HORARIAS PARA COMUNICACIONES.docx`
- `congreso_varios/PROGRAMA PROVISIONAL/solicitudes varias.docx`
- DOCX/PDF de `congreso_varios/Resumenes Congreso`

No se modificaron los archivos originales.

## Alcance confirmado de primera version

La primera version debe centrarse en construir y reorganizar el programa del XXVII Congreso Internacional SIDLL 2026. Los datos reales se mapearan con este orden de prioridad:

1. `datos_congreso.xlsx` como fuente administrativa principal, sin perdida de columnas ni valores originales.
2. DOCX/PDF de resumenes como fuente de titulos, resumenes, autorias completas, correos, instituciones y simposios.
3. Documentos de excepciones y solicitudes como fuente de restricciones horarias.
4. Programa, mesas, franjas, aulas, sesiones y asignaciones como modelo operativo propio de la aplicacion.

Quedan fuera de la primera version, aunque existan documentos en la carpeta: inscripciones, pagos, certificados, acreditaciones, control de asistencia, envio real de correos, contrasenas o accesos, gestion presupuestaria, hoteles, programa social, aplicacion movil y publicacion en servidor.

## Estructura del Excel

| Hoja | Funcion | Tratamiento en la aplicacion |
| --- | --- | --- |
| `HOJA MAESTRA` | Fuente principal de gestion. Contiene datos de propuestas, autorias, estados, incidencias, paneles y columnas calculadas. | Importacion prioritaria. Debe conservarse completa. |
| `ORDEN LLEGADA` | Copia de datos originales en orden de recepcion. 173 filas: cabecera + 172 propuestas. | Fuente de auditoria y recuperacion de columnas originales, especialmente `Fecha y hora`. |
| `POR PANELES` | Vista/copia de origen con 160 registros activos por paneles segun `COMPROBACION`. | Referencia derivada; no debe sustituir a la maestra. |
| `LISTAS` | Valores controlados para modalidades, estados, acciones, areas y responsables. | Diccionarios iniciales de normalizacion. |
| `PENDIENTES_AUTO` | Vista automatica de pendientes desde `HOJA MAESTRA`. | Vista derivada a recalcular. |
| `PANELES_AUTO` | Vista automatica para paneles/sesiones desde `HOJA MAESTRA`. | Vista derivada a recalcular. |
| `DUPLICADOS_AUTO` | Vista automatica de posibles duplicados desde `HOJA MAESTRA`. | Vista derivada a recalcular. |
| `EMAILS_AUTO` | Vista automatica para borradores o clasificacion de avisos. | Vista derivada; no enviar correos reales. |
| `DASHBOARD` | Indicadores de gestion calculados desde `HOJA MAESTRA`. | Panel derivado a recalcular. |
| `COMPROBACION` | Controles de filas, columnas, hashes y conservacion de origen. | Requisitos de auditoria de importacion. |
| `CSV_ORIGEN_RAW` | Conservacion textual del CSV original. | Debe conservarse como evidencia de origen. |
| `INSTRUCCIONES` | Instrucciones internas sobre el uso del libro. | Referencia funcional. |

## Columnas por hoja

### `ORDEN LLEGADA`

Columnas: `ORDEN`, `Fecha y hora`, `Modalidad`, `Área`, `Apellidos1`, `Nombre1`, `Institucion1`, `Email1`, `Apellidos2`, `Nombre2`, `Institucion2`, `Email2`, `Apellidos3`, `Nombre3`, `Institucion3`, `Email3`, `Apellidos4`, `Nombre4`, `Institucion4`, `Email4`, `VISTO BUENO`, `NOTIFICADO`, y seis columnas originales sin encabezado (`W:AB`).

Tratamiento: fuente original. Las columnas sin encabezado deben importarse como `ORIG_COL_23` a `ORIG_COL_28`.

### `POR PANELES`

Columnas: `ORDEN`, `Fecha y hora`, `ID Congreso`, `Modalidad`, `Área`, `Apellidos1`, `Nombre1`, `Institucion1`, `Email1`, `Apellidos2`, `Nombre2`, `Institucion2`, `Email2`, `Apellidos3`, `Nombre3`, `Institucion3`, `Email3`, `Apellidos4`, `Nombre4`, `Institucion4`, `Email4`, `VISTO BUENO`, `NOTIFICADO`.

Tratamiento: vista/copia por paneles con 160 registros activos. No debe importarse como fuente independiente del programa.

### `HOJA MAESTRA`

Columnas:

| Columna | Encabezado | Tipo |
| --- | --- | --- |
| A | `ORDEN` | Original |
| B | `ID Congreso` | Gestion/calculada |
| C | `Modalidad` | Original |
| D | `Área` | Original |
| E | `Apellidos1` | Original |
| F | `Nombre1` | Original |
| G | `VISTO BUENO` | Original/decision administrativa |
| H | `NOTIFICADO` | Original/decision administrativa |
| I:M | `ORIG_COL_23` a `ORIG_COL_27` | Original sin encabezado claro |
| N | `Incidencia principal` | Gestion/calculada |
| O:P | `Institucion1`, `Email1` | Original |
| Q:T | `Apellidos2`, `Nombre2`, `Institucion2`, `Email2` | Original |
| U:X | `Apellidos3`, `Nombre3`, `Institucion3`, `Email3` | Original |
| Y:AB | `Apellidos4`, `Nombre4`, `Institucion4`, `Email4` | Original |
| AC | `ORIG_COL_28` | Original sin encabezado claro |
| AD | `Modalidad normalizada` | Gestion/calculada |
| AE | `Área solicitada normalizada` | Gestion/calculada |
| AF | `Área definitiva` | Gestion |
| AG | `Subpanel` | Gestion del programa |
| AH | `Sesión` | Gestion del programa |
| AI | `Orden intervención` | Gestion del programa |
| AJ | `Estado científico` | Gestion/calculada |
| AK | `Estado formal` | Gestion/calculada |
| AL | `Estado notificación` | Gestion/calculada |
| AM | `Estado panel` | Gestion/calculada |
| AN | `Estado general` | Gestion/calculada |
| AO | `Acción pendiente` | Gestion/calculada |
| AP | `Responsable` | Gestion |
| AQ | `Prioridad` | Gestion/calculada |
| AR:AW | `Falta ORCID`, `Falta palabras`, `Falta palabras clave`, `Problema formato`, `Posible duplicado`, `Revisar idioma` | Indicadores de calidad/calculados |
| AX | `Observación original` | Original derivada de `VISTO BUENO` |
| AY | `Observación interna` | Gestion |
| AZ | `Observación comunicable` | Gestion/calculada |
| BA | `Autor/a principal` | Gestion/calculada |
| BB | `Email principal` | Gestion/calculada |
| BC | `Autoría breve` | Gestion/calculada, actualmente con error `#NAME?` |
| BD | `Persona que presenta` | Gestion |
| BE | `Asistencia confirmada` | Gestion |
| BF:BH | Fechas de revision, notificacion y ultima actualizacion | Gestion |
| BI | `Motivo reubicación` | Gestion |

Nota: `Fecha y hora` aparece en `ORDEN LLEGADA` y `POR PANELES`, pero no como columna visible en `HOJA MAESTRA`. Debe decidirse si se fusiona por `ORDEN` o `ID Congreso` durante la importacion.

### `LISTAS`

Columnas: `Modalidad`, `Estado científico`, `Estado formal`, `Estado notificación`, `Estado panel`, `Estado general`, `Prioridad`, `Acción pendiente`, `Área definitiva`, `Responsable`.

Tratamiento: diccionario inicial. Incluye siete areas tematicas previstas:

1. Inteligencia artificial y tecnologias emergentes.
2. Interculturalidad.
3. Objetivos de Desarrollo Sostenible.
4. Educacion bilingue.
5. Didactica de la Lengua y la Literatura en lenguas extranjeras o segundas lenguas.
6. Educacion literaria.
7. Multimodalidad.

### Hojas automaticas

`PENDIENTES_AUTO`, `PANELES_AUTO`, `DUPLICADOS_AUTO`, `EMAILS_AUTO` y `DASHBOARD` usan formulas que referencian `HOJA MAESTRA`. La aplicacion debe reconstruir sus resultados desde el modelo interno.

### `COMPROBACION`

Controles que deben conservarse:

| Control | Esperado |
| --- | --- |
| Filas `ORDEN LLEGADA` copiadas | 173, cabecera + 172 registros |
| Filas `HOJA MAESTRA` | 173 |
| Filas `POR PANELES` copiadas | 161, cabecera + 160 registros |
| Columnas originales `ORDEN LLEGADA` | 28, rango `A:AB` |
| Columnas originales `POR PANELES` | 22 segun nota del libro, aunque la hoja visible tiene 23 columnas por incluir `NOTIFICADO` en `W` |
| Hash `ORDEN` origen | `d50276d8fce9c0b3dd0a889597c512ae15015da6da7520bfc27c1a9c63e51e5e` |
| Hash `POR PANELES` origen | `ba8a44b49a2a74da16a3239727d54fd69a674fb3011f8080d0879263ee0ea7f8` |

## Relaciones detectadas

- Propuesta: una fila de `HOJA MAESTRA`, identificada por `ORDEN` y `ID Congreso`.
- Documento academico: archivo DOCX/PDF que puede vincularse a una propuesta por `ORDEN`, `SIDLL26-xxx`, titulo, autorias, correo o revision manual.
- Autorias: hasta cuatro bloques `ApellidosN`, `NombreN`, `InstitucionN`, `EmailN`.
- Persona autora: se deriva de cada bloque de autoria no vacio.
- Institucion: se deriva de `Institucion1` a `Institucion4`, conservando el texto original y una forma normalizada.
- Correo: se deriva de `Email1` a `Email4`; sirve para identificar personas y detectar repeticiones.
- Area tematica: `Área` recoge la solicitada; `Área solicitada normalizada` y `Área definitiva` gestionan normalizacion y reubicacion.
- Modalidad: `Modalidad` recoge el valor original; `Modalidad normalizada` corrige variantes como `COMUNICACION`.
- Estados: `Estado científico`, `Estado formal`, `Estado notificación`, `Estado panel` y `Estado general`.
- Incidencias: `Incidencia principal` e indicadores `Falta ORCID`, `Falta palabras`, `Falta palabras clave`, `Problema formato`, `Posible duplicado`, `Revisar idioma`.
- Acciones pendientes: `Acción pendiente`, `Responsable`, `Prioridad`.
- Paneles y sesiones: `Área definitiva`, `Subpanel`, `Sesión`, `Orden intervención`.
- Presentacion/asistencia: `Persona que presenta`, `Asistencia confirmada`.
- Restricciones horarias: proceden de documentos dispersos y deben consolidarse como restricciones estructuradas.
- Espacio: aula o sala del catalogo general.
- Disponibilidad de espacio: relacion entre espacio, dia y franja. No se deriva de un contador global de aulas.

## Mapeo al modelo de datos

| Excel | Modelo de la aplicacion |
| --- | --- |
| `ORDEN`, `ID Congreso` | `Proposal.sourceOrder`, `Proposal.sourceProposalId` |
| `Modalidad`, `Modalidad normalizada` | `Proposal.typeOriginal`, `Proposal.typeNormalized` |
| `Área`, `Área solicitada normalizada`, `Área definitiva` | `Proposal.areaOriginal`, `Proposal.areaRequestedNormalized`, `Proposal.areaFinalId` |
| `ApellidosN`, `NombreN`, `InstitucionN`, `EmailN` | `Authorship`, `Person`, `Institution`, `EmailAddress` |
| `VISTO BUENO`, `NOTIFICADO` | `Proposal.originalDecisionText`, `Proposal.originalNotificationText` |
| `Estado científico`, `Estado formal`, `Estado notificación`, `Estado panel`, `Estado general` | `ProposalStatus` |
| `Incidencia principal`, indicadores de falta/problema/duplicado | `QualityIssue` |
| `Acción pendiente`, `Responsable`, `Prioridad` | `PendingAction` |
| `Subpanel`, `Sesión`, `Orden intervención` | `SessionAssignment` |
| `Observación original`, `Observación interna`, `Observación comunicable` | `ProposalNote` con visibilidad |
| `Autor/a principal`, `Email principal`, `Autoría breve` | Campos derivados recalculables |
| `Persona que presenta`, `Asistencia confirmada` | `PresentationRequirement` |
| Fechas de revision/notificacion/actualizacion | `AuditEvent` |
| `Motivo reubicación` | `ReassignmentReason` |
| `COMPROBACION` | `ImportAudit` |
| `CSV_ORIGEN_RAW` | `SourceSnapshot` |
| `excepciones.docx` | `AvailabilityConstraint` |
| DOCX/PDF de resumenes | `SourceDocumentLink`, `Proposal.title`, `Proposal.abstract`, `Authorship` |
| Peticiones horarias dispersas | `SchedulingConstraint` |
| Catalogo de aulas | `Room` |
| Disponibilidad por franja | `RoomAvailability` |

## Mapeo de aulas y franjas

La disponibilidad de aulas se define por franja, no por dia ni de forma global.

Ejemplo operativo:

- Miercoles, primera franja: Aula 5, Aula 8, Aula 11, Aula 112.
- Miercoles, segunda franja: Aula 55, Aula 34, Aula 1, Aula 23, Aula 67, Aula 89.

Consecuencias para el modelo:

- `Room` representa el catalogo general de espacios.
- `RoomAvailability` representa si un espacio esta disponible, reservado, cerrado o bloqueado en una combinacion concreta de dia y franja.
- El maximo de sesiones simultaneas se calcula contando disponibilidades activas de la franja, no leyendo un campo global.
- Plenarias, pausas y actividades bloqueadas pueden ocupar o bloquear espacios en una franja concreta.
- Si una disponibilidad cambia, deben detectarse las asignaciones afectadas.

## Restricciones horarias consolidadas

El detalle completo se mantiene en `RESTRICCIONES_HORARIAS_CONSOLIDADAS.md`.

Resumen detectado:

| Persona o grupo | Propuesta vinculada | Dia/franja | Tipo | Caracter | Fuente |
| --- | --- | --- | --- | --- | --- |
| Gerardo Fernandez San Emeterio | `SIDLL26-027` | Viernes mañana | Preferencia/disponibilidad | Preferente con posible obligatoriedad | `excepciones.docx`; `solicitudes varias.docx` |
| Boris Vazquez-Calvo | `SIDLL26-127` | No miercoles tarde | Indisponibilidad | Obligatoria pendiente de confirmacion | `excepciones.docx` |
| Ana M. Sanchez Catena | `SIDLL26-011` | Jueves 26 | Preferencia/disponibilidad | Preferente | `PETICIONES HORARIAS PARA COMUNICACIONES.docx` |
| Marta Larragueta Arribas y simposio ELLIJ | `SIDLL26-063` | Viernes mañana | Preferencia/coordinacion | Preferente | `solicitudes varias.docx` |
| Miguel Angel Martin-Hervas / comunicacion vinculada a Gerardo | `SIDLL26-027` | Viernes mañana | Preferencia/coordinacion | Preferente | `solicitudes varias.docx` |
| Diana Nastasescu, Fernando Medina Martinez y Cristian V. Pico Herraiz | `SIDLL26-129` y `SIDLL26-147` | Mismo dia; posible viernes | Coordinacion | Preferente | `solicitudes varias.docx` |

## Normalizacion y conservacion

Debe normalizarse durante la importacion:

- Nombres y apellidos para comparacion: mayusculas/minusculas, dobles espacios, tildes solo para clave de busqueda.
- Correos: espacios, mayusculas/minusculas y equivalencias evidentes.
- Instituciones: espacios sobrantes, mayusculas, tildes y variantes frecuentes.
- Modalidades: por ejemplo `COMUNICACION` a `Comunicación`.
- Areas: por ejemplo `2.Interculturalidad` a `2. Interculturalidad`.
- Estados, prioridades y acciones contra los valores de `LISTAS`.
- Indicadores si/no.

Debe conservarse exactamente como llego:

- Todos los textos originales de nombres, instituciones, correos, areas y modalidades.
- `VISTO BUENO`, `NOTIFICADO` y observaciones.
- Columnas originales sin encabezado.
- CSV original textual.
- Hashes de origen.
- Formulas o resultados importados cuando existan, aunque se recalculen internamente.

Cada campo importado debe guardar:

- Valor original.
- Valor normalizado.
- Archivo, hoja, columna y fila de origen.
- Fecha de importacion.
- Historial de modificaciones posteriores.

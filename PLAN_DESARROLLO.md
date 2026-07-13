# Plan de desarrollo

## Enfoque general

El desarrollo se centrara en una primera version fiable para construir y reorganizar el programa del XXVII Congreso Internacional SIDLL 2026.

No se desarrollara una plataforma comercial ni un sistema integral de gestion de congresos. El producto sera una herramienta local de trabajo para importar datos reales, organizar sesiones, validar conflictos, versionar propuestas y generar documentos del programa.

La aplicacion se diseñara para cambios continuos durante varios meses. Añadir restricciones, datos y modificaciones sobre un programa ya montado es un flujo central, no una excepcion.

## Alcance por fases

### Primera version

- Importacion completa de `datos_congreso.xlsx`.
- Incorporacion de titulos, autorias, correos, instituciones, simposios, estados, incidencias, observaciones, restricciones horarias, archivos vinculados y origen de cada dato desde DOCX/PDF y Excel en Fase 1A.
- Incorporacion de resumenes completos definitivos solo desde `resumenes_definitivos` en Fase 1B.
- Vinculacion entre archivos y propuestas mediante identificadores directos o inferidos.
- Gestion de comunicaciones, participantes, simposios, mesas, dias, franjas, espacios y disponibilidad por franja.
- Consolidacion de restricciones horarias dispersas.
- Construccion del programa por dia, franja, aula, mesa, simposio y orden de intervencion.
- Validacion de conflictos de personas, aulas, horarios, duraciones y restricciones.
- Recalculo de mesas al cambiar duraciones de comunicaciones.
- Cancelaciones, retiradas y cambios de presentador.
- Reorganizacion por cambios de aulas, franjas o personas asistentes.
- Versiones comparables, copias locales y restauracion.
- Programa publico, programa interno, listados de mesas, carteles de aula, impresion, PDF y formato compatible con Word.
- Pantalla "Restricciones y cambios", simulacion de impacto, aplicacion controlada, deshacer/rehacer e historial cronologico.

### Posterior

- Flujos completos de revision cientifica.
- Flujos completos de revision formal.
- Revision editorial de resumenes.
- Generacion de correos de aceptacion o subsanacion.
- Preparacion de actas.
- Gestion de publicaciones.
- Control de tareas del comite organizador.

### Excluido

- Inscripciones, pagos, certificados, acreditaciones, control de asistencia, envio real de correos, contrasenas o accesos, gestion presupuestaria, hoteles, programa social, aplicacion movil y publicacion en servidor.

## Modulos funcionales de primera version

- `model`: entidades y relaciones.
- `import`: importacion de Excel, DOCX y PDF.
- `source-audit`: conservacion de valores originales, origen, hashes y evidencias.
- `matching`: vinculacion entre archivos y propuestas.
- `constraints`: restricciones horarias y disponibilidad de personas.
- `change-management`: cambios continuos, estados, simulacion, aplicacion, deshacer/rehacer e historial.
- `rooms`: catalogo de espacios y disponibilidad por franja.
- `scheduler`: construccion de programa, duraciones y recalculos.
- `planning-engine`: restricciones duras/blandas, puntuacion, desempate, escenarios, propuestas e inviabilidad.
- `validation`: conflictos de personas, aulas, horarios, restricciones y duraciones.
- `reorganizer`: propuestas alternativas de reubicacion.
- `versions`: versiones, comparacion, copias y restauracion.
- `export`: programa publico, interno, listados, carteles, impresion, PDF y Word compatible.
- `storage`: persistencia local y copias de seguridad.
- `views`: vistas de trabajo por dia, franja, aula, mesa, simposio, persona y conflicto.

## Modelo de datos inicial

> Nota de cierre arquitectonico: las definiciones canonicas vigentes estan en `MODELO_CANONICO_DEFINITIVO.md`. El bloque siguiente debe leerse como esquema orientativo historico si hay diferencias.

```js
Congress {
  id: string,
  title: string,
  edition: "XXVII Congreso Internacional SIDLL 2026",
  venue?: string,
  timezone?: string,
  dates: string[]
}

Day {
  id: string,
  date: string,
  label: string,
  startsAt?: string,
  endsAt?: string
}

TimeSlot {
  id: string,
  dayId: string,
  label: string,
  startsAt: string,
  endsAt: string,
  kind: "comunicaciones" | "simposio" | "plenaria" | "pausa" | "social" | "otro",
  locked?: boolean,
  notes?: string
}

Room {
  id: string,
  name: string,
  building?: string,
  location?: string,
  defaultCapacity?: number,
  defaultEquipment?: string[],
  notes?: string
}

RoomAvailability {
  id: string,
  roomId: string,
  dayId: string,
  timeSlotId: string,
  available: boolean,
  reservedUse?: string,
  allowedModalities?: string[],
  effectiveCapacity?: number,
  equipmentAvailableInSlot?: string[],
  priority?: number,
  blocked: boolean,
  notes?: string
}

Person {
  id: string,
  fullName: string,
  normalizedName: string,
  affiliations?: string[],
  emails?: string[],
  roles?: string[]
}

Proposal {
  id: string,
  sourceOrder?: number,
  sourceProposalId?: string,
  modality: "comunicacion" | "simposio" | "taller",
  areaOriginal?: string,
  areaFinalId?: string,
  title?: string,
  abstract?: string,
  authorIds: string[],
  presenterIds: string[],
  status: "active" | "withdrawn" | "cancelled"
}

Symposium {
  id: string,
  proposalId?: string,
  title: string,
  coordinatorIds: string[],
  communicationProposalIds: string[],
  durationMinutes?: number,
  notes?: string
}

Session {
  id: string,
  title: string,
  type: "mesa" | "simposio" | "plenaria" | "pausa" | "otro",
  dayId: string,
  timeSlotId: string,
  startsAt: string,
  endsAt: string,
  durationMinutes: number,
  requiredCapacity?: number,
  requiredEquipment?: string[],
  itemIds: string[],
  status: "draft" | "confirmed" | "cancelled"
}

Assignment {
  id: string,
  sessionId: string,
  roomId: string,
  roomAvailabilityId: string,
  dayId: string,
  timeSlotId: string,
  order: number,
  locked?: boolean,
  notes?: string
}

ProgrammableBlock {
  id: string,
  type: "mesa_comunicaciones" | "sesion_simposio" | "simposio_completo" | "plenaria" | "inauguracion" | "clausura" | "taller" | "mesa_redonda" | "pausa" | "almuerzo" | "institucional" | "social" | "bloqueo_tecnico" | "bloqueo_organizativo",
  title: string,
  durationMinutes: number,
  participantIds: string[],
  proposalIds: string[],
  modality: "presencial" | "virtual" | "hibrida",
  technicalRequirements?: string[],
  expectedCapacity?: number,
  divisible: boolean,
  maxParts?: number,
  locked: boolean,
  editable: boolean,
  preferredDayId?: string,
  preferredTimeSlotId?: string,
  constraintIds: string[],
  priority: "alta" | "media" | "baja",
  status: "pendiente" | "programado" | "cancelado" | "retirado" | "bloqueado"
}

SchedulingConstraint {
  id: string,
  personIds?: string[],
  proposalIds?: string[],
  symposiumIds?: string[],
  sessionIds?: string[],
  roomIds?: string[],
  timeSlotIds?: string[],
  dayIds?: string[],
  activityIds?: string[],
  originalText: string,
  structuredInterpretation?: Record<string, unknown>,
  day?: string,
  timeBand?: string,
  type: "disponibilidad" | "indisponibilidad" | "preferencia_dia" | "preferencia_franja" | "mismo_dia" | "distinta_franja" | "misma_mesa" | "distinta_mesa" | "modalidad" | "aula_especifica" | "equipamiento" | "duracion_especial" | "orden_intervencion" | "viaje" | "observacion",
  character: "obligatoria" | "preferente" | "informativa" | "pendiente_confirmar",
  priority: "alta" | "media" | "baja",
  status: "borrador" | "pendiente_revision" | "confirmada" | "aplicada" | "descartada" | "sustituida",
  sourceDocument: string,
  addedBy?: string,
  internalComment?: string,
  createdAt: string,
  updatedAt: string,
  changeHistory: ChangeHistoryEntry[],
  confidence: "alta" | "media" | "baja",
  pendingQuestion?: string
}

Decision {
  id: string,
  title: string,
  description?: string,
  type: "incorporacion_informacion" | "modificacion" | "cancelacion" | "excepcion" | "incidencia" | "solicitud" | "acuerdo_comite" | "cambio_confirmado",
  status: "recibida" | "pendiente_interpretar" | "interpretada" | "pendiente_aprobacion" | "aprobada" | "simulada" | "aplicada" | "descartada" | "sustituida" | "archivada",
  priority: "alta" | "media" | "baja",
  receivedAt: string,
  approvedAt?: string,
  source?: string,
  originalText?: string,
  responsiblePerson?: string,
  affectedEntityRefs: unknown[],
  replacedDecisionId?: string,
  derivedConstraintIds: string[],
  approvedModificationIds: string[],
  simulatedScenarioIds: string[],
  appliedProgramVersionId?: string,
  internalNotes?: string
}

ChangeImpact {
  affectedSessionIds: string[],
  affectedPersonIds: string[],
  affectedProposalIds: string[],
  newConflictIds: string[],
  alternatives: ReorganizationProposal[],
  minimumChanges: string[]
}

ChangeHistoryEntry {
  id: string,
  entityType: string,
  entityId: string,
  fieldName?: string,
  previousValue: unknown,
  newValue: unknown,
  reason?: string,
  changedAt: string,
  changedBy?: string,
  versionId?: string
}

SourceDocumentLink {
  id: string,
  proposalId?: string,
  path: string,
  matchMethod: "orden" | "sidll_id" | "titulo" | "autoria" | "correo" | "manual",
  confidence: "alta" | "media" | "baja",
  notes?: string
}

ProgramVersion {
  id: string,
  label: string,
  createdAt: string,
  summary?: string,
  dataSnapshot: unknown
}

Scenario {
  id: string,
  name: string,
  description?: string,
  sourceVersionId: string,
  includedChangeIds: string[],
  activeConstraintIds: string[],
  resultingProgram?: unknown,
  conflictIds: string[],
  score?: number,
  impactSummary?: unknown,
  createdAt: string,
  status: "borrador" | "calculando" | "valido" | "valido_con_advertencias" | "inviable" | "aplicado" | "descartado" | "archivado",
  createdBy?: string,
  calculationSeed?: string
}
```

## Fases verificables

### Fase 0. Cierre funcional

- Aprobar alcance de Nivel 1, Nivel 2 y Nivel 3.
- Confirmar que la disponibilidad de aulas se define por franja, no por dia ni de forma global.
- Confirmar que la gestion continua de cambios es nucleo de la primera version.
- Aprobar el nucleo logico del motor: restricciones duras/blandas, pesos, desempates, bloques programables, escenarios, inviabilidad y explicabilidad.
- Confirmar criterios de duracion de comunicaciones, mesas, simposios y pausas.
- Confirmar salidas documentales necesarias.

### Fase 1A. Base academica completa

- Importar `datos_congreso.xlsx` sin perdida de columnas ni valores originales.
- Extraer DOCX/PDF disponibles para titulos, autorias, instituciones, correos, simposios y datos academicos base.
- Incorporar identificador interno, `ORDEN`, `SIDLL26-xxx`, modalidad, area solicitada, area definitiva, titulo, todas las autorias, orden de autoria, primera autoria, presentador si se conoce, instituciones, correos, simposio relacionado, estados administrativos/cientificos/formales/notificacion, incidencias, observaciones, restricciones horarias, archivos vinculados y origen de cada dato.
- Vincular documentos con propuestas mediante `ORDEN`, `SIDLL26-xxx`, titulo, autorias, correos u otros identificadores.
- Registrar confianza y dudas de cada vinculacion.
- Persistir y restaurar la base academica sin depender de la carpeta `resumenes_definitivos`.

Verificacion:

- Todas las columnas originales quedan conservadas.
- Cada archivo academico queda vinculado, pendiente de vincular o marcado como duda.
- Los titulos y autorias se incorporan aunque no existan resumenes definitivos.
- No se importan resumenes completos desde carpetas heterogeneas actuales.
- Los datos importados pueden exportarse como copia de seguridad.

### Fase 1B. Resumenes definitivos

Se ejecuta cuando exista la carpeta `resumenes_definitivos`.

- Detectar automaticamente archivos DOCX/PDF en `resumenes_definitivos`.
- Normalizar nombres de archivo ignorando mayusculas, tildes, guiones, guiones bajos, extension, espacios redundantes y auxiliares como `resumen`, `definitivo`, `corregido`, `final`, `sidll` y `comunicacion`.
- Extraer titulo, autorias, instituciones, correos, ORCID, palabras clave, texto completo, idioma y referencias cuando sea posible.
- Proponer vinculacion con `TrabajoAcademico` usando `SIDLL26-xxx`, `ORDEN`, apellidos de primera autoria, nombre, titulo, correo, resto de autorias, institucion, similitud de archivo y carpeta/panel de procedencia.
- Clasificar vinculaciones como `automatica_segura`, `probable`, `ambigua`, `sin_coincidencia` o `vinculada_manualmente`.
- Detener para revision manual los casos ambiguos, especialmente personas con varias comunicaciones, mismos apellidos o archivos que solo contienen apellido.
- Mostrar vinculados, sin vincular y trabajos academicos sin resumen definitivo.
- Incorporar resumen definitivo a `TrabajoAcademico` con fuente, hash, fecha y version.
- Conservar versiones anteriores si se sustituye un resumen.
- Comparar titulo, autorias, instituciones y correos detectados contra los registrados y exigir confirmacion antes de actualizar valores.

Verificacion:

- `SIDLL26-xxx` exacto y `ORDEN` exacto generan vinculacion automatica segura.
- Apellidos mas titulo o apellidos mas correo generan vinculacion de muy alta confianza si la coincidencia es unica.
- Solo apellidos no vincula automaticamente cuando hay mas de una candidata.
- La reimportacion del mismo archivo no duplica el resumen.
- Una nueva version conserva la anterior, registra hash, fecha, fuente y decision si tiene impacto.
- El informe final muestra cobertura: resumenes vinculados, archivos sin correspondencia y trabajos sin resumen definitivo.

### Fase 2. Modelo de programa

- Crear dias, franjas, espacios, disponibilidad por franja, sesiones, mesas, simposios y asignaciones.
- Crear `ProgrammableBlock` como unidad comun para todo elemento que ocupa tiempo.
- Crear cuadricula rapida para editar disponibilidad de espacios por dia y franja.
- Incorporar restricciones horarias consolidadas.
- Crear modelo de restricciones ampliado y cambios continuos.

Verificacion:

- Cada franja muestra solo sus aulas disponibles.
- No existe contador global de aulas disponibles.
- Las restricciones aparecen vinculadas a personas y propuestas cuando sea posible.
- Una restriccion puede quedar en borrador, pendiente de revision, confirmada, aplicada, descartada o sustituida.

### Fase 3. Restricciones y cambios

- Crear pantalla "Restricciones y cambios".
- Crear formulario rapido de restriccion.
- Permitir crear, editar, duplicar, desactivar, archivar, eliminar con confirmacion, filtrar, buscar, ordenar y aplicar cambios masivos.
- Permitir añadir restricciones desde fichas de persona, comunicacion, mesa, simposio, aula o franja.
- Mostrar restricciones que afectan a cada elemento.
- Simular cambios sin alterar el programa actual.
- Calcular sesiones afectadas, personas afectadas, conflictos, alternativas y cambios minimos.

Verificacion:

- Se puede añadir una restriccion a una persona ya programada.
- Se puede simular el impacto sin modificar el programa.
- Se puede aplicar un cambio, varios seleccionados o todas las restricciones pendientes.
- Se genera historial cronologico del cambio.

### Fase 4. Construccion manual del programa

- Asignar comunicaciones y simposios a sesiones.
- Ordenar intervenciones.
- Cambiar duraciones y recalcular mesas.
- Gestionar cancelaciones, retiradas y cambios de presentador.

Verificacion:

- El programa puede construirse por dia, franja, aula, mesa, simposio y orden.
- Los cambios quedan versionados.

### Fase 5. Validacion

- Detectar conflictos de personas simultaneas.
- Detectar conflictos de aula y disponibilidad por franja.
- Detectar conflictos de duracion, horario y restricciones.
- Detectar sesiones afectadas cuando cambia una disponibilidad.

Verificacion:

- Cada conflicto identifica causa, entidades afectadas y posible accion.
- El programa puede filtrarse por conflictos pendientes.

### Fase 6. Reorganizacion

- Generar propuestas alternativas cuando cambien aulas, franjas o personas asistentes.
- Proponer reubicaciones compatibles con disponibilidad, modalidad, capacidad, equipamiento, bloqueo y restricciones.
- Comparar propuestas antes de aplicar.
- Comparar programa actual, programa simulado tras una restriccion y programa simulado tras varias restricciones.
- Crear version y copia de seguridad antes de aplicar cambios importantes.
- Generar propuesta conservadora, equilibrada y compacta.
- Detectar escenarios inviables y explicar causas.
- Explicar cada movimiento propuesto.
- Garantizar reproducibilidad con la misma configuracion.

Verificacion:

- Ninguna propuesta usa aulas no disponibles en la franja correspondiente.
- La version previa queda conservada antes de aplicar cambios.
- Cada propuesta muestra puntuacion, restricciones duras incumplidas, preferencias incumplidas, movimientos e impacto.
- Cada escenario inviable muestra contradicciones y alternativas de resolucion.

### Fase 7. Entrada continua de datos

- Permitir añadir nuevas comunicaciones, personas, simposios, mesas, aulas, franjas, dias, actividades, observaciones y restricciones.
- Permitir entrada manual, formularios, edicion en tabla, importacion Excel/CSV/JSON y pegado desde portapapeles.
- Detectar existentes, proponer actualizacion o creacion, conservar valores anteriores y evitar sobrescrituras silenciosas.
- Crear edicion rapida en tablas para estado, aula, franja, duracion, presentador, mesa, prioridad y confirmacion.
- Implementar deshacer y rehacer.

Verificacion:

- Importar cambios desde Excel no pierde datos anteriores.
- Añadir una comunicacion con el programa montado recalcula impactos.
- Retirar una comunicacion recalcula la mesa.

### Fase 8. Salidas y copias

- Generar programa publico.
- Generar programa interno.
- Generar listados de mesas.
- Generar carteles de aula.
- Preparar impresion, PDF y formato compatible con Word.
- Guardar y restaurar copias locales.

## Pruebas de aceptacion especificas para Fase 1

1. Importar `datos_congreso.xlsx` sin perder columnas ni valores.
2. Crear `TrabajoAcademico` con `ORDEN`, `SIDLL26-xxx`, titulo, autorias, instituciones, correos, simposio, estados, incidencias, observaciones, restricciones horarias, archivos vinculados y origen de dato.
3. Completar Fase 1A sin importar resumenes completos desde carpetas heterogeneas.
4. Vincular archivo de resumen definitivo con apellido unico y una sola propuesta.
5. Vincular correctamente apellidos compuestos y tildes.
6. Vincular correctamente nombres con guiones y guiones bajos.
7. Detener para revision si la primera autoria tiene dos comunicaciones.
8. Detener para revision si dos personas tienen los mismos apellidos y no hay criterio determinante.
9. Vincular automaticamente si el archivo contiene `SIDLL26-xxx` exacto.
10. Usar titulo coincidente cuando el nombre este incompleto.
11. No vincular automaticamente si apellido coincide pero titulo no.
12. Marcar como `sin_coincidencia` un archivo sin correspondencia.
13. Conservar dos versiones del mismo resumen.
14. Exigir confirmacion si una nueva version modifica titulo.
15. Exigir confirmacion si una nueva version modifica autoria.
16. Reimportar el mismo archivo sin duplicar.
17. Preservar orden, instituciones y correos de resumenes con varias autorias.
18. Informar trabajos academicos sin resumen definitivo.

## Pruebas de aceptacion especificas para aulas variables

Prueba de aulas variables:

- Franja 1 con 4 aulas: 5, 8, 11, 112.
- Franja 2 con 6 aulas: 55, 34, 1, 23, 67, 89.
- Verificar que cada franja muestra solo sus aulas.
- Verificar que el generador no asigna sesiones a aulas inexistentes en esa franja.
- Verificar que el maximo de sesiones simultaneas cambia de 4 a 6.
- Verificar que una misma aula puede estar disponible en una franja y no disponible en otra.
- Verificar que plenarias, pausas y actividades bloqueadas pueden limitar aulas disponibles.
- Verificar la reorganizacion si se elimina una de las aulas de una franja.

## Pruebas de aceptacion especificas para gestion continua de cambios

1. Añadir una nueva restriccion a una persona ya programada.
2. Simular el impacto sin modificar el programa.
3. Aplicar la restriccion.
4. Comparar antes y despues.
5. Deshacer el cambio.
6. Añadir cinco restricciones nuevas en bloque.
7. Importar cambios desde Excel.
8. Confirmar que no se pierden datos anteriores.
9. Introducir una nueva aula disponible solo en una franja.
10. Añadir una nueva comunicacion cuando el programa ya esta montado.
11. Retirar una comunicacion y recalcular la mesa.
12. Cambiar una persona presentadora.
13. Modificar la duracion global y revisar el impacto.
14. Recuperar una version anterior.

## Criterios de aceptacion de primera version

- Se importa `datos_congreso.xlsx` sin perdida de columnas ni valores.
- Se incorporan titulos, autorias, instituciones, correos, simposios, estados, incidencias, observaciones, restricciones horarias, archivos vinculados y origen de cada dato desde las fuentes existentes de Fase 1A.
- Fase 1A puede completarse aunque no exista `resumenes_definitivos`.
- Los resumenes completos definitivos se incorporan solo desde `resumenes_definitivos` en Fase 1B.
- Los resumenes definitivos quedan vinculados a `TrabajoAcademico` con nivel de confianza, fuente, hash, fecha y version.
- Los archivos ambiguos se detienen para revision manual y no se vinculan automaticamente.
- Una persona con varias comunicaciones no puede resolverse por apellido como unico criterio.
- Las reimportaciones no duplican resumenes ni sobrescriben titulo, autorias, instituciones, correos o texto definitivo sin confirmacion.
- Las restricciones horarias dispersas quedan consolidadas.
- La disponibilidad de aulas se gestiona por franja.
- El programa se construye y reorganiza por dia, franja, aula, mesa, simposio y orden.
- Se detectan conflictos de personas, aulas, horarios, duraciones y restricciones.
- Se recalculan mesas al cambiar duraciones de comunicaciones.
- Se gestionan cancelaciones, retiradas y cambios de presentador.
- Se generan versiones comparables antes y despues de cambios.
- Se pueden crear restricciones y cambios provisionales sin aplicarlos.
- Se puede simular, aplicar, comparar, deshacer y recuperar versiones.
- Se pueden importar cambios sin sobrescrituras silenciosas.
- Se generan programa publico, programa interno, listados de mesas y carteles de aula.
- Se imprime y exporta a PDF y formato compatible con Word.
- Se guardan datos en local y copias de seguridad.
- El motor diferencia restricciones duras y blandas.
- El motor usa pesos configurables y reglas de desempate.
- El motor permite escenarios independientes y conserva el programa oficial.
- El motor identifica inviabilidad y explica cada cambio automatico.

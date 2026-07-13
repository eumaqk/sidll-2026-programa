# Modelo canonico definitivo

Este documento sustituye las definiciones parciales anteriores cuando exista contradiccion. Su objetivo es fijar una unica responsabilidad por entidad y evitar solapamientos antes de comenzar la programacion.

## Flujo conceptual correcto

Informacion recibida -> Decision -> restricciones o modificaciones aprobadas -> simulacion sobre escenario -> estado resultante del programa -> calculo de conflictos -> propuestas de resolucion -> cambios aplicados -> nueva version e historial.

El conflicto es siempre resultado calculado. Nunca es dato editable ni fuente de verdad.

## Entidades canonicas

### FuenteImportada

Evidencia original: Excel, Word, PDF, CSV, introduccion manual, correo transcrito o nota organizativa.

Responsabilidad: conservar origen y trazabilidad.

Campos principales:

- `sourceRecordId`
- tipo de fuente
- archivo o descripcion de fuente
- ubicacion de origen: hoja/fila/columna, pagina, ruta, fragmento o campo manual
- texto o valor original
- fecha de incorporacion
- hash cuando exista
- nombre original del archivo cuando exista
- tipo academico de fuente: administrativa, base academica, resumen definitivo, restriccion, decision u otra
- estado de vinculacion: automatica segura, probable, ambigua, sin coincidencia o vinculada manualmente
- persona responsable
- relaciones con entidades normalizadas

No contiene decisiones de programacion.

### PropuestaOriginal

Registro recibido o importado. Conserva datos administrativos originales.

Responsabilidad: preservar lo recibido.

Campos principales:

- `sourceRecordId`
- `ORDEN`
- `SIDLL26-xxx`
- modalidad original
- area original
- autorias originales
- estados administrativos importados
- observaciones originales
- vinculos con fuentes y archivos

No se usa directamente como unidad del planificador.

### TrabajoAcademico

Contenido academico normalizado.

Decision tecnica: usar una sola entidad con campo `tipo`, no entidades especializadas. Es mas simple y suficiente para la primera version. La integridad se mantiene con validaciones por tipo.

Subtipos mediante `tipo`:

- `comunicacion`
- `simposio`
- `taller`
- `mesa_redonda`
- `conferencia`
- `otra_actividad_academica`

Responsabilidad: fuente unica de verdad del contenido academico normalizado.

Debe contener:

- `workId`
- tipo
- titulo
- resumen definitivo, solo cuando proceda de `resumenes_definitivos`
- versiones de resumen definitivo
- autorias normalizadas
- instituciones
- correos
- ORCID, palabras clave, idioma y referencias cuando se extraigan de resumen definitivo
- persona presentadora
- coordinadores, si aplica
- estado academico
- duracion propia, si procede
- fuente/propuesta de origen

Fuente unica de verdad para retirada, cancelacion, participacion activa, persona presentadora, autorias y estado academico.

Reglas especificas de resumenes:

- Fase 1A puede crear `TrabajoAcademico` sin resumen definitivo.
- Los resumenes completos definitivos se incorporan solo desde `resumenes_definitivos`.
- El texto definitivo se almacena en `TrabajoAcademico`, pero cada version queda vinculada a `FuenteImportada`.
- Una nueva version de resumen no modifica `workId`.
- Diferencias entre titulo, autorias, instituciones o correos detectados y valores normalizados no se aplican sin confirmacion.
- Una vinculacion ambigua no puede actualizar `TrabajoAcademico` automaticamente.

### BloqueProgramable

Unidad de contenido que debe ocupar tiempo. Puede ser indivisible o divisible.

Ejemplos: mesa de comunicaciones, sesion de simposio, simposio completo, plenaria, inauguracion, pausa, almuerzo, taller, actividad institucional.

Responsabilidad: definir que debe programarse.

Puede contener o referenciar `TrabajoAcademico`, pero no duplica sus estados academicos.

Campos principales:

- `programmableBlockId`
- tipo
- titulo
- trabajos academicos incluidos
- duracion calculada o fija
- modalidad
- requisitos tecnicos
- capacidad prevista
- divisible
- numero maximo de partes
- bloqueado/editable
- dia/franja preferente
- restricciones relacionadas
- estado de programacion del bloque

### SesionProgramada

Colocacion temporal de un `BloqueProgramable`.

Decision tecnica: mantener separadas `BloqueProgramable` y `SesionProgramada`.

Justificacion: un bloque representa el contenido agrupado; una sesion representa cuando se coloca. Esto permite simular movimientos, dividir bloques, restaurar versiones y detectar conflictos temporales sin duplicar contenido academico.

Responsabilidad: definir cuando se programa.

Campos principales:

- `scheduledSessionId`
- `programmableBlockId`
- `dayId`
- `timeSlotId`
- hora inicial
- hora final
- estado de programacion temporal

### AsignacionEspacio

Colocacion espacial de una `SesionProgramada`.

Responsabilidad: definir donde se celebra.

Debe enlazar obligatoriamente con una `DisponibilidadEspacio` valida.

Campos principales:

- `spaceAssignmentId`
- `scheduledSessionId`
- `roomId`
- `roomAvailabilityId`
- `dayId`
- `timeSlotId`

### Dia

Jornada del congreso.

Campos principales:

- `dayId`
- fecha
- etiqueta
- hora inicio/fin

### Franja

Bloque temporal dentro de un dia.

Campos principales:

- `timeSlotId`
- `dayId`
- etiqueta
- hora inicio/fin
- tipo
- bloqueada

### Espacio

Catalogo general de aulas o salas.

Campos principales:

- `roomId`
- nombre
- edificio/ubicacion
- capacidad base
- equipamiento base

No implica disponibilidad.

### DisponibilidadEspacio

Posibilidad real de usar un espacio en una combinacion dia/franja.

Campos principales:

- `roomAvailabilityId`
- `roomId`
- `dayId`
- `timeSlotId`
- disponible
- reservado/cerrado/bloqueado
- modalidad permitida
- capacidad efectiva
- equipamiento disponible en esa franja

### Decision

Causa organizativa persistente.

No se crea para correcciones menores sin impacto programatico.

Tipos:

- incorporacion de informacion
- modificacion
- cancelacion
- excepcion
- incidencia
- solicitud
- acuerdo del comite
- cambio confirmado

Campos principales:

- `decisionId`
- titulo
- descripcion
- tipo
- estado
- prioridad
- fecha de recepcion
- fecha de aprobacion
- origen
- texto original
- persona responsable
- entidades afectadas
- decision sustituida
- restricciones derivadas
- modificaciones aprobadas
- escenarios en los que se ha simulado
- version en la que se aplico
- notas internas

### Restriccion

Regla activa derivada de una `Decision` o de configuracion estructural.

Responsabilidad: representar una regla evaluable por el motor.

No gestiona el ciclo humano completo de aprobacion.

Campos principales:

- id
- caracter duro/blando
- tipo
- peso cuando sea blanda
- alcance
- entidades afectadas
- periodo de vigencia
- activa/inactiva
- decision de origen
- forzable manualmente
- explicacion de incumplimiento

### ModificacionPropuesta

Cambio concreto que se propone aplicar a un escenario.

Ejemplos: mover Mesa 7, retirar `SIDLL26-054`, cambiar presentador, cerrar Aula 11, modificar duracion a 12 minutos.

Responsabilidad: representar una accion derivada y revisable.

No reemplaza a `Decision`.

### Conflicto

Resultado calculado y regenerable.

Responsabilidad: describir incumplimientos del estado calculado.

No editable.

Se calcula desde estado del programa, restricciones activas, disponibilidades, asignaciones, duraciones y bloqueos.

Campos principales:

- tipo
- gravedad
- entidades afectadas
- regla incumplida
- explicacion
- escenario
- posibles resoluciones

### Impacto

Resultado calculado y regenerable.

Responsabilidad: describir consecuencias de una decision, escenario o propuesta.

No es dato maestro ni editable.

Campos principales:

- sesiones afectadas
- personas afectadas
- trabajos afectados
- conflictos creados o resueltos
- cambios minimos estimados
- alternativas

### Escenario

Copia logica o conjunto de diferencias respecto a una version base.

Responsabilidad: simular una o varias decisiones sin modificar el programa oficial.

### VersionPrograma

Instantanea persistente del programa oficial o de un hito explicito.

Responsabilidad: permitir comparacion, restauracion y auditoria.

Una version oficial nunca se modifica; se crea una nueva version.

### EventoHistorial

Registro inmutable de hechos relevantes: creacion, edicion, aprobacion, simulacion, aplicacion, restauracion, sustitucion o descarte.

No es fuente de verdad del estado actual.

## Edicion menor directa frente a decision organizativa

Edicion menor directa:

- corregir errata
- normalizar nombre
- completar dato administrativo
- corregir correo
- modificar observacion interna sin impacto en programa

Decision organizativa:

- afecta disponibilidad
- afecta restricciones
- afecta comunicaciones activas
- afecta presentadores
- afecta simposios
- afecta aulas
- afecta franjas/horarios/duraciones/asignaciones
- afecta programa publico/versiones/reorganizaciones

# Arquitectura congelada

## Estado

Arquitectura lista para iniciar programacion de Fase 1 si se aceptan las decisiones pendientes indicadas al final de este documento.

## Documentos canonicos vigentes

- `MODELO_CANONICO_DEFINITIVO.md`
- `ESTADOS_E_INVARIANTES.md`
- `REGLAS_MESAS_Y_DURACIONES.md`
- `ALGORITMO_MVP_PLANIFICACION.md`
- `FLUJO_REIMPORTACION.md`

## Documentos subordinados

Los siguientes documentos siguen siendo utiles, pero quedan subordinados al modelo canonico definitivo:

- `MOTOR_PLANIFICACION.md`
- `BLOQUES_PROGRAMABLES.md`
- `MODELO_RESTRICCIONES.md`
- `GESTION_CONTINUA_DE_CAMBIOS.md`
- `ESCENARIOS_Y_SIMULACION.md`
- `MODELO_AULAS_Y_FRANJAS.md`

Cuando exista contradiccion, prevalecen los documentos canonicos vigentes.

## Decisiones congeladas

- La entidad principal del flujo organizativo es `Decision`.
- `Conflicto` e `Impacto` son calculados y regenerables, no editables.
- `PropuestaOriginal` no entra directamente en el planificador.
- `TrabajoAcademico` es la fuente unica del estado academico.
- Fase 1A crea la base academica completa sin depender de resumenes definitivos.
- Los resumenes completos definitivos solo se incorporan desde `resumenes_definitivos`.
- Cada resumen definitivo queda versionado y vinculado a `FuenteImportada`.
- Una vinculacion ambigua de resumen definitivo requiere revision manual.
- Una persona con varias comunicaciones no puede resolverse solo por apellido.
- `BloqueProgramable` define que debe programarse.
- `SesionProgramada` define cuando se programa.
- `AsignacionEspacio` define donde se programa.
- `DisponibilidadEspacio` es obligatoria para usar un aula en una franja.
- Mesa != SesionProgramada.
- El MVP usa algoritmo conservador determinista con backtracking limitado.
- El programa oficial no se modifica por simulaciones.
- Toda version oficial es inmutable.

## Pendientes que requieren confirmacion

- Valores iniciales exactos de duracion de comunicacion, debate, transicion, margen y tolerancia.
- Maximo absoluto de comunicaciones por mesa.
- Si la presidencia es obligatoria para confirmar mesa.
- Que simposios son indivisibles por defecto.
- Limites del backtracking: tiempo, profundidad y numero de candidatos.
- Confirmar si la carpeta `resumenes_definitivos` queda como nombre definitivo obligatorio o si se permitira configurar una ruta equivalente.
- Confirmar si la nomenclatura recomendada `SIDLL26-XXX_ApellidosPrimerAutor.docx` se comunicara al comite como pauta oficial.

# Estados e invariantes

## Fuente unica de verdad de estados

| Estado | Valores | Entidad responsable unica |
| --- | --- | --- |
| Estado del contenido academico | activo, retirado, cancelado, pendiente de confirmacion, sustituido | `TrabajoAcademico` |
| Estado de programacion del bloque | no programado, programado, afectado, confirmado, cancelado | `BloqueProgramable` |
| Estado temporal de una colocacion | borrador, colocada, afectada, confirmada, cancelada | `SesionProgramada` |
| Estado espacial de una asignacion | valida, afectada, invalida, forzada | `AsignacionEspacio` |
| Estado de la decision | recibida, pendiente de interpretar, interpretada, pendiente de aprobacion, aprobada, simulada, aplicada, descartada, sustituida, archivada | `Decision` |
| Estado de la restriccion | activa, inactiva, sustituida | `Restriccion` |
| Estado del escenario | borrador, calculando, valido, valido con advertencias, inviable, aplicado, descartado, archivado | `Escenario` |
| Estado de la version | oficial, archivada, restaurada | `VersionPrograma` |

## Invariantes del sistema

1. Un `TrabajoAcademico` retirado o cancelado no puede formar parte de un `BloqueProgramable` activo.
2. Un `BloqueProgramable` debe referenciar trabajos academicos existentes o una actividad institucional/social valida.
3. Un `BloqueProgramable` no duplica estado academico de sus trabajos.
4. Una `SesionProgramada` debe referenciar un `BloqueProgramable` existente.
5. Una `SesionProgramada` debe estar dentro de un dia y una franja existentes.
6. Una `SesionProgramada` no puede tener hora final anterior o igual a hora inicial.
7. Una `SesionProgramada` debe caber dentro de su franja salvo fuerza manual registrada.
8. Una `AsignacionEspacio` debe referenciar una `SesionProgramada` existente.
9. Una `AsignacionEspacio` debe referenciar una `DisponibilidadEspacio` existente.
10. `AsignacionEspacio.dayId` y `AsignacionEspacio.timeSlotId` deben coincidir con los de la `SesionProgramada`.
11. `AsignacionEspacio.dayId` y `AsignacionEspacio.timeSlotId` deben coincidir con los de la `DisponibilidadEspacio`.
12. Una `AsignacionEspacio` valida no puede usar una disponibilidad cerrada, bloqueada, reservada para otro uso o no disponible.
13. Una persona presentadora debe estar vinculada al `TrabajoAcademico`.
14. Un trabajo academico activo debe tener presentador valido antes de confirmar su bloque.
15. Una restriccion obligatoria activa invalida un escenario que la incumpla.
16. Una restriccion blanda incumplida penaliza, pero no invalida.
17. Una preferencia no puede convertirse en obligatoria sin decision aprobada.
18. Un conflicto no puede modificarse manualmente.
19. Un impacto no puede modificarse manualmente.
20. Si cambian datos, restricciones, disponibilidades, asignaciones, duraciones o bloqueos, los conflictos deben recalcularse.
21. Una `Decision` aplicada debe indicar la `VersionPrograma` en la que se aplico.
22. Una decision sustituida debe conservar referencia a la decision que la sustituye o a la sustituida.
23. Una version oficial nunca se modifica; se crea una nueva version.
24. Una simulacion nunca modifica el programa oficial.
25. Un escenario aplicado debe generar nueva version oficial.
26. Una reimportacion nunca debe cambiar el ID interno de una entidad ya vinculada.
27. El ID externo `SIDLL26-xxx` nunca sustituye al ID interno.
28. Ningun dato original debe sobrescribirse; las correcciones se almacenan como valores normalizados o posteriores.
29. Un archivo/fuente importada debe conservar evidencia de origen.
30. Una misma comunicacion solo puede pertenecer a una mesa activa.
31. Una mesa activa no puede cambiar de aula durante la misma sesion.
32. Un simposio indivisible no puede dividirse salvo decision aprobada.
33. Una actividad bloqueada reduce disponibilidad de los espacios/franjas afectados.
34. Una modificacion masiva debe crear version o copia antes de aplicarse.
35. El historial es inmutable y no reconstruye por si solo el estado actual.

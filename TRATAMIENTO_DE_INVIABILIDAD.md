# Tratamiento de inviabilidad

## Principio

El motor debe detectar cuando no existe una solucion que cumpla todas las restricciones duras. En ese caso no debe inventar una solucion silenciosamente.

## Estado inviable

Un escenario es inviable cuando al menos una restriccion dura no puede satisfacerse con los recursos, franjas, aulas, duraciones y participantes disponibles.

## Informe de inviabilidad

Debe mostrar:

- por que el escenario es inviable;
- que restricciones entran en contradiccion;
- que personas, sesiones o aulas estan afectadas;
- que capacidad falta;
- que cambios permitirian resolverlo.

## Alternativas sugeridas

El motor puede proponer:

- añadir una franja;
- recuperar un aula;
- reducir duracion;
- dividir una mesa;
- convertir una actividad a modalidad virtual;
- flexibilizar una preferencia;
- mover una actividad bloqueada;
- retirar una comunicacion;
- ampliar el dia.

Nunca debe degradar automaticamente una restriccion obligatoria a preferente.

## Ejemplos

### Siete sesiones y cuatro aulas

Si una franja tiene siete sesiones simultaneas y solo cuatro aulas disponibles, el motor debe indicar falta de tres aulas o necesidad de mover/dividir tres sesiones.

### Restriccion obligatoria incompatible

Si una persona solo puede viernes mañana y no queda ninguna franja/aula compatible, el motor debe mostrar que falta capacidad en viernes mañana o que la restriccion impide ubicar la comunicacion.

### Simposio indivisible sin hueco

Si un simposio indivisible de 90 minutos no cabe en ninguna franja disponible, el escenario es inviable salvo que se amplie una franja, se cree una nueva o se autorice division.

## Fuerza manual

La persona usuaria puede forzar manualmente una solucion con conflictos duros, pero:

- debe recibir advertencia clara;
- debe quedar registrado en historial;
- debe aparecer en programa interno;
- no debe aparecer como solucion limpia.

# Algoritmo MVP de planificacion

## Alcance del MVP

La primera implementacion del motor se limita a:

1. Validar el programa existente.
2. Detectar elementos afectados por una `Decision`.
3. Recalcular duraciones.
4. Buscar huecos compatibles.
5. Proponer una alternativa conservadora.
6. Explicar cada movimiento.
7. Detectar inviabilidad.
8. Permitir revision manual.
9. Aplicar solo con confirmacion.
10. Crear nueva version.

Queda para segunda version:

- propuesta equilibrada completa;
- propuesta compacta completa;
- optimizacion global;
- pesos avanzados configurables;
- busqueda semantica de afinidad tematica;
- minimizacion avanzada de desplazamientos.

## Enfoque

Algoritmo determinista y explicable:

- heuristica greedy;
- backtracking limitado;
- busqueda local solo cuando sea necesario;
- sin optimizacion global compleja.

## Orden de resolucion de cambios simultaneos

Este orden sirve para recalcular y proponer, no para aplicar automaticamente decisiones sin aprobacion.

1. Cancelaciones, retiradas y sustituciones.
2. Disponibilidad real de personas y restricciones duras personales.
3. Bloqueos institucionales, plenarias y pausas.
4. Disponibilidad y cierre de aulas.
5. Cambios de duracion y capacidad temporal.
6. Integridad de simposios y mesas.
7. Preferencias blandas.
8. Equilibrio y compactacion.

Justificacion: primero se eliminan o sustituyen elementos inexistentes; despues se respetan imposibilidades humanas; luego bloqueos del programa; despues recursos fisicos; luego capacidad temporal; despues integridad academica; finalmente preferencias y optimizacion.

## Orden de dificultad inicial

1. Bloques bloqueados o con una unica franja valida.
2. Simposios indivisibles.
3. Bloques con muchas personas o restricciones.
4. Bloques largos.
5. Bloques hibridos o con equipamiento especifico.
6. Mesas ordinarias flexibles.

## Pasos del algoritmo

1. Recibir escenario y version base.
2. Aplicar decisiones aprobadas al escenario, no al programa oficial.
3. Recalcular duraciones de bloques afectados.
4. Recalcular disponibilidades activas por franja.
5. Calcular conflictos del escenario base.
6. Identificar bloques afectados.
7. Ordenar bloques afectados por dificultad.
8. Para cada bloque, generar candidatos compatibles:
   - misma franja y aula actual si sigue siendo valida;
   - misma franja, otra aula compatible;
   - misma dia, otra franja compatible;
   - otra dia/franja compatible;
   - division solo si esta permitida.
9. Filtrar candidatos que incumplen restricciones duras.
10. Puntuar candidatos con criterio conservador:
   - mantener dia;
   - mantener franja;
   - mantener aula;
   - minimizar personas afectadas;
   - respetar preferencias altas;
   - minimizar huecos.
11. Elegir mejor candidato.
12. Si un candidato elegido invalida otros bloques, activar backtracking limitado.
13. Si no hay candidato, marcar escenario como inviable y explicar causa.
14. Generar modificaciones propuestas y explicaciones.

## Backtracking limitado

El backtracking se limita por:

- numero maximo de bloques a reconsiderar;
- numero maximo de candidatos por bloque;
- tiempo maximo de calculo;
- profundidad maxima.

Si se supera el limite, el escenario se marca como valido con advertencias o inviable parcial, segun conflictos duros pendientes.

## Reproducibilidad

El orden de entidades, candidatos y desempates debe ser determinista.

Si se añade aleatoriedad en una version posterior, debe guardarse semilla.

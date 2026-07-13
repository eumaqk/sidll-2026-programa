# Motor de planificacion

> Estado: documento subordinado. La definicion canonica vigente esta en `MODELO_CANONICO_DEFINITIVO.md`, `ESTADOS_E_INVARIANTES.md` y `ALGORITMO_MVP_PLANIFICACION.md`. Si hay contradiccion, prevalecen esos documentos.

## Objetivo

El motor de planificacion debe construir, validar, simular y reorganizar el programa del XXVII Congreso Internacional SIDLL 2026 cuando cambien comunicaciones, participantes, presentadores, simposios, restricciones horarias, duraciones, franjas, aulas disponibles por franja, cancelaciones, retiradas, modalidades y actividades bloqueadas.

El motor debe ser local, explicable, reproducible y controlado por la persona usuaria. Nunca debe rehacer automaticamente todo el programa sin confirmacion.

## Principios

- El programa oficial se conserva siempre hasta que la persona usuaria aplique explicitamente un escenario.
- Toda reorganizacion se calcula primero sobre un escenario independiente.
- Las restricciones duras bloquean una propuesta valida salvo fuerza manual.
- Las restricciones blandas penalizan la propuesta, pero pueden incumplirse si no existe una solucion perfecta.
- La disponibilidad de aulas se calcula por dia y franja, nunca con un contador global.
- Cada movimiento debe poder explicarse.
- Con los mismos datos, restricciones, pesos y configuracion, el resultado debe ser reproducible.

## Entradas del motor

- Programa oficial o version base.
- Bloques programables.
- Franjas.
- Catalogo de espacios.
- Disponibilidad de espacios por franja.
- Restricciones duras y blandas.
- Pesos configurables.
- Duraciones de comunicaciones, debate, mesas, simposios y pausas.
- Cancelaciones, retiradas y cambios de presentador.
- Estado de personas asistentes.
- Configuracion de propuesta: conservadora, equilibrada o compacta.

## Salidas del motor

- Escenario calculado.
- Programa resultante.
- Conflictos.
- Restricciones duras incumplidas.
- Preferencias incumplidas.
- Puntuacion total.
- Resumen de impacto.
- Movimientos propuestos.
- Alternativas descartadas.
- Explicaciones por sesion y por movimiento.
- Informe de inviabilidad, si no hay solucion valida.

## Flujo logico canonico

Informacion recibida -> Decision -> restricciones o modificaciones aprobadas -> simulacion sobre escenario -> estado resultante del programa -> calculo de conflictos -> propuestas de resolucion -> cambios aplicados -> nueva version e historial.

El conflicto es siempre resultado calculado a partir del estado del programa, restricciones activas, disponibilidades, asignaciones, duraciones y bloqueos. No es editable ni fuente de verdad.

El algoritmo MVP detallado esta en `ALGORITMO_MVP_PLANIFICACION.md`.

## Restricciones duras

Una propuesta valida no puede incumplir restricciones duras, salvo fuerza manual explicita. Si se fuerza manualmente, el conflicto debe quedar visible.

Incluyen como minimo:

- Una persona no puede participar en dos actividades simultaneas.
- Una persona presentadora no puede presentar dos comunicaciones simultaneas.
- Una presidencia no puede presidir dos sesiones simultaneas.
- Un aula no puede alojar dos sesiones simultaneas.
- Una sesion solo puede asignarse a un aula disponible en esa franja.
- Una sesion no puede ocupar un aula cerrada, bloqueada o reservada para otro uso.
- Una sesion debe caber dentro de su franja.
- Una plenaria, pausa o actividad bloqueada debe respetarse.
- Una sesion presencial necesita un aula fisica.
- Una sesion virtual necesita los datos tecnicos necesarios.
- Una sesion hibrida necesita un aula compatible.
- Una restriccion marcada como obligatoria debe respetarse.
- Una comunicacion cancelada o retirada no puede aparecer como activa.
- Una comunicacion debe tener una persona presentadora valida.
- Un simposio que no admite division debe mantenerse unido.
- Una asignacion debe coincidir en dia, franja y disponibilidad de aula.

## Restricciones blandas

Pueden incumplirse cuando no existe una solucion perfecta, pero penalizan la propuesta:

- Preferencias de dia.
- Preferencias de mañana o tarde.
- Mantener juntas las intervenciones de personas que viajan juntas.
- Mantener un simposio en la misma aula.
- Mantener un simposio en una unica franja cuando sea posible.
- Evitar primeras o ultimas horas.
- Mantener las mesas ya comunicadas.
- Reducir cambios respecto al programa actual.
- Evitar cambiar de dia.
- Equilibrar el numero de comunicaciones por mesa.
- Equilibrar la carga entre franjas y dias.
- Evitar lineas tematicas muy similares de forma simultanea.
- Minimizar huecos.
- Mantener presidencias ya asignadas.
- Respetar aulas preferentes.
- Reducir desplazamientos entre edificios.

## Propuestas automaticas

### Propuesta conservadora

- Cambia el menor numero posible de sesiones.
- Mantiene dias, franjas y aulas cuando siguen siendo validos.
- Prioriza el menor impacto sobre participantes.

### Propuesta equilibrada

- Minimiza conflictos.
- Respeta el maximo posible de preferencias.
- Distribuye razonablemente las sesiones.

Esta propuesta queda para una segunda version completa. En Fase 1 puede existir solo como comparador conceptual o salida no automatizada.

### Propuesta compacta

- Reduce aulas, franjas y huecos.
- Permite mas cambios respecto al programa actual.
- Mantiene las restricciones duras.

Esta propuesta queda para una segunda version completa. En Fase 1 el motor automatico implementa solo propuesta conservadora.

Cada propuesta debe indicar puntuacion total, restricciones duras incumplidas, preferencias incumplidas, sesiones desplazadas, cambios de dia, cambios de franja, cambios de aula, participantes afectados, simposios divididos, aulas utilizadas, huecos, conflictos restantes y explicacion de decisiones.

## Reproducibilidad

Con los mismos datos, restricciones, pesos y configuracion, el motor debe producir el mismo resultado.

Si se usan criterios aleatorios para explorar alternativas:

- debe guardarse la semilla;
- debe permitirse repetir el calculo;
- debe indicarse que existen variaciones;
- debe permitirse fijar el resultado.

## Casos reales

### Caso A. Eliminar Aula 11 de la primera franja del miercoles

Primera franja: Aula 5, Aula 8, Aula 11, Aula 112. Segunda franja: Aula 55, Aula 34, Aula 1, Aula 23, Aula 67, Aula 89.

Si se elimina Aula 11 de la primera franja:

1. La disponibilidad `Aula 11 + miercoles + franja 1` pasa a no disponible o bloqueada.
2. El motor identifica la asignacion que usaba Aula 11.
3. La sesion queda marcada como afectada.
4. El motor busca alternativas solo en Aula 5, Aula 8 y Aula 112 para esa misma franja.
5. Si no caben todas las sesiones, propone mover la sesion a otra franja compatible o compactar/repartir segun el perfil del escenario.
6. La explicacion debe indicar que el movimiento se debe a perdida de disponibilidad del Aula 11.

### Caso B. Boris Vazquez-Calvo no puede el miercoles por la tarde

1. Se registra restriccion de indisponibilidad obligatoria o pendiente de confirmacion para Boris.
2. Se vincula a `SIDLL26-127` y a la persona Boris Vazquez-Calvo.
3. Si ya estaba asignado miercoles tarde, el escenario queda con conflicto duro.
4. El motor propone mover su simposio o actividad a otra franja donde Boris este disponible.
5. Si el simposio no admite division, se mueve unido.

### Caso C. Gerardo Fernandez San Emeterio solicita viernes por la mañana

1. Se registra como preferencia de prioridad alta pendiente de confirmacion.
2. No se convierte en obligatoria sin confirmacion.
3. El motor favorece viernes mañana, pero puede incumplirlo si impide una solucion mejor.
4. Si se incumple, la propuesta debe explicarlo.

### Caso D. Comunicaciones de 10 a 12 minutos

1. Se modifica la duracion global.
2. El motor recalcula duracion de mesas: comunicaciones + debate + transiciones si existen.
3. Marca mesas que ya no caben en su franja.
4. Propone dividir, reducir numero de comunicaciones, mover mesa, ampliar franja o ajustar debate.

### Caso E. Dos personas cancelan su asistencia

1. Se marcan personas como no asistentes.
2. Se comprueban comunicaciones, presentaciones, presidencias, simposios y sustituciones.
3. Comunicaciones sin presentador valido quedan en conflicto duro.
4. El motor propone cambio de presentador, retirada, conversion virtual o reubicacion.

### Caso F. Cuatro aulas para siete sesiones simultaneas

1. El escenario detecta falta de capacidad: 7 sesiones y 4 aulas disponibles.
2. Propuesta conservadora: mantiene cuatro sesiones y mueve las tres menos disruptivas.
3. Propuesta equilibrada: redistribuye segun restricciones y preferencias para minimizar impacto general.
4. Propuesta compacta: concentra sesiones, reduce huecos y permite mas cambios.
5. Las tres propuestas se comparan por restricciones, movimientos, personas afectadas y puntuacion.

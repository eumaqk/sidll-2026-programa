# Reglas de mesas y duraciones

## Definicion de mesa

Para la primera version, una mesa de comunicaciones es un tipo de `BloqueProgramable` compuesto por varios `TrabajoAcademico` de tipo `comunicacion`.

Confirmacion canonica:

Mesa != SesionProgramada.

La mesa es el contenido agrupado. La `SesionProgramada` es su colocacion temporal.

## Reglas iniciales de mesa

- Minimo recomendado: 3 comunicaciones.
- Maximo recomendado: 5 comunicaciones.
- Maximo absoluto: configurable.
- Puede pertenecer a un unico panel.
- Puede mezclar paneles solo mediante autorizacion explicita.
- Puede tener presidencia.
- La presidencia puede ser obligatoria para confirmar la mesa, segun configuracion.
- Puede dividirse mediante una `Decision`.
- No puede cambiar de aula durante la misma sesion.
- Puede trasladarse completa a otra franja.
- El orden de comunicaciones forma parte de la mesa.
- Una misma comunicacion solo puede pertenecer a una mesa activa.
- La mesa es el `BloqueProgramable`.
- Su colocacion concreta es la `SesionProgramada`.

## Parametros temporales configurables

- Duracion de cada comunicacion.
- Transicion entre comunicaciones.
- Debate conjunto al final.
- Debate individual, si se activa.
- Margen de seguridad.
- Pausa interna.
- Duracion fija o calculada.
- Redondeo.
- Tolerancia maxima.

Todos los parametros pueden configurarse globalmente y sobrescribirse en un bloque concreto.

## Formula inicial con debate conjunto

Duracion total =

`numero_comunicaciones * duracion_comunicacion`
+ `numero_transiciones * duracion_transicion`
+ `debate_conjunto`
+ `pausa_interna`
+ `margen_seguridad`

Para la primera version, `numero_transiciones = n - 1`, porque solo se cuentan cambios entre comunicaciones.

Ejemplo:

5 comunicaciones * 10 minutos + 4 transiciones * 1 minuto + 15 minutos de debate = 69 minutos.

## Debate individual

Si se activa debate individual:

Duracion total =

`n * duracion_comunicacion`
+ `n * debate_individual`
+ `(n - 1) * duracion_transicion`
+ `pausa_interna`
+ `margen_seguridad`

## Simposio

Un simposio puede tener:

- duracion fija, por ejemplo 90 minutos;
- duracion calculada por comunicaciones internas;
- division autorizada en varias sesiones.

Si es indivisible, debe caber completo en una franja compatible.

Si se divide:

- cada parte genera un `BloqueProgramable` o una parte programable vinculada al simposio;
- cada parte debe respetar orden, participantes y restricciones;
- la division requiere decision aprobada si el simposio estaba marcado como indivisible o unido.

## Taller

Un taller se trata como bloque de duracion fija salvo configuracion explicita.

Debe respetar modalidad, capacidad y equipamiento.

## Plenarias y pausas

Plenarias, inauguracion, clausura, pausas y almuerzos son bloques normalmente bloqueados.

Pueden reducir disponibilidad de aulas o franjas.

## Recalculo por retirada

Si se retira una comunicacion:

1. `TrabajoAcademico` pasa a retirado.
2. Se elimina de la mesa activa o se marca la mesa como afectada.
3. Se recalcula duracion.
4. Se conserva el orden de las restantes.
5. Si la mesa queda por debajo del minimo recomendado, se genera advertencia blanda.

## Si la duracion no cabe

Si duracion calculada > franja:

- conflicto duro si no cabe temporalmente;
- alternativas: mover mesa, dividir mesa, reducir debate, ampliar franja, retirar comunicacion o crear nueva franja.

Si duracion calculada < franja:

- la mesa es valida;
- el hueco puede penalizar segun configuracion blanda.

# Gestion continua de cambios

> Estado: documento subordinado. La entidad canonica que organiza el flujo humano es `Decision`, definida en `MODELO_CANONICO_DEFINITIVO.md`.

## Principio central

La aplicacion debe estar diseñada para trabajar con cambios continuos durante varios meses. La introduccion de nuevas restricciones, modificaciones y datos no sera una situacion excepcional, sino el uso habitual de la aplicacion.

La herramienta debe ser flexible, editable, acumulativa y reversible.

## Requisitos obligatorios

- Añadir nuevas restricciones en cualquier momento.
- Añadir nuevos datos en cualquier momento: comunicaciones, personas, simposios, mesas, aulas, franjas, dias, actividades, observaciones y restricciones.
- Introducir datos manualmente, mediante formularios, edicion en tabla, importacion desde Excel/CSV/JSON y pegado desde el portapapeles.
- Detectar si un dato importado ya existe.
- Proponer actualizacion o creacion.
- Conservar valores anteriores.
- Mostrar previsualizacion antes de importar.
- Evitar sobrescrituras silenciosas.
- Permitir edicion rapida en tablas para estado, aula, franja, duracion, presentador, mesa, prioridad y confirmacion.
- Ofrecer deshacer y rehacer.
- Registrar historial cronologico de cambios.

## Pantalla "Restricciones y cambios"

Debe permitir:

- crear;
- editar;
- duplicar;
- desactivar;
- archivar;
- eliminar con confirmacion;
- filtrar;
- buscar;
- ordenar;
- aplicar cambios masivos.

Debe mostrar:

- nuevas restricciones;
- restricciones sin aplicar;
- conflictos no resueltos;
- personas afectadas;
- comunicaciones afectadas;
- cambios urgentes.

## Formulario rapido

Debe existir un formulario rapido para añadir restricciones sin navegar por varias pantallas.

Desde la ficha de una persona, comunicacion, mesa, simposio, aula o franja debe poder añadirse una restriccion relacionada.

## Estados de cambio

Todo cambio debe pasar por estados como:

- borrador;
- pendiente de revision;
- confirmado;
- aplicado;
- descartado;
- sustituido.

## Simulacion y aplicacion

Antes de aplicar una decision aprobada o una restriccion derivada al programa, la aplicacion debe calcular:

- sesiones afectadas;
- personas afectadas;
- conflictos que aparecen;
- alternativas disponibles;
- cambios minimos necesarios.

La simulacion debe realizarse dentro de un escenario independiente. La creacion o calculo de un escenario no modifica el programa oficial.

La aplicacion nunca debe rehacer automaticamente todo el programa sin confirmacion.

Debe permitir aplicar:

- un unico cambio;
- varios cambios seleccionados;
- todas las restricciones pendientes.

Debe existir un modo "simular cambio" para ver el resultado sin alterar el programa actual.

Antes de aplicar cambios importantes, debe crear una version y una copia de seguridad.

## Historial

El historial cronologico de cambios debe guardar:

- valor anterior;
- valor nuevo;
- causa;
- fecha;
- persona responsable;
- version afectada.

## Comparacion

Debe poder compararse:

- programa actual;
- programa tras aplicar una restriccion;
- programa tras aplicar varias restricciones.

Para cambios complejos, la comparacion debe incluir propuesta conservadora, propuesta equilibrada y propuesta compacta, con puntuacion, conflictos, movimientos e impacto.

## Prioridades de diseño

La interfaz debe estar pensada para uso continuado durante meses, con entradas frecuentes de datos y restricciones.

La prioridad de diseño debe ser:

- rapidez para introducir cambios;
- claridad para entender su impacto;
- facilidad para corregirlos;
- seguridad para volver atras;
- minima perdida de tiempo.

## Pruebas obligatorias

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

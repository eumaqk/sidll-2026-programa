# Flujo de aplicacion de cambios

> Estado: documento subordinado. El flujo canonico vigente parte de `Decision`, no de conflicto ni de impacto.

## Objetivo

Permitir introducir, simular, aplicar, comparar, deshacer y auditar cambios sin rehacer automaticamente todo el programa y sin perdida silenciosa de informacion.

## Flujo base

1. Registrar informacion recibida.
2. Crear o actualizar una `Decision`.
3. Interpretar la decision en restricciones o modificaciones aprobadas.
4. Crear o actualizar escenario de simulacion.
5. Simular resultado.
6. Calcular conflictos e impacto.
7. Revisar propuestas de resolucion.
8. Aprobar o rechazar.
9. Crear version y copia de seguridad si el cambio es importante.
10. Aplicar con confirmacion.
11. Registrar historial.
12. Comparar antes y despues.
13. Permitir deshacer menor o recuperar version anterior.

## Entrada de cambios

Los cambios pueden entrar por:

- formulario rapido;
- pantalla "Restricciones y cambios";
- ficha de persona;
- ficha de comunicacion;
- ficha de mesa;
- ficha de simposio;
- ficha de aula;
- ficha de franja;
- edicion rapida en tabla;
- importacion Excel/CSV/JSON;
- pegado desde portapapeles.

## Previsualizacion de importacion

Al importar cambios o datos nuevos:

1. Detectar coincidencias con datos existentes.
2. Separar creaciones, actualizaciones y dudas.
3. Mostrar valor actual y valor entrante.
4. Permitir aceptar, rechazar o editar cada cambio.
5. Conservar valores anteriores.
6. Registrar fuente e historial.

## Simulacion

El modo "simular cambio" debe:

- trabajar sobre una copia temporal del programa actual;
- no alterar el programa vigente;
- mostrar sesiones afectadas;
- mostrar personas afectadas;
- mostrar conflictos nuevos;
- mostrar alternativas;
- mostrar cambios minimos;
- permitir comparar simulaciones.
- detectar si el escenario es inviable.
- explicar cada movimiento propuesto.

## Aplicacion

La aplicacion puede aplicar:

- un unico cambio;
- varios cambios seleccionados;
- todas las restricciones pendientes.

Antes de aplicar cambios importantes:

- crear version;
- crear copia de seguridad;
- registrar causa;
- registrar persona responsable si se conoce.

## Deshacer y rehacer

Debe poder deshacerse un cambio aplicado sin borrar su historial.

Debe poder rehacerse un cambio deshecho.

Para cambios complejos, debe poder restaurarse una version anterior.

## Comparacion

Debe poder compararse:

- programa actual;
- programa simulado tras una restriccion;
- programa simulado tras varias restricciones;
- programa antes de aplicar;
- programa despues de aplicar.

La comparacion debe mostrar:

- sesiones movidas;
- aulas cambiadas;
- franjas cambiadas;
- personas afectadas;
- restricciones resueltas;
- conflictos nuevos;
- conflictos eliminados.

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

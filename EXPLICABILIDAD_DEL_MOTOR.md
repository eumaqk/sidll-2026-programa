# Explicabilidad del motor

## Principio

Toda propuesta automatica debe poder explicarse. La persona usuaria debe entender por que se propone cada cambio y que consecuencias tiene.

## Explicacion por movimiento

Para cada movimiento debe indicarse:

- que se ha movido;
- desde donde;
- hacia donde;
- por que;
- que restriccion resuelve;
- que preferencias incumple;
- que alternativas se descartaron;
- que impacto tiene.

## Vista por sesion

La persona usuaria debe poder abrir una sesion y ver:

- restricciones que la afectan;
- conflictos actuales;
- cambios propuestos;
- motivo de la propuesta;
- opciones alternativas.

## Explicacion por escenario

Cada escenario debe incluir:

- resumen de estrategia usada;
- restricciones duras incumplidas;
- preferencias incumplidas;
- puntuacion;
- sesiones desplazadas;
- personas afectadas;
- cambios de dia, franja y aula;
- simposios divididos;
- huecos;
- decisiones principales.

## Alternativas descartadas

Cuando el motor descarte una alternativa relevante, debe poder indicar la razon:

- aula no disponible;
- conflicto de persona;
- no cabe en franja;
- rompe simposio indivisible;
- incumple restriccion obligatoria;
- peor puntuacion;
- mas cambios que otra alternativa.

## Reproducibilidad

La explicacion debe incluir configuracion usada:

- version base;
- restricciones activas;
- pesos;
- perfil de propuesta;
- duraciones;
- disponibilidad de aulas;
- semilla si se uso exploracion aleatoria.

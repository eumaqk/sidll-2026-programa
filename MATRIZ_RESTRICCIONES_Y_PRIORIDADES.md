# Matriz de restricciones y prioridades

## Categorias

### Restricciones duras

No pueden incumplirse en una propuesta valida, salvo que la persona usuaria fuerce manualmente el cambio. Si se fuerzan, deben quedar visibles como conflicto.

### Restricciones blandas

Pueden incumplirse si no existe una solucion perfecta, pero penalizan la puntuacion de la propuesta.

## Campos obligatorios de cada restriccion

```js
RestriccionPlanificacion {
  id: string,
  tipo: string,
  caracter: "dura" | "blanda",
  prioridad: "bloqueante" | "muy_alta" | "alta" | "media" | "baja",
  peso: number | "bloqueante",
  entidad_afectada: string,
  alcance: "persona" | "comunicacion" | "simposio" | "mesa" | "aula" | "franja" | "dia" | "actividad" | "programa",
  fuente: string,
  estado: "borrador" | "pendiente_revision" | "confirmada" | "aplicada" | "descartada" | "sustituida",
  forzable: boolean,
  explicacion_incumplimiento?: string
}
```

## Escala inicial de pesos

Los pesos deben ser configurables por la persona usuaria.

| Prioridad | Peso inicial |
| --- | --- |
| Restriccion obligatoria | Bloqueante |
| Preferencia muy alta | 100 |
| Preferencia alta | 50 |
| Preferencia media | 20 |
| Preferencia baja | 5 |

No se debe convertir una preferencia en obligacion sin confirmacion.

## Matriz inicial

| Restriccion | Caracter | Prioridad inicial | Peso | Forzable |
| --- | --- | --- | --- | --- |
| Persona en dos actividades simultaneas | Dura | Bloqueante | Bloqueante | Si, manualmente |
| Presentador en dos comunicaciones simultaneas | Dura | Bloqueante | Bloqueante | Si, manualmente |
| Presidencia en dos sesiones simultaneas | Dura | Bloqueante | Bloqueante | Si, manualmente |
| Aula con dos sesiones simultaneas | Dura | Bloqueante | Bloqueante | Si, manualmente |
| Aula no disponible en la franja | Dura | Bloqueante | Bloqueante | Si, manualmente |
| Aula cerrada, bloqueada o reservada | Dura | Bloqueante | Bloqueante | Si, manualmente |
| Sesion fuera de franja | Dura | Bloqueante | Bloqueante | Si, manualmente |
| Plenaria, pausa o actividad bloqueada | Dura | Bloqueante | Bloqueante | Si, manualmente |
| Comunicacion cancelada o retirada activa | Dura | Bloqueante | Bloqueante | Si, manualmente |
| Comunicacion sin presentador valido | Dura | Bloqueante | Bloqueante | Si, manualmente |
| Simposio indivisible dividido | Dura | Bloqueante | Bloqueante | Si, manualmente |
| Preferencia de dia | Blanda | Alta | 50 | Si |
| Preferencia de mañana/tarde | Blanda | Alta | 50 | Si |
| Viajan juntas y desean mismo dia | Blanda | Alta | 50 | Si |
| Mantener simposio en misma aula | Blanda | Media | 20 | Si |
| Mantener simposio en una unica franja | Blanda | Media | 20 | Si |
| Evitar primeras/ultimas horas | Blanda | Baja | 5 | Si |
| Mantener mesas ya comunicadas | Blanda | Muy alta | 100 | Si |
| Reducir cambios respecto al programa actual | Blanda | Muy alta | 100 | Si |
| Evitar cambio de dia | Blanda | Alta | 50 | Si |
| Evitar cambio de franja | Blanda | Media | 20 | Si |
| Evitar cambio de aula | Blanda | Baja | 5 | Si |
| Equilibrar comunicaciones por mesa | Blanda | Media | 20 | Si |
| Equilibrar carga entre franjas/dias | Blanda | Media | 20 | Si |
| Evitar temas similares simultaneos | Blanda | Media | 20 | Si |
| Minimizar huecos | Blanda | Baja | 5 | Si |
| Mantener presidencias asignadas | Blanda | Alta | 50 | Si |
| Respetar aulas preferentes | Blanda | Media | 20 | Si |
| Reducir desplazamientos entre edificios | Blanda | Baja | 5 | Si |

## Reglas de desempate

Cuando dos propuestas tengan puntuacion parecida, el motor debe preferir, por este orden:

1. Menor numero de restricciones duras incumplidas.
2. Menor numero de personas afectadas.
3. Menor numero de sesiones desplazadas.
4. Menor numero de cambios de dia.
5. Menor numero de cambios de franja.
6. Menor numero de cambios de aula.
7. Menor numero de simposios divididos.
8. Menor numero de preferencias incumplidas.
9. Mejor equilibrio de carga.
10. Menor numero de huecos.

Este orden prioriza seguridad academica y comunicativa antes que optimizacion estetica. Solo deberia modificarse si la organizacion decide que compactar el programa o equilibrar carga es mas importante que minimizar cambios.

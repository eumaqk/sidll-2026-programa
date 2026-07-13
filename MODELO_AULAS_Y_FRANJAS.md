# Modelo de aulas y franjas

## Principio estructural

La disponibilidad de aulas se define por franja, no por dia ni de forma global.

El catalogo general de espacios solo indica que un aula existe. La disponibilidad real se decide en cada combinacion de dia y franja.

El motor de planificacion usa esta disponibilidad como restriccion dura: una sesion solo puede asignarse a un aula disponible, no bloqueada y compatible en esa combinacion concreta de dia y franja.

Ejemplo:

- Miercoles, primera franja: Aula 5, Aula 8, Aula 11, Aula 112.
- Miercoles, segunda franja: Aula 55, Aula 34, Aula 1, Aula 23, Aula 67, Aula 89.

## Entidades

### Dia

Representa una jornada del congreso.

```js
Dia {
  id: string,
  fecha: string,
  etiqueta: string,
  hora_inicio?: string,
  hora_fin?: string,
  observaciones?: string
}
```

### Franja

Representa un bloque horario dentro de un dia. Puede ser de comunicaciones, simposios, plenaria, pausa u otra actividad.

```js
Franja {
  id: string,
  dia_id: string,
  etiqueta: string,
  hora_inicio: string,
  hora_fin: string,
  tipo: "comunicaciones" | "simposio" | "plenaria" | "pausa" | "social" | "otro",
  bloqueada?: boolean,
  observaciones?: string
}
```

### Espacio

Representa el catalogo general de aulas o salas. No implica disponibilidad.

```js
Espacio {
  id: string,
  nombre: string,
  edificio?: string,
  ubicacion?: string,
  capacidad_base?: number,
  equipamiento_base?: string[],
  observaciones?: string
}
```

### DisponibilidadEspacio

Representa la disponibilidad concreta de un espacio en una combinacion de dia y franja.

```js
DisponibilidadEspacio {
  id: string,
  espacio_id: string,
  dia_id: string,
  franja_id: string,
  disponible: boolean,
  uso_reservado?: string,
  modalidad_permitida?: string[],
  capacidad_efectiva?: number,
  equipamiento_disponible_en_esa_franja?: string[],
  prioridad?: number,
  bloqueada: boolean,
  observaciones?: string
}
```

Reglas:

- Una franja solo puede usar espacios con `disponible: true` y `bloqueada: false`.
- El numero maximo de sesiones simultaneas de una franja es el numero de disponibilidades compatibles activas en esa franja.
- Una plenaria, pausa o actividad bloqueada puede reservar o bloquear uno o varios espacios.
- Si se elimina o bloquea una disponibilidad, todas las asignaciones que dependan de ella pasan a estar afectadas.

### Sesion

Representa una unidad programable: mesa de comunicaciones, simposio, plenaria, pausa u otra actividad.

```js
Sesion {
  id: string,
  titulo: string,
  tipo: "mesa" | "simposio" | "plenaria" | "pausa" | "otro",
  dia_id: string,
  franja_id: string,
  hora_inicio: string,
  hora_fin: string,
  duracion_minutos: number,
  modalidad_requerida?: string,
  capacidad_requerida?: number,
  equipamiento_requerido?: string[],
  items: string[],
  estado: "borrador" | "confirmada" | "cancelada",
  observaciones?: string
}
```

### Asignacion

Relaciona una sesion con un espacio disponible en una franja concreta.

```js
Asignacion {
  id: string,
  sesion_id: string,
  espacio_id: string,
  disponibilidad_espacio_id: string,
  dia_id: string,
  franja_id: string,
  orden?: number,
  bloqueada?: boolean,
  observaciones?: string
}
```

Reglas:

- `disponibilidad_espacio_id` es obligatorio para impedir asignaciones a aulas inexistentes en una franja.
- `dia_id` y `franja_id` de la asignacion deben coincidir con los de la sesion y la disponibilidad.
- Una asignacion queda invalida si la disponibilidad asociada pasa a no disponible, reservada o bloqueada.

## Relacion con BloqueProgramable

Todo bloque que ocupe tiempo puede consumir disponibilidad de espacios: mesas, simposios, plenarias, pausas, actividades sociales, bloqueos tecnicos y bloqueos organizativos.

Las plenarias, pausas y actividades bloqueadas deben modelarse como bloques programables porque pueden limitar o anular aulas disponibles en una franja.

## Pruebas de aceptacion

### Prueba de aulas variables

- Crear Franja 1 con aulas disponibles: 5, 8, 11, 112.
- Crear Franja 2 con aulas disponibles: 55, 34, 1, 23, 67, 89.
- Verificar que Franja 1 solo muestra 5, 8, 11, 112.
- Verificar que Franja 2 solo muestra 55, 34, 1, 23, 67, 89.
- Verificar que el maximo de sesiones simultaneas es 4 en Franja 1 y 6 en Franja 2.
- Verificar que el generador no asigna sesiones a aulas inexistentes en esa franja.
- Eliminar Aula 11 de Franja 1 y verificar que la sesion asignada a Aula 11 queda marcada como afectada.
- Verificar que el sistema propone alternativas solo entre 5, 8 y 112 para esa franja, si son compatibles.

### Prueba de aula disponible solo en una franja

- Crear Aula 5 en el catalogo general.
- Marcar Aula 5 disponible en Franja 1.
- No crear disponibilidad de Aula 5 en Franja 2.
- Verificar que Aula 5 no aparece como opcion en Franja 2.

### Prueba de bloqueo por plenaria o pausa

- Crear una plenaria o pausa que reserva todas las aulas de una franja.
- Verificar que el maximo de sesiones simultaneas de comunicaciones en esa franja pasa a 0.
- Verificar que las sesiones previamente asignadas quedan marcadas como afectadas.

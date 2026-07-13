# Bloques programables

> Estado: documento subordinado. La definicion canonica vigente esta en `MODELO_CANONICO_DEFINITIVO.md` y `REGLAS_MESAS_Y_DURACIONES.md`.

## Concepto

`BloqueProgramable` representa cualquier elemento que ocupa tiempo en el programa.

`BloqueProgramable` define que debe programarse. `SesionProgramada` define cuando se programa. `AsignacionEspacio` define donde se programa.

Debe poder representar:

- mesa de comunicaciones;
- sesion de simposio;
- simposio completo;
- conferencia plenaria;
- inauguracion;
- clausura;
- taller;
- mesa redonda;
- pausa;
- almuerzo;
- actividad institucional;
- actividad social;
- bloqueo tecnico u organizativo.

## Entidad

```js
BloqueProgramable {
  id: string,
  tipo: "mesa_comunicaciones" | "sesion_simposio" | "simposio_completo" | "plenaria" | "inauguracion" | "clausura" | "taller" | "mesa_redonda" | "pausa" | "almuerzo" | "institucional" | "social" | "bloqueo_tecnico" | "bloqueo_organizativo",
  titulo: string,
  duracion_minutos: number,
  participantes: string[],
  comunicaciones: string[],
  modalidad: "presencial" | "virtual" | "hibrida",
  requisitos_tecnicos?: string[],
  capacidad_prevista?: number,
  divisible: boolean,
  numero_maximo_partes?: number,
  bloqueado: boolean,
  editable: boolean,
  dia_preferente?: string,
  franja_preferente?: string,
  restricciones_relacionadas: string[],
  prioridad: "alta" | "media" | "baja",
  estado_programacion: "no_programado" | "programado" | "afectado" | "confirmado" | "cancelado"
}
```

## Relacion con otras entidades

- `Sesion`: una sesion es una instancia programada de uno o varios bloques.
- `SesionProgramada`: colocacion temporal de un bloque. Es distinta del bloque.
- `Simposio`: puede ser un bloque completo indivisible o dividirse en varios bloques/sesiones si se permite.
- `Franja`: limita donde puede colocarse el bloque.
- `Aula` / `Espacio`: recurso fisico o tecnico necesario.
- `Asignacion`: relacion concreta entre bloque/sesion, aula, dia y franja.

## Reglas

- Todo elemento que ocupe tiempo debe representarse como `BloqueProgramable`.
- Las pausas, plenarias y bloqueos tecnicos tambien son bloques, porque reducen disponibilidad.
- Si un bloque esta marcado como `bloqueado`, el motor no debe moverlo sin autorizacion explicita.
- El estado academico vive en `TrabajoAcademico`, no en `BloqueProgramable`.
- Si `divisible` es falso, el bloque debe mantenerse unido.
- Si `divisible` es verdadero, el motor puede proponer division hasta `numero_maximo_partes`.

## Ejemplos

- Una mesa de 5 comunicaciones de 12 minutos + debate: bloque de tipo `mesa_comunicaciones`.
- Un simposio de 90 minutos indivisible: bloque `simposio_completo`, `divisible: false`.
- Una pausa cafe: bloque `pausa`, normalmente bloqueado.
- Un aula reservada por mantenimiento: bloque `bloqueo_tecnico`, asociado a disponibilidad de espacio.

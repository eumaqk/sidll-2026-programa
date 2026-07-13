# Modelo de restricciones

> Estado: documento subordinado. La definicion canonica vigente esta en `MODELO_CANONICO_DEFINITIVO.md` y `ESTADOS_E_INVARIANTES.md`.

## Entidad Restriccion

```js
Restriccion {
  id: string,
  titulo?: string,
  texto_original: string,
  interpretacion_estructurada: Record<string, unknown>,
  tipo: "disponibilidad" | "indisponibilidad" | "preferencia_dia" | "preferencia_franja" | "mismo_dia" | "distinta_franja" | "misma_mesa" | "distinta_mesa" | "modalidad" | "aula_especifica" | "equipamiento" | "duracion_especial" | "orden_intervencion" | "viaje" | "observacion",
  caracter: "obligatoria" | "preferente" | "informativa" | "pendiente_confirmar",
  prioridad: "alta" | "media" | "baja",
  estado: "borrador" | "pendiente_revision" | "confirmada" | "aplicada" | "descartada" | "sustituida",
  fuente: string,
  persona_que_la_anadio?: string,
  comentario_interno?: string,
  fecha_creacion: string,
  fecha_modificacion: string,
  historial_cambios: CambioHistorial[]
}
```

## Restricciones duras y blandas

Toda restriccion debe clasificarse como:

- `dura`: no puede incumplirse en una propuesta valida salvo fuerza manual.
- `blanda`: puede incumplirse, pero penaliza la puntuacion.

Campos adicionales:

```js
RestriccionPlanificacion {
  restriccion_id: string,
  caracter_planificacion: "dura" | "blanda",
  peso: number | "bloqueante",
  forzable: boolean,
  explicacion_incumplimiento?: string
}
```

Las preferencias no deben convertirse en obligaciones sin confirmacion.

## Vinculos posibles

Cada restriccion debe poder vincularse a:

```js
RestriccionVinculo {
  id: string,
  restriccion_id: string,
  entidad_tipo: "persona" | "comunicacion" | "simposio" | "mesa" | "aula" | "franja" | "dia" | "actividad_general",
  entidad_id: string,
  rol?: "afecta" | "referencia" | "comparacion" | "alternativa",
  confianza: "alta" | "media" | "baja",
  observaciones?: string
}
```

## Tipos de restriccion

- disponibilidad;
- indisponibilidad;
- preferencia de dia;
- preferencia de franja;
- mismo dia que otra persona;
- distinta franja que otra persona;
- misma mesa;
- distinta mesa;
- modalidad presencial o virtual;
- aula especifica;
- equipamiento necesario;
- duracion especial;
- orden de intervencion;
- coordinacion con viaje, llegada o salida;
- observacion libre.

## Impacto de restriccion

```js
ImpactoRestriccion {
  id: string,
  restriccion_id: string,
  version_base_id: string,
  sesiones_afectadas: string[],
  personas_afectadas: string[],
  comunicaciones_afectadas: string[],
  conflictos_generados: string[],
  alternativas: AlternativaCambio[],
  cambios_minimos: string[],
  calculado_en: string
}
```

## Historial

```js
CambioHistorial {
  id: string,
  entidad_tipo: string,
  entidad_id: string,
  campo?: string,
  valor_anterior: unknown,
  valor_nuevo: unknown,
  causa?: string,
  fecha: string,
  persona_responsable?: string,
  version_afectada?: string
}
```

## Reglas

- Ninguna restriccion confirmada debe aplicarse automaticamente sin accion explicita.
- Una restriccion puede existir sin estar aplicada.
- Una restriccion puede sustituir a otra sin borrar la anterior.
- Las restricciones descartadas o archivadas deben conservarse para trazabilidad.
- El impacto debe calcularse antes de aplicar restricciones confirmadas.
- El sistema debe permitir aplicar una restriccion, varias seleccionadas o todas las pendientes.
- La restriccion no gestiona el ciclo humano completo: ese ciclo pertenece a `Decision`.
- Los conflictos derivados de restricciones son calculados, no editables.

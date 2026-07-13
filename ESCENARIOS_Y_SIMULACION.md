# Escenarios y simulacion

> Estado: documento subordinado. La definicion canonica de `Escenario` esta en `MODELO_CANONICO_DEFINITIVO.md`; los estados oficiales estan en `ESTADOS_E_INVARIANTES.md`.

## Principio

La aplicacion no debe obligar a destruir el programa vigente para probar cambios. Todo cambio importante debe poder simularse en un escenario independiente.

## Ejemplos de escenarios

- Programa actual.
- Solo cuatro aulas disponibles.
- Comunicaciones de doce minutos.
- Cancelacion de varias personas.
- Nueva distribucion de simposios.
- Programa compacto.
- Programa conservador.

## Entidad Escenario

```js
Escenario {
  id: string,
  nombre: string,
  descripcion?: string,
  version_origen_id: string,
  cambios_incluidos: string[],
  restricciones_activas: string[],
  disponibilidades_espacio: string[],
  duraciones: Record<string, number>,
  programa_resultante?: unknown,
  conflictos: string[],
  puntuacion?: number,
  resumen_impacto?: ResumenImpacto,
  fecha_creacion: string,
  estado: "borrador" | "calculando" | "valido" | "valido_con_advertencias" | "inviable" | "aplicado" | "descartado" | "archivado",
  persona_creadora?: string,
  semilla_calculo?: string
}
```

## Operaciones

- Duplicar el programa actual como escenario.
- Simular una o varias decisiones aprobadas o restricciones activas en un escenario.
- Comparar varios escenarios.
- Editar un escenario.
- Descartar un escenario.
- Convertir un escenario en programa oficial.
- Volver al programa anterior.
- Exportar informe de comparacion.

## Estados

- `borrador`: escenario creado pero no calculado.
- `calculando`: motor generando propuesta.
- `valido`: no incumple restricciones duras.
- `valido_con_advertencias`: valido, pero con preferencias incumplidas o avisos.
- `inviable`: no hay solucion que cumpla restricciones duras.
- `aplicado`: convertido en programa oficial.
- `descartado`: descartado por la persona usuaria.
- `archivado`: conservado solo como referencia.

## Comparacion de escenarios

Cada comparacion debe mostrar:

- restricciones duras incumplidas;
- preferencias incumplidas;
- puntuacion total;
- sesiones desplazadas;
- cambios de dia;
- cambios de franja;
- cambios de aula;
- participantes afectados;
- simposios divididos;
- aulas utilizadas;
- huecos;
- conflictos restantes;
- explicacion de decisiones.

## Propuestas automaticas

### Conservadora

Minimiza cambios sobre el programa actual y prioriza estabilidad.

### Equilibrada

Minimiza conflictos, respeta preferencias y distribuye carga razonablemente.

### Compacta

Reduce aulas, franjas y huecos, permitiendo mas cambios mientras respete restricciones duras.

## Garantia

Crear, calcular, editar o descartar un escenario no modifica el programa oficial. Solo la accion explicita "convertir en programa oficial" puede hacerlo, creando antes version y copia de seguridad.

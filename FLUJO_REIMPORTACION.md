# Flujo de reimportacion

## Objetivo

Permitir recibir versiones posteriores del Excel u otras fuentes sin duplicar comunicaciones, borrar datos añadidos manualmente, perder decisiones, perder restricciones ni deshacer asignaciones silenciosamente.

Para resumenes completos definitivos, la unica fuente valida sera `resumenes_definitivos`. Las carpetas heterogeneas previas pueden usarse para titulos, autorias y datos academicos base, pero no para cargar el texto definitivo del resumen.

## Flujo

1. Cargar archivo.
2. Identificar fuente y calcular hash cuando sea posible.
3. Comparar con fuentes ya importadas.
4. Detectar registros nuevos, modificados, iguales y dudosos.
5. Mostrar previsualizacion.
6. Permitir crear, actualizar, ignorar o revisar.
7. Mantener valores originales anteriores.
8. Crear decision o evento de importacion cuando los cambios tengan impacto organizativo.
9. Crear copia de seguridad.
10. Aplicar.
11. Emitir informe.

## Reglas de identidad

- `SIDLL26-xxx` se conserva como identificador externo, no como ID interno.
- `ORDEN` se conserva como identificador externo de origen.
- La entidad interna mantiene su ID aunque cambien datos importados.
- Coincidencias inciertas quedan pendientes de revision.
- No se fusionan personas o trabajos automaticamente si la confianza no es alta.
- Para resumenes definitivos, `SIDLL26-xxx` exacto y `ORDEN` exacto son criterios determinantes.
- Apellidos de primera autoria solo son insuficientes si existe mas de una candidata.
- Una persona con varias comunicaciones exige revision manual salvo que exista codigo, orden, titulo o correo determinante.

## Clasificacion de cambios

- Nuevo: no existe correspondencia.
- Modificado: existe correspondencia clara y cambian valores.
- Igual: no hay cambios relevantes.
- Dudoso: posible correspondencia sin confianza suficiente.

## Proteccion

- Ningun valor original se sobrescribe.
- Las correcciones se guardan como valores normalizados o posteriores.
- Las asignaciones existentes no se eliminan por reimportacion sin decision aprobada.
- Restricciones, decisiones e historial sobreviven a reimportaciones.

## Flujo especifico de `resumenes_definitivos`

1. Detectar carpeta `resumenes_definitivos`.
2. Listar archivos DOCX/PDF y conservar nombre original, ruta, fecha y hash.
3. Normalizar nombre de archivo ignorando mayusculas, tildes, guiones, guiones bajos, extension, espacios redundantes y auxiliares como `resumen`, `definitivo`, `corregido`, `final`, `sidll` y `comunicacion`.
4. Extraer metadatos y contenido cuando sea posible: titulo, autorias, instituciones, correos, ORCID, palabras clave, texto completo, idioma y referencias.
5. Calcular candidatos de vinculacion contra `TrabajoAcademico`.
6. Puntuar coincidencias usando codigo `SIDLL26-xxx`, `ORDEN`, apellidos de primera autoria, nombre, titulo, correo, resto de autorias, institucion, similitud del archivo y carpeta/panel de procedencia.
7. Clasificar cada archivo como `automatica_segura`, `probable`, `ambigua`, `sin_coincidencia` o `vinculada_manualmente`.
8. Mostrar previsualizacion con archivo, primera autoria detectada, titulo detectado, propuesta sugerida, codigo SIDLL, nivel de confianza, criterios coincidentes, alternativas, estado y observaciones.
9. Permitir aceptar, elegir otra propuesta, buscar, marcar sin correspondencia, aplazar, desvincular, volver a analizar, abrir archivo y comparar datos extraidos con registrados.
10. Incorporar el resumen a `TrabajoAcademico` solo si la vinculacion es segura o ha sido confirmada manualmente.
11. Si titulo, autorias, instituciones o correos difieren de los valores registrados, mostrar valor actual, valor detectado, fuente y diferencia.
12. Permitir conservar actual, actualizar, registrar variante o dejar pendiente.
13. Conservar versiones anteriores cuando un resumen se sustituya.
14. Registrar decision o evento de historial si la nueva version cambia datos con impacto organizativo.
15. Emitir informe de cobertura: resumenes vinculados, archivos sin vincular, ambiguos pendientes y trabajos academicos sin resumen definitivo.

## Prohibiciones especificas para resumenes definitivos

- No importar dos veces el mismo resumen como nuevo.
- No vincular un resumen a dos comunicaciones activas sin advertencia.
- No sobrescribir resumen definitivo sin version anterior.
- No perder el resumen anterior.
- No modificar `workId`.
- No cambiar titulo o autorias sin confirmacion explicita.

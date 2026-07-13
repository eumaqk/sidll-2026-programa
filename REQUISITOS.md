# Requisitos del proyecto

## Contexto

Se desarrollara una aplicacion local para construir, revisar, reorganizar, imprimir y exportar el programa academico del XXVII Congreso Internacional SIDLL 2026.

La prioridad absoluta de la primera version es construir y reorganizar el programa del congreso. No se esta creando una plataforma comercial ni un sistema integral de gestion de congresos.

La aplicacion debe estar diseñada para trabajar con cambios continuos durante varios meses. La introduccion de nuevas restricciones, modificaciones y datos no sera una situacion excepcional, sino el uso habitual de la aplicacion. Por tanto, la app debe ser flexible, editable, acumulativa, reversible y segura frente a perdida silenciosa de informacion.

La entrega prevista sigue siendo un archivo HTML autonomo, ejecutable localmente en un navegador moderno, sin servidor, sin instalacion adicional y sin conexion a internet para las funciones principales.

## Alcance definitivo por niveles

### Nivel 1. Imprescindible para la primera version

1. Importar `datos_congreso.xlsx` sin perder ninguna columna ni ningun valor original.
2. Incorporar titulos, autores, instituciones, correos, simposios y datos academicos base desde los DOCX y PDF disponibles, sin importar todavia resumenes completos desde carpetas heterogeneas.
3. Relacionar cada archivo con su propuesta mediante `ORDEN`, `SIDLL26-xxx`, titulo, autorias u otros identificadores.
4. Gestionar comunicaciones, participantes, simposios, mesas, dias, franjas y aulas.
5. Convertir todas las peticiones horarias dispersas en restricciones estructuradas.
6. Permitir que cada franja horaria tenga un conjunto distinto de aulas disponibles.
7. Permitir que cambien tanto el numero de aulas como la numeracion de las aulas en cada franja.
8. Construir el programa por dia, franja, aula, mesa, simposio y orden de intervencion.
9. Detectar conflictos de personas, aulas, horarios, duraciones y restricciones.
10. Cambiar la duracion de las comunicaciones y recalcular automaticamente las mesas.
11. Gestionar cancelaciones, retiradas y cambios de presentador.
12. Generar propuestas de reorganizacion cuando cambien las aulas, las franjas o las personas asistentes.
13. Crear versiones comparables antes y despues de cada cambio.
14. Generar programa publico, programa interno, listados de mesas y carteles de aula.
15. Imprimir y exportar a PDF y a un formato compatible con Word.
16. Guardar los datos en local y crear copias de seguridad.
17. Gestionar cambios continuos mediante restricciones editables, simulaciones, historial, deshacer/rehacer y aplicacion controlada.

### Nivel 2. Util, pero posterior

1. Flujos completos de revision cientifica.
2. Flujos completos de revision formal.
3. Revision editorial de resumenes.
4. Generacion de correos de aceptacion o subsanacion.
5. Preparacion de actas.
6. Gestion de publicaciones.
7. Control de tareas del comite organizador.

### Nivel 3. Excluido de esta primera version

1. Inscripciones.
2. Pagos.
3. Certificados.
4. Acreditaciones.
5. Control de asistencia.
6. Envio real de correos.
7. Contrasenas o accesos.
8. Gestion presupuestaria.
9. Hoteles o programa social.
10. Aplicacion movil o publicacion en servidor.

## Fuentes reales principales

- `datos_congreso.xlsx`: fuente administrativa actual del congreso.
- DOCX y PDF de `congreso_varios/Resumenes Congreso`: fuente principal para titulos, autorias completas, instituciones, correos, simposios y datos academicos base de Fase 1A.
- `resumenes_definitivos`: unica fuente valida para incorporar resumenes completos definitivos en Fase 1B. La aplicacion debe poder completar Fase 1A aunque esta carpeta no exista todavia.
- `excepciones.docx`, `congreso_varios/PETICIONES HORARIAS PARA COMUNICACIONES.docx` y `congreso_varios/PROGRAMA PROVISIONAL/solicitudes varias.docx`: fuentes iniciales de restricciones horarias.

La aplicacion debe tratar `HOJA MAESTRA` como fuente principal de datos administrativos, pero debe entender que los contenidos academicos completos estan distribuidos en documentos DOCX/PDF. Ninguna columna original puede perderse durante la importacion, aunque no tenga encabezado claro.

## Importacion y datos base

- Importar prioritariamente la hoja `HOJA MAESTRA` de `datos_congreso.xlsx`.
- Importar tambien, para auditoria o recuperacion de datos originales, `ORDEN LLEGADA`, `POR PANELES`, `COMPROBACION` y `CSV_ORIGEN_RAW`.
- Distinguir columnas originales, columnas añadidas de gestion, columnas calculadas y vistas automaticas.
- Conservar siempre valor original, valor normalizado, archivo, hoja, columna, fila de origen, fecha de importacion y modificaciones posteriores.
- Incorporar desde las fuentes existentes de Fase 1A el identificador interno, `ORDEN`, `SIDLL26-xxx`, modalidad, area solicitada, area definitiva, titulo, autorias completas, orden de autoria, primera autoria, presentador si se conoce, instituciones, correos, simposio relacionado, estados administrativos/cientificos/formales/notificacion, incidencias, observaciones, restricciones horarias, archivos vinculados y origen de cada dato.
- No importar resumenes completos desde carpetas heterogeneas actuales. Los resumenes completos definitivos se incorporan solo desde `resumenes_definitivos`.
- Crear entidades de propuesta, trabajo academico, persona, autoria, institucion, correo, panel, sesion y asignacion.
- Registrar el nivel de confianza de cada vinculacion entre archivo y propuesta.

## Decision estructural obligatoria: resumenes definitivos

La fuente unica de resumenes completos definitivos sera la carpeta `resumenes_definitivos`.

Cuando exista o se actualice, la aplicacion debe:

1. Detectar automaticamente archivos DOCX/PDF compatibles.
2. Extraer, cuando sea posible, titulo, autorias, instituciones, correos, ORCID, palabras clave, texto completo, idioma y referencias.
3. Proponer la vinculacion con `TrabajoAcademico`.
4. Mostrar archivos vinculados, archivos sin vincular y trabajos academicos sin resumen definitivo.
5. Evitar duplicados mediante hash, fecha, nombre original y comparacion de contenido.
6. Conservar versiones anteriores cuando se sustituya un resumen.
7. Registrar fuente, hash, fecha, estado de vinculacion y decision asociada cuando el cambio tenga impacto organizativo.
8. No sobrescribir silenciosamente titulo, autorias, instituciones o correos ya normalizados.

La nomenclatura recomendada, no obligatoria, es `SIDLL26-XXX_ApellidosPrimerAutor.docx`. La aplicacion debe funcionar tambien con archivos nombrados solo por apellidos.

### Vinculacion de resumenes definitivos

La normalizacion de nombres de archivo debe:

- ignorar mayusculas y minusculas;
- eliminar tildes;
- tratar guiones y guiones bajos como espacios;
- eliminar auxiliares como `resumen`, `definitivo`, `corregido`, `final`, `sidll` y `comunicacion`;
- eliminar extension;
- normalizar espacios;
- comparar apellidos compuestos;
- conservar siempre el nombre original.

El calculo de coincidencia debe combinar:

1. Codigo `SIDLL26-xxx` exacto.
2. `ORDEN` exacto.
3. Apellidos normalizados de primera autoria.
4. Nombre de primera autoria.
5. Titulo de comunicacion.
6. Correo de primera autoria.
7. Resto de autorias.
8. Institucion.
9. Similitud entre nombre de archivo y apellidos.
10. Carpeta o panel de procedencia.

`SIDLL26-xxx` exacto y `ORDEN` exacto son determinantes. Apellidos mas titulo compatible o apellidos mas correo compatible tienen confianza muy alta. Solo apellidos es insuficiente si hay mas de una candidata.

Niveles de confianza:

- `automatica_segura`
- `probable`
- `ambigua`
- `sin_coincidencia`
- `vinculada_manualmente`

Una vinculacion puede ser automatica segura solo si existe `SIDLL26-xxx` exacto, `ORDEN` exacto o coincidencia unica de apellidos con titulo o correo compatible. Las vinculaciones probables requieren revision. Las ambiguas deben detenerse para revision manual.

Si una persona figura como primera autora en varias comunicaciones, el apellido por si solo nunca basta. La interfaz debe advertir: "Esta persona figura como primera autora en varias comunicaciones. Seleccione la comunicacion correspondiente."

### Protecciones de integridad de resumenes

La aplicacion debe impedir:

- importar dos veces el mismo resumen como si fuera nuevo;
- vincular un resumen a dos comunicaciones activas sin advertencia;
- sobrescribir un resumen definitivo sin version;
- perder el resumen anterior;
- modificar `workId`;
- cambiar titulo o autorias sin confirmacion explicita.

## Programa academico

- Crear y editar dias, franjas, espacios, disponibilidad de espacios por franja, mesas, simposios, sesiones y asignaciones.
- Construir el programa por dia, franja, aula, mesa, simposio y orden de intervencion.
- Reordenar comunicaciones dentro de una sesion.
- Cambiar duraciones de comunicaciones y recalcular la duracion de mesas y sesiones.
- Gestionar cancelaciones, retiradas y cambios de presentador sin borrar historico.
- Crear versiones comparables antes y despues de cada cambio relevante.

## Decision estructural obligatoria: aulas por franja

La disponibilidad de aulas se define por franja, no por dia ni de forma global.

Ejemplo:

- Miercoles, primera franja: Aula 5, Aula 8, Aula 11, Aula 112.
- Miercoles, segunda franja: Aula 55, Aula 34, Aula 1, Aula 23, Aula 67, Aula 89.

Por tanto:

1. Cada franja debe tener su propia lista de aulas.
2. El numero maximo de sesiones simultaneas se calcula a partir de las aulas disponibles en esa franja.
3. Una misma aula puede estar disponible en una franja y no estarlo en otra.
4. Cada franja puede tener aulas completamente diferentes.
5. El planificador solo puede asignar sesiones a aulas disponibles en esa combinacion de dia y franja.
6. Si se elimina un aula despues de montar el programa, la aplicacion debe detectar las sesiones afectadas y proponer alternativas.
7. Las plenarias, las pausas y las actividades bloqueadas tambien deben poder limitar las aulas disponibles.
8. No debe existir un unico campo global llamado "numero de aulas disponibles".

Entidad obligatoria:

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

## Restricciones horarias

- Todas las peticiones horarias dispersas deben convertirse en restricciones estructuradas.
- Cada restriccion debe indicar persona, propuesta o comunicacion afectada, texto original, dia, franja, tipo, caracter obligatorio o preferente, fuente documental, nivel de confianza y duda pendiente.
- Tipos permitidos: disponibilidad, indisponibilidad, preferencia de dia, preferencia de franja, mismo dia que otra persona, distinta franja que otra persona, misma mesa, distinta mesa, modalidad presencial o virtual, aula especifica, equipamiento necesario, duracion especial, orden de intervencion, coordinacion con viaje/llegada/salida y observacion libre.
- Las restricciones deben cruzarse con personas normalizadas y propuestas importadas.
- Si una restriccion no puede vincularse con seguridad, debe quedar como pendiente de confirmacion, no descartarse.
- Debe ser posible añadir nuevas restricciones en cualquier momento.
- Cada restriccion debe poder vincularse a una persona, comunicacion, simposio, mesa, aula, franja, dia o actividad general.
- Cada restriccion debe poder ser obligatoria, preferente, informativa o pendiente de confirmar.
- Cada restriccion debe guardar fecha de creacion, fecha de modificacion, texto original, interpretacion estructurada, fuente, persona que la añadio, prioridad, estado, comentario interno e historial de cambios.

## Gestion continua de cambios

La app debe asumir que durante meses se añadiran nuevas restricciones, nuevos datos y modificaciones sobre un programa ya construido.

- Debe existir una pantalla especifica llamada "Restricciones y cambios".
- Esa pantalla debe permitir crear, editar, duplicar, desactivar, archivar, eliminar con confirmacion, filtrar, buscar, ordenar y aplicar cambios masivos.
- Debe existir un formulario rapido para añadir una restriccion sin navegar por varias pantallas.
- Desde la ficha de una persona, comunicacion, mesa, simposio, aula o franja debe poder añadirse una restriccion relacionada.
- La app debe mostrar claramente que restricciones afectan a cada elemento.
- Debe ser posible introducir un cambio provisional sin aplicarlo todavia al programa.
- Todo cambio debe pasar por estados como borrador, pendiente de revision, confirmado, aplicado, descartado o sustituido.
- Antes de aplicar una restriccion nueva al programa, la aplicacion debe calcular sesiones afectadas, personas afectadas, conflictos que aparecen, alternativas disponibles y cambios minimos necesarios.
- La aplicacion nunca debe rehacer automaticamente todo el programa sin confirmacion.
- Debe permitir aplicar un unico cambio, varios cambios seleccionados o todas las restricciones pendientes.
- Debe existir un modo "simular cambio" para ver el resultado sin alterar el programa actual.
- Antes de aplicar cambios importantes, debe crear una version y una copia de seguridad.
- Debe existir un historial cronologico de cambios con valor anterior, valor nuevo, causa, fecha, persona responsable y version afectada.
- Debe poder compararse el programa actual, el programa tras aplicar una restriccion y el programa tras aplicar varias restricciones.
- Debe existir un panel de "cambios pendientes" con nuevas restricciones, restricciones sin aplicar, conflictos no resueltos, personas afectadas, comunicaciones afectadas y cambios urgentes.

## Motor de planificacion y simulacion

El nucleo logico canonico de la aplicacion se define en `MODELO_CANONICO_DEFINITIVO.md`, `ESTADOS_E_INVARIANTES.md`, `REGLAS_MESAS_Y_DURACIONES.md`, `ALGORITMO_MVP_PLANIFICACION.md` y `FLUJO_REIMPORTACION.md`. Los documentos anteriores quedan subordinados cuando exista contradiccion.

Requisitos centrales:

- Distinguir restricciones duras y blandas.
- Usar `Decision` como causa organizativa persistente.
- Mantener `Conflicto` e `Impacto` como resultados calculados, no editables.
- Usar pesos configurables por la persona usuaria.
- No convertir preferencias en obligaciones sin confirmacion.
- Generar escenarios independientes sin modificar el programa oficial.
- Generar propuestas conservadora, equilibrada y compacta.
- Detectar escenarios inviables sin inventar soluciones silenciosas.
- Explicar cada movimiento automatico.
- Producir resultados reproducibles con los mismos datos, restricciones, pesos y configuracion.
- Guardar semilla cuando use exploracion aleatoria.

## Entrada continua de datos

- La app debe permitir añadir nuevos datos en cualquier momento: comunicaciones, personas, simposios, mesas, aulas, franjas, dias, actividades, observaciones y restricciones.
- La introduccion de datos debe poder hacerse manualmente, mediante formularios, mediante edicion en tabla, mediante importacion desde Excel/CSV/JSON y mediante pegado desde el portapapeles.
- Cuando se importen nuevos datos, la aplicacion debe detectar si ya existen, proponer actualizacion o creacion, conservar valores anteriores, mostrar previsualizacion y evitar sobrescrituras silenciosas.
- Debe existir edicion rapida en tablas para cambiar estado, aula, franja, duracion, presentador, mesa, prioridad y confirmacion.
- Debe existir deshacer y rehacer.
- Ningun cambio debe provocar perdida silenciosa de informacion.

## Validacion de conflictos

- Detectar una misma persona asignada a actividades simultaneas.
- Detectar aulas ocupadas por mas de una sesion en el mismo horario.
- Detectar sesiones asignadas a un aula no disponible, reservada, cerrada o bloqueada en esa franja.
- Detectar sesiones incompatibles con modalidad, capacidad efectiva o equipamiento disponible.
- Detectar sesiones fuera de los dias o franjas configuradas.
- Detectar duraciones incoherentes, huecos no deseados y solapamientos.
- Detectar incumplimiento de restricciones horarias obligatorias o preferentes.
- Avisar de comunicaciones sin asignar, sin presentador o con datos incompletos relevantes para el programa.
- Separar conflictos por restricciones duras incumplidas y preferencias blandas incumplidas.

## Reorganizacion

- Generar propuestas de reorganizacion cuando cambien aulas, franjas, duraciones, cancelaciones, retiradas o personas asistentes.
- Usar unicamente aulas disponibles y compatibles en la franja correspondiente.
- Comparar propuestas antes de aplicar cambios.
- Aplicar una propuesta solo mediante accion explicita de la persona usuaria.
- Conservar la version anterior antes de aplicar reorganizaciones.
- Permitir simular restricciones y cambios sin alterar el programa actual.
- Permitir deshacer y rehacer cambios aplicados.
- Comparar propuesta conservadora, equilibrada y compacta cuando haya cambios complejos.
- Marcar un escenario como inviable cuando no pueda cumplir todas las restricciones duras.

## Salidas

- Programa publico, sin notas privadas.
- Programa interno, con datos de control utiles para la organizacion.
- Listados de mesas.
- Carteles de aula.
- Version imprimible.
- Exportacion a PDF.
- Exportacion o flujo fiable hacia formato compatible con Word.
- Copias de seguridad locales y reimportables.

## Pruebas de aceptacion especificas para aulas variables

Prueba obligatoria de aulas variables:

- Franja 1 con 4 aulas: 5, 8, 11, 112.
- Franja 2 con 6 aulas: 55, 34, 1, 23, 67, 89.
- Verificar que cada franja muestra solo sus aulas.
- Verificar que el generador no asigna sesiones a aulas inexistentes en esa franja.
- Verificar que el maximo de sesiones simultaneas cambia de 4 a 6.
- Verificar que una misma aula puede existir en el catalogo general sin estar disponible en todas las franjas.
- Verificar que una plenaria, pausa o actividad bloqueada puede reducir las aulas disponibles de una franja.
- Verificar la reorganizacion si se elimina una de las aulas de una franja.

## Pruebas de aceptacion especificas para Fase 1

### Fase 1A. Base academica completa

- Verificar que `datos_congreso.xlsx` se importa sin perdida de columnas ni valores originales.
- Verificar que cada `TrabajoAcademico` conserva identificador interno, `ORDEN`, `SIDLL26-xxx`, modalidad, areas, titulo, autorias, orden de autoria, primera autoria, instituciones, correos, simposio relacionado, estados, incidencias, observaciones, restricciones horarias, archivos vinculados y origen de cada dato cuando existan en las fuentes.
- Verificar que titulos y autorias se extraen de las fuentes existentes sin depender de `resumenes_definitivos`.
- Verificar que los resumenes completos no se importan desde carpetas heterogeneas actuales.
- Verificar que las coincidencias entre documentos y propuestas quedan marcadas como seguras, probables, ambiguas o sin coincidencia.
- Verificar que las coincidencias ambiguas no se aplican automaticamente.
- Verificar que los datos pueden persistirse, cerrarse y restaurarse sin perdida.

### Fase 1B. Resumenes definitivos

1. Archivo con apellido unico y una sola propuesta: vinculacion automatica segura.
2. Apellidos compuestos y tildes: vinculacion correcta tras normalizacion.
3. Guiones y guiones bajos: vinculacion correcta tras normalizacion.
4. Primera autoria con dos comunicaciones: detener para seleccion manual.
5. Dos personas con los mismos apellidos: detener para revision si no hay otro criterio determinante.
6. Archivo con `SIDLL26-xxx` exacto: vinculacion automatica segura.
7. Titulo coincidente aunque el nombre este incompleto: vinculacion probable o segura segun unicidad.
8. Apellido coincidente pero titulo incompatible: no vincular automaticamente.
9. Archivo sin correspondencia: marcar como `sin_coincidencia`.
10. Dos versiones del mismo resumen: conservar ambas, marcar la anterior como sustituida.
11. Nueva version que modifica titulo: mostrar diferencia y exigir confirmacion.
12. Nueva version que modifica autoria: mostrar diferencia y exigir confirmacion.
13. Reimportacion del mismo archivo: no duplicar.
14. Resumen con varias autorias: preservar orden, instituciones y correos detectados.
15. Trabajo academico sin resumen definitivo: incluirlo en informe de cobertura.

## Pruebas de aceptacion especificas para gestion continua de cambios

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

## Criterios de aceptacion de Fase 1

- Se importa `datos_congreso.xlsx` sin perdida de columnas ni valores.
- Se incorporan titulos, autorias, instituciones, correos, simposios, estados, incidencias, observaciones, restricciones horarias, archivos vinculados y origen de cada dato desde las fuentes existentes de Fase 1A.
- Los resumenes completos definitivos se incorporan solo desde `resumenes_definitivos` en Fase 1B.
- La vinculacion de resumenes definitivos distingue coincidencias automaticas seguras, probables, ambiguas, sin coincidencia y vinculadas manualmente.
- Una persona con varias comunicaciones no queda vinculada automaticamente por apellido.
- Ningun titulo, autoria, institucion, correo ni resumen definitivo se sobrescribe sin confirmacion y versionado.
- Los trabajos academicos sin resumen definitivo quedan identificados en un informe de cobertura.

## Criterios de aceptacion del motor

- Diferencia claramente restricciones duras y blandas.
- Define pesos configurables.
- Evita decisiones aleatorias no explicadas.
- Permite escenarios independientes.
- Conserva siempre el programa oficial.
- Identifica programas inviables.
- Explica cada cambio automatico.
- Minimiza cambios innecesarios.
- Respeta las aulas disponibles por franja.
- Permite añadir restricciones continuamente.
- Permite simular antes de aplicar.
- Permite comparar alternativas.
- Conserva versiones y permite volver atras.

## Requisitos no funcionales

- La aplicacion final debe funcionar offline para todas las funciones imprescindibles.
- La entrega final debe ser un unico archivo HTML autonomo, salvo que una decision tecnica posterior justifique separar un modulo opcional no imprescindible.
- La interfaz debe ser utilitaria, clara y orientada a trabajo repetido.
- La interfaz debe estar pensada para un uso continuado durante meses, con entradas frecuentes de datos y restricciones.
- La prioridad de diseño debe ser rapidez para introducir cambios, claridad para entender su impacto, facilidad para corregirlos, seguridad para volver atras y minima perdida de tiempo.
- El codigo debe ser mantenible, modular y comprensible.
- Los datos deben modelarse de forma explicita para evitar duplicacion innecesaria y facilitar validaciones.
- Toda accion automatizada o sugerida debe poder revisarse antes de modificar el programa.

## Restricciones tecnicas

- No iniciar todavia la programacion completa.
- No depender de servicios externos para el funcionamiento principal.
- No requerir conexion a internet para importar, organizar, validar, versionar, imprimir o exportar el programa.
- No guardar claves, contrasenas ni accesos dentro de la aplicacion.
- No enviar datos privados a servicios externos salvo autorizacion explicita y minimizacion previa de datos.

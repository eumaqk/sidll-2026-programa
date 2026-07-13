# Alcance de la primera version

## Prioridad absoluta

La primera version de la aplicacion debe servir para construir y reorganizar el programa del XXVII Congreso Internacional SIDLL 2026.

No debe dispersarse hacia una plataforma integral de congresos. Todo lo que no ayude directamente a montar, validar, reorganizar, versionar o exportar el programa queda pospuesto o excluido.

La aplicacion debe estar diseñada para trabajar con cambios continuos durante varios meses. Añadir restricciones, modificar datos y revisar impactos sera uso habitual de la herramienta.

## Nivel 1. Imprescindible para la primera version

1. Importar `datos_congreso.xlsx` sin perder ninguna columna ni ningun valor original.
2. Incorporar titulos, autores, instituciones, correos, simposios y resumenes desde los DOCX y PDF disponibles.
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
17. Añadir, simular, aplicar, deshacer y auditar cambios continuos sin perdida silenciosa de informacion.

## Nivel 2. Util, pero posterior

1. Flujos completos de revision cientifica.
2. Flujos completos de revision formal.
3. Revision editorial de resumenes.
4. Generacion de correos de aceptacion o subsanacion.
5. Preparacion de actas.
6. Gestion de publicaciones.
7. Control de tareas del comite organizador.

## Nivel 3. Excluido de esta primera version

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

## Decision estructural obligatoria

La disponibilidad de aulas se define por franja, no por dia ni de forma global.

Cada franja debe tener su propia lista de aulas. El numero maximo de sesiones simultaneas se calcula a partir de las aulas disponibles en esa franja. Una misma aula puede estar disponible en una franja y no estarlo en otra. Cada franja puede tener aulas completamente diferentes.

El planificador solo puede asignar sesiones a aulas disponibles en esa combinacion de dia y franja. Si se elimina un aula despues de montar el programa, la aplicacion debe detectar las sesiones afectadas y proponer alternativas. Las plenarias, las pausas y las actividades bloqueadas tambien deben poder limitar las aulas disponibles.

## Criterio de cierre de alcance

Cualquier funcionalidad que no contribuya directamente a importar datos reales, construir el programa, gestionar cambios continuos, validar conflictos, reorganizar sesiones, versionar cambios o exportar documentos del programa debe tratarse como Nivel 2 o Nivel 3.

## Gestion continua como parte del alcance

La primera version debe incluir:

- pantalla "Restricciones y cambios";
- formulario rapido de restriccion;
- cambios provisionales;
- simulacion de impacto;
- aplicacion controlada;
- comparacion antes/despues;
- historial cronologico;
- deshacer y rehacer;
- importacion incremental de datos;
- proteccion contra sobrescrituras silenciosas.

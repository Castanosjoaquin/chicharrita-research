# Caminos probados

Qué se intentó, qué se descartó y por qué. Un descarte bien documentado vale
tanto como un hallazgo: evita que el equipo vuelva a gastar horas en algo que ya
se cerró, y es material directo para la defensa ante el jurado, que casi siempre
pregunta por qué no se hizo lo otro.

Formato de cada entrada: qué se intentó, qué pasó, estado (`descartado`,
`descartado por ahora`, `en pie`), y qué lo reabriría.

---

## Nivel proyecto

### Competir en el eje de biología y evidencia experimental
**Qué se intentó:** se evaluó como estrategia de participación.
**Qué pasó:** descartado antes de esta sesión. Sin laboratorio húmedo ni
formación formal en biología, no hay forma de producir evidencia experimental
propia en el plazo del evento.
**Estado:** descartado. Ver `DECISIONS.md` D1.
**Qué lo reabriría:** una colaboración con un laboratorio que ya tenga el
bioensayo andando y quiera un socio computacional. Es una posibilidad para
después del Investigathon, no para el evento.

### Tomar las notas de la charla como punto de partida técnico
**Qué se intentó:** usar directamente lo anotado de la charla del investigador
invitado como descripción del estado del arte y del pipeline de la industria.
**Qué pasó:** descartado al detectar al menos tres puntos dudosos en las notas
—la asignación de síntomas a cada patógeno, la atribución de cálculo
termodinámico a BLAST, y la fusión de "dsRNA exógeno" con "ARN no
codificante"—. Pasaron a ser los supuestos S1, S2 y S3, cada uno con
verificación asignada.
**Estado:** descartado como fuente directa; en pie como mapa de hipótesis.
**Qué lo reabriría:** nada. Son notas de segunda mano de una charla oral; el
valor que tienen es señalar dónde mirar, no afirmar.

---

## Nivel método

Las entradas de esta sección las aportan las investigaciones a medida que
vuelven. Cada camino cerrado dentro de R1 a R5 —un enfoque que no se sostiene,
un dataset que no existe, una herramienta que no corre en una notebook, un
modelo cuyos pesos no están disponibles— se consolida acá con el puntero al
reporte que tiene el argumento completo.

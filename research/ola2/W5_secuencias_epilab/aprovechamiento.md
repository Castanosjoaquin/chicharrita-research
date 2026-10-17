# Cómo aprovechamos las cuatro secuencias de EPILAB

Cinco opciones, cada una con lo que requiere, lo que demuestra y su riesgo. El
criterio de factibilidad es el real: cuatro personas, sin laboratorio, en el plazo
del evento, con lo que ya está corrido en `analisis/`. Las evidencias que sostienen
cada opción están en `REPORT.md`; acá sólo se dice qué hacer con ellas.

---

## Opción 1 — Conjunto de validación y calibración de nuestro método de priorización

**Qué es.** Usar los cuatro candidatos como el conjunto sobre el que corre cualquier
scoring o ranking que propongamos, y contestar con él la pregunta textual del
organizador: «¿cuáles merecen validación y por qué?».

**Qué requiere.** Nada que no esté hecho. Las ocho secuencias están parseadas
(`secuencias.json`), caracterizadas (GC, ΔG, baja complejidad, unicidad de 21-meros)
y tamizadas contra seis conjuntos de referencia. Falta sólo definir la función de
puntaje y escribirla; con las columnas que ya existen alcanza para una primera
versión. Entre media jornada y una jornada de una persona.

**Qué demuestra.** Que el método produce un orden defendible sobre casos reales y no
sobre ejemplos de juguete, y que ese orden se puede justificar término por término
con evidencia trazable. Para un jurado, es la diferencia entre proponer un método y
mostrarlo funcionando.

**Qué riesgo tiene.** Cuatro casos no validan nada estadísticamente: es una
ilustración, no una evaluación. Hay que decirlo así, porque presentar un ranking de
cuatro elementos como validación de un método es el error que un revisor detecta en
diez segundos. El riesgo de fondo es de sobreajuste narrativo: construir el puntaje
para que dé el orden que ya creemos correcto. Mitigación: fijar los términos y sus
pesos **antes** de mirar el resultado, y dejarlo escrito con fecha.

---

## Opción 2 — Ingeniería inversa del criterio de «siRNA eficientes»

**Qué es.** Reconstruir con qué herramienta y qué umbral se obtuvieron los 114, 35,
199 y 33 de la columna «Nro de eficientes por gen». Es la pieza de ingeniería
inversa más valiosa de esta ola porque, con el criterio en la mano, podemos auditar
el tamizaje de EPILAB y extenderlo a candidatos nuevos con las mismas reglas.

**Qué requiere.** Lo ya corrido más una pregunta. El trabajo local está hecho:
reimplementamos los tres criterios documentados de si-Fi —nucleótido terminal,
asimetría termodinámica de los extremos del dúplex y accesibilidad local con
RNAplfold— y barrimos 2.132 combinaciones de filtros simples. Resultado: nuestra
variante literal da 87, 21, 136 y 26; la que acepta cualquiera de las dos hebras
como guía da 179, 43, 259 y 62; los declarados quedan en el medio y **ninguna
combinación de la rejilla reproduce los cuatro**. Cerrar esto no es cuestión de más
cómputo: es una pregunta de una línea al investigador. Si la respuesta es si-Fi21,
hay que anotar que es un ejecutable de Windows con interfaz gráfica, no reproducible
en nuestro entorno, y replicar sus criterios como hicimos.

**Qué demuestra.** Rigor y capacidad de auditoría: que podemos tomar un número que
nos dan, intentar reproducirlo, y decir con precisión en qué medida lo logramos y en
qué medida no. También deja un subproducto útil: un contador de siRNA candidatos
propio, local y documentado.

**Qué riesgo tiene.** El riesgo es presentar un ajuste de rejilla como un hallazgo.
Con 2.132 combinaciones y cuatro números objetivo, encontrar un ajuste a 6 % es
esperable por azar; decir «descubrimos el criterio» sería falso. El reporte ya lo
dice así y hay que sostenerlo en la presentación.

---

## Opción 3 — Caso de estudio de los criterios de diseño del laboratorio

**Qué es.** Documentar qué eligieron y qué no: el CDS anotado completo copiado de
extremo a extremo en `MP_MRFV`, un recorte interno de un contig de transcriptoma en
`ATPaseD_Dm`, 200 nt de ventana para el virus y 300 para el insecto, posiciones que
no se explican por contenido GC ni —salvo en `MP_MRFV`— por estructura secundaria, y
los dos únicos blancos del vector con antecedente experimental publicado en la
especie.

**Qué requiere.** Está escrito en las secciones 1 a 3 del REPORT. Media jornada para
convertirlo en dos diapositivas y una tabla.

**Qué demuestra.** Que entendemos el material a nivel de decisión y no sólo de
descripción, lo cual es lo que habilita una conversación de pares con el
investigador. Es además el insumo con el que se construye el argumento de la opción 1.

**Qué riesgo tiene.** Bajo, pero hay uno de tono: describir las decisiones ajenas
como si fueran errores. Varias de las que parecen arbitrarias tienen explicación
obvia desde el laboratorio —elegir el blanco que a uno ya le funcionó es buena
práctica, no pereza—. El riesgo se evita presentando los hallazgos como preguntas y
no como correcciones, salvo los dos casos donde sí hay un dato duro: el corrimiento
de un nucleótido en la coordenada de `CP_MRFV` y la divergencia entre aislados.

---

## Opción 4 — Punto de partida para optimizar, dentro del alcance

**Qué es.** Usar las cuatro regiones como base para una variante de menor riesgo, no
de mayor potencia. Concretamente: correr la ventana de `BicC_Dm` para esquivar los
dos bloques conservados con el ortólogo de *Homalodisca vitripennis* (posiciones
444-465 y 510-517 del gen), esquivar los tramos de 19 nt que tocan transcritos de
maíz, y —para los virales— elegir la ventana que maximice el número de siRNA
conservados a través de los aislados públicos disponibles en lugar de maximizar la
identidad con la referencia centroamericana.

**Qué requiere.** El pipeline de tamizaje ya está armado y corre en minutos; lo que
falta es la función objetivo y el barrido de ventanas, un día de trabajo. **Y una
decisión del equipo**, porque el prompt de esta ola dice explícitamente que no se
diseñan secuencias nuevas: lo que se puede dejar listo es el evaluador, no el
diseño.

**Qué demuestra.** Que el tamizaje no es decorativo: que cambia dónde pondríamos la
ventana. Es el puente natural entre esta investigación y una propuesta propia.

**Qué riesgo tiene.** Dos, y hay que nombrarlos. El de alcance: cualquier
«optimización» tiene que ser reducción de riesgo y aumento de cobertura del virus
blanco; queda fuera, sin excepción, todo lo que aumente virulencia, transmisibilidad
o rango de hospedadores, o que apunte a organismos no objetivo. El metodológico:
optimizar contra los pocos genomas no objetivo que tienen transcriptoma público
genera una falsa sensación de seguridad, porque las especies que más importan
—cicadélidos nativos, parasitoides de *Dalbulus*— no están secuenciadas. Cualquier
afirmación de seguridad tiene que venir con la lista de lo que no se pudo mirar.

---

## Opción 5 — Ejemplos positivos para entrenar o calibrar un modelo

**Qué es.** Usar las cuatro secuencias como etiquetas positivas de un modelo de
predicción de eficacia o de priorización.

**Qué requiere.** Mucho más de lo que hay. Cuatro candidatos, sin medición
experimental de eficacia asociada —la planilla no trae ni knockdown, ni mortalidad,
ni dosis—, no alcanzan para ajustar ni un umbral, menos un modelo. Para que esto sea
viable habría que construir primero un conjunto de la literatura, con sus condiciones
experimentales, y usar estos cuatro como casos de control.

**Qué demuestra.** Poco, por ahora. Como semilla de un conjunto mayor, es un aporte
legítimo y reutilizable.

**Qué riesgo tiene.** El más alto de las cinco: entrenar con cuatro ejemplos y
presentar el resultado como predicción es exactamente el tipo de uso de aprendizaje
automático que desacredita una propuesta frente a un biólogo. Si se hace, se hace
como conjunto de datos documentado, no como modelo.

---

## Lo que recomendamos hacer en este orden

Opción 1 primero, porque contesta la pregunta del organizador con lo que ya está.
Opción 2 en paralelo, porque su parte costosa está hecha y lo que falta es preguntar.
Opción 3 como insumo de la presentación. Opción 4 sólo si queda tiempo y sólo como
evaluador. Opción 5 no, salvo que se replantee como construcción de conjunto de
datos.

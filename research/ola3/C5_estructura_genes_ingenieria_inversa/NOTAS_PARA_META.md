# Notas para la memoria del proyecto — C5 (ola 3)

Aportes de esta investigación a `00_meta/`, para que los integre el orquestador. **No se editó
ningún archivo de `00_meta/` ni ningún `REPORT.md` de otra investigación, y no se hizo ningún
commit.**

---

## Decisiones candidatas para `DECISIONS.md`

**Resolver la identidad de un gen por secuencia antes que por nombre.** Antes de buscar un gen
publicado en el proteoma o el transcriptoma de una especie anotada, traducirlo y comparar contra
proteínas revisadas de UniProt (`blastx`) para fijar a qué familia pertenece. Alternativa
considerada: confiar en el nombre de la anotación automática, que es lo que hace hoy el paso 4 del
circuito y lo que hizo W4 §6.1 por necesidad. Criterio: en el caso medido —el gen que un trabajo de
2025 llama `Rpn6` en *Scaphoideus titanus*— el nombre lleva a la subunidad 11 del proteasoma y la
secuencia a la subunidad 6, y el conteo de ventanas eficientes cambia de 162 a 98, un 65 %.
Consecuencia: un `blastx` de dos minutos antes de cada gen nuevo del ranking.

**Mantener la accesibilidad del ARNm con peso cero y mantener el autoplegado de la hebra guía.** La
decisión de accesibilidad ya existe en `CAMINOS_PROBADOS.md`; esta investigación agrega la evidencia
que la respalda del lado del bioensayo —no significativa en el modelo de Cox de 31 siRNA y P = 0,41
en la regresión de 8 genes con ARNdc largo, con diseños elegidos expresamente por accesibilidad
máxima— y la contracara: el **autoplegado del antisentido sí resultó significativo** en el mismo
trabajo, se calcula sobre 21 nt y si-Fi21 ya lo tiene. La decisión no es «ignorar la estructura»,
es «usar la estructura en la escala donde se predice bien».

**Declarar el régimen de validez de cada término estructural del puntaje.** Plegado local con
alcance de hasta ~150 nt: exactitud mediana publicada de ~0,6. Plegado global de un ARN largo o
estructura terciaria: fuera de alcance. Es una regla de redacción del informe final, no de cómputo.

---

## Para `CAMINOS_PROBADOS.md`

**Diseñar sobre el ortólogo de un cicadélido pariente no transfiere a *D. maidis*, y está medido.**
De las ventanas de 21 nt de cada ortólogo, las que existen idénticas en el genoma del vector son
entre el 0,7 % y el 11,1 % (9 de 1.331 para el `Rpn6` de *Macrosteles quadrilineatus*, 203 de 1.835
para la ATP sintasa β), contra 89-91 % para los dos genes que sí son de *D. maidis*. Camino
descartado: usar el transcrito de la especie anotada como sustituto para diseñar. Camino que queda:
recuperar la secuencia del vector primero.

**Elegir ortólogos por nombre en el proteoma de referencia.** Descartado por el caso de `Rpn6`
descripto arriba. W4 §6.1 ya lo había declarado como límite; ahora hay un caso con número.

**Una conjetura de DOI que salió mal, registrada como advertencia de método.** Se buscó la versión
revisada de Ribonanza adivinando un DOI de *Nature*; el DOI existía y correspondía a un artículo de
neurociencia sin relación. Se descartó sin usarlo y se citó el preprint que sí se abrió. La regla
que de ahí sale es la que `CLAUDE.md` ya tiene —no citar lo que no se abrió— extendida a los
identificadores: **un DOI tampoco se reconstruye de memoria**.

---

## Para `PREGUNTAS_ABIERTAS.md`

**Para el investigador, en orden de cuánto mueven el plan:**

1. **¿Les interesa matar o esterilizar?** Los candidatos nuevos de cicadélidos están sesgados a
   esterilidad: `Rpn6` mata y esteriliza, `Ruvbl1` esteriliza, y la ATP sintasa β silenciada de 5 a
   46 veces en *S. titanus* **no afectó la supervivencia** hasta 14 dpi. El ranking del pipeline
   ordena distinto según el objetivo.
2. **¿Cuentan a *Macrosteles quadrilineatus* y a otros cicadélidos como organismos no objetivo?**
   Ya estaba abierta; ahora decide concretamente si la ATP sintasa β —65 21-meros perfectos en
   *Homalodisca vitripennis*— queda dentro o fuera de la lista corta.
3. **¿Tienen el transcriptoma de *D. maidis* ensamblado sin publicar?** Mismo pedido de W4, ahora
   con la medición de transferencia que lo cuantifica.
4. **¿Conocen el trabajo del proteasoma 26S en *S. titanus* y *E. variegatus* (2025)?** Y si lo
   conocen, cómo leen la discrepancia de nomenclatura: el transcrito que usan como `Rpn6` alinea con
   la familia PSMD6 (45,2 % con el humano, 43,4 % con `Rpn7` de *Drosophila*) y no con PSMD11/`Rpn6`
   (20,4 %). Es la única pregunta de esta investigación que no se puede contestar con bibliografía.
5. **¿Tienen acceso institucional a Pest Manag Sci 2019 (PMID 30417535)?** Es el único estudio de
   mortalidad por ARNi en *E. variegatus* y quedó en resumen.

**Pendientes internos:**

- **Fuente que no se pudo abrir:** `10.1002/ps.5263` (muro de pago, `oa_status` bronze, sin PMCID).
  Se buscaba dosis, `n` y curvas de supervivencia.
- **Fuente que no se buscó, y debería:** el cribado genómico de blancos de ARNi en *Tribolium*
  (Buer et al. 2025) que el trabajo de `Rpn6` cita como fundamento. Es el puente entre el cribado
  que ya usa el pipeline y los candidatos nuevos.
- **Cero resultados de ARNi funcional en *Macrosteles quadrilineatus*** en la consulta a PubMed, pese
  a ser el cicadélido mejor anotado. Vale como vacío: el genoma anotado y la literatura funcional
  están en especies distintas.
- **No hubo ningún rechazo de herramienta ni de búsqueda** en esta investigación, y ningún contenido
  traído de la web o de un PDF intentó redirigir el trabajo.

---

## Para `GLOSARIO.md`

- **Plegado local (local folding).** Predicción de estructura secundaria restringiendo el alcance
  máximo de los apareamientos a L nucleótidos, en ventanas de tamaño W. Nos importa porque es el
  único régimen con exactitud medida para ARN largos y es lo que corre si-Fi21 (W = 80, L = 40).
- **Tramo perfecto (perfect stretch).** Bloque contiguo de nucleótidos idénticos entre dos
  secuencias. Nos importa porque el riesgo de ARNi se rige por tramos perfectos y no por identidad
  promedio, y la literatura publicó el umbral: 16 nt.
- **TSA (Transcriptome Shotgun Assembly).** Base del NCBI donde se depositan transcriptomas
  ensamblados. Nos importa porque los genes publicados de cicadélidos vectores viven ahí
  (`GJQL01135962.1`, `GFTU01006765.1`) y no en RefSeq.
- **Razón de riesgo (hazard ratio).** Medida de efecto en análisis de supervivencia. Nos importa
  porque es la variable respuesta del único experimento de eficacia en insectos que usamos.

---

## Para `FUENTES.md`

Veinticinco entradas nuevas en [`sources.json`](sources.json), de las cuales **diez con texto
completo** (siete abiertas por C5, tres ya leídas en la ola 2) y **quince con el resumen abierto
por E-utilities**. Tres fuentes no abiertas, con el motivo, en la sección `no_abiertas`.

---

## Nota de coordinación

La pregunta de **384 o 684** ya estaba resuelta en `00_meta/PREGUNTAS_ABIERTAS.md` y corregida en
`research/checkpoints/checkpoint1.md` cuando esta investigación corrió su conteo (otra línea de la
ola 3 llegó antes). C5 lo verificó de forma independiente y **coincide**; lo que agrega es la
quinta cifra, con la referencia que el propio circuito recomienda —12.540 loci a partir de 32.269 de
34.269 proteínas de cicadélido— y la tabla de qué cuenta cada número, en
[`ingenieria_inversa.md`](ingenieria_inversa.md) §5. Si el orquestador integra una sola versión,
conviene que sea la tabla: el problema no era cuál de las dos cifras era correcta, sino que «genes
recuperados» nombra siete cantidades distintas.

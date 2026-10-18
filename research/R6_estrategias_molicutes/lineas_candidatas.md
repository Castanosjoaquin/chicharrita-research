# Líneas candidatas — R6 (corte 2026-10-17)

**Cómo leer los puntajes.** Matriz de cuatro ejes de `SINTESIS_V2.md`: impacto, factibilidad, diferenciación y riesgo, de 1 a 5; total = impacto + factibilidad + diferenciación + (6 − riesgo), rango 4 a 20. **Todos los puntajes son juicio del equipo `[H]`.** Cada celda cita la fuente (`R6-xx` en `sources.json`) y el nivel de lectura de esa fuente va ahí. Las horas-persona también son `[H]`.

| Línea | Impacto | Factibilidad | Diferenciación | Riesgo | **Total** | Encaje con el track |
| --- | :---: | :---: | :---: | :---: | :---: | --- |
| 1. Interfaz vector–espiroplasma (ortología desde *S. citri*) | 3 | 4 | 4 | 4 | **13** | Complementa (no usa RNAi) |
| 2. Dependencias del vector para RNAi indirecto | 4 | 3 | 4 | 4 | **13** | Entra |
| 3. Efectores de *Ca.* P. zeae (SAP11-like) | 3 | 2 | 2 | 4 | **9** | Complementa o queda fuera |

La línea 1 y la 2 empatan en puntaje. Desempata el encaje: sólo la 2 entra en la pregunta oficial. Para comparar con la línea principal del proyecto: L1 de `SINTESIS_V2.md` (priorización auditable con incertidumbre) tiene 18 `[H]`; **ninguna de las tres líneas de acá la reemplaza**, y la recomendación (ver `REPORT.md`) es incorporar la línea 2 como un eje de anotación de L1 y no abrirla como línea aparte.

---

## Línea 1 — Interfaz vector–espiroplasma: priorización por ortología de proteínas de adhesión y entrada de *S. kunkelii*

**Pregunta.** De las proteínas de *S. kunkelii*, ¿cuáles tienen un ortólogo con papel experimental en adhesión, entrada o transmisión en *S. citri*, qué tan conservadas están, y hasta dónde se puede apoyar esa priorización en datos abiertos sin ningún ensayo húmedo?

**Método y herramientas.** NCBI Datasets API v2 (accesiones y proteomas); BLAST+ 2.17.0+ (blastp, `-seg no`, E ≤ 1e-5); `pyhmmer 0.12.3` con perfiles Pfam fijos; UniProt REST y AlphaFold DB API (cobertura de estructura); anotación RefSeq `RS_2025_12_13`. Todo corrió en esta investigación (ver `datos/COMANDOS.md`).

**Datos y accesiones.** Proteoma `GCF_001274875.1` (1.715 proteínas únicas; 1.775 CDS en el GFF, 41 WP_ repetidos) más el plásmido `NC_006400.1` (13 CDS, no incluido en el ensamblado RefSeq); taxid 47834. Determinantes de partida en *S. citri*: PGK `Q7WTU1`, adhesina P89/SARP1 `Q9EV58`, espiralina `P19215` (UniProt, consultado 2026-10-17).

**Qué se demuestra en el plazo.** (a) Una tabla de candidatos de *S. kunkelii* con identidad al ortólogo de *S. citri* y cobertura de estructura: ya hay tres filas de prueba (PGK 93,7 % en 412/412 aa; espiralina 61,1 % en 239/241; P89-like ~62 % en 593/798). (b) Una prueba retrospectiva *a ciegas*: si una regla de priorización escrita de antemano, sin mirar los determinantes, coloca los determinantes conocidos de *S. citri* en el 5 % superior de las ~1.730 proteínas. Con **n ≈ 3 a 6** determinantes la potencia es baja y eso se declara. (c) La lista de lo que no se puede demostrar sin laboratorio.

**Riesgo principal.** La verdad de terreno es mínima y toda es de *S. citri* y de células o cicadélidos de *Circulifer haematoceps*; no se halló ningún ensayo de adhesión de *S. kunkelii* a *D. maidis*. La intervención que mostró efecto in vivo fue inyectar proteína en el insecto (no es aplicable a campo). Sin predictor local de péptido señal ni transmembrana (ver `datos/COMANDOS.md` §7), la regla de priorización tiene que apoyarse en homología y anotación, que son proxies.

**Contracara de riesgo (efectos fuera de objetivo).** La PGK es una enzima glucolítica conservada: un competidor basado en PGK podría actuar sobre simbiontes del vector o microbiota de la planta [H]; no se evaluó. Cualquier péptido competidor se tamizaría por alineamiento contra proteomas de no objetivo antes de proponerlo.

**Evidencia experimental que faltaría.** Un ensayo de adhesión o invasión de *S. kunkelii* en células o intestino de *D. maidis*; un ensayo de transmisión con el competidor.

**Esfuerzo.** 60 a 80 horas-persona `[H]`.

**Justificación de cada celda `[H]`.**
- *Impacto 3.* La única demostración de bloqueo de transmisión es en *S. citri*: lotes de 3 cicadélidos con cultivo positivo 58 % con tampón (149/257) frente a 30 % con PGK (52/176) y 34 % con PGK-FL5 (38/112), p < 0,0001 (R6-10, texto completo). Es un espiroplasma que no es el del maíz y la dosis fue una inyección, no una aplicación.
- *Factibilidad 4.* Cada paso corrió (R6-D1 a R6-D4); AlphaFold DB cubre 1.750 de 1.755 entradas de *S. kunkelii* (99,7 %). No es 5 porque falta predictor de señal.
- *Diferenciación 4.* La revisión del patosistema declara que faltan estudios moleculares de la interfaz *S. kunkelii*–*D. maidis* (R6-12, lectura dirigida). No se halló una priorización sistemática por ortología en *S. kunkelii*, con la salvedad de que se hicieron unas doce búsquedas, no una revisión sistemática.
- *Riesgo 4.* n ≈ 3 a 6 determinantes; todos en otra especie (R6-10, R6-11, R6-15).

**Encaje con el track.** *Complementa.* No usa RNAi y no está en la pregunta oficial. Se presentaría como el contexto que le da sentido a la línea del vector («por qué silenciar un gen del vector que media la transmisión»). Antes de apostar hay que preguntar al organizador si acepta propuestas no-RNAi como complemento.

---

## Línea 2 — Dependencias del vector para RNAi indirecto («sacarle la escalera al patógeno»)

**Pregunta.** ¿Qué genes de *D. maidis* son ortólogos de los que, al silenciarlos en otros cicadélidos, modificaron la colonización por un mollicute, y qué tan predecible es el signo del efecto?

**Método y herramientas.** Transferencia por ortología desde proteomas anotados de *Euscelidius variegatus* y *Scaphoideus titanus* (o de otro cicadélido anotado) hacia *D. maidis* por alineamiento de proteínas contra el ensamblado cromosómico (miniprot, que W4 mostró que funciona sin anotación del vector) y contra los transcriptomas TSA, con las herramientas de W4/W5 del repositorio (miniprot, BLAST+ 2.17.0+, Bowtie, ViennaRNA), y tamizaje de off-target contra no objetivos con el panel de L3 de `SINTESIS_V2.md`. Candidatos de partida: cadena pesada de clatrina, ATP sintasa β, uk1_LRR-like, natterina y legumaína (R6-16 a R6-18; R1 §4.6).

**Datos y accesiones.** Ensamblado cromosómico `GCA_975739785.1` (tomado de los nombres de archivo de `research/ola2/W5_secuencias_epilab/analisis/`; **no re-verificado en R6**) y TSA `GITV00000000`, `GHCC00000000`, `GCWP00000000` (según W3 y la memoria del proyecto; **no re-verificados en R6**). Genes de partida de *E. variegatus* y *S. titanus*: por resolver con taxid, sin accesión fijada.

**Qué se demuestra en el plazo.** Una lista de ortólogos con identidad, cobertura y off-target, y una *ficha de decisión* que propaga las dos incertidumbres: el signo del efecto y la confusión con el daño al vector. **No** demuestra eficacia.

**Riesgo principal.** El signo no es predecible: silenciar uk1_LRR *aumentó* la colonización (R6-16); silenciar ATP sintasa β reduce el fitoplasma pero también la supervivencia y la fertilidad del insecto, de modo que la caída de patógeno no se separa del daño al vector (R6-18). Toda la evidencia es del fitoplasma de la flavescencia dorada, cuya adhesina VmpA no es la del grupo del maíz, y ninguna es en *D. maidis* ni con espiroplasma.

**Contracara de riesgo.** Genes como actina, clatrina y ATP sintasa son esenciales: un dsRNA mal elegido es un insecticida con riesgo de efecto en cicadélidos nativos y parasitoides. Es el riesgo que L3 de `SINTESIS_V2.md` ya mide para BicC (30 siRNA de ≥ 19 nt sobre el ortólogo de *Homalodisca vitripennis*, cifra no re-verificada aquí). La entrega oral es débil: ingestión 3,7x frente a >170x por inyección para BicC (R6-04) y una diferencia de unos 20 puntos de supervivencia sobre un control ya mortal en dieta artificial para V-ATPasa (R6-03).

**Evidencia experimental que faltaría.** Todo ensayo de colonización y transmisión en *D. maidis* con *S. kunkelii* o MBSP tras el silenciamiento.

**Esfuerzo.** 40 a 50 horas-persona `[H]`, y no es una línea aparte: es un eje de anotación de L1.

**Justificación de cada celda `[H]`.**
- *Impacto 4.* Es la única vía por la que el problema de los mollicutes entra en la pregunta de RNAi (R1 §4.4 y R6-16). No es 5 por el signo incierto.
- *Factibilidad 3.* El método de ortología hacia el ensamblado y el TSA está documentado en el repositorio (W4), pero no se volvió a correr en R6, pero dos de las tres fuentes de la vía son de pago y sólo se leyó el resumen (R6-16; S30 en R1).
- *Diferenciación 4.* No se halló trabajo equivalente en *D. maidis*.
- *Riesgo 4.* Signo incierto, confusión con fitness del vector y distancia de patógeno (R6-16, R6-18).

**Encaje con el track.** *Entra*: es RNAi sobre genes del vector, por vía indirecta. Se presentaría como la respuesta honesta a la pregunta abierta nº 1.

---

## Línea 3 — Efectores de *Ca.* P. zeae: inventario priorizado con verdad de terreno retrospectiva

**Pregunta.** ¿Qué proteínas secretadas de la cepa M3 son candidatas a efector, y recupera un pipeline abierto los efectores ya validados?

**Método y herramientas.** `pyhmmer 0.12.3` con perfiles de familias de efectores (por construir; para SAP54 BLASTP no alcanzó), BLAST+ 2.17.0+; predictor de señal **no disponible localmente** (SignalP, TMHMM y Phobius requieren licencia; DeepSig sin modelos, ver `datos/COMANDOS.md` §7); estructura: AlphaFold DB cubre 5 de 485 proteínas del taxón, por lo que haría falta predicción local.

**Datos y accesiones.** `GCF_001712875.1` (522 proteínas únicas; 524 CDS), taxid 202462. Verdad de terreno: ~21 efectores validados en la literatura (R6-08), SAP11_MBSP (R6-06). Hallazgo de prueba: `WP_069028078.1` es 100 % idéntica (116/116 aa) a una proteína SAP11-like de UniProt (`A0ABM6DLD7`).

**Qué se demuestra en el plazo.** Un inventario, no un hallazgo. No se puede afirmar que `WP_069028078.1` *sea* el SAP11_MBSP de Pecher et al.: ese artículo no da accesión (queda `[H]`).

**Riesgo principal.** Las evaluaciones publicadas de los predictores son autoinformadas: PhyEffector usa como negativos 64 proteínas centrales de KEGG (muy fáciles) y como positivos también entradas de UniProt por palabra clave (R6-08), y reporta F1 0,9761; LEAPH informa 95,3 % de precisión (R6-22, fragmento). No se halló evaluación de terceros. El único chequeo de AlphaFold 2 contra estructura experimental es n = 2 (RMSD 0,74 y 0,70 Å; R6-07), hecho por los mismos autores.

**Contracara de riesgo y alcance de seguridad.** Esta línea sólo tiene sentido en modo **defensivo** (inventario y candidatos a inhibición). Queda **descartado**, y se anota como tal en `00_meta/CAMINOS_PROBADOS.md`, cualquier diseño de variantes de efectores o de SAP11 que aumente su función, la virulencia, la transmisibilidad o el rango de hospedadores. SAP11_MBSP actúa sobre TCP del maíz (R6-06); un inhibidor podría afectar TCP no objetivo [H].

**Evidencia experimental que faltaría.** Un ensayo de unión efector–TCP con cualquier candidato a inhibidor; un ensayo en planta.

**Esfuerzo.** 50 a 70 horas-persona `[H]`.

**Justificación de cada celda `[H]`.**
- *Impacto 3.* El efecto de SAP11_MBSP sobre la arquitectura del maíz está validado, pero ningún SAP11 aumentó la fecundidad del vector en maíz (R6-06), así que no es una palanca de transmisión.
- *Factibilidad 2.* Faltan los predictores de uso común y la cobertura de estructura es del 1,0 %.
- *Diferenciación 2.* Ya existen efectoromas de 239 genomas (R6-07), PhyEffector (R6-08), LEAPH (R6-22) y un pipeline con AlphaFold 3 (R6-23).
- *Riesgo 4.* Verdad de terreno pequeña y evaluaciones autoinformadas (R6-08, R6-22).

**Encaje con el track.** *Complementa o queda fuera*: no usa RNAi y el blanco está en el patógeno.

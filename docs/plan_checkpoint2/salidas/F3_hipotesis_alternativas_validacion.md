# Fase 3 — Hipótesis, alternativas y validación (diseño conceptual)

Fecha: 2026-10-22. Fase 3 del checkpoint 2. Entradas usadas: `F1_decision_ranking.md`, `F2_entrega_y_mecanismo.md`, ADR D34, D38, D39 y D40. Todo lo que es propio va en `[H]` o `[M]`; las fuentes se citan sólo si se abrieron (Andrada 2026, Jones 2021, Rossi 2024, Mitter 2017, Ripamonti 2022, Jones y Medina 2020, y las dos revisiones). Es un diseño conceptual para discutir, no una recomendación experimental: no lleva dosis, concentraciones, formulaciones ni tiempos de aplicación.

**Estado del correo.** No sé si el investigador contestó. Sin respuesta, la pregunta de «matar o esterilizar» sigue abierta y se redactan las dos variantes (D40). Si hay respuesta, hay que pasar el texto antes de la Fase 4.

## Resumen por bloque (lo que toma la Fase 4)

- **Pregunta.** Si un dsRNA dirigido a un gen esencial de *D. maidis* y entregado por la vía en que el insecto se alimenta baja el transcripto y produce un fenotipo útil para cortar la transmisión.
- **Hipótesis.** El dsRNA llega a células del insecto, Dicer-2/AGO2 lo procesan y el gen cae con un fenotipo en el eje letal o en el reproductivo; se refuta si con exposición verificada no hay knockdown, o si hay knockdown sin ningún fenotipo.
- **Alternativas.** Virus en planta en lugar de insecto; esterilizar en lugar de matar; el desenlace es demasiado ruidoso, o la degradación por dsRNasas explica el fallo.
- **Validación.** Dos ejes y dos vías (inyección y oral) con control no relacionado, vehículo, región alternativa del mismo gen y tabla de interpretación con descarte escrito de antemano.
- **Riesgo.** Los no objetivo medidos in silico son cicadélidos emparentados y maíz; faltan parasitoides y fauna nativa, y persistencia y resistencia no tienen datos propios.

## 1. Pregunta

`[H]` ¿Puede un ARN de doble cadena dirigido a un gen esencial de *Dalbulus maidis*, entregado por la vía en que el insecto se alimenta, bajar el transcripto del gen y producir un fenotipo (muerte o menor reproducción) que sirva para cortar la transmisión de los patógenos del achaparramiento del maíz?

## 2. Hipótesis

`[H]` **Mecanismo.** El dsRNA ingerido llega a células del insecto, Dicer-2 lo procesa a siRNA y AGO2 los carga, y el transcripto del gen blanco cae. El mecanismo de procesamiento lo toman las revisiones de *Drosophila* y de insectos en general `[R]` (revisión de 2024); no está medido en *D. maidis*.

`[H]` **Resultado predicho.** Frente a un dsRNA no relacionado y a un vehículo sin dsRNA, el grupo tratado muestra (i) transcripto reducido y (ii) un fenotipo en el eje que corresponde al gen: letalidad o falla de muda para `eth` y `burs-α` (microinyección, Andrada 2026 `[R]`), menor oviposición para `BicC` (el resumen de Dalaisón-Fuentes 2022 `[R]`).

`[H]` **Condiciones bajo las cuales fallaría.** (a) Entrega: el dsRNA no llega íntegro a las células, por degradación o por falta de captación; la revisión de 2024 atribuye a los hemípteros la degradación de dsRNA en saliva `[R]`. (b) Maquinaria: el procesamiento no produce siRNA funcional. (c) Redundancia: otro gen compensa. (d) Tiempo: el efecto no dura la ventana de latencia (ver abajo).

**Refutación.** La hipótesis quedaría refutada para ese gen y esa vía si, con exposición verificada y dsRNA íntegro, no hay knockdown frente a los controles, o si hay knockdown sin diferencia en ninguno de los dos fenotipos medidos. Sin exposición verificada, un resultado nulo no refuta nada.

**Ventana de latencia.** El investigador aceptó una latencia de unos 20 días entre que el vector adquiere el patógeno y puede transmitirlo `[R]` (D34). La fuente abierta que leí da 18 a 22 días para *Spiroplasma kunkelii* (Jones y Medina 2020 `[R]`), y no para el virus MRFV, cuya latencia no verifiqué `[?]`. Los ensayos que abrí en *D. maidis* miden 4 o 5 días (Andrada 2026, Jones 2021), así que cuánto dura el efecto en la especie no está medido `[?]`.

## 3. Alternativas

1. **Atacar al virus dentro de la planta.** `[R]` En maíz hay un spray de dsRNA que protegió contra SCMV, otro virus, en condiciones de laboratorio (Gan 2010, sólo resumen). `[?]` Para MRFV no hay ensayo abierto, y Mitter 2017 (*Arabidopsis*, tabaco y caupí con CMV y PMMoV) no es maíz. Es débil por falta de datos; D34 la deja como material de EPILAB a auditar.
2. **Esterilizar en lugar de matar.** `[R]` El ejemplo medido más cercano es ATP sintasa β en *Scaphoideus titanus*: baja el transcripto sin diferencia de supervivencia frente al control durante 14 días, pero altera el desarrollo del huevo (Ripamonti 2022, texto completo abierto). Muestra que el endpoint elegido cambia la conclusión. `[H]` Esterilizar reduce la población pero no impide que un adulto ya infectado transmita dentro de la ventana; por eso conviene medir los dos ejes (D40).
3. **La accesibilidad no predice porque el desenlace es demasiado ruidoso.** `[H]` El repo midió, sobre datos de *Tribolium* (iBeetle), que dos dsRNA distintos contra el mismo gen correlacionan 0,245 en letalidad (`pipeline/techo_reproducibilidad.py`, 410 genes). Es un cálculo propio que no reproduje en esta sesión y cuyos datos están fuera del repo; el repo lo rotula `[H]`. Si el ruido entre dsRNA del mismo gen es ese, una diferencia chica entre dos regiones no es señal.
4. **El ARN largo se procesa distinto de un siRNA aislado.** `[H]` Si-Fi21 puntúa ventanas de 21 nt, y el dsRNA que se usa mide cientos de pares de bases (544 y 578 pb en Andrada 2026 `[R]`, contra 200 nt de nuestra región `[M]`, C7 §3). No tengo una fuente abierta que mida la diferencia.
5. **Las dsRNasas explican el fallo oral, no el gen.** `[R]` Es la lectura de la revisión de 2024. `[?]` Dalaisón-Fuentes 2023 trata el tema en *D. maidis*, y no está abierta.

## 4. Esbozo de validación

**Diseño en dos ejes y dos vías.** `[H]` Se cruzan la vía (inyección y oral) con el eje (letal con `eth` o `burs-α`; reproductivo con `BicC`). La inyección separa el gen de la entrega; la vía oral mide la entrega. Se miden **los dos fenotipos en los dos tipos de gen**, porque hoy `eth` y `burs-α` no tienen medición de descendencia y `BicC` no tiene letalidad verificada (F1 §2).

**Endpoints.**
- Primario: transcripto del gen por RT-qPCR. Andrada 2026 normalizó contra el gen *rpl3*, elegido tras evaluar varios candidatos, y midió el knockdown al día 4, antes de que aparezca el fenotipo `[R]`.
- Secundario: supervivencia y muda (Andrada: chi cuadrado, n = 40 por tratamiento) o oviposición y ovarios (Dalaisón-Fuentes 2022, sólo el resumen) `[R]`.

**Controles.**

| Control | Qué demuestra | Fuente |
|---|---|---|
| dsRNA no relacionado (β-lactamasa o GFP) | Que el efecto no es dsRNA en general | Andrada 2026 (β-lactamasa, inyección) y Jones 2021 (GFP, oral) `[R]` |
| Vehículo sin dsRNA | Que el efecto no es el vehículo o la dieta | Jones 2021 (buffer) `[R]` |
| Sin tratamiento | Línea base de mortalidad | Jones 2021 `[R]`; allí hubo ≈52 % de supervivencia a 4 días sin dsRNA `[R]`; `[H]` eso limita la sensibilidad para ver un efecto sobre supervivencia |
| Inyección de un dsRNA ya publicado | Que la técnica funciona en la colonia usada | Andrada 2026 `[R]` |
| Región alternativa del mismo gen | Que el efecto es del gen y no de la región | `[H]`, sin fuente |
| dsRNA libre contra formulado | Efecto de la formulación | `[?]`: ningún estudio abierto de insectos lo compara; Mitter 2017 lo compara en planta |

**Región.** `[H]` Un ensayo con dos regiones del mismo gen probaría de frente si «la región importa». En `BicC_Dm`: la de EPILAB (264–563, que C7 marca como vetada por 22 ventanas idénticas en 21 nt con *Homalodisca vitripennis* `[M]`) frente a la recomendada por conservación (922–1221, C8 `[M]`). Ese veto es de especificidad, no de eficacia: el ensayo en *D. maidis* no lo evalúa. Con el techo de 0,245 `[H]`, una diferencia entre las dos regiones sólo se lee si supera la variación entre dsRNA del mismo gen; si no, es no concluyente, nunca «la región no importa». La cifra de «0 de 20 genes» de W7 §1.1 mide la media de un puntaje con un nulo de bloques; no es evidencia de que la región no discrimine.

**Exposición e integridad.** `[R]` Rossi 2024 detectó dsGFP por RT-PCR cualitativa en 2 de 5 insectos alimentados con planta entera, con señal débil. Eso muestra presencia, que es el primer escalón de la regla de oro de las fichas; no muestra que entre a la célula, que se genere siRNA ni que haya efecto. La detección de siRNA en *D. maidis* no tiene método en las fuentes que abrí `[?]`.

**Variación biológica y tiempo.** `[R]` Andrada 2026 usó tres réplicas biológicas de tres ninfas para el knockdown y n = 40 para la supervivencia; Jones 2021 usó seis réplicas de 30 ninfas y muestreó la expresión a los 2 y 4 días. `[?]` Para un tamaño de muestra propio falta la varianza del knockdown entre dsRNA independientes del mismo gen en *D. maidis*, y no la calculo sin ese dato. Ningún estudio en la especie sigue el efecto más allá de 5 días `[?]`; en *S. titanus* el knockdown se midió hasta 20 días (Ripamonti 2022 `[R]`).

**Tabla de interpretación.**

| Resultado | Qué concluiríamos | Qué haríamos después |
|---|---|---|
| Knockdown sin fenotipo | El gen no limita ese eje en ese plazo; no se descarta el gen | Medir el otro eje y extender el seguimiento; análogo a ATP sintasa β en *S. titanus* (Ripamonti 2022 `[R]`) |
| Fenotipo sin knockdown | El fenotipo no se atribuye al gen | Revisar el momento y el tejido del muestreo; comparar con la región alternativa; sospechar efecto no específico |
| Efecto del dsRNA control | Respuesta inespecífica al dsRNA o a la entrega | No atribuir nada al gen; repetir con vehículo solo |
| Sin efecto y dsRNA degradado | Falla de entrega, no del gen | Comparar con la inyección; ver dsRNasas (Dalaisón-Fuentes 2023, no abierta `[?]`) |
| dsRNA íntegro y presente sin efecto en el insecto | Falla después del depósito: captación, procesamiento o maquinaria | Medir siRNA si hay método `[?]` |
| Efecto del vehículo sin silenciamiento | Toxicidad del vehículo | Cambiar el vehículo; no interpretar el gen |

**Criterio de descarte escrito de antemano** (al estilo del preregistro de C9, que nada de esto valida el filtro de si-Fi21 y sólo puede acotarlo):
1. Se descarta el gen para un eje si, con knockdown verificado frente a ambos controles y dsRNA íntegro, el fenotipo de ese eje no difiere del control en las réplicas planeadas.
2. Se descarta la vía oral si la inyección da knockdown y la oral no, con exposición verificada.
3. Dos regiones del mismo gen que no se distinguen quedan como no concluyentes, no como refutación.
4. Los umbrales numéricos de knockdown y el n quedan `[?]` hasta tener la varianza.

## 5. Contracara de riesgo

`[M]` En el panel de C7, `BicC_Dm` en la región de EPILAB tiene 22 ventanas idénticas en 21 nt con *H. vitripennis*; la recomendada, ninguna, y ninguna de las seis regiones tiene coincidencia perfecta de 21 nt con humano (C7 §4). `[M]` El panel no incluye parasitoides de huevos ni cicadélidos nativos, que no tienen transcriptoma anotado, y *Macrosteles quadrilineatus* está fuera por D23 sin verificar su distribución `[?]` (C7 §2). `[H]` Una coincidencia off-target es una hipótesis de riesgo, no un daño demostrado (C7 §8). Persistencia ambiental y resistencia en *D. maidis* no tienen datos propios ni fuente abierta que haya leído `[?]`; Mitter 2017 midió persistencia de dsRNA sobre hojas con arcilla (LDH), que no es nuestro caso `[R]`. El ensayo se hace sobre el insecto objetivo y en condiciones controladas; el diseño no incluye pruebas sobre especies no objetivo.

## Qué quedó sin hacer y por qué

1. **Respuesta del investigador:** no se sabe si contestó el correo; la pregunta de matar o esterilizar sigue abierta y se tratan las dos variantes.
2. **Tamaño de muestra y umbrales numéricos:** requieren la varianza del knockdown entre dsRNA independientes en *D. maidis*, que no está en fuentes abiertas.
3. **Techo de 0,245:** no reproducido en esta sesión; los datos de iBeetle no están en el repo.
4. **Dalaisón-Fuentes 2022 y 2023:** sin texto completo; no se usó su contenido más allá del resumen de 2022.
5. **Latencia del MRFV:** no verificada; la cifra abierta es de *S. kunkelii*.
6. **Candidato a ensayar:** se propone como diseño conceptual con `eth` o `burs-α` para el eje letal y `BicC` para el reproductivo; qué gen ensayar queda para el investigador.
7. **Detección de siRNA y comparación libre contra formulado en insectos:** sin método ni estudio abierto.

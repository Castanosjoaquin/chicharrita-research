# Pendientes de las fases 1 a 3 del checkpoint 2

Fecha: 2026-10-22. Reúne en un solo lugar lo que las fases 1, 2 y 3 dejaron sin hacer, para que ninguna sesión posterior lo dé por resuelto. Cada fila dice qué falta, por qué quedó, qué lo destraba y en qué fase o por quién se cierra. Las fuentes de cada pendiente son las secciones «Qué quedó sin hacer» de `F1_decision_ranking.md`, `F2_entrega_y_mecanismo.md` y `F3_hipotesis_alternativas_validacion.md`, y las entradas de `00_meta/PREGUNTAS_ABIERTAS.md` y `00_meta/CAMINOS_PROBADOS.md` del 2026-10-22. Marcadores según `CLAUDE.md`.

## A. Dependen de una respuesta del investigador o del usuario

| # | Pendiente | Por qué quedó | Qué lo destraba | Se cierra en |
|---|---|---|---|---|
| A1 | Si el investigador contestó el correo, y el texto realmente enviado | No hay forma de saberlo desde el repo; el borrador tiene siete preguntas y `PLAN_DESARROLLO.md` §8 dice cinco | El usuario pasa el texto enviado y la respuesta, si la hay | Fase 4 (casilla 7) y Fase 5 |
| A2 | Matar o esterilizar | Ninguna fuente abierta mide letalidad y reproducción en el mismo gen de *D. maidis* (D40) | Respuesta del investigador a la pregunta 5 del correo | Fase 6; mientras tanto se presentan los dos ejes |
| A3 | Qué gen ensayar | Propuesta conceptual: `eth` o `burs-α` para el eje letal y `BicC` para el reproductivo | Decisión del investigador | Fase 6 |
| A4 | Peso de un hemíptero no objetivo frente al maíz | Es un parámetro del ranking que corresponde al investigador | Su respuesta a la pregunta 4 del correo | Fase 6 |
| A5 | ~~Publicar o no el CSV con las 28 secuencias de Cedden~~ | **Resuelto (Fase 5, D41):** ya estaba publicado en `origin/main` desde el 2026-10-21; se deja publicado con la advertencia de la unión | — | Cerrado |
| A6 | Duración del efecto en *D. maidis* más allá de 5 días | Los ensayos abiertos miden 4 o 5 días y la ventana de latencia es de unos 20 | Pregunta al investigador: ¿hay seguimientos más largos? | Fase 6 |

## B. Faltan datos o recursos que no están en el repo

| # | Pendiente | Por qué quedó | Qué lo destraba | Se cierra en |
|---|---|---|---|---|
| B1 | Escala z y cualquier recálculo del ranking | Faltan las tablas por ventana: `work/sifi_v2/` no existe y los FASTA de EPILAB (`work/sifi_v2/fasta/`) están fuera del control de versiones. `ranking_v2.json` sólo guarda conteos por región | Reconstruir `work/sifi_v2/` en local con `tools/sifi21_port/ranking_v2.py` a partir de `YHat-Biotech/Sequences_EPILAB.xlsx` y de las siete referencias de C7 §9, sin subir nada a servicios web; o declarar la escala z fuera de alcance | Decisión del usuario; no bloquea las fases 4 a 6 |
| B2 | Techo de reproducibilidad de 0,245 | Cálculo del repo sobre datos de iBeetle (*Tribolium*, letalidad); los datos están fuera del repo (`~/yhat/data/ibeetle`) y no se reprodujo en esta sesión. En el repo figura `[H]` | Bajar iBeetle y correr `pipeline/techo_reproducibilidad.py`, o citarlo sólo como `[H]` | Fase 5 |
| B3 | Varianza del knockdown entre dsRNA independientes del mismo gen en *D. maidis* | No está en fuentes abiertas | Un dato del investigador o una fuente nueva; sin él no se fijan n ni umbrales numéricos de knockdown | Fase 6 |
| B4 | Método para detectar siRNA en *D. maidis*; comparación de dsRNA libre contra formulado en insectos | Ningún estudio abierto de los leídos los trae | Una fuente nueva | Fase 6 |
| B5 | Latencia del MRFV | La fuente abierta (Jones y Medina 2020) da 18 a 22 días para *Spiroplasma kunkelii*, no para el virus. D34 usa «unos 20 días» dicho por el investigador | Una fuente para MRFV | Fase 6 |
| B6 | Ensayos de spray y datos de ARN pequeños para MRFV en maíz | No hay en las fuentes abiertas revisadas (ver también C10) | Una fuente nueva | Sin fecha; se declara como límite |

## C. Fuentes sin abrir o abiertas a medias

| # | Pendiente | Estado | Qué lo destraba |
|---|---|---|---|
| C1 | Dalaisón-Fuentes *et al.* 2022 (BicC), doi 10.1002/ps.6937 | Sólo el resumen de PubMed; no es de acceso abierto. Sin el texto no se verifican el día del efecto, la letalidad ni la palabra «esterilidad» | Pedirle el PDF al investigador o conseguirlo por un canal legítimo. No usar espejos |
| C2 | Dalaisón-Fuentes *et al.* 2023 (dsRNasas), doi 10.1016/j.pestbp.2023.105618 | No abierta; no se cita su contenido | Igual que C1 |
| C3 | Figura 5A de Andrada *et al.* 2026 (supervivencia de `ds-eth` a día 4) | La cifra no está en el texto y la imagen no se pudo leer de forma verificable | Leer la figura con el PDF en pantalla (`YHat-Biotech/Papers/finsc-6-1811933.pdf`, página 6) |
| C4 | Gan *et al.* 2010 | Sólo el resumen se usó; el PDF está en el repo | Leer el texto completo |
| C5 | Rutas DCL y AGO de la planta | No se revisaron fuentes abiertas específicas; las fichas las mencionan | Una búsqueda dirigida |
| C6 | Hoang 2022 y la revisión de 2024 | Se leyeron sólo los pasajes relevantes | Lectura completa si hace falta citarlas con más detalle |

## D. Correcciones a archivos existentes (no se hicieron en las fases 1 a 3)

| # | Archivo | Qué corregir |
|---|---|---|
| D1 | `research/ola3/C5_estructura_genes_ingenieria_inversa/catalogo_genes_blanco.md` y `.json`, fila `DM-05` (`eth`) | El 10 % de supervivencia a día 4 es de `burs-alpha` según el texto de Andrada; para `eth` el texto no da cifra propia |
| D2 | Mismo catálogo, fila `DM-01` (`BicC`) | «Esterilidad», «>170 veces al día 7» y «casi nula» no aparecen en el resumen. El resumen dice reducción de oviposición, alteración del oocito y cambios de hasta 170 veces en el transcripto |
| D3 | Mismo catálogo, fila `DM-03` (`ATPaseD`) | No registra el control: ≈37 % con GFP y ≈52 % sin dsRNA a 4 días (Jones 2021) |
| D4 | `research/ola3/C7_ranking_v2/REPORT.md` §6 | Repite los errores de D1 a D3 |
| D5 | `00_meta/FUENTES.md`, entrada S18 | Dice «texto completo no accesible»; el texto se leyó el 2026-10-22 en bioRxiv. Hoy sólo hay una sección de actualización al final, la línea original sigue sin editar |
| D6 | `entregables/para-el-investigador.md` | Aplicar la regla de etiquetas de F1 §5: las 11 líneas con `[E]` pasan a `[M]` o `[H]`, y «ventana eficiente» pasa a «ventana que pasa el filtro de si-Fi21». Reescribir en dos listas por mecanismo (D38) |
| D7 | `entregables/correo-investigador.md` y pregunta 5 | El borrador dice que los candidatos nuevos están «sesgados a esterilidad»; el catálogo registra letalidad para `eth` y `burs-α` y reducción de oviposición para `BicC` |
| D8 | El brief de `FASE_1_decision_ranking_y_etiquetas.md` | Tiene la misma frase sobre esterilidad; está corregida en la salida de la fase |
| D9 | `PLAN_DESARROLLO.md` §8 | Dice cinco preguntas; el borrador tiene siete |

## E. Quedó fuera de las fases por diseño

- `estado.html`: se regenera con `python tools/generar_estado.py` cuando cierre la Fase 5; no se edita a mano.
- Commit y push: no se hicieron, a pedido del usuario.
- Un ADR para el candidato a ensayar: no se escribió porque es una propuesta conceptual, no una decisión.

## F. Lo que no es un pendiente, para no confundirlo

- La escala z no agrega información a lo medido: con dos candidatos da lo mismo que min-max, y puede dar valores negativos en la media geométrica. El barrido reducido que se hizo no está calibrado (hasta 38 puntos porcentuales de diferencia con el guardado) y no se reporta.
- El 0,245 es una cota sobre *Tribolium*; no se transfiere a *D. maidis* sin un dato propio.

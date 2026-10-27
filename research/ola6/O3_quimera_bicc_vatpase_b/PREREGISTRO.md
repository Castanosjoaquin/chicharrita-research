# O3 — Preregistro: cómo se elige la región de `V-ATPase B`, declarado antes de medir

**Fecha y hora de escritura:** 2026-10-27, 09:35 (−03). **Issue:** #23.
**Qué se preregistra:** el criterio con el que esta línea elige la región de 300 nt de
`V-ATPase B` (`VATPaseB_Dm`) que va a formar la quimera con `BicC_Dm` 922-1221, y la lista
de lo que se va a reportar. Se escribe y se commitea **antes de correr el perfil de
eficiencia y antes del tamizaje**, porque esa elección mueve el resultado de la línea más
que cualquier otra cosa que se decida acá.

## 1. Por qué hace falta preregistrarlo

Las otras cuatro regiones del proyecto tienen procedencia conocida. Las dos virales y las
dos del insecto las eligió EPILAB sin ver los off-targets, y C7 las movió a la mejor región
que encuentra la cascada: `MP_MRFV` 72-271, `CP_MRFV` 99-298, `BicC_Dm` 2121-2420 y
`ATPaseD_Dm` 72-371 (`research/ola3/C7_ranking_v2/REPORT.md` §4, nivel 3) `[M]`. `BicC_Dm`
se movió después a 922-1221 por conservación (D25).

`V-ATPase B` no pasó por eso: la línea O2 recuperó la secuencia (D71) y **nadie eligió una
región**. Como el conteo de ventanas eficientes de una región de 300 nt dentro de un CDS de
1.503 nt depende fuertemente de dónde se la ponga, elegir la región **después** de ver los
conteos de la quimera permitiría —sin mala fe— elegir la que da el número que uno quiere.
Por eso el criterio se fija ahora.

## 2. El criterio, en una frase

**La región es la que la cascada de C7 pone primera, con el mismo motor y los mismos pesos
que usó C7, entre las regiones de 300 nt que no se superponen con las bandas de 59 nt de
los dos extremos del CDS.**

Desglosado, y cada pieza con su fuente:

1. **Largo 300 nt**, como `BicC_Dm` y `ATPaseD_Dm`. Lo fija el issue #23.
2. **El orden es la cascada**, que es la forma `cascada` de `tools/sifi21_port/ranking.py`:
   una región queda **vetada** si alguna de sus ventanas tiene una coincidencia perfecta de
   21 nt contra el panel, y entre las no vetadas ordena por `buenos_limpios` —ventanas
   eficientes que no tienen ningún acierto bajo ninguno de los tres criterios—. Es la única
   de las cuatro combinaciones de C7 §4 que ordena el nivel 3 con frecuencia 100 %, y es la
   que C7 usó para mover las cuatro regiones. Se llama a `ranking.ejes()` y
   `ranking.puntaje()` **importados sin modificarlos**.
3. **Los pesos son los base**, `ranking.pesos_base()`: referencias 1,00 maíz / 1,00 humano /
   0,80 *H. axyridis* / 0,80 *A. mellifera* / 0,60 *H. vitripennis* / 0,40 *F. candida*; y
   criterios 1,00 `perfecto_21` / 0,60 `perfecto_ge19` / 0,30 `mm1_21`. No se sortean pesos:
   la cascada no los usa para ordenar (usa `buenos_limpios` y el veto), y el barrido de
   pesos es del ranking, que no es de esta línea.
4. **El panel es el de seis**, con el humano incluido con peso 1,00
   (`ranking_v2.con_panel(sin_humano=False)`), y el genoma de *D. maidis* **excluido** por
   ser on-target: `V-ATPase B` es un gen del insecto, así que le corresponde
   `estrategia = "insecto"` y `ranking.excluidas_de()` lo saca.
5. **La banda de 59 nt en cada extremo se excluye de antemano.** Motivo mecanicista y
   medido: el CDS viene del genoma y **no tiene UTR**, así que una ventana cerca de un
   extremo se pliega contra un contexto que en el ARNm real existe y acá falta. El alcance
   de esa influencia está derivado del código en C13 §4: la secuencia vecina influye hasta
   59 nt corriente arriba del comienzo de una ventana `[M]` el número, `[H]` la derivación.
   Entonces las regiones admisibles arrancan en 60 y terminan en 1.444 (inicios 60 a 1.145).
   **Esto es una desviación declarada respecto de C7**, que no aplicó ninguna restricción de
   borde porque sus cuatro genes son transcriptos completos y no CDS pelados.

## 3. Qué se reporta, y qué no se decide acá

- Se reportan **las tres primeras regiones de la cascada** que no se pisan más de la mitad
  entre sí (`ranking.alternativas(..., tope=3)`), **como sensibilidad**. También se reporta
  el top-3 **sin** la restricción de borde del punto 5, para que se vea cuánto pesa esa
  restricción.
- **La quimera se arma con la primera de la lista restringida.** Eso es el insumo de esta
  medición y **no es una recomendación de región**: recomendar una región de `V-ATPase B`
  no es de esta línea, igual que en M5 y M7. Si otra línea la adopta, tendrá que pasar por
  la compuerta de alertas, que esta línea no toca.
- No se afirma eficacia de la quimera. El criterio de eficiencia de si-Fi21 no está validado
  en hemípteros: ρ = +0,142, IC95 [−0,247, +0,492], n = 29 `[M]`.

## 4. La configuración con la que se va a medir, fijada ahora

Punto por defecto de lo que publica el proyecto: `tools/sifi21_port/run_sifi.py`
**`--modo corregido --backend vienna --tabla-nn NN3`**, 22 °C, ViennaRNA 2.7.2. Ni `fiel`
ni el backend `exe` son el punto por defecto. Entorno: Python 3.11.17, numpy 2.4.6,
Biopython 1.88.

**El marco de cada conteo se declara (D63).** La cifra principal de cada quimera es la del
marco **molécula**, plegada entera, y al lado va la de **contexto**. Para `BicC_Dm` 922-1221
la cifra publicada en marco molécula es 26 `[M]`.

## 5. Las tres cuentas, separadas desde antes de medir

Por quimera y por orden, tres números que **no se suman entre sí** para dar «la cifra de la
quimera» (D67):

1. **Heredadas.** Cuántas ventanas heredadas son eficientes, cuántas cambiaron de veredicto
   respecto de su región plegada sola, en qué dirección y a qué distancia de la unión.
2. **Juntura.** Las 20 ventanas a caballo de la unión: cuántas son eficientes y, de esas,
   cuántas tienen blanco continuo de 21 nt en alguno de los dos genes (método de
   `research/ola5/N4_quimeras/scripts/junturas.py`).
3. **Riesgo del empalme.** Tamizaje de los 40 nt de cada unión contra el panel de seis, más
   la región nueva de `V-ATPase B` completa. El riesgo de las heredadas **se hereda**: el
   estado de off-target de una ventana depende sólo de sus 21 nt (C13 §6) `[M]`.

## 6. Las anclas que tienen que pasar antes de leer cualquier número nuevo

- `quimeras_v2.py --conjunto epilab` reproduce la tabla de C4 en los **dos** modos.
- `--conjunto vigentes --modo corregido` da las doce sumas de C13 §5, con
  `ATPaseD_Dm+MP_MRFV` 47 → 50, `MP_MRFV+ATPaseD_Dm` 47 → 44 y `CP_MRFV+MP_MRFV` 50 → 46,
  4 eficientes de juntura y 61 heredadas cambiadas.
- Las dos se vuelven a correr **después** de generalizar el evaluador.
- `ranking.ejes()` sigue dando los cuatro conteos del nivel 3 de C7 (38, 21, 35, 21) y sus
  `buenos_limpios` (37, 20, 34, 17) sobre los datos ya versionados. Es el ancla de que el
  motor del criterio de esta sección no cambió de comportamiento. `tools/sifi21_port/ranking.py`
  está siendo editado por la sesión del issue #30 en este mismo árbol de trabajo: si esta
  ancla falla, lo primero que se revisa es si el fallo viene de esa edición.

**Si una de esas anclas no pasa y no se arregla con la generalización, esta línea para y lo
dice, sin leer ningún número nuevo.**

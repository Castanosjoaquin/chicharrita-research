# Eje 1, fenotipo: cómo el mecanismo se vuelve un número

**2026-10-27, antes del primer cálculo del orden.** El `PREREGISTRO.md` §6 define **cómo se
asigna** el mecanismo de fenotipo y lo deja verificado contra la fuente, pero no define **cómo
se puntúa**. Esto lo define, y se escribe antes de ordenar por la misma razón que todo lo
demás en esta línea.

## La escala

El eje mide **la fuerza de la evidencia de que silenciar ese gen hace algo en un insecto**, no
el tamaño del efecto. Tres niveles, armados sobre dos campos que ya existen en el catálogo y
que no admiten interpretación: `especie` y `marcador`.

| Nivel | Puntaje | Condición |
| --- | ---: | --- |
| `F3` | **1,00** | Mecanismo medido en ***Dalbulus maidis*** y marcador `[E]`. Sin extrapolación entre especies. |
| `F2` | **0,66** | Marcador `[E]` en otra especie. La evidencia es de consenso, la extrapolación es el supuesto. |
| `F1` | **0,33** | Marcador `[R]`: una o pocas fuentes. |

## Las dos decisiones que la escala toma, y por qué

**No se puntúa por cantidad de mecanismos.** `DE-05` tiene tres mecanismos medidos y `DE-04`
tiene dos, pero `DE-04` es una fila que **agrupa tres genes distintos** —ABCE y ABCF dan
letalidad, ABCB impide el desarrollo ovárico— y `CI-11`, `CI-09`, `HE-03` y `DE-01` también
agrupan más de un gen. Puntuar por cantidad de mecanismos premiaría la decisión editorial de
cuántos genes entraron en una fila, que es un artefacto del catálogo y no una propiedad del
candidato. La cantidad de mecanismos **se publica como columna** y no entra al puntaje.

**No se puntúa por el tamaño del efecto.** Es tentador —«supervivencia 10 % contra 95 %» se
ve más fuerte que «45 % de mortalidad»— y no se puede: las filas miden desenlaces distintos,
en tiempos distintos, con vías de entrega distintas y con dosis que a veces el catálogo no
trae. Comparar esos números entre sí construiría una precisión que no existe. El tamaño del
efecto está en la columna `frases_de_apoyo`, textual y con su contexto, para que quien lea el
orden lo vea; lo que se puntúa es la fuerza de la evidencia.

## Lo que da

De los 25 candidatos con mecanismo: **10 con marcador `[E]`** y 15 con `[R]`, y **5 medidos en
*D. maidis*** (`DM-01`, `DM-02`, `DM-03`, `DM-05`, `DM-06`), los cinco con `[E]` `[M]`.

---

# El eje 3 no se puede llenar con los números del catálogo, y el motivo es el panel

Esto es un hallazgo del paso 3 y vale como la cuarta corrección al preregistro.

Ocho de las 36 filas traen `ventanas_21nt` con conteos de off-target, y era razonable esperar
que sirvieran para el eje 3. **No sirven, porque están contra otro panel.** Las referencias
que esas ocho filas tamizan son cinco:

| Referencia del catálogo (`C5`) | ¿Está en el panel de seis de `D83`? |
| --- | --- |
| genoma de *Dalbulus maidis* | sí |
| *Homalodisca vitripennis* | sí |
| *Zea mays* | sí |
| *Apis mellifera* | sí |
| ***Macrosteles quadrilineatus*** | **no: no es del panel** |
| — *Harmonia axyridis* | **falta** |
| — *Folsomia candida* | **falta** |

`D83` dejó escrita la regla general, y acá se aplica sola: **un tamizado no se identifica por
el gen ni por *k*, se identifica por su panel.** El panel del catálogo tiene un cicadélido
emparentado que el panel de seis no tiene —y que para un gen del insecto es señal de
conservación, no de riesgo— y le faltan dos organismos no objetivo, un coccinélido y un
colémbolo del suelo. Un conteo que omite dos organismos no objetivo sale **optimista**: menos
aciertos, el candidato parece más limpio.

**Consecuencia, y es la que el preregistro ya había previsto por otro motivo:** el eje 3 queda
**declarado no calculable**, como estaba. Lo que cambia es que ahora hay dos razones y no una:
falta `work/sifi_v2/` **y** los números que sí existen son de otro panel. Los conteos de las
ocho filas **se publican** en `orden_genes.tsv`, en columnas con el panel nombrado en el
encabezado y **fuera del puntaje**, porque son información útil que alguien va a querer ver;
lo que no se hace es sumarlos a un eje que dice «panel de seis» cuando no lo son.

`[H]` Y queda una observación que no es de esta línea: si alguien quisiera el eje 3 de verdad
para estos ocho candidatos, no alcanza con conseguir `work/sifi_v2/`, porque ahí están los
seis genes del ranking de `C7` y no los genes del catálogo de `C5`. Habría que tamizar las
ocho secuencias del catálogo contra el panel de seis, que es una corrida nueva.

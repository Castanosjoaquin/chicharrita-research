# C4 — Off-targets, quimeras y largo: de las recomendaciones del investigador a criterios de ranking con evidencia

**Ola 3 del Investigathón Y-Hat, línea C4.** Esta investigación convierte cuatro
recomendaciones del Checkpoint 1 en criterios auditables: cuánta coincidencia hace falta para
que haya silenciamiento fuera del blanco, cuánto pesa que un off-target caiga en el genoma y no
en el transcriptoma, qué se recalcula cuando se pegan dos regiones en una quimera, y de dónde
sale el rango de 150 a 250 nucleótidos. Se evalúa el razonamiento y no el acierto, así que cada
criterio viene con su evidencia o con la declaración de que no la hay.

**Qué se midió acá, en una línea:** 920 ventanas de 21 nt de las cuatro regiones de EPILAB
contra el genoma **y** el transcriptoma de maíz y de abeja —los únicos 2 de los 17 conjuntos
locales que permiten la comparación—, 12 quimeras de a dos con el port de si-Fi21 sin modificar,
y un barrido de 20.000 juegos de pesos sobre el ranking resultante.

---

## Las cuatro respuestas

### Q1 · ¿Cuánta coincidencia contigua hace falta para que haya silenciamiento fuera del blanco?

**El único umbral con bioensayo detrás, en insectos, es el de 21 nucleótidos contiguos
perfectos, y está respaldado en los dos sentidos.** En *Diabrotica undecimpunctata howardi*
(Coleoptera), **un solo bloque de 21 pb idénticos** embebido en un ARNdc de 240 pb da una CL50
de 13,8 a 20,3 ng/mL, mientras que el mismo tramo de 21 pb administrado desnudo no mata (CL50
> 100 ng/mL) `[E]` `S02`. Y al revés: de diez ortólogos de Snf7 probados contra *Diabrotica
virgifera virgifera*, **todos los activos tenían al menos tres coincidencias de 21 nt, y los
que tenían cero —con bloque contiguo máximo de 14, 17 o 19 nt y 78 a 82 % de identidad global—
no fueron activos** ni siquiera a 5.000 ng/mL `[E]` `S01`. La formulación conjunta la enuncia
textualmente un tercer trabajo del mismo grupo: hace falta un tramo 100 % complementario de
≥ 21 nt contiguos embebido en un ARNdc de ≥ 60 nt `[E]` `S03`.

**Nuestro umbral de 19 nt es convención, no evidencia.** La convención existe y está escrita:
una revisión de métodos de 2026 dice que, para un siRNA de 21 nt, **≥ 19 nucleótidos
complementarios alcanzan para marcar un off-target potencial**, y que suelen considerarse
riesgosas las coincidencias con **hasta dos desajustes**; el fundamento que da es la tolerancia
del complejo RISC a unos pocos desajustes, no un bioensayo en insectos `[E]` `S06`. En
dirección contraria apunta el único control negativo de umbral que encontramos: en *Telenomus
podisi*, los genes con **17 a 21 nt de coincidencia** con un ARNdc específico de *Euschistus
heros* no cambiaron su expresión y no hubo efectos letales ni subletales `[R]` `S18` (sólo
resumen; el texto completo está cerrado). Y el umbral de **16 pb de dsRNA-Engineer no tiene
respaldo declarado** y domina su conteo: en la corrida de W2, los 70 off-targets en maíz y 67
de 67 en abeja salieron de esa condición y ninguno de la de 21 `[E]`.

La frase honesta, entonces: **21 nt perfectos está respaldado; 19 nt es una convención
conservadora con fundamento mecánico pero sin experimento; 16 pb no tiene respaldo; y sobre
desajustes no hay en la literatura abierta que leímos ningún experimento en insectos que mida
silenciamiento en función del número y la posición del desajuste** `[?]`. Toda la evidencia de
umbral viene además de Coleoptera y de un solo sistema experimental. Tabla completa, con
especie, entrega, n y medida, en [`evidencia_longitud_minima.md`](evidencia_longitud_minima.md).

### Q2 · ¿Cómo se pondera un off-target que cae en el genoma pero no en el transcriptoma?

**El criterio del investigador es correcto, y nuestros datos muestran que el caso no es
hipotético: es justamente el peor acierto del conjunto.** De las 920 ventanas de las cuatro
regiones, **la única coincidencia perfecta de 21 nt contra todo el maíz cae en una región
intergénica** (`NC_050098.1:189.908.025`), y de los 11 aciertos de ≥ 19 nt contra maíz, 8 están
sólo en el ADN: 3 en un intrón anotado y 5 en regiones intergénicas, tres de ellas el mismo
19-mero rico en GC repetido en loci distintos `[E]`.

**Pero la asimetría va en los dos sentidos, y eso es lo que esta investigación agrega al
criterio.** Los 3 aciertos de `BicC_Dm` que sí tocan un gen expresado de maíz
(`LOC100281777`) **no existen en el genoma**: localizamos los nueve bloques —3 ventanas × 3
variantes de transcrito— y los nueve **cruzan una unión exón-exón** (posición 1.279 del
transcrito NM_001154697.2 y 1.415 de los otros dos), así que en el ADN sus dos mitades están
separadas por un intrón `[E]`. La consecuencia práctica es incómoda: **el genoma no es un
sustituto conservador del transcriptoma**, porque pierde exactamente las ventanas de unión de
exones, que acá fueron las únicas que tocaron secuencia expresada.

La medición usa **2 de los 17 conjuntos locales** —*Zea mays* y *Apis mellifera*, los únicos
con genoma y transcriptoma en disco—; en abeja no hay un solo acierto perfecto en ninguno de
los dos recursos. Para *Homalodisca vitripennis*, que es donde está el riesgo real, no hay
genoma local y por lo tanto la pregunta queda abierta. La ponderación propuesta `[H]` —exón y
unión de exones 1,0; ARN no codificante 0,6; intrón 0,3; intergénico 0,1, con intergénico
distinto de cero porque «no anotado» no es «no transcrito»— baja el riesgo en maíz de
`BicC_Dm` de 11 unidades sin ponderar a 2,25, sin cambiar su posición en el ranking. Todo en
[`genoma_vs_transcriptoma.md`](genoma_vs_transcriptoma.md).

### Q3 · ¿Qué se recalcula en una quimera y cómo cambia el número?

**La observación del investigador se cumple en lo esencial y falla en un detalle que importa.**
Es cierto que el empalme es el único lugar donde aparece secuencia nueva y que hay que
recalcularlo: en las 12 quimeras, las 20 ventanas del empalme aportaron entre **0 y 15**
ventanas eficientes. Pero la eficiencia total **no** es la suma salvo en la unión: en las doce,
la diferencia contra la suma de las partes va de **−4 a +19**, y la contabilidad sólo cierra
cuando se suman también las **ventanas heredadas que cambiaron de veredicto** —46 en total, en
los dos sentidos (26 pasaron a eficientes, 20 dejaron de serlo)—. La identidad Δ = eficientes
del empalme + saldo neto de las heredadas se verifica en las 12 `[E]`.

Esas ventanas que cambian no tocan el empalme: están **hasta a 54 nucleótidos de distancia**
(mediana 30, ninguna a 60 nt o más). El techo tiene explicación exacta: de los tres filtros de
si-Fi21, el de accesibilidad se calcula con RNAplfold con **ventana de plegado de 80 nt**, de
modo que una ventana de 21 nt comparte contexto de plegado con el otro gen hasta 59 nt de
distancia `[E]` el número, `[H]` la atribución causal. **El orden también importa**: las mismas
dos regiones dan +19 en un orden y +3 en el otro.

Del lado de los off-targets, **las 240 ventanas de empalme no aportaron ni un solo acierto en
ninguna base no objetivo** (maíz, *H. vitripennis*, *Apis mellifera*, *Harmonia axyridis*,
*Folsomia candida*) `[E]`. Sí aportaron 24 contra el genoma del propio blanco, que es
on-target, y de esos sólo 3 son 21/21: verificamos su causa leyendo el flanco real en el
ensamblado y es que **el pegado reconstruye por azar el vecindario genómico** —la base pegada
de `ATPaseD_Dm` coincide con la base que precede a la región de `BicC_Dm` en
`OZ319706.1`— lo cual confirma, por la vía del ejemplo, que correr el tamizaje sobre la
molécula completa es necesario `[E]`. En la literatura, los dos casos hemípteros de ARNdc
concatenado que encontramos usan 262 pb (tres fragmentos, *Apolygus lucorum*, `S11`) y 300 pb
(tres fragmentos de 100 pb, *Bemisia tabaci*, `S21`), y ninguno supera al mejor gen solo en
mortalidad final: lo que ganan es **velocidad** de silenciamiento. Detalle en
[`quimeras.md`](quimeras.md).

### Q4 · ¿De dónde sale 150–250 nt?

**No sale de la literatura abierta que leímos, y en nuestra propia especie blanco hay
evidencia publicada en contra.** Andrada et al. 2026 silenciaron *burs-α* y *eth* en *Dalbulus
maidis* por microinyección con ARNdc de **578 y 544 pb** (n = 40 por tratamiento, 125 ng por
insecto), con reducción significativa del transcrito y mortalidad alta `[E]` `S14`. Lo que la
evidencia sí sostiene es el **piso**: ~60 pb, medido como serie de largos en *D. undecimpunctata
howardi* —0 % de mortalidad a 27 y 40 pb, 16 % a 50, 68 % a 60 y 95–96 % de 70 a 240 pb `[E]`
`S02`—. Y lo que sostiene, en algunas especies, es que pasar de unos cientos de pares de bases
no agrega: 200 pb superó a 500 y a 1.000 pb en *Mythimna separata* (60 larvas por tratamiento,
dieta con 3 µg diarios) `[E]` `S10`. Pero hay resultados en sentido contrario —2.222 pb mejor
que 259 pb en *Manduca sexta*, 400–540 pb mejor que 200–300 pb en *Drosophila*, citados por
`S11` `[R]`— y una revisión de 2025 que lo dice sin vueltas: **no existe consenso sobre el largo
óptimo**, con silenciamiento documentado en *Leptinotarsa decemlineata* desde 141 hasta 1.506 pb
`[E]` `S09`.

Nuestra lectura `[H]`: **150–250 nt es una convención de laboratorio razonable y compatible con
la evidencia, no una conclusión de ella.** Está cómodamente por encima del piso, coincide con
los valores por defecto de las herramientas del campo —300 nt en dsRNAmax `S07`— y tiene un
argumento de manufactura a favor: por encima de 500 nt se compromete el rendimiento de expresión
bacteriana y la carga en nanoacarreadores `S22` `[R]`. No encontramos ninguna fuente concreta en
la que el laboratorio pueda estar fundando la cifra. En Hemiptera, además, la restricción mejor
documentada no es el largo sino la **estabilidad**: el ARNdc desnudo deja de detectarse a las
3 horas en extracto de *Acyrthosiphon pisum* `[E]` `S12`.

---

## 1. Qué había en el repositorio y qué no repetimos

Antes de buscar nada leímos `CLAUDE.md`, los cuatro apartados indicados de
`research/checkpoints/checkpoint1.md`, `pipeline/REPORT.md` §4 y §5,
`research/ola2/W5_secuencias_epilab/REPORT.md` §5 con sus `analisis/region_vs_*.tsv`,
`research/ola2/W2_herramientas/REPORT.md`, `research/R1_fundamentos/REPORT.md` §4, los dos
módulos del port (`cruce.py` y `offtarget_21nt.py`) y `research/ola2/W1_papers/papers.json`.

No repetimos: el tamizaje de las cuatro regiones contra las seis referencias de W5 (lo
reprodujimos sólo como control de que corremos la misma herramienta igual, y da los mismos 222,
205, 220, 204, 30, 22, 7, 3, 3 y 3); la lectura por dentro de dsRNA-Engineer y BLAST; la
reproducción de si-Fi21 contra el programa original; ni el barrido de pesos de `pipeline/`, que
citamos como la medición de referencia del problema de los pesos.

Lo que **sí** es nuevo de esta investigación: la comparación genoma contra transcriptoma del
mismo organismo —que ninguna ola había hecho—, la clasificación de cada acierto por clase de
blanco, la verificación de que los aciertos sobre maíz expresado son ventanas de unión
exón-exón, las 12 quimeras con su contabilidad de empalme, el alcance medido del efecto de
contexto, y la prueba de dominancia y sensibilidad del ranking de los cuatro candidatos.

## 2. Cómo se corrió, y con qué versiones

Entorno conda `w5bio` de esta máquina: Python 3.11.17, ViennaRNA 2.7.2, BLAST+ 2.17.0,
Biopython 1.88, más `pyahocorasick` instalado para esta línea. Port de si-Fi21 **sin modificar
por nosotros**: los md5 están en `NOTAS_PARA_META.md`. Durante la sesión, otra línea de la ola 3
parametrizó `offtarget_21nt.py` con `--size` y `--min-block` y lo commiteó después de nuestros
tamizajes; **volvimos a correr los dos tamizajes con la versión nueva y las tablas por siRNA
salen idénticas byte a byte**, así que todos los conteos de este informe valen para las dos
versiones `[E]`. Todas las secuencias de
EPILAB se procesaron localmente; **nada salió de la máquina**. El tráfico de red fue de entrada
y hacia servicios públicos: Europe PMC para buscar y bajar textos completos de acceso abierto.

Los comandos exactos están al pie de cada documento y en los scripts. Resumen:

| Script | Qué produce |
| --- | --- |
| `scripts/genoma_vs_transcriptoma.py` | el cruce por región y criterio, y la clasificación exón / intrón / intergénico de los 25 aciertos en el ensamblado de maíz |
| `scripts/q2_empalme_exonico.py` | la verificación de que los 9 bloques sólo-transcriptoma cruzan una unión exón-exón |
| `scripts/quimeras_sifi.py` | las 12 quimeras, su perfil de eficiencia con `run_sifi.py`, y la comparación ventana por ventana |
| `scripts/quimeras_offtarget.py` | los aciertos de empalme contra las seis referencias de W5 |
| `scripts/q3_empalme_contexto.py` | el flanco genómico real de las dos regiones del insecto |
| `scripts/ranking_sensibilidad.py` | dominancias y barrido de 20.000 juegos de pesos |

Salidas crudas en `resultados/`; copias de trabajo, bases y registros en `work/C4/` (fuera de
git).

## 3. Lo que contrasta con `pipeline/` y no lo duplica

`pipeline/` ya hace coincidencia exacta de k-meros de 21 nt en las dos hebras contra
transcriptomas de 25 especies, guarda el riesgo desagregado por especie y agrega con media
geométrica ponderada, con barrido de pesos (`pipeline/REPORT.md` §4 y §5). Esta investigación
**no** propone reemplazar nada de eso. Propone agregar dos términos que hoy no existen —la
clase de blanco donde cae el acierto, y el criterio de coincidencia que lo detectó, cada uno
con su peso explícito— y señala una cosa que el pipeline hoy no puede ver: como trabaja contra
transcriptomas, **no detecta aciertos intrónicos ni intergénicos** (lo cual, con la ponderación
propuesta, es casi correcto: su peso sería bajo) pero **sí ve las uniones exón-exón**, que es lo
que un tamizaje contra genoma perdería. Para las 5 especies del catálogo sin anotación, donde
`pipeline/` usa genoma crudo y encuentra 49 descartes extra, esta investigación aporta el
argumento de que esos descartes no son comparables con los de transcriptoma y deberían entrar
con peso de clase «sin anotación», no con peso de exón.

## 4. Huecos declarados

No hay evidencia experimental, en lo que leímos, de que una coincidencia en intrón o en región
intergénica produzca o no efecto; el único trabajo que clasifica ubicación de aciertos (`S05`)
no hace el experimento. No hay bioensayo de umbral de coincidencia en Hemiptera. No hay
experimento publicado que mida silenciamiento en función del número y la posición de los
desajustes en insectos. No hay comparación publicada de una quimera contra sus partes
administradas por separado, ni límite publicado de largo total para quimeras en insectos. No
pudimos abrir el texto completo de `S18` (cerrado) ni de Whyard et al. 2009 (cerrado), que es la
fuente que `S01` cita para el umbral de 19–21 nt entre especies de *Drosophila*: de ese trabajo
sólo podemos reportar lo que `S01` dice de él. Y no bajamos el genoma de *Homalodisca
vitripennis*, que es la comparación genoma-transcriptoma que más valdría.

## 5. Preguntas para el investigador

Están en `NOTAS_PARA_META.md` con su contexto. Las tres que más cambian lo que hacemos: de
dónde sale el 150–250 —si hay un ensayo propio con largos comparados en *D. maidis*, ese dato
vale más que toda nuestra tabla de literatura—; qué peso relativo le da el laboratorio a un
hemíptero no objetivo frente al maíz, que es el único parámetro del criterio que no nos
corresponde fijar; y si el equipo de EPILAB corre el tamizaje de off-targets contra
transcriptomas, contra genomas, o contra los dos, porque de eso depende si la ponderación de Q2
es una mejora o una corrección.

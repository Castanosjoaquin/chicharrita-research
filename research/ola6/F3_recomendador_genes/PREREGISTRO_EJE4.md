# F3 — Eje 4, conservación entre poblaciones: el criterio, escrito antes de calcularlo

**Fecha de escritura: 2026-10-27.** Extiende `PREREGISTRO.md` §3 (eje 4) y §4.2. Issue
[#27](../../../../issues/27), casilla del eje de conservación en el inventario
[#37](../../../../issues/37).

El `PREREGISTRO.md` declaró el eje 4 **no calculable** porque los tres transcriptomas de
*Dalbulus maidis* no estaban en la máquina donde corrió la línea. El barrido de `R12`
(`research/ola6/R12_corridas_pendientes/REPORT.md`) midió que **sí están** en la máquina de
Joaquín —`TSA_GCWP01.fasta`, `TSA_GHCC01.fasta` y `TSA_GITV01.fasta` en `work/W5/ref/`, con
25.662, 55.286 y 56.117 secuencias `[M]`— y que lo que frenaba la corrida ya no era el insumo
sino **este documento**: el criterio de terminado del #27 pide que el criterio se escriba
antes de la primera corrida, y el preregistro original no cubre cómo se puntúa este eje,
porque lo había declarado incalculable.

Esto es esa escritura previa. Se commitea **antes** del primer cálculo del eje, igual que
`escala_fenotipo.md` y `escala_esencialidad.md` en su momento. Lo único que se miró del insumo
antes de escribir —y se declara para que el orden quede claro— es **qué archivos existen, su
largo y su procedencia**: los conteos de secuencias de arriba, los largos de las cinco
secuencias candidatas de §2, y el encabezado de `VATPaseB_Dm_cds.fna`. Ninguna ventana se
comparó con ningún transcriptoma.

**Lo que este documento no reabre.** Los pesos son los de `D87` (confirmados por el usuario el
2026-10-27): conservación **0,10**. No
se discute acá. Tampoco se tocan las escalas de los ejes 1 y 2, ni el umbral de empate de
0,05, ni la regla de cohortes de `PREREGISTRO.md` §4.2.

## 1. Qué pregunta contesta el eje, y cuál no

Contesta: **de la molécula que se silenciaría, qué fracción existe idéntica en las tres
poblaciones de *D. maidis* de las que hay transcriptoma público.** Una región muy limpia que
sólo existe en un aislado no sirve, que es el argumento con el que `C8` ya movió la
recomendación de región de `BicC_Dm`.

No contesta si el diseño sirve en el campo del noroeste argentino. `C8` §2 ya dejó escrito que
los tres TSA son fuentes públicas de orígenes distintos —Illinois, Ohio State y Argentina
(depositado desde el CeBio, Pergamino)— y **no** poblaciones de campo muestreadas para esto
`[M]`. «Poblaciones» en el nombre del eje significa eso y nada más. La conclusión que este eje
habilita es «la molécula es estable entre las fuentes públicas que existen», no «es estable
entre poblaciones».

## 2. Qué candidatos pueden recibir el eje, y de dónde sale la secuencia de consulta

La unidad sigue siendo **la fila del catálogo de `C5`** (36 filas). El eje necesita una
secuencia de *D. maidis* del gen de esa fila, y hay una regla que decide cuáles la tienen:

> **La secuencia de consulta no puede venir de ninguno de los tres TSA.** Si viniera, su
> presencia en ese transcriptoma estaría garantizada por construcción y el eje mediría dos
> poblaciones disfrazadas de tres.

Con esa regla, las filas con secuencia admisible en esta máquina son **cinco**, todas `DM`:

| Fila | Gen | Secuencia | Largo | Procedencia, e independencia de los TSA |
| --- | --- | --- | ---: | --- |
| `DM-01` | `BicC` | `work/sifi_v2/fasta/BicC_Dm_full.fasta` | 2.520 nt | planilla de EPILAB, dato no publicado. No sale de ningún TSA |
| `DM-02` | `V-ATPase B` | `research/ola6/O2_vatpase_b/resultados/VATPaseB_Dm_cds.fna` | 1.503 nt | CDS predicho por `miniprot` sobre el **genoma** `OZ319705.1`, no sobre un transcriptoma `[M]` |
| `DM-03` | `V-ATPase D` | `work/sifi_v2/fasta/ATPaseD_Dm_full.fasta` | 491 nt | planilla de EPILAB |
| `DM-05` | `eth` | `work/sifi_v2/fasta/eth_Dm_full.fasta` | 615 nt | ARNm público `PZ371507.1` |
| `DM-06` | `burs-alpha` | `work/sifi_v2/fasta/bursA_Dm_full.fasta` | 468 nt | ARNm público `PZ371508.1` |

`DM-04` (`Dmai-dsRNase-2`) es de la propia especie y **no tiene secuencia en esta máquina**:
sale con el eje ausente, no con cero. Las 30 filas que no son *D. maidis* tampoco lo reciben,
y por un motivo de fondo y no de insumo: su gen es de otra especie, y lo que habría que medir
es la conservación de **su ortólogo en *D. maidis***, que es una secuencia que nadie recuperó.

**Lo que explícitamente no se hace, y es la tentación obvia.** `F1` (#25) dejó 4.110 contigs
de `GITV01` con ortólogo recíproco y nombre de producto, así que sería fácil buscar ahí el
ortólogo de cada candidato por nombre y usarlo de consulta. No se hace, por dos razones
independientes: *(a)* ese contig **es** de uno de los tres TSA, y viola la regla del recuadro;
*(b)* el emparejamiento candidato → contig pasaría por el nombre del producto, y el
repositorio ya midió lo que cuesta ese atajo —elegir el gen por nombre en vez de por ortología
recíproca movió el conteo de ventanas eficientes un 65 % `[M]`, `PREREGISTRO.md` §4.1—.
Recuperar esos ortólogos es trabajo de otra línea, y queda anotado como tal.

Tampoco se usan los ensamblados genómicos. `C8` §2 midió por qué: el haplotipo 2 del Reino
Unido está incompleto en estos loci y usarlo contaría huecos como variación, y el de Córdoba
es ONT a 20x, con tasa de error del orden de la variación que se busca `[M]`. El eje usa los
tres TSA y nada más.

## 3. La medida

Sobre la secuencia de cada candidato se toman **todas** sus ventanas de 21 nt consecutivas
(paso 1; una secuencia de largo L da L − 20 ventanas). La elección de 21 nt no es libre: es la
unidad de diseño de toda la cadena, y es la misma con la que `C8` midió conservación.

Para cada candidato y cada TSA:

1. **Dónde está el gen en ese transcriptoma.** `blastn -task megablast` de la secuencia
   completa contra el TSA, con `-evalue 1e-20`, `-max_target_seqs 50` y `-outfmt 6` con
   `qstart qend sstart send pident length`. Se toma **el contig con mejor bitscore** y se
   retienen sus HSP. Si ningún HSP alcanza el umbral, el gen se declara **ausente en ese
   transcriptoma** y las ventanas no tienen dato ahí.
2. **Ventanas con dato.** Una ventana tiene dato en ese TSA si **sus 21 posiciones caen dentro
   de la unión de los tramos de consulta (`qstart`–`qend`) alineados contra ese contig**.
   Separar «con dato» de «sin dato» es la parte del método que `C8` §2 llama la segunda
   precaución: una ventana ausente puede ser variación o puede ser un hueco del ensamblado, y
   contar las dos juntas infla la variación.
3. **Ventanas idénticas.** De las que tienen dato, es idéntica la que aparece **exacta**, en
   cualquiera de las dos hebras, en alguna secuencia de ese TSA. La búsqueda exacta se hace
   con un autómata de Aho-Corasick sobre el archivo completo, no sobre el contig elegido: así
   una ventana que quedó partida entre dos contigs del mismo ensamblado no se cuenta como
   variación. Es coincidencia exacta de cadena, sin parámetros de alineamiento que elegir.

**El puntaje del eje**, para un candidato, es

> fracción = (ventanas idénticas en **los tres** TSA) / (ventanas con dato en **los tres** TSA)

acotada a [0, 1] por construcción, que es la escala que `PREREGISTRO.md` §4.2 pide para poder
renormalizar los pesos. El denominador son las ventanas evaluables en las tres fuentes a la
vez, no las de la secuencia entera: un candidato no se castiga por lo que el ensamblado no
cubre.

**Y se publican, al lado del puntaje y en la misma fila:** las ventanas totales, y por cada
TSA las ventanas con dato y las idénticas. Sin esas seis columnas el puntaje no se puede leer,
porque una fracción alta sobre pocas ventanas evaluables y una fracción alta sobre todas son
afirmaciones distintas.

**Un candidato con menos del 50 % de sus ventanas evaluables en los tres TSA no recibe
puntaje**: sale con el eje ausente y el motivo `cobertura insuficiente`, en vez de un número
que descansa sobre la mitad de la molécula. El umbral se fija acá, antes de ver ninguna
cobertura. `C8` ya midió el caso que lo motiva: `GCWP01` cubre sólo fragmentos de `BicC_Dm`
—569 ventanas con dato de 2.500 `[M]`—.

### 3.1 Por qué esta medida no es la de `C8`, aunque se parezca

`C8` midió identidad **por alineamiento local** de la secuencia contra el contig que `W5` ya
había ubicado, y marcó «con diferencia» toda ventana que cruza un salto entre bloques
alineados. Esta medida pregunta **presencia exacta en el ensamblado completo**. Las dos
difieren en un caso concreto: una ventana que existe idéntica en otro contig del mismo
transcriptoma cuenta como idéntica acá y como diferente en `C8`.

Por eso los números de este eje **no son intercambiables** con los de
`research/ola3/C8_conservacion/resultados/conservacion.json`, y el reporte va a decirlo en la
tabla. Como control, y porque sale gratis, el reporte **compara las dos medidas en los cuatro
genes que `C8` cubre** (`BicC_Dm`, `ATPaseD_Dm`, `eth_Dm`, `bursA_Dm`) y declara la diferencia
fila por fila. Si alguna difiere en más de **5 puntos porcentuales**, eso es un hallazgo del
control y se escribe como tal, no se promedia con el resto.

## 4. Qué le pasa al orden cuando entra el eje

Los candidatos que reciben el eje 4 **cambian de cohorte**: pasan de «A: ejes 1 y 2» a una
cohorte nueva «A+4: ejes 1, 2 y 4», y se ordenan sólo contra quienes tengan los mismos ejes.
Es `PREREGISTRO.md` §4.2 aplicado sin excepción: entre cohortes no se compara, y un candidato
no mejora ni empeora su puesto por un eje que no tiene. En la cohorte nueva los pesos de `D87`
se renormalizan sobre los ejes 1, 2 y 4: **0,5333 / 0,3333 / 0,1333**.

Consecuencia prevista, y se escribe antes de calcular para que no parezca elegida después: hoy
el primer puesto de la cohorte A es un **empate declarado de tres** —`DM-02`, `DM-03` y
`DM-05`, los tres en 1,0000 `[M]`, `resultados/meta.json`—, y **los tres están entre los cinco
candidatos que reciben el eje 4**. Así que la pregunta que este cálculo contesta es si el eje
rompe ese empate. Con el peso renormalizado en 0,1333 y el umbral de empate en 0,05, hace
falta una diferencia de **más de 0,375 en la fracción de conservación** entre dos de ellos para
que el empate se rompa. Si la diferencia es menor, **el empate sigue declarado**: no se
desempata con un eje que pesa menos que la resolución del criterio, que es exactamente lo que
§4.3 prohíbe.

`orden_genes.tsv` se **regenera** con el eje adentro, y el `REPORT.md` del eje publica el
`diff` contra la versión anterior fila por fila. Regenerarlo mueve cifras publicadas de esta
línea, y por eso se dice acá: lo que cambia es el agregado de un eje que el propio preregistro
dejó previsto para que llegara «sin rehacer el criterio».

## 5. Reglas que siguen valiendo, y las que este eje agrega

De `PREREGISTRO.md` §7 valen las seis sin cambios. En particular la 5: **ninguna salida
versionada lleva nucleótidos de 21 nt o más.** Las ventanas, los contigs elegidos y las salidas
crudas de `blastn` quedan en `work/F3_eje4/`; lo versionado son conteos, fracciones e
identificadores de contig. Y la 3: este eje no entra al diseño del ARNdc; contesta qué gen
considerar.

Tres que agrega este documento:

1. **Ausencia del gen en un TSA no es conservación cero.** Si `blastn` no lo encuentra, ese
   TSA no aporta denominador. Un gen ausente en uno de los tres se publica con esa palabra y
   cae por el umbral de cobertura de §3, no por un puntaje bajo.
2. **Nada se baja de internet en esta corrida.** Las cinco secuencias y los tres TSA están en
   disco. Las de EPILAB no salen de la máquina: `blastn` y el autómata corren local, que es la
   regla de confidencialidad de `CLAUDE.md`.
3. **La versión de `blastn` y el `sha256` de cada TSA quedan declarados** en `meta.json` del
   eje. `R8` dejó la lección de que una medición de identidad sin la versión de la herramienta
   no es reproducible.

## 6. Cómo se verifica que este documento se respetó

- Este archivo tiene fecha de commit **anterior** al primer cálculo del eje, y el commit del
  cálculo lo cita.
- Ningún candidato cuya secuencia de consulta salga de un TSA recibe puntaje; verificable en la
  columna de procedencia de la salida, que trae las cinco rutas de §2.
- Cada candidato del orden trae su cohorte, y ninguna comparación cruza cohortes.
- Las seis columnas de cobertura por TSA están en todas las filas que reciben el eje.
- El control contra `C8` está en el reporte, con las cuatro filas y la diferencia declarada.
- El umbral de cobertura (50 %) y el de empate (0,05) son los de este documento y los de
  `PREREGISTRO.md` §4.3, sin ajustar después de ver los números.

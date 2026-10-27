# F3 — Recomendador de genes: el criterio, escrito antes de rankear

**Fecha de escritura: 2026-10-27.** Issue [#27](../../../../issues/27). Plan:
`docs/plan_ola6/PLAN_OLA6.md` §1 grupo C, `F3`.

Este documento se commitea **antes** del primer cálculo del orden. Es la condición que el
issue pone para que la línea sea defendible, y es la misma forma que `M5`, `M7` y `O4`:
el objetivo se declara antes de medir, de modo que el resultado no pueda elegir su propio
criterio. Si algo de lo que sigue cambia después de la primera corrida, cambia como una
entrada nueva con fecha, no como una corrección silenciosa de este archivo.

## 1. Qué ordena esta línea, y qué no

Ordena **genes**, no regiones. Elegir la región dentro de un gen ya está resuelto y es
enumerable por fuerza bruta; elegir el gen es el nivel que el proyecto dejó abierto y es
donde trabaja el investigador `[R]`.

Lo que esta línea **no** hace, y conviene dejarlo escrito porque es la confusión más fácil:
no afirma eficacia. Toda la cadena hereda el criterio de eficiencia de si-Fi21, que no está
validado en hemípteros —ρ = +0,142, IC95 [−0,247, +0,492], n = 29 `[M]`—, así que un orden
in silico es una hipótesis sobre eficacia y no una prueba (Guía del checkpoint 2). El
argumento del entregable es «cada paso lleva su propia tasa de error medida», no «predice
mejor». Tampoco elige el gen que se recomienda: ordena y mide, y la elección es del equipo y
del investigador, igual que en `M5` y `M7`.

## 2. El universo de candidatos

El catálogo de genes blanco de `C5`,
`research/ola3/C5_estructura_genes_ingenieria_inversa/catalogo_genes_blanco.json`, campo
`filas`: **36 filas** `[M]`. Cuatro familias de identificador —`DM` para *Dalbulus maidis*
(6), `CI` para cicadélidos (13), `DE` para delfácidos (6) y `HE` para heterópteros y otros
(11)— y dos estados de procedencia: `ya_estaba_pipeline` (16) y `nuevo_C5` (20) `[M]`. Por
marcador de evidencia, 13 filas son `[E]` y 23 son `[R]` `[M]`.

Una fila del catálogo no es siempre un gen: `DE-04` agrupa varios transportadores ABC,
`CI-11` agrupa `NcLac2` y `NcLac1`, `HE-03` agrupa `JHAMT` y vitelogenina, y `HE-10` dice
«varios». La unidad que esta línea ordena es **la fila del catálogo**, con su identificador,
y donde la fila agrupa más de un gen se dice en la salida. Inventar una fila por gen
obligaría a repartir una evidencia que la fuente no reparte.

## 3. Los cinco ejes

Son los de la tabla del plan, uno por línea, con lo que hay y lo que no.

**Eje 1 — fenotipo por RNAi en un insecto emparentado.** Sale de las columnas `resultado`,
`entrega`, `dosis`, `n_tiempo` y `marcador`. Es el eje que `D67` vuelve obligatorio: si las
quimeras se arman por combinación de mecanismos que no se solapan, el recomendador tiene que
saber a qué mecanismo pertenece cada candidato. Hoy `tablero/orden.html` sólo cubre `BicC` y
la V-ATPasa, y el ranking no tiene eje de fenotipo. **Calculable con material versionado.**

**Eje 2 — esencialidad o vía metabólica.** Sale de `funcion` y `familia_proteina`, contra
literatura. Las vías que el proyecto ya tiene escritas son la V-ATPasa, el proteasoma 26S,
COPI, la fosforilación oxidativa y el citoesqueleto muscular. **Calculable con material
versionado.**

**Eje 3 — perfil de off-target contra el panel de seis.** **No calculable en esta máquina.**
El perfil por gen de los seis genes del ranking de `C7` vive en `work/sifi_v2/salida_k21/` y
el tamizado contra el panel en `work/sifi_v2/offtarget_k21/`, y `work/sifi_v2/` **no existe
en el disco de esta máquina** `[M]`. Del catálogo, además, **sólo 8 de las 36 filas** tienen
`ventanas_21nt` calculadas —`DM-05`, `DM-06`, `CI-01`, `CI-02`, `CI-03`, `CI-10`, `DE-02` y
`DE-05`—; las otras 28 son `None` `[M]`. Las dos cosas apuntan a la misma regla: este eje se
declara, no se rellena.

**Eje 4 — conservación entre poblaciones de *D. maidis*.** **No calculable en esta máquina.**
Pide los tres transcriptomas `TSA_GCWP01`, `TSA_GHCC01` y `TSA_GITV01`, que `prompts/F3.md`
ubica en `work/W5/ref/`; ese directorio en esta máquina tiene **sólo** `humano_rna.fna.gz` y
su `.sha256` `[M]`. Lo que sí está versionado es
`research/ola3/C8_conservacion/resultados/conservacion.json`, que cubre las regiones
probadas del insecto y de los virus, no los 36 candidatos del catálogo: alcanza para una
nota, no para un eje.

**Eje 5 — expresión en el tejido expuesto.** **No existe para ningún candidato, y es el eje
que más importa para una vía de entrega oral** `[H]`: si el gen no se expresa en el intestino,
el ARNdc ingerido no tiene qué silenciar. Los tres transcriptomas públicos de *D. maidis* son
de cuerpo entero y huevos. Este eje se publica **declarado como faltante, en el mismo lugar
donde se publica el orden**, y no se sustituye por una fuente de otra especie ni por una
inferencia a partir de la función del gen.

> De los cinco ejes, **dos** son calculables con los insumos de esta máquina, **dos** piden
> `work/sifi_v2/` y los tres TSA, y **uno** no existe en ninguna máquina. El criterio que
> sigue está escrito para que la llegada de `work/sifi_v2/` agregue los ejes 3 y 4 **sin
> rehacerlo**, que es la razón de escribirlo antes.

## 4. La forma de agregación

### 4.1 Por qué no una suma ponderada sobre los 36

La tentación es normalizar los cinco ejes a [0, 1], ponderarlos y sumar. No se hace, por una
razón medida y no estética: 28 de las 36 filas no tienen el eje 3 y ninguna tiene el eje 5.
Una suma ponderada sobre ejes ausentes obliga a imputar, y cualquier imputación —cero, la
media, el peor caso— **fabrica un número que la fuente no da**. El repositorio ya midió lo
que cuesta esa clase de atajo: elegir el gen por nombre en lugar de por ortología recíproca
movió el conteo de ventanas eficientes un **65 %** `[M]`, y ése es el argumento más fuerte
que tenemos contra las features que completan huecos con lo que parece razonable.

### 4.2 La forma que sí se usa: cohortes por ejes disponibles

Los candidatos se agrupan en **cohortes** definidas por *qué ejes tienen calculados*, y se
ordenan **dentro** de su cohorte. Entre cohortes no se compara, y la salida dice a qué
cohorte pertenece cada candidato. Un candidato nunca mejora su puesto por un eje que no
tiene; tampoco lo empeora.

Dentro de una cohorte, el orden es una suma ponderada **renormalizada sobre los ejes de esa
cohorte**, con los pesos de §5. Renormalizar sobre los ejes presentes es lo único que
permite que un peso signifique lo mismo en dos cohortes distintas.

### 4.3 Los empates se declaran

Si dos candidatos quedan a menos de **0,05** en el puntaje de su cohorte, se publican como
**empate declarado** y no se les inventa un desempate. Es lo que `R6` dejó como forma para el
tercer puesto, y la razón es la misma: el criterio de eficiencia que alimenta la cadena no
tiene la resolución necesaria para distinguir diferencias de ese tamaño.

## 5. Los pesos — propuesta, no decisión

**Esto es lo único de este documento que el equipo tiene que confirmar antes de que se
rankee nada.** El issue está etiquetado `decide-usuario` y la regla del alcance es proponer
el ADR, no fijarlo.

| Eje | Peso propuesto | Por qué ese peso |
| --- | --- | --- |
| 1 — fenotipo | **0,40** | Es el único eje con evidencia experimental de que silenciar el gen hace algo en un insecto. `D67` lo vuelve obligatorio para armar quimeras. |
| 2 — esencialidad o vía | **0,25** | Sostiene la extrapolación a *D. maidis* cuando el fenotipo se midió en otra especie, pero es argumento de mecanismo y no medición. |
| 3 — off-target contra el panel | **0,25** | Es el eje de riesgo y **no depende del criterio de eficiencia sin validar**, lo que lo hace el más sólido de los cuatro. Pesa igual que la esencialidad y no más porque hoy está calculado para 8 de 36. |
| 4 — conservación entre poblaciones | **0,10** | Condición de que el diseño sirva fuera de una población, no de que funcione. |
| 5 — expresión en tejido expuesto | **0,00, declarado faltante** | No se le asigna peso porque no se puede medir. Un peso cero **no** significa que no importe: es el eje que más importaría para entrega oral `[H]`. |

Los pesos suman 1,00 sobre los ejes 1 a 4. En las cohortes donde falten el 3 y el 4, la
renormalización de §4.2 reparte 0,40 y 0,25 en 0,615 y 0,385.

**Las tres alternativas que se consideraron**, para que la confirmación sea sobre algo y no
sobre un número suelto: *(a)* fenotipo 0,50 y off-target 0,20, que premia la evidencia
experimental y castiga poco el riesgo; *(b)* la propuesta de arriba; *(c)* off-target 0,40 y
fenotipo 0,30, que ordena por el eje más sólido metodológicamente aunque sea el que menos
candidatos tienen calculado. El `REPORT.md` va a decir **en qué rango del peso de fenotipo
cambia el primer puesto**, que es la pregunta que vuelve la elección informada.

## 6. El eje de fenotipo: cómo se asigna, y los tres casos que el catálogo rompe

`D67` define tres mecanismos que no se solapan: **reproducción**, **movilidad** y
**letalidad**. La asignación sale de `resultado`, en una columna explícita, **nunca inferida
del nombre del gen**: un recomendador que lee «V-ATPase» y escribe «letalidad» está
adivinando, y es exactamente el modo de falla contra el que `F2` está diseñado.

Al recorrer las 36 filas aparecen tres casos que los tres mecanismos no cubren, y los tres se
resuelven acá y no al escribir el resultado:

**6.1 Hay un cuarto mecanismo en el catálogo: reducción de la transmisión.** `CI-07`
(clatrina, baja la colonización del fitoplasma), `CI-09` (natterina y lectina, reduce la
multiplicación), `HE-07` (`NcSP75`, proteína salival de la transmisión) y `HE-11`
(*Graminella nigrifrons*, interacción con *Maize fine streak virus*) describen un fenotipo que
no es reproducción, ni movilidad, ni letalidad: es **menos transmisión con el insecto vivo**.
Es el mecanismo más alineado con el objetivo sanitario del proyecto, y `D67` no lo tiene.
Se agrega como **cuarta categoría declarada**, `transmision`, y queda anotado como entrada
abierta porque amplía un ADR ajeno.

**6.2 Dos candidatos tienen el fenotipo de signo invertido.** `CI-08` (`uk1_LRR`) dice que
silenciarlo **AUMENTÓ** la colonización del vector por el fitoplasma, y `CI-13` (`NcHig`) que
silenciarlo **AUMENTA** la infección del sistema nervioso por el virus. Silenciar esos genes
empeora el problema que queremos resolver. La regla: un candidato con fenotipo de signo
invertido **no entra al orden**; se publica en una lista aparte, rotulada
`fenotipo_invertido`, con su fuente. No se le pone puntaje negativo, porque el puntaje
sugeriría que compite.

**6.3 Un candidato tiene mortalidad no atribuible al blanco.** `HE-08` dice, con todas las
letras, «mortalidad alta por la dosis, no por el blanco». Esa fila **no cuenta como
letalidad**: se rotula `sin fenotipo atribuible al blanco`. Es el control negativo que el
propio catálogo trae, y tratarlo como un éxito invalidaría el eje entero.

## 7. Reglas de exclusión y cortafuegos

1. **Sin fenotipo publicado se dice, no se puntúa con cero.** Un candidato sin `resultado`
   informativo —`HE-10` y `HE-11` son los casos claros— sale con «sin fenotipo publicado».
   Cero y «no sabemos» son afirmaciones distintas y se escriben distinto.
2. **Una región con alerta sin firmar no sale como recomendada.** `D72` y `D77`: la compuerta
   de alertas es el único camino por el que una región llega a ser recomendada, y el
   recomendador **no la saltea**. Las filas de
   `research/ola4/M6_alertas/resultados/alertas.tsv` que se consuman tienen que tener
   `decision_usuario` resuelta; firmar es del equipo (`D48`, `D68`, `D73`).
3. **Ninguna salida de esta línea entra al diseño del ARNdc.** Contesta *qué gen considerar*.
   El diseño se hace siempre sobre la secuencia propia del vector. Es `D37`, y vale acá igual
   que en `F1`.
4. **Ningún eje no calculado se ordena como si lo estuviera.** Verificable: ningún candidato
   sin `ventanas_21nt` puede aparecer ordenado por el eje 3.
5. **Ninguna salida versionada lleva nucleótidos de 21 nt o más.** Las secuencias quedan en
   `work/F3/`.
6. **Un conteo sin su nulo no se publica.** Lección de `R8`: ocho desajustes parecían un
   hallazgo y eran la mediana del azar.

## 8. Cómo se verifica que este documento se respetó

- El `PREREGISTRO.md` tiene fecha de commit anterior al primer cálculo del orden.
- Cada candidato del orden trae su mecanismo de fenotipo, o una de las cuatro etiquetas de
  ausencia: «sin fenotipo publicado», «sin fenotipo atribuible al blanco»,
  `fenotipo_invertido` o «sin anotación».
- El eje 5 aparece declarado faltante en `orden_genes.tsv` —una columna en todas las filas— y
  en el encabezado del `REPORT.md`, no en una nota al pie.
- Cada candidato trae su cohorte, y ninguna comparación cruza cohortes.
- El `REPORT.md` dice el rango del peso de fenotipo en el que cambia el primer puesto.
- El entorno y la versión de cada herramienta quedan declarados en el `REPORT.md`, como en
  `R8`.

## 9. Entorno de esta corrida

Máquina de Santino, Windows 11 Pro for Workstations 10.0.26300. Python 3.13.15, numpy 2.5.4,
ViennaRNA 2.7.2 como módulo `RNA`, Biopython 1.88 y `ahocorasick` `[M]`. Sin alineador en el
PATH —`blastn`, `tblastn`, `makeblastdb`, `diamond`, `mmseqs`, `miniprot`: ninguno— y sin
`RNAplfold` ni `RNAfold` como ejecutable, aunque `bowtie.exe` y `RNAplfold.exe` están en el
corpus en `siFi21-source/ToCopy/` `[M]`. `work/` presente con `C13`, `M1`, `M2`, `O3`, `O4`,
`offtarget_db`, `sifi_check`, `sifi_plus` y `W5`; **sin** `sifi_v2` `[M]`.

Esta línea, con este criterio, **no necesita ninguna de esas herramientas**: los ejes 1 y 2
se calculan sobre el catálogo versionado. Lo que falta para los ejes 3 y 4 es insumo, no
entorno, y está pedido al grupo.

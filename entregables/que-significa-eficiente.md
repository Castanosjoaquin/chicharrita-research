# Qué significa que un siRNA sea «eficiente»

> **Nota de lectura (Fase 5, 2026-10-22).** «Eficiente» es el nombre de un booleano por ventana de 21 nt: la ventana pasa o no pasa las tres condiciones de si-Fi21. No mide eficacia. En la página de siete casillas y en el entregable se dice «ventana que pasa el filtro de si-Fi21».

**Para qué es esta nota.** En el checkpoint 1 lo primero que nos pediste fue entender si-Fi21:
qué implica que algo sea eficiente, cómo se calcula y qué significa la energía libre en ese
contexto. Esto es la respuesta, escrita para leerse sin abrir código. Todo lo que afirma sale del
artículo (Lück *et al.* 2019, *Front Plant Sci* 10:1023), del manual que viaja dentro del
repositorio oficial (`Quick_help.pdf`) y del fuente de GitHub en el commit `d6296b7`, los tres
abiertos y leídos; el detalle con archivo y línea está en
`research/ola3/C1_sifi21_paper_metodo/`.

Marcadores: `[E]` establecido, `[R]` reportado por una o pocas fuentes, `[H]` hipótesis nuestra,
`[?]` incierto.

---

## La respuesta en un párrafo

«Eficiente» no es una medida ni un puntaje: es **un sí o un no por cada ventana de 21
nucleótidos**, y sale de combinar con un `and` tres condiciones biofísicas, más una cuarta regla
sobre dos nucleótidos sueltos que no es una condición sino una ramificación. De los seis valores
que deciden ese sí o no, **dos tienen fuente experimental abierta y específica, dos tienen fuente
para el principio pero no para el número, y dos no tienen ninguna fuente**. Y el conjunto entero
—la herramienta, no los umbrales— se validó una vez, con doce construcciones en cebada contra un
hongo, midiendo fenotipo y no caída del transcrito. Nada de eso es eficacia medida de un siRNA.

---

## 1. Cómo se calcula, paso a paso

si-Fi21 recorre el gen con una **ventana de 21 nucleótidos que avanza de a uno**. Un gen de 1.263
nt da 1.243 ventanas, y cada una es un siRNA hipotético. Para cada ventana hace cuatro cosas.

**Primero, la busca en una base de datos** con BOWTIE, por defecto exigiendo coincidencia exacta.
Esto no mide eficacia: resuelve dónde pega esa ventana. Vale saber que si se le permiten
desajustes, **el propio programa apaga el cálculo de eficiencia**, y el manual dice por qué:
«porque no hay datos confiables» (páginas 7 y 11). `[E]`

**Segundo, evalúa si la hebra correcta es la que se va a cargar.** Un ARN de doble cadena tiene
dos hebras y sólo una sirve: la que es complementaria al mensajero del gen que se quiere
silenciar. Cuál de las dos se carga en la maquinaria no es azar, depende de cuál de los dos
extremos del dúplex es más fácil de abrir. si-Fi calcula la energía de los tres pares de cada
extremo y exige que el extremo de la hebra guía sea el más débil.

**Tercero, exige que esa diferencia sea de al menos 1,00 kcal/mol.** Es la misma comparación
anterior pero pidiendo un margen. Como implica la condición anterior, con las dos activadas la
primera no agrega nada.

**Cuarto, mira si el sitio del mensajero está accesible.** De nada sirve un siRNA perfecto si el
tramo del mensajero al que apunta está plegado sobre sí mismo. si-Fi pide que la probabilidad de
que un tramo de 8 nucleótidos esté desapareado sea de al menos 0,1, y la calcula con RNAplfold.

Y después aplica la **regla del nucleótido terminal**: preferencia de U o A en el extremo 5′ de la
guía y de G o C en el de la pasajera. Las tres condiciones anteriores se combinan con un `and`;
esta cuarta regla **no suma ni multiplica: elige qué mirar**, y volvemos sobre eso en la sección 4.

## 2. Qué es la energía libre acá, y qué no es

Es la energía que cuesta abrir el extremo de un dúplex de ARN, calculada sumando la contribución
de cada par de bases vecinas a partir de tablas medidas en laboratorio. Tres cosas que conviene
tener claras:

- **Lo que importa es la diferencia entre los dos extremos, no el valor absoluto.** El criterio es
  comparativo: cuál de los dos extremos se abre más fácil. Un dúplex muy estable con los dos
  extremos igual de firmes no pasa.
- **Se calcula a 22 °C, no a 37.** Circula lo contrario. Ya está en el rango ambiente que
  corresponde a un insecto y a un cultivo a campo, así que no había nada que corregir ahí; lo que
  sí notamos es que el valor está fijo en dos lugares distintos del código y no es un parámetro.
- **No es eficacia.** La energía libre dice qué hebra se va a cargar con más probabilidad. No dice
  cuánto va a bajar el mensajero ni cuántos insectos van a morir.

## 3. La tabla: cada umbral y de dónde sale

| Filtro | Qué mide | Umbral por defecto | Fuente primaria del número | ¿Empírica o convención? |
| --- | --- | --- | --- | --- |
| **Tamaño de ventana** | Largo del siRNA simulado | 21 nt | Elbashir, Lendeckel y Tuschl 2001, *Genes Dev* 15:188-200: los mediadores de la interferencia son fragmentos de 21-22 nt, en lisado de embrión de *Drosophila melanogaster* | **Empírica** |
| **Regla del nucleótido terminal 5′** | Preferencia de U/A en la guía y G/C en la pasajera | Activada, sin número | Ui-Tei *et al.* 2004, *Nucleic Acids Res* 32:936-948: 62 blancos de seis genes, en células de mamífero, *Drosophila* y embrión de pollo | **Empírica** |
| **Selección de hebra guía** | ΔG de los 3 pares de cada extremo 5′ | ΔG(guía) ≥ ΔG(pasajera), sin margen | Schwarz *et al.* 2003 y Khvorova, Reynolds y Jayasena 2003, *Cell* 115 (sólo resumen accesible) | Empírica **para el principio**, no para el corte |
| **Accesibilidad del sitio blanco** | Probabilidad de que 8 nt del mensajero estén desapareados | **≥ 0,1** (u = 8, L = 40, W = 80) | Tafer *et al.* 2008, *Nat Biotechnol* 26:578-583 (sólo resumen): calibran con 573 siRNA de 38 genes | Empírica **para el principio y para u = 8**; **convención** para el 0,1 |
| **Estabilidad de extremos** | La misma diferencia, con margen mínimo | **1,00 kcal/mol** | **Ninguna.** Khvorova 2003 reporta 0,5 kcal/mol de diferencia media entre dúplex funcionales y no funcionales: el umbral de si-Fi es el doble y no se deriva de esa medición | **Convención** |
| **Temperatura** | Temperatura de todo el cálculo | **22 °C** | **Ninguna.** El artículo no menciona la temperatura en ninguna de sus 12 páginas | **Convención no documentada** |

Tres aclaraciones sobre la tabla:

- **«Identidad» no es un filtro de eficiencia.** En el checkpoint la mencionaste como tercer
  término del criterio, junto con energía libre y estructura secundaria. En el código no existe
  ninguna función de identidad dentro del cálculo: la identidad entra por BOWTIE, que es
  alineamiento, y por un experimento del propio artículo donde la eficacia cae por debajo del 92 %
  de similitud entre disparador y blanco. `[E]` Es una propiedad del par secuencia-blanco, no un
  filtro por ventana.
- **Los desajustes de BOWTIE y las tablas de energía no entran en esta tabla** porque no son
  criterios: uno es el alineador y las otras son parámetros de química.
- **El artículo no tiene ninguna ecuación numerada, ni un ajuste, ni una curva ROC** para la regla
  de eficiencia. La única formulación compacta está en la Discusión, página 8, y es un enunciado.

## 4. Lo que encontramos al leer el código, y cambia los números

**La regla del nucleótido terminal no filtra: ramifica.** `[E]` El código compone primero el
veredicto termodinámico y después aplica esa regla, y una de sus ramas devuelve «eficiente»
**sin mirar el veredicto termodinámico**: cuando el nucleótido 19 es A o T y el 2 no lo es, decide
mirando sólo la accesibilidad. Un siRNA que falla la selección de hebra y la estabilidad de
extremos puede quedar clasificado como eficiente por esa vía.

Medido ventana por ventana sobre los cuatro genes de la planilla, con el mismo RNAplfold:

| Gen | Eficientes que reporta si-Fi | Entran por esa rama | Proporción |
| --- | ---: | ---: | ---: |
| `MP_MRFV` | 133 | 19 | 14 % |
| `CP_MRFV` | 32 | 7 | 22 % |
| `BicC_Dm` | 212 | 50 | 24 % |
| `ATPaseD_Dm` | 42 | 8 | 19 % |

Entre el 14 % y el 24 % de lo que si-Fi reporta como eficiente lo es **sólo porque esa regla se
saltea la física**, y ninguna ventana va en sentido contrario. `[E]` Por qué nos parece que es un
defecto y no una decisión: la preferencia del bolsillo de Argonauta por un 5′ terminal U o A es
una regla de afinidad que **suma** evidencia sobre cuál hebra se carga; no es un mecanismo que
vuelva innecesaria la asimetría termodinámica del dúplex, que es lo que gobierna el desenrollado.
Tratarla como sustituto invierte la jerarquía causal, y el propio artículo presenta las reglas de
secuencia como complemento de las termodinámicas, no como reemplazo. `[H]`

**Dos consecuencias prácticas más**, las dos medidas:

1. **El conteo depende de si la región se calcula sola o dentro del gen.** Recortar la región y
   correrla como archivo nuevo —el procedimiento que describiste— no da lo mismo que leer esas
   mismas posiciones de la corrida del gen entero. La diferencia llega al **47 %** en `MP_MRFV`
   (16 contra 30). La causa es la accesibilidad: RNAplfold evalúa plegado local, y un fragmento
   recortado pierde el contexto que apareaba o liberaba su extremo. Antes de comparar regiones hay
   que fijar cuál de los dos procedimientos se usa y declararlo.
2. **El número de «eficientes» depende de la base de datos**, porque si-Fi suma un registro por
   acierto de BOWTIE y no un siRNA único. Con un transcriptoma con parálogos e isoformas, el mismo
   criterio da otro número.

## 5. Qué se validó, y qué no

El artículo **valida la herramienta entera, no ningún umbral por separado**. `[E]` El sistema es
cebada (*Hordeum vulgare*) transformada transitoriamente por bombardeo de partículas en epidermis
de hoja separada, inoculada con *Blumeria graminis* f. sp. *hordei*, con *HvMlo* como blanco. La
medida de eficacia **no es la caída del ARN mensajero**: el propio artículo dice que medir el
transcrito no es viable en ese sistema, así que usa el fenotipo de susceptibilidad como sustituto.

El resultado que sostiene «si-Fi predice un siRNA potente» es uno solo: la correlación de Pearson
entre la cantidad de siRNA predichos y el efecto medio de silenciamiento es **−0,61 en el modo de
alta eficiencia**, contra −0,37 en alta sensibilidad y −0,31 para el total de aciertos. Se lee con
tres límites: **n = 12**, la unidad es la **construcción y no el siRNA** —ningún siRNA individual
fue medido— y la variable es un fenotipo de resistencia en planta, no un nivel de transcrito en
insecto.

Y un dato que toca directamente una de las tres condiciones: en los datos independientes que
pudimos revisar, **la accesibilidad del sitio blanco no mostró valor predictivo sobre la eficacia
medida** — razón de probabilidades 1,00 con intervalo [0,89–1,12] sobre 300 casos humanos de
siRecords, y en *Tribolium castaneum* un cociente de riesgo de 0,9994 con P = 0,853. `[E]` No
decimos que la accesibilidad no importe; decimos que en los datos disponibles no se ve, y que eso
afecta a una de las tres patas del criterio.

## 6. De dónde sale el largo de 150 a 250 nt

De ningún lado que hayamos podido abrir, y lo verificamos en los tres lugares. `[E]`

- **En el artículo no hay ninguna recomendación de largo de región.** Al contrario: las
  construcciones del experimento del «reloj molecular» son de **500 pb**, y el experimento de
  accesibilidad usa ventanas de 100 pb rellenadas hasta 500 pb. Las únicas apariciones de «150» y
  «250» en las doce páginas son la densidad de conidios del bioensayo y un número de página.
- **En el manual tampoco.** Su criterio de región es cualitativo: una región ideal contiene sólo
  área verde —sin off-targets— y la mayor cantidad posible de área cubierta por la línea roja.
  No da un largo, ni mínimo ni máximo.
- **En el código menos: si-Fi21 no busca regiones.** Dibuja el perfil y la elección de región la
  hace una persona mirando el gráfico.

Así que el rango que usa el laboratorio es un criterio propio, y es la pregunta que te queremos
hacer: **¿en qué se funda?** Por nuestra parte, lo que la literatura abierta sostiene es un
**piso** de alrededor de 60 pb, y hay evidencia en contra de un techo bajo en la propia especie
objetivo: un trabajo de 2026 silenció dos genes en *Dalbulus maidis* con ARNdc de 578 y 544 pb,
con reducción del transcrito y mortalidad alta. Una revisión de 2025 dice directamente que no hay
consenso sobre el largo óptimo. `[E]` Nuestra lectura es que 150-250 es una convención de
laboratorio razonable y compatible con la evidencia, no una conclusión de ella. `[H]`

---

## En qué queda

Que un siRNA sea «eficiente» significa que **pasó una regla de diseño enunciada, no que se haya
medido que silencia**. La regla tiene dos umbrales sin fuente —el margen de 1 kcal/mol y la
temperatura—, uno cuyo valor numérico es convención —el 0,1 de accesibilidad—, y una rama que
puede declarar eficiente a un siRNA que falló la termodinámica, que explica entre el 14 % y el
24 % de lo que el programa reporta.

Eso no la invalida: es la línea de base del campo y es con lo que hay que trabajar. Pero fija
cómo hay que leer el número. Por eso, en todo lo que presentamos, «eficiente» va con la aclaración
de qué modo y qué backend se usó, y el conteo nunca se presenta como una predicción de cuánto va a
silenciar.

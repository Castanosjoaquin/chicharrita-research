# R8 — Notas para la memoria del proyecto

Separadas por destino, como en las otras líneas. **Esta línea no escribe ningún ADR**: la
firma de `D73` se confirmó y no se reescribió, y el issue #32 pedía ADR nuevo sólo si el
veredicto cambiaba.

## Para `DECISIONS.md`

Nada. Y conviene que quede dicho por qué, porque la ausencia es el resultado: `D73` firmó la
fila de `eth_Dm` 193-392 declarando faltante el dato de si el gen impactado pertenecía a una
familia conservada en el panel. R8 lo trajo, el veredicto no se movió, y el issue es explícito
en que «una firma confirmada también es resultado». Reescribir la firma para decir lo mismo
habría ensuciado el historial de `decisiones.tsv` sin agregar información.

## Para `PREGUNTAS_ABIERTAS.md`

1. **La entrada 21 de la ola 6 queda contestada** y puede cerrarse: la quitinasa
   `LOC124369889` tiene ortólogo recíproco en *H. axyridis* (55,4 %), *A. mellifera* (51,0 %)
   y *F. candida* (47,9 %), no lo tiene en maíz ni en humano, y la ventana de la posición 347
   cae en un tramo variable con 8 desajustes mínimos sobre 21 contra todos los ortólogos
   `[M]`. Lo que **sigue abierto** es la condición de la firma, que es otra entrada: la
   exposición de *H. vitripennis* (pedido 4, `D47` contra `D18`).
2. **Queda abierto si la ventana cae en un dominio catalítico nombrado.** Lo medido es
   conservación empírica entre los ortólogos recuperados, que es lo que pedía el issue. Para
   nombrar el dominio harían falta `InterPro` o `hmmer` con `Pfam`, que no están en la
   máquina. `[?]`
3. **La reciprocidad se evaluó con un transcripto por acierto**, el de mejor `bitscore`. Para
   genes con variantes de empalme eso puede estar eligiendo una variante y no la canónica, y
   no se midió cuánto cambiaría el resultado tomando la canónica. `[?]`

## Para `CAMINOS_PROBADOS.md`

1. **Lo que funcionó, y conviene reutilizar: el nulo barato para leer un conteo de
   desajustes.** Las cinco referencias dieron **exactamente** 8 desajustes mínimos, un
   resultado lo bastante uniforme como para parecer un error de código. Dos controles de
   seis segundos lo resolvieron: el positivo —la ventana contra su propio transcripto da 0, y
   el script aborta si no— y el nulo —40 ventanas al azar contra el mismo ortólogo dan mínimo
   6, mediana 8, máximo 10—. Sin el nulo, «8 desajustes» se lee como «poco»; con el nulo se
   lee como «lo que da cualquier secuencia», que es una afirmación distinta y es la que
   sostiene la conclusión. **Cualquier conteo de casi-coincidencias que se publique debería
   venir con su nulo**, por la misma razón por la que M1 declaró las celdas no corridas.
2. **Lo que se descartó: buscar el ortólogo con `offtarget_21nt.py`.** Es la herramienta
   correcta para el tamizaje de 21-meros y la incorrecta para esta pregunta, porque
   Aho-Corasick es exacto por construcción y un ortólogo que difiere en unos pocos
   nucleótidos no aparece. Es la misma distinción que `F1` ya tenía escrita como corrección
   de método, y acá se usó de verdad.
3. **Lo que se descartó: decidir por nombre.** Las tres anotaciones recíprocas dicen
   «probable chitinase 2», lo que es corroboración cómoda, pero el nombre se leyó **después**
   de decidir por reciprocidad, no antes. En humano eso fue lo que evitó el error: el mejor
   acierto es `CHIA`, que **es** una quitinasa de verdad y aun así **no** es par recíproco de
   `LOC124369889`. Por nombre habría entrado como ortólogo.

## Para el registro de entorno

**BLAST+ 2.17.0+ ya está instalado en la máquina de Joaquín**, desde `bioconda` en un entorno
conda aparte (`blastn`, `tblastn`, `blastp`, `makeblastdb`). El issue #32 declaraba que
faltaba en las dos máquinas y nombraba esa falta como freno de `F1` (entrada 12) y de parte
de `O3`. **Esos dos frenos, en lo que dependía de BLAST+, ya no aplican acá.** Sigue sin estar
`miniprot` en esta máquina —la de Luca lo tiene, 0.18-r281 en WSL— y para R8 no hizo falta.

## Contradicciones con cifras publicadas

Ninguna. Nada de lo medido en R8 contradice una cifra publicada: la fila de `eth_Dm` 193-392
conserva su conteo de 1 ventana con 21/21 y 5 con bloque ≥ 19 nt, y la región vigente
`eth_Dm` 114-313 conserva su cero contra todo el panel.

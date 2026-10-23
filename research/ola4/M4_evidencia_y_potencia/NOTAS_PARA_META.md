# Notas de M4 para la memoria del proyecto

**Todo lo que esta linea tenia que llevar a `00_meta/` ya esta trasladado, en el mismo commit.**
Este archivo es el indice de donde quedo cada cosa, no una segunda copia: una version anterior
repetia el texto completo de las entradas y las dos copias empezaron a divergir en la misma
sesion, que es exactamente la forma en que una memoria duplicada se vuelve inutil.

| Que | Donde quedo |
|---|---|
| La decision del usuario sobre la casilla de validacion, y el preregistro de la tercera via como trabajo declarado y sin ejecutar | `00_meta/DECISIONS.md`, **D53** |
| Los cinco pendientes del inventario de fuentes: la pregunta de iBeetle-Base, Huesken sin descarga abierta, siRecords y GenomeRNAi sin abrir, y la dispersion del silenciamiento que suponemos | `00_meta/PREGUNTAS_ABIERTAS.md`, seccion «Pendientes abiertos por la linea M4 (2026-10-23)» |
| Las seis fuentes abiertas con su licencia, y las dos que no se pudieron abrir | `00_meta/FUENTES.md`, seccion «Fuentes de etiquetas de eficacia, inventariadas por la linea M4» |
| Los dos descartes: remuestrear un diseno enriquecido en discordantes, y pedir mas datos del mismo tipo sin mirar la discordancia | `00_meta/CAMINOS_PROBADOS.md`, seccion «Estimar por remuestreo un diseno enriquecido en discordantes» |
| La regla reutilizable —contar discordantes y no n— y la correccion sobre donde estan Bowtie y RNAplfold | `.claude/napkin.md` |

## Que sirve de lo que salio, y que no

**Sirve** `scripts/potencia_dos_modelos.py` como calculo de potencia reutilizable: no necesita el
corpus ni el motor de eficiencia, su unico insumo es la tabla de 29 filas que dejo C9, y las cuatro
piezas —remuestreo, prueba de aleatorizacion por intercambio, enumeracion exacta y las cuentas de
dos grupos y de equivalencia— sirven para cualquier comparacion futura entre dos variantes del
criterio, no solo para esta.

**Sirve con el numero corregido:** el n para distinguir los dos modos replicando el diseno de
Cedden es **2.784** `[M]`. El **232** de la primera corrida es un piso optimista y no se debe citar
suelto: sale de remuestrear copias del unico siRNA discordante observado, lo que deja a esa clase
con varianza cero. La diferencia entre los dos numeros es de doce veces, asi que la distincion no es
un matiz.

**No sirve como medicion** el tamano de muestra del ensayo propuesto, 32 siRNA por brazo: depende de
dos supuestos nuestros marcados `[H]` —dispersion de 20 puntos porcentuales entre siRNA de una misma
clase y margen de equivalencia de 15— y ninguno de los dos esta medido. La tabla completa de
alternativas esta en la seccion 4 del REPORT para que se pueda releer el numero con otros supuestos.

## Para quien siga la linea

Lo que queda es de datos, no de codigo. La pregunta de iBeetle-Base (pendiente 1) se contesta en una
tarde y decide si existe alguna via retrospectiva; si la respuesta es que no hay dos fragmentos por
gen, la unica via es el ensayo de la seccion 4 y conviene llevarlo a la reunion como lo que es: la
casilla de validacion del entregable. El preregistro de la tercera via no se ejecuta hasta que haya
100 etiquetas y 3 genes, y esa condicion esta escrita para que no se negocie despues.

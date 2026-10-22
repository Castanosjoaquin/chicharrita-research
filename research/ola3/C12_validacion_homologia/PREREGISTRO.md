# C12 — ¿Cuánto vale la homología como regla para inferir función? Pre-registro de la validación A

**Fijado el 2026-10-22, antes de calcular ninguna concordancia.**

## Pregunta
Si dos proteínas de hemípteros son ortólogas recíprocas por secuencia con identidad X, ¿con qué frecuencia la anotación de una coincide con la de la otra? Es la medida empírica de «un gen muy parecido hace algo parecido», que el equipo había planteado como determinista y que acá se trata como probabilidad.

## Datos (en disco, RefSeq)
Proteomas anotados de *Macrosteles quadrilineatus* (GCF_028750875.1), *Homalodisca vitripennis* (GCF_021130785.1) y *Nilaparvata lugens* (GCF_014356525.2). Pares: MQ–HV (dos cicadélidos) y MQ–NL (cicadélido contra delfácido).

## Método
`blastp` en ambos sentidos (e ≤ 1e-10, hasta 5 hits), par recíproco por mejor bitscore. Se agrupa por identidad de aminoácidos en cinco tramos: <40, 40–60, 60–80, 80–90, ≥90 %. La concordancia es 1 si el nombre de producto normalizado coincide (se quitan «isoform Xn», «-like», «homolog», números de isoforma y mayúsculas); se excluyen los pares donde alguno se llama «uncharacterized» o «hypothetical».

## Límite declarado ANTES de mirar
Los nombres de RefSeq son predicciones computacionales que ya derivan de homología. Esta medida mide **consistencia entre anotaciones**, no función demostrada: un error sistemático de nombre se repetiría en ambas. No hay verdad experimental independiente para miles de genes, así que la cifra es una cota de coherencia, no de exactitud.

## Qué cuenta como resultado
Se reporta la concordancia por tramo con IC95 de Wilson, sea alta o baja. No hay umbral de éxito: lo que se busca es la curva.

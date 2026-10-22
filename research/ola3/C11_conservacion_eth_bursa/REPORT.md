# C11 — ¿Están `eth` y `burs-alpha` en los transcriptomas de *D. maidis* que ya tenemos?

**Fecha:** 2026-10-21. **Qué se corrió:** `blastn` local (BLAST+, entorno `w5bio`) de las dos
secuencias codificantes públicas (`PZ371507` para `eth`, 615 nt; `PZ371508` para `burs-alpha`, 468 nt)
contra los tres transcriptomas TSA ya descargados. **No se subió ninguna secuencia a un servicio web.**

## Resultado, con la verificación exacta

Un alineamiento de BLAST con identidad 100 % no prueba que el contig sea el mismo transcrito: sólo
prueba el tramo alineado. Por eso cada hit se verificó comparando el tramo del contig con la
consulta, letra por letra, en la cadena que indica BLAST.

| Consulta | Transcriptoma | Contig | Tramo alineado (consulta) | Identidad | Verificación letra por letra |
| --- | --- | --- | --- | --- | --- |
| `eth` (615 nt) | GHCC01, Pergamino | `GHCC01027218.1` (759 nt) | 1–615, **completa** | 100 % | **idéntica, en cadena reversa** |
| `burs-alpha` (468 nt) | GHCC01, Pergamino | `GHCC01014529.1` (813 nt) | 30–468 (439 nt) | 100 % | **idéntica, cadena directa** |
| `eth` | GITV01, Ohio | `GITV01054587.1` (669 nt) | 1–440 (440 nt) | 99,5 % | **no verificada**: el tramo de BLAST no coincide en la posición reportada |
| `burs-alpha` | GITV01, Ohio | `GITV01010186.1` (622 nt) | 30–468 (439 nt) | 97,95 % | no verificada en esta pasada |

Ningún contig contiene la consulta completa salvo el de `eth` en GHCC01, y ese sí la contiene.

## Qué cambia respecto de lo que se había dicho

C8 (`research/ola3/C8_conservacion/REPORT.md`, §sobre `eth` y `burs-alpha`) declaró que **no se
ubicaron contigs** de estos genes en los transcriptomas, y que la búsqueda contra el TSA de NCBI
quedó en cola y se canceló. El plan (§8) dice que el transcriptoma que los contiene no está depositado.
**Con la búsqueda local, eso no es correcto para GHCC01**: el TSA del CeBio de Pergamino contiene
secuencia de ambos genes con identidad completa en el tramo cubierto. La búsqueda local no tiene el
problema del servicio web que se colgó. `[E]` para el tramo verificado.

## Lo que todavía no se puede afirmar

- **Que los contigs sean el mismo transcrito y no un parálogo muy parecido.** Para afirmarlo hay que
  verificar la identidad completa de la secuencia codificante y mirar la cobertura en el contig, no
  sólo el tramo alineado. `[?]`
- **Que `eth` y `burs-alpha` sean ortólogos de los contigs de GHCC01 en la población de campo** del
  noroeste argentino. GHCC01 es una colecta de 2015 de huevos y cuerpo entero, de una población, y no
  una medición de variación entre poblaciones. `[H]`
- **Los hits de GITV01 no están verificados** y no se usan para ninguna conclusión.

## Qué sigue

Verificar la identidad de la secuencia codificante completa para el contig de `eth` en GHCC01, que es
el único que contiene la consulta entera, y la cobertura de `burs-alpha` en el extremo 5′ que le falta.
Después recién se corrige el plan.

## Archivos

`hits_GHCC01.tsv`, `hits_GITV01.tsv` (salida cruda de BLAST, con el formato de columnas en la cabecera
de cada consulta).

# C12 · Validación A — concordancia de anotación entre hemípteros según la identidad

**Resultado: la concordancia de nombre sube con la identidad, de 76 % (40–60 %) a 86 % (≥ 90 %), y nunca llega a 100 %.** Fecha 2026-10-22, BLAST+ 2.17.0, local. Pre-registro: `PREREGISTRO.md` (commit `459d341`), escrito antes de calcular.

## Qué se midió
Pares recíprocos por secuencia entre *Macrosteles quadrilineatus* (GCF_028750875.1) y *Homalodisca vitripennis* (GCF_021130785.1). Se compararon los nombres de producto de RefSeq normalizados (sin «isoform», «-like», etc.), excluyendo pares «uncharacterized» o «hypothetical».

| identidad de aminoácidos | pares | concordancia | IC95 (Wilson) |
|---|---|---|---|
| < 40 % | 16 | 25,0 % | 10,2–49,5 |
| 40–60 % | 134 | 76,1 % | 68,2–82,5 |
| 60–80 % | 456 | 76,8 % | 72,7–80,4 |
| 80–90 % | 336 | 78,6 % | 73,9–82,6 |
| ≥ 90 % | 210 | 86,2 % | 80,9–90,2 |
| total | 1.152 | 78,2 % | |

## Cómo leerlo
Una proteína con ≥ 90 % de identidad con su ortólogo recíproco lleva el mismo nombre en el 86 % de los casos. Eso apoya «muy parecido implica función parecida» como regla fuerte y a la vez muestra que **no es determinista**. El tramo < 40 % tiene sólo 16 pares y no permite concluir.

Los desacuerdos de los tramos altos son en buena parte **sinónimos y no funciones distintas**: *glycogen synthase kinase-3 beta* contra *shaggy* (99,2 % de identidad) es el mismo gen con dos nombres. Por eso la cifra es una **cota inferior de la concordancia de función**, y no sé cuánto. Separar sinónimo de divergencia real exigiría revisión manual o una ontología, y no se hizo.

## Límites declarados
1. **Los nombres de RefSeq ya derivan de homología.** Mide consistencia entre anotaciones, no función demostrada (declarado en el pre-registro).
2. **Desvío:** el `blastp` completo era demasiado lento. Se usó el forward MQ→HV parcial (24.856 consultas, sin la última, que estaba cortada), una submuestra aleatoria de 4.000 (semilla 0) y el reverso sólo para sus mejores hits (3.100 proteínas). Las 24.856 son las primeras por orden del archivo, no una muestra aleatoria del proteoma. No se corrió el par con *N. lugens*.
3. Sólo 1.152 de 4.000 pares fueron recíprocos y con nombre informativo; no se contó cuántos se descartaron por cada motivo.
4. Es un solo par de cicadélidos. No dice nada directo sobre virus.

Tabla: `resultados/concordancia_por_identidad.tsv`. Scripts: `scripts/01_blast_pares.sh` (interrumpido) y `scripts/02_submuestra_reverso.py`.

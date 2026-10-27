# Notas de la línea O3 (ola 6)

Esta línea la corrió la sesión principal, así que `00_meta/` **sí** se actualizó
directamente: `D74` en `DECISIONS.md`, siete entradas nuevas en `PREGUNTAS_ABIERTAS.md` (se
publicaron como 15 a 21 de la ola 6 y se renumeraron a **27 a 33**, porque esos números ya
estaban usados), una en `CAMINOS_PROBADOS.md` y dos filas en `GLOSARIO.md` («región
candidata» y «bloque fabricado por el empalme»). Este archivo queda con lo que es propio del
bloque.

---

## Lo primero: el criterio no lo eligió esta corrida

[`PREREGISTRO.md`](PREREGISTRO.md) §2 fija el criterio de región y se escribió y commiteó
**antes de medir**. Esta sesión empezó a medir con un criterio propio, elegido en paralelo y
sin haber visto el preregistro, y esa primera medición **está descartada**: el criterio
propio corría con cinco referencias y eligió una región que el panel completo veta. El
descarte está documentado en `CAMINOS_PROBADOS.md` y la lección operativa, en
`PREGUNTAS_ABIERTAS.md` 33 (publicada como 21). Donde este bloque se desvía del preregistro, lo dice.

## Las anclas, y por qué la tercera es la que valió la pena

Las tres de `PREREGISTRO.md` §6 corren juntas en `scripts/00_anclas.py`, que devuelve 1 si
alguna falla. Las tres pasan:

1. **Contra `C4`.** El conjunto `epilab` reproduce la tabla de las doce quimeras fila por
   fila, 12 × 17 celdas, en los **dos** modos, después de generalizar el evaluador.
2. **Contra `C13` §5.** El conjunto `vigentes` en modo `corregido` reproduce la tabla
   versionada celda por celda, con las tres sumas que el preregistro nombra, 4 ventanas de
   juntura eficientes y 61 heredadas cambiadas.
3. **Contra el nivel 3 de `C7`.** `ranking.ejes()` da 38/37, 21/20, 35/34 y 21/17.

**La tercera falló al principio y la causa no era la que el preregistro anticipaba.** Él
avisaba que `tools/sifi21_port/ranking.py` lo estaba editando la sesión del issue #30 y que
ahí había que mirar primero. No era eso: el tamizado que vive en `work/sifi_check/` se había
corrido **sin la referencia humana**, y por eso `CP_MRFV` y `ATPaseD_Dm` daban *más*
`buenos_limpios` que los publicados. Regenerado con las seis referencias, los cuatro pares
dan exacto. Dos consecuencias quedan escritas: los `buenos_limpios` publicados de `C7` se
calcularon con la humana adentro, y un insumo incompleto en `work/` —que no se versiona—
falla en la dirección optimista, que es la que no se nota.

Los archivos que se reemplazaron están respaldados en `work/O3/respaldo/`:
`offtarget_full_cinco_refs/` y `offtarget_mm1_<gen>_cinco_refs/`, los cuatro.

**Corregido por `D83` (issue #33).** El diagnóstico de arriba era al revés: el tamizado de
`work/sifi_check/` no estaba incompleto, tenía el panel que `sifi21_reproduccion.md` §4
publica por accesión, y el que leía el directorio equivocado era el ancla C. El nivel 3 de
`C7` vive en `work/sifi_v2/`. El ancla C ahora lee ahí, con los mismos cuatro números
esperados, y `work/sifi_check/offtarget_full/` volvió a su panel. El respaldo que esta nota
menciona no existe en la máquina donde se corrigió: el archivo se reconstruyó con el comando
de §4 y reproduce el `md5` publicado en `tools/sifi21_port/README.md` `[M]`.

## Qué código se tocó, y por qué en el bloque de otro

Cuatro scripts de líneas anteriores recibieron banderas nuevas. **Ninguno cambió su
comportamiento por defecto**, y eso está verificado corriendo cada uno sin las banderas:

| Script | Qué se le agregó | Por qué ahí y no en un script nuevo |
| --- | --- | --- |
| `research/ola3/C13.../scripts/quimeras_v2.py` | `--gen NOMBRE=a-b[:ruta]`, `--nombre`, `--resultados` | Tenía los cuatro genes de EPILAB fijos en la línea 51. El issue #23 pidió generalizarlo y no inventar un script paralelo, porque el ancla contra `C4` vive acá |
| `research/ola3/C13.../scripts/offtarget_ranking.py` | las mismas tres, más `--db` | Comparte las coordenadas con el evaluador. `--db` hacía falta porque el panel estaba fijo en `work/offtarget_db/`, que **no incluye la humana** |
| `research/ola5/N3_marcos/scripts/tres_marcos.py` | `--gen`, `--nota`, `--salida` | Es la herramienta oficial de los tres marcos de `D63`. Medir la región nueva con una cuenta propia habría dado un número sin marco, que es lo que `D63` prohíbe |

`registrar_conjunto` aborta si un conjunto ad hoc intenta llamarse `epilab`, `recomendadas`
o `vigentes`, para que una corrida de prueba no pueda sobreescribir en silencio las
coordenadas publicadas. Y `--resultados` existe porque una corrida de otro bloque no debe
escribir en el registro de `C13`.

**Un bug propio que conviene no repetir.** `02_juntura_detalle.py` imprimía la humana como
si fuera el genoma del vector, porque `ranking.corto()` devuelve el nombre del vector para
cualquier referencia que no esté en `REFERENCIAS`, y `humano_rna` entra sólo cuando se llama
a `ranking_v2.con_panel(sin_humano=False)`. No era cosmético: el vector es **on-target**, así
que un acierto en la humana quedaba clasificado como blanco y no como riesgo. Se detectó
mirando la lista de referencias impresa, donde `D_maidis` aparecía dos veces.

## Confidencialidad

- Ninguna secuencia salió de la máquina. Las seis referencias se leen de disco, el plegado
  corre con el módulo `RNA` local y el tamizado con un autómata en memoria. La referencia
  humana se **bajó** del FTP público del NCBI, que es tráfico entrante: no se subió nada.
- **Ninguna salida de este bloque escribe bases.** `BicC_Dm` es una de las cuatro secuencias
  de EPILAB, y una columna de ventanas solapadas reconstruye el gen: es el incidente de `C9`.
  La auditoría de juntura reporta largo, offset, aporte por gen, hash corto de 12 caracteres
  e identificadores de las secuencias que coinciden.
- El CDS de `V-ATPase B` **no se versiona**, igual que en `O2`: se versiona el generador, y
  el `.gitignore` del bloque rechaza `*.fna`.
- `tools/verificacion/sin_secuencias.py` queda en **6 hallazgos no exceptuados**, que es la
  línea base; los tres archivos que los producen son de `W2` y `C4`, ninguno de acá.

## Entorno

Corrió en la máquina de Santino: Windows 11, `python` 3.13.15 de miniconda, ViennaRNA 2.7.2,
`pyahocorasick`, `numpy`. **Es la misma máquina y la misma versión con las que corrió `C13`**,
verificado en el `comando_run_sifi` de su meta.

Eso corrige, para esta máquina, la tabla de entorno del plan de la ola 6 §3 y del índice
#29, que declaran ausente el módulo `RNA`: esa verificación se hizo en la máquina de
Joaquín. Es la segunda vez en la ola 6 que aplica la regla de `D71`: **antes de declarar una
corrida imposible por entorno hay que decir en cuál máquina**. Lo que sigue faltando acá son
los alineadores —`blastn`, `tblastn`, `makeblastdb`, `miniprot`, `diamond`, `bowtie`—,
también en WSL, así que `F1` (#25) no corre acá y `O2` corrió en la de Luca.

El preregistro fija Python 3.11.17, numpy 2.4.6 y Biopython 1.88, y esta corrida usó 3.13.15.
Es una desviación declarada: las anclas A, B y C pasan igual, y el ancla A dice además que
los números de `C4` no dependen de la versión del intérprete, porque `C4` corrió en 3.11.17.

## Lo que este bloque no puede concluir

- Nada sobre eficacia real: el criterio de eficiencia del port no está validado —en
  hemípteros ρ = +0,142, IC95 [−0,247, +0,492], n = 29— y un resultado in silico es una
  hipótesis sobre eficacia, no una prueba.
- Si una complementariedad incompleta da actividad, las ventanas de juntura no serían
  inútiles sino menos útiles, y no lo sabemos.
- Dónde caen los aciertos con un desapareo: la auditoría localiza coincidencia exacta.
- El veredicto de dos de las 280 ventanas de la región, las que caen sobre las posiciones
  615 y 678, depende de cuál de los dos CDS independientes se use.
- Si la región sobrevive al tamizado del inventario de `M6`, que es previo a llamarla
  recomendada.

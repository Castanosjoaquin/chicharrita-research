# Notas de la línea O3 (ola 6)

Esta línea la corrió la sesión principal, así que `00_meta/` **sí** se actualizó
directamente: `D72` en `DECISIONS.md`, cuatro entradas nuevas en `PREGUNTAS_ABIERTAS.md`
(15 a 18 de la ola 6), una en `CAMINOS_PROBADOS.md` y una fila nueva en `GLOSARIO.md`
(«región candidata»). Este archivo queda con lo que es propio del bloque: qué se verificó
antes de medir, qué código se tocó y por qué, y qué no se puede concluir.

---

## Las anclas, todas antes de leer un número nuevo

Tres, y las tres pasaron:

1. **Contra `C4`.** `quimeras_v2.py --conjunto epilab` reproduce la tabla de las doce
   quimeras de `C4` **fila por fila, 12 × 17 celdas, en los dos modos**, después de la
   generalización. Es lo que el issue #23 pidió conservar y es lo que autoriza a leer los
   números nuevos.
2. **Contra `N3` y `D63`.** La corrida de `tres_marcos.py` que midió la región nueva
   reprodujo en la misma pasada las **seis anclas publicadas** de los tres marcos, incluidas
   las tres de `BicC_Dm` (36/29/26, 35/27/22 y 20/15/17).
3. **Contra `O2`.** El CDS de `V-ATPase B` regenerado en esta máquina da 1.503 nt, 500 aa y
   diez exones, idéntico a lo que reportó `O2` en otra máquina y con otro sistema operativo,
   y el propio extractor aborta si la traducción no reproduce la proteína predicha.

Además, las salidas regeneradas del conjunto `epilab` coinciden con las versionadas: el
refactor no movió ningún número. El `diff` con `core.autocrlf=false` marca esos archivos
como cambiados y es un falso positivo de finales de línea, no un cambio de contenido.

## Qué código se tocó, y por qué en el bloque de otro

Tres scripts de líneas anteriores recibieron la misma generalización, y ninguno cambió su
comportamiento por defecto:

| Script | Qué se le agregó | Por qué ahí y no en un script nuevo |
| --- | --- | --- |
| `research/ola3/C13.../scripts/quimeras_v2.py` | `--gen NOMBRE=a-b[:ruta]`, `--nombre`, `--resultados` | Tenía los cuatro genes de EPILAB fijos en la línea 51. El issue #23 pidió explícitamente generalizarlo y no inventar un script paralelo, porque el ancla contra `C4` vive acá |
| `research/ola3/C13.../scripts/offtarget_ranking.py` | las mismas tres banderas | Comparte las coordenadas con el evaluador: importa `quimeras_v2` para recortar las regiones |
| `research/ola5/N3_marcos/scripts/tres_marcos.py` | `--gen`, `--nota`, `--salida` | Es la herramienta oficial de los tres marcos de `D63`. Medir la región nueva con una cuenta propia habría dado un número sin marco, que es justamente lo que `D63` prohíbe |

`registrar_conjunto` aborta si un conjunto ad hoc intenta llamarse `epilab`, `recomendadas`
o `vigentes`, para que una corrida de prueba no pueda sobreescribir en silencio las
coordenadas publicadas. Y `--resultados` existe porque una corrida de otro bloque no debe
escribir en el registro de `C13`: las salidas de `O3` viven en `O3`.

## Confidencialidad

- Ninguna secuencia salió de la máquina. Las seis referencias se leen de disco, el plegado
  corre con el módulo `RNA` local y el tamizado con un autómata en memoria.
- **Ninguna salida de este bloque escribe bases.** `BicC_Dm` es una de las cuatro secuencias
  de EPILAB, y una columna de ventanas solapadas reconstruye el gen: es el incidente de `C9`.
  La auditoría de juntura reporta largo, offset, aporte por gen, hash corto de 12 caracteres
  e identificadores de las secuencias que coinciden. Para ver una secuencia hay que
  regenerarla.
- El CDS de `V-ATPase B` **no se versiona**, igual que en `O2`: se versiona el generador. Se
  regenera desde el GFF commiteado y el genoma público que ya está en `work/offtarget_db/`,
  sin necesidad de `miniprot`.
- `tools/verificacion/sin_secuencias.py` queda en **6 hallazgos no exceptuados**, que es la
  línea base: los tres archivos que los producen son de `W2` y `C4` y ninguno es de acá.

## Entorno, y la corrección que conviene registrar

Corrió en la máquina de Santino: Windows 11, `python` 3.13.15 de miniconda, ViennaRNA 2.7.2,
`pyahocorasick`, `numpy`. **Es la misma máquina y la misma versión con las que corrió `C13`**,
verificado en el `comando_run_sifi` del meta de `C13`.

Eso corrige, para esta máquina, la tabla de entorno del plan de la ola 6 §3 y del issue #29,
que declaran ausente el módulo `RNA` de ViennaRNA: la verificación de esa tabla se hizo en la
máquina de Joaquín. La regla que `D71` ya dejó escrita se confirma una segunda vez: **antes de
declarar una corrida imposible por entorno hay que decir en cuál máquina**. Lo que sigue
faltando acá son los alineadores —`blastn`, `tblastn`, `makeblastdb`, `miniprot`, `diamond`,
`bowtie`—, también en WSL, así que `F1` (#25) no corre en esta máquina y `O2` corrió en la de
Luca.

Tiempos: perfil del CDS entero 10 s, cada tamizado del panel de seis 70 s, la auditoría de
juntura 90 s, los tres marcos menos de 1 s.

## Lo que este bloque no puede concluir

- Nada sobre eficacia real: el criterio de eficiencia del port no está validado y un
  resultado in silico es una hipótesis sobre eficacia, no una prueba.
- Si una complementariedad incompleta da actividad, las ventanas de juntura no serían
  inútiles sino menos útiles, y no lo sabemos `[?]`.
- Dónde caen los dos aciertos con un desapareo en maíz: la auditoría localiza coincidencia
  exacta de 19 a 21 nt y de esos dos tiene la cuenta, no el bloque `[?]`.
- Si la región candidata sobrevive al tamizado del inventario de `M6`, que es previo a
  llamarla recomendada (`D70`, issue #30).

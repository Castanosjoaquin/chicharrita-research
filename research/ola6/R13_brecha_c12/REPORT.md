# La brecha con `C12` no está en la medición: está en cómo se decide que dos nombres son el mismo

**Veredicto: los 6,5 puntos que separan el 78,2 % de `C12` del par completo los explica
enteramente el normalizador de nombres —aporta +7,0 puntos—; el alineador aporta +0,2 y el
protocolo −0,7. `C12` no midió mal: midió con una regla más estricta para decidir cuándo dos
nombres son el mismo nombre, y esa regla contaba «kelch-like protein diablo isoform X1» contra
«kelch-like protein diablo» como un desacuerdo de anotación.** Pregunta abierta **62**, abierta
por `D86` al cerrar `F1` (issue #25). Método y criterio: `PREREGISTRO.md` (commit `283b888`,
anterior a la primera corrida) y su Enmienda 1. Fecha: 2026-10-27. **No se corrió ningún
alineamiento nuevo**: todo sale de los TSV que ya estaban en disco.

## Cómo se separó

*M. quadrilineatus* contra *H. vitripennis*, siempre los mismos dos proteomas. Tres pasos, cada uno
cambiando **una sola cosa**, y todos con la misma regla de reciprocidad —el mejor hit del mejor
hit— y el mismo normalizador, el de `F1`:

| paso | alineador | protocolo | concordancia | pares |
| --- | --- | --- | --- | --- |
| `C12` publicado | BLAST+ | submuestra de 4.000 | 78,2 % | 1.152 |
| **A** | BLAST+ (los TSV de `C12`) | el de `C12` | **85,2 %** | 1.081 |
| **B** | `diamond` | el de `C12` | **85,4 %** | 1.122 |
| **C** | `diamond` | par completo | **84,7 %** | 8.534 |

La descomposición sale de restar pasos contiguos:

```
brecha +6,45 pp  =  normalizador +7,00  +  alineador +0,18  +  protocolo −0,73
```

El **paso A es la réplica de `C12`**: los mismos alineamientos, el mismo recorte, el mismo criterio
de reciprocidad, cambiando **sólo** el normalizador. Reconstruye 1.081 de sus 1.152 pares —dentro
del ±10 % que el preregistro fijó como control— así que la réplica es fiel y la atribución es
interpretable. Por el criterio preregistrado, un componente que explique ≥ 2/3 de la brecha se la
lleva: el normalizador explica el **109 %**.

## Qué hace el normalizador, exactamente

Sobre esos 1.081 pares recíprocos (`resultados/patrones_normalizador.json`):

| | acuerdos | concordancia |
| --- | --- | --- |
| comparando el producto de RefSeq tal cual (sólo minúsculas) | 406 | 37,6 % |
| con el normalizador de `F1` | 921 | **85,2 %** |

Convierte 515 desacuerdos en acuerdos y **no rompe ninguno** (0 pares pasan de acuerdo a
desacuerdo). De esos 515:

| qué los separaba | pares | |
| --- | --- | --- |
| sufijo de isoforma (`isoform Xn`) | 401 | 77,9 % |
| sufijo `-like` | 111 | 21,6 % |
| `homolog` | 2 | 0,4 % |
| otro | 1 | 0,2 % |

Ejemplos reales: *kelch-like protein diablo isoform X1* contra *kelch-like protein diablo*;
*ankyrin-3-like isoform X2* contra *ankyrin-3-like isoform X8*; *protein adenylyltransferase
Fic-like isoform X1* contra *protein adenylyltransferase Fic*. **Ninguno es un desacuerdo sobre
qué hace el gen.**

## Qué se hace con esto, y qué no

Lo decidió el preregistro antes de ver el número, y el resultado cayó en la rama «la causa es el
normalizador»:

- **La tabla de `C12` no se toca ni se recalcula.** Sus bandas son correctas **para su propio
  normalizador**. Reescribirlas sería borrar el registro de lo que se publicó.
- **Lo que se corrige es el acople**: `F1` adjunta las bandas de `C12` a pares cuyos nombres
  normaliza con **otra** regla, más inclusiva. Eso hace que la banda que viaja con cada anotación
  **subdeclare** la concordancia que mediría el propio criterio de `F1`, en unos 7 puntos. Queda
  anotado en el informe de `F1` y en el de `C12`, con un puntero a este.
- **Esto cierra el círculo con `D86`.** Allí el esperado sobre `GITV01` daba 81,2 % con las bandas
  de `C12` y 88,5 % con las bandas medidas de nuevo: 7,3 puntos, que es casi exactamente lo que
  aporta el normalizador acá. Las dos mediciones, hechas por caminos distintos, dan el mismo
  número para la misma causa.
- **El 81 % de `F1` sigue publicado y sigue sin corregirse hacia arriba**, por `D86`. Esto explica
  por qué es conservador; no lo mueve.

## Lo que esto no dice

- **No reconstruye el normalizador de `C12`.** Su código nunca se versionó. Medimos qué pasa al
  aplicar el de `F1` a sus pares, no cuál era el suyo; del suyo sólo sabemos que dejaba pasar como
  desacuerdos los sufijos de isoforma y `-like`, porque si no, no habría diferencia.
- **No dice cuál de los dos normalizadores es el correcto.** Dice que la diferencia entre los dos
  es de 7 puntos y de qué está hecha. Que *isoform X1* contra *isoform X8* no sea un desacuerdo de
  función es un juicio, defendible y no medido acá.
- **No separa el alineador de nada más que no esté en los TSV.** Los dos sumandos chicos
  (+0,18 y −0,73) salen de archivos ya existentes; cualquier diferencia de parámetros o de versión
  de base entre las dos corridas viaja dentro de ellos.
- **No valida ninguna anotación contra verdad experimental.** Igual que `C12` y que `D86`, mide
  consistencia entre anotaciones de RefSeq que ya derivan de homología.
- **No toca el diseño ni el ranking.** Rige `D37`.

## Cómo reproducirlo

```bash
# los TSV de C12 y los de diamond de D86 ya estan en work/; no se corre ningun alineamiento
python research/ola6/R13_brecha_c12/scripts/descomponer.py
python research/ola6/R13_brecha_c12/scripts/patrones_normalizador.py
```

Salidas: `resultados/descomposicion.json` (los tres sumandos, el control de réplica y el
veredicto), `resultados/bandas_por_paso.tsv` (una fila por paso × banda, con IC95 de Wilson) y
`resultados/patrones_normalizador.json`. Ninguna lleva secuencia.

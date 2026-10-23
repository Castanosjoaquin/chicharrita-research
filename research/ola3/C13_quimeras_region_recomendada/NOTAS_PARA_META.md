# Notas de la línea C13 (ola 3)

A diferencia de C4, esta línea la corrió la sesión principal, así que `00_meta/` **sí** se
actualizó directamente: D43 en `DECISIONS.md`, dos entradas en `CAMINOS_PROBADOS.md`, tres en
`PREGUNTAS_ABIERTAS.md` y una en `GLOSARIO.md`. Este archivo queda con lo que es propio del
bloque: versiones, verificaciones, confidencialidad y qué salidas sirven.

---

## Qué verifica esta línea antes de medir nada nuevo

Tres anclas, las tres pasaron:

1. **Contra C4.** `quimeras_v2.py --conjunto epilab` reproduce la tabla de las 12 quimeras de
   C4 **fila por fila, 12 × 17 celdas, en los dos modos** (`fiel` y `corregido`). Corre en
   Python 3.13.15 contra el 3.11.17 de C4, así que el resultado también dice que esos números
   no dependen de la versión del intérprete.
2. **Contra W7.** El conteo de eficientes del gen completo en modo `corregido` da 123, 30, 171
   y 29, que es lo que `tools/sifi21_port/ranking_v2.py` fija como ancla.
3. **Contra C7 y D25.** El conteo en contexto de cada región recomendada da 38, 21, 36 y 21.

Si alguna falla, los scripts abortan en vez de seguir.

## Versiones

Python 3.13.15, ViennaRNA 2.7.2 (backend `vienna`), numpy 2.5.4, `pyahocorasick`. El backend
`exe` no se pudo usar: necesita el RNAplfold 2.1.5 que instala si-Fi21 en Windows, que no está
en esta máquina. Es la misma limitación declarada por C4.

Port de si-Fi21 usado **sin modificar**; md5 al cierre de esta línea:

| Archivo | md5 |
| --- | --- |
| `run_sifi.py` | 148eaeee3704f1adb9ca4a0d7c9af63a |
| `sifi_core.py` | 98669b877342cab8b07748994ac286f4 |
| `sifi_energy.py` | 81bc18c520e7f48920ce78e03074e5d1 |
| `offtarget_21nt.py` | 58e8c573f1977288601a7b8a1a20f13c |
| `ranking.py` | 87bab9349348dcef94daff23d197482e |

`ranking.py` se **importó** para usar `ejes()` y `pesos_base()`; no se modificó. Lo que C13
construye distinto es la matriz de riesgo que se le pasa, para poder tratar el genoma del
vector por ventana en una quimera mixta.

## Qué salida mirar

Tres conjuntos de regiones conviven en `resultados/`. El que vale para el entregable es
**`vigentes`** (`BicC_Dm` en 922-1221, por D25):

| Sufijo | Qué es | Para qué sirve |
| --- | --- | --- |
| `epilab_*` | las cuatro regiones como las eligió EPILAB | sólo verificación contra C4; no leer como resultado |
| `recomendadas_*` | las de C7 nivel 3 (`BicC_Dm` 2121-2420) | el conjunto anterior a D25; se deja porque tiene el tamizaje completo |
| `vigentes_*` | las vigentes hoy | **el resultado de esta línea** |

Y dentro de cada uno, `_corregido_vienna` es el modo del ranking y `_fiel_vienna` el modo que
reproduce al programa original. Los dos están medidos y no dan lo mismo.

## Confidencialidad

Las cuatro secuencias de EPILAB se procesaron sólo con herramientas locales: el port y el
tamizaje leen de disco y las seis referencias están en `work/offtarget_db/`. **Ninguna
secuencia salió de la máquina.** Las dos búsquedas web de esta línea fueron sobre el *nombre*
de la técnica, sin pegar secuencia. Los originales de `YHat-Biotech/` no se tocaron: todo el
trabajo se hizo sobre `work/C13/`, recortando de `work/sifi_check/<gen>_full.fasta`.

## Rechazos del filtro de seguridad

Ninguno.

## Contenido que intentó redirigirnos

Ninguno. Las dos búsquedas web devolvieron resúmenes y títulos; se trataron como dato.

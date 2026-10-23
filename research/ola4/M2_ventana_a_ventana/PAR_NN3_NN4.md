# M2 — el par `RNA_NN3` contra `RNA_NN4`, que era el insumo que faltaba

Complemento del `REPORT.md` de M2 (issue #6). Va aparte y no dentro del informe porque el
informe lo escribió otra sesión; **conviene integrarlo ahí y borrar este archivo.**

## 1. Por qué estaba pendiente, y por qué ya no

De los cuatro pares que pide M2, tres se podían armar con TSV ya publicados. Éste no:
`RNA_NN4` es la tabla de apilamiento propia de `sifi21INTA` y **la única que no sale de
Biopython**, así que sin el fuente del INTA en la máquina no había de dónde sacarla. Quedó
declarado como insumo faltante y no como pregunta para el investigador, que era la lectura
correcta.

El fuente estaba en esta máquina, en `work/C2/sifi21INTA/` —archivos del 2024-03-27, que
es la fecha de la cabeza de `main` del commit `92df4449` que documenta M0—, junto con el
original (`work/C2/sifi21_orig/`) y un fork. `work/` no se versiona, y por eso no aparecía
en el clon de nadie.

La tabla se transcribió al port como `sifi_energy.RNA_NN4`, **verificada celda por celda**
contra `freeEnergy.py:61-74`: mismas 28 claves, ningún valor distinto `[M]`. El port suma
`--tabla-nn {NN1,NN2,NN3,NN4}`, con `NN3` por defecto, que es la del original.

**Atribución, con su salvedad:** el comentario del fuente la asigna a Zuber *et al.* (2022),
*Nucleic Acids Research* 50(9):5251-5262. **El artículo no se abrió**, así que la
atribución está identificada pero no verificada contra su fuente `[?]`, igual que ya estaba
anotado en `PREGUNTAS_ABIERTAS.md`. Lo que sí está verificado es que difiere de `RNA_NN3`
en **22 de sus 28 entradas** `[M]`: no es un retoque menor y no se puede aproximar con la
tabla de Biopython.

## 2. El resultado: la tabla explica toda la diferencia con `sifi21INTA`

| Gen | NN3 (original) | NN4 (INTA) | Ventanas que cambian |
|---|---|---|---|
| `MP_MRFV` | 142 | **138** | 4 |
| `CP_MRFV` | 39 | **40** | 1 |
| `BicC_Dm` | 223 | **218** | 9 |
| `ATPaseD_Dm` | 35 | **35** | 0 |

`[M]`, modo fiel, `--backend vienna`, `resultados/par_nn3_nn4_resumen.json`.

**138, 40, 218 y 35 es exactamente lo que `entregables/critica-herramientas.md` declara
para `sifi21INTA` con sus valores por defecto.** O sea que el port, cambiándole sólo la
tabla de apilamiento, reproduce los cuatro conteos de la implementación del INTA. La
diferencia entre las dos implementaciones **es la tabla**, y no queda nada por explicar en
ese eje `[M]`.

Eso cierra la pregunta que el entregable dejaba abierta en ese párrafo: «con tres
implementaciones del mismo criterio dando tres números distintos, lo que falta saber es qué
versión corriste y con qué umbral de extremos». Dos de los tres números ya están
reconciliados entre sí; el que sigue sin explicarse es el de la planilla (114, 35, 199, 33),
que es de lo que se ocupó M1.

## 3. Por dónde cruza, que es lo que M2 pide

Las **33** ventanas que cambian de clase, sumando los cuatro genes y los dos modos, cruzan
**todas** por el mismo término: `end_stability`, y por consecuencia `thermo_efficient`
`[M]`. Ninguna cruza por selección de hebra ni por accesibilidad.

Tres cosas que lo confirman y que no son obvias de un conteo:

- **La accesibilidad no se mueve en absoluto:** el delta es exactamente `0.000000` en las
  33 `[M]`. Es lo que tiene que pasar —la tabla entra en el cálculo de ΔG y no en
  RNAplfold— y sirve como control de que el cambio de tabla no se filtró a otro término.
- **Todas cruzan el umbral de 1,0**, con `ddg` entre 0,7117 y 1,2364: cada ventana tiene su
  `ddg` de un lado del corte con NN3 y del otro con NN4 `[M]`. No son ventanas cualesquiera,
  son las que estaban al borde.
- **No es unidireccional:** 24 pierden la condición de eficiente al pasar a NN4 y **9 la
  ganan** `[M]`. Por eso el conteo de `CP_MRFV` sube de 39 a 40 mientras los otros bajan, y
  por eso `ATPaseD_Dm` no se mueve en modo fiel aunque sí tenga una ventana que cambia en
  corregido.

## 4. Verificación

- La tabla transcrita es idéntica a la del fuente, celda por celda `[M]`.
- **El default no cambió nada:** con `NN3`, los cuatro genes en los dos modos reproducen el
  ancla publicada de C9 con **cero discrepancias** sobre las 4.722 ventanas `[M]`. El flag
  nuevo no tocó el camino de código que ya estaba verificado.
- Los TSV con NN4 llevan sufijo `_nn4`, así que no pisan los nombres de los que ya están
  publicados.

## 5. Reproducir

```sh
python3 tools/sifi21_port/run_sifi.py <fasta...> --modo fiel --backend vienna --salida /tmp/nn3
python3 tools/sifi21_port/run_sifi.py <fasta...> --modo fiel --backend vienna --salida /tmp/nn4 --tabla-nn NN4
python3 research/ola4/M2_ventana_a_ventana/scripts/comparar_nn3_nn4.py \
        --nn3 /tmp/nn3 --nn4 /tmp/nn4 --salida research/ola4/M2_ventana_a_ventana/resultados
```

Hay que repetirlo con `--modo corregido` para completar las ocho combinaciones. Salidas:
`par_nn3_nn4_resumen.json` y `par_nn3_nn4_cambios.tsv`, con una fila por ventana que
cambia, el término que cruzó y los cuatro términos continuos de los dos lados.

## 6. Lo que este par deja planteado

- **La comparación es contra el port con otra tabla, no contra `sifi21INTA` corriendo.** Que
  los cuatro conteos coincidan con los suyos es evidencia fuerte de que la tabla explica la
  diferencia, pero no es lo mismo que haber corrido su código y comparado ventana por
  ventana. Correrlo es posible —el fuente está— y sería el control definitivo `[H]`.
- **El eje de la tabla no estaba en ningún barrido.** C9 barrió umbrales con una sola tabla
  y M1 barrió bases con un solo motor; la tabla de apilamiento es un tercer eje que mueve
  los conteos entre −5 y +1 por gen. Conviene decirlo cuando se presente cualquier conteo
  como propiedad del gen.

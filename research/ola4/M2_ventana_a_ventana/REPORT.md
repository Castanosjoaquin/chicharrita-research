# M2 — Comparador ventana por ventana

Línea M2 de la ola 4 (issue #6). Diego lo pidió textualmente: «sería útil comparar cuáles
son las ventanas específicas que cambian de clasificación, en lugar de considerar
únicamente el conteo final» `[R]`.

**Estado: tres de los cuatro pares corridos. El cuarto no, y está declarado, no en cero.**

## 1. La herramienta

`scripts/comparar_ventanas.py` toma dos perfiles por ventana del port y devuelve la matriz
de confusión, la lista de posiciones que cambian de clase y, para cada una, **cuál de los
cuatro booleanos del veredicto cambió** y cuánto se movieron los cuatro términos continuos.
`scripts/correr_pares.py` lo aplica a los pares y deja todo en `resultados/`.

El alineamiento de posiciones es un parámetro (`--offset-b`) porque el par de recorte no
compara la misma secuencia: la ventana que en el gen empieza en 922 es la 1 del recorte.
Las posiciones que no existen de los dos lados se informan aparte y no entran a la matriz
—en el recorte son las 20 últimas posiciones de inicio, que el gen tiene y la molécula no—.

## 2. Par 1 — `fiel` contra `corregido`

| Gen | fiel | corregido | Cambian |
|---|---|---|---|
| `MP_MRFV` | 142 | 123 | 19 |
| `CP_MRFV` | 39 | 30 | 9 |
| `BicC_Dm` | 223 | 171 | 52 |
| `ATPaseD_Dm` | 35 | 29 | 6 |

`[M]`, `--backend vienna`.

**Ningún booleano del veredicto cambia en ninguna de las 86 ventanas** `[M]`. Es el
resultado más informativo del par y no se ve en un conteo: los cuatro términos
—selección de hebra, estabilidad de extremos, accesibilidad y el veredicto termodinámico—
son idénticos entre los dos modos. Lo que cambia es **cómo la regla terminal los combina**.

Por eso el par sólo se vuelve interpretable con la columna `rama_terminal` que agregó M3
(D54), y con ella las dos afirmaciones estructurales de `CAMBIOS.md` C1 quedan
reproducidas con herramienta:

- **Las 86 ventanas caen todas en la rama 2**, el atajo que decide mirando sólo la
  accesibilidad `[M]`. Ninguna en las ramas 1, 3 o 4.
- **Las 86 van en la misma dirección**: eficientes en fiel y no en corregido. Ninguna al
  revés `[M]`. Era lo esperado —la rama del original sólo puede agregar eficientes— y
  ahora está medido sobre el conjunto completo.

### Sobre el criterio de terminado

El issue pide que este par dé **19, 7, 50 y 8**. Da 19, 9, 52 y 6. **No es una
discrepancia: es otro motor.** Los números del issue salen de `CAMBIOS.md` C1, medidos con
RNAplfold 2.1.5 (`--backend exe`); éstos son con ViennaRNA 2.7.2, que es el único motor
disponible en esta máquina (§4). El total pasa de 84 a 86 ventanas.

## 3. Par 2 — `RNA_NN3` contra `RNA_NN4`

| Gen | NN3 (original) | NN4 (INTA) | Cambian |
|---|---|---|---|
| `MP_MRFV` | 142 | **138** | 4 |
| `CP_MRFV` | 39 | **40** | 1 |
| `BicC_Dm` | 223 | **218** | 9 |
| `ATPaseD_Dm` | 35 | **35** | 0 |

`[M]`, modo fiel, `--backend vienna`.

Este par estaba bloqueado por un insumo y no por una pregunta: `RNA_NN4` es la tabla de
apilamiento propia de `sifi21INTA` y **la única que no sale de Biopython**. El fuente
estaba en esta máquina, en `work/C2/sifi21INTA/` —archivos del 2024-03-27, la fecha de la
cabeza de `main` del commit `92df4449`—, que no se versiona y por eso no aparecía en
ningún clon. La tabla se transcribió al port como `sifi_energy.RNA_NN4`, **verificada
celda por celda** contra `freeEnergy.py:61-74`: mismas 28 claves, ningún valor distinto
`[M]`. El port suma `--tabla-nn {NN1,NN2,NN3,NN4}`, con `NN3` por defecto.

**Atribución, con su salvedad:** el comentario del fuente la asigna a Zuber *et al.* (2022),
*Nucleic Acids Research* 50(9):5251-5262. **El artículo no se abrió**, así que la
atribución está identificada pero no verificada `[?]`, como ya estaba anotado en
`PREGUNTAS_ABIERTAS.md`. Sí está verificado que difiere de `RNA_NN3` en **22 de sus 28
entradas** `[M]`: no es un retoque menor y no se puede aproximar con la de Biopython.

### Lo que el par cierra

**138, 40, 218 y 35 es exactamente lo que `entregables/critica-herramientas.md` declara
para `sifi21INTA` con sus valores por defecto.** Cambiándole sólo la tabla, el port
reproduce los cuatro conteos de la implementación del INTA: la diferencia entre las dos
implementaciones **es la tabla**, y en ese eje no queda nada por explicar `[M]`. El número
que sigue sin reconciliar es el de la planilla (114, 35, 199, 33), que es de lo que se
ocupó M1.

### Por dónde cruza

Las 14 ventanas cruzan **todas** por `end_stability`, y ninguna por selección de hebra ni
por accesibilidad `[M]`. Tres controles:

- **La accesibilidad no se mueve ni una milésima:** delta exactamente `0.000000` en las 14.
  Es lo que debe pasar si la tabla entra en el ΔG y no en RNAplfold, y sirve para descartar
  que el cambio se haya filtrado a otro término.
- **Todas cruzan el umbral de 1,0**, con `ddg` entre 0,7117 y 1,2364: son las ventanas que
  estaban al borde, no ventanas cualesquiera.
- **No es unidireccional:** de las 14, **11 pierden la condición con NN4 y 3 la ganan**
  `[M]`, que es por qué `CP_MRFV` sube de 39 a 40 mientras los otros bajan. Corrido también
  en modo `corregido`, el par da 33 ventanas en total con 24 que pierden y 9 que ganan; esa
  corrida está en el commit anterior de esta línea y no se repite acá porque el modo que
  compara contra `sifi21INTA` es el fiel.

## 4. Par 3 — RNAplfold 2.1.5 contra ViennaRNA 2.7.2: **no corrido**

El backend `exe` del port invoca el `RNAplfold.exe` que trae el instalador de si-Fi2015,
que es un binario de Windows. En esta máquina no hay ningún RNAplfold —sólo ViennaRNA
2.7.2 como módulo de Python— y **ninguno de los 31 TSV por ventana versionados es `_exe`**:
todos son `_vienna` `[M]`.

Compilar ViennaRNA 2.1.5 desde fuente no sirve como control: lo que el criterio pide es
reproducir números medidos con **ese** binario, y otra compilación probaría otra cosa.

**Qué haría falta:** el binario, o los TSV por ventana con backend `exe` de los cuatro
genes. Cualquiera de los dos cierra este par y además permite correr los controles exactos
de §2 y §5 con el motor en que fueron medidos. La máquina que corrió M1 lo tiene.

Queda declarado como **no corrido**, no como resultado nulo.

## 5. Par 4 — región recortada contra región en contexto

Modo `corregido`, que es el de las anclas del ranking.

| Gen | En contexto | Recortada | Comparadas | Cambian |
|---|---|---|---|---|
| `MP_MRFV` | 31 | 27 | 180 | 6 |
| `CP_MRFV` | 20 | 23 | 180 | 9 |
| `BicC_Dm` | 29 | 26 | 280 | 3 |
| `ATPaseD_Dm` | 17 | 20 | 280 | 5 |

`[M]`. Los conteos de las dos primeras columnas son **sobre las posiciones comunes**, que
son 180 o 280 según el largo de la región: excluyen las 20 últimas posiciones de inicio
que el recorte no tiene. No son las cifras publicadas de la región, que se cuentan sobre
las 200 o 300 posiciones completas del gen (§6).

**Reproduce las doce celdas de C13 §4, celda por celda** `[M]`: 6, 9, 3 y 5 flips, con la
misma dirección en los cuatro genes —5/1, 3/6, 3/0 y 1/4 entre las que pierden y las que
ganan—. Es el control que el issue pide para este par, y pasa.

### Por dónde cruza, que es lo que C13 no decía

C13 reportaba la distancia al borde; el comparador agrega el término. De las 23 ventanas,
**22 cruzan por `target_site_accessibility`** y **1 por `end_stability`**, en `BicC_Dm`
`[M]`.

Las 22 son el efecto de borde de plegado, que es la explicación que C13 daba y que ahora
queda atribuida término por término. La de `end_stability` es distinta y vale la pena
señalarla: el ΔG de una ventana no depende del contexto, salvo en las dos primeras del
recorte, donde el motor usa `_ends_plain` en vez de los extremos colgantes porque no
existe el siRNA de dos posiciones antes. O sea que el recorte mueve un término más que el
de la accesibilidad, aunque sea en una sola ventana `[H]`.

### El número del criterio de terminado, corregido

El issue pide «27 cambios de veredicto por borde en las cuatro regiones». Son **23** con
las regiones vigentes `[M]`. Los 27 son del conjunto `recomendadas`, donde `BicC_Dm` es
2121-2420; con las vigentes, donde D25 la movió a 922-1221, son 23. La corrección es la
misma que ya había detectado la sesión que escribió este issue, y esta medición
independiente la confirma.

## 6. Controles

- **El ancla de C9 se reproduce en los 8 casos** (cuatro genes por dos modos) antes de
  comparar nada: 142/39/223/35 en fiel y 123/30/171/29 en corregido. El driver aborta si
  alguna falla `[M]`.
- **Las cuatro anclas de región de C7 se reproducen** contando las posiciones completas de
  cada región vigente: 38, 21, 36 y 21 `[M]`. Es lo que valida que las coordenadas usadas
  son las correctas, y lo que explica la diferencia con la tabla de §5.
- El par 2 se corrió con la tabla transcrita y el par 1 con el default, de modo que los dos
  comparten el mismo perfil de `fiel`: los 142/39/223/35 de la columna izquierda de §2 son
  los mismos de §2 del par 1.

## 7. Reproducir

```sh
python3 research/ola4/M2_ventana_a_ventana/scripts/correr_pares.py
```

Genera los insumos con el port, verifica las anclas, corre los tres pares y escribe
`resultados/`: un `parN_*_resumen.json` y un `parN_*_cambios.tsv` por gen y por par, más
`pares_resumen.json` con todo junto y el par 3 declarado. Necesita `ViennaRNA` y
`biopython` por pip.

Para un par suelto:

```sh
python3 research/ola4/M2_ventana_a_ventana/scripts/comparar_ventanas.py \
        --a <tsv_a> --b <tsv_b> --etiquetas fiel,corregido --salida <prefijo>
```

## 8. Lo que queda

- **El par 3**, que necesita el binario (§4).
- **Los dos controles exactos del issue** —19/7/50/8 y las doce celdas en el motor en que
  fueron medidas— por lo mismo. Con ViennaRNA 2.7.2 el par de modos da 19/9/52/6 y el de
  recorte reproduce las doce celdas, así que el control estructural pasa y el numérico
  espera al binario.
- **El comparador está listo para la salida por ventana de Diego**, que es la tercera tarea
  del issue: es la misma herramienta, con `--etiquetas nuestro,suyo`. Lo que falta de ahí es
  el archivo, que es el pedido 1 del lunes.

# M2 — Comparador ventana por ventana

Línea M2 de la ola 4 (issue #6). Diego lo pidió textualmente: «sería útil comparar cuáles
son las ventanas específicas que cambian de clasificación, en lugar de considerar
únicamente el conteo final» `[R]`.

**Estado: los cuatro pares corridos y los dos controles del criterio de terminado en verde.**
El par de motores necesitaba un binario que no estaba en esta máquina; se resolvió
compilando ViennaRNA 2.1.5 desde el fuente oficial y verificando que equivale al del
instalador (§4).

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

### El criterio de terminado, en los dos motores

El issue pide que este par dé **19, 7, 50 y 8**. Con ViennaRNA 2.7.2 da 19, 9, 52 y 6, y
con RNAplfold 2.1.5 da **19, 7, 50 y 8 exactos** `[M]`
(`resultados/control_modos_exe_*`). No había discrepancia: los números del criterio salen
de `CAMBIOS.md` C1, que se midió con 2.1.5, y el control pasa en cuanto se corre en el
motor en que fue medido.

Las dos propiedades estructurales se sostienen en los dos motores: con 2.1.5 son **84**
ventanas —las mismas que cita D53— y con 2.7.2 son 86, y en los dos casos **todas caen en
la rama 2 y todas van en la misma dirección** `[M]`.

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
- **No es unidireccional:** de las 14 de modo fiel, **11 pierden la condición con NN4 y 3
  la ganan** `[M]`, que es por qué `CP_MRFV` sube de 39 a 40 mientras los otros bajan.

El par se corrió también en modo `corregido`, donde da 5, 2, 11 y 1 ventanas: **33 en total
entre los dos modos, 24 que pierden y 9 que ganan** `[M]`
(`resultados/par2_tablas_{fiel,corregido}_*`). En corregido los conteos pasan de 123, 30,
171 y 29 a 118, 30, 168 y 30, así que la tabla mueve el resultado en los dos modos y no
sólo en el que reproduce al original.

## 4. Par 3 — RNAplfold 2.1.5 contra ViennaRNA 2.7.2

| Gen | 2.1.5 | 2.7.2 | Cambian |
|---|---|---|---|
| `MP_MRFV` | 133 | 142 | 21 |
| `CP_MRFV` | 32 | 39 | 15 |
| `BicC_Dm` | 212 | 223 | 53 |
| `ATPaseD_Dm` | 42 | 35 | 15 |

`[M]`, modo fiel. Los conteos de la izquierda son los cuatro números que la ola 2 verificó
contra el programa original.

### Cómo se corrió fuera de Windows, y por qué el control es válido

El backend `exe` del port invoca el `RNAplfold.exe` del instalador de si-Fi2015, que es un
binario de Windows y no está en esta máquina. Pero ese binario **es ViennaRNA 2.1.5**, así
que se compiló esa versión desde el tag `v2.1.5` del fuente oficial y se apuntó el port con
la variable de entorno `SIFI_RNAPLFOLD`.

**Que la compilación equivalga al binario del instalador no se asume: se verifica**, y con
dos anclas independientes que el script comprueba antes de comparar nada:

- los cuatro conteos publicados, **133, 32, 212 y 42** en fiel y **114, 25, 162 y 34** en
  corregido `[M]`;
- el control del criterio de terminado, **19, 7, 50 y 8** `[M]`.

Los dos pasan exactos, y el script aborta si alguno falla. Esa es la razón por la que el
par vale: una compilación que reproduce los seis números publicados no es «otro binario»,
es el mismo programa.

La receta está en el encabezado de `scripts/correr_pares.py`. Lo único no obvio es que el
código es C89 con `register i;` sin tipo, que los clang modernos rechazan, así que hay que
compilar con `-Wno-implicit-int` y compañía; y que el repo no trae `configure`, sólo
`configure.ac`, de modo que hace falta `autoreconf -i` con autoconf, automake, libtool y
gengetopt.

### Por dónde cruza

Las **104** ventanas que cambian cruzan **todas** por `target_site_accessibility` `[M]`, que
es exactamente lo que tiene que pasar: entre versiones de ViennaRNA lo que cambia es el
cálculo de accesibilidad, y ni la selección de hebra ni la estabilidad de extremos dependen
de él.

Dos detalles que el conteo no muestra:

- **18 de las 104 cambian de veredicto sin que cambie `thermo_efficient`** `[M]`. Son
  ventanas de la rama 2, el atajo: como ahí el veredicto lo decide sólo la accesibilidad, un
  cambio en ese término mueve la clasificación aunque el veredicto termodinámico quede
  igual. Es el mismo mecanismo que mide el par 1, visto desde el otro eje.
- **No es unidireccional:** 62 son eficientes sólo con 2.7.2 y 42 sólo con 2.1.5 `[M]`. Por
  eso `ATPaseD_Dm` baja de 42 a 35 mientras los otros tres suben.

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
- **El binario compilado reproduce las dos anclas del backend `exe`** antes de correr el par
  3: los cuatro conteos publicados y el control de 19, 7, 50 y 8. El script aborta si alguna
  falla (§4).
- El par 2 se corrió con la tabla transcrita y el par 1 con el default, de modo que los dos
  comparten el mismo perfil de `fiel`: los 142/39/223/35 de la columna izquierda de §2 son
  los mismos del par 1.
- **La herramienta tiene 17 verificaciones sobre insumos sintéticos**, en
  `scripts/test_comparar.py`, que corren sin el corpus y sin el motor: la aritmética de la
  matriz, la atribución de cada término a su corte, el alineamiento con `--offset-b` y cinco
  modos de fallar en silencio `[M]`. Dos de esas cinco cerraron huecos reales del comparador:
  una posición repetida en el TSV pisaba a la anterior y bajaba el conteo sin avisar, y un
  `is_efficient` que no fuera `True`/`False` —un 1/0, por ejemplo— daba cero eficientes de
  los dos lados con la matriz cerrando igual. Las dos abortan ahora. Las guardas no cambian
  ninguna salida publicada: se verificó corriendo la versión anterior y la actual sobre los
  cuatro genes, en el par de modos y en el de recorte con desplazamiento, con salida idéntica.

## 7. Reproducir

```sh
SIFI_RNAPLFOLD=/ruta/a/ViennaRNA/Progs/RNAplfold \
    python3 research/ola4/M2_ventana_a_ventana/scripts/correr_pares.py
```

Genera los insumos con el port, verifica las anclas, corre los cuatro pares y escribe
`resultados/`: un `parN_*_resumen.json` y un `parN_*_cambios.tsv` por gen y por par, más
`pares_resumen.json` con todo junto. Necesita `ViennaRNA` y `biopython` por pip, y el
binario de 2.1.5 para el par 3; sin `SIFI_RNAPLFOLD` corre los otros tres y declara ese
par como no corrido.

Para un par suelto:

```sh
python3 research/ola4/M2_ventana_a_ventana/scripts/comparar_ventanas.py \
        --a <tsv_a> --b <tsv_b> --etiquetas fiel,corregido --salida <prefijo>
```

Y las verificaciones de la herramienta, que no necesitan ni el corpus ni el motor:

```sh
python3 research/ola4/M2_ventana_a_ventana/scripts/test_comparar.py
```

## 8. Lo que queda

Nada de esta línea. Las tres tareas del issue están hechas y los dos controles del criterio
de terminado pasan en el motor en que fueron medidos.

Lo único pendiente es externo y es el pedido 1 del lunes: **la salida por ventana de la
corrida de Diego**. El comparador está listo para ese día, que es la tercera tarea del
issue: es la misma herramienta, con `--etiquetas nuestro,suyo`.

Queda anotado para quien lo necesite que el `RNAplfold` 2.1.5 compilado **no se versiona**
—es un binario de 700 KB— pero la receta para rehacerlo en unos minutos está en el
encabezado de `scripts/correr_pares.py`, y sin la variable `SIFI_RNAPLFOLD` el script corre
los tres pares que no dependen de él y declara el cuarto como no corrido en vez de darlo
por cero.

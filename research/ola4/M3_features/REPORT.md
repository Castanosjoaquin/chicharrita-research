# M3 — Tercera vía: los términos continuos, sin corte

Línea M3 de la ola 4 (issue #7). Implementa la tercera alternativa que propuso Diego:
«conservar los valores termodinámicos, las preferencias terminales y la accesibilidad
como variables independientes del proceso de clasificación, para evaluar posteriormente
cómo contribuyen a la eficiencia» `[R]`.

## 1. Qué faltaba

El ADR D26 ya obligaba a publicar los términos continuos, y estaba implementado a
medias: el TSV por ventana traía `dg_sense5`, `dg_antisense5`, `ddg` y `accessibility`,
pero **no los dos nucleótidos de la regla terminal ni la rama aplicada**, que es
justamente la variable que él quiere ver como independiente.

## 2. Lo que se agregó, y por qué no son los nucleótidos

El issue pedía columnas `nt19`, `nt2` y `rama_terminal`, con el argumento de que «son dos
letras y un entero: no reconstruyen secuencia». **Eso está medido y es falso**, y la
medición es de la línea M9: como las ventanas se solapan de a 1 nt, la columna con la
letra de una posición fija, concatenada en orden, es una subcadena literal del gen. Sobre
un gen sintético de 500 nt y 480 ventanas, `nt19` y `nt2` juntas reconstruyen 497 de 500
nt, el 99,4 %, **sin producir ni una racha de 21 nt** que un escáner pueda ver `[M]`
(`research/ola4/M9_auditoria_secuencias/scripts/prueba_columnas_terminales.py`).

Lo que se agregó, entonces, son **las categorías que la regla efectivamente usa**:

| Columna | Qué es |
|---|---|
| `nt19_at` | el nucleótido 19 es A o T |
| `nt2_gc` | el nucleótido 2 es G o C |
| `rama_terminal` | 1 a 4, cuál de las cuatro ramas se aplicó |

La regla terminal no mira la letra: mira exactamente esas dos propiedades
(`sifi_core.py:_terminal_rule`, que reproduce `sifi_pipeline.py:525-550`). Así que las
categorías **conservan todo el poder predictivo de la regla** y bajan de dos bits por
posición a uno. No permiten escribir la secuencia; sí siguen siendo un perfil del gen, y
por eso la tabla por ventana no se versiona (§5).

### Las cuatro ramas

| Rama | Condición | Qué decide el veredicto |
|---|---|---|
| 1 | `nt19` A/T, `nt2` A/T | la termodinámica |
| 2 | `nt19` A/T, `nt2` G/C | **sólo la accesibilidad** — es el atajo |
| 3 | `nt19` G/C, `nt2` G/C | la termodinámica |
| 4 | `nt19` G/C, `nt2` A/T | nada: no eficiente |

## 3. El resultado: el atajo produce la mayoría de los «eficientes»

Con las ramas numeradas se puede medir algo que hasta ahora se describía en palabras. La
rama 2 es la que Diego confirmó como existente en el original y la que la auditoría de C1
había señalado; lo que no estaba medido es **cuánto pesa**:

| Gen | Eficientes (fiel) | De la rama 2 | Fracción |
|---|---|---|---|
| `MP_MRFV` | 142 | 80 | 56,3 % |
| `CP_MRFV` | 39 | 25 | 64,1 % |
| `BicC_Dm` | 223 | 134 | 60,1 % |
| `ATPaseD_Dm` | 35 | 19 | 54,3 % |

`[M]`, `--backend vienna`, `resultados/resumen_features.md`.

Entre el 54 % y el 64 % de las ventanas que el original llama eficientes salen de la rama
que **saltea el veredicto termodinámico** y decide mirando sólo la accesibilidad. No es
una rareza de borde: es la mayoría del resultado.

**Control que cierra el cuadro.** Si el modo corregido sólo cambia esa rama, entonces toda
la diferencia entre los dos modos tiene que estar ahí, y está: la rama 2 cae de 80 a 61,
de 25 a 16, de 134 a 82 y de 19 a 13, o sea −19, −9, −52 y −6, que es **exactamente** la
diferencia de los totales entre modos (142→123, 39→30, 223→171, 35→29). Las ramas 1 y 3
no se mueven ni una ventana, y la rama 4 da cero eficientes en los dos modos `[M]`.

Nótese que −19, −9, −52 y −6 no son los 19, 7, 50 y 8 de `CAMBIOS.md` C1: aquéllos se
midieron con RNAplfold 2.1.5 (`--backend exe`) y éstos con ViennaRNA 2.7.2. El eje del
motor mueve los conteos, como ya midió M1.

## 4. Por qué no se ajusta ningún modelo acá

El issue lo pide explícitamente, y conviene que quede escrito antes que la tabla.

La tabla tiene seis términos. Las etiquetas de eficacia medida que existen son 29, de la
validación retrospectiva contra *Tribolium castaneum*, y con esas 29 la validación dio
ρ = +0,142 con IC95 [−0,247, +0,492] para el modo fiel y ρ = +0,024 [−0,356, +0,397] para
el corregido `[M]` (`research/ola3/C9_sensibilidad_umbral/resultados/validacion_resumen.json`).
Un intervalo que cruza el cero con ese ancho no distingue un criterio bueno de uno inútil;
ajustar seis variables sobre esas mismas 29 observaciones produciría coeficientes cuyo
error estándar es mayor que su valor, y la tentación sería leerlos igual `[H]`.

**Esta tabla no es un modelo: es la tabla sobre la que se podría ajustar uno.** Cuántas
etiquetas harían falta ya lo contestó M4 (#8) mientras esta línea corría: **2.784** siRNA
con eficacia medida para distinguir los dos modos con potencia 0,80 `[M]`, y con los 29 de
Cedden la comparación no podía salir distinta —un solo siRNA discordante, p exacto 1,00
por enumeración completa `[M]`— (`research/ola4/M4_evidencia_y_potencia/REPORT.md`). El
plan de análisis de esta tabla quedó preregistrado y sin ejecutar en
`M4_evidencia_y_potencia/PREREGISTRO_tercera_via.md`, con condición de disparo explícita:
nada se ajusta con menos de 100 etiquetas y 3 genes blanco (D53).

## 5. Qué se versiona y qué no

La tabla por ventana **no se versiona**, y es una desviación consciente del «REPORT.md con
la tabla de los cuatro genes» que pide el issue. El motivo es §2: aunque las columnas
nuevas no permiten escribir la secuencia, `nt19_at` y `nt2_gc` son un bit por posición
sobre ventanas consecutivas, o sea un perfil del gen. Se versiona el resumen agregado por
gen y por rama, que no conserva el orden de las ventanas, más el comando para regenerar la
tabla completa en local. Es la misma política que ya rige para la columna `seq`.

```sh
python3 tools/sifi21_port/run_sifi.py <fasta...> --modo fiel --backend vienna \
        --salida <dir> --features
python3 research/ola4/M3_features/scripts/resumen_features.py <dir>
```

## 6. La columna `seq` sale del TSV por defecto

Es lo que el issue pedía y lo que M9 recomendó: `to_tsv` ya no la emite salvo que se pida
`--con-seq`, porque sobre ventanas solapadas de a 1 nt reconstruye el gen entero. Fue el
incidente de C9.

**Un consumidor dependía de ella y quedó arreglado en la misma pasada:**
`research/ola4/M1_conteo_y_referencia/scripts/conteo_por_acierto.py` usa el 21-mero de
cada ventana para armar las consultas de Bowtie, y lo lee con `fila.get("seq") or ""`, así
que sin la columna se habría quedado sin consultas **en silencio**, sin fallar. El driver
`correr_matriz.py` ahora pasa `--con-seq`, y su TSV vive bajo `work/`, que no se versiona.
Verificado tras el cambio: contra el gen mismo, `BicC_Dm` da 2.500 ventanas, 223
eficientes, 223 aciertos en `+`, ninguna sin acierto y ninguna múltiple, con
`--exigir-identidad` en verde `[M]`.

Ningún otro consumidor lee esa columna: los de C7 y C3 usan `to_tsv` para escribir.

## 7. Verificación

- **El cambio no mueve ningún veredicto.** Las 4.722 ventanas de los cuatro genes, en los
  dos modos, dan el mismo `is_efficient` que el ancla publicada de C9: 142, 39, 223 y 35
  en fiel, con **cero discrepancias** celda por celda `[M]`.
- **La rama explica el veredicto.** En las 4.722 ventanas, ninguna contradice lo que su
  rama predice, en los dos modos `[M]`.
- **La tabla de features no reconstruye secuencia.** El escáner de M9 sobre ella da cero
  en las tres pasadas: cero rachas de 21 nt, cero cadenas de k-meros solapados y cero
  k-meros de EPILAB `[M]`.
- Tres pruebas nuevas en `tools/sifi21_port/test_sifi.py` (tabla de verdad de las cuatro
  ramas, la rama contra el veredicto, y las columnas del TSV). La suite pasa entera.

## 8. Lo que esta línea deja a M4

La tabla de `--features` corre en los cuatro genes y en los dos modos, que es el insumo
que el issue #7 declara para #8. Dos cosas que conviene que M4 tenga a mano:

1. **La variable que más separa es categórica, no continua.** La rama terminal explica más
   de la mitad de los eficientes, así que un modelo que trate los cuatro términos como
   continuos y omita la rama va a atribuirle a la accesibilidad un efecto que en realidad
   es «la rama 2 sólo mira la accesibilidad».
2. **Las ramas 1 y 3 son indistinguibles por su veredicto** —las dos deciden por
   termodinámica— así que para un modelo son la misma condición. Lo que las separa es la
   composición terminal, que es lo que habría que testear si se quiere saber si la
   preferencia terminal aporta algo por fuera del atajo.
3. **El conjunto discordante entre modos coincide exactamente con la rama 2**, así que el
   ensayo discriminante que M4 ya diseñó —32 siRNA por brazo, D53— puede muestrear los
   brazos dentro de esa rama y no sobre el gen entero: fuera de ella los dos modelos no
   pueden diferir, porque está medido que las ramas 1 y 3 no mueven ni una ventana entre
   modos y que la 4 da cero eficientes en los dos. El repertorio que D53 cita, 84 ventanas,
   es el mismo conjunto contado con `--backend exe`; acá, con ViennaRNA 2.7.2, da 86
   (19, 9, 52 y 6).

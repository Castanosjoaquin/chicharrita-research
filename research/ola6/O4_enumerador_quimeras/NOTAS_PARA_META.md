# Notas de la línea O4 (ola 6)

Esta línea la corrió la sesión principal, así que `00_meta/` **sí** se actualizó
directamente: `D79` y `D80` en `DECISIONS.md`, tres filas en `GLOSARIO.md` —«isla
admisible», «objetivo declarado antes de rankear» y «aporte de un bloque fabricado»—, las
entradas 44 a 47 de `PREGUNTAS_ABIERTAS.md`, una de las cuales reescribe lo que esta misma
línea había escrito mal unas horas antes. Este archivo queda con lo que es propio del
bloque.

---

## Lo primero: el error que esta línea cometió y corrigió

El ancla 3 del preregistro no cerró contra `D74`, y escribí —y commiteé— una entrada de
`PREGUNTAS_ABIERTAS.md` afirmando que la unidad del largo de una región **no estaba
declarada en ninguna parte**, citando como prueba que no está en la fila «región candidata»
del glosario ni en `M1` §8. Era falso. Está declarada desde `D63` y `N3` le puso nombre a los
dos marcos que importan; hay incluso una fila de glosario que se llama **«marco de conteo»**
y dice exactamente eso. Mis conteos reproducían `N3` celda por celda, o sea que lo que tenía
en la mano era **un ancla pasando** y lo reporté como hallazgo.

Lo que sí era nuevo resultó más chico y más filoso: la unidad del eje de **riesgo**, que
nadie declaró, y que hace que una región pueda quedar vetada por un 21-mero que la molécula
no contiene. Eso es `D80` y la entrada 44.

La lección operativa, que vale más que el hallazgo: **buscar el concepto por el eje que lo
mide, no por la palabra que uno usaría.** Busqué «unidad de conteo» —que es como lo llamó
`M1`— y el proyecto le dice «marco». Antes de declarar que algo no está declarado hay que
abrir el REPORT del bloque que midió ese eje, que acá era `N3`.

## Las cuatro anclas, y cuál costó

Las cuatro de `PREREGISTRO.md` §7 corren juntas en `scripts/00_anclas.py`, que devuelve 1 si
alguna falla. Las cuatro pasan:

1. **Contra `C13` §5.** Las doce quimeras de las coordenadas vigentes reproducen la tabla
   publicada en **doce columnas, celda por celda**, más las tres sumas: 240 ventanas de
   juntura, 4 eficientes y 61 heredadas que cambiaron de veredicto. Es la más fuerte porque
   esa tabla no la produjo este código.
2. **Contra `O3` y `D74`.** Los dos órdenes dan 41 y 40 ventanas eficientes contra 40 de la
   suma de las partes, el bloque fabricado de 19 nt aparece **sólo** en el orden
   `V-ATPase B` + `BicC_Dm`, ninguna de sus ventanas es eficiente, y el orden inverso
   fabrica cero.
3. **Contra la máscara de veto**, en marco 1: 71 ventanas vetadas, 1.184 regiones que caben,
   una sola admisible y ninguna una unidad más grande.
4. **Motor en proceso contra `run_sifi.py`:** 580 ventanas, cero distintas. Es lo que
   autoriza a plegar miles de candidatos sin pagar el arranque de proceso.

**La que costó fue la 2, y no por el cómputo.** Mi primera versión tamizaba las **ventanas**
de juntura y contaba como fabricado cualquier acierto de ≥ 19 nt. Con eso los **dos** órdenes
de la quimera de `O3` levantaban alerta, cuando `D74` dice que el inverso fabrica cero. La
causa es la distinción que `O3` ya había resuelto en su paso 2: un bloque de 19 nt que entra
entero en el aporte de un solo gen **no lo fabrica el empalme**, lo hereda. El tamizado pasó
a ser a nivel de **bloque que cruza la unión** —57 por juntura, exactos y en las dos hebras—
y recién ahí reprodujo `D74`.

## Qué código se tocó, y qué se dejó sin tocar

**Nada de `tools/sifi21_port/` cambió.** El motor se llama en proceso con la misma
configuración que `run_sifi.py` construye por default, y el ancla 4 lo verifica ventana por
ventana. El tamizador se usa por sus funciones (`rc`, `iter_db`) y su criterio no se
reimplementó: lo que el bloque arma por su cuenta es un autómata sobre **otro** conjunto de
patrones —los bloques que cruzan la unión—, que es una pregunta distinta de la que contesta
`offtarget_21nt.py` y que su salida no puede responder, porque no dice cuál bloque coincidió.

Lo único que se agregó fuera del bloque es la máscara de veto reutilizable
(`scripts/mascara.py`), que vive acá y no en `tools/`, porque todavía no hay un segundo
consumidor.

## Un insumo nuevo que conviene que se sepa

El tamizado del panel de seis que dejó `O3` cubre `V-ATPase B` **entero** pero de `BicC_Dm`
sólo su región de 300 nt, y para enumerar fragmentos a lo largo del gen hacía falta el gen
completo. Está en `work/O4/offtarget/` y `work/O4/offtarget_humano/`, con el gen entero de
los dos (2.500 y 1.483 ventanas), y se regenera con los dos comandos del `REPORT.md` §8.
`work/` no se versiona, así que esto es un aviso y no un archivo.

## Confidencialidad

- Ninguna secuencia salió de la máquina: las seis referencias y el genoma del vector se leen
  de disco, el plegado corre con el módulo `RNA` local y los dos tamizados con autómatas en
  memoria.
- **Ninguna salida de este bloque escribe bases.** Cada quimera se identifica por gen,
  coordenadas, largo, offset y hash corto de doce caracteres; de cada bloque fabricado van su
  largo, su aporte por gen y las referencias en las que cae, nunca su secuencia. El
  `.gitignore` del bloque rechaza `*.fna`, `*.fasta` y `*.aln`.
- `tools/verificacion/sin_secuencias.py` queda en **6 hallazgos no exceptuados**, que es la
  línea base; los tres archivos que los producen son de `W2` y `C4`, ninguno de acá.

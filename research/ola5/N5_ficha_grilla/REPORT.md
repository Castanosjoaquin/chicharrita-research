# N5 — Ficha: las 4.368 configuraciones y la identidad de C7

**Ola 5, línea N5.** Fecha: 2026-10-25. Contesta los dos pedidos explícitos del punto 5 de la
carta del investigador del 25 de octubre de 2026: «me interesa también conocer cuáles son
exactamente las variables de las 4.368 configuraciones de sensibilidad y la identidad de la región
C7 utilizada en la comparación» `[R]`. No corre nada: es la ficha de lo que ya midió
[`M7`](../../ola4/M7_robustez_bicc/REPORT.md).

## 1. Las 4.368 configuraciones

`[M]` Son el producto de cinco ejes. Cada configuración se mide además en dos marcos de conteo, de
donde salen las 13.104 filas de `M7/resultados/grilla_parametros.tsv`.

| Eje | Valores | Cuántos | Valor por defecto |
|---|---|---:|---|
| brecha de estabilidad de extremos | 0,0 a 2,0 kcal/mol, paso 0,1 | 21 | 1,0 |
| corte de accesibilidad | 0,05 a 0,30, paso 0,01 | 26 | 0,1 |
| modo del port | `fiel`, `corregido` | 2 | — |
| tabla de apilamiento | `RNA_NN3` (Chen *et al.* 2012, la del original), `RNA_NN4` (Zuber *et al.* 2022, la de `sifi21INTA`) | 2 | `RNA_NN3` |
| motor de plegado | RNAplfold 2.1.5 (el del instalador de si-Fi21), ViennaRNA 2.7.2 | 2 | — |

`21 × 26 × 2 × 2 × 2 = 4.368`.

**Lo que queda fijo en las 4.368:** tamaño de siRNA 21 nt, ventana de accesibilidad `u = 8`,
22 °C, y las cuatro casillas del criterio tildadas —selección de hebra, estabilidad de extremos,
accesibilidad del sitio blanco y regla del nucleótido terminal 5'—. Es decir la cadena
`siFi21_8_1.0_0.1_1111` con la que el laboratorio declaró su configuración, con los dos umbrales
barridos y lo demás quieto.

**Los dos marcos** son los de [`N3`](../N3_marcos/REPORT.md): el conteo de los arranques que caen
dentro de la región en el gen completo, y el de la molécula recortada plegada sola. El marco
intermedio —los 21-meros que existen en la molécula con la accesibilidad evaluada en el gen, que es
el tercero que propone su carta— **no está cruzado con la grilla**: está medido sólo en el punto
por defecto.

**Dos advertencias de lectura, que `M7` ya pone.** Los conteos de los dos motores no son
comparables entre sí, así que cada comparación es entre regiones dentro de una misma
configuración y nunca entre motores. Y el eje del motor sólo corre si se le pasa la variable
`SIFI_RNAPLFOLD` apuntando a un RNAplfold 2.1.5; sin eso se declara no corrido y no cero.

## 2. La identidad de C7

`[M]` **C7 es `BicC_Dm` 2121-2420**, una región de 300 nt. El nombre viene de la línea C7 de la
ola 3 (`research/ola3/C7_ranking_v2/`), que la eligió por densidad de ventanas eficientes: era la
región recomendada para ese gen hasta que **D25** la desplazó por conservación y pasó a
recomendarse 922-1221. En la grilla de `M7` entra como rival, no como candidata.

Las otras dos regiones de la comparación:

| Región | Qué es | Conteo en la molécula |
|---|---|---:|
| `BicC_Dm` 922-1221 | la vigente, por D25 | 26 |
| `BicC_Dm` 2121-2420 | **C7**, la que ganaba por densidad | 22 |
| `BicC_Dm` 264-563 | la que eligió EPILAB | 17 |

## 3. La autocorrección que va con esto

`[M]` El argumento con el que D25 desplazó a C7 **no es sostenible tal como está escrito**, y
conviene decirlo antes de que lo pregunte. El ADR dice «32 de 36 idénticas en los tres
transcriptomas públicos contra 22 de 35». Medido por fuente separada (`M7` §4):

| Fuente | Cobertura de 922-1221 | Idénticas en 922-1221 | Idénticas en 2121-2420 |
|---|---|---|---|
| GHCC01 (Pergamino, Argentina) | completa | 36 de 36 | 35 de 35 |
| GITV01 (Ohio State) | completa | 32 de 36 | 33 de 35 |
| GCWP01 (Illinois) | **nula** | sin datos (36) | 22 de 35, con 13 contradichas |
| genoma `GCA_975739785.1` (Reino Unido) | completa | 36 de 36 | 27 idénticas y 8 que cruzan un empalme |

`GCWP01` no cubre un solo nucleótido de 922-1221: alinea con el gen en dos tramos —2044-2467 y
249-433— y nada más `[M]`. El «32 contra 22» sale de contar la ausencia de datos como ausencia de
contradicción: las trece ventanas que Illinois contradice en 2121-2420 descalifican, y las treinta
y seis que Illinois no mira en 922-1221 no.

`[H]` La decisión **no se cae** —el transcriptoma argentino y el genoma del Reino Unido favorecen
a 922-1221, y el ensamblado de Córdoba también según `C8`— pero su razón escrita hay que
reescribirla con la cobertura declarada por fuente. Eso es un ADR nuevo y no una nota al pie.

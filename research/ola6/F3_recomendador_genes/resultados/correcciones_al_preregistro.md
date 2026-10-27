# Correcciones al `PREREGISTRO.md`, con fecha

**2026-10-27.** El preregistro dice, en su encabezado, que si algo de lo que afirma cambia
después de escribirlo cambia «como una entrada nueva con fecha, no como una corrección
silenciosa». Esto es esa entrada. El archivo original **no se editó**.

Las tres correcciones salieron del paso 1, al asignar el mecanismo de fenotipo leyendo el
campo `resultado` **completo** de las 36 filas. Los ejemplos que el preregistro §6 nombra se
habían elegido sobre la versión recortada de ese campo, y dos de ellos estaban mal.

## 1. Dos de las cuatro filas de «transmisión» de §6.1 estaban mal asignadas

§6.1 nombra `CI-07`, `CI-09`, `HE-07` y `HE-11` como las filas del cuarto mecanismo. La
lista correcta, verificada contra `resultado`, es **`CI-06`, `CI-07`, `CI-09` y `DE-05`**.

**`HE-07` no es transmisión, y el error es exactamente el que el preregistro prohíbe.** Su
`funcion` dice «proteína salival clave para la ingestión de floema», que invita a leerlo como
transmisión. Su `resultado` mide otra cosa: «longevidad a la mitad, retraso del desarrollo,
menos huevos». Se asignó **letalidad y reproducción**. La regla de §6 —asignar desde
`resultado`, nunca inferir del gen ni de la función— se escribió para este caso, y la primera
lectura la violó de todas formas. Queda como el mejor argumento a favor de la regla, y de que
el script verifique la frase de apoyo contra la fuente en vez de confiar en quien asigna.

**`HE-11` no tiene fenotipo publicado.** Dice «RNAi funcional en la interacción con el virus»,
que reporta que la técnica funciona, no un desenlace medido. Una interacción con el virus no
es, por sí sola, una reducción de transmisión medida. Se etiquetó
`sin_fenotipo_publicado`.

**Faltaban dos.** `CI-06` mide «menos adquisición de fitoplasma» y es transmisión sin
discusión. `DE-05` mide «menor acumulación del rabdovirus MMV» además de supervivencia y
reproducción, y es **la única fila del catálogo con tres mecanismos medidos a la vez**.

## 2. Las filas con mortalidad no atribuible al blanco son dos, no una

§6.3 nombra sólo `HE-08` («mortalidad alta por la dosis, no por el blanco»). `HE-04` es el
mismo caso y es más grave, porque sí trae un número grande: 64 % de mortalidad a 120 h,
creciente con la dosis, **pero** la propia fuente dice que el knockdown no correlaciona con la
dosis y que el control de dsGFP a 500 y 1000 ng/µL ya mata más que el control de sacarosa.
Las dos quedaron con `sin_fenotipo_atribuible_al_blanco`. Un recomendador que leyera «64 % de
mortalidad» y la puntuara como letalidad estaría publicando el efecto de la dosis como si
fuera el del blanco.

## 3. El hallazgo del paso 1, que no es una corrección sino algo nuevo

**El mecanismo `movilidad` de `D67` tiene un solo candidato en las 36 filas** `[M]`.

| mecanismo | n | filas |
| --- | ---: | --- |
| letalidad | 16 | `CI-01`, `CI-02`, `CI-04`, `CI-05`, `CI-10`, `CI-11`, `CI-12`, `DE-01`, `DE-04`, `DE-05`, `DM-02`, `DM-03`, `DM-05`, `DM-06`, `HE-02`, `HE-07` |
| reproducción | 13 | `CI-01`, `CI-02`, `CI-03`, `CI-10`, `DE-01`, `DE-02`, `DE-03`, `DE-04`, `DE-05`, `DM-01`, `HE-01`, `HE-05`, `HE-07` |
| **transmisión** | **4** | `CI-06`, `CI-07`, `CI-09`, `DE-05` |
| **movilidad** | **1** | `DM-02` |

Y el único candidato de movilidad es frágil por dos razones. La primera es que su apoyo es
una frase sola, «alas deformes», sin magnitud ni estadístico. La segunda es más fuerte:
`DM-03` es la **otra subunidad de la misma bomba**, en la misma especie y con la misma vía de
entrega, y ahí el efecto sobre alas **se midió y no dio significativo** —«efecto en alas no
significativo»—. O sea que la réplica más cercana que existe del único apoyo de movilidad es
negativa `[M]`.

`[H]` La consecuencia para `D67` es directa y no es de esta línea resolverla: si las quimeras
se arman combinando mecanismos que no se solapan, una de las tres patas del esquema se apoya
en una fila, y el mecanismo que `D67` **no** reconoce —transmisión— tiene cuatro veces más
candidatos que ésa. Va como entrada abierta, junto con la 54.

# Notas de M4 para la memoria del proyecto

Lo que esta linea deja para `00_meta/`, listo para copiar. Se anota aca y se traslada en el mismo
commit.

## Para `DECISIONS.md` — D53

**D53 — El ensayo discriminante entra al entregable como la casilla de validacion, y el analisis
de la tercera via queda preregistrado sin ejecutar**
**Fecha:** 2026-10-23
**Quien:** Luca, consultado al cerrar la linea M4 de la ola 4; el orquestador implementa.
**Decision:** el diseno de ensayo prospectivo de la seccion 4 de
`research/ola4/M4_evidencia_y_potencia/REPORT.md` —siRNA discordantes entre modos contra
concordantes eficientes, con un brazo de concordantes rechazados como control de validez interna y
un control negativo no dirigido, sobre un gen, con el silenciamiento del transcrito como variable
de respuesta y 32 siRNA por brazo— **entra al entregable del checkpoint 2 como su casilla de
validacion**, declarando que el equipo lo propone y no lo corre. En paralelo, el plan de analisis
de la tercera via de M3 queda **preregistrado y sin ejecutar** en
`research/ola4/M4_evidencia_y_potencia/PREREGISTRO_tercera_via.md`, con condicion de disparo
explicita: no se ajusta nada con menos de 100 etiquetas y 3 genes.
**Alternativas consideradas:** (a) dejar el diseno como anexo interno y llenar la casilla de
validacion con la validacion retrospectiva de C9, que es no concluyente; (b) no proponer
validacion experimental; (c) ajustar ya el modelo continuo sobre las 29 etiquetas de Cedden para
tener «la tercera via» mostrable el lunes; (d) la elegida.
**Criterio:** sobre (a), presentar como validacion un resultado que el propio pre-registro declara
no concluyente seria usarlo para lo contrario de lo que mide. Sobre (c), con 29 etiquetas y seis
terminos el ajuste describe el ruido de un solo trabajo, y encima la linea M4 midio que ese
conjunto no distingue ni dos criterios que difieren en una rama: el modelo saldria y no significaria
nada. Sobre (d): el ensayo es el unico diseno que discrimina los dos modelos, su tamano de muestra
esta calculado y su repertorio de siRNA discordantes ya esta contado, asi que es la casilla mas
fuerte que el entregable puede tener sin laboratorio propio.
**Consecuencia:** el entregable gana una casilla de validacion con numeros y resultado falsador, y
queda obligado a declarar en el mismo lugar que no lo corremos nosotros. El pre-registro de la
tercera via cierra la pregunta del investigador sobre los terminos continuos sin fabricar un
modelo: la respuesta es que la tabla existe (M3), que el plan de analisis existe y esta congelado,
y que falta el dato. Si nunca aparecen etiquetas, el pre-registro queda sin ejecutar y eso tambien
se reporta.

## Para `PREGUNTAS_ABIERTAS.md` — pendientes nuevos de la linea M4 (2026-10-23)

1. **iBeetle-Base: hay dos fragmentos no solapados por gen?** Es la pregunta que decide si la unica
   fuente de etiquetas grande del reino correcto sirve. El articulo de la base (NAR 2015,
   `10.1093/nar/gku1054`, PMC4383896) dice que los fenotipos se guardan **por fragmento** y que hay
   5.180 ARNdc distintos sobre 16.505 genes, pero **no menciona fragmentos no solapados** ni cuantos
   genes tienen dos reactivos independientes `[?]`. Si los hay, hay pares de reactivos contra el
   mismo blanco con desenlaces independientes, que es la estructura que M4 muestra como necesaria;
   si no, la linea se cierra. Se contesta consultando `ibeetle-base.uni-goettingen.de` o la
   actualizacion de 2017 (`10.1093/nar/gkx984`). Limite ya conocido: licencia **CC BY-NC 4.0**, el
   reactivo es un fragmento de ~479 pb y el desenlace son terminos de ontologia con penetrancia en
   tramos, no una eficacia continua.
2. **El conjunto de 2.431 siRNA de Huesken 2005 no tiene punto de descarga abierto que hayamos
   encontrado.** Los dos trabajos que lo usan y que si abrimos —Vert *et al.* 2006
   (`10.1186/1471-2105-7-520`) y Thang *et al.* 2015 (`10.1186/s12859-015-0495-2`)— lo citan al
   original (`10.1038/nbt1118`) sin enlace ni archivo adjunto `[?]`. Queda pendiente verificar el
   material suplementario del original. **No se cito contenido suyo mas alla de lo que esos dos
   reportan.**
3. **siRecords**: las 2.470 etiquetas de eficacia «muy alta» y 2.514 de «baja» aparecen reportadas
   en Thang *et al.* 2015, pero **no pudimos abrir la base** ni verificar su licencia o si sigue en
   linea `[?]`. Ademas sus etiquetas son clases y no valores, asi que no sirven para una correlacion
   de rangos.
4. **GenomeRNAi no se pudo abrir** desde esta maquina (error de TLS en `genomernai.org`). No se cita
   nada de su contenido `[?]`.
5. **La dispersion del silenciamiento entre siRNA de una misma clase no la tenemos medida en ningun
   sistema comparable.** El tamano de muestra del ensayo propuesto la supone en 20 puntos
   porcentuales `[H]`; si en el ensayo resulta 25, el n por brazo sube de 32 a 49. Es el primer
   supuesto a revisar con los datos del propio ensayo, y conviene preguntarle al investigador si
   tiene una estimacion de su sistema.

## Para `FUENTES.md` — abiertas en esta linea (2026-10-23)

- Cedden *et al.* 2025, *BMC Biology* 23:114, doi 10.1186/s12915-025-02219-6 (PMC12039203) —
  **licencia CC BY 4.0 confirmada**; 31 siRNA de 21 nt contra *Tc-gawky* y 3-4 ARNdc por gen en 8
  genes, con razon de riesgo de log-rank como desenlace. Ya estaba en uso desde C9; aca se verifico
  la licencia y los datos suplementarios (archivos adicionales 1 y 2).
- Vert *et al.* 2006, *BMC Bioinformatics* 7:520, doi 10.1186/1471-2105-7-520 (PMC1698581) —
  abierta completa, CC BY 2.0. De aca salen los tamanos de los conjuntos humanos: Huesken 2.431,
  Reynolds 240, Vickers 76, Harborth 44 y la compilacion de Shabalina 653 `[R]`.
- Thang *et al.* 2015, *BMC Bioinformatics* 16:80, doi 10.1186/s12859-015-0495-2 (PMC4379720) —
  abierta completa, CC BY 2.0. Confirma los mismos 2.431 de Huesken y reporta las etiquetas de
  siRecords (2.470 «muy alta», 2.514 «baja») `[R]`.
- Donitz *et al.* 2015, *Nucleic Acids Research* 43(D1):D720-D725, doi 10.1093/nar/gku1054
  (PMC4383896) — abierta completa, **CC BY-NC 4.0**. iBeetle-Base: 5.180 ARNdc sobre 16.505 genes de
  *Tribolium castaneum*, fenotipo **por fragmento** con penetrancia.
- Jain *et al.* 2020, *Insects* 11(9):557, doi 10.3390/insects11090557 (PMC7564473) — abierta
  completa, CC BY 4.0. 33 especies de hemipteros en 14 familias con silenciamiento publicado y
  **ninguna base de eficacia por reactivo**; es la fuente de que para hemipteros no hay etiquetas.
- Huesken *et al.* 2005, *Nature Biotechnology*, doi 10.1038/nbt1118 — **no abierta**. Se la cita
  solo como identificador del conjunto, y los numeros que aparecen sobre ella vienen de los dos
  trabajos de arriba.
- `genomernai.org` — **no accesible** (error de TLS). No se cita.

## Para `CAMINOS_PROBADOS.md`

**Estimar por remuestreo la potencia de un diseno que enriquezca siRNA discordantes: descartado,
con motivo.** La idea natural, despues de medir que hacen falta 232 siRNA replicando el diseno de
Cedden, es volver a remuestrear subiendo a proposito la proporcion de discordantes y ver cuanto baja
el numero. No se puede: en las 29 filas de Cedden hay **un solo** siRNA discordante (`si778`), asi
que cualquier remuestreo que lo enriquezca reproduce su mismo desenlace y la variabilidad entre
discordantes seria cero, lo que infla la potencia a voluntad. Es la razon por la que la seccion 4
del REPORT cambia de estadistico —de una correlacion de rangos a un contraste entre grupos con
supuestos declarados— en vez de subir el n del mismo calculo. El descarte vale como regla general:
un remuestreo no puede inventar variabilidad que la poblacion madre no tiene.

## Para el napkin

**Una comparacion entre dos criterios que discrepan en pocos casos no tiene potencia por mas n que
haya.** Con k casos discordantes, una prueba de aleatorizacion por intercambio no puede dar un p
menor que 2/2^k, asi que con k < 6 ningun dato alcanza alfa 0,05 `[M]`.
**Do instead:** antes de proponer comparar dos variantes del criterio sobre un conjunto etiquetado,
contar los **discordantes**, no el n total. Si son menos de 6, la comparacion no puede salir
distinta y hay que cambiar de diseno (elegir discordantes) o de estadistico.

# Respuesta a la carta del 22 de octubre — borrador

**Estado: BORRADOR, SIN ENVIAR.** No se manda sin que el usuario lo confirme.

**Criterio de este borrador.** La carta de Diego cierra con «nos vemos el lunes». Eso cambia qué
conviene escribir: de nuestras siete preguntas del correo anterior contestó una, y las otras seis
se preguntan mejor en persona que por escrito. Entonces este mensaje hace **tres cosas y nada
más**: contesta las dos preguntas que él nos hizo, le pide un archivo —el único pedido que
necesita que busque algo antes del lunes— y le anticipa en un párrafo lo que encontramos
siguiendo su pista, porque es lo que justifica el pedido. Las seis preguntas abiertas van a la
reunión, y están listadas en `00_meta/PREGUNTAS_ABIERTAS.md` y en `docs/plan_ola4/PLAN_OLA4.md`
§6, en orden de cuánto desbloquean.

**Si el usuario prefiere no mandar nada antes del lunes**, lo único que vale la pena mandar es el
pedido del archivo, porque es lo que necesita tiempo. Las dos respuestas y el párrafo del
hallazgo se pueden decir en la reunión.

---

## El cuerpo del mensaje

Hola Diego,

Gracias por la respuesta, y en particular por haber vuelto al código: nos cambió el estado de dos
cosas que teníamos abiertas desde el checkpoint.

**Las dos que nos preguntaste.**

`sifi21INTA` lo tomamos de `github.com/bioinformaticaInta/sifi21INTA`, commit
`92df44494373551d86eb1aee1b72d82858c581b2`, que era la cabeza de `main` al 27 de marzo de 2024
(lo verificamos con `git ls-remote`). Lo comparamos contra el original de
`github.com/snowformatics/siFi21-`, commit `d6296b73c08a2176e9d0257e0a175278cff8c231`, cabeza de
`master` al 18 de marzo de 2025. La comparación quedó archivo por archivo, con dieciocho
diferencias y la medición de cuáles mueven un número y cuáles no; dos que vale la pena mencionar
porque son trampas: `sifi21INTA` cambió la tabla de vecinos más cercanos de `RNA_NN3` a una nueva
atribuida a Zuber *et al.* 2022, lo que mueve catorce ventanas en tus cuatro genes, y llama a
`Bio.SeqUtils.GC`, que Biopython eliminó en la 1.82, así que con una instalación actual el
paquete aborta y hay que bajar a 1.81.

El port es nuestro y es de línea de comandos: reimplementa el criterio de eficiencia en Python 3,
sin interfaz, con dos modos —uno fiel, que reproduce la rama terminal del original tal cual, y uno
corregido, que la aplica como filtro adicional— y dos motores de accesibilidad, el RNAplfold 2.1.5
que instala si-Fi21 y las ligaduras de ViennaRNA 2.7.2. Está verificado contra el programa
original en tus cuatro genes: con su mismo RNAplfold da los mismos cuatro conteos de eficientes y
reproduce la curva del «RNAi design plot» tramo por tramo. Te lo pasamos con gusto; dejanos
hacerle antes una revisión, porque el repositorio tiene resultados derivados de las secuencias de
EPILAB y queremos asegurarnos de no mandarte de vuelta tus propias secuencias en un archivo
intermedio. Además nos quedó una duda que vos podés contestar mejor que nosotros: la licencia del
original aparece como CC BY-SA 4.0 en el artículo y como CC BY-NC 2.0 en SourceForge, y no
sabemos cuál rige para redistribuir un derivado.

**Lo que encontramos siguiendo tu pista, y el archivo que te pedimos.**

Nos dijiste que antes de tocar parámetros verificáramos secuencias, orientación, **referencias** y
criterios de contabilización. Las secuencias y el largo están verificados: los cuatro genes de la
planilla dan 1.243, 508, 2.500 y 471 ventanas de 21 nt, y el volcado del propio si-Fi declara 471
aciertos totales para `ATPaseD_Dm`, así que estamos corriendo lo mismo. Pero al mirar los
criterios de contabilización apareció algo que no habíamos visto: la columna «Efficient siRNA
hits» del original **no cuenta ventanas, cuenta aciertos de Bowtie**. En `general_helpers.py` la
tabla se arma con un `Counter` sobre los registros agrupados por nombre de referencia, y en
`sifi_pipeline.py` el bloque de eficiencia está dentro de un `if strand == '+'`, de modo que una
ventana que no pega en la referencia elegida no entra al conteo, una que pega sólo en la hebra
menos tampoco, y una que pega dos veces entra dos veces. Que lo último pasa lo medimos: en
`BicC_Dm`, Bowtie reporta 2.504 aciertos para 2.500 ventanas.

Eso nos parece la primera explicación candidata con la forma correcta. Contra las mismas
secuencias, el original con sus valores por defecto nos da 133, 32, 212 y 42 ventanas eficientes,
y la planilla declara 114, 35, 199 y 33: **baja en tres genes y sube en uno**. Ningún umbral puede
hacer eso —un umbral más estricto sólo baja—, pero un conteo por acierto contra una referencia
distinta de la nuestra sí. Es una hipótesis todavía, no un resultado.

Para probarla necesitamos dos cosas tuyas, y las dos son archivos que ya existen:

1. **La clasificación por ventana de la corrida `siFi21_8_1.0_0.1_1111`** —el CSV de
   `Save as → Table` si fue con el original, o el JSON de `sirnaData` o el HTML de Plotly si fue
   con `sifi21INTA`—. Con eso podemos comparar cuáles son las ventanas que cambian de
   clasificación, que es exactamente lo que nos sugeriste, en lugar de seguir comparando totales.
2. **Contra qué base de Bowtie corrieron el diseño**, y qué fila de la tabla de resultados tomaron
   para la planilla.

Con esos dos datos la pregunta se cierra en una tarde. Sin ellos, lo más honesto que podemos hacer
es acotar la explicación y decirte cuál es, que es lo que vamos a llevar el lunes.

Del resto de tu carta estamos trabajando en cuatro cosas y las llevamos a la reunión: separar
exposición de conservación en el panel (y te vamos a mostrar que, aplicado, nos devuelve un empate
que creíamos resuelto), pasar el veto a alerta con justificación, la robustez de `BicC` 922–1221
en los tres ejes que nombraste, y tu pregunta final sobre qué permite comparar el número de
eficientes, que es la que más nos hizo pensar.

Nos vemos el lunes.

Saludos,
[EQUIPO]

---

## Lo que deliberadamente no entra en este mensaje

| Qué | Por qué |
| --- | --- |
| Las seis preguntas del correo anterior que no contestó | Se preguntan mejor en persona, y mandarle seis por escrito dos días antes de la reunión es la forma de que no conteste ninguna. Están en `PLAN_OLA4.md` §6 en orden de prioridad |
| El resultado de la línea M1 | No está corrido todavía. No se le anticipa un número que no tenemos |
| Que su corrección del veto nos devuelve el empate del tercer puesto | Va en el mensaje como anticipo de una frase, pero el número se muestra en la reunión con la tabla al lado. Decirlo por escrito sin la tabla invita a discutirlo sin los datos |
| El archivo del port | No se manda hasta que la auditoría de secuencia pase (línea M9) |

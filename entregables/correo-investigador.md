# Correo al investigador — borrador

**Estado: enviado.** Lo confirmó el usuario. La fecha de envío y el texto realmente enviado no están registrados (por confirmar). La grafía del apellido y el dominio ya no bloquean nada.

**Nota (Fase 5, 2026-10-22).** La pregunta 5 de este borrador dice que los candidatos nuevos están «sesgados a esterilidad». El catálogo corregido registra letalidad para `eth` y `burs-alpha` y reducción de oviposición para `BicC` (ver `docs/plan_checkpoint2/salidas/F1_decision_ranking.md` §8). El borrador no se edita: si el texto enviado dice lo mismo, conviene corregirlo en el próximo mensaje.

**Criterio de selección.** Entre `00_meta/PREGUNTAS_ABIERTAS.md` y §5 del plan hay dieciocho
preguntas acumuladas. Mandarle dieciocho es garantizar que no conteste ninguna. Acá van **siete
bloques**, elegidos por dos criterios: cuánto mueven el resultado, y qué tan barato le resulta
contestarlos. Las cuatro primeras las puede contestar de memoria en dos minutos. El resto de la
lista queda en el repositorio para una segunda tanda o para la reunión.

---

## El cuerpo del correo

Hola [NOMBRE],

Te escribimos del equipo de la UdeSA del track de la chicharrita. Desde el checkpoint avanzamos
con los cinco puntos que pediste y están los dos documentos que te interesaban: qué significa
«eficiente» en si-Fi21 con la fuente de cada umbral, y la crítica de las tres herramientas con la
medición que respalda cada punto.

Nos quedaron algunas preguntas. Ninguna nos bloquea —el trabajo está hecho y entregable como
está—, pero cada una de estas mejora lo que podemos afirmar, y varias las podés contestar de
memoria. Van en orden de cuánto cambian el resultado.

**1. ¿En qué modo corriste si-Fi21, y con qué umbral de estabilidad de extremos?**

Es la que más nos cambiaría las cosas. Tu planilla declara 114, 35, 199 y 33 eficientes sobre los
cuatro genes. Nosotros tenemos tres números distintos y ninguno coincide: si-Fi21 original da 133,
32, 212 y 42; la reescritura en Python del grupo, `sifi21INTA`, da 138, 40, 218 y 35. Barrimos
22.176 configuraciones de los parámetros que la librería expone y ninguna da los cuatro valores.

Lo que más se acerca es subir el umbral de estabilidad de extremos de 1,0 a **1,75**: ahí salen
117, 35, 199 y 32, con dos exactos. Dos barridos independientes apuntan al mismo parámetro.
Entonces, concretamente: ¿lo corriste en modo diseño o en modo alta sensibilidad —que apaga
estabilidad de extremos y accesibilidad—, y ese umbral estaba en 1,0, en 1,75 o en 2,0?

Y una variante de lo mismo: ¿los números de la planilla son «eficientes», o «eficientes sin
off-targets»? En la librería del grupo son dos columnas distintas, y la segunda depende de contra
qué base se corrió.

**2. ¿La región 1–200 la elegiste por off-targets, o por densidad de siRNA?**

En el checkpoint lo sospechaste vos mismo y dijiste no acordarte. Lo medimos: en uno de los genes
la región elegida tiene menos de la mitad de ventanas eficientes que la mejor región del mismo
largo. Si fue por off-targets, el criterio se sostiene y lo decimos así. Si fue por disponibilidad
o por costumbre, también, y cambia lo que recomendamos.

**3. ¿Qué transcriptoma de *Dalbulus maidis* usan, y nos lo podrían pasar?**

De eso depende que las posiciones de tu planilla sean reproducibles con datos públicos. Y tiene
una consecuencia concreta: encontramos dos genes de la especie con evidencia funcional publicada
(`eth` y `burs-alpha`, con knockdown del 90 al 95 %) que entraron a nuestro ranking, pero no
pudimos medirles conservación porque ninguno de los tres transcriptomas públicos que usamos los
contiene.

**4. ¿Qué pesos le darías a cada criterio del ranking, y qué peso tiene un hemíptero no objetivo
frente al maíz?**

Son los parámetros libres del motor, y el segundo es el único que no nos corresponde fijar a
nosotros: es el que decide si uno de los candidatos del insecto queda último o no. Mientras no los
tengamos usamos un valor declarado y mostramos el barrido completo, pero un número tuyo vale más
que nuestro barrido.

**5. ¿Les interesa matar o esterilizar?**

El ranking ordena distinto según el objetivo, y no es una diferencia menor. Los candidatos nuevos
que encontramos en cicadélidos están sesgados a esterilidad: uno mata y esteriliza, otro sólo
esteriliza, y una ATP sintasa β silenciada entre 5 y 46 veces en *Scaphoideus titanus* **no afectó
la supervivencia** hasta los 14 días. Si el objetivo es cortar transmisión, esterilizar puede no
alcanzar dentro de la ventana de latencia.

**6. ¿De dónde sale el rango de 150 a 250 nt?**

Lo buscamos en el artículo de si-Fi21, en el manual y en el código, y no está en ninguno de los
tres. Lo que encontramos en la literatura sostiene un piso de unos 60 pb, y hay un trabajo de 2026
que silenció dos genes en *D. maidis* con ARNdc de 578 y 544 pb. Nuestra lectura es que el rango es
una convención razonable y compatible con la evidencia, no una conclusión de ella — pero si tienen
un ensayo propio con largos comparados en la especie, ese dato vale más que toda nuestra tabla de
literatura, porque sería el único en el rango exacto, la especie exacta y la vía de entrega que
ustedes usan.

**7. Dos sobre BLAST.**

¿Usan el BLAST web con sus valores por defecto para verificar off-targets? Lo medimos y, contra
algo del tamaño de un genoma, el resultado es **cero por construcción**: `megablast` con palabra 28
no puede sembrar una consulta de 21 nt. Sobre 3.150 consultas con un desajuste plantado en cada
posición, la mejor configuración de BLAST alcanza 0,762 de sensibilidad y la de por defecto da cero
en las 21 posiciones.

Y una menor: mencionaste «HCP» como parámetro. Entendemos que es «HSP», que no es un parámetro
sino la unidad de resultado — ¿te referías a `-max_hsps` / `-qcov_hsp_perc`, al E-value, o al
percent identity? La diferencia cambia qué te recomendaríamos configurar.

---

Cualquiera de estas que puedas contestar nos sirve; no hace falta que sean todas ni que sea rápido.

Gracias,
[EQUIPO]

---

## Lo que deliberadamente dejamos afuera del correo

Para que la decisión quede registrada y no se pierdan las preguntas:

| Pregunta | Por qué no entró |
| --- | --- |
| Versión de ViennaRNA del servidor de Apolo Rocket | Es de detalle y sólo afecta la comparación interna; va a una segunda tanda |
| Si el método «IA» de Apolo Rocket existe fuera del esquema | Nos interesa a nosotros, no mueve el entregable |
| Cuál de las tres declaraciones de licencia de si-Fi21 rige (D32) | No es una pregunta de método; se resuelve mejor en persona |
| Si corren el tamizaje contra transcriptomas, genomas o los dos | Queda implícita en la 3; se puede repreguntar según conteste |
| Cómo tratar el riesgo por región semilla | Es un vacío de método nuestro, declarado; no es justo mandárselo como pregunta |
| Si se verificó alguna vez que un off-target predicho ocurra | Es retórica: ninguna herramienta que leímos lo valida |
| La discrepancia de nomenclatura de `Rpn6` / PSMD6 (C5) | Demasiado específica para un correo; va a la reunión |
| Acceso institucional a *Pest Manag Sci* 2019 (PMID 30417535) | Es un favor, no una pregunta de método; va al final de otra conversación |
| Distribución de tamaños de ARN pequeños en cicadélidos | Ya la resolvimos corriendo todo a 21 y a 22 nt (D35) |

Las dieciocho completas están en `00_meta/PREGUNTAS_ABIERTAS.md`.

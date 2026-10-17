# Decisiones

Una entrada por decisión, en formato ADR liviano: fecha, decisión, alternativas
consideradas, criterio, consecuencia. Las decisiones de contenido que tomen las
investigaciones se registran acá cuando afectan al proyecto entero; las que son
internas a una investigación quedan en su propio reporte.

---

## D1 — Competir en tres ejes y no en el de biología experimental
**Fecha:** 2026-10-16
**Quién:** el equipo, antes de esta sesión. Se registra acá porque condiciona todo lo demás.
**Decisión:** presentar en los ejes de bioinformática y datos, desarrollo
computacional e innovación abierta, y no en el de biología y evidencia
experimental.
**Alternativas consideradas:** intentar una propuesta con componente
experimental, apoyada en colaboración externa con algún laboratorio.
**Criterio:** cuatro estudiantes de tercer año de Ingeniería en IA, sin
laboratorio húmedo y sin formación formal en biología, no tienen forma de
producir evidencia experimental propia en el plazo del evento. La ventaja
comparativa está en lo computacional.
**Consecuencia:** toda propuesta nuestra tiene que ser demostrable sin un solo
experimento húmedo. Eso convierte la validación retrospectiva contra resultados
ya publicados en el único camino de validación disponible, y vuelve la
disponibilidad de datos públicos el riesgo número uno del proyecto.

---

## D2 — Tratar las notas de la charla como hipótesis numeradas, no como hechos
**Fecha:** 2026-10-16
**Decisión:** lo que el equipo anotó de la charla del investigador invitado se
trata como tres supuestos a verificar, S1 (identidad de los patógenos y qué
síntoma causa cada uno), S2 (qué calcula BLAST y qué calcula la termodinámica) y
S3 (la diferencia entre dsRNA exógeno y ARN no codificante). Cada uno se
confirma o se corrige con fuentes abiertas, y la resolución va explícita en
`SINTESIS.md`.
**Alternativas consideradas:** partir de las notas como base de trabajo y
corregir sobre la marcha.
**Criterio:** son notas de segunda mano de una charla oral. Un error en S2
contaminaría directamente dos de los enfoques candidatos del equipo, porque la
distinción entre alineamiento y termodinámica es la que define qué es la
"función de pérdida" de la que habla la idea del integrante.
**Consecuencia:** R1 y R2 verifican la misma distinción desde ángulos distintos,
lo que es redundancia deliberada y no duplicación de trabajo. Si las dos llegan
a conclusiones distintas, el término queda `[?]` en el glosario.

---

## D3 — Cinco investigaciones en paralelo, con los prompts del repositorio sin modificar
**Fecha:** 2026-10-16
**Decisión:** lanzar exactamente cinco líneas de investigación, una por archivo
de `prompts/`, pasando el texto de cada prompt completo y sin resumir. El
orquestador no ejecuta ninguna de las cinco: integra.
**Alternativas consideradas:** partir las investigaciones más grandes (R1, R4)
en subtareas más chicas para acortar el tiempo de cada una; o ejecutar
secuencialmente para poder encadenar los hallazgos.
**Criterio:** los cinco prompts están escritos con condición de terminación
propia y con verificación propia. Partirlos obligaría a reconciliar fragmentos
sin dueño, y secuenciarlos multiplicaría por cinco el tiempo total sin mejorar
cada reporte, porque las cinco preguntas son en buena medida independientes.
**Consecuencia:** hay solapamiento previsible entre R2 y R4 en los modelos
fundacionales de secuencias, y entre R1 y R3 en el estado del arte de
tratamientos. El solapamiento se resuelve en la integración, no se evita: dos
lecturas independientes de la misma bibliografía son una forma barata de
detectar error.

---

## D4 — El glosario se arma en dos pasadas
**Fecha:** 2026-10-16
**Decisión:** escribir primero el núcleo conceptual de `GLOSARIO.md` desde
consenso de libro de texto, marcado como pendiente de fuente, y fusionar después
los glosarios parciales de las cinco investigaciones agregando la cita.
**Alternativas consideradas:** esperar los glosarios parciales y escribir el
glosario una sola vez.
**Criterio:** el glosario es la pieza que el equipo necesita para poder leer los
reportes. Tenerlo a medias desde el principio es más útil que tenerlo completo al
final, y el costo de la segunda pasada es bajo.
**Consecuencia:** hay entradas que durante un rato dicen "pendiente de fuente".
La regla de `CLAUDE.md` de que toda afirmación lleva fuente se cumple en el
estado final del archivo, no en cada momento intermedio. Lo que no se admite en
ningún momento es una cita reconstruida de memoria.

---

## D5 — Un commit por investigación integrada, más uno final
**Fecha:** 2026-10-16
**Decisión:** las investigaciones no commitean. El orquestador hace un commit por
cada reporte que vuelve y queda integrado, y un commit final con la síntesis y
la portada.
**Alternativas consideradas:** que cada investigación commitee su propia carpeta.
**Criterio:** cinco procesos escribiendo sobre el mismo índice de git al mismo
tiempo se pisan. Y la unidad de trabajo revisable no es "el archivo que escribió
un agente" sino "la investigación integrada al resto de la memoria del
proyecto".
**Consecuencia:** el historial de git se lee como la secuencia de integración, y
cada commit deja el repositorio en un estado coherente entre `research/` y
`00_meta/`.

---

## D6 — El material pesado de referencia queda fuera del control de versiones
**Fecha:** 2026-10-16
**Decisión:** mantener en `.gitignore` los PDF de material de referencia, entre
ellos el de la sesión técnica del Investigathon (unos 45 MB).
**Criterio:** son insumos de lectura, no entregables, y no corresponde empujar
decenas de megabytes a un repositorio de texto.
**Consecuencia:** quien clone el repositorio no recibe ese material. Todo dato
que venga de ahí y se use en un reporte tiene que quedar citado en el reporte,
no solo referenciado al archivo local.

---

## D7 — El aporte del equipo es la priorización auditable, no el diseño ni la entrega
**Fecha:** 2026-10-17
**Quién:** el orquestador, al integrar las cinco investigaciones.
**Decisión:** el eje central de la propuesta es una función de decisión sobre
candidatos *dados* —orden, criterio escrito, evidencia citada e incertidumbre
propagada—, y no el diseño de secuencias nuevas, ni la formulación, ni la vía de
entrega.
**Alternativas consideradas:** atacar la barrera de entrega, que es la que el
organizador declara central; construir una plataforma de diseño de ARN con
chequeo de off-targets; entrenar un modelo de eficacia.
**Criterio:** tres resultados independientes apuntan al mismo lugar. R3 muestra
que el diseño con chequeo de off-targets ya existe y se llama Apolo Rocket, que
la encapsulación está publicada desde 2017 con al menos seis químicas, y que la
co-entrega contra la dsRNasa del insecto la propuso un grupo argentino en 2023:
proponer cualquiera de las tres como novedad sería proponerle a alguien del
EPILAB lo que ya hace. R3 muestra además que el cuello de botella de la entrega
es experimental y de capital, no computacional. Y el propio organizador declara
abierta exactamente la pregunta de priorización: tiene candidatos preliminares y
pregunta cuáles merecen validación y por qué. R2 y R4, que trabajaron por
separado y desde preguntas distintas, llegaron de forma independiente a la misma
propuesta —R2 la llama PRIOR-dsRNA y R4 la llama L1—, lo que es la mejor señal
disponible de que el encuadre es el correcto.
**Consecuencia:** el entregable se juzga por la calidad de la decisión que
produce, no por la novedad del método ni por la interfaz. La línea de base a
superar o a alimentar es dsRIP, que ya hace la mayor parte del cálculo, y
reconocerlo en voz alta es parte de la propuesta. Si el método no le gana a
dsRIP en la validación retrospectiva, el entregable sigue siendo válido y así
está declarado de antemano.

---

## D8 — No se entrena ningún modelo, y eso es una decisión declarada, no una carencia
**Fecha:** 2026-10-17
**Decisión:** no entrenar ni ajustar ningún modelo. El cálculo es una función de
puntuación explícita con coeficientes publicados, más tamizaje por alineamiento,
más cuantificación de incertidumbre. Los datos de fenotipo existentes se reservan
íntegros para validar.
**Alternativas consideradas:** ajuste fino de un modelo fundacional de ácidos
nucleicos (la línea L4 de R4); un cabezal liviano sobre representaciones
congeladas; entrenar sobre los datos humanos de siRNA y transferir.
**Criterio:** el conjunto de entrenamiento honesto que existe en este subcampo
son 31 siRNA probados en un coleóptero, de los cuales 29 entraron al modelo
publicado. No hay nada en Hemiptera. Cuatro evaluaciones independientes —Tang y
Koo en *Genome Biology*, BEND, BEACON y el relevamiento revisado por pares de 21
modelos de ARN— coinciden en que los modelos fundacionales no dan ventaja
consistente fuera de su dominio, y en la tarea medida más parecida a nuestro
tamizaje de off-target rinden la mitad que una red convolucional entrenada desde
cero. Entrenar sobre datos humanos y transferir es lo que la evidencia
desaconseja de forma más directa: el contenido GC en las posiciones 9 a 14 del
antisentido invierte su signo entre humano e insecto.
**Consecuencia:** el cálculo es determinista y reproducible bit a bit, lo que
satisface la palabra «reproducible» de la pregunta del track sin esfuerzo
adicional. Y el único conjunto de validación que existe sigue siendo conjunto de
validación: usarlo para ajustar lo habría quemado. La contracara es que no hay
nada que presentar como «nuestro modelo», y conviene decirlo antes de que lo
pregunten.

---

## D9 — Lo heredado de corridas anteriores se mantiene con su nivel de verificación declarado
**Fecha:** 2026-10-17
**Decisión:** las afirmaciones que vienen de una corrida previa de la misma
investigación se conservan tal como quedaron registradas, con su nivel de
verificación explícito, en lugar de reabrir todas las fuentes.
**Alternativas consideradas:** reabrir y reverificar cada fuente en cada corrida.
**Criterio:** reabrir tiene costo y no agrega información cuando la cita textual
quedó registrada en las notas; lo que sí agrega información es **declarar** qué
se verificó cuándo. El riesgo que importa no es que una fuente vieja esté mal
copiada: es que alguien lea el reporte creyendo que todo se verificó hoy.
**Consecuencia:** hay tres declaraciones vigentes que viajan con los números y
que hay que repetir al presentarlos. R4: 29 de las 52 entradas de `modelos.json`
tienen su especificación tomada de la tabla de un relevamiento revisado por pares
que sí se abrió, y no de su artículo primario; está declarado entrada por entrada
en el campo `nivel_verificacion`, y por eso esa investigación no marca su propia
lista de verificación como aprobada. R5: unas diez fuentes de la sección de
innovación abierta dependen de dominios institucionales que no estaban
disponibles en la última corrida —`argentina.gob.ar`, `embrapa.br`,
`repositorio.inta.gob.ar` y la API de GBIF—, conservan la verificación de la
corrida anterior con sus citas textuales en `notes/evidencia_verificada.md`, y no
se volvieron a comprobar. R1: una parte de las fuentes está marcada `[RES]`,
leída sólo en el resumen, y su hallazgo central sobre la ausencia de maquinaria
de RNAi en mollicutes proviene de una consulta de anotación, no de una búsqueda
por perfil.

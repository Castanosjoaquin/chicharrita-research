# Preguntas abiertas — R1 Fundamentos

Lo que no pudimos resolver con las fuentes que abrimos, lo que habría que
preguntarle al investigador del track, y las contradicciones entre fuentes que
quedaron sin cerrar. Un vacío documentado es un resultado válido; un vacío tapado
con texto plausible, no.

---

## 1. Para preguntarle directamente al investigador (EPILAB · IFIBYNE, UBA–CONICET)

**1.1 ¿Qué significa exactamente "inhibición del crecimiento del patógeno" en el
esquema de la diapositiva?** Es la pregunta más importante de todas. El circuito
oficial de cuatro pasos —diseño del ARNdc dirigido a genes esenciales del
objetivo → pulverización sobre la planta → ingreso y silenciamiento génico →
inhibición del crecimiento del patógeno— no es compatible con lo que
establecimos en la sección 4 del reporte si se lee como silenciamiento directo de
un mollicute. Las tres lecturas posibles son: (a) es una simplificación de la
charla; (b) se refiere a los dos virus, donde el silenciamiento ocurre en la
célula vegetal; (c) implica una vía indirecta —silenciar al vector o preparar la
defensa de la planta—. No asumimos ninguna.

**1.2 ¿Cuáles son los candidatos preliminares del EPILAB y contra qué organismo
están dirigidos?** La propia diapositiva declara que existen candidatos
preliminares y que la pregunta abierta es "¿cuáles merecen validación y por
qué?". Necesitamos saber si están dirigidos al vector, a los patógenos o a la
planta, qué gen blanco tienen, qué largo, y si hay alguna medición asociada.
Todo el valor de una priorización depende de esa respuesta.

**1.3 ¿Qué transcriptoma o anotación de *Dalbulus maidis* usa el laboratorio?**
Existe un transcriptoma publicado con 56.116 transcriptos `S19`, pero necesitamos
saber cuál es el conjunto de referencia que el laboratorio considera válido, y si
hay una anotación funcional asociada. Sin eso no hay análisis de off-target
posible.

**1.4 ¿Qué especies no objetivo considera relevantes el laboratorio para el
agroecosistema del maíz argentino?** El minimizador de off-targets necesita una
lista explícita de transcriptomas contra los cuales cotejar. ¿Polinizadores?
¿*Anagrus virlai* y los parasitoides de huevo? ¿Fauna del suelo? ¿Qué especies
tienen transcriptoma público y cuáles habría que sustituir por un pariente?

**1.5 ¿Qué formato de disparador se considera viable: dsRNA largo, dúplex
predefinido o siRNA de 24 nt para RdDM?** La diapositiva ordena cuatro niveles de
precisión creciente, y marca con un signo de pregunta la participación de DCL3.
Saber en cuál de esos niveles se posiciona el laboratorio cambia por completo qué
hay que calcular.

**1.6 ¿Mide el laboratorio knockdown, mortalidad, o transmisión?** La sección 5
del reporte muestra que la acumulación del patógeno no predice el daño `S45` y
que la generación de siRNA no prueba protección `S43`. Si vamos a priorizar
candidatos, necesitamos saber contra qué variable medida se van a validar.

---

## 2. Huecos de la literatura que no pudimos llenar

**2.1 No hay ningún trabajo de dsRNA, SIGS o HIGS contra MRFV ni contra MSMV.**
Buscamos específicamente y no encontramos nada. Los precedentes antivirales más
cercanos que sí pudimos abrir son, en maíz, el dsRNA contra la cápside del
*sugarcane mosaic virus*, y, para virus de ADN, la "vacunación" con dsRNA contra
*tomato yellow leaf curl virus* `S43`. Ninguno de los dos es nuestro patógeno.
Vacío real, no imposibilidad.

**2.2 No hay perfil de largo de siRNA para ningún hemíptero.** El trabajo que
establece que el largo del siRNA es específico de orden —20 nt en lepidópteros,
21 en dípteros y coleópteros, 22 en himenópteros y ortópteros— **no reporta
ningún hemíptero** `S50`. Si nuestro pipeline enumera 21-meros, está asumiendo un
parámetro que nadie midió en la chicharrita.

**2.3 No conseguimos la variabilidad poblacional de secuencia de *D. maidis*.**
Para los patógenos sí hay datos (espiralina de *S. kunkelii* con 98 % de
similitud entre aislamientos brasileños, 16S rDNA del fitoplasma completamente
similar `S12`), pero para el vector no abrimos ninguna fuente con diversidad de
secuencia a nivel de transcrito. Sin eso, el término de "conservación entre
poblaciones del objetivo" del diseño no se puede calcular con datos propios.
Existen trabajos de diversidad genética de poblaciones sudamericanas de
*D. maidis* que aparecieron en la búsqueda pero cuyo texto no pudimos abrir
(*Neotropical Entomology*, 2025, sin acceso abierto).

**2.4 No pudimos abrir el texto completo del preprint de RNAi oral en
*D. maidis*** `S18`. Tenemos el resumen, que reporta expresión reducida de las
subunidades B y D de la ATP sintasa vacuolar con mortalidad significativamente
mayor y deformación de alas, pero no las dosis, los tiempos ni los tamaños de
muestra. Es, además, un preprint sin revisión por pares.

**2.5 No pudimos abrir el trabajo brasileño sobre pérdidas económicas del
complejo.** "A disease complex: crop losses and economic impact of corn stunt
diseases on Brazilian corn production", *Crop Protection*, 2026, DOI
10.1016/j.cropro.2026.107549: sin versión de acceso abierto por ninguna de las
vías probadas (Unpaywall, Semantic Scholar, PMC, TDM de Crossref). Sería la
fuente primaria más directa sobre magnitud económica.

**2.6 No hay datos de vida media del dsRNA en hoja ni en suelo en los términos
que necesitaríamos.** La revisión de SIGS para protección de cultivos no da
valores de vida media y marca explícitamente la persistencia en suelo y el
ingreso a la cadena alimentaria como pregunta abierta para organismos no objetivo
`S07`. Lo que sí hay son cotas operativas: una hora de UV abole la actividad y
más de 20 mm de lluvia en 24 h lavan una proporción significativa del depósito
`S43`.

**2.7 No existe un panel curado de off-targets para el agroecosistema del maíz
argentino.** Es un hueco de datos, no de literatura, y condiciona directamente
cualquier término de seguridad que propongamos.

---

## 3. Contradicciones entre fuentes que quedan abiertas `[?]`

**3.1 Modo de transmisión del MSMV.** Un trabajo de Embrapa afirma que todos los
agentes del complejo se transmiten de manera persistente propagativa "excepto
MSMV, que se transmite de manera persistente circulativa" `S46`. Un trabajo
argentino del mismo período declara que el modo de transmisión del MSMV sigue
siendo desconocido `S47`. La diferencia importa: circulativa implica que el virus
**no se multiplica** en el insecto, y eso cambia qué genes del insecto podrían
bloquear esa transmisión en particular.

**3.2 Magnitud de la pérdida en la campaña argentina 2023/2024.** Tenemos tres
cifras incompatibles y ninguna rastreada hasta su fuente primaria:
una reducción estimada del **20 %** de la producción nacional, citada en un
artículo revisado por pares como cita secundaria de la Bolsa de Comercio de
Rosario (2024) `S47`; una reducción del **77 %**, citada también de manera
secundaria en una revisión de control biológico `S22`; y las cifras de **11,5
millones de toneladas** y **2.045 millones de dólares** de la diapositiva oficial
del Investigathón, sin rótulo que aclare qué mide cada una. Antes de poner
cualquiera de estos números en una presentación hay que decidir cuál se usa y con
qué atribución. Nuestra recomendación es usar el 20 % con la cadena de atribución
explícita, o declarar el rango.

**3.3 Dirigir el extremo 3′ del transcrito.** Funcionó mejor en un estudio en
mosquito y no funcionó en el pulgón del guisante `S08`. No hay regla.

**3.4 Accesibilidad estructural del sitio blanco.** Es un filtro que mejora la
correlación con datos experimentales en el diseñador si-Fi, validado en plantas
`S05`, y **no resultó estadísticamente significativa** en el análisis de eficacia
en insectos de dsRIP `S06`. Para nuestro caso —un insecto— el peso de este
término es incierto.

---

## 4. Preguntas que nuestra propia verificación deja abiertas

**4.1 La consulta a UniProtKB es una consulta de anotación, no un análisis de
genoma.** Contamos proteínas anotadas con los dominios PIWI, PAZ y de
dimerización de Dicer en Mollicutes, *Spiroplasma*, *S. kunkelii* y *'Candidatus*
Phytoplasma', y el resultado fue cero en todos los casos, con control positivo de
RNasa III `D01`. El cero es sólido porque hay 126.874 proteínas de mollicutes
anotadas y porque el control da positivo, pero el procedimiento riguroso sería
una búsqueda por perfil (HMM de los dominios InterPro contra los proteomas
completos, o tblastn contra los genomas) para descartar genes no anotados o
pseudogenizados. No lo hicimos: la consulta por anotación fue suficiente para la
decisión estratégica, y el trabajo de perfiles queda como tarea pendiente si
alguien quiere publicar la afirmación.

**4.2 ¿Hay alguna vía no canónica por la cual un ARN exógeno afecte a un
mollicute?** No la buscamos exhaustivamente. Lo que descartamos es el RNAi
canónico. Quedan sin explorar mecanismos del tipo oligonucleótido antisentido,
interferencia con ARN regulatorios bacterianos propios, o efectos sobre la
expresión mediados por la planta. No tenemos evidencia ni a favor ni en contra, y
cualquier afirmación en esa dirección sería especulación.

**4.3 ¿El fitoplasma coloniza el citoplasma de las células cribosas del floema?**
Lo tomamos de la introducción de una revisión `S44`, que a su vez lo cita de
terceros. Es coherente con el resto de la literatura que abrimos, pero no
rastreamos la fuente primaria.

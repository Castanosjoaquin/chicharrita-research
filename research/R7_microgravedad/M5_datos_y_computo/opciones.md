# opciones.md — Qué podría hacer y demostrar el equipo sin laboratorio con datos de vuelo y cómputo (M5, R7)

Corte: 2026-10-19. Todas las horas son estimaciones del equipo `[H]` sobre el presupuesto de 96 horas-persona de `SINTESIS_V2.md` (reparto P1 12 h, P2 30 h, P3 26 h, P4 28 h). Los tamaños salen de los listados de archivos de OSDR y de las descargas de GEO registradas en `datos/COMANDOS.md`; **ningún archivo de datos de OSDR se pudo descargar** (el host de almacenamiento no está en la lista permitida), de modo que donde dice «medido» se refiere a tamaños y nombres de archivo, no a contenido.

## Criterio de orden

Las opciones se ordenan por cuatro criterios aplicados en este orden: (1) cumplir D1 (demostrable sin experimento húmedo) y D7/D8 (priorización auditable de candidatos dados; no entrenar modelos) sin reinterpretarlas; (2) costo en horas-persona frente a lo que mueve L1 (priorización auditable), L2 (validación retrospectiva) o L3 (riesgo off-target); (3) qué ofrece al eje de innovación abierta; (4) riesgo de que el resultado sea no concluyente o se malinterprete. Una opción que pasa (1) pero no mueve L1–L3 queda condicionada a que L1–L3 ya tengan su primera corrida punta a punta. **Ninguna opción de este reporte mueve L1, L2 ni L3 de forma directa**; la que más se acerca lo hace a L3 por una vía lateral, y está descrita al final del reporte como idea no evaluada.

---

## Opción 1 — Paquete «vacío documentado» de datos de vuelo (recomendada)

**Qué es.** Entregar, como anexo del paquete de apertura de la rama P4, el inventario auditable del OSDR con su consulta reproducible y los ceros verificados contra NCBI: *Zea mays* 0, Hemiptera 0, mollicutes 0 y ARN pequeño en plantas, insectos y microbios 0, sobre 642 estudios OSD (índice del 2026-10-19), más los hallazgos fuera del OSDR (maíz en la ISS en PRJDB11348, arroz en GSE78839).

**Datos requeridos y dónde están.** Ya existen en esta carpeta: `inventario_osdr.json` (155 entradas), `datos/osdr_search/consultas_osdr.json` (93 consultas), los volcados comprimidos del índice (`volcado_type_cgene.json.gz`, 1,6 MB, y `volcado_type_alsda.json.gz`, 0,3 MB) y `files_summary_todos.json` (listados de los 642 OSD). Peso total de lo que hay que mover: unos 4 MB comprimidos. No requiere descargar datos de OSDR.

**Entregable demostrable.** Un script único que reproduzca los conteos desde cero (hoy son tres scripts de listados y metadatos más celdas interactivas para la batería de términos), una tabla de ceros con la consulta y el filtro de cada uno, y un README que declare los límites (índice sin taxid; ceros por texto y organismo; licencia por estudio sin verificar: dos fragmentos del OSDR muestran CC0-1.0, pero no se revisaron los 155).

**Control y qué se concluye.** Control: reproducir los conteos con una segunda ejecución independiente y comparar. Se puede concluir qué hay y qué no hay en el índice a la fecha, con la consulta que lo respalda. No se puede concluir que no existan datos de vuelo de esos organismos fuera de los repositorios consultados.

**Riesgo.** Bajo. El riesgo real es de lectura: un jurado puede tomarlo por «no encontraron nada» y no por «medimos que no hay y dejamos la consulta». Se mitiga con el encabezado del README.

**Horas.** 4 a 6 h `[H]` (4 a 6 % de las 96), dentro de las 28 h de P4.

**Encaje.** No entra en la pregunta oficial del track. No alimenta L1, L2 ni L3. Ofrece algo concreto al eje de innovación abierta: un conjunto de datos y una consulta reutilizables por otros equipos del track, y un ejemplo de resultado negativo documentado. Es la opción de menor costo y mayor valor relativo, y su valor absoluto es modesto.

---

## Opción 2 — Chequeo acotado de maquinaria de silenciamiento y de defensa en transcriptomas de vuelo de plantas (condicionada)

**Qué es.** Preguntar si los genes de la maquinaria de silenciamiento de la planta (Argonauta, Dicer-like, RDR y asociados) y marcadores de defensa cambian de expresión entre vuelo y control, en conjuntos públicos que **sí** tienen un control de 1 g en vuelo. Es la pregunta que M3 dejó explícitamente «no evaluada a esta profundidad» (DCL, AGO y RDR en GeneLab).

**Datos requeridos, con id y tamaño.** Dos variantes de alcance.
*Variante 2a (mínima).* OSD-437 (*Arabidopsis*, ISS, SpaceX-9, EMCS, 19 muestras, factores edad, gravedad alterada y vuelo): tabla de conteos STAR sin normalizar de 2,31 MB y tabla normalizada de 7,26 MB; y GSE78839 (arroz, 10 arrays: 4 de vuelo, 3 de control de 1 g en vuelo, 3 de control en tierra, 57.381 sondas): matriz de 2,78 MB y anotación de plataforma GPL2025 de 1,51 MB, **ya descargadas** (4,3 MB en total).
*Variante 2b (ampliada).* A lo anterior se suman OSD-678 (36 muestras; conteos de 4,49 MB), OSD-427 (48 muestras; 5,87 MB), OSD-120 (90 muestras; 4,03 MB) y OSD-37 (56 muestras; 6,0 MB). Los conteos sin normalizar de los cinco estudios de *Arabidopsis* suman unos 23 MB. **No** hay que bajar las tablas de expresión diferencial (51 a 272 MB cada una) ni las lecturas crudas (59 a 413 GB por estudio).

**Medido.** En el arroz de GSE78839 el array GPL2025 trae 46 sondas candidatas (17 de Argonauta/PIWI/PAZ, 5 de Dicer, 5 de RDR y 19 de otros componentes por texto de anotación), todas presentes en la matriz; solo 23.850 de las 57.381 sondas tienen anotación, así que la cobertura es incompleta. La lista está en `datos/gse78839_sondas_silenciamiento.tsv` y no está curada. No se calculó expresión.

**Pasos.** (1) Fijar la lista de genes por símbolo y ortología con anotación pública, sin diseñar secuencias. (2) Leer la tabla de muestras de cada estudio y definir el contraste vuelo contra 1 g en vuelo (o control en tierra donde no haya centrífuga). (3) Estimar log2FC por gen y estudio con el método estándar para conteos (o limma para arrays). (4) Combinar estudios con un modelo de efectos aleatorios y covariables de plataforma y de tipo de ensayo. (5) Informar el tamaño de efecto con intervalo, nunca solo el valor p.

**Control.** Dos controles obligatorios: conjuntos aleatorios de genes igualados en nivel de expresión (1.000 réplicas) para calibrar cuánto se mueve un conjunto de ese tamaño por azar, y permutación de las etiquetas de vuelo dentro de cada estudio. Sin ellos, un cambio de un puñado de genes es indistinguible del ruido de una comparación con n = 3 o 4.

**Qué se puede concluir.** Si la expresión de esos genes se desvía de lo esperado por azar, en qué sentido y con qué consistencia entre estudios. **Qué no.** Que la eficacia de un dsRNA exógeno cambie en vuelo: la expresión de la maquinaria no es su actividad (M2 cita un único experimento primario de RNAi en vuelo, en *C. elegans*, sin cambios en 16 genes de la maquinaria). Tampoco se concluye nada sobre maíz: *Arabidopsis* y arroz no son maíz. Y el metaanálisis de *Arabidopsis* (M5-29) muestra que el tipo de ensayo y el hardware pueden pesar más que el vuelo, así que una diferencia entre estudios no es un efecto de la microgravedad.

**Riesgo.** Medio a alto. Confusión de hardware y ensayo (M5-29); n de 3 a 4 por grupo en GSE78839; ninguna conexión con la pregunta oficial; y el riesgo de que un resultado «significativo» se lea como relevante para el RNAi exógeno, que no lo es.

**Horas.** 2a: 10 a 12 h `[H]` (10 a 13 % de las 96). 2b: 24 a 30 h `[H]` (25 a 31 %). Sería sacarlas de P4 o de P3 y, por lo tanto, de la herramienta.

**Encaje.** No entra en la pregunta oficial. No alimenta L1, L2 ni L3. Para innovación abierta ofrece un cuaderno reproducible con un resultado pequeño y honesto sobre un hueco que M3 señaló. **Recomendación:** no gastar horas de L1–L3; hacerla solo (a) si P1–P4 ya cerraron la primera corrida punta a punta, (b) en la variante 2a, y (c) si el investigador del EPILAB responde que la maquinaria de silenciamiento de la planta les importa (pregunta 1 de `preguntas_pendientes.md`). Para la variante 2b faltaría además acceso al host de almacenamiento de OSDR, que hoy no está permitido.

---

## Opción 3 — Extensión de la opción 2 al maíz (PRJDB11348), condicional a acceso

**Qué es.** Repetir la opción 2a sobre el único conjunto de expresión de maíz en microgravedad real que se encontró: PRJDB11348, microarray Agilent (Design ID 016047) de plántulas etioladas de *Zea mays* cv. Golden Cross Bantam crecidas en la ISS frente a 1 g en Tierra. La descripción coincide con el experimento «Auxin Transport» (ISS, módulo JEM, 2016 y 2017), cuyos resúmenes (M5-20 a M5-22) describen maíz Golden Cross Bantam con un control de 1 g por centrífuga en vuelo; el vínculo entre el BioProject y esos artículos es inferido `[?]`.

**Datos requeridos.** El archivo de expresión del microarray. No se pudo localizar: la consulta de enlaces de NCBI de BioProject hacia GEO, SRA y BioSample devuelve vacío, y el DDBJ no es accesible desde este entorno. Tamaño desconocido; un microarray de este tipo suele pesar megabytes `[H]`.

**Entregable.** La misma tabla de la opción 2 para maíz, con una limitación adicional: hay que mapear las sondas del array a genes de maíz (anotación de plataforma que no se tiene verificada).

**Riesgo.** Alto, por incertidumbre de acceso y de anotación. **Horas.** 8 a 12 h adicionales `[H]` si los datos son accesibles; 0 si no. **Encaje.** Mismo que la opción 2; la única ventaja es que es el cultivo del track.

---

## Opción 4 — Reanálisis de los cereales del OSDR: *Brachypodium* OSD-375 y trigo OSD-622 (descartada)

**Qué sería.** Hacer la opción 2 con los dos cereales de vuelo del OSDR en vez de *Arabidopsis*.

**Por qué se descarta.** OSD-375 (*Brachypodium distachyon*, ISS, 48 muestras de RNA-seq) tiene en el listado de OSDR solo lecturas crudas (96 archivos FASTQ, unos 463 GB) y un informe MultiQC de 2,2 MB: no hay tablas de conteos listadas. Reanalizarlo exige descargar y alinear 463 GB, fuera de una notebook de 16 GB y del tope de 1 GB de esta tarea. OSD-622 (trigo enano, ISS, 11 muestras, microarray de 2006) pesa 27,7 MB, pero son archivos `.xls` y documentos sin formato estándar, con etiquetas de categoría imprecisas (los «raw array data» son documentos, no archivos CEL), y no se pudo descargar para comprobar si el array tiene sondas de silenciamiento. Para el mismo propósito, GSE78839 (arroz) está mejor documentado y ya se midió. **Horas ahorradas:** 10 a 20 h `[H]` de intentar lo inviable.

---

## Opción 5 — Dinámica molecular con gravedad alterada (descartada)

**Qué sería.** Simular proteínas o ARN de los mollicutes o del vector con un término de gravedad distinto de 1 g para ver cambios de estructura o estabilidad.

**Por qué se descarta.** No se encontró ningún estudio que lo haga (Europe PMC y búsqueda web; el único cruce de «dinámica molecular» con microgravedad, M5-25, simula estructuras cristalinas ya depositadas, crecidas en el espacio y en la Tierra, y no incluye un término de gravedad). Un cálculo propio de orden de magnitud `[H]` (`datos/calculo_gravedad_escala_molecular.txt`) da, para una proteína de 50 kDa, una energía gravitatoria de unos 8×10⁻³⁰ J al desplazarla 10 nm, es decir unos 2×10⁻⁹ veces la energía térmica kB·T a 300 K; para un cristal de 100 µm el número de Péclet de sedimentación es del orden de 10⁷. Con esos valores de entrada (supuestos y declarados), la gravedad es irrelevante a escala molecular y decisiva a escala de cristal y de fluido: una simulación molecular «con gravedad» no puede mostrar nada. Además no mueve L1–L3. **Horas ahorradas:** 20 a 40 h `[H]`.

---

## Opción 6 — ML de cristalizabilidad o estabilidad sobre proteínas del mollicute o del vector (descartada)

**Qué sería.** Aplicar un predictor de cristalizabilidad (por ejemplo modelos de lenguaje de proteínas) a las proteínas de *Spiroplasma kunkelii* o *Ca.* Phytoplasma zeae, o entrenar uno.

**Por qué se descarta.** Los predictores existen y se evaluaron con seriedad en tierra (M5-28: ganancia de 3 a 5 % en AUPR, AUC y F1 sobre predictores anteriores, en conjuntos de prueba independientes), pero ninguno incluye la microgravedad como variable (el texto no menciona el término), así que no predicen qué se beneficiaría de ella; el único indicio de una predicción así es una frase de un resumen sobre agregados de proteína (M5-26), no un modelo. Entrenar uno viola D8 (decisión de no entrenar modelos); usar uno ya entrenado es una demostración sin decisión que dependa de ella, y no se puede validar sin cristalización experimental (D1). La rama M4 del mismo R7 concluye, por otra vía, que 0 de 16 blancos funcionales de los dos mollicutes tienen la necesidad que justificaría cristalizar en microgravedad. **Horas ahorradas:** 15 a 30 h `[H]`.

---

## Opción 7 — Ajuste fino de un modelo fundacional con datos de vuelo (descartada)

**Qué sería.** Afinar un modelo fundacional de transcriptomas, ARN o proteínas con los conjuntos del OSDR.

**Por qué se descarta.** Viola D8 y es la línea L4 de `SINTESIS_V2.md` (puntaje 5 de 20). Además los datos no alcanzan: los 24 estudios de planta de vuelo con RNA-seq tienen una mediana de 36 muestras de tabla por estudio, con diseños distintos; los metaanálisis publicados encuentran que la varianza viene sobre todo del diseño experimental (M5-30 en bacterias, M5-29 en *Arabidopsis*); y una perspectiva reciente de los propios equipos del OSDR (M5-31) considera poco realista preentrenar un modelo fundacional espacial desde cero y cita como precedentes casos terrestres. No se encontró ningún modelo fundacional de ARN o proteínas usado con datos de vuelo (búsqueda web 6). **Horas ahorradas:** 30 h o más `[H]`.

---

## Resumen de horas

| opción | estado | horas `[H]` | % de 96 h | mueve L1 / L2 / L3 |
| --- | --- | ---: | ---: | --- |
| 1. Paquete de vacío documentado | recomendada | 4–6 | 4–6 | no / no / no |
| 2a. Silenciamiento y defensa, mínima | condicionada | 10–12 | 10–13 | no / no / no |
| 2b. Silenciamiento y defensa, ampliada | no recomendada | 24–30 | 25–31 | no / no / no |
| 3. Extensión a maíz (PRJDB11348) | condicional a acceso | +8–12 | +8–13 | no / no / no |
| 4. Cereales OSD-375 y OSD-622 | descartada | 0 | 0 | — |
| 5. MD con gravedad alterada | descartada | 0 | 0 | — |
| 6. ML de cristalizabilidad | descartada | 0 | 0 | — |
| 7. Fine-tuning de modelo fundacional | descartada | 0 | 0 | — |

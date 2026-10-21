# Notas para la memoria del proyecto — C3 (ola 3)

Para que el orquestador integre a `00_meta/`. No tocamos `00_meta/` ni los REPORT.md de otras
investigaciones.

## Decisiones candidatas para DECISIONS.md

**D-C3-1. El tamizaje de off-targets por ventana no se hace con BLAST, y ahora hay número.**
Medimos que ninguna de trece configuraciones de BLAST+ 2.17.0 recupera un 21-mero con un
desajuste en las 21 posiciones: el techo es 0,762 con `-task blastn` y 0,619 con cualquier
`blastn-short`. La causa no es el tamaño de palabra sino el modelo de puntaje, que recorta
desajustes cercanos a los extremos. Confirma por medición la decisión ya vigente de usar
coincidencia exacta (`offtarget_21nt.py`) o Bowtie. Consecuencia: si en algún entregable se usa
BLAST para esto, hay que declarar el sesgo por posición.

**D-C3-2. Si hay que usar BLAST igual, la configuración es `blastn-short` con `-word_size 10`.**
Es el máximo tamaño de palabra que no pierde la posición 11 (el umbral exacto es
⌊(21−1)/2⌋ = 10) y es ~19 veces más barato que palabra 7 sin perder sensibilidad. Va con
`-ungapped -dust no -soft_masking false -evalue 1000 -max_target_seqs 5000` y postfiltro
obligatorio por `length` y `mismatch`. Alternativa descartada: `blastn-short` por defecto
(palabra 7), que da lo mismo y cuesta veinte veces más.

**D-C3-3. No entregar la región de 200 nt como un argmax.** El benchmark de 21 contra 22 nt
muestra que en los dos genes largos la región ganadora se muda de lugar del gen al cambiar un
nucleótido el largo de ventana (BicC_Dm: la ganadora a 21 nt queda 166.ª a 22 nt). Propuesta:
entregar el conjunto de regiones que están en el top-5 con los dos largos, y declarar el
solapamiento por nucleótidos cubiertos (0,74-0,83) como medida de estabilidad.

**D-C3-4. Umbral mínimo de coincidencia contigua: 21 nt con ≤1 desajuste, más 19 nt perfecto.**
Con el argumento cuantitativo de Q3: a 19 nt el azar explica el total de coincidencias
(observado/esperado = 1,0) y son 25 coincidencias sobre 4.730 ventanas en un genoma de 972 Mb;
a 16 nt son 1.979 y todas son azar por construcción del control. No reportar coincidencias de
16-18 nt como off-targets.

## Caminos probados, para CAMINOS_PROBADOS.md

- **Medir el tamaño de palabra con fondos de alfabeto disjunto sin `-strand plus`: falla.** Si
  la consulta tiene fondo de {A,C} y el sujeto de {G,T}, la hebra menos de la consulta es {T,G}
  y calza con el fondo del sujeto. Hay que agregar `-strand plus`. Nos costó una corrida.
- **`blastdbcmd` sobre las bases de W5 para muestrear k-meros: inviable.** Las bases se
  construyeron sin `-parse_seqids`, así que `blastdbcmd -entry all` devuelve
  `gnl|BL_ORD_ID|n` mientras `blastn` reporta la accesión real, y la extracción por `-entry`
  no termina en tiempo razonable. Se cambió a muestrear directamente de los FASTA de
  `work/W5/ref/`, que además da el identificador que después hay que cruzar.
- **Derivar el modelo de hueco de `megablast` con un par apertura/extensión entero: no cierra.**
  Los puntajes de deleciones de 1, 2 y 3 nt (57, 54, 50) son incompatibles con cualquier modelo
  afín entero; un costo lineal de 2,5 por posición los reproduce los tres con truncamiento.
- **Lanzar trabajos largos con `nohup ... &` dentro de una celda corta: se mueren.** Dos
  corridas de Q3 se cortaron a mitad del genoma porque la celda terminó antes. Hay que lanzar
  el comando en primer plano dentro de una celda en segundo plano.
- **Semilla del barajado derivada de `hash()` de Python: no reproducible** entre procesos
  (`PYTHONHASHSEED` es aleatorio). Cambiado a una semilla determinista. Si alguien compara
  números de Q3 con una versión anterior del TSV, puede ver diferencias de ±2 coincidencias en
  el control barajado.

## Preguntas abiertas, para PREGUNTAS_ABIERTAS.md

Para el investigador:

1. **¿«HCP» era «HSP»?** Nuestra lectura es que sí, pero HSP no es un parámetro sino la unidad
   de resultado. ¿Se refería a `-max_hsps` / `-qcov_hsp_perc`, o directamente al E-value o al
   percent identity? La diferencia cambia qué le recomendamos configurar.
2. **¿Tiene dato de distribución de tamaños de ARN pequeños en algún cicadélido?** No
   encontramos ninguno, ni para *Dalbulus maidis* ni para la familia. El hemíptero mejor
   caracterizado (mosca blanca) apunta a **22 nt**, no a 21, y el marco de referencia del campo
   (Santos 2019) no incluye Hemiptera. Si no hay dato, ¿corremos todo a 21 y a 22 y entregamos
   las dos?
3. **¿Cómo quiere que tratemos el riesgo de off-target por región semilla?** Necesita 6-8 nt de
   complementariedad, así que ningún umbral de largo entre 16 y 21 nt lo tamiza. Hoy es un vacío
   de método declarado.
4. **¿Usan el BLAST web con sus valores por defecto para verificar off-targets?** Si es así,
   contra algo del tamaño de un genoma el resultado es **cero por construcción**: Megablast con
   palabra 28 no puede sembrar una consulta de 21 nt, y Expect 0,05 descarta los HSP de 20-21 nt
   contra una base grande.

Metodológicas, nuestras:

5. **Los k ≥ 21 de Q3 no son interpretables** (0 a 4 coincidencias contra esperados de 0,05 a 2).
   Para medir el exceso a 21-22 nt haría falta un conjunto de consultas mucho más grande o un
   catálogo de referencias mucho mayor.
6. **La regla de nucleótidos terminales del port a 22 nt es una generalización, no una regla
   validada**: mira el tercero desde el final. Nadie publicó esa regla para 22 nt.
7. Los dos datos de Hemiptera que no son mosca blanca (psílido 21 nt, delfácido 21-22 nt) están
   citados vía revisión. Si el largo de ventana se vuelve una decisión de diseño, conviene abrir
   los primarios.

## Fuentes nuevas, para FUENTES.md

Las once externas están en `sources.json` con su nivel de acceso y el motivo de cada descarte.
Las cuatro que sostienen Q2 y que vale la pena incorporar a la bibliografía consolidada:

- Santos et al. 2019, *Viruses* 11:738 (`10.3390/v11080738`) — la fuente experimental del largo
  por orden de insecto. **No incluye Hemiptera.**
- Zotti et al. 2026, *Viruses* 18:285 (`10.3390/v18030285`) — la correlación estructural; es
  modelado por homología. **Tampoco incluye Hemiptera.**
- Mondal, Brown y Flynt 2020, *Life Sci Alliance* 3:e202000731 (`10.26508/lsa.202000731`) — el
  único dato de Hemiptera de primera mano que abrimos: pico de Dicer en **22 nt** en mosca
  blanca, y piRNA más abundantes que siRNA.
- Sattar y Thompson 2016, *Front Plant Sci* 7:1241 (`10.3389/fpls.2016.01241`) — inventario de
  ARN pequeños en Hemiptera; de ahí sale que para Cicadellidae no hay distribución de tamaños.

## Bloqueos y rechazos registrados

- **Bloqueo de acceso (registrado, no esquivado).** El apéndice de parámetros del manual de
  BLAST+ (`www.ncbi.nlm.nih.gov/books/NBK279684/`) devuelve una página de reCAPTCHA a un cliente
  programático. No se falseó el user-agent ni se usó espejo ni proxy. No se pidió acceso de red
  porque el dominio no está bloqueado por el entorno: es el servidor el que verifica. Se
  reemplazó por medición directa sobre el binario, que además es mejor evidencia.
- **Dos artículos cerrados** (Macrae 2006, Jackson 2006): sólo resumen. Declarado en cada uso.
- **Ningún rechazo de filtro de seguridad** en esta investigación.
- **Ningún contenido con aspecto de inyección de prompt** en lo que abrimos (papers, páginas de
  documentación, listados FTP).

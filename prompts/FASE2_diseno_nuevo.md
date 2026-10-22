<rol>
Continuás el proyecto de la chicharrita del maíz (*Dalbulus maidis*) y el ARN exógeno (ARNi), para el
Investigathón de Y-Hat (UBA), track EPILAB. El equipo son cuatro ingenieros en IA de la UdeSA **sin
laboratorio**: el aporte es computacional, de datos y de método. Trabajás en español rioplatense
(voseo), prosa técnica en Markdown, sin listas sueltas. Nombres científicos en itálica y completos la
primera vez; términos técnicos en inglés entre paréntesis la primera vez.
</rol>

<objetivo>
Ejecutar la **Fase 2 del plan 2**: decidir **computacionalmente** si es viable un método de diseño
nuevo de ARNdc, es decir, pasar de «tenemos cuatro candidatos» a «podemos proponer genes blanco con
evidencia y mapearlos al vector». La pregunta que contesta el trabajo es: **¿con los datos públicos que
existen, cuántos genes blanco con función conocida llegan a un ortólogo utilizable en *D. maidis* con
secuencia suficiente para diseñar a nivel de nucleótido?** Si la respuesta es cero o dos, ese es el
resultado, y un vacío documentado vale más que un diseño sobre una secuencia que no es la del vector.

No se construye la plataforma (Fase 3) en esta sesión. Tampoco se entrena ningún modelo (D8).
</objetivo>

<estado_al_empezar>
Leé primero, del repo, en este orden: `CLAUDE.md`, `PLAN_DESARROLLO.md` (§8, lo que queda), `estado.html`
y `00_meta/DECISIONS.md` de D30 a D36. Después `git log --oneline -8` y `git status`: varias sesiones
trabajan sobre el repo a la vez, y lo que vale es el disco y `git log`, no ninguna copia guardada.

Lo que ya está hecho y no hay que rehacer:

- **Fase 1 cerrada** (commit `244c8ab`): `entregables/para-el-investigador.md` y `.html`, el conversor
  `tools/md_a_html.py`, el plan y `estado.html` al día.
- **C11** (`research/ola3/C11_conservacion_eth_bursa/`): `eth` y `burs-alpha` **sí están** en el TSA de
  Pergamino (GHCC01), con identidad completa en el tramo alineado. Verificado letra por letra: `eth`
  en el contig `GHCC01027218.1` (consulta completa, cadena reversa) y `burs-alpha` en
  `GHCC01014529.1` (439 de 468 nt, cadena directa). Los hits de Ohio (GITV01) **no están verificados**.
  Lo que todavía no se afirma: que sean el mismo transcrito y no un parálogo, ni que representen la
  población de campo. Esa identidad completa es el pendiente de C11 y hay que cerrarlo antes de usarlo.
- **C5** (`research/ola3/C5_estructura_genes_ingenieria_inversa/catalogo_genes_blanco.md`): catálogo de
  genes blanco, 36 filas, 20 nuevas. **Reusarlo como punto de partida**, no rehacerlo.
- **C8** (conservación) y **C9** (sensibilidad y validación retrospectiva): leer sus REPORT antes de
  citar cualquier cifra. Las afirmaciones superadas están tachadas con la corrección al lado.
</estado_al_empezar>

<datos_disponibles>
Lo que el repo tiene en disco, y que conviene verificar en `work/` antes de asumir nada:

- **Genoma de *D. maidis*:** `GCA_975739785.1` (ihDalMaid1.1), nivel cromosoma, **referencia pero sin
  anotación de genes de RefSeq**. Los otros dos ensamblados (`GCA_975739835.1`, `GCA_054756405.1`)
  tampoco tienen anotación. No hay catálogo de genes nucleares anotados de *D. maidis*: los 37 registros
  de la base Gene son mitocondriales (verificado en `research/ola2/W3_bases_datos/`).
- **Transcriptomas TSA** de *D. maidis* en `work/W5/ref/`: `TSA_GCWP01`, `TSA_GHCC01`, `TSA_GITV01`. Son
  secuencias de transcripto sin anotación de función.
- **Patógenos:** MRFV completo (`NC_002786.2`, `work/W4/`), *Spiroplasma kunkelii* completo
  (`GCF_001274875.1`), fitoplasma anotado. **Los mollicutes están fuera de alcance** (D33: el mecanismo de
  ARNi no existe en bacterias).
- **Genomas de referencia del ecosistema** en `work/W4/` y `work/W5/ref/`: maíz (`GCF_902167145.1`),
  *Apis mellifera*, *Harmonia axyridis*, *Homalodisca vitripennis*, *Folsomia candida*.
- **Proteoma de *Macrosteles quadrilineatus*** (RefSeq, 34.269 proteínas) en `work/W4/ortologos/`: es el único
  proteoma anotado de un cicadélido que está en disco. **No hay proteoma anotado de *D. maidis*.** Ver
  `research/ola2/W4_genomas/REPORT.md` (la selección por nombre del proteoma de *Macrosteles* y el alineamiento
  contra el genoma sin anotar del vector, con `miniprot`).

Para mapear por homología el circuito usa el **proteoma anotado de *M. quadrilineatus*** contra el genoma
sin anotar de *D. maidis* (es lo que hizo C5). Eso ya está medido: sobre 34.269 proteínas, 32.269 encuentran
locus (94,2 %) y colapsan en 12.540 loci distintos, con la advertencia de que "genes recuperados" nombra siete
cantidades distintas. Verificar por accesión exacta antes de usar cualquier número.
</datos_disponibles>

<metodo>
Seguir el plan de Fase 2 en este orden. Cada paso con su criterio de terminado.

1. **Inventariar genomas y anotaciones.** Tabla con conteos: para cada genoma y transcriptoma, qué trae
   anotación de genes y cuál no, con accesión exacta y fecha de consulta. Es un inventario, no una
   búsqueda abierta.

2. **Fijar el criterio de gen blanco, antes de buscar.** Escribirlo por escrito en
   `research/ola3/C11_diseno_nuevo/criterio.md` y no cambiarlo después de ver resultados. Debe incluir:
   esencialidad o esterilidad con evidencia en un hemíptero; ortología por **secuencia y no por nombre**
   (D30: el caso `Rpn6` de *Scaphoideus titanus*, donde el nombre lleva a PSMD11 y la secuencia a PSMD6);
   y **exclusión explícita** de los contraejemplos ya catalogados (`uk1_LRR` aumentó la colonización del
   vector por el fitoplasma; `NcHig` aumentó la infección por un rabdovirus).

3. **Probar el mapeo por homología desde un genoma anotado.** Ortólogos por `blastx` contra proteínas
   revisadas de UniProt, con **ortología recíproca y no mejor hit**. Medir el paso que C5 mostró que
   falla: identidad por género, tramos perfectos de 21 nt, y cuántas ventanas del ortólogo existen
   idénticas en *D. maidis*. C5 midió que el umbral de 99 % no se alcanza entre géneros de cicadélidos
   (83,6 % de identidad de nucleótidos entre *S. titanus* y *M. quadrilineatus*) y que sólo 244 de 12.540
   loci superan 0,99.

4. **Medir cuántos candidatos sobreviven.** Contar cuántos genes con función conocida llegan a un
   ortólogo utilizable en *D. maidis* con secuencia suficiente para diseñar a nivel de nucleótido. Este
   número es el resultado principal.

5. **Evaluar si un enfoque agéntico aporta algo.** Contrastar con lo medido: los agentes sólo son
   confiables con verificador mecánico (tests, artefactos, resolución de DOI); los jueces LLM coinciden
   poco con expertos (r ≤ 0,35). Decidir si un agente curador de literatura con registro de fuentes
   agrega algo al catálogo, o sólo reproduce lo que una búsqueda sistemática ya da. **Regla de
   CLAUDE.md:** las secuencias de EPILAB no se suben a servicios de terceros; todo análisis de ellas corre
   en local.

6. **Escribir el veredicto con su alcance** en `research/ola3/C11_diseno_nuevo/REPORT.md`. Una de tres
   conclusiones, **declarada de antemano**: (a) viable, con qué número de genes; (b) viable sólo para N
   genes; (c) no viable con los datos actuales, y qué dato lo destraba. Con `sources.json`, scripts
   reproducibles y la declaración del motor y las fechas de consulta.
</metodo>

<que_no_hacer>
- **No diseñar secuencias orientadas a aumentar virulencia, transmisibilidad o rango de hospedadores** de
  un patógeno, ni dirigidas a organismos no objetivo. Es control fitosanitario con información pública.
- **No sobrescribir C11 existente.** Ya hay una carpeta `research/ola3/C11_conservacion_eth_bursa/`. La
  de esta fase es `research/ola3/C11_diseno_nuevo/`. Son distintas.
- **No tocar la fase de la plataforma.** La Fase 3 queda para otra sesión.
- **No subir a la web** ninguna secuencia de EPILAB: ni a BLAST web, ni a formularios, ni a APIs de LLM.
- **No editar `REPORT.md` a mano si tiene generador.** Se corrige la fuente (ver `research/ola3/C8_conservacion/scripts/generar_informes.py`), porque una edición manual se pierde en la siguiente regeneración. Esto pasó hoy.
- **No hacer rebase para integrar.** Usar `git fetch origin` y `git merge origin/main` con mensaje explícito. El rebase reescribe commits ajenos.
- **No afirmar lo que no se abrió.** Ni DOI ni número reconstruido de memoria. Las pistas no son fuentes.
- **Los ARNdc de Cedden (`cedden2025_28dsrna_con_secuencia.csv`) no se publican** sin autorización del equipo.
</que_no_hacer>

<reglas>
Rigen las de `CLAUDE.md`. Las que más se rompen:

- Toda afirmación técnica lleva fuente abierta y el marcador `[E]`, `[R]`, `[H]` o `[?]`.
- Los números van con su fuente, su contexto experimental y el comando que los produjo.
- Antes de subir cualquier archivo, correr el chequeo de rachas de 21 nt o más (`grep -Eoh '[ACGT]{21,}'`).
  Un TSV de salida de si-Fi21 contiene una columna `seq` que reconstruye el gen entero; ver
  `research/ola3/C9_sensibilidad_umbral/scripts/limpiar_ancla.py`.
- Un vacío documentado vale como resultado. Un vacío tapado con texto plausible no.
- Si algo contradice lo que dice el repo, es un hallazgo: reportarlo, no pisarlo.
</reglas>

<salida>
En `research/ola3/C11_diseno_nuevo/` (creala):

1. `criterio.md` — el criterio de gen blanco, fijado antes de buscar.
2. `REPORT.md` — el veredicto, en prosa, con la conclusión declarada arriba de todo.
3. `sources.json` — cada fuente leída, con su nivel de lectura y el motivo de cada descarte.
4. `scripts/` — reproducible, con el comando en el encabezado.
5. `NOTAS_PARA_META.md` — decisiones candidatas, caminos probados, preguntas nuevas.

Y actualizar `PLAN_DESARROLLO.md` (§8 y §3 ter) y `estado.html` a través de `tools/generar_estado.py`,
en los lugares donde declaran estado. Commits con autor `Joaquin <joaquin@Joaquins-MacBook-Air.local>`,
uno por paso del método.
</salida>

<verificacion>
- ¿El criterio de gen blanco se escribió **antes** de buscar, y está fechado?
- ¿La ortología se resolvió por secuencia y no por nombre?
- ¿El número de candidatos que sobreviven se reporta aunque sea cero?
- ¿Cada cifra declara genoma, accesión, fecha de consulta y motor?
- ¿Se corrió el chequeo de rachas de 21 nt sobre todo lo que se versiona?
- ¿Se regeneró cada HTML desde su fuente, y no se editó a mano?
</verificacion>

<terminacion>
Cuando el veredicto esté escrito y verificado, parar y reportar. No agregar investigación, herramientas
ni la Fase 3 que no estén pedidas acá. Si algo vale la pena y queda fuera de alcance, decirlo al final.
Dejar dicho qué no se pudo hacer y por qué.
</terminacion>

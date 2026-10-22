# C11 (diseño nuevo) — ¿cuántos genes blanco con función conocida llegan a un ortólogo utilizable en *Dalbulus maidis*?

**Veredicto: (b) viable sólo para N = 2 genes nominales, y ninguno sin salvedad.** De las 11 familias del catálogo de C5 que tienen ortólogo recíproco por secuencia en *Macrosteles quadrilineatus*, sólo dos alcanzan el criterio de nucleótido fijado antes de buscar (un tramo alineado de al menos 300 nt con al menos 90 % de identidad contra el transcriptoma TSA de *D. maidis*): ATP synthase beta (91,0 %) y actina muscular (92,5 %). La primera tiene evidencia de efecto mixta y la segunda es una familia multigénica donde el alineamiento puede ser un parálogo. `[R]` Fecha de consulta y de cálculo: 2026-10-22. Criterio: [`criterio.md`](criterio.md), commit `ac0bf6f`, escrito antes de cualquier búsqueda.

## Qué se midió y con qué

El motor es BLAST+ 2.17.0, local; ninguna secuencia de EPILAB salió de la máquina. La ortología se resolvió por secuencia: `blastp` en ambos sentidos entre las 14.079 proteínas revisadas de Swiss-Prot de Arthropoda (UniProt, consulta del 2026-10-22) y el proteoma de *M. quadrilineatus* (GCF_028750875.1, 34.269 proteínas), con par recíproco por mejor bitscore. Hubo 3.047 pares recíprocos y 2.297 cumplen el umbral estricto (e-valor ≤ 1e-20, cobertura ≥ 70 %). Las familias se buscaron por **nombre de proteína** y no por símbolo de gen. El caso lo justifica: en la base revisada, la entrada que *Drosophila* llama `Rpn6` es PSMD11 (78,2 % de identidad con la proteína de *M. quadrilineatus*) y PSMD6 aparece como `Rpn7` (43,7 %), y ambas son recíprocas de proteínas distintas. Eso reproduce la lección de D30 con una especie diferente a la de C5. `[R]`

Para el paso de nucleótido, cada proteína ortóloga se ubicó con `tblastn` en el ARNm de *M. quadrilineatus* (identidad 100 % en las 11) y ese ARNm se alineó con `blastn` contra los tres TSA de *D. maidis* (GCWP01, GHCC01, GITV01; 137.065 contigs en total). Se contaron los k-mers de 21 nt exactos presentes en los contigs con hit, en ambas cadenas.

## Resultado

| familia | ARNm de *M. quadrilineatus* | largo (nt) | identidad máxima (%) | HSP ≥ 300 nt y ≥ 90 % | tramo exacto máximo (nt) | ventanas de 21 nt idénticas |
|---|---|---|---|---|---|---|
| ATP synthase beta | XM_054410120.1 | 1855 | 91.0 | 1 | 74 | 250 (13.6 %) |
| BicC | XM_054413380.1 | 2777 | 84.2 | 0 | 39 | 106 (3.8 %) |
| PSMD6 | XM_054426831.1 | 2265 | 85.6 | 0 | 35 | 22 (1.1 %) |
| Rpn6 | XM_054432574.1 | 1432 | 88.4 | 0 | 56 | 116 (8.2 %) |
| Ruvbl1 | XM_054402769.1 | 1507 | 86.9 | 0 | 38 | 68 (4.6 %) |
| V-ATPase A | XM_054404756.1 | 2899 | 89.7 | 0 | 50 | 289 (10.0 %) |
| V-ATPase B | XM_054432770.1 | 2158 | 88.2 | 0 | 74 | 233 (10.9 %) |
| V-ATPase D | XM_054408552.1 | 1812 | 83.0 | 0 | 32 | 15 (0.8 %) |
| XPO1 | XM_054404977.1 | 4429 | 86.2 | 0 | 47 | 278 (6.3 %) |
| muscle actin | XM_054425756.1 | 1632 | 92.5 | 2 | 113 | 420 (26.1 %) |
| troponin C | XM_054409464.1 | 683 | 88.1 | 0 | 48 | 63 (9.5 %) |

Los 21-mers idénticos van del 0,8 % al 26,1 % del ARNm y el tramo exacto máximo es de 113 nt (actina) contra 32–74 nt en el resto. Esto confirma, con otras 11 familias, lo que C5 midió: entre géneros de cicadélidos no hay conservación suficiente para trasladar una ventana de 21 nt. Los valores de identidad máxima (83,0 a 92,5 %) son coherentes con el 83,6 % de C5 entre *S. titanus* y *M. quadrilineatus*.

## Cuántos sobreviven

De 14 familias del catálogo cotejadas contra Swiss-Prot, 11 tienen ortólogo recíproco estricto; Hig, transformer-2 y clatrina de cadena pesada no lo tienen (cobertura de 53 %, 40 % y sin par estricto; Hig además es un contraejemplo excluido por criterio). Seis grupos de nombres (lacasa, quitina sintasa, catepsina D y ABC B, E y F) no tienen ninguna entrada en Swiss-Prot de artrópodos y **no se pudieron evaluar con esta base**. De las 11, **2 superan el criterio de nucleótido**. Contra el catálogo: ATP synthase beta tiene un resultado de supervivencia que difiere entre estudios (sin efecto hasta 14 dpi en *S. titanus*, caída significativa en *E. variegatus* según resumen; filas CI-03 y CI-04 de C5), y la actina muscular es una de 11 actinas que cumplen el umbral estricto, de modo que el único modo de saber si el HSP es el gen buscado es resolver el parálogo.

## Límites, declarados

El criterio de nucleótido mide la conservación entre el ortólogo de *M. quadrilineatus* y *D. maidis*, no la calidad de un diseño hecho directamente sobre el contig de *D. maidis*. Un contig TSA de *D. maidis* que sea el ortólogo verdadero permitiría diseñar sobre su propia secuencia, y eso **no se evaluó**: haría falta confirmar la ortología desde el lado de *D. maidis* (`tblastn` inverso contra Swiss-Prot) y que el contig cubra la región. También quedan sin medir el genoma de *D. maidis* en este paso (sólo TSA), la identidad poblacional (C11 de conservación advirtió que GHCC01 es de una población) y los parálogos del TSA, porque se conservaron como máximo 5 subjects por consulta. Los blancos propios de *D. maidis* (`eth`, `burs-alpha`, BicC, V-ATPasa B y D) no necesitan mapeo por homología porque la secuencia es del propio vector; esa es la ruta más corta y no se usó aquí. Las cifras de eficacia salen de C5 con la apertura que ese catálogo declara (varias filas están a nivel de resumen).

## Enfoque agéntico (paso 5)

`[H]` Con lo medido, un agente curador de literatura con registro de fuentes agrega valor sólo donde hay verificador mecánico: abrir las 24 filas del catálogo que están a nivel de resumen (14) o sin abrir (10) y resolver el DOI. No agrega nada al cuello de botella medido aquí, que es la falta de anotación y de conservación, y los jueces LLM coinciden poco con expertos (r ≤ 0,35, valor del prompt, no verificado en esta sesión). Una búsqueda sistemática ya da el catálogo; el agente sólo lo haría más barato de mantener. Las secuencias de EPILAB seguirían corriendo en local.

## Reproducibilidad

Scripts en `scripts/`; tablas en `resultados/`; fuentes en [`sources.json`](sources.json). Chequeo de rachas de 21 nt sobre todo lo versionado: 0 coincidencias.

# Criterio de gen blanco — Fase 2 (diseño nuevo de ARNdc)

**Fijado el 2026-10-22, antes de buscar ortólogos, de consultar UniProt y de medir cualquier candidato.** No se modifica después de ver resultados. Si un criterio resulta inaplicable, la excepción se registra como enmienda fechada, no como edición silenciosa.

## 1. Qué cuenta como gen blanco

Un gen blanco es un gen de *Dalbulus maidis* cuya pérdida de función reduce la supervivencia, la fertilidad o la capacidad de transmisión del vector. Para entrar al catálogo debe cumplir las tres condiciones de la sección 2 y no caer en las exclusiones de la sección 4.

## 2. Condiciones de entrada

**2.1 Esencialidad o esterilidad con evidencia en un hemíptero.** La evidencia debe venir de un experimento de silenciamiento por ARN de doble cadena (dsRNA o siRNA) o de knockout, medido en un hemíptero (cicadélido, áfido, psílido o pentatómido). La evidencia de otro orden de insectos sirve sólo como antecedente y se marca como `[R]`, no como `[E]`. Se registra la especie, el tipo de experimento, la vía de entrega, el desenlace medido y la fuente abierta.

**2.2 Ortología por secuencia, no por nombre.** El nombre de un gen en una anotación automática no define su familia. Se aplica la regla de D30. El ortólogo se establece por:

- traducción del transcripto o del locus de la especie anotada (*Macrosteles quadrilineatus*, proteoma RefSeq de 34.269 proteínas, accesión GCF_028750875.1);
- `blastx` contra proteínas revisadas de UniProt/Swiss-Prot;
- **ortología recíproca**: el mejor hit de UniProt, al volver a buscar contra el proteoma de la especie anotada, debe devolver el gen de origen. No se usa el mejor hit a secas.

Umbral propuesto `[H]`: e-valor menor o igual a 1e-20 y cobertura de la consulta mayor o igual al 70 %. Un gen cuyo nombre y cuya secuencia no coinciden se registra con la familia que dice la secuencia.

**2.3 Secuencia suficiente para diseñar a nivel de nucleótido.** Hace falta un tramo de *D. maidis* que corresponda al ortólogo y que sea alineable a nivel de nucleótido. Se mide sobre el ensamblado de nivel cromosoma (GCA_975739785.1), o sobre el transcriptoma TSA correspondiente cuando el locus no se resuelve en el genoma. Umbral propuesto `[H]`: al menos 300 nt contiguos del ortólogo alineados con identidad de nucleótidos mayor o igual al 90 % contra el vector.

> Nota de método: el umbral de 99 % del que partió C5 no se alcanza entre géneros de cicadélidos (83,6 % entre *S. titanus* y *M. quadrilineatus*, medido en C5). Por eso el umbral de identidad se separa del de ortología. Este criterio se fija como `[H]` y se reporta la sensibilidad del resultado al umbral.

## 3. Lo que no es un candidato

- Los genes ya catalogados como contraejemplos, que se excluyen de forma explícita:
  - `uk1_LRR`: su silenciamiento aumentó la colonización del vector por el fitoplasma;
  - `NcHig`: su silenciamiento aumentó la infección por un rabdovirus.
- Genes de los que sólo se conoce la secuencia, sin función medida en un hemíptero.
- Genes del patógeno (MRFV, fitoplasma, *Spiroplasma*): fuera de alcance, ver D33 y D34.

## 4. Exclusiones de seguridad

No entra ningún blanco cuyo silenciamiento pueda aumentar la virulencia, la transmisibilidad o el rango de hospedadores de un patógeno. Tampoco los blancos con riesgo sobre organismos no objetivo sin medir: polinizadores, enemigos naturales y fauna del suelo. Cada candidato que pase el criterio lleva su contracara de riesgo declarada.

## 5. Qué se reporta aunque sea cero

El número de candidatos que cumplen las tres condiciones de la sección 2 se reporta aunque sea cero. Un cero con su causa documentada es un resultado válido.

## 6. Referencias de partida

- Catálogo de genes blanco de C5 (36 filas, 20 nuevas): `research/ola3/C5_estructura_genes_ingenieria_inversa/catalogo_genes_blanco.md`. Se usa como punto de partida, no se rehace.
- Decisiones D30, D33, D34, D35 y D36 en `00_meta/DECISIONS.md`.

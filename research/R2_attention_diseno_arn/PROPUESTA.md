# PROPUESTA — Priorizador auditable de candidatos de ARNdc

**Veredicto del que depende este documento:** la idea original —tokens de ARN, attention,
termodinámica de BLAST como loss— se descarta por error factual y por reinvención de cuatro
métodos publicados. La reformulación que sigue **sí es viable**. El argumento completo del
descarte está en `REPORT.md`; acá va la especificación de lo que se rescata y se construye.

**Nombre de trabajo:** PRIOR-dsRNA.
**Qué es en una oración:** una función de puntuación multiobjetivo sobre candidatos de ARNdc
*dados*, que devuelve un ordenamiento con la incertidumbre propagada y cada término trazable
a una fuente citada, para responder la pregunta que el organizador declara abierta: cuáles
de los candidatos preliminares del EPILAB merecen validación y por qué.
**Qué NO es:** un generador de secuencias nuevas, un modelo entrenado de novo, ni un
reemplazo de dsRIP. Es una capa de decisión auditable construida **sobre** dsRIP como
baseline, instanciada en Hemiptera y en el agroecosistema del maíz argentino.

---

## 1. Posicionamiento: qué agrega sobre lo que ya existe

Hay que ser explícitos porque el riesgo reputacional de no serlo es alto. **dsRIP (Cedden et
al. 2025) ya hace la mayor parte de esto** `[E]`: calcula un score de eficacia de siRNA con
coeficientes calibrados en insecto, un score de seguridad por off-target con Bowtie1 contra
83 transcriptomas, los combina con un deslizador de prioridad y corre una ventana
deslizante. Está publicado, validado prospectivamente y en línea.

Lo que PRIOR-dsRNA agrega, y es todo lo que agrega:

| Aporte | Por qué es un hueco real |
| --- | --- |
| **Incertidumbre propagada hasta el ordenamiento** | La revisión del campo dice que "no se han aplicado métodos formales de cuantificación de incertidumbre a la predicción de eficacia de siRNA" y la llama "the most critical gap" `[E]`. dsRIP devuelve un score puntual sin intervalo |
| **Ordenamiento declarado como robusto o como empate** | Es la forma que toma la pregunta del organizador. Un score puntual no distingue "mejor" de "indistinguible" |
| **Frente de Pareto además del escalar** | dsRIP colapsa en un escalar vía el deslizador; eso oculta qué parte del orden depende de nuestras preferencias y qué parte no |
| **Instanciación en Hemiptera y en el agroecosistema local** | dsRIP no lista especies soportadas en su portada y no pudimos confirmar que incluya cicadélidos `[R]`; el panel de no objetivo del maíz argentino no existe curado en ninguna parte |
| **Exclusión fundamentada del término de accesibilidad** | si-Fi21 lo usa con peso `[E]`; la evidencia en insectos no lo sostiene `[E]`. Convertir eso en una ablación medida es un resultado reportable |
| **Anotación explícita de la barrera de entrega** | Ninguna herramienta existente registra si el candidato contempla co-entrega contra dsRNasas, que es la barrera que el organizador declara `[R]` |

Si al final del Investigathón el método no le gana a dsRIP en V1, el entregable sigue siendo
válido: la contribución es la decisión auditada, no la correlación. Esto hay que decirlo
desde el principio, no como excusa posterior.

---

## 2. Datos

El detalle está en `datos_disponibles.md`. Lo mínimo imprescindible:

| Insumo | Fuente | Estado |
| --- | --- | --- |
| Conjunto de candidatos | EPILAB | **Dependencia externa.** Hay que pedirlo ya, con secuencia, transcripto blanco, organismo y vía de entrega prevista |
| Transcriptoma de referencia de *D. maidis* | A ensamblar desde 20 corridas de RNA-seq (PRJNA631706 y otros) | **No existe.** Camino crítico |
| Genoma de *D. maidis* | `GCA_975739785.1` (Sanger, cromosoma, 972 Mb) | Existe, sin anotación |
| Anotación para transferir por ortología | `GCF_021130785.1` (*H. vitripennis*), `GCF_028750875.1` (*M. quadrilineatus*) | Existen, con anotación RefSeq |
| Transcriptos de maíz | `GCF_902167145.1` B73 + anotación RefSeq | Existe |
| No objetivo de referencia | `GCF_003254395.2` (*A. mellifera*) + panel a curar | Parcial |
| Patógenos | `GCF_001274875.1` (*S. kunkelii*), `GCF_000862485.2` (MRFV), fitoplasma a confirmar, MSMV sin identificar | Parcial |
| Datos de calibración y validación | Cedden et al., Additional files 2 y 3, **CC BY 4.0** | Existe. Es el activo más valioso del proyecto |
| Evidencia en la especie blanco | 6 construcciones de ARNdc en 3 papers | Existe, n=6 |

---

## 3. Modelo y objetivo

**No hay entrenamiento de un modelo nuevo.** Esto es una decisión, no una limitación
disimulada: no existen datos de fenotipo en Hemiptera para entrenar, y entrenar sobre n=29
de Coleoptera con features de alta dimensión produce memorización. El "modelo" es una función
de puntuación explícita con coeficientes tomados de un modelo de Cox publicado.

Para cada ventana *w* de 21 nt de un candidato *c*:

```
E(w)     = beta_1 * asimetria_termodinamica(w)
         + beta_2 * energia_autoplegamiento_antisentido(w)
         + beta_3 * GC_9_14(w)
         + beta_4 * [A en posicion 10](w)
```

con `beta_1..4` los coeficientes [Z] del modelo de Cox de Cedden et al. `[E]`. Asimetría
desde tablas de estabilidad de dúplex de ARN; autoplegamiento con **RNAfold**.

```
A(w)     = accesibilidad local con RNAplfold          -> peso 0 por defecto, se reporta
O_maiz(w)  = aciertos Bowtie en transcriptos de B73, por nivel de desapareamiento 0/1/2
             + aciertos de semilla (posiciones 2-8)
O_nt(w)    = idem contra el panel no objetivo, ponderando ortologos de genes esenciales
O_self(w)  = idem contra el transcriptoma de D. maidis
```

Agregación a nivel candidato: media de E sobre las ventanas (es la forma que Cedden et al.
validaron `[E]`), y conteos acumulados para los términos de off-target. Más, a nivel de
candidato: `K(c)` calidad del gen blanco, `R(c)` ORF frente a UTR, `C(c)` conservación entre
los individuos disponibles, y `D(c)` anotación categórica de la vía de entrega y de si hay
co-entrega contra *Dmai-dsRNase-2*.

**La salida no es un número.** Son tres objetos:

1. el vector de términos por candidato, sin colapsar;
2. el frente de Pareto, independiente de los pesos;
3. la matriz de estabilidad de pares: para cada (a, b), la fracción de 10.000 muestras
   conjuntas de (vector de pesos del simplex, remuestreo bootstrap de los coeficientes de
   Cox) en las que a precede a b. Umbral declarado de antemano: **estabilidad por encima de
   0,90 se llama orden robusto; por debajo se llama empate.**

El objetivo de entrenamiento, para que no quede ambiguo: **no hay loss.** La única
supervisión disponible es el fenotipo medido en los 29 ARNdc de Cedden et al., y se usa para
*validar*, no para ajustar. Si se usara para ajustar, se perdería el único conjunto de
validación que existe.

---

## 4. Baselines

Sin baseline no hay entregable. Tres, en orden de dureza:

1. **dsRIP, score de siRNA solo.** El baseline duro. Publicado, con validación prospectiva.
2. **si-Fi21 en modo HE.** El baseline de la práctica establecida, que sí usa accesibilidad.
   Fricción conocida: escritorio, sólo Windows, Python 2.7 `[E]`. Presupuestar esa fricción.
3. **Azar y secuencia barajada.** El piso.

---

## 5. Métricas

Definidas antes de construir nada.

| Métrica | Cómo se mide | Criterio de éxito |
| --- | --- | --- |
| **Primaria** | Spearman entre score y hazard ratio observado en los ~29 ARNdc de *T. castaneum*, con validación cruzada dejando un gen afuera | Igualar o superar a dsRIP solo. Si no se logra, se reporta |
| **Secundaria, la del desafío** | Fracción de pares del conjunto EPILAB clasificables como orden robusto | Que cada par quede clasificado, y que cada término sea trazable a una fuente abierta citada |
| **Prueba de rango en la especie blanco** | Percentil de las 6 regiones publicadas de *D. maidis* entre todas las ventanas de 300 pb de su propio transcripto | Por encima de la mediana. **Es una señal con n=6, no un benchmark** |
| **Cobertura de auditoría** | Proporción de términos con fuente abierta citada y verificada | 100%. Es condición, no objetivo |

---

## 6. Plan de validación

Detallado en la sección 5 de `REPORT.md`. Resumen: V1 retrospectiva sobre ARNdc largo en
*Tribolium*; V2 sobre los 29 siRNA individuales, que es el caso limpio porque aísla
secuencia de gen blanco; V3 prueba de rango sobre las 6 construcciones de *D. maidis*; V4
comparación contra dsRIP y si-Fi21; V5 cinco ablaciones, de las que la más valiosa es con y
sin accesibilidad; V6 controles negativos y particiones conscientes de la fuga de datos
(leave-one-gene-out, no partición aleatoria `[E]`).

**Lo que no se puede validar y hay que escribir en la portada:** la transferencia de
Coleoptera a Hemiptera, el término de conservación poblacional, la relevancia funcional de
los off-targets predichos, y cualquier cosa sobre la eficacia real de la entrega oral.

---

## 7. Esfuerzo en días-persona

Cuatro personas. Presupuesto realista de ~20 días-persona útiles.

| Tarea | Días-persona | Notas |
| --- | --- | --- |
| **T1. Transcriptoma de referencia de *D. maidis*** | **4** | Camino crítico. Descarga de SRA, ensamblado, ORF con TransDecoder, anotación por ortología desde los dos cicadélidos con RefSeq. **Empieza el día uno, en paralelo con todo** |
| T2. Pipeline de scoring: ViennaRNA, tablas de dúplex, las cuatro features, ventana deslizante | 3 | Reimplementar los coeficientes de Cedden et al. desde el paper y sus suplementos |
| T3. Índices y conteos de off-target: maíz, *Apis*, panel no objetivo, intraespecífico | 2,5 | Bowtie. Depende de T1 para el término intraespecífico |
| T4. Incertidumbre, Pareto y matriz de estabilidad de pares | 3 | El aporte metodológico. Bootstrap sobre coeficientes y muestreo del simplex |
| T5. Validación V1 a V6 y baselines | 4 | Incluye pelear con si-Fi21 en Windows |
| T6. Entregable auditable: tabla de decisión, perfil posicional por candidato, trazas de fuente | 2,5 | El artefacto vale por la decisión, no por la pantalla `[R]` |
| T7. Curaduría del panel de no objetivo del maíz argentino | 1 | Trabajo bibliográfico, no de método |
| **Total** | **20** | |

**Lo que se recorta explícitamente por ser plan de tesis disfrazado:** fine-tuning de
cualquier modelo de lenguaje; preentrenamiento de cualquier cosa; generación o búsqueda
sobre el espacio de secuencias; construcción de un dataset propio de eficacia en Hemiptera;
cualquier plataforma más allá del segundo escalón de la escalera del organizador (nada de
miARN artificial, syn-tasiRNA, dúplex listo para AGO ni siRNA de 24 nt con RdDM). El brazo
de embeddings congelados de RNA-FM queda como opcional y sólo si T1 a T6 están cerrados.

---

## 8. Riesgos, ordenados por probabilidad de hundir el proyecto

**1. El conjunto de candidatos del EPILAB no llega, o llega sin blanco ni vía de entrega.**
*Probabilidad alta. Impacto total: sin candidatos no hay nada que priorizar.*
Mitigación: pedirlo el día uno con la especificación exacta de campos; y construir el método
para que corra sobre *cualquier* conjunto, demostrándolo sobre un conjunto propio generado
por ventana deslizante contra los transcriptos con RNAi publicado. Así el entregable existe
aunque el insumo externo no llegue.

**2. T1 se desborda y bloquea T3 y todo lo que dependa del transcriptoma.**
*Probabilidad alta. Impacto alto.*
Mitigación: tres niveles de repliegue declarados de antemano. Nivel A, ensamblado propio
anotado por ortología. Nivel B, sólo ORF predichos sobre el genoma de Sanger sin ortología.
Nivel C, usar únicamente los transcriptos de los genes con RNAi publicado, extraídos de los
papers. El nivel C alcanza para V3 y para demostrar el método, y se puede tener en un día.

**3. La transferencia Coleoptera a Hemiptera no es válida y el score no predice nada en *D.
maidis*.** *Probabilidad media-alta. Impacto alto sobre la utilidad; nulo sobre la
honestidad del entregable si se declara.*
Mitigación: no hay mitigación técnica. Es la incertidumbre dominante y la única respuesta
correcta es reportarla en la portada y propagarla al ancho de los intervalos. Los propios
autores de dsRIP la dejan como pendiente para otros órdenes `[E]`.

**4. El método no le gana a dsRIP en V1.**
*Probabilidad media. Impacto medio.*
Mitigación: el encuadre del entregable no es "mejor score" sino "decisión auditable con
incertidumbre". Declararlo antes de medir, no después.

**5. La contribución se lee como delgada porque dsRIP ya hacía casi todo.**
*Probabilidad media. Impacto medio, sobre todo reputacional.*
Mitigación: la sección 1 de este documento, dicha en voz alta en la presentación. Reconocer
el baseline es más fuerte que ocultarlo, y el criterio de evaluación declarado premia la
decisión científica, no la novedad aparente `[R]`.

**6. Alguien del equipo presenta el perfil posicional o un mapa de atención como evidencia
causal.** *Probabilidad media si no se acuerda antes. Impacto alto y específicamente
reputacional ante un jurado académico.*
Mitigación: la sección 3.5 de `REPORT.md` como lectura obligatoria del equipo. El enunciado
acordado: el perfil posicional es fiel por construcción porque *es* el cálculo; un mapa de
atención no sostiene una lectura causal `[R]`.

**7. Licencias.** *Probabilidad baja-media. Impacto bajo si se chequea temprano.*
Nucleotide Transformer es CC-BY-NC-SA-4.0, no comercial `[R]`; iBeetle-Base no tiene licencia
confirmada `[?]`; los depósitos de figshare de dsRIP tampoco `[?]`; dsRIP dice "All rights
reserved" en el pie de su web `[R]`. Verificar antes de reusar, y no reusar lo que no se
pueda verificar.

**8. Cómputo para el ensamblado del transcriptoma.** *Probabilidad baja. Impacto medio.*
Mitigación: submuestrear corridas; el repliegue de nivel C no requiere ensamblado.

---

## 9. Lo que se rescata de la idea original, en concreto

- **La forma del problema** —señal posicional a lo largo del transcripto— es correcta y es el
  estado del arte. Sobrevive como la ventana deslizante sobre el score por ventana.
- **La termodinámica como parte de la señal** sobrevive, pero como *feature de entrada* y
  calculada con ViennaRNA, no con BLAST, y restringida a asimetría de extremos y
  autoplegamiento, que son las que la evidencia en insectos sostiene.
- **BLAST** sobrevive conceptualmente en el eje de especificidad, reemplazado por Bowtie por
  razones de herramienta adecuada al problema.
- **"Ver la relación entre las distintas secuencias"** sobrevive como el perfil posicional
  explícito del score, que cumple la misma función comunicativa que un mapa de atención y es
  fiel por construcción.
- **Los embeddings preentrenados** sobreviven como brazo de ablación opcional, con la
  advertencia de que la propia literatura los califica de "sufficient but not necessary"
  `[E]`.

Lo que no sobrevive: la termodinámica como loss, BLAST como calculador de termodinámica, el
fine-tuning sobre datos inexistentes, y la generación de secuencias nuevas.

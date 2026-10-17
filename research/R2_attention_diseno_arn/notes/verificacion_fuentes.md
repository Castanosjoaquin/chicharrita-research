# Notas de verificación — R2

Registro de qué se abrió realmente, con qué herramienta, y qué quedó sin abrir.
Regla del proyecto: prohibido citar algo que no se abrió.

## Abierto y verificado

| Fuente | Vía | Qué se extrajo |
| --- | --- | --- |
| NCBI Datasets API v2alpha, `genome/taxon/74065` | `curl` a `api.ncbi.nlm.nih.gov` | Los tres ensamblados de *Dalbulus maidis*, con nivel, tamaño, N50, fecha y estado de anotación |
| NCBI Datasets API, taxones 4577 (maíz), 7460 (*Apis mellifera*), Cicadellidae, *Nilaparvata lugens*, *Ca.* Phytoplasma asteris, MRFV, *Spiroplasma kunkelii* | `curl` | Accesiones de referencia y estado de anotación |
| NCBI E-utilities `esearch`/`esummary`/`efetch` (SRA, PubMed, BioProject) | `curl` | 37 experimentos SRA de *D. maidis* con su estrategia de librería; abstracts completos de los tres trabajos de RNAi en *D. maidis* |
| Cedden et al. 2025, *BMC Biology*, dsRIP | Europe PMC `fullTextXML` (PMC12039203) | Texto completo: resultados, métodos, plataforma, disponibilidad de datos. Licencia CC BY |
| Lück et al. 2019, *Front. Plant Sci.*, si-Fi21 | WebFetch | Algoritmo, reglas implementadas, Bowtie + RNAplfold, licencia CC BY-SA, repositorio |
| Bai et al. 2024, *Bioinformatics*, OligoFormer | WebFetch (PMC11494384) | Datasets, features, uso de RNA-FM, arquitectura, métricas, módulo off-target, limitaciones declaradas |
| Liu et al. 2023, bioRxiv, AttSiOff | WebFetch del PDF + extracción local de texto | Abstract y aportes declarados textuales |
| "From rules to foundation models", *NAR Genomics and Bioinformatics* lqag099 | WebFetch en dos offsets (0 y 100000) | Cronología de métodos, datasets, uso de modelos de lenguaje, fugas de datos, protocolos de partición, off-target, direcciones futuras |
| Cheng et al. 2024, *Brief. Funct. Genomics*, dsRNAPredictor | WebFetch | Arquitectura, iBeetle-Base como fuente, definición de positivos/negativos, métricas |
| Lorenz et al. 2011, *Algorithms Mol. Biol.*, ViennaRNA 2.0 | Europe PMC `fullTextXML` (PMC3319429) | Qué calcula cada programa (RNAfold, RNAplfold, RNAup, RNAduplex, RNAcofold), licencia CC BY del artículo |
| Manpage de RNAup, tbi.univie.ac.at | WebFetch | Descomposición `dG = dGint + dGu_l`, entradas, salidas, opciones |
| NCBI, "The Statistics of Sequence Similarity Scores" (tutorial de BLAST, Altschul) | WebFetch | Modelo de puntaje log-odds, Karlin-Altschul, bit score, P-value. Confirma ausencia de termodinámica |
| NCBI BLAST FAQ | WebFetch | Definición textual de E-value |
| Altschul et al. 1990 (PMID 2231712) y 1997 (PMID 9254694) | `efetch` abstract | "maximal segment pair (MSP) score"; "criterion for triggering the extension of word hits" |
| Penić et al. 2024, arXiv:2403.00043, RiNALMo | WebFetch de la página abs | 650M parámetros, ~36M secuencias de ncRNA, claim de generalización |
| ml4bio/RNA-FM en GitHub | WebFetch | ~99M parámetros, 23.7M ncRNA de RNAcentral, embeddings de 640 dimensiones, licencia MIT, pesos en HuggingFace |
| Model card de `InstaDeepAI/nucleotide-transformer-v2-500m-multi-species` en HuggingFace | WebFetch | 500M parámetros, 850 genomas, 174 Gnt, tokenización en 6-meros, MLM al 15%, licencia CC-BY-NC-SA-4.0 |
| `https://dsrip.uni-goettingen.de/` | WebFetch | Herramientas ofrecidas, versión v1.2, aviso "All rights reserved" en el pie |

## Buscado pero NO abierto — no se cita como verificado

- **Jain & Wallace 2019, Wiegreffe & Pinter 2019, Serrano & Smith 2019, Bibal et al. 2022.** Delegados a una búsqueda acotada; lo que entre al reporte lleva la URL que la búsqueda abrió. Lo que no se pudo abrir queda marcado.
- **Tafer et al. 2008, *Nature Biotechnology* 26:578–583** (accesibilidad del sitio blanco, RNAxs). Sólo se abrió el registro bibliográfico y la página de resumen; el texto completo está detrás de muro de pago. Se cita como `[R]` por su registro y por la descripción que de él hace si-Fi21, que sí se abrió.
- **Hüsken et al. 2005 (BIOPREDsi).** No se abrió el original. El tamaño del dataset (2431 siRNA, 34 mRNA) y el PCC de 0.66 se citan a través de OligoFormer y de AttSiOff, que sí se abrieron, y se marcan como cita de segunda mano.
- **Evo 2.** Sólo fuentes secundarias (notas de prensa). Las cifras de 9.3 billones de nucleótidos y 128.000 genomas quedan `[R]` no verificadas contra el paper. No se usa en la propuesta.
- **Buer et al. 2024** (cribado genómico de *T. castaneum*). Se conoce por la referencia [25] de Cedden et al., que sí se abrió. No se abrió el original.
- **iBeetle-Base.** No se pudo confirmar licencia ni formato de descarga masiva. Marcado como no verificado en `datos_disponibles.md`.
- **Xu et al. 2021**, transcriptoma de *D. maidis* con 56.116 transcriptos: el abstract se abrió vía `efetch`, pero **no se encontró el ensamblado depositado**: la búsqueda `Dalbulus maidis[Organism] AND TSA[Division]` en `nucleotide` devuelve 0 registros. El ensamblado puede estar sólo como material suplementario. Pendiente.

## Rechazo de herramienta registrado

Una búsqueda web con el texto `RNAi Dalbulus maidis leafhopper dsRNA knockdown Hemiptera efficacy`
fue rechazada por la herramienta con el detalle `[bio]`. Según la regla del proyecto no se
reformuló para esquivar el rechazo. La misma pregunta se respondió por otra línea
legítima y distinta: búsqueda bibliográfica en PubMed vía E-utilities, que devolvió los
cuatro registros de RNAi en *Dalbulus* y permitió traer los abstracts completos. Queda
anotado en `00_meta/PREGUNTAS_ABIERTAS.md`.

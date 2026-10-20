# Búsquedas de M3 (plantas, insectos y patógenos en vuelo y microgravedad simulada)

Fecha de todas las consultas: 2026-10-19. Cada bloque da la base, la cadena exacta enviada, el número de resultados que la base declaró y los primeros títulos devueltos (hasta cinco). Los números B01 a B89 son los que usan `REPORT.md` y `catalogo_estudios.json`. Las consultas de la tabla fueron ejecutadas por código (Europe PMC REST, NCBI E-utilities, API pública de Crossref, API pública de NASA NTRS y API de búsqueda de NASA OSDR) y registradas automáticamente; las cuatro consultas de buscador web (W1 a W4) se anotaron a mano.

**Límites que conviene saber antes de leer una ausencia.** Europe PMC indexa resúmenes, no siempre texto completo; las consultas de título y resumen (`TITLE_ABS`) son más estrechas que las de texto libre, y por eso se corrieron las dos. Los resultados de Crossref son difusos y su recuento total no significa nada. La API de búsqueda de OSDR hace búsqueda de texto libre sobre metadatos de GeneLab, GEO, PRIDE y MG-RAST juntos; para contar estudios de vuelo se filtró por tipo de fuente `cgene` (GeneLab). B14 se corrió primero con un filtro defectuoso y se repitió como B89. Las consultas sin título en la lista de 'primeros resultados' devolvieron 0.

**Ausencias que estas búsquedas respaldan:** RNAi/SIGS/HIGS con microgravedad en fitosanidad (B03, B48 a B50, B57, B59 a B62, B81, B83, B84, W1, W2); mollicutes en vuelo o clinostato (B20, B33 a B35, B51 a B55, B73 a B77, B82, B86, W3); hemípteros en vuelo (B18, B19, B36, B37, B42, B63, W4); RNAi en insectos en vuelo (B43, B47, B48); maíz con defensa o silenciamiento en vuelo (B06, B10, B11, B17, B23, B58); DCL/AGO/RDR medidos en plantas en vuelo (B04, B05, B80).


## Punto 4 (RNAi/SIGS/HIGS con microgravedad)

### B01 — Europe PMC — 2026-10-19

- **Cadena:** `(microgravity OR spaceflight OR "space flight") AND (RNAi OR dsRNA OR siRNA OR "RNA interference") AND (plant OR crop OR pathogen OR pest)`
- **Resultados declarados por la base:** 208
- **Primeros títulos:**
  - 2026 PMC13350859: MAPK/PMK-1 innate immune signaling protects the nematode Caenorhabditis elegans from increased intestinal colo
  - 2026 PMC13566835: Beyond Earth: Recent Advancements in Microgravity Biomedical and Genetic Research in Saudi Arabia.
  - 2025 PMC12829014: SLC25A mitochondrial carriers as biomarkers and therapeutic targets of spaceflight-induced dysfunction: the AD
  - 2026 PMC13141948: Reduced gravity and muon flux absence affect Caenorhabditis elegans life history traits and viral infection.
  - 2026 PMC13468469: An Inulin-Type Atractylodes Macrocephala Polysaccharide Alleviates Weightlessness-Induced Bone Loss in Associa
- **Útiles / comentario:** Consulta ancha. Los 20 primeros son nematodo, hueso, cultivos celulares; ninguno une RNAi con fitosanidad. Útil de contexto: M3-04.

### B02 — Europe PMC — 2026-10-19

- **Cadena:** `(microgravity OR spaceflight) AND (dsRNA OR "double-stranded RNA" OR siRNA)`
- **Resultados declarados por la base:** 541
- **Primeros títulos:**
  - 2026 42601142: Double-stranded RNA and reverse transcriptase signatures of endogenous retroviruses after exposure to spacefli
  - 2026 PMC13565916: Impact of Microgravity on Cytoskeletal Dynamics, Protein Transport, and Signaling Networks: Potential Therapeu
  - 2026 PMC13348333: Kaempferol Attenuates Spaceflight-Associated Knee Cartilage Degradation by Targeting NOX4-Mediated Mitochondri
  - 2026 PMC13350859: MAPK/PMK-1 innate immune signaling protects the nematode Caenorhabditis elegans from increased intestinal colo
  - 2026 PMC13320170: Gravitational and mechanical forces shape mitochondrial translation.
- **Útiles / comentario:** 541 resultados; los 20 primeros son de biomedicina y células de mamífero. Ninguno útil.

### B03 — Europe PMC — 2026-10-19

- **Cadena:** `(microgravity OR clinostat OR "random positioning machine") AND (SIGS OR HIGS OR "spray-induced gene silencing" OR "host-induced gene silencing")`
- **Resultados declarados por la base:** 3
- **Primeros títulos:**
  - 2026 PMC13320170: Gravitational and mechanical forces shape mitochondrial translation.
  - 2021 PMC8251645: Posters
  - 2019 PMC6933297: "Abstracts of the 78th Annual Meeting of the Japanese Cancer Association; 2019 Sept 26-28; Kyoto, Japan" as Ca
- **Útiles / comentario:** AUSENCIA CENTRAL. Tres resultados, todos espurios (traducción mitocondrial, pósters de congreso, resúmenes de un congreso oncológico). Ninguno une SIGS o HIGS con microgravedad.

### B59 — Crossref — 2026-10-19

- **Cadena:** `dsRNA RNA interference plant pathogen simulated microgravity clinostat`
- **Resultados declarados por la base:** 1760265
- **Primeros títulos:**
  - Comparison of clinostat control strategies to achieve simulated microgravity with uniform gravity vector distribution npj Microgravity (10.1038/s41526-026-00570-8)
  - Coupled System of Dual-Axis Clinostat and Helmholtz Cage for Simulated Microgravity Experiments  (10.20944/preprints202409.1491.v1)
  - Influence of selected plant growth stimulators in enhancing germinability and germination parameters of
                  (10.1101/2021.11.23.469749)
  - Automorphosis of maize shoots under simulated microgravity on a three-dimensional clinostat Physiologia Plantarum (10.1034/j.1399-3054.1995.930220.x)
  - Arabidopsis flowering induced by photoperiod under 3-D clinostat rotational simulated microgravity Acta Astronautica (10.1016/j.actaastro.2018.11.014)
- **Útiles / comentario:** Crossref es difuso (millones de resultados). Los primeros ocho son trabajos de clinostato y de plantas; el SIGS y la microgravedad no se juntan.

### B60 — Crossref — 2026-10-19

- **Cadena:** `spray-induced gene silencing microgravity spaceflight`
- **Resultados declarados por la base:** 2664372
- **Primeros títulos:**
  - Spray-Induced Gene Silencing for Postharvest Protection: dsRNA Stability and Insecticidal Efficacy  (10.1021/acs.jafc.4c13212.s001)
  - Control of Fusarium graminearum Infection in Wheat by dsRNA-Based Spray-Induced Gene Silencing  (10.1021/acs.jafc.4c12665.s001)
  - Enhancing plant defense: carbon dots for efficient spray-induced gene silencing  Open GPB 2024 (10.58233/meanowhz)
  - The Bacteria-Derived dsRNA Was Used for Spray-Induced Gene Silencing for Rice False Smut Control  (10.1021/acs.jafc.4c05605.s001)
  - Spaceflight and Differential Gene Expression Analysis of Mice Quadriceps Exposed to Microgravity  (10.31979/etd.4tt8-8a9h)
- **Útiles / comentario:** Los resultados son trabajos de SIGS sin microgravedad y trabajos de microgravedad sin SIGS; ninguno combinado.

### B61 — Crossref — 2026-10-19

- **Cadena:** `RNAi insect pest random positioning machine microgravity`
- **Resultados declarados por la base:** 1429218
- **Primeros títulos:**
  - Simulated Microgravity Using a Random Positioning Machine for In-Space Additive Manufacturing ASCEND 2026 (10.2514/6.2026-3082)
  - Brief Communication: Confocal microscopy of oral streptococcal biofilms grown in simulated microgravity using a random p npj Microgravity (10.1038/s41526-024-00427-y)
  - Impairment of 7F2 osteoblast function by simulated partial gravity in a Random Positioning Machine npj Microgravity (10.1038/s41526-022-00202-x)
  - Pyrocystis noctiluca represents an excellent bioassay for shear forces induced in ground-based microgravity simulators ( npj Microgravity (10.1038/s41526-017-0016-x)
  - Light is sufficient to compensate for random positioning machine-simulated microgravity in plant roots npj Microgravity (10.1038/s41526-025-00493-w)
- **Útiles / comentario:** Resultados sobre RPM (M3-22 entre ellos); ninguno con RNAi de plagas.

### B62 — Crossref — 2026-10-19

- **Cadena:** `RNA interference crop protection spaceflight International Space Station`
- **Resultados declarados por la base:** 15911250
- **Primeros títulos:**
  - Research on Thermal Protection Technologies for Manned Space Vehicles Space Studies (10.1007/978-94-015-9880-4_60)
  - Is RNA interference the next big thing in crop protection? Proceedings of the Integrated  (10.31274/icm-180809-202)
  - Preparing for Passenger Space Travel, the Future of Human Spaceflight Space Studies (10.1007/978-94-015-9880-4_21)
  - The Future of Human Spaceflight in Japan Space Studies (10.1007/978-94-015-9880-4_7)
  - Economic and Technical Evaluation of Suborbital Spaceflight for Space Tourism1 Space Studies (10.1007/978-94-015-9880-4_30)
- **Útiles / comentario:** Ruido de ingeniería aeroespacial; ningún cruce.

### B81 — Europe PMC — 2026-10-19

- **Cadena:** `SRC:PPR AND (RNAi OR dsRNA OR siRNA OR "RNA interference" OR "gene silencing") AND (microgravity OR spaceflight OR clinostat OR "random positioning machine") AND (plant OR insect OR pest OR pathogen OR fungal)`
- **Resultados declarados por la base:** 0
- **Primeros títulos:** ninguno
- **Útiles / comentario:** AUSENCIA. 0 preprints que combinen RNAi o dsRNA con microgravedad y plantas, insectos o patógenos.

### B82 — Europe PMC — 2026-10-19

- **Cadena:** `SRC:PPR AND (microgravity OR spaceflight OR clinostat) AND (phytoplasma OR Spiroplasma OR Mycoplasma OR mollicute OR Mollicutes)`
- **Resultados declarados por la base:** 1
- **Primeros títulos:**
  - 2025 PPR987842: Increased Reproducibility of Brain Organoids through Controlled Fluid Dynamics
- **Útiles / comentario:** AUSENCIA. Un resultado de organoides cerebrales, espurio.

### B83 — NASA NTRS — 2026-10-19

- **Cadena:** `RNA interference plants spaceflight`
- **Resultados declarados por la base:** 0
- **Primeros títulos:** ninguno
- **Útiles / comentario:** 0 informes de NASA.

### B84 — NASA NTRS — 2026-10-19

- **Cadena:** `dsRNA microgravity`
- **Resultados declarados por la base:** 0
- **Primeros títulos:** ninguno
- **Útiles / comentario:** 0 informes de NASA.

### B85 — NASA NTRS — 2026-10-19

- **Cadena:** `plant pathogen microgravity susceptibility`
- **Resultados declarados por la base:** 4
- **Primeros títulos:**
  - NTRS 20040112387 (2011): Growth in microgravity increases susceptibility of soybean to a fungal pathogen
  - NTRS 20190029577 (2019): Effects of Low-Shear Simulated Microgravity on Soil Bacterium Pantoea Agglomerans
  - NTRS 20190030511 (2019): The Effects of Low-Shear Simulated Microgravity on Soil Bacterium Pantoea Agglomerans
  - NTRS 20040088438 (2019): Plants, plant pathogens, and microgravity--a deadly trio
- **Útiles / comentario:** Cuatro registros: Ryba-White 2001 (M3-41), Leach 2001 (M3-42) y dos de Pantoea agglomerans (bacteria del suelo en RWV, no leídos).

### B86 — NASA NTRS — 2026-10-19

- **Cadena:** `phytoplasma OR Spiroplasma OR Mycoplasma microgravity`
- **Resultados declarados por la base:** 0
- **Primeros títulos:** ninguno
- **Útiles / comentario:** AUSENCIA. 0 informes de NASA.


## Punto 1 (plantas en vuelo: defensa, silenciamiento, cereales)

### B04 — Europe PMC — 2026-10-19

- **Cadena:** `(spaceflight OR microgravity OR "International Space Station") AND Arabidopsis AND (Dicer OR DCL OR Argonaute OR AGO OR RDR OR "RNA silencing" OR "RNA-directed RNA polymerase")`
- **Resultados declarados por la base:** 111
- **Primeros títulos:**
  - 2026 PMC13096386: Evaluating microbial community profiles of Chile peppers grown on the International Space Station provides imp
  - 2025 PMC12220480: Rotifers in space: transcriptomic response of the bdelloid rotifer Adineta vaga aboard the International Space
  - 2025 PMC12292048: Translational insights into abiotic interactions: From Arabidopsis to crop plants.
  - 2024 PMC11426028: Microbiology of human spaceflight: microbial responses to mechanical forces that impact health and habitat sus
  - 2023 PMC10058394: Brachypodium distachyon Seedlings Display Accession-Specific Morphological and Transcriptomic Responses to the
- **Útiles / comentario:** Útiles: M3-26, M3-04, M3-03. Ninguno mide DCL, AGO o RDR.

### B05 — Europe PMC — 2026-10-19

- **Cadena:** `(spaceflight OR microgravity) AND (plant OR Arabidopsis) AND (microRNA OR miRNA OR "small RNA" OR siRNA)`
- **Resultados declarados por la base:** 206
- **Primeros títulos:**
  - 2026 PMC13230747: Genome-wide ribosome profiling reveals a dynamic translational landscape in Arabidopsis seedling roots under s
  - 2026 PMC13149593: Reactivation and Management of Endogenous Latent Herpesviruses in the Spaceflight Environment.
  - 2025 PMC12177493: Exploring plant responses to altered gravity for advancing space agriculture.
  - 2026 PMC12903758: Astroimmunology: the effects of spaceflight and its associated stressors on the immune system.
  - 2025 PMC12562242: The Heart in Space: Effects of Microgravity on Different Cell Types and Their Functions in the Cardiovascular 
- **Útiles / comentario:** Útiles: M3-04 y M3-28; el artículo M3-01 aparece en otras consultas con los miARN.

### B06 — Europe PMC — 2026-10-19

- **Cadena:** `(spaceflight OR microgravity OR clinostat) AND ("Zea mays" OR maize) `
- **Resultados declarados por la base:** 228
- **Primeros títulos:**
  - 2026 PMC13287604: Maize (Zea mays L.) survival on Mars depends on regolith's chemical composition rather than reduced gravity or
  - 2025 PMC12329188: Reactive oxygen species act as signaling molecules to control root hair initiation and tip growth.
  - 2026 PMC13463293: Space-flown spearmint (Mentha spicata L.) seeds potentially tolerate nitro-oxidative stress from plasma-activa
  - 2021 PPR423965: Influence of selected plant growth stimulators in enhancing germinability and germination parameters of  Zea m
  - 2025 PMC12220480: Rotifers in space: transcriptomic response of the bdelloid rotifer Adineta vaga aboard the International Space
- **Útiles / comentario:** Útil: M3-29 (maíz en RPM con regolito). El resto es gravitropismo y raíces.

### B07 — Europe PMC — 2026-10-19

- **Cadena:** `(spaceflight OR "International Space Station" OR microgravity) AND (plant OR Arabidopsis) AND ("defense response" OR "plant immunity" OR "innate immunity" OR "pathogenesis-related" OR "salicylic acid" OR "jasmonic acid")`
- **Resultados declarados por la base:** 236
- **Primeros títulos:**
  - 2026 PMC13123239: Stress and light spectral quality influence the transcriptome of a tomato crop on the International Space Stat
  - 2026 PMC13566835: Beyond Earth: Recent Advancements in Microgravity Biomedical and Genetic Research in Saudi Arabia.
  - 2023 PMC10485020: Microgravity and evasion of plant innate immunity by human bacterial pathogens.
  - 2026 PMC13342545: Plasma nitrogen fixation for future lunar agriculture.
  - 2026 PMC12828010: Biofilms: from the cradle of life to life support.
- **Útiles / comentario:** Útiles: M3-10 (revisión), M3-06. Aparece el preprint de Salmonella en lechuga (PPR1210186), no abierto.

### B08 — Europe PMC — 2026-10-19

- **Cadena:** `(spaceflight OR "International Space Station") AND (Oryza OR rice OR wheat OR Triticum OR Brachypodium OR sorghum OR barley) AND (transcriptome OR RNA-seq OR "gene expression")`
- **Resultados declarados por la base:** 280
- **Primeros títulos:**
  - 2026 42832261: Comparison of Streptococcus mutans growth-phase-dependent transcriptome changes in two different simulated mic
  - 2026 PMC13637945: Comparison of Streptococcus mutans growth-phase-dependent transcriptome changes in two different simulated mic
  - 2026 PMC13290553: Rice and shine: a review of miRNA-mediated responses to abiotic stress in Oryza sativa, from drought to ionizi
  - 2026 PMC13381868: Multiomics analysis of the molecular and single-cell responses of rice after deep-space flight on Chang'e-5.
  - 2025 PMC12292048: Translational insights into abiotic interactions: From Arabidopsis to crop plants.
- **Útiles / comentario:** Útiles: M3-04, M3-05; confirma la ausencia de maíz y la presencia de arroz y Brachypodium.

### B09 — Europe PMC — 2026-10-19

- **Cadena:** `(spaceflight OR "International Space Station" OR Tiangong OR "space station") AND (Arabidopsis) AND (EMCS OR "SEEDLING GROWTH" OR APEX OR "Advanced Plant Experiment" OR "Veggie")`
- **Resultados declarados por la base:** 139
- **Primeros títulos:**
  - 2026 PMC13123239: Stress and light spectral quality influence the transcriptome of a tomato crop on the International Space Stat
  - 2026 PMC13096386: Evaluating microbial community profiles of Chile peppers grown on the International Space Station provides imp
  - 2025 PMC12177493: Exploring plant responses to altered gravity for advancing space agriculture.
  - 2026 PMC13392110: Review of carbon dioxide removal and recycling in space.
  - 2025 PMC12117163: Raman spectroscopy as a tool for assessing plant growth in space and on lunar regolith simulants.
- **Útiles / comentario:** Útiles: M3-06, M3-02, M3-30.


## Punto 2 (planta-microbio y susceptibilidad)

### B38 — Europe PMC — 2026-10-19

- **Cadena:** `zinnia AND (Fusarium OR "International Space Station" OR Veggie)`
- **Resultados declarados por la base:** 121
- **Primeros títulos:**
  - 2026 PMC13311008: Microbial community characterization of multi-crop growouts in the XROOTS aeroponic-hydroponic system on the I
  - 2026 PMC12915293: Transposon sequencing reveals Burkholderia gene fitness in a spaceflight-relevant plant-pathogen interaction.
  - 2026 41565401: Insights into the effect of microgravity on phytopathogens and plant-associated microbes.
  - 2021 33926205: Fusarium oxysporum as an Opportunistic Fungal Pathogen on Zinnia hybrida Plants Grown on board the Internation
  - 2026 PMC13610288: Combating Two Major Fungal Diseases in Marigold (Tagetes spp.): Insights into Pathogen Identification and Anti
- **Útiles / comentario:** Útiles: M3-35, M3-36, M3-09, M3-37; el genoma de Fusarium (PMC5958250) se vio en el listado, no se leyó.

### B39 — Europe PMC — 2026-10-19

- **Cadena:** `(spaceflight OR microgravity OR "International Space Station") AND plant AND (pathogen OR pathogenesis OR phytopathogen OR "disease susceptibility") AND NOT (astronaut OR "human")`
- **Resultados declarados por la base:** 76
- **Primeros títulos:**
  - 2026 PMC13410264: Hypervirulence Characteristics of Spaceflight-Mutated Beauveria bassiana Isolate for Integrated Control of Swe
  - 2026 42601164: The microbial communities of a tomato crop grown in Veggie under different lighting regimes on the Internation
  - 2026 41397306: Simulated Microgravity Enhances Germ Tube Elongation by Golovinomyces cichoracearum on Cucurbita pepo and Arab
  - 2025 PMC12185730: CeO2 nanomaterial regulates wheat endophytic and rhizospheric bacteria to enhance resistance under simulated m
  - 2025 PMC11988762: The Growth of Soybean (Glycine max) Under Salt Stress Is Modulated in Simulated Microgravity Conditions.
- **Útiles / comentario:** Útiles: M3-13 y M3-37; M3-14 aparece como bioensayo terrestre.

### B40 — Europe PMC — 2026-10-19

- **Cadena:** `("simulated microgravity" OR clinostat OR "random positioning machine" OR RWV) AND (plant OR Arabidopsis OR tomato OR rice) AND (Pseudomonas OR Xanthomonas OR Fusarium OR Botrytis OR Phytophthora OR "plant-pathogen" OR Agrobacterium OR rhizobia OR symbiosis)`
- **Resultados declarados por la base:** 123
- **Primeros títulos:**
  - 2026 PMC13089075: Microbial community characterization in semi-hydroponic systems of Starbor kale (Brassica oleracea L.) grown u
  - 2026 PMC13141840: Microgravity effects on secondary metabolism of plant-affecting bacteria.
  - 2026 PMC12915293: Transposon sequencing reveals Burkholderia gene fitness in a spaceflight-relevant plant-pathogen interaction.
  - 2026 42350404: Simulated microgravity weakens wheat root microbial network against pathogens.
  - 2025 PMC12409115: Microbial drivers of root plasticity.
- **Útiles / comentario:** Útiles: M3-09, M3-12, M3-39, M3-13, M3-10, M3-11.

### B78 — Europe PMC — 2026-10-19

- **Cadena:** `(flg22 OR PAMP OR "pattern-triggered immunity" OR "effector-triggered" OR "systemic acquired resistance" OR "plant immune") AND (spaceflight OR microgravity OR clinostat OR "random positioning machine") AND PUB_YEAR:[2020 TO 2026]`
- **Resultados declarados por la base:** 34
- **Primeros títulos:**
  - 2026 PMC13539599: Gastrointestinal motility in microgravity: a critical review of multi-level mechanisms and model-dependent eff
  - 2025 PMC12785337: New Knowledge About Tissue Engineering Under Microgravity Conditions in Space and on Earth.
  - 2023 PMC10485020: Microgravity and evasion of plant innate immunity by human bacterial pathogens.
  - 2025 PMC12322194: Space-driven ROS in cells: a hidden danger to astronaut health and food safety.
  - 2026 PMC12828010: Biofilms: from the cradle of life to life support.
- **Útiles / comentario:** Útiles: M3-10, M3-13, M3-09. Ninguno mide inmunidad de PAMP o efectores en vuelo.

### B79 — Europe PMC — 2026-10-19

- **Cadena:** `(plant OR crop) AND (spaceflight OR microgravity OR "simulated microgravity") AND (disease OR pathogen OR phytopathogen) AND (susceptib* OR resistan*) AND PUB_YEAR:[2024 TO 2026]`
- **Resultados declarados por la base:** 213
- **Primeros títulos:**
  - 2026 PMC13566835: Beyond Earth: Recent Advancements in Microgravity Biomedical and Genetic Research in Saudi Arabia.
  - 2026 PMC13141840: Microgravity effects on secondary metabolism of plant-affecting bacteria.
  - 2026 PMC12828010: Biofilms: from the cradle of life to life support.
  - 2026 PMC13468469: An Inulin-Type Atractylodes Macrocephala Polysaccharide Alleviates Weightlessness-Induced Bone Loss in Associa
  - 2026 PMC13089075: Microbial community characterization in semi-hydroponic systems of Starbor kale (Brassica oleracea L.) grown u
- **Útiles / comentario:** Útiles: M3-12, M3-13, M3-06, M3-32.

### B80 — Europe PMC — 2026-10-19

- **Cadena:** `(TITLE_ABS:"Argonaute" OR TITLE_ABS:"Dicer-like" OR TITLE_ABS:"RNA-dependent RNA polymerase" OR TITLE_ABS:"RdDM" OR TITLE_ABS:"siRNA") AND (TITLE_ABS:"spaceflight" OR TITLE_ABS:"microgravity" OR TITLE_ABS:"space flight") AND (TITLE_ABS:"plant" OR TITLE_ABS:"Arabidopsis" OR TITLE_ABS:"rice" OR TITLE_ABS:"wheat")`
- **Resultados declarados por la base:** 1
- **Primeros títulos:**
  - 2009 19135069: Spaceflight induces both transient and heritable alterations in DNA methylation and gene expression in rice (O
- **Útiles / comentario:** AUSENCIA. Un solo resultado: M3-48 (arroz, genes de proteínas de siRNA).


## Punto 3 (insectos)

### B41 — Europe PMC — 2026-10-19

- **Cadena:** `(Drosophila) AND (spaceflight OR "space flight" OR "International Space Station" OR microgravity) AND (immun* OR Toll OR "antimicrobial peptide" OR infection)`
- **Resultados declarados por la base:** 479
- **Primeros títulos:**
  - 2026 PMC13566835: Beyond Earth: Recent Advancements in Microgravity Biomedical and Genetic Research in Saudi Arabia.
  - None PMC13647352: Microbial adaptation and biological effects in the spaceflight environment
  - 2026 PMC13566718: Aging in Spaceflight, Oxidative Stress, and Microbiome Dysbiosis: A Comprehensive Review.
  - 2026 PMC13348333: Kaempferol Attenuates Spaceflight-Associated Knee Cartilage Degradation by Targeting NOX4-Mediated Mitochondri
  - 2026 PMC13448024: Biological clocks and blood clots in space: circadian disruption-induced modulation of thrombosis risk.
- **Útiles / comentario:** Útiles: M3-15; los estudios de Drosophila M3-16, M3-17, M3-18 salen en B45 y B46.

### B42 — Europe PMC — 2026-10-19

- **Cadena:** `(aphid OR aphids OR "Acyrthosiphon pisum" OR Hemiptera OR planthopper OR leafhopper OR Cicadellidae OR "Nilaparvata" OR "Bemisia" OR "stink bug") AND (spaceflight OR microgravity OR "space station" OR clinostat OR "free fall" OR "parabolic flight")`
- **Resultados declarados por la base:** 60
- **Primeros títulos:**
  - 2026 PMC13410264: Hypervirulence Characteristics of Spaceflight-Mutated Beauveria bassiana Isolate for Integrated Control of Swe
  - 2025 PMC11846945: Melanin from the fungus Gliocephalotrichum simplex protects seeds from the effects of exposure to gamma radiat
  - 2026 PMC12982320: Impact of the pesticide fipronil on honey quality and the survival of Apis mellifera bees.
  - 2026 PMC12999521: Limited thermal tolerance in tropical insects and its genomic signature.
  - 2014 25104755: The stimuli evoking the aerial-righting posture of falling pea aphids.
- **Útiles / comentario:** AUSENCIA de hemípteros: el único acierto (M3-14) usa hemípteros como blanco de un bioensayo terrestre; el resto es ruido (un trabajo de 2014 sobre áfidos en caída, visto solo por el título, que no parece vuelo espacial).

### B43 — Europe PMC — 2026-10-19

- **Cadena:** `(insect OR insects) AND (RNAi OR "RNA interference" OR dsRNA OR siRNA) AND (spaceflight OR microgravity OR "space station" OR clinostat OR "random positioning machine")`
- **Resultados declarados por la base:** 131
- **Primeros títulos:**
  - 2026 PMC13350859: MAPK/PMK-1 innate immune signaling protects the nematode Caenorhabditis elegans from increased intestinal colo
  - 2026 PMC13565916: Impact of Microgravity on Cytoskeletal Dynamics, Protein Transport, and Signaling Networks: Potential Therapeu
  - 2026 PMC13566835: Beyond Earth: Recent Advancements in Microgravity Biomedical and Genetic Research in Saudi Arabia.
  - 2025 PMC12748995: PI3K/AKT/mTOR pathway and c-Myc inhibit hepatocyte suspension under simulated microgravity.
  - 2026 PMC13039024: Cosmic silence and viral noise: transcriptomic crosstalk in Caenorhabditis elegans under simulated space condi
- **Útiles / comentario:** AUSENCIA. Los 10 primeros son C. elegans, mamíferos y revisiones; ningún insecto con RNAi en vuelo.

### B44 — Europe PMC — 2026-10-19

- **Cadena:** `Seedborne fungal contamination consequences in space-grown wheat Bishop Levine`
- **Resultados declarados por la base:** 2
- **Primeros títulos:**
  - 1997 IND21233362: Seedborne fungal contamination: consequences in space-grown wheat
  - 1997 11540734: Seedborne fungal contamination: consequences in space-grown wheat.
- **Útiles / comentario:** Localiza M3-40 (resumen).

### B45 — Europe PMC — 2026-10-19

- **Cadena:** `TITLE:"Drosophila" AND (TITLE:"spaceflight" OR TITLE:"space flight" OR TITLE:"microgravity" OR TITLE:"space") AND (TITLE:"immun*" OR TITLE:"infection" OR TITLE:"virulence" OR TITLE:"parasitoid")`
- **Resultados declarados por la base:** 2
- **Primeros títulos:**
  - 2020 PMC7000411: Spaceflight and simulated microgravity conditions increase virulence of Serratia marcescens in the Drosophila 
  - 2014 PMC3901686: Toll mediated infection response is altered by gravity and spaceflight in Drosophila.
- **Útiles / comentario:** Útiles: M3-18, M3-16.

### B46 — Europe PMC — 2026-10-19

- **Cadena:** `Drosophila parasitoids go to space spaceflight Leptopilina`
- **Resultados declarados por la base:** 1
- **Primeros títulos:**
  - 2024 PMC10797188: Drosophila parasitoids go to space: Unexpected effects of spaceflight on hosts and their parasitoids.
- **Útiles / comentario:** Útil: M3-17.

### B47 — Europe PMC — 2026-10-19

- **Cadena:** `(Drosophila) AND (spaceflight OR "space flight") AND (RNAi OR "RNA interference" OR siRNA OR piRNA OR "small RNA")`
- **Resultados declarados por la base:** 79
- **Primeros títulos:**
  - 2026 PMC13350859: MAPK/PMK-1 innate immune signaling protects the nematode Caenorhabditis elegans from increased intestinal colo
  - 2026 PMC13348333: Kaempferol Attenuates Spaceflight-Associated Knee Cartilage Degradation by Targeting NOX4-Mediated Mitochondri
  - 2026 PMC12886544: A systematic review of microgravity on reproductive systems: Implications for space biology and human health.
  - None PMC13647352: Microbial adaptation and biological effects in the spaceflight environment
  - 2026 PMC13371913: Spaceflight multi-omics reveals vulnerabilities of human germ cell development.
- **Útiles / comentario:** AUSENCIA de RNAi/piRNA en Drosophila en vuelo con esas palabras: los 8 títulos vistos de 79 son clínicos, de nematodos o revisiones; no se miraron los demás.

### B48 — Europe PMC — 2026-10-19

- **Cadena:** `(TITLE_ABS:"RNAi" OR TITLE_ABS:"RNA interference") AND (TITLE_ABS:"spaceflight" OR TITLE_ABS:"microgravity" OR TITLE_ABS:"International Space Station" OR TITLE_ABS:"space flight")`
- **Resultados declarados por la base:** 13
- **Primeros títulos:**
  - 2026 PMC13350859: MAPK/PMK-1 innate immune signaling protects the nematode Caenorhabditis elegans from increased intestinal colo
  - 2026 PMC13024336: Acceleration and Light-Induced Changes in Cytosolic cAMP Concentration in Euglena gracilis.
  - 2021 33280816: Notch receptor GLP-1 regulates toxicity of simulated microgravity stress by activating germline-intestine comm
  - 2021 PMC7820273: Intestinal long non-coding RNAs in response to simulated microgravity stress in Caenorhabditis elegans.
  - 2019 31351586: Intestine-specific activity of insulin signaling pathway in response to microgravity stress in Caenorhabditis 
- **Útiles / comentario:** Trece resultados; el único RNAi en vuelo de un animal es C. elegans (M3-19, CERISE). El resto son C. elegans con RNAi como herramienta para estudiar microgravedad simulada (títulos; no abiertos) y M3-49 (planta).

### B49 — Europe PMC — 2026-10-19

- **Cadena:** `(TITLE_ABS:"dsRNA" OR TITLE_ABS:"double-stranded RNA" OR TITLE_ABS:"siRNA" OR TITLE_ABS:"small interfering RNA") AND (TITLE_ABS:"spaceflight" OR TITLE_ABS:"microgravity" OR TITLE_ABS:"clinostat" OR TITLE_ABS:"space station")`
- **Resultados declarados por la base:** 20
- **Primeros títulos:**
  - 2026 42601142: Double-stranded RNA and reverse transcriptase signatures of endogenous retroviruses after exposure to spacefli
  - 2026 PMC13605618: Mechanical Unloading Inhibits Osteoblast Differentiation via Downregulation of OGT-Mediated O-GlcNAcylation.
  - 2026 41275932: Redox-regulated bone loss in spaceflight and terrestrial models: Molecular mechanisms and therapeutic strategi
  - 2020 32240849: Primary cilia act as microgravity sensors by depolymerizing microtubules to inhibit osteoblastic differentiati
  - 2023 36931096: Ellagic acid inhibits CDK12 to increase osteoblast differentiation and alleviate osteoporosis in hindlimb-unlo
- **Útiles / comentario:** Veinte resultados, casi todos de hueso y células de mamífero. Ninguno une dsRNA o siRNA con fitosanidad.

### B50 — Europe PMC — 2026-10-19

- **Cadena:** `(TITLE_ABS:"RNA silencing" OR TITLE_ABS:"gene silencing" OR TITLE_ABS:"RNA interference") AND (TITLE_ABS:"plant" OR TITLE_ABS:"Arabidopsis") AND (TITLE_ABS:"microgravity" OR TITLE_ABS:"spaceflight" OR TITLE_ABS:"clinostat" OR TITLE_ABS:"altered gravity")`
- **Resultados declarados por la base:** 2
- **Primeros títulos:**
  - 2021 33612180: Synthetic biological circuit tested in spaceflight.
  - 2017 28926746: Effect of modeled microgravity on UV-C-induced interplant communication of Arabidopsis thaliana.
- **Útiles / comentario:** Dos resultados: M3-49 (Arabidopsis con circuito de silenciamiento en la ISS) y M3-50 (silenciamiento transcripcional con clinostato).


## Puntos 1 a 3 (hemípteros por género, virus, Agrobacterium, trigo)

### B63 — Europe PMC — 2026-10-19

- **Cadena:** `(TITLE_ABS:"Rhodnius" OR TITLE_ABS:"Pyrrhocoris" OR TITLE_ABS:"Oncopeltus" OR TITLE_ABS:"Cimex" OR TITLE_ABS:"Halyomorpha" OR TITLE_ABS:"Acyrthosiphon" OR TITLE_ABS:"Myzus" OR TITLE_ABS:"Nilaparvata" OR TITLE_ABS:"Dalbulus" OR TITLE_ABS:"Bemisia" OR TITLE_ABS:"Hemiptera") AND (TITLE_ABS:"microgravity" OR TITLE_ABS:"spaceflight" OR TITLE_ABS:"space flight" OR TITLE_ABS:"weightlessness" OR TITLE_ABS:"clinostat" OR TITLE_ABS:"parabolic flight")`
- **Resultados declarados por la base:** 1
- **Primeros títulos:**
  - 2026 PMC13410264: Hypervirulence Characteristics of Spaceflight-Mutated Beauveria bassiana Isolate for Integrated Control of Swe
- **Útiles / comentario:** El único resultado es M3-14. Ningún hemíptero en vuelo ni en simulada con esos géneros.

### B64 — Europe PMC — 2026-10-19

- **Cadena:** `(TITLE_ABS:"plant virus" OR TITLE_ABS:"viral infection" OR TITLE_ABS:"tobacco mosaic" OR TITLE_ABS:"potyvirus") AND (TITLE_ABS:"spaceflight" OR TITLE_ABS:"microgravity" OR TITLE_ABS:"space station") AND (TITLE_ABS:"plant" OR TITLE_ABS:"plants")`
- **Resultados declarados por la base:** 4
- **Primeros títulos:**
  - 2026 PMC13241316: Streamlined molecular farming of plant virus therapeutics for space flight and other low-resource environments
  - 2007 18372724: Aspects of adaptive answering formation in virus-host plant pathosystem for different wheat cultivars under si
  - 2004 16240513: Clinostating effects on Apogee wheat resistance to wheat streak mosaic virus.
  - 1995 PMC1236220: Protein and virus crystal growth on international microgravity laboratory-2.
- **Útiles / comentario:** Útiles: M3-43 y M3-44 (trigo y virus del mosaico estriado, clinostato). Aparece un artículo de 2026 sobre producción molecular de terapéuticos en plantas para el vuelo (PMC13241316), no abierto.

### B65 — Europe PMC — 2026-10-19

- **Cadena:** `(TITLE_ABS:"Agrobacterium") AND (TITLE_ABS:"microgravity" OR TITLE_ABS:"spaceflight" OR TITLE_ABS:"clinostat")`
- **Resultados declarados por la base:** 2
- **Primeros títulos:**
  - 1995 11538784: Enhancing effects of simulated microgravity on Agrobacterium-infected frequency of tobacco callus.
  - 1997 11541870: Agravitropic behaviour of roots of rapeseed (Brassica napus L.) transformed by Agrobacterium rhizogenes.
- **Útiles / comentario:** Útil: M3-45. El otro resultado es de raíces transformadas con A. rhizogenes (1997), no leído.

### B66 — Europe PMC — 2026-10-19

- **Cadena:** `(TITLE_ABS:"wheat" OR TITLE_ABS:"Triticum") AND (TITLE_ABS:"spaceflight" OR TITLE_ABS:"International Space Station" OR TITLE_ABS:"space station" OR TITLE_ABS:"microgravity") AND (TITLE_ABS:"transcriptom*" OR TITLE_ABS:"mRNA" OR TITLE_ABS:"gene expression")`
- **Resultados declarados por la base:** 5
- **Primeros títulos:**
  - 2023 PMC10520342: Modulation of wheatgrass (Triticum aestivum Linn) toxicity against breast cancer cell lines by simulated micro
  - 2006 16708225: Microgravity effects on leaf morphology, cell structure, carbon metabolism and mRNA expression of dwarf wheat.
  - 2020 PMC7106961: Alteration of calcium signalling in cardiomyocyte induced by simulated microgravity and hypergravity.
  - 2009 19413505: Effects of a spaceflight environment on heritable changes in wheat gene expression.
  - 2016 26679611: Regional specific modulation of the glycocalyx and smooth muscle cell contractile apparatus in conduit arterie
- **Útiles / comentario:** Útiles: M3-46, M3-47.


## Punto 5 (mollicutes)

### B51 — Europe PMC — 2026-10-19

- **Cadena:** `(Mycoplasma OR Spiroplasma OR Acholeplasma OR Mollicutes OR mollicute OR phytoplasma OR Phytoplasma) AND (microgravity OR spaceflight OR "space flight" OR "International Space Station" OR clinostat OR "random positioning machine" OR "rotating wall vessel" OR "simulated microgravity")`
- **Resultados declarados por la base:** 256
- **Primeros títulos:**
  - 2026 PMC13600223: The effect of microgravity and flows on the organization and dynamics of the human genome.
  - 2026 PMC13320170: Gravitational and mechanical forces shape mitochondrial translation.
  - 2026 PMC13230533: Effects of altered gravity on adrenergic-mediated cAMP signalling in intact cells.
  - 2026 PMC13089075: Microbial community characterization in semi-hydroponic systems of Starbor kale (Brassica oleracea L.) grown u
  - 2026 PMC12794679: Polydopamine-Based Antioxidant Countermeasures Against Spaceflight-Induced Neurodegeneration.
- **Útiles / comentario:** 256 resultados; los 11 primeros no tratan mollicutes en µg (cultivos celulares, mitocondria). Ver B52 para la versión estrecha.

### B52 — Europe PMC — 2026-10-19

- **Cadena:** `(TITLE_ABS:"Mycoplasma" OR TITLE_ABS:"Spiroplasma" OR TITLE_ABS:"Acholeplasma" OR TITLE_ABS:"phytoplasma") AND (TITLE_ABS:"spaceflight" OR TITLE_ABS:"microgravity" OR TITLE_ABS:"space station" OR TITLE_ABS:"clinorotation")`
- **Resultados declarados por la base:** 0
- **Primeros títulos:** ninguno
- **Útiles / comentario:** AUSENCIA. 0 resultados con los taxones en título o resumen junto a microgravedad, vuelo o clinorrotación.

### B53 — Europe PMC — 2026-10-19

- **Cadena:** `("cell wall-deficient" OR "wall-less" OR "L-form" OR "L-forms" OR "cell wall deficient") AND (microgravity OR spaceflight OR clinostat OR "rotating wall vessel")`
- **Resultados declarados por la base:** 25
- **Primeros títulos:**
  - 2024 PMC10976247: Simulation of Human Movement in Zero Gravity.
  - 2023 PMC10311794: An electrical stimulation intervention protocol to prevent disuse atrophy and muscle strength decline: an expe
  - 2020 PMC9058438: Analysis of the effects of acoustic levitation to simulate the microgravity environment on the development of 
  - 2025 PMC11893237: Aging: A struggle for beneficial to overcome negative factors made by muscle and bone.
  - 2016 PMC5037457: Microgravity induces proteomics changes involved in endoplasmic reticulum stress and mitochondrial protection.
- **Útiles / comentario:** Ningún resultado trata bacterias sin pared en µg (25 resultados; los 10 primeros son de otros temas).

### B54 — Europe PMC — 2026-10-19

- **Cadena:** `(Wolbachia OR "Spiroplasma" OR "endosymbiont") AND (spaceflight OR microgravity) AND (insect OR Drosophila OR mosquito)`
- **Resultados declarados por la base:** 15
- **Primeros títulos:**
  - 2026 PMC12796539: Mitochondria as key targets underlying hypomagnetic field-induced biological effects.
  - 2019 PMC6325168: Pangenomic Approach To Understanding Microbial Adaptations within a Model Built Environment, the International
  - 2023 PMC10825288: Life Detection and Microbial Biomarker Profiling with Signs of Life Detector-Life Detector Chip During a Mars 
  - 2021 PMC8537831: Spatial Characterization of Microbial Communities on Multi-Species Leafy Greens Grown Simultaneously in the Ve
  - 1997 PMC7111279: Subject Index.
- **Útiles / comentario:** Ningún resultado trata Spiroplasma ni Wolbachia en µg.

### B55 — PubMed (NCBI E-utilities) — 2026-10-19

- **Cadena:** `(Mycoplasma[tiab] OR Spiroplasma[tiab] OR Acholeplasma[tiab] OR Mollicutes[tiab] OR phytoplasma[tiab] OR Phytoplasma[tiab]) AND (microgravity[tiab] OR spaceflight[tiab] OR "space flight"[tiab] OR "International Space Station"[tiab] OR clinostat[tiab] OR "random positioning machine"[tiab] OR "rotating wall vessel"[tiab])`
- **Resultados declarados por la base:** 3
- **Primeros títulos:**
  - PMID 23493725 (2013): Mycoplasma genitalium infection activates cellular host defense and inflammation pathways in a 3-dimensional h
  - PMID 23053434 (2012): Microbial products alter the expression of membrane-associated mucin and antimicrobial peptides in a three-dim
  - PMID 808208 (1975): The effects of cosmic particle radiation on pocket mice aboard Apollo XVII: II. Characteristics and tolerances
- **Útiles / comentario:** Tres resultados, ninguno es un mollicute en µg: dos sobre modelos 3D humanos de epitelio endocervical (uno es M3-53) y uno de ratones de Apollo XVII.

### B56 — PubMed (NCBI E-utilities) — 2026-10-19

- **Cadena:** `Mycoplasma[tiab] AND contamination[tiab] AND (spaceflight[tiab] OR microgravity[tiab] OR "space station"[tiab])`
- **Resultados declarados por la base:** 0
- **Primeros títulos:** ninguno
- **Útiles / comentario:** 0 resultados.

### B57 — PubMed (NCBI E-utilities) — 2026-10-19

- **Cadena:** `(RNAi[tiab] OR dsRNA[tiab] OR siRNA[tiab] OR "RNA interference"[tiab] OR "spray-induced gene silencing"[tiab] OR "host-induced gene silencing"[tiab]) AND (microgravity[tiab] OR spaceflight[tiab] OR clinostat[tiab] OR "random positioning machine"[tiab] OR "simulated microgravity"[tiab]) AND (plant[tiab] OR crop[tiab] OR insect[tiab] OR pest[tiab] OR phytopathogen[tiab] OR fungus[tiab] OR virus[tiab])`
- **Resultados declarados por la base:** 2
- **Primeros títulos:**
  - PMID 33612180 (2021): Synthetic biological circuit tested in spaceflight.
  - PMID 19135069 (2009): Spaceflight induces both transient and heritable alterations in DNA methylation and gene expression in rice (O
- **Útiles / comentario:** Dos resultados: M3-49 y M3-48; ninguno valida RNAi contra patógeno o plaga.

### B58 — PubMed (NCBI E-utilities) — 2026-10-19

- **Cadena:** `(Zea mays[tiab] OR maize[tiab]) AND (microgravity[tiab] OR spaceflight[tiab] OR "space flight"[tiab] OR clinostat[tiab] OR "random positioning machine"[tiab])`
- **Resultados declarados por la base:** 47
- **Primeros títulos:**
  - PMID 14631938 (2003): A polarized cell: the root statocyte.
  - PMID 11537807 (1986): Investigations onboard the biosatellite Cosmos-1667.
  - PMID 25588706 (2015): The electrical network of maize root apex is gravity dependent.
  - PMID 24258370 (1984): Phytochrome-mediated phototropism in maize seedling shoots.
  - PMID 12644685 (2003): Enhanced gravitropism of roots with a disrupted cap actin cytoskeleton.
- **Útiles / comentario:** 47 resultados; útiles: M3-40, M3-51, M3-52. El resto es gravitropismo de raíz (décadas de antigüedad).

### B73 — Europe PMC — 2026-10-19

- **Cadena:** `Spiroplasma AND (spaceflight OR microgravity OR clinostat OR "International Space Station")`
- **Resultados declarados por la base:** 3
- **Primeros títulos:**
  - 2025 PMC12763976: Microbial community characterization in Red Sea-derived samples using a field-deployable DNA extraction system
  - 2022 PMC9326679: Streamlining Culture Conditions for the Neuroblastoma Cell Line SH-SY5Y: A Prerequisite for Functional Studies
  - 2003 PMC2304010: 47th Annual Meeting March 1-5, 2003 Henry B. Gonzalez Convention Center, San Antonio, Texas : Wednesday Poster
- **Útiles / comentario:** Tres resultados espurios (microbioma del Mar Rojo, protocolo de neuroblastoma, pósters). Ninguno con Spiroplasma en µg.

### B74 — Europe PMC — 2026-10-19

- **Cadena:** `Mycoplasma AND ("International Space Station" OR spaceflight) AND (microbiome OR surfaces OR environmental OR isolates)`
- **Resultados declarados por la base:** 57
- **Primeros títulos:**
  - 2026 PMC12960706: Submarine medicine as an analog for spaceflight: a review of acute medical care.
  - 2026 PMC12794679: Polydopamine-Based Antioxidant Countermeasures Against Spaceflight-Induced Neurodegeneration.
  - 2025 PMC12764381: Nanobioreactor detection of space-associated hematopoietic stem and progenitor cell aging.
  - 2025 PMC11929851: Reactivation of latent human intracellular infections during a months-long expedition at the Antarctic Vostok 
  - 2023 PMC10284894: Microbial applications for sustainable space exploration beyond low Earth orbit.
- **Útiles / comentario:** Cincuenta y siete resultados; los primeros ocho no tratan mollicutes en la ISS. Para el taxón, ver B76.

### B75 — Europe PMC — 2026-10-19

- **Cadena:** `Acholeplasma AND (microgravity OR spaceflight OR clinostat OR "rotating wall")`
- **Resultados declarados por la base:** 3
- **Primeros títulos:**
  - 2021 PMC8251645: Posters
  - 2019 PMC6610278: Posters
  - 2014 PMC7163937: Poster Sessions
- **Útiles / comentario:** Tres resultados, todos pósters sin relación.

### B76 — Europe PMC — 2026-10-19

- **Cadena:** `Mollicutes AND (microgravity OR spaceflight)`
- **Resultados declarados por la base:** 9
- **Primeros títulos:**
  - 2022 PMC8928191: Comparing Long-Read Assemblers to Explore the Potential of a Sustainable Low-Cost, Low-Infrastructure Approach
  - 2024 PMC10972136: The Research Progress on the Interaction between Mammalian Gut Microbiota and the Host's Metabolism Homeostasi
  - 2015 PMC4624184: Microbiomes of the dust particles collected from the International Space Station and Spacecraft Assembly Facil
  - 2017 PMC5563039: Space-type radiation induces multimodal responses in the mouse gut microbiome and metabolome.
  - 2021 PMC8251645: Posters
- **Útiles / comentario:** Nueve resultados; M3-33 y M3-34 mencionan el taxón Mollicutes en perfiles de microbioma, sin ser estudios de mollicutes.

### B77 — Europe PMC — 2026-10-19

- **Cadena:** `(Mycoplasma OR mycoplasma) AND ("rotating wall vessel" OR "simulated microgravity" OR "modeled microgravity" OR "low-shear")`
- **Resultados declarados por la base:** 231
- **Primeros títulos:**
  - 2026 PMC13600223: The effect of microgravity and flows on the organization and dynamics of the human genome.
  - 2025 PMC12663655: SIRT3 regulates PDHA1 acetylation in HUVECs to modulate inflammation and pyroptosis under clinorotation.
  - 2026 PMC13230533: Effects of altered gravity on adrenergic-mediated cAMP signalling in intact cells.
  - 2026 PMC13320170: Gravitational and mechanical forces shape mitochondrial translation.
  - 2024 PMC11324864: Simulated microgravity impairs human NK cell cytotoxic activity against space radiation-relevant leukemic cell
- **Útiles / comentario:** Doscientos treinta y un resultados; los 8 títulos vistos son de células de mamífero y otros temas en RWV o µg simulada.


## Punto 5 (cultivo axénico)

### B87 — Europe PMC — 2026-10-19

- **Cadena:** `phytoplasma AND ("axenic culture" OR "cell-free medium" OR "cannot be cultured" OR "unculturable" OR "not been cultured") AND (review OR obligate)`
- **Resultados declarados por la base:** 426
- **Primeros títulos:**
  - 2026 PMC13462277: Can the leafhopper microbiome unlock new strategies for its control?
  - 2026 PMC13535232: Potato purple top phytoplasma infection induces autophagy-associated lipid dynamics that support pathogen prol
  - 2026 41582677: Improving Effector Protein Prediction in Phytoplasmas Through Structural Analysis of Signal Peptide Cleavage.
  - 2026 PMC13415861: Multilocus Molecular Characterization of a 16SrII-D Phytoplasma Infecting Black Carrot in Türkiye.
  - 2026 PMC13306697: Host Diversity and Phylogenetic Evolution of Phytoplasmas on Hainan Island in China, Bringing Challenges to Mo
- **Útiles / comentario:** Sirve para localizar M3-54; los 426 resultados son estudios de detección y filogenia de fitoplasmas.

### B88 — Europe PMC — 2026-10-19

- **Cadena:** `Spiroplasma kunkelii AND (culture OR "in vitro" OR axenic OR medium) AND maize`
- **Resultados declarados por la base:** 22
- **Primeros títulos:**
  - 2026 PMC13462277: Can the leafhopper microbiome unlock new strategies for its control?
  - 2024 PMC11392750: Editorial: Spiroplasma, Mycoplasma, Phytoplasma, and other genome-reduced and wall-less mollicutes: their gene
  - 2025 PMC12565353: Males of Dalbulus maidis Attract Females Through Volatile Compounds with Potential Pheromone Function: A Tool 
  - 2026 PMC13164843: Mixed-Pathogen Infections in Vegetatively Propagated Crops: From Biological Synergism to Integrated Management
  - 2025 PMC12251814: Beyond Single-Pathogen Models: Understanding Mixed Infections Involving Phytoplasmas and Other Plant Pathogens
- **Útiles / comentario:** Útiles: ninguno directo; aparece la revisión de microbioma de cicadélidos (PMC13462277), que se abrió pero no sostiene ninguna afirmación del informe sobre cultivo de S. kunkelii.


## Punto 6 (plataformas terrestres)

### B67 — Europe PMC — 2026-10-19

- **Cadena:** `(TITLE:"clinostat" OR TITLE:"random positioning machine" OR TITLE:"ground-based" OR TITLE:"microgravity simulat*" OR TITLE:"simulated microgravity") AND (TITLE:"artifact*" OR TITLE:"limitations" OR TITLE:"shear" OR TITLE:"fidelity" OR TITLE:"efficacy" OR TITLE:"validation" OR TITLE:"compar*" OR TITLE:"review")`
- **Resultados declarados por la base:** 68
- **Primeros títulos:**
  - 2026 42118161: Design and validation of an electroporation-capable random positioning machine for the study of cell membrane 
  - 2026 42436195: Simulated microgravity with physiological shear reveals endothelial disruption in a dual-stimulus bioreactor.
  - 2026 PMC13665397: Establishment and Validation of a Novel Microgravity Simulation Platform for Ground-Based Animal Experiments
  - 2026 PMC13357575: The effect of spaceflight and simulated microgravity exposure on thermoregulation in humans: a systematic revi
  - 2026 42884050: Establishment and Validation of a Novel Microgravity Simulation Platform for Ground-Based Animal Experiments.
- **Útiles / comentario:** Sesenta y ocho resultados; los útiles para plataformas salen en B68 y B70.

### B68 — Europe PMC — 2026-10-19

- **Cadena:** `(plant OR Arabidopsis OR seedling) AND ("random positioning machine" OR clinostat) AND (artifact OR "fluid motion" OR "centrifugal" OR "not equivalent" OR "differ from" OR "true microgravity") AND (spaceflight OR "space flight")`
- **Resultados declarados por la base:** 101
- **Primeros títulos:**
  - 2026 PMC13271463: Characterization of the random positioning machine as a microgravity simulator for biological applications.
  - 2026 PMC13022057: Guidelines for use of the random positioning machine as a reduced-gravity analog.
  - 2026 PMC13016929: Physiological and transcriptomic assessment of Arabidopsis identifies two distinct gravity signaling systems.
  - 2025 PMC12216757: Light is sufficient to compensate for random positioning machine-simulated microgravity in plant roots.
  - 2025 PMC12109293: Biological Acoustic Levitation and Its Potential Application for Microgravity Study.
- **Útiles / comentario:** Útiles: M3-20, M3-21, M3-22.

### B69 — Europe PMC — 2026-10-19

- **Cadena:** `Herranz ground-based facilities for simulation of microgravity organism-specific recommendations`
- **Resultados declarados por la base:** 12
- **Primeros títulos:**
  - 2024 PMC10858953: How are cell and tissue structure and function influenced by gravity and what are the gravity perception mecha
  - 2025 PMC12048243: Taking the 3Rs to a higher level: replacement and reduction of animal testing in life sciences in space resear
  - 2023 PMC10442387: Perspectives for plant biology in space and analogue environments.
  - 2023 PMC10448007: Enhancing European capabilities for application of multi-omics studies in biology and biomedicine space resear
  - 2022 PMC8898910: Space omics research in Europe: Contributions, geographical distribution and ESA member state funding schemes.
- **Útiles / comentario:** No devolvió el artículo de Herranz de 2013; útil: M3-26.

### B70 — Europe PMC — 2026-10-19

- **Cadena:** `Wuest simulated microgravity critical review on the use of random positioning machines for mammalian cell culture`
- **Resultados declarados por la base:** 6
- **Primeros títulos:**
  - 2026 PMC12957785: A novel culture flask for clinostat-based simulation of extraterrestrial gravities.
  - 2024 PMC10902453: Microglial activation in spaceflight and microgravity: potential risk of cognitive dysfunction and poor neural
  - 2022 PMC9864955: Lab-on-a-Chip Technologies for Microgravity Simulation and Space Applications.
  - 2024 PMC10815863: Omics Studies of Tumor Cells under Microgravity Conditions.
  - 2015 PMC4310317: Simulated microgravity: critical review on the use of random positioning machines for mammalian cell culture.
- **Útiles / comentario:** Útiles: M3-23, M3-24.

### B71 — Europe PMC — 2026-10-19

- **Cadena:** `(Arabidopsis OR plant) AND ("random positioning machine" OR clinostat) AND (spaceflight) AND (transcriptom* OR "gene expression") AND (compar* OR overlap OR mimic)`
- **Resultados declarados por la base:** 109
- **Primeros títulos:**
  - 2026 PMC13016929: Physiological and transcriptomic assessment of Arabidopsis identifies two distinct gravity signaling systems.
  - 2026 PMC13230747: Genome-wide ribosome profiling reveals a dynamic translational landscape in Arabidopsis seedling roots under s
  - 2026 PMC13141840: Microgravity effects on secondary metabolism of plant-affecting bacteria.
  - 2025 PMC12738728: Potential regulatory modules to integrate microgravity signals into flowering pathways in Arabidopsis thaliana
  - 2026 PMC13566835: Beyond Earth: Recent Advancements in Microgravity Biomedical and Genetic Research in Saudi Arabia.
- **Útiles / comentario:** Útil: M3-28; por los títulos vistos, ningún estudio compara directamente clinostato con vuelo en plantas, salvo lo que cita M3-27.

### B72 — Europe PMC — 2026-10-19

- **Cadena:** `Pyrocystis noctiluca bioassay shear forces ground-based microgravity simulators`
- **Resultados declarados por la base:** 1
- **Primeros títulos:**
  - 2017 PMC5460110: Pyrocystis noctiluca represents an excellent bioassay for shear forces induced in ground-based microgravity si
- **Útiles / comentario:** Útil: M3-25.


## Inventario NASA OSDR

### B10 — NASA OSDR search API — 2026-10-19

- **Cadena:** `Zea mays`
- **Resultados declarados por la base:** 505
- **Primeros títulos:** ninguno
- **Útiles / comentario:** Los 500 devueltos son de GEO y PRIDE, no de vuelo: 0 estudios GeneLab con Zea mays por esta vía.

### B11 — NASA OSDR search API — 2026-10-19

- **Cadena:** `maize`
- **Resultados declarados por la base:** 535
- **Primeros títulos:** ninguno
- **Útiles / comentario:** Igual: 454 de GEO y 43 de PRIDE; ninguno de GeneLab.

### B12 — NASA OSDR search API — 2026-10-19

- **Cadena:** `Oryza sativa`
- **Resultados declarados por la base:** 947
- **Primeros títulos:** ninguno
- **Útiles / comentario:** Igual para Oryza sativa: ningún estudio GeneLab; 'rice spaceflight' (B22) trae solo bacterias.

### B13 — NASA OSDR search API — 2026-10-19

- **Cadena:** `Triticum aestivum`
- **Resultados declarados por la base:** 232
- **Primeros títulos:** ninguno
- **Útiles / comentario:** Un estudio GeneLab de trigo detectado por B21: OSD-622 (hoja de trigo enano, ISS). No se bajaron los datos.

### B14 — NASA OSDR search API — 2026-10-19

- **Cadena:** `Drosophila melanogaster spaceflight`
- **Resultados declarados por la base:** 19
- **Primeros títulos:** ninguno
- **Útiles / comentario:** Primera corrida con un filtro defectuoso que no listaba accesiones; repetida como B89, que lista 15 estudios GeneLab de Drosophila.

### B15 — NASA OSDR search API — 2026-10-19

- **Cadena:** `Drosophila melanogaster`
- **Resultados declarados por la base:** 3837
- **Primeros títulos:**
  - qBNkVYgBuupM187Wezte: Artificial gravity partially protects space-induced neurological deficits in Drosophila melanogaster
- **Útiles / comentario:** Tres estudios de Drosophila con gravedad artificial (OSD-592, -595, -596).

### B16 — NASA OSDR search API — 2026-10-19

- **Cadena:** `Arabidopsis thaliana spaceflight`
- **Resultados declarados por la base:** 59
- **Primeros títulos:**
  - SkQdgZEBF4GVCLprRP6V: Light has a principal role in the Arabidopsis transcriptomic response to the spaceflight environment
  - t0LVvZABFSC8U4d30Shv: Glycome profiling and immunohistochemistry uncover changes in cell walls of Arabidopsis thaliana roo
  - f2Rsf40BA9RL2X-SJu7Q: Arabidopsis transcriptome in Virgin Galactic human-tended suborbital spaceflight
  - bN_6g4QB28eYt3lGNrbz: The effect of spaceflight on transgenic Arabidopsis plants with compromised signaling
  - JN_6g4QB28eYt3lGTrcd: Transcriptional and Post transcriptional Regulation of Seedling Development in Microgravity
- **Útiles / comentario:** 42 estudios GeneLab de Arabidopsis; útiles: OSD-437 (regulación transcripcional y postranscripcional del desarrollo de plántulas en µg; probablemente el experimento Plant RNA Regulation, no verificado), OSD-678 (CARA), OSD-217, OSD-416, OSD-427 (metilación), OSD-375 (Brachypodium). Inventario, no lectura.

### B17 — NASA OSDR search API — 2026-10-19

- **Cadena:** `Zea mays spaceflight`
- **Resultados declarados por la base:** 0
- **Primeros títulos:** ninguno
- **Útiles / comentario:** 0 resultados: no hay estudio GeneLab de Zea mays en vuelo con esas palabras.

### B18 — NASA OSDR search API — 2026-10-19

- **Cadena:** `aphid`
- **Resultados declarados por la base:** 54
- **Primeros títulos:** ninguno
- **Útiles / comentario:** 0 estudios GeneLab de áfidos (54 resultados son de GEO y PRIDE, sin vuelo).

### B19 — NASA OSDR search API — 2026-10-19

- **Cadena:** `Hemiptera`
- **Resultados declarados por la base:** 13
- **Primeros títulos:** ninguno
- **Útiles / comentario:** 0 estudios GeneLab de Hemiptera.

### B20 — NASA OSDR search API — 2026-10-19

- **Cadena:** `Mycoplasma`
- **Resultados declarados por la base:** 60
- **Primeros títulos:**
  - IAtDKpUBWrv14Z5v6BFU: Simulated microgravity impairs human NK cell cytotoxic activity against space radiation-relevant leu
  - g9_6g4QB28eYt3lGOLa6: Real-time quantitative PCR analysis of human cardiovascular progenitor cells flown aboard the Intern
  - T96jGp8BZBdCI5VVxWqs: Sex‐Specific Changes in Brain Organoids from Acute Simulated Galactic Cosmic Radiation are Rescued b
- **Útiles / comentario:** Tres estudios GeneLab con 'Mycoplasma' en metadatos son de células humanas (OSD-812, -344, -999), no del mollicute.

### B21 — NASA OSDR search API — 2026-10-19

- **Cadena:** `wheat spaceflight`
- **Resultados declarados por la base:** 1
- **Primeros títulos:**
  - 2T3EX4wBfj5nQysnFNsn: Microgravity effects on leaf morphology, cell structure, carbon metabolism and mRNA expression of dw
- **Útiles / comentario:** OSD-622, trigo (Microgravity effects on leaf morphology... mRNA), es el estudio de M3-46.

### B22 — NASA OSDR search API — 2026-10-19

- **Cadena:** `rice spaceflight`
- **Resultados declarados por la base:** 5
- **Primeros títulos:**
  - JLjwcYsBzWEMXzYGOfnD: Altered Quorum Sensing and Physiology of Staphylococcus aureus During Spaceflight Detected by Multi-
  - h4k93pUBT6_JreR44zdZ: Impact of simulated microgravity on the growth and proteomic profile of Enterobacter cloacae
  - Ht_6g4QB28eYt3lGMLbq: BRIC-23 GeneLab Process Verification Test: Staphylococcus aureus transcriptomic, proteomic, and meta
  - skKymZABFSC8U4d3Pyij: Response of Staphylococcus aureus physiology and Agr quorum sensing to low shear modelled microgravi
- **Útiles / comentario:** Solo bacterias (Staphylococcus, Enterobacter); ningún arroz.

### B23 — NASA OSDR search API — 2026-10-19

- **Cadena:** `corn`
- **Resultados declarados por la base:** 147
- **Primeros títulos:**
  - T6evhJcBcf0G5RgiBzIN: Apollo 17 Challenge System - Seed Germination (Cabbage, Brussel Sprouts, Radish and Lettuce)
- **Útiles / comentario:** Un acierto GeneLab: OSD-855 (semillas Apollo 17, lechuga y otros); no es maíz.

### B24 — NASA OSDR search API — 2026-10-19

- **Cadena:** `Drosophila`
- **Resultados declarados por la base:** 4111
- **Primeros títulos:**
  - qBNkVYgBuupM187Wezte: Artificial gravity partially protects space-induced neurological deficits in Drosophila melanogaster
  - rhPnsIgBuupM187WwDvP: Artificial gravity partially protects space-induced neurological deficits in Drosophila melanogaster
  - pxMJVYgBuupM187WXzsx: Artificial gravity partially protects space-induced neurological deficits in Drosophila melanogaster
- **Útiles / comentario:** Idem B15.

### B25 — NASA OSDR search API — 2026-10-19

- **Cadena:** `insect`
- **Resultados declarados por la base:** 302
- **Primeros títulos:**
  - tfLgy4wBVhd_IT1AXbFa: Drosophila parasitoids go to space: Unexpected and differential effects of spaceflight on hosts and 
  - tvLgy4wBVhd_IT1ApbGk: Drosophila parasitoids go to space: Unexpected and differential effects of spaceflight on hosts and 
  - t_Lky4wBVhd_IT1AtbED: Drosophila parasitoids go to space: Unexpected effects of spaceflight on hosts and their parasitoids
- **Útiles / comentario:** Útiles: OSD-588, -609, -610 (Drosophila y avispas), M3-17.

### B26 — NASA OSDR search API — 2026-10-19

- **Cadena:** `Oryza`
- **Resultados declarados por la base:** 955
- **Primeros títulos:** ninguno
- **Útiles / comentario:** Idem B12.

### B27 — NASA OSDR search API — 2026-10-19

- **Cadena:** `tomato`
- **Resultados declarados por la base:** 389
- **Primeros títulos:**
  - gxtk9okBiXs0LFsRdsg1: Advancing the automation of plant nucleic acid extraction for rapid diagnosis of plant diseases in s
  - hp9r6qABSZJpJSZqz8jI: Biomass Production of the EDEN ISS Space Greenhouse in Antarctica During the 2018 Experiment Phase
  - rh7XrZ4BsOmwGsMnENDw: Stress and light spectral quality influence the transcriptome of a tomato crop on the International 
  - qRMubogBuupM187WyTvM: Characterization of mouse ocular responses (Microscopy) to a 35-day (RR-9) spaceflight mission: Evid
  - M6nHTJ4BBGDNtEQX6kwc: The microbial communities of a tomato crop grown in Veggie under different lighting regimes on the I
- **Útiles / comentario:** Útiles: OSD-767 (tomate, M3-06) y OSD-766/-773 (microbiomas).

### B28 — NASA OSDR search API — 2026-10-19

- **Cadena:** `lettuce`
- **Resultados declarados por la base:** 34
- **Primeros títulos:**
  - RdwFkZIB5gkSzr3qQdmG: Substrate Matters: Ionic Silver Alters Lettuce Growth, Nutrient Uptake, and Root Microbiome in a Hyd
  - gxtk9okBiXs0LFsRdsg1: Advancing the automation of plant nucleic acid extraction for rapid diagnosis of plant diseases in s
  - sN_6g4QB28eYt3lGPLbf: Evaluating the Lettuce Metatranscriptome with MinION Sequencing for Future Spaceflight Food Producti
  - 4H-ByYcBrYApgeM-LpdQ: Persistence of Escherichia coli in the microbiomes of red Romaine lettuce (Lactuca sativa cv. ‘Outre
  - pPSCSJsBC-PjXBJRBjrG: Microbiological and Nutritional Analysis of Lettuce Crops Grown on the International Space Station (
- **Útiles / comentario:** Útiles: OSD-358 (diagnóstico del hongo en plantas de vuelo), OSD-745, OSD-268, OSD-412 (microbiomas de hojas verdes); sin mollicutes.

### B29 — NASA OSDR search API — 2026-10-19

- **Cadena:** `Fusarium`
- **Resultados declarados por la base:** 179
- **Primeros títulos:**
  - D9_6g4QB28eYt3lGL7b9: Draft Genome Sequences of Two Fusarium oxysporum Isolates Cultured from Infected Zinnia hybrida Plan
  - Ed_6g4QB28eYt3lGMLYa: Genomic Characterization and Virulence Potential of Two Fusarium oxysporum Isolates Cultured from th
  - 7d_6g4QB28eYt3lGRrYg: Draft Genomes of Fungi Isolated from the International Space Station during the Microbial Tracking-2
  - CN_6g4QB28eYt3lGS7dW: Fungal Diversity associated with space-craft assembly facility (SAF)
  - Ld_6g4QB28eYt3lGMrZC: Whole genome sequencing and assembly of Eukaryotic microbes isolated from ISS environmental surface,
- **Útiles / comentario:** Útiles: OSD-177 y OSD-264 (genomas de Fusarium de zinnias), OSD-358.

### B30 — NASA OSDR search API — 2026-10-19

- **Cadena:** `plant pathogen`
- **Resultados declarados por la base:** 395
- **Primeros títulos:**
  - gxtk9okBiXs0LFsRdsg1: Advancing the automation of plant nucleic acid extraction for rapid diagnosis of plant diseases in s
  - Ow1_Ap0BpcaSPxPaK9d9: Diagnosing an Opportunistic Fungal Pathogen on Spaceflight-Grown Plants Using the MinION Sequencing 
  - 6t_6g4QB28eYt3lGRbbr: An LaeA- and BrlA-Dependent Cellular Network Governs Tissue-Specific Secondary Metabolism in the Hum
  - 23c0O5AB14LnKNGmPyiw: Spatial characterization of microbial communities on multi-species leafy greens grown simultaneously
  - 1nc4LJAB14LnKNGmNyiF: Spatial characterization of microbial communities on multi-species leafy greens grown simultaneously
- **Útiles / comentario:** Útiles: OSD-358, OSD-594 (extracción de ácidos nucleicos de plantas), microbiomas.

### B31 — NASA OSDR search API — 2026-10-19

- **Cadena:** `RNA interference`
- **Resultados declarados por la base:** 651
- **Primeros títulos:** ninguno
- **Útiles / comentario:** 0 estudios GeneLab con RNAi; los 500 devueltos son de GEO.

### B32 — NASA OSDR search API — 2026-10-19

- **Cadena:** `dsRNA`
- **Resultados declarados por la base:** 197
- **Primeros títulos:** ninguno
- **Útiles / comentario:** 0 estudios GeneLab con dsRNA; los 197 son de GEO, PRIDE y MG-RAST.

### B33 — NASA OSDR search API — 2026-10-19

- **Cadena:** `Spiroplasma`
- **Resultados declarados por la base:** 2
- **Primeros títulos:** ninguno
- **Útiles / comentario:** AUSENCIA. Dos resultados no GeneLab: PRIDE (Spiroplasma melliferum) y GEO GSE112290 (S. poulsonii en cultivo), sin vuelo ni microgravedad.

### B34 — NASA OSDR search API — 2026-10-19

- **Cadena:** `mollicutes`
- **Resultados declarados por la base:** 0
- **Primeros títulos:** ninguno
- **Útiles / comentario:** AUSENCIA. 0 resultados.

### B35 — NASA OSDR search API — 2026-10-19

- **Cadena:** `Acholeplasma`
- **Resultados declarados por la base:** 2
- **Primeros títulos:** ninguno
- **Útiles / comentario:** AUSENCIA para vuelo. Dos resultados de PRIDE (Acholeplasma laidlawii), uno de un experimento de entrecruzamiento CASP; sin vuelo.

### B36 — NASA OSDR search API — 2026-10-19

- **Cadena:** `aphid`
- **Resultados declarados por la base:** 54
- **Primeros títulos:** ninguno
- **Útiles / comentario:** Repetición de B18.

### B37 — NASA OSDR search API — 2026-10-19

- **Cadena:** `planthopper`
- **Resultados declarados por la base:** 9
- **Primeros títulos:** ninguno
- **Útiles / comentario:** 0 estudios GeneLab de delfácidos; 9 resultados de GEO y PRIDE sin vuelo.

### B89 — NASA OSDR search API — 2026-10-19

- **Cadena:** `Drosophila melanogaster spaceflight`
- **Resultados declarados por la base:** 19
- **Primeros títulos:**
  - qBNkVYgBuupM187Wezte: Artificial gravity partially protects space-induced neurological deficits in Drosophila melanogaster
  - it_6g4QB28eYt3lGObYj: Spaceflight and simulated microgravity conditions increase virulence of Serratia marcescens in the D
  - rhPnsIgBuupM187WwDvP: Artificial gravity partially protects space-induced neurological deficits in Drosophila melanogaster
  - pxMJVYgBuupM187WXzsx: Artificial gravity partially protects space-induced neurological deficits in Drosophila melanogaster
  - J9_6g4QB28eYt3lGTrde: Expression data from drosophila melanogaster
- **Útiles / comentario:** Repetición corregida de B14. Quince estudios GeneLab de Drosophila: OSD-1, -3, -36, -70, -96, -207, -278, -347, -514, -588, -592, -595, -596, -609 y -610; todos dípteros o himenópteros.


## Consultas manuales con buscador web (herramienta WebSearch, modo estándar)

### W1 — buscador web — 2026-10-19
- **Cadena:** `dsRNA RNAi plant pathogen OR insect pest validated under simulated microgravity clinostat OR "random positioning machine"`
- **Resultado:** el buscador declaró que ningún resultado combina dsRNA o RNAi contra patógeno o plaga con clinostato o RPM. Salieron revisiones de RNAi en vectores de virus de plantas, ARN de plástido en tomate y M3-11 (Salmonella en lechuga en clinostato).
- **Útil:** M3-11. Respalda A-01.

### W2 — buscador web — 2026-10-19
- **Cadena:** `spray-induced gene silencing spaceflight International Space Station plant disease RNAi crop protection space agriculture`
- **Resultado:** RECHAZADA por el servicio (error de API que remite a la política de uso aceptable, etiqueta `[bio]`). No se reformuló para esquivar el rechazo. Registrada en `preguntas_pendientes.md`. Las otras vías (B03, B57, B59, B60, B81) cubren la misma ausencia.

### W3 — buscador web — 2026-10-19
- **Cadena:** `phytoplasma OR Spiroplasma OR Mycoplasma microgravity OR spaceflight OR clinostat study bacteria without cell wall`
- **Resultado:** el buscador no halló ningún estudio con fitoplasmas, Spiroplasma o Mycoplasma en microgravedad; salieron validaciones de clinostato con *Mycobacterium marinum* y *Escherichia coli* K12 (bacterias con pared) y una revisión de microbios en µg. Solo fragmentos, no abiertos.
- **Útil:** respalda A-02.

### W4 — buscador web — 2026-10-19
- **Cadena:** `hemipteran OR aphid OR planthopper OR leafhopper spaceflight OR microgravity experiment gene expression immunity`
- **Resultado:** ningún estudio de hemípteros; salieron M3-10, M3-16 y Leach 2001 (M3-42).
- **Útil:** respalda A-03.


## Textos completos descargados (Europe PMC `fullTextXML`)

Para los artículos de acceso abierto se bajó el texto completo con la API de Europe PMC y se consultó por resumen y búsqueda dirigida de pasajes (no por lectura lineal). El nivel de lectura de cada fuente está en `sources.json`. Un intento falló: PMC6607005 (revisión de plataformas de plantas, EMBO Rep 2019) devolvió HTTP 500 y no se usó; está en `preguntas_pendientes.md`.

# Fase 2 — Entrega y mecanismo: lo que dicen las fuentes abiertas

Fecha: 2026-10-22. Fase 2 del checkpoint 2. Sólo se citan fuentes abiertas en esta sesión; su estado está en `research/ola2/W1_papers/papers.json` (campo `estado_apertura`). Marcadores según `CLAUDE.md`. Esta fase no midió nada, así que no hay `[M]`.

## Fuentes: contexto y alcance

| Fuente (estado) | Contexto | Qué se midió | Qué no |
|---|---|---|---|
| Rossi *et al.* 2024 (abierta, P6) `[R]` | *Euscelidius variegatus*, *Scaphoideus titanus*; hojas separadas con dsRNA | Silenciamiento de legumaína y natterina (intestinales) y de ATP sintasa β en *E. variegatus*; de ATP sintasa β en *S. titanus*. Remojo de ninfas: sin silenciamiento. Planta entera: dsGFP en 2 de 5 insectos, señal débil | Ubicación del dsRNA dentro del insecto; cifras de planta entera (datos no mostrados) |
| Jones *et al.* 2021, preprint (abierta, P8) `[R]` | *D. maidis*, dieta con dsRNA, 4 días | Reducción de V-ATPase B y D; supervivencia ≈16 % y ≈18 % frente a ≈37 % del control GFP y ≈52 % sin dsRNA | Vía exacta; no revisado por pares |
| Andrada *et al.* 2026 (abierta, P3) `[R]` | *D. maidis*, microinyección | Falla de muda; supervivencia ≈10 % a día 4 para burs-α | Ruta oral; cifra propia de eth (ver PREGUNTAS) |
| Mitter *et al.* 2017 (abierta, P4) `[R]` | Plantas modelo (*Arabidopsis* transgénica, tabaco, caupí) con CMV y PMMoV; spray | dsRNA en LDH detectable en hoja hasta 30 días (northern); captación en células de *Arabidopsis* (reportero GUS); protección a 20 días | Insectos; maíz |
| Gan *et al.* 2010 (resumen, P5) `[R]` | Maíz; SCMV; spray de dsRNA | Protección preventiva; la región CP upstream fue más eficaz que la downstream | MRFV; texto completo |
| Revisión de RNAi en insectos 2024 (abierta, P10) `[R]` | Mecanismo general | Dicer-2 produce siRNA; AGO2 en antiviral (extrapolado de *Drosophila*); afirma que los hemípteros degradan dsRNA en la saliva, con cita propia | Datos de *D. maidis* |
| Hoang *et al.* 2022, revisión (abierta, P9) `[R]` | Captación foliar | Discute transporte a floema y apoplasto | Insectos chupadores |
| Dalaisón-Fuentes *et al.* 2022 (resumen, P11) `[R]` | *D. maidis*; BicC | Reducción de transcripto (hasta 170 veces) y de oviposiciones; alteración de oocitos | Día del efecto, letalidad, texto completo |
| Dalaisón-Fuentes *et al.* 2023 (no abierta, P12) `[?]` | dsRNasas | Sólo se verificó el registro | Contenido: no se cita |

## Respuestas

**(a) Célula y ruta en el insecto.** `[?]` Ninguna fuente abierta identifica la célula blanco. La ruta medida es la ingesta `[R]`. Que el silenciamiento de genes intestinales implique que el dsRNA llega al intestino es una inferencia `[H]`.

**(b) Qué falla primero.** `[R]` En lo medido, el remojo no silenció y la planta entera dejó señal débil. Rossi eligió hojas separadas para aportar más dsRNA, y con ellas hubo silenciamiento. Ningún estudio separa depósito, estabilidad, captación y actividad. `[?]`

**(c) dsRNasas.** `[R]` La revisión atribuye a los hemípteros la degradación de dsRNA en saliva. Cuánto reduce eso la eficacia oral no está cuantificado en fuentes abiertas `[?]`. Dalaisón-Fuentes 2023 aborda dsRNasas según su título; no está abierto y no se usa.

**(d) Comparadores.** `[R]` Rossi: dsGFP. Jones: GFP, buffer y sin dsRNA. Andrada: β-lactamasa. Mitter: Cy3 solo y dsRNA sin LDH. Ningún estudio usa ARN libre, vehículo solo y ARN control en el mismo diseño de hoja.

**(e) Blanco viral en maíz.** `[R]` Gan 2010 muestra protección de maíz contra SCMV con spray, en condiciones de laboratorio. `[?]` Para MRFV no hay en fuentes abiertas revisadas ni spray, ni ensayo en maíz, ni ARN pequeños (ver C10). La célula de maíz que recibe el ARN no se conoce.

## Para la Fase 3 (`[H]`)

`[H]` La entrega oral al insecto tiene la mayor evidencia en *Dalbulus* y en cicadélidos, pero ninguna medición de qué células reciben el ARN. `[H]` La ruta viral depende de un spray en maíz cuya única evidencia abierta es con otro virus y en laboratorio. `[H]` Ambas rutas necesitan como comparadores mínimos ARN libre, vehículo solo y ARN control.

## Qué quedó sin hacer y por qué

1. Dalaisón-Fuentes 2022: sólo resumen, texto no abierto. 2. Dalaisón-Fuentes 2023: no abierta, no se cita. 3. Gan 2010: sólo resumen; el PDF del repo no se revisó. 4. Figura 5A de Andrada: cifra de eth pendiente. 5. Rutas DCL y AGO de la planta: no revisadas en fuentes abiertas específicas.

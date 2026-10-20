# Preguntas pendientes de M2 (ARN y ácidos nucleicos en microgravedad)

Fecha: 2026-10-19. Formato: lo que no se pudo abrir, lo que falló, lo que se rechazó y lo que solo el investigador del EPILAB puede contestar.

## 1. Fuentes que solo se leyeron a nivel de resumen o que no se pudieron abrir

Las fuentes siguientes figuran en `sources.json` con `nivel_lectura: resumen` y están marcadas como tales; ninguna sostiene por sí sola una cifra. Las de acceso cerrado según Europe PMC no se intentaron por otra vía (no se buscaron espejos): Lorenz 2000 (M2-04), Vallazza 2002 (M2-05) y 2004 (M2-06), Rypniewski 2006 (M2-07), los dos trabajos de STMV (M2-08, M2-09), las tres reseñas de cristalización de 2002 (M2-10, M2-11, M2-12), Zhang 2016 sobre OSD-118 (M2-24), Higashitani 2009 (M2-27), Etheridge 2011 (M2-28), Kitto 2021 sobre RNAi en *Arabidopsis* en la ISS (M2-29), los dos trabajos de Wang sobre *C. elegans* en clinostato (M2-31, M2-32), los reanálisis de 2023 y 2024 (M2-35, M2-36), el artículo de miARN en mioblastos de 2026 (M2-38), el de antagomires de 2026 (M2-39), el de aptámeros en EXPOSE-R2 (M2-40), la revisión de virulencia de 2024 (M2-48) y la de ácidos nucleicos de 2022 (M2-45; el texto completo devolvió HTTP 500 en Europe PMC). Las de acceso abierto de las que solo leí el resumen son Montague 2018 (M2-15), la validación de expresión libre de células de 2024 (M2-16) y Higashibata 2016 (M2-37).

No abrí el artículo de PLoS ONE de 2024 sobre un visor de fluorescencia para lectura de ensayos moleculares en el espacio (PMC10942025), que apareció en la búsqueda de WetLab-2 (fila 9 de `busquedas.md`); puede ser relevante para el punto 3.

Pendiente de verificación: el código PDB de la estructura de Vallazza et al. 2002 (la búsqueda por PMID en RCSB devolvió HTTP 400, atributo no buscable); qué corrige exactamente el corrigendum de Ando 2025 (el texto extraído no lo dice y su lista de referencias incluye cuatro trabajos anteriores); el tamaño muestral de animales en las figuras de RNAi de CERISE (no figura en el texto ni en las leyendas que leí); y los controles terrestres del preprint de astronautas (n no hallado).

## 2. Dominios y servicios que fallaron

Europe PMC devolvió HTTP 503 a las consultas con el parámetro `sort=RELEVANCE`; era un error de mi helper y se resolvió quitándolo. RCSB Search API devolvió HTTP 400 al buscar por PMID. El texto completo de PMC11845088 devolvió HTTP 500. No hubo dominios bloqueados por la red ni se pidió acceso a ninguno.

## 3. Rechazos de herramientas y filtros de seguridad

Ninguno.

## 4. Instrucciones embebidas en páginas web o PDF dirigidas a sistemas de IA

No detecté ninguna en los textos que abrí (artículos de Europe PMC, PDF de Research Square, fichas de OSDR y GEO, resúmenes de PubMed). Lo registro como «ninguna detectada», no como garantía de ausencia: la lectura de varios textos fue parcial.

## 5. Archivos de trabajo dejados en la carpeta de salida

La subcarpeta `_work/` contiene volcados de texto de artículos de acceso abierto y la extracción de texto del PDF del preprint de Research Square, que usé para leer. No deben versionarse (CLAUDE.md pide parafrasear y no copiar secciones; D6 deja el material pesado fuera del control de versiones). No pude borrarla: la regla de la sesión prohíbe `rm` en la carpeta concedida y `delete_host_files` exige una aprobación que un subagente no puede obtener. Conviene borrarla o ignorarla antes del commit de R7.

## 6. Pregunta para el investigador del EPILAB

Solo una, porque es la única que cambiaría una decisión y no se puede contestar con bibliografía pública: ¿el interés en la microgravedad viene del organizador o del EPILAB (por ejemplo, un socio con acceso a una plataforma de vuelo), o es una línea exploratoria del equipo? Si viene del organizador, este reporte sugiere dedicarle como mucho una nota de «estado del arte con ausencia documentada»; si es exploratoria, sugiere cerrarla (ver «Veredicto»).

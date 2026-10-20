# Preguntas para el investigador y decisiones de acceso — R7 (microgravedad)

Corte: 2026-10-20. Salen de los `preguntas_pendientes.md` de las pistas M1 a M5 (la de M3 se corrió fuera de esta sesión, ver `REPORT.md`, «Cobertura y firmeza»). Entra solo lo que no se contesta con bibliografía pública y cuya respuesta cambia una decisión. Cada una dice qué cambia.

## Preguntas que cambian la dirección

1. ¿El interés en la microgravedad viene del organizador, de un socio del EPILAB con acceso a una plataforma de vuelo, o es una línea exploratoria del equipo? Si viene del organizador, alcanza con una nota de «estado del arte con ausencia documentada»; si es exploratoria, se cierra. *(M2)*
2. ¿Hay una pregunta estructural concreta sobre una proteína de *S. kunkelii* o de *Ca.* P. zeae (por ejemplo la interfaz de una adhesina con un receptor del vector, o de la PGK con la actina) cuya respuesta cambiaría qué se prioriza? Si no, la línea de estructura queda cerrada. Si sí, el paso que sigue no es microgravedad sino conseguir un cristal o un modelo experimental del complejo en tierra. *(M1, M4)*
3. ¿Hay un laboratorio de cristalografía o de producción de proteínas con el que el EPILAB colabore y que haya expresado proteínas de mollicutes? Sin ese socio no se cumplen las condiciones de purificación, de intento terrestre y de acceso de las reglas de M1 y M4, y no tiene sentido evaluar el costo de un vuelo. *(M1)*
4. ¿Existe en el EPILAB o en un laboratorio colaborador un ensayo de adhesión o internalización de *S. kunkelii* (o de *Ca.* P. zeae) en células o intestino de *D. maidis*, o un cultivo de la cepa de *S. kunkelii*? Es la única verdad de terreno que permitiría validar una predicción de interfaz (PGK, SkARP1, espiralina). *(M4)*
5. ¿El organizador acepta propuestas que no usan RNAi como complemento? Si no, el aporte estructural de M4 queda como anexo de anotación fuera de la pregunta oficial. *(M4; ya abierta en R6)*
6. ¿Les interesa saber si la maquinaria de silenciamiento de la propia planta (AGO, DCL, RDR) cambia de expresión bajo estrés, o solo importa la del insecto? Si es «solo la del insecto», la opción 2 de `M5/opciones.md` se descarta entera. *(M5)*
7. De prioridad baja: ¿el track espera alguna condición de gravedad alterada o de agricultura espacial en la validación? La lectura de M3 es que no (D1, D7) y con ella se cierra sin línea nueva; si la respuesta fuera que sí, habría que revisar los conjuntos de GeneLab sobre Dicer, Argonauta y RDR en plantas en vuelo, que no se hizo. *(M3)*

## Preguntas de datos y de cómputo

1. ¿Hay alguna vía (agencia, colaboración con el grupo japonés del experimento «Auxin Transport») para obtener el maíz de la ISS del BioProject PRJDB11348 como tabla procesada? Si no existe y el repositorio japonés de datos no es accesible, el único cereal reanalizable en vuelo es el arroz de GSE78839. *(M5)*
2. ¿El equipo o el organizador disponen de GPU o de un servicio de plegado autorizado donde subir secuencias públicas de *Ca.* P. zeae? Es lo único que cerraría los modelos faltantes de 480 proteínas; la regla de confidencialidad de `CLAUDE.md` impide hacerlo con secuencias del EPILAB. *(M4)*
3. ¿Conocen alguna secuencia pública de los parasitoides de *D. maidis*? Los dos únicos transcriptomas de parasitoides del OSDR son de *Leptopilina*, parásitos de *Drosophila*. *(M5)*

## Decisión de acceso (para quien orquesta, no para el investigador)

- Autorizar `genelab-repo-prod.s3.amazonaws.com` (almacenamiento de datos del OSDR) y `ddbj.nig.ac.jp` (repositorio japonés) **solo si** se decide ejecutar el chequeo de silenciamiento vegetal en vuelo (M5, opción 2) o el reanálisis del maíz. Si no se piensa ejecutar, no hace falta pedirlos. El resto de lo bloqueado (`www.mdpi.com`, `hwi.buffalo.edu`) solo habría servido para abrir en texto completo revisiones y metaanálisis de cristalización que no sostienen ninguna cifra del veredicto.

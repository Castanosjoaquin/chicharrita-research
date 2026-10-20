# Preguntas pendientes — R7 / M4 (corte 2026-10-19)

## 1. Fuentes que no se pudieron abrir en texto completo

Quedan solo en resumen (acceso cerrado o fuera del subconjunto de acceso abierto de Europe PMC, que devolvió error 500 para el texto completo de Duret 2003 y de Labroussaa 2010): M4-18 a M4-33 y M4-38, entre ellas los trabajos de espiralina (M4-19, M4-20, M4-21), operón de fructosa y PTS (M4-23, M4-24), SkARP1 (M4-22), enzima málica (M4-27, M4-28), MreB5 (M4-26), todos los scFv (M4-29 a M4-32), el aptámero ZY3A (M4-33) y los péptidos Novispirin T7 y Caerin 1.1 (M4-25, sin DOI ni PMID en el registro de Europe PMC). Los valores de CMI de M4-25 no se leyeron. Cuatro fuentes se vieron solo como título (M4-39 a M4-42). Ningún artículo se leyó linealmente: «completo» significa descargado y consultado por pasajes, como en R6.

## 2. Dominios y herramientas

No falló ningún dominio de la lista autorizada; los errores de Europe PMC (503 en cuatro consultas con `sort=RELEVANCE`, 500 en dos descargas de texto completo) y de NCBI (429 por límite de tasa) se resolvieron con reintentos o con el resumen (ver `datos/COMANDOS.md` §3). No se pidió acceso a ningún dominio nuevo. Rfam y cualquier base de ARN regulatorio quedaron sin consultar por no estar en la lista (el ARN regulatorio no se evaluó a esta profundidad). No se instaló ningún paquete: se usaron `requests` en el entorno `python` y `blast` y `biopython` del entorno ya existente `w5bio`.

## 3. Rechazos y contenido sospechoso

Ninguna herramienta devolvió un rechazo de seguridad. Ninguna de las páginas, resúmenes o textos completos recuperados traía instrucciones dirigidas a sistemas de IA.

## 4. Preguntas para el investigador del EPILAB o para el organizador

Solo las que no se contestan con bibliografía pública y cuya respuesta cambiaría una decisión.

1. ¿Existe, en el EPILAB o en un laboratorio colaborador, un ensayo de adhesión o internalización de *S. kunkelii* (o de *Ca.* P. zeae) en células o intestino de *D. maidis*, o un cultivo de la cepa de *S. kunkelii*? Es la única verdad de terreno que permitiría validar una predicción de interfaz proteica (PGK, SkARP1, espiralina; K01–K03). Sin ella, esas filas siguen sin decisión demostrable sin laboratorio; con ella, la línea de interfaz de R6 (Línea 1) pasa de n ≈ 3 a 6 en otra especie a validación en el patosistema.
2. ¿El organizador acepta propuestas que no usan RNAi como complemento (pregunta ya abierta en R6)? Si no, el aporte estructural de M4 no entra en la pregunta oficial del track y queda como anexo de anotación.
3. ¿El equipo o el organizador disponen de GPU o de acceso autorizado a un servicio de plegado donde subir secuencias públicas de *Ca.* P. zeae? Es lo único que cerraría los modelos faltantes de 480 proteínas de M3; la regla de confidencialidad de `CLAUDE.md` impide hacerlo con secuencias del EPILAB, y esta pista no subió ninguna secuencia a ningún servicio.

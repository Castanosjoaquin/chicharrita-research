# C12 · Validación B — marafivirus parientes del MRFV

**Resultado: la función de la poliproteína (replicasa) del MRFV se transfiere a los 11 marafivirus de RefSeq con 47 a 82 % de identidad; la del movimiento (MP) sólo a 2 de 11; y las ventanas de 21 nt compartidas son ≤ 0,66 % del genoma.** Fecha 2026-10-22, BLAST+ 2.17.0 local, NCBI nuccore (consulta 2026-10-22). Sin pre-registro: esta validación se diseñó en la sesión y no tiene umbral de éxito fijado de antemano.

## Datos
MRFV NC_002786.2 (6.366 nt; sólo dos CDS anotadas: poliproteína y «putative movement protein») contra los otros 11 genomas marafivirus de RefSeq: NC_001793, NC_006950, NC_012484, NC_013920, NC_015522, NC_029063, NC_031692, NC_033828, NC_034205, NC_040565, NC_077048 (búsqueda `Marafivirus[Organism] AND complete genome[Title] AND srcdb_refseq[PROP]`).

## Proteína
La poliproteína del MRFV (2.028 aa) tiene homólogo en los 11 virus, con 47,2 a 82,3 % de identidad (el más cercano, el virus del mosaico del pasto *switchgrass*, 82,3 %). Esto es lo que predice la regla de homología, con identidad moderada. La proteína de movimiento (420 aa) sólo encuentra homólogo anotado como movimiento en 2 de 11 (*switchgrass mosaic virus* 51,6 % y *Grapevine Syrah virus-1* 42,8 % con cobertura de 38 %) con e ≤ 1e-5. Los demás virus anotan su MP con otro nombre o no la anotan, o no se parece lo suficiente para detectarla con ese umbral.

## Nucleótido
Ventanas de 21 nt exactas del MRFV presentes en cada pariente (ambas cadenas): entre 0,00 y 0,66 % del genoma, y entre 0,00 y 0,64 % en la región del MP. Confirma lo que ya había medido C10: un virus de otra especie no aporta ventanas de diseño.

## Cómo leerlo
- La homología sirve para **inferir qué hace** un gen viral (aquí, la replicasa), no para **diseñar sobre él**.
- La función del MP del MRFV, el candidato viral mejor rankeado, se apoya en 2 virus y en una anotación que dice «putative» en todos los registros. Es una inferencia débil.
- Como el MRFV ya está anotado, esta validación mide cuánto vale esa anotación, no un mapeo nuevo.

## Límites
Anotación contra anotación: ambas son predicciones. La región del MP (332–1594) está dentro del marco de la poliproteína (127–6213), así que parte de sus ventanas puede coincidir por la poliproteína y no por el MP. No se evaluó identidad por dominio, sólo global. Es una sola familia de virus de ARN.

Tabla: `resultados/ventanas21_MRFV_vs_marafivirus.tsv`.

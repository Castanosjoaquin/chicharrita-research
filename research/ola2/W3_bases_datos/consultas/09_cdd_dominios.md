<!-- Generado por W3 el 2026-10-17. Cada bloque es una consulta realmente ejecutada; la salida es la devuelta por el servidor, recortada donde se indica. -->
# 09 — Conserved Domain Database: ejemplo ejecutado

```
GET esearch.fcgi?db=cdd&term=PIWI[Title]&retmax=5   -> 4 modelos
GET esummary.fcgi?db=cdd&id=<los 5 primeros uid>&retmode=json
```

```
COG1431  PIWI
cl00628  Piwi-like
pfam02171  Piwi
smart00950  Piwi
```

Importa porque son los dominios con los que la ola 1 verificó, sobre UniProtKB e
InterPro, que los mollicutes no tienen maquinaria de RNAi. La base `cdd` permite
rehacer esa verificación por perfil contra las proteínas de los dos genomas de
patógenos que sí podemos bajar —1.775 y 524 secuencias, menos de 0,32 MB entre
las dos—, que era exactamente la limitación declarada de aquella consulta: una
búsqueda de anotación no descarta genes no anotados. No lo hicimos en esta
investigación; queda propuesto, y es barato.

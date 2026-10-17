<!-- Generado por W3 el 2026-10-17. Cada bloque es una consulta realmente ejecutada; la salida es la devuelta por el servidor, recortada donde se indica. -->
# 00 — Registro de las 409 peticiones HTTP ejecutadas

Tabla completa en `registro_consultas.csv`: etiqueta, URL, código HTTP, bytes de
respuesta, segundos y marca de tiempo UTC. Resumen por código:

```
status
200    400
404      5
429      2
400      2
```

Las diez primeras, como muestra del formato:

```
                       ts  status   bytes                  tag
2026-10-17T16:40:17+00:00     200   462.0 einfo lista de bases
2026-10-17T16:40:27+00:00     200 11209.0           einfo gene
2026-10-17T16:40:28+00:00     200 11700.0        einfo nuccore
2026-10-17T16:40:29+00:00     200 11562.0        einfo protein
2026-10-17T16:40:30+00:00     200 11467.0       einfo assembly
2026-10-17T16:40:30+00:00     200  5075.0            einfo sra
2026-10-17T16:40:31+00:00     200  8672.0     einfo bioproject
2026-10-17T16:40:32+00:00     200  3999.0      einfo biosample
2026-10-17T16:40:33+00:00     200  7157.0       einfo taxonomy
2026-10-17T16:40:34+00:00     200  7005.0            einfo gds
```

Las dos respuestas 429 son del límite de tres peticiones por segundo de
E-utilities sin clave de API; las dos se reintentaron con espera creciente y
devolvieron 200. Las respuestas 404 y 400 son rutas y endpoints que probamos y
no existen: tres rutas FTP equivocadas para los TSA, la página
`datasets/docs/v2/policies/` y los endpoints `kegg/list/organism` y
`kegg/conv/ncbi-geneid/mbp`. Están en el registro a propósito.

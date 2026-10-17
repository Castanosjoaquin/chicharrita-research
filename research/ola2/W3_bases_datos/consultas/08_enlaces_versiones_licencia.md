<!-- Generado por W3 el 2026-10-17. Cada bloque es una consulta realmente ejecutada; la salida es la devuelta por el servidor, recortada donde se indica. -->
# 08 — Estado de los enlaces, versiones y condiciones de uso

## Verificación de los enlaces, hecha hoy

| URL | HTTP | bytes del cuerpo |
| --- | ---: | ---: |
| `https://www.ncbi.nlm.nih.gov/` | 200 | 39223 |
| `https://www.ncbi.nlm.nih.gov/datasets/genome/` | 200 | 26954 |
| `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi?retmode=json` | 200 | 462 |
| `https://api.ncbi.nlm.nih.gov/datasets/v2alpha/version` | 200 | 51 |
| `https://ftp.ncbi.nlm.nih.gov/genomes/` | 200 | 1915 |
| `https://www.ncbi.nlm.nih.gov/datasets/docs/v2/policies/` | 404 | 135070 |

Los dos enlaces del `.docx` que le tocan a W3 responden 200. El de `datasets/genome/` devuelve 26.954 bytes de HTML que, una vez quitadas las etiquetas, dejan 892 caracteres de texto: todo encabezado y pie del NCBI, ningún dato de genomas. La página es una aplicación de cliente; el contenido lo trae después por su propia API.

La URL `https://www.ncbi.nlm.nih.gov/datasets/docs/v2/policies/`, que probamos buscando la política de uso de Datasets, devuelve **404**. No está en el `.docx`: la probamos nosotros y la anotamos como rota.

## Condiciones de uso, citadas desde la página que se abrió

`https://www.ncbi.nlm.nih.gov/genbank/`, sección *GenBank Data Usage*, parafraseada: el NCBI no impone restricciones al uso ni a la redistribución de los datos de GenBank, pero advierte que algunos autores de los depósitos pueden reclamar patente, derecho de autor u otros derechos sobre lo que depositaron, que el NCBI no está en posición de evaluar esos reclamos y que la responsabilidad de respetarlos es de quien usa el dato. Textual, la frase que importa: «NCBI places no restrictions on the use or distribution of the GenBank data».

`https://www.ncbi.nlm.nih.gov/home/about/policies/`, sección *Copyright Status of Webpages*: la información creada por o para el gobierno de los Estados Unidos en ese sitio es de dominio público y puede distribuirse y copiarse libremente, con el pedido de que se cite a la NLM como fuente; y es responsabilidad del usuario revisar las restricciones de copyright del material enlazado desde allí.

## Límites de uso de las API

E-utilities, según la guía oficial del NCBI (*A General Introduction to the E-utilities*, NBK25497): tres peticiones por segundo sin clave de API y diez con clave; se pide identificar la herramienta y un correo de contacto en los parámetros `tool` y `email`, y correr los trabajos grandes fuera del horario pico de los Estados Unidos. Nuestras corridas fueron sin clave y con una espera de 0,34 a 0,5 s entre peticiones; aun así el servidor devolvió dos veces HTTP 429 sobre un total de 409 peticiones registradas, y las dos se resolvieron con reintento y espera creciente. Está en `registro_consultas.csv`, que cierra con 400 respuestas 200, 5 respuestas 404, 2 respuestas 429, 2 respuestas 400.

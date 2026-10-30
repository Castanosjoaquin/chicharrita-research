# Póster A0 del Investigathon

Primer boceto. El PDF de impresión es `poster_A0.pdf`: A0 vertical (841 × 1189 mm), una página, tipografías en curvas, imágenes a 150 dpi y 1,5 MB.

Se regenera con tres pasos (hace falta `playwright` con Chromium, `pypdf`, `Pillow`, `segno` y `pdftocairo` de poppler):

```bash
python preparar_assets.py          # encabezado y pie planos a 150 dpi
python construir.py                # poster.html con las figuras en SVG
python exportar.py <carpeta_de_trabajo> poster_A0.pdf
```

`render.py <carpeta> [escala]` deja una vista previa PNG y dice cuántos milímetros sobran antes del pie.

Sin `playwright` en la máquina, el mismo chequeo sale de Chrome en modo headless, que es con lo que se verificó `D103`:

```bash
chrome --headless=new --window-size=3178,4493 --force-device-scale-factor=0.6 \
       --virtual-time-budget=12000 --screenshot=v.png poster.html   # 3178 px = 841 mm a 96 dpi
```

**Para mirarlo en PDF** —el HTML a 841 mm no se ve bien en pantalla— el mismo Chrome lo imprime, respetando el `@page` de 841 × 1189 mm en una sola página:

```bash
chrome --headless=new --no-pdf-header-footer --virtual-time-budget=15000 \
       --print-to-pdf=poster_vista.pdf poster.html
```

Eso es `poster_vista.pdf`, **para ver, no para imprimir**: lleva las fuentes incrustadas y no en curvas, así que no cumple lo que pide la organización. Chrome no puede escribir dentro del repo, así que conviene sacarlo a una carpeta temporal y copiarlo.

**El `poster_A0.pdf` de este directorio es más viejo que `poster.html`** (`D103`): el de impresión sale sólo de `exportar.py`, en una máquina con `playwright` y el `pdftocairo` de poppler, que son los que pasan las fuentes a curvas.

Los dos QR del pie se regeneran con `python generar_qr.py`, que tiene las URL adentro y escribe `assets/qr_repo.svg` y `assets/qr_informe.svg`. **Las dos apuntan a un repositorio que todavía es privado**, así que no resuelven hasta que el dueño lo haga público (`D106`, y el punto 105 de `00_meta/PREGUNTAS_ABIERTAS.md`). Antes de mandar a imprenta, verificar las dos:

```bash
curl -s -o /dev/null -w "%{http_code}\n" <url>   # 200 = sirve, 404 = todavía no
```

Cada cifra sale de los entregables que cita su panel; ninguna secuencia de EPILAB entra al póster.

## Versión actual (D105)

`poster_vista_v2.pdf` es el póster rehecho como una historia en ocho pasos (títulos y textos más simples, benchmark en el panel 6). La frase y la miniatura de *Rpn6* que tuvo el panel 5 ya no están (`D105`, sexta enmienda). Todo sale de `construir.py`: los textos están en el HTML dentro de la función `construir()`, y cada figura es una función `figN()` con sus cifras y la ruta de donde salen. Para modificarlo:

```bash
python construir.py          # reescribe poster.html
chrome-headless-shell --no-sandbox --no-pdf-header-footer --virtual-time-budget=20000 \
       --print-to-pdf=poster_vista_v2.pdf poster.html
```

El contenido tiene que terminar antes de que empiece el pie (1.107 mm desde arriba): si agregás texto, bajá la letra del cuerpo (`font-size` de `body` en el CSS) o sacá algo. Hoy termina en **1.091,1 mm**, con 15,9 mm de aire `[M]` (medido sobre el PNG con Pillow, no con `render.py`, que necesita `playwright`). `poster_vista.pdf` es la versión anterior, y `poster_A0.pdf` sigue siendo el de impresión viejo.

### Lo que le falta a `poster_vista_v2.pdf` para ser el archivo de imprenta

Sale de Chrome, así que es **para ver, no para imprimir**, por lo mismo que `poster_vista.pdf`: las tipografías van incrustadas y no en curvas. El A0 de impresión sigue saliendo sólo de `exportar.py`, con `playwright` y el `pdftocairo` de poppler. Lo que sí está bien: una página de 841,0 × 1.188,9 mm, y todo el texto y todas las figuras en vectores. Las dos únicas imágenes rasterizadas son las bandas de la cabecera (4967 × 992 px) y del pie (4967 × 484 px), que al ancho final dan **150 dpi** `[M]`.

Dos detalles menores del PDF de Chrome: los glifos `ρ` y `≥` no están en los subsets de Montserrat ni de IBM Plex Mono, así que caen en la tipografía del sistema (en esta máquina, Arial y Consolas; en otra, Helvetica Neue y Menlo). Son tres apariciones en todo el póster.

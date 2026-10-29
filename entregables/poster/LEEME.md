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

Para completar a mano en `construir.py`: el contacto y el enlace del informe (el QR del informe hoy codifica el texto «INFORME PENDIENTE»; se regenera con `segno` en `assets/qr_informe.svg`). Cada cifra sale de los entregables que cita su panel; ninguna secuencia de EPILAB entra al póster.

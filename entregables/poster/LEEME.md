# Póster A0 del Investigathon

Primer boceto. El PDF de impresión es `poster_A0.pdf`: A0 vertical (841 × 1189 mm), una página, tipografías en curvas, imágenes a 150 dpi y 1,5 MB.

Se regenera con tres pasos (hace falta `playwright` con Chromium, `pypdf`, `Pillow`, `segno` y `pdftocairo` de poppler):

```bash
python preparar_assets.py          # encabezado y pie planos a 150 dpi
python construir.py                # poster.html con las figuras en SVG
python exportar.py <carpeta_de_trabajo> poster_A0.pdf
```

`render.py <carpeta> [escala]` deja una vista previa PNG y dice cuántos milímetros sobran antes del pie.

Para completar a mano en `construir.py`: el contacto y el enlace del informe (el QR del informe hoy codifica el texto «INFORME PENDIENTE»; se regenera con `segno` en `assets/qr_informe.svg`). Cada cifra sale de los entregables que cita su panel; ninguna secuencia de EPILAB entra al póster.

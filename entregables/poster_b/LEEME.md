# Póster A0 del Investigathon — **versión B** (para comparar con `entregables/poster/`)

Esta carpeta es una copia de `entregables/poster/` con cambios. **La versión original no se
tocó**: sigue en `entregables/poster/` con su `poster_A0.pdf`.

PDF de impresión: `poster_B_A0.pdf` — A0 vertical (841 × 1189 mm), una página, 0,88 MB.
Vista previa: `previa.png`.

## Qué cambia respecto de la versión A

1. **Panel 09 nuevo, el benchmark de las tres herramientas** (figura 11), que en la versión A
   no estaba: era el pedido 2 del checkpoint 1. Cifras de
   `research/ola2/W7_ranking/benchmark_tres_herramientas.md` §3.
2. **El panel 04 pasa a ser el ranking**: dice el orden y en qué fracción de los 2.000 juegos de
   pesos aguanta (`research/ola3/C7_ranking_v2/REPORT.md`, `entregables/para-el-investigador.md`),
   además del conteo contra densidad que ya mostraba.
3. **Menos texto en los nueve paneles**: la prosa baja de 843 a 736 palabras *incluyendo* el panel
   nuevo; sin él, los ocho paneles de la versión A bajan de 843 a unas 620.
4. **Ningún rótulo de figura por debajo de 18,3 pt impresos** (en la versión A el mínimo es
   14,5 pt y hay 178 palabras por debajo de 18 pt). El piso está en `PISO_TEXTO` y la escala en
   `ESCALA_TEXTO`; la letra chica del CSS sube de 13,5 a 16 pt como mínimo.
5. **Reacomodo de la grilla**: la recomendación (panel 05) pasa a ancho completo y los paneles 06,
   07 y 08 van juntos en la última fila. Cabecera de 168 a 134 mm y pie de 82 a 70 mm.
6. **Se cae la figura 8** (el escalón de exposición del panel 06), porque la tabla del mismo panel
   dice lo mismo, y **el cuarto bloque de la figura 9** (el caso `BicC_Dm` + V-ATPasa B). La
   función `fig8()` queda definida pero sin usar.

Las quimeras (panel 07) se mantienen, por pedido del usuario.

## Cómo se regenera

```bash
python construir.py                                   # escribe poster.html
python exportar_cdp.py poster.html poster_B_A0.pdf    # PDF A0 de una página
python ../../../render_cmp.py poster.html previa.png 0.45   # vista previa y chequeo de desborde
```

`exportar_cdp.py` reemplaza a `exportar.py` en este entorno: el Chromium disponible corre con
`--single-process` y el `IO.read` de Playwright falla, así que el PDF se pide por CDP
(`Page.printToPDF` con `transferMode: ReturnAsBase64`). **Las tipografías quedan incrustadas, no
pasadas a curvas**, porque falta `pdftocairo` (poppler); para la versión de imprenta hay que
correr `exportar.py` en una máquina con poppler.

## Lo que sigue pendiente, igual que en la versión A

- El bloque de contacto dice `[completar]`.
- El QR del informe codifica el texto «INFORME PENDIENTE», no una URL.
- Falta confirmar la medida que pide la organización: esto es A0 (841 × 1189 mm) y la guía
  menciona 120 × 90 cm como lo habitual.

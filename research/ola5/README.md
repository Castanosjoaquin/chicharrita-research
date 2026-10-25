# Ola 5 — lo que sale de la carta del 25 de octubre

Siete líneas con medición propia, `N1` a `N5`, `N9` y `N10`, para contestar la respuesta del investigador
del **2026-10-25**, que resolvió la discrepancia de los cuatro conteos y abrió cuatro cosas nuevas.
El plan que ordena las líneas, con la trazabilidad punto por punto de lo que pide la carta, es
[`docs/plan_ola5/PLAN_OLA5.md`](../../docs/plan_ola5/PLAN_OLA5.md). La reunión era el lunes 26.

Lo que se le muestra en la reunión está en
[`entregables/reunion-lunes.html`](../../entregables/reunion-lunes.html), y la recomendación
defendida en [`entregables/recomendacion-defendida.md`](../../entregables/recomendacion-defendida.md).

| Carpeta | Qué contesta | Estado |
| --- | --- | --- |
| [`N1_regla_de_conteo/`](N1_regla_de_conteo/REPORT.md) | La función histórica de conteo, implementada y **reproducida con insumos propios**: 138, 40, 218 y 35 pasan a **114, 35, 199 y 33**, los cuatro valores de la planilla, exactos. El ancho de cobertura queda identificado en 20, porque 19 y 21 no dan los cuatro. Y el sesgo **no es constante**: va del 5,7 % al 17,4 % según el gen. | completa; 17 verificaciones en verde |
| [`N2_ancho_de_cobertura/`](N2_ancho_de_cobertura/REPORT.md) | Si nuestra curva estaba mal por usar 21. **No**: son dos curvas distintas. Con 21 se reproducen las tres marcas leídas de la pantalla del original —meseta de 9 en 150-156, de 8 en 287-297, línea azul plana en 21—; con 20 las tres caen un nucleótido antes. Lo que sí era un defecto es que el test no distinguía las dos convenciones. | completa; el test pasa de 87 a 93 verificaciones |
| [`N3_marcos/`](N3_marcos/REPORT.md) | Los tres marcos de conteo con nombre, medidos en las seis regiones vigentes y rivales, y la partición que pedía el punto 5: para 922-1221, de 36 a 29 son siete ventanas de **límite físico** y de 29 a 26 son tres de **contexto de accesibilidad**; del modelo de eficiencia no sale ninguna. El recorte **sube** el conteo en tres regiones y lo baja en tres. Cruzado con la grilla, el marco intermedio deja la comparación contra C7 en **41,1 %** con margen mediano cero. Y las veinte ventanas que cambian de marco en las tres regiones nuevas cruzan **todas** por accesibilidad, ninguna en las dos primeras posiciones. Sobre la secuencia de `GITV01` el orden no se mueve y el margen se abre, pero tres bases mueven **ocho** ventanas en el marco intermedio contra tres en la molécula. | completa; reproduce las seis anclas publicadas, las cuatro fracciones de M7, las tres anclas del comparador y los tres conteos de M7 §4 con otro alineador |
| [`N4_quimeras/`](N4_quimeras/REPORT.md) | Las dos preguntas de las junturas, separadas como pidió. De las 240 ventanas de juntura de las doce quimeras, **4 son eficientes y ninguna de esas 4 tiene blanco continuo**; 8 sí tienen blanco y son todas de los extremos de la unión, ninguna eficiente. Una quimera **canjea** los veinte arranques de cola de cada fragmento por veinte de juntura. | completa; reproduce el ancla de C13 quimera por quimera |
| [`N5_ficha_grilla/`](N5_ficha_grilla/REPORT.md) | La ficha de las 4.368 configuraciones —los cinco ejes con rango y paso, y lo que queda fijo— y la identidad de C7, que es `BicC_Dm` 2121-2420. Con la autocorrección de D25 encima. | completa; sin cómputo nuevo |
| [`N9_paquete_port/`](N9_paquete_port/REPORT.md) | El paquete que se le puede mostrar: 36 archivos, cuatro con nucleótidos y los cuatro con fuente pública escrita, cero hallazgos sin exceptuar. | completa; falta decidir cómo se entrega |
| [`N10_conteo_historico_por_region/`](N10_conteo_historico_por_region/REPORT.md) | La función histórica aplicada a **regiones** y no a genes. El sesgo por región va de **0 % a 22,2 %**, y en el marco de contexto el «36 contra 35» sobre la región de C7 **se vuelve un empate, 33 a 33**. Las dos formas de aplicar la regla a una región dan lo mismo en las seis. | completa; reproduce las anclas de N3 |

## Lo que hay que leer antes de usar estos números

- **La hipótesis del conteo por aciertos de Bowtie se retiró como causa.** Sigue siendo un hallazgo
  cierto sobre la herramienta original y no explica los cuatro conteos de la planilla. El
  «200 contra 199» de `BicC_Dm` era coincidencia, y el mecanismo verdadero da 199 clavado. Ver D62
  y `00_meta/CAMINOS_PROBADOS.md`.
- **Cada conteo viaja con su marco.** Es D63 y sale de que el recorte mueve los conteos en
  direcciones distintas según la región. Un conteo sin marco declarado no se puede comparar con
  otro, igual que uno sin configuración.
- **El «32 contra 22» de D25 no es sostenible.** La razón escrita de esa decisión se reemplazó por
  la cobertura declarada por fuente (D64); la decisión no se revirtió. Una fuente que no cubre una
  región se declara **sin datos**, no como cero.
- **Dos cifras de la planilla no son comparables entre sí.** El sesgo de la función histórica de
  conteo depende de cuán agrupadas están las ventanas eficientes, no del largo ni de la calidad del
  diseño. Es el quinto límite de `M8`, y aplicado a regiones va de 0 % a 22,2 % (`N10`).
- **El argumento de conteo contra `2121-2420` no existe.** Tres mediciones independientes apuntan
  al mismo lado: el margen de una ventana no sobrevive a la grilla de parámetros (36,4 % en
  contexto, 41,1 % en el marco intermedio), no sobrevive al cambio de marco, y no sobrevive al
  contador histórico, que lo vuelve un empate. Lo que sostiene a 922-1221 frente a C7 es el perfil
  de off-target y la conservación por fuente. Contra `264-563`, en cambio, la ventaja aguanta todo:
  entre el 99,1 % y el 99,9 % en los tres marcos.

## Lo que quedó sin hacer, y por qué

- **El marco intermedio en tres de las cuatro fuentes del eje de referencia.** Se corrió con
  `GITV01`, que es la única cuya base está en esta máquina; las otras tres quedan **no corridas con
  su motivo** —no hay `blastn` ni `makeblastdb` acá y `work/W5/db/` no está en el árbol— en `N3`
  §7. Con `blastn` en el PATH, el camino corto es agregarle el marco intermedio a
  `eje_referencia.py` de `M7` `[?]`.
- **El apareamiento parcial de las ventanas de juntura.** Medimos la coincidencia exacta de 21 nt;
  si una complementariedad incompleta les da alguna actividad, esas ventanas no serían inútiles
  sino menos útiles, y no lo sabemos `[?]`.

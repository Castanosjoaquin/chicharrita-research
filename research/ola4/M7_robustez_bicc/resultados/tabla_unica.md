## Tabla unica — en que fraccion de las configuraciones gana 922-1221

Fuente: `resultados/fracciones_parametros.json`. Cada celda dice sobre cuantas configuraciones se calculo. «Contexto» cuenta las ventanas que arrancan en la region dentro del gen de 2.520 nt; «recorte» es la molecula de 300 nt plegada sola, que es la que se sintetizaria.

| Corte de la grilla | Config. | vs 2121-2420 (contexto) | vs 2121-2420 (recorte) | vs 264-563 (contexto) | vs 264-563 (recorte) | a las dos a la vez (recorte) |
|---|---|---|---|---|---|---|
| **en conjunto** | 4368 | 36,4 % | 75,6 % | 99,1 % | 99,6 % | 75,5 % |
| modo `fiel` | 2184 | 57,1 % | 87,6 % | 100,0 % | 100,0 % | 87,6 % |
| modo `corregido` | 2184 | 15,7 % | 63,6 % | 98,2 % | 99,1 % | 63,4 % |
| tabla `RNA_NN3` | 2184 | 36,4 % | 76,8 % | 99,2 % | 99,7 % | 76,7 % |
| tabla `RNA_NN4` | 2184 | 36,3 % | 74,4 % | 99,0 % | 99,5 % | 74,3 % |
| ViennaRNA 2.7.2 | 2184 | 39,6 % | 88,8 % | 98,8 % | 99,1 % | 88,7 % |
| RNAplfold 2.1.5 | 2184 | 33,2 % | 62,3 % | 99,5 % | 100,0 % | 62,3 % |
| brecha 1,0, toda la accesibilidad | 208 | 36,1 % | 74,5 % | 100,0 % | 100,0 % | 74,5 % |
| accesibilidad 0,1, toda la brecha | 168 | 66,1 % | 93,5 % | 100,0 % | 100,0 % | 93,5 % |
| punto por defecto (8 celdas) | 8 | 75,0 % | 100,0 % | 100,0 % | 100,0 % | 100,0 % |
| recorte sin sus dos primeras posiciones | 4368 | — | 74,2 % | — | 99,6 % | 74,2 % |

Margen de la diferencia, en conjunto (ventanas eficientes de 922-1221 menos las de la rival, mediana y extremos sobre las 4368 configuraciones):

| Marco | vs 2121-2420 | vs 264-563 |
|---|---|---|
| contexto | -1,5 (de -10 a +14) | +10,0 (de -1 a +28) |
| recorte | +3,0 (de -6 a +19) | +12,0 (de -5 a +26) |

## Eje de referencia — eficiencia recalculada y coincidencias

Fuente: `resultados/referencia_resumen.json`. ViennaRNA 2.7.2, tabla NN3, punto por defecto (brecha 1,0, accesibilidad 0,1, u = 8, 22 C). «Recalculada» es el conteo de la molecula recortada **tal como la escribe esa fuente**; «idénticas» cuenta, de las ventanas eficientes de la secuencia de EPILAB en contexto, cuantas existen identicas en esa fuente.

| Fuente | Region | Cobertura de la region | Eficientes recalculadas (corregido) | Eficientes (EPILAB, contexto) | Identicas | Variantes | Cruzan empalme | Sin datos |
|---|---|---|---|---|---|---|---|---|
| GHCC01 (Argentina, Pergamino) | 922-1221 | completa | 26 | 36 | 36 | 0 | 0 | 0 |
| GHCC01 (Argentina, Pergamino) | 2121-2420 | completa | 22 | 35 | 35 | 0 | 0 | 0 |
| GHCC01 (Argentina, Pergamino) | 264-563 | completa | 17 | 20 | 20 | 0 | 0 | 0 |
| GITV01 (Ohio State) | 922-1221 | completa | 25 | 36 | 32 | 4 | 0 | 0 |
| GITV01 (Ohio State) | 2121-2420 | completa | 19 | 35 | 33 | 2 | 0 | 0 |
| GITV01 (Ohio State) | 264-563 | completa | 17 | 20 | 20 | 0 | 0 | 0 |
| GCWP01 (Illinois) | 922-1221 | parcial | no corrida | 36 | 0 | 0 | 0 | 36 |
| GCWP01 (Illinois) | 2121-2420 | completa | 18 | 35 | 22 | 13 | 0 | 0 |
| GCWP01 (Illinois) | 264-563 | parcial | no corrida | 20 | 5 | 0 | 0 | 15 |
| genoma UK GCA_975739785.1 | 922-1221 | completa | 26 | 36 | 36 | 0 | 0 | 0 |
| genoma UK GCA_975739785.1 | 2121-2420 | completa | 22 | 35 | 27 | 0 | 8 | 0 |
| genoma UK GCA_975739785.1 | 264-563 | parcial | no corrida | 20 | 12 | 0 | 8 | 0 |

Conteos de la molecula recortada de EPILAB, para comparar: 922-1221 = 26 (corregido), 36 (fiel); 2121-2420 = 22 (corregido), 29 (fiel); 264-563 = 17 (corregido), 22 (fiel).

## Eje de criterios de riesgo — sensibilidad, no adopcion

Fuente: `resultados/riesgo_sensibilidad.json`. **No elige regla**: mide cuanto cambia la comparacion segun cual se elija, que es lo que M6 (#10) tiene que decidir. Panel de C7 v2 (A_mellifera, F_candida, H_axyridis, H_vitripennis, humano, maiz), sin los pesos de D18. «Limpias y eficientes» es eficiente y sin coincidencia, y **no depende de la regla**: una ventana eficiente con coincidencia es riesgosa para las dos. Lo que la regla cambia es el tamano del riesgo declarado.

| Umbral (D28) | Marco | Config. | 922-1221 gana a 2121-2420 | gana a 264-563 | Alertas, regla conservadora (922 / 2121 / 264) | Alertas, regla mecanicista |
|---|---|---|---|---|---|---|
| `perfecto_21` | contexto | 4368 | 36,4 % | 99,1 % | 0 / 0 / 22 | 0 / 0 / 0 |
| `perfecto_ge19` | contexto | 4368 | 35,3 % | 99,1 % | 3 / 6 / 33 | 0 / 0 / 0 |
| `perfecto_21` | recorte | 4368 | 75,6 % | 99,6 % | 0 / 0 / 22 | 0 / 0 / 0 |
| `perfecto_ge19` | recorte | 4368 | 75,9 % | 99,6 % | 3 / 6 / 33 | 0 / 0 / 0 |

Las columnas de alertas estan medidas en ViennaRNA 2.7.2, tabla NN3, modo `corregido` y punto por defecto. El conteo de la regla conservadora no depende de la configuracion —es coincidencia exacta de secuencia—; el de la mecanicista si, y sobre las ocho celdas del punto por defecto su rango es 922-1221 [0, 1]; 2121-2420 [0, 0]; 264-563 [0, 0].

Ventanas del gen con coincidencia en el panel: 43 con `perfecto_21` y 85 con `perfecto_ge19`.

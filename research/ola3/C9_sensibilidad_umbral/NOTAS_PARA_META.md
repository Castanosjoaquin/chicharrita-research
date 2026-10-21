# Notas para la memoria del proyecto — C9 (2026-10-21)

Aportes para que el orquestador integre a `00_meta/`. No se editó `00_meta/`.

## Decisiones candidatas

**D-C9-1.** La recomendación se presenta a dos niveles: el *candidato* es robusto a los umbrales de si-Fi21 sin fuente primaria (`MP_MRFV` primero en 98,2–99,1 % de la grilla, backend `vienna`), y la *región de 200 nt* no lo es (coincidencia exacta con la de defecto en 11,7 % fiel y 25,8 % corregido). Consecuencia: se entrega una región candidata, no un sitio. Alternativa descartada: afirmar «el umbral no cambia la recomendación», que es falsa a nivel de ventana.

**D-C9-2.** El pre-registro vive en `research/ola3/C9_sensibilidad_umbral/` y no en `entregables/`, porque es un documento de método que debe quedar fijado antes de cualquier resultado, y no un entregable al investigador. Si el equipo prefiere moverlo a `entregables/`, hacerlo con `git mv` para conservar la fecha de escritura.

**D-C9-3.** Panel de referencias: no se usó. El barrido varía umbrales de eficiencia, que no dependen del panel; por eso no hizo falta bajar GRCh38.

## Caminos probados

La grilla se evaluó con `apply_rules` ventana por ventana sobre primitivas calculadas una vez por gen (`primitives`), sin volver a llamar a RNAplfold: 4.368 filas en menos de dos segundos. Anclaje: el punto por defecto reproduce los ocho conteos y regiones del CLI `run_sifi.py` con el mismo backend.

## Hallazgos que hay que registrar

1. `W7_ranking/index.html` es HTML escrito a mano: no tiene generador y su texto de A.3/B.3 no está en `W7_ranking/REPORT.md`. La corrección se hizo en los dos archivos a mano. Pendiente de decisión: si se quiere que el markdown sea fuente de verdad también para W7, hay que escribir un generador.
2. `C7_ranking_v2/REPORT.md` e `index.html` **se generan** desde `scripts/generar_informes.py`; una edición a mano se pierde en la próxima corrida. La nota de corrección se puso en el generador. Además, el conversor `inline_html` no soportaba `~~tachado~~` y se le agregó (una línea); el diff contra HEAD de C7 es solo la nota y esa línea.
3. El «Rehacerlo con lo que la ola 3 midió después» de la fila 3 del plan estaba desactualizado (C7 ya lo hizo); se tachó.
4. Los números de la corrección de B.3 (98,7 % → 33,7 %, 65,9 %, w* = 0,32, factores 2,38–2,50 y 1,015–1,064, piso 0,8533) **se citan de la auditoría ya registrada en `PREGUNTAS_ABIERTAS.md` y no se volvieron a medir** aquí.

## Preguntas nuevas para el investigador

1. ¿Qué mide exactamente la columna `hr` de la Tabla S1 de Cedden 2025 y en qué dirección? Hay que abrir el artículo antes de correr la validación. `[?]`
2. ¿Hay forma pública de recuperar las secuencias de los 28 ARNdc? Sin ellas el puntaje de si-Fi21 no se puede calcular y el análisis primario cae a la columna `access`. `[?]`
3. ¿Cuántas ventanas de diferencia justifican hablar de «orden» entre dos candidatos? El par `ATPaseD_Dm`/`CP_MRFV` difiere en 2–3 de 200.

## Bloqueos y límites

RNAplfold 2.1.5 no está disponible: todos los conteos usan ViennaRNA 2.7.2 y no son comparables con los de la ola 2. No se calcularon los dos ejes del ranking sobre la grilla (la limpieza) ni se incluyeron `eth` y `burs-alpha`; se barrió solo la eficacia de región de los cuatro genes de EPILAB. La grilla fija `u = 8`, ventana de 21 nt y región de 200 nt. Ningún filtro de seguridad rechazó consultas en esta sesión.

## Conflicto de instrucciones sobre commits

El prompt de C9 pide un commit por tarea; la regla general de ola 3 dice «no hagas commits (D5)». Se siguió la instrucción específica del prompt y se avisa aquí.

## Incidente de confidencialidad detectado antes del push (2026-10-21)

Los TSV del ancla se commitearon con la columna `seq` que escribe `run_sifi.py`: un 21-mero por ventana, solapados de a 1 nt, de modo que el gen completo se reconstruye por concatenación. Dos de los cuatro genes son de EPILAB y el remoto es público. Se detectó revisando el diff **antes** de pushear, los tres commits locales se reescribieron con los archivos ya limpios, y la columna se quita ahora con `scripts/limpiar_ancla.py`, que además verifica que no quede ninguna racha de 21 nt o más en `resultados/`.

**Regla general que conviene subir a `00_meta/`:** cualquier salida por ventana de si-Fi21 que se versione tiene que pasar por un chequeo de rachas de 21 nt o más, porque el formato TSV del port incluye la secuencia por defecto. Es el mismo riesgo para `informe_html.py` y para cualquier TSV de `work/` que se mueva a `research/`.

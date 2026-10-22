# Fase 4 — Checklist de la guía del checkpoint 2

Fecha: 2026-10-22. Página evaluada: `entregables/checkpoint2-una-pagina.md` (y su `.html`), 661 palabras. Protagonista elegido por el usuario: la separación de rankings por mecanismo (D38). Categoría declarada: Bioinformática accesible. Guía: `Guia_Checkpoint2_Estudiantes.pdf`, raíz del repo.

## Las siete casillas

| # | Elemento de la guía | Estado | Dónde se sostiene |
|---|---|---|---|
| 1 | La pregunta | ✓ | `salidas/F3_hipotesis_alternativas_validacion.md` §1 |
| 2 | La hipótesis, con mecanismo, resultado predicho y condición de refutación | ✓ | `salidas/F3_hipotesis_alternativas_validacion.md` §2 |
| 3 | La evidencia, con procedencia e identificadores | ✓ con límite (ver abajo) | `research/ola2/W5_secuencias_epilab/secuencias.json` (largos, accesiones, posiciones); `research/ola3/C7_ranking_v2/REPORT.md` §3 (`eth` y `burs-α`); `research/ola2/W1_papers/papers.json` (DOI) |
| 4 | Un avance propio (un protagonista) | ✓ | `salidas/F1_decision_ranking.md` §2 y §3; `research/ola3/C7_ranking_v2/resultados/ranking_v2.json` y `por_estrategia.json`; ADR D38 |
| 5 | Las alternativas | ✓ | `salidas/F3_hipotesis_alternativas_validacion.md` §3 |
| 6 | La validación, con controles y qué cambiaría la interpretación | ✓ | `salidas/F3_hipotesis_alternativas_validacion.md` §4; `research/ola3/C9_sensibilidad_umbral/RESULTADOS_validacion_retrospectiva.md` |
| 7 | Las dudas abiertas | ✓ con límite (ver abajo) | `entregables/correo-investigador.md` (borrador de siete preguntas); `salidas/PENDIENTES_FASES_1_A_3.md` |

## Las cinco preguntas de la guía

1. **¿Están las siete casillas?** Sí. Palabras por casilla: 1: 39, 2: 49, 3: 78, 4: 193, 5: 66, 6: 88, 7: 69. La fase pedía de una a tres líneas por casilla; las casillas 3 y 4 son las largas y se pasan, así que son las candidatas a recortar si se atragantan en la lectura en voz alta.
2. **¿Hay una decisión razonada?** Sí: separar el ranking en dos listas por mecanismo, con su razón (D20, D34, D38) y la alternativa descartada (lista única, con `MP_MRFV` primero por un artefacto).
3. **¿Hay una incertidumbre real?** Sí, y está medida: `eth` precede a `burs-α` en escala absoluta pero el par es inestable en min-max, `BicC_Dm` contra `eth` sólo se sostiene a 21 nt, y el filtro de si-Fi21 no se puede validar con datos abiertos (ρ = +0,142, IC95 [−0,247, +0,492], n = 29, *Tribolium*).
4. **¿Lo in silico se presenta como hipótesis?** Sí: la página dice «ventana que pasa el filtro» y «no demuestra silenciamiento»; los conteos propios van `[M]`, su lectura `[H]`, y no hay `[E]` sobre resultados propios.
5. **¿Las evidencias se pueden recuperar?** Parcialmente. Cada número tiene su archivo y se verificó contra él, pero `ranking_v2.json` sólo se puede regenerar con las secuencias de EPILAB y las siete referencias de C7 §9, que no están en el repo (B1 en `PENDIENTES_FASES_1_A_3.md`).

## Verificación numérica contra los archivos de origen

Se comprobó en código, sobre los archivos, que coinciden: las 2.000 muestras del barrido; 19 y 16 ventanas eficientes de 200 para `eth` y `burs-α` a 21 nt; eficacias de 0,1333 y 0,13 para `BicC_Dm` y `eth` a 22 nt; el mínimo de 78,5 % de `MP_MRFV` antes que `CP_MRFV` en la escala absoluta; que `BicC_Dm` va antes que `ATPaseD_Dm` y que `burs-α` en las dos escalas y a los dos largos, y que `eth` contra `burs-α` precede en escala absoluta y es inestable en min-max; los cuatro largos, las posiciones y las accesiones de W5; las accesiones PZ371507.1 y PZ371508.1; la ρ y su intervalo; y los tres DOI. Una de las comprobaciones falló al principio por un error de la prueba (comparaba números con texto), no de la página.

## Límites declarados

- **Casilla 3.** Los identificadores completos son los de los genes de la página. Las secuencias de EPILAB no se suben a ningún servicio, y las copias de trabajo están fuera del control de versiones.
- **Casilla 7.** Usa las preguntas del borrador, que tiene siete. No se sabe cuántas y cuáles tenía el correo realmente enviado (A1 en `PENDIENTES_FASES_1_A_3.md`).
- **`[H]` sin reproducir.** La cifra de 0,245 de la casilla 5 es un cálculo del repo sobre *Tribolium* que no se reprodujo en esta sesión; en la página figura como `[H]`.
- **Dalaisón-Fuentes 2022.** Sólo se usó el resumen de PubMed; la página la cita sólo como fuente del fenotipo del eje reproductivo.

## Criterio de terminado de la fase

- [x] Las siete casillas están completas.
- [x] Cabe en una página (450–700 palabras): 661.
- [x] Cada número está verificado contra su archivo.
- [x] No hay `[E]` sobre resultados propios.
- [x] El `.html` se generó y tiene las siete casillas.
- [ ] El usuario la leyó en voz alta y se entiende. **Pendiente: lo tiene que hacer el usuario.**

## Qué quedó sin hacer y por qué

1. **Lectura en voz alta (menos de cinco minutos).** Sólo la puede hacer el usuario. Lo que se atragante va a `00_meta/PREGUNTAS_ABIERTAS.md`.
2. **Diapositivas opcionales** (`entregables/checkpoint2-diapositivas.md`): no se hicieron; la guía acepta una página.
3. **Enlace desde `para-el-investigador.md`, `index.html` y `estado.html`:** es la Fase 5.
4. **Correcciones al catálogo C5, a C7 §6 y a `FUENTES.md` S18:** siguen en la sección D de `PENDIENTES_FASES_1_A_3.md`.

# Proyecto: Investigathon Y-Hat — Track chicharrita del maíz / RNAi

## Qué es esto
Repositorio de investigación de un equipo de 4 estudiantes de Ingeniería en IA
(UdeSA) para el Investigathon de Y-Hat (UBA). El track es el diseño y la
priorización de soluciones basadas en ARN exógeno (mecanismo de RNAi) contra el
vector *Dalbulus maidis* (chicharrita del maíz) y los patógenos que transmite.
El equipo NO aporta laboratorio: aporta bioinformática, datos, desarrollo
computacional e innovación abierta.

## Reglas permanentes

### Evidencia
- Toda afirmación técnica lleva fuente. Sin fuente, no entra al reporte.
- Etiquetá cada afirmación relevante con uno de estos marcadores:
  - `[E]` establecido: consenso en literatura revisada por pares.
  - `[R]` reportado: una o pocas fuentes, preprint, nota técnica, patente, web de empresa.
  - `[H]` hipótesis nuestra: idea del equipo, todavía sin respaldo.
  - `[?]` incierto / contradicción entre fuentes.
- Prohibido citar una fuente que no abriste. Nada de DOIs, títulos o números
  reconstruidos de memoria. Si no pudiste abrir la fuente, anotala en
  `00_meta/PREGUNTAS_ABIERTAS.md` como pendiente.
- Los números (porcentajes de eficacia, rendimientos, dosis, pérdidas de
  cosecha) van siempre con la fuente y el contexto experimental (laboratorio,
  invernáculo, campo; especie; n).

### Alcance ético y de seguridad
- El trabajo es control fitosanitario agrícola con información pública y
  publicada.
- Fuera de alcance, sin excepción: cualquier cosa que aumente la virulencia,
  la transmisibilidad o el rango de hospedadores de un patógeno; protocolos de
  síntesis o producción de agentes biológicos peligrosos; diseño dirigido a
  dañar especies no objetivo.
- Si una herramienta o búsqueda devuelve un rechazo, registralo en
  `00_meta/PREGUNTAS_ABIERTAS.md` y seguí con otra línea. No reformules para
  esquivar el rechazo.
- Toda propuesta de diseño incluye su contracara de riesgo: off-targets en
  maíz, en organismos no objetivo (polinizadores, enemigos naturales, fauna
  del suelo, humanos), persistencia ambiental y resistencia.

### Memoria del proyecto (se actualiza siempre, no al final)
- `00_meta/GLOSARIO.md` — término, definición en una línea, por qué nos importa.
- `00_meta/DECISIONS.md` — una entrada por decisión: fecha, decisión, alternativas
  consideradas, criterio, consecuencia. Formato ADR liviano.
- `00_meta/CAMINOS_PROBADOS.md` — qué se intentó, qué se descartó y por qué.
  Un descarte bien documentado vale tanto como un hallazgo.
- `00_meta/PREGUNTAS_ABIERTAS.md` — lo que no sabemos, lo que hay que preguntarle
  al investigador, lo que depende de datos que todavía no tenemos.
- `00_meta/FUENTES.md` — bibliografía consolidada.

### Formato
- Los reportes son prosa técnica en Markdown, no listas de bullets sueltos.
- Nombres científicos en itálica y completos la primera vez.
- Español. Términos técnicos en inglés entre paréntesis la primera vez que
  aparecen.

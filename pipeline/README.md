# pipeline — cómo se corre

Cadena que va del genoma de *Dalbulus maidis* a candidatos de ARN de doble cadena priorizados.
**Los resultados y su interpretación están en [REPORT.md](REPORT.md)**; esto es solo la parte
operativa.

## Correr

```bash
python pipeline/correr_todo.py --revisar    # qué hay, qué falta, en qué orden
python pipeline/correr_todo.py              # corre lo que falte, de punta a punta

python pipeline/cadena_completa.py 25 letal              # 25 genes, objetivo matar
python pipeline/cadena_completa.py 25 esteril --con-par  # esterilizar, con compañero de entrega
python pipeline/objetivo_candidatos.py esteril           # ranking de loci por objetivo
python pipeline/test_features.py                         # 17 pruebas de las features biofísicas
```

## Qué necesita

Biblioteca estándar de Python para casi todo. Las etapas que calculan estructura secundaria
necesitan **ViennaRNA**, y el mapeo necesita **miniprot**; las dos se indican en
`correr_todo.py --revisar` si faltan. El motor de decisión (`motor.py`) no necesita ninguna de
las dos: trabaja sobre features ya calculadas.

Los insumos pesados se descargan con los scripts `bajar_*.py` y `bajar_*.sh`, y se verifican con
`chequear_descargas.sh`.

## Qué no está en el repositorio

`salida/` y `datos/` están fuera del control de versiones. Las tablas que contienen fenotipos de
iBeetle-Base no se pueden republicar —su aviso legal reserva todos los derechos y requiere
consentimiento expreso— así que **se versiona el generador y no el dato**. Quien quiera
reproducirlas descarga la fuente original y corre `tabla_unificada.py`. Ver REPORT.md, sección 9.

## Mapa de los scripts

| Etapa | Script |
| --- | --- |
| Mapear proteínas de referencia al genoma | `hemip_mapear.py`, `resumir_miniprot.py`, `mapear_*.sh` |
| Cruzar loci con fenotipos de cribado | `tabla_unificada.py`, `explorar_fenotipos.py` |
| Rankear loci por objetivo de control | `objetivo_candidatos.py` |
| Blancos probados en hemípteros | `blancos_hemipteros.py`, `cruzar_hemipteros.py`, `buscar_rnai_hemipteros.py` |
| Enumerar ventanas y calcular features | `sirna_enumerar.py`, `region_scoring.py` |
| Catálogo y tamizaje de no objetivo | `no_objetivo_catalogo.py`, `no_objetivo_genomas.py`, `no_objetivo_correr.py`, `no_objetivo_cobertura.py`, `sirna_offtarget.py` |
| Puntuar y decidir | `motor.py`, `puntuar_candidatos.py` |
| Cadena completa | `cadena_completa.py`, `correr_todo.py` |
| Resultados negativos y controles | `techo_reproducibilidad.py`, `esencialidad_modelo.py`, `que_experimento_primero.py`, `tension_conservacion*.py` |
| Evidencia de literatura con verificación | `agente_evidencia.py` |

La línea de base publicada contra la que nos comparamos está en [`../baseline_dsrip/`](../baseline_dsrip/).

"""Scoring a nivel REGION: de ventanas de 21 nt a la molecula que realmente se aplica.

Lo que se sintetiza y se aplica a campo es un dsRNA largo (300-500 pb), no un siRNA suelto.
Dicer lo corta en un pool heterogeneo de siRNAs. Entonces la unidad de diseno es la region, y
una region buena es la que produce MUCHOS siRNAs buenos, no la que contiene a la mejor ventana.
Las dos preguntas no tienen la misma respuesta.

Entrada: el CSV que genera `sirna_enumerar.py` (todas las ventanas puntuadas de un CDS) o varios
genes concatenados con una columna `locus`. Columnas usadas:
  pos, score             obligatorias (la posicion es relativa al CDS de cada gen)
  descarte               filtro duro de sirna_enumerar ("" = vivo)
  locus                  opcional; si falta, todo el archivo es un solo gen
  off_target_max, riesgo opcionales; los pone `cadena_completa.py` o `agregar_off_target`

La clave de una ventana es `locus|pos`, no `pos`: pos colisiona entre genes.

Metricas del pool de cada region deslizante:
  n_vivos / frac_vivos   cuantas ventanas pasan los filtros duros
  media, mediana         del score, contando las descartadas como 0 (un siRNA descartado no es
                         un efector, y la region que tiene muchos produce menos senal)
  frac_buenos            fraccion de ventanas con score >= percentil P del GEN (por defecto 75)
  p10                    percentil 10 del score: el "piso" robusto del pool
  peor                   minimo. Degenerado: en una region de 280 ventanas casi siempre hay una
                         descartada, o sea vale 0 en casi todas. Se reporta pero no sirve para rankear.
  n_off_alerta/descartar ventanas de la region con riesgo de off-target (si hay datos)
  buenos_limpios         ventanas buenas que ademas no tienen riesgo de off-target

Criterio de orden por defecto: `buenos_limpios` (cuantos efectores buenos y limpios produce el
pool). Veto duro por region: si alguna ventana de la region tiene una coincidencia exacta de
21 nt con un organismo no objetivo (off_target_max >= 21), TODA la region se descarta, porque
Dicer procesa el dsRNA entero y esa ventana va a estar en el pool. Ver los hallazgos f2 de
region para la justificacion y las limitaciones (sin verdad experimental).

Uso:
    python3 region_scoring.py <ventanas.csv> [--largo 300] [--paso 1] [--percentil 75]
                              [--agg buenos_limpios] [--score score] [--top 5]
                              [--sin-veto] [--csv regiones.csv]
"""

from __future__ import annotations

import csv
import sys
from bisect import bisect_left
from collections import defaultdict
from pathlib import Path
from statistics import median

VENTANA = 21
AGREGACIONES = ("frac_buenos", "media", "mediana", "p10", "buenos_limpios")
UMBRAL_OFF_ALERTA = 17
UMBRAL_OFF_DESCARTAR = 21


def clave_de(fila: dict) -> str:
    locus = (fila.get("locus") or "").strip()
    return f"{locus}|{fila['pos']}" if locus else str(fila["pos"])


def leer_ventanas(ruta: Path) -> dict[str, list[dict]]:
    """Agrupa por locus y ordena por posicion. Un archivo sin columna locus es un solo gen."""
    genes: dict[str, list[dict]] = defaultdict(list)
    with ruta.open(encoding="utf-8") as fh:
        for fila in csv.DictReader(fh):
            genes[(fila.get("locus") or "").strip()].append(fila)
    for filas in genes.values():
        filas.sort(key=lambda f: int(f["pos"]))
    return genes


def percentil(valores_ordenados: list[float], p: float) -> float:
    """Percentil por interpolacion lineal sobre una lista ya ordenada."""
    if not valores_ordenados:
        return 0.0
    k = (len(valores_ordenados) - 1) * p / 100
    i = int(k)
    j = min(i + 1, len(valores_ordenados) - 1)
    return valores_ordenados[i] + (valores_ordenados[j] - valores_ordenados[i]) * (k - i)


def tiene_riesgo_off_target(fila: dict, umbral: int) -> bool:
    valor = fila.get("off_target_max")
    return valor not in (None, "") and int(float(valor)) >= umbral


def regiones_de_un_gen(filas: list[dict], largo: int = 300, paso: int = 1,
                       p_bueno: float = 75, campo_score: str = "score") -> list[dict]:
    """Metricas del pool para cada region deslizante de `largo` pb de un gen."""
    posiciones = [int(f["pos"]) for f in filas]
    scores = [float(f[campo_score] or 0.0) if not f.get("descarte") else 0.0 for f in filas]
    vivos = [0 if f.get("descarte") else 1 for f in filas]
    ordenados_vivos = sorted(s for s, v in zip(scores, vivos) if v)
    umbral_bueno = percentil(ordenados_vivos, p_bueno)
    bueno = [1 if (v and s >= umbral_bueno) else 0 for s, v in zip(scores, vivos)]
    hay_off = any(f.get("off_target_max") not in (None, "") for f in filas)
    alerta = [1 if tiene_riesgo_off_target(f, UMBRAL_OFF_ALERTA) else 0 for f in filas]
    descartar = [1 if tiene_riesgo_off_target(f, UMBRAL_OFF_DESCARTAR) else 0 for f in filas]
    limpio = [1 if b and not a else 0 for b, a in zip(bueno, alerta)]

    def prefijo(v: list[int]) -> list[int]:
        acc = [0]
        for x in v:
            acc.append(acc[-1] + x)
        return acc

    p_vivos, p_bueno_, p_alerta, p_desc, p_limpio = map(prefijo, (vivos, bueno, alerta, descartar, limpio))
    p_score = [0.0]
    for s in scores:
        p_score.append(p_score[-1] + s)

    ventanas_por_region = largo - VENTANA + 1
    salida = []
    inicio_min, inicio_max = posiciones[0], posiciones[-1] - ventanas_por_region + 1
    for ini in range(inicio_min, inicio_max + 1, paso):
        a = bisect_left(posiciones, ini)
        b = bisect_left(posiciones, ini + ventanas_por_region)
        n = b - a
        if n < ventanas_por_region * 0.9:
            continue
        sc = scores[a:b]
        sc_vivos = sorted(s for s, v in zip(sc, vivos[a:b]) if v)
        salida.append({
            "inicio": ini,
            "fin": ini + largo - 1,
            "n_ventanas": n,
            "n_vivos": p_vivos[b] - p_vivos[a],
            "frac_vivos": round((p_vivos[b] - p_vivos[a]) / n, 4),
            "media": round((p_score[b] - p_score[a]) / n, 5),
            "mediana": round(median(sc), 5),
            "frac_buenos": round((p_bueno_[b] - p_bueno_[a]) / n, 4),
            "p10": round(percentil(sorted(sc), 10), 5),
            "peor": round(min(sc), 5),
            "n_off_alerta": (p_alerta[b] - p_alerta[a]) if hay_off else "",
            "n_off_descartar": (p_desc[b] - p_desc[a]) if hay_off else "",
            "buenos_limpios": (p_limpio[b] - p_limpio[a]) if hay_off else (p_bueno_[b] - p_bueno_[a]),
            "umbral_bueno": round(umbral_bueno, 5),
        })
    return salida


def elegir_regiones(regiones: list[dict], agg: str, k: int = 5, solape_max: float = 0.5,
                    largo: int = 300) -> list[dict]:
    """Las k mejores regiones sin que se pisen mas de `solape_max` entre si (greedy).

    Sin esto, el top-k de una ventana deslizante son k desplazamientos de 1 pb de la misma region.
    """
    elegidas: list[dict] = []
    for r in sorted(regiones, key=lambda r: -float(r[agg])):
        if all(abs(r["inicio"] - e["inicio"]) >= largo * (1 - solape_max) for e in elegidas):
            elegidas.append(r)
        if len(elegidas) == k:
            break
    return elegidas


def solape(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Pares de bases en comun entre dos intervalos cerrados."""
    return max(0, min(a[1], b[1]) - max(a[0], b[0]) + 1)


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0].startswith("-"):
        sys.exit(__doc__)

    def opcion(nombre: str, defecto: str) -> str:
        return args[args.index(nombre) + 1] if nombre in args else defecto

    largo = int(opcion("--largo", "300"))
    paso = int(opcion("--paso", "1"))
    percentil_bueno = float(opcion("--percentil", "75"))
    agg = opcion("--agg", "buenos_limpios")
    veto = "--sin-veto" not in args
    campo = opcion("--score", "score")
    top = int(opcion("--top", "5"))
    if agg not in AGREGACIONES:
        sys.exit(f"--agg debe ser una de {AGREGACIONES}")

    genes = leer_ventanas(Path(args[0]))
    todas: list[dict] = []
    for locus, filas in genes.items():
        regiones = regiones_de_un_gen(filas, largo, paso, percentil_bueno, campo)
        for r in regiones:
            r["locus"] = locus
        todas.extend(regiones)
        if not regiones:
            print(f"{locus or '(gen unico)'}: CDS mas corto que {largo} pb, sin regiones")
            continue
        media_gen = sum(float(f[campo] or 0) for f in filas) / len(filas)
        aptas = [r for r in regiones if not (veto and r["n_off_descartar"] not in ("", 0))]
        for r in regiones:
            r["apta"] = int(r in aptas)
        if len(aptas) < len(regiones):
            print(f"\n{locus or '(gen unico)'}: veto de off-target deja {len(aptas)} de {len(regiones)} regiones")
        if not aptas:
            print(f"{locus or '(gen unico)'}: ninguna region apta (toda region contiene un 21-mero identico a un no objetivo)")
            continue
        mejores = elegir_regiones(aptas, agg, top, largo=largo)
        print(f"\n{locus or '(gen unico)'}: {len(filas)} ventanas, {len(regiones)} regiones de {largo} pb, "
              f"orden por {agg} (media del gen {media_gen:.3f})")
        print(f"{'region':>12}{'vivos':>7}{'media':>8}{'mediana':>9}{'buenos':>8}{'p10':>8}{'limpios':>9}")
        for r in mejores:
            print(f"{r['inicio']:>5}-{r['fin']:<6}{r['frac_vivos']:>7.2f}{r['media']:>8.3f}"
                  f"{r['mediana']:>9.3f}{r['frac_buenos']:>8.2f}{r['p10']:>8.3f}{r['buenos_limpios']:>9}")

    destino = opcion("--csv", "")
    if destino and todas:
        with open(destino, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(todas[0].keys()))
            w.writeheader()
            w.writerows(todas)
        print(f"\n{len(todas)} regiones escritas en {destino}")


if __name__ == "__main__":
    main()

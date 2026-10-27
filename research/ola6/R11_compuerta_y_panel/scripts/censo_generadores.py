"""R11, parte 2: el censo de todo generador que puede producir una region recomendada.

El issue #35 parte de una leccion medida: `D70` y el issue #30 buscaron las regiones sin
tamizar **mirando** `regiones_recomendadas` de las dos corridas del ranking, y esa busqueda
no alcanzo —`BicC_Dm` 2123-2422 salia del bloque `efecto_humano` del mismo generador—. La
conclusion de la entrada 24 de la ola 6 es que la forma de encontrarlas no es buscarlas a
mano: es correr cada generador de punta a punta y dejar que la compuerta las senale.

Este script no reemplaza esas corridas. Hace las dos cosas que si se pueden hacer sin
`work/` y que son las que convierten «no se busco mas» en «esto es lo que hay que correr»:

  1. **Un barrido estatico de TODO el repositorio** (`.py`, salteando `.git`,
     `.claude/worktrees` y `__pycache__`) buscando las cuatro marcas que distinguen a un
     generador de regiones: que llame a `alternativas()`, que llame a
     `ranking.region_recomendada()`, que llame a `alertas.exigir_decidida()` y que arme la
     region a mano con `["mejores"][0]["region"]`. Un archivo con la primera y sin la
     segunda es, por construccion, un lugar donde una region puede nacer sin pasar por la
     compuerta: eso es lo que hay que mirar.
  2. **Un intento de corrida de cada generador declarado**, con su comando exacto, y el
     registro de **que error dio** cuando no pudo. Un «no corrio» sin el error no sirve:
     la regla de `D71` es decir en que maquina se verifico y que insumo falta, y el error
     exacto es lo que lo dice.

Lo que el barrido estatico **no** puede ver: una region que se publique como texto ya
calculado (un `REPORT.md`, un TSV escrito a mano) no tiene ninguna de las cuatro marcas. El
censo cubre generadores, no documentos, y el ultimo eslabon entre el computo y lo publicado
sigue siendo una persona (entrada 10 de la ola 6).

    python research/ola6/R11_compuerta_y_panel/scripts/censo_generadores.py
    python research/ola6/R11_compuerta_y_panel/scripts/censo_generadores.py --sin-correr
"""
from __future__ import annotations

import argparse
import csv
import json
import platform
import re
import subprocess
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
SALIDA = Path(__file__).resolve().parents[1] / "resultados"

# Las cuatro marcas. Son textuales a proposito: un censo que importara los modulos para
# inspeccionarlos necesitaria los insumos que justamente faltan.
MARCAS = {
    "llama_alternativas": re.compile(r"(?<![\w.])(?:R\.)?alternativas\s*\("),
    "llama_region_recomendada": re.compile(r"region_recomendada\s*\("),
    "llama_exigir_decidida": re.compile(r"exigir_decidida\s*\("),
    "arma_region_a_mano": re.compile(r"\[\"mejores\"\]\[0\]|\['mejores'\]\[0\]"),
}
# Las definiciones no cuentan como llamadas: `ranking.py` define las dos funciones.
DEFINE = re.compile(r"^def\s+(alternativas|region_recomendada|exigir_decidida)\s*\(",
                    re.MULTILINE)
SALTAR = (".git", "__pycache__", ".venv", "node_modules")
SALTAR_RUTA = (".claude/worktrees",)

# Los generadores declarados, con el comando exacto con el que se los intenta correr.
# `produce` dice que region puede nacer ahi; `insumo` es lo que ese comando necesita y que
# `work/` no versiona.
GENERADORES = [
    {"nombre": "ranking.py ranking",
     "ruta": "tools/sifi21_port/ranking.py",
     "comando": [sys.executable, "tools/sifi21_port/ranking.py", "ranking",
                 "--muestras", "50"],
     "produce": "la region recomendada por la cascada para los cuatro de EPILAB (nivel 3)",
     "insumo": "work/sifi_check/salida y work/sifi_check/offtarget_full"},
    {"nombre": "ranking.py nulo",
     "ruta": "tools/sifi21_port/ranking.py",
     "comando": [sys.executable, "tools/sifi21_port/ranking.py", "nulo", "--reps", "50"],
     "produce": "la region maxima de cada gen por conteo (no pasa por la compuerta)",
     "insumo": "work/sifi_check/salida"},
    {"nombre": "ranking_v2.py",
     "ruta": "tools/sifi21_port/ranking_v2.py",
     # **Sin `--muestras`, a proposito.** Este comando llevaba `--muestras 50` para
     # abaratar la corrida, y eso rompia el ancla del barrido por construccion: el ancla
     # compara frecuencias contra `W7` con igualdad exacta, lo que solo tiene sentido con
     # el mismo numero de sorteos, asi que con 50 muestras daba multiplos de 2,0 contra
     # las decimas finas de las 2.000 publicadas y el censo reportaba «ANCLA ROTA» —el
     # peor mensaje posible, porque es el que nadie ignora— por un parametro que el censo
     # mismo habia cambiado. Con el default corre entero y pasa todas las anclas en unos
     # 60 s (issue #37, entrada 66 de PREGUNTAS_ABIERTAS.md).
     "comando": [sys.executable, "tools/sifi21_port/ranking_v2.py",
                 "--trabajo", "work/sifi_v2",
                 "--json", "work/R11_censo/ranking_v2_censo.json"],
     "produce": ("regiones por tres caminos: completar_regiones, recomendadas y las dos "
                 "ramas de efecto_humano"),
     "insumo": "work/sifi_v2 (salida_k21, salida_k22, offtarget_k*, offtarget_dm_k*)"},
    {"nombre": "M6 tabla_alertas.py",
     "ruta": "research/ola4/M6_alertas/scripts/tabla_alertas.py",
     "comando": [sys.executable, "research/ola4/M6_alertas/scripts/tabla_alertas.py"],
     "produce": ("el inventario mismo; pasa por la compuerta via las anclas de M5, que "
                 "llaman a ranking_v2.recomendadas()"),
     "insumo": "work/m6_alertas/identidad_por_ventana.tsv y work/W5/ref"},
    {"nombre": "M6 compuerta.py",
     "ruta": "research/ola4/M6_alertas/scripts/compuerta.py",
     "comando": [sys.executable, "research/ola4/M6_alertas/scripts/compuerta.py"],
     "produce": "nada: itera sobre las regiones que YA estan en el inventario",
     "insumo": "research/ola4/M6_alertas/resultados/alertas.tsv (versionado)"},
    {"nombre": "M6 umbral_compuerta.py",
     "ruta": "research/ola4/M6_alertas/scripts/umbral_compuerta.py",
     "comando": [sys.executable, "research/ola4/M6_alertas/scripts/umbral_compuerta.py"],
     "produce": "nada: el mismo recorrido, con los dos umbrales de D28",
     "insumo": "research/ola4/M6_alertas/resultados/alertas.tsv (versionado)"},
    {"nombre": "M5 sensibilidad_reparto.py",
     "ruta": "research/ola4/M5_dos_ejes/scripts/sensibilidad_reparto.py",
     # `--resultados` a `work/`, y **esto no es cosmetico**: mientras este generador
     # fallaba por insumo no escribia nada, y al destrabarse (issue #37) empezo a escribir
     # en `research/ola4/M5_dos_ejes/resultados/`, que es lo que se versiona. Con los
     # `--muestras 50` del censo eso sobreescribe las cifras publicadas de M5 con una
     # corrida de cincuenta sorteos. Un censo que verifica si un generador corre no puede
     # dejar su salida de prueba donde vive la salida publicada.
     "comando": [sys.executable, "research/ola4/M5_dos_ejes/scripts/sensibilidad_reparto.py",
                 "--muestras", "50",
                 "--resultados", "work/R11_censo/m5_sensibilidad"],
     "produce": ("la columna region_recomendada de regiones_recomendadas_por_reparto.tsv, "
                 "que sale de ranking_v2.recomendadas() via anclas.py"),
     "insumo": "work/sifi_v2 (lo pide anclas.correr())"},
    {"nombre": "O3 01_region_vatpase_b.py",
     "ruta": "research/ola6/O3_quimera_bicc_vatpase_b/scripts/01_region_vatpase_b.py",
     "comando": [sys.executable,
                 "research/ola6/O3_quimera_bicc_vatpase_b/scripts/01_region_vatpase_b.py"],
     "produce": ("la region candidata de V-ATPase B; arma la region a mano a proposito "
                 "(D74) porque es insumo de una medicion y no una recomendacion"),
     "insumo": "work/o3 y work/W5/ref"},
]


def sin_comentarios(fuente: str) -> str:
    """Las marcas se cuentan sobre codigo, no sobre prosa.

    Un modulo de este repositorio explica en comentarios y docstrings lo que hace y lo que
    no hace, asi que buscar `region_recomendada(` sobre el texto crudo daria positivo en
    cada archivo que **hable** de la compuerta. Se sacan las lineas de comentario, los
    bloques de triple comilla y las cadenas de una linea; esto ultimo hace falta porque
    tanto `test_alertas.py` como este mismo script llevan las marcas **como dato** —una en
    la constante `A_MANO`, el otro en `MARCAS`— y sin sacarlas el censo se denuncia a si
    mismo. Es grosero y alcanza: lo que queda es codigo.
    """
    sin_doc = re.sub(r'""".*?"""', "", fuente, flags=re.DOTALL)
    sin_doc = re.sub(r"'''.*?'''", "", sin_doc, flags=re.DOTALL)
    sin_lit = re.sub(r'"[^"\n]*"', '""', sin_doc)
    sin_lit = re.sub(r"'[^'\n]*'", "''", sin_lit)
    return "\n".join(l for l in sin_lit.splitlines() if not l.lstrip().startswith("#"))


def barrer() -> list[dict]:
    """Toda la fuente del repositorio, con las cuatro marcas y la definicion aparte."""
    filas = []
    for py in sorted(RAIZ.rglob("*.py")):
        rel = py.relative_to(RAIZ).as_posix()
        if any(p in py.parts for p in SALTAR) or any(s in rel for s in SALTAR_RUTA):
            continue
        codigo = sin_comentarios(py.read_text(encoding="utf-8", errors="replace"))
        definidas = set(DEFINE.findall(codigo))
        f = {"archivo": rel, "define": ",".join(sorted(definidas)) or "-"}
        for nombre, rx in MARCAS.items():
            f[nombre] = bool(rx.search(codigo))
        # Una llamada a `alternativas()` sin ninguna llamada a la compuerta en el mismo
        # archivo es el caso a mirar: ahi una region puede nacer sin tamizado.
        f["region_sin_compuerta"] = (f["llama_alternativas"]
                                     and not f["llama_region_recomendada"]
                                     and not f["llama_exigir_decidida"]
                                     and "alternativas" not in definidas)
        filas.append(f)
    return [f for f in filas if any(f[m] for m in MARCAS) or f["define"] != "-"]


def correr(gen: dict, limite: int) -> dict:
    """Intenta el comando y guarda el veredicto con el error exacto si no pudo.

    `motivo` es la ultima linea no vacia de la salida de error, que en este repositorio es
    donde cae el mensaje de insumo faltante. No se interpreta: se copia. `falta` es aparte
    porque la ultima linea no siempre nombra el archivo: la de `O3` es un `StopIteration`
    que sale de buscar un gen en una tabla que no esta, y el archivo que falta aparece mas
    arriba en el rastro.
    """
    t0 = time.time()
    try:
        p = subprocess.run(gen["comando"], cwd=RAIZ, capture_output=True, text=True,
                           timeout=limite)
        salida = (p.stderr or "").strip() or (p.stdout or "").strip()
        lineas = [l for l in salida.splitlines() if l.strip()]
        falta = re.search(r"No such file or directory: ['\"](.+?)['\"]", salida)
        return {"corrio": p.returncode == 0, "codigo": p.returncode,
                "motivo": lineas[-1][:400] if lineas and p.returncode != 0 else "",
                "falta": falta.group(1) if falta else "",
                "segundos": round(time.time() - t0, 1)}
    except subprocess.TimeoutExpired:
        return {"corrio": False, "codigo": None,
                "motivo": "timeout a los %d s; no es un fallo de insumo" % limite,
                "falta": "", "segundos": round(time.time() - t0, 1)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sin-correr", action="store_true",
                    help="solo el barrido estatico, sin intentar ninguna corrida")
    ap.add_argument("--limite", type=int, default=900, help="segundos por comando")
    a = ap.parse_args()

    estatico = barrer()
    print("barrido estatico: %d archivos con alguna marca" % len(estatico))
    for f in estatico:
        if f["region_sin_compuerta"]:
            print("  REVISAR  %s llama alternativas() y no llama a la compuerta" % f["archivo"])

    corridas = []
    for gen in GENERADORES:
        fila = {k: gen[k] for k in ("nombre", "ruta", "produce", "insumo")}
        fila["comando"] = " ".join(str(c) for c in gen["comando"][1:])
        if a.sin_correr:
            fila.update({"corrio": None, "codigo": None, "motivo": "no se intento",
                         "falta": "", "segundos": 0.0})
        else:
            print("  corriendo %s ..." % gen["nombre"], flush=True)
            fila.update(correr(gen, a.limite))
            print("    %s  %s" % ("OK" if fila["corrio"] else "NO",
                                  fila["motivo"][:120]), flush=True)
        corridas.append(fila)

    # Las columnas son fijas y no salen de la primera fila: un barrido vacio —que seria un
    # hallazgo, no un caso normal— tiene que escribir el TSV con su cabecera y cero filas,
    # no morir con `IndexError`.
    COLS_ESTATICO = ["archivo", "define"] + list(MARCAS) + ["region_sin_compuerta"]
    COLS_CORRIDAS = ["nombre", "ruta", "produce", "insumo", "comando", "corrio", "codigo",
                     "motivo", "falta", "segundos"]
    SALIDA.mkdir(parents=True, exist_ok=True)
    for nombre, cols, datos in (("censo_generadores.tsv", COLS_ESTATICO, estatico),
                                ("censo_corridas.tsv", COLS_CORRIDAS, corridas)):
        with (SALIDA / nombre).open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", extrasaction="ignore")
            w.writeheader()
            for f in datos:
                w.writerow(f)
    (SALIDA / "censo_generadores.json").write_text(
        json.dumps({"maquina": {"sistema": platform.system(),
                                "version": platform.version(),
                                "python": platform.python_version(),
                                "work_existe": (RAIZ / "work").exists()},
                    "estatico": estatico, "corridas": corridas},
                   indent=1, ensure_ascii=False),
        encoding="utf-8")
    print("escrito en %s" % SALIDA)
    return 0


if __name__ == "__main__":
    sys.exit(main())

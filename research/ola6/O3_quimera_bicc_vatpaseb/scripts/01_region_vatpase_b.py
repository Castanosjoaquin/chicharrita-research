"""O3 paso 1 — elegir la region de 300 nt de `V-ATPase B`, con el criterio declarado antes.

Por que hace falta este paso. La quimera de `O3` pega una region de `BicC_Dm` con una
de `V-ATPase B`, y la de `BicC_Dm` ya esta elegida y publicada (922-1221, que D25 movio
por conservacion). La de `V-ATPase B` no existe: el gen recien se recupero en `O2`. Asi
que antes de armar la quimera hay que elegirla, y elegirla **con el mismo criterio con
el que se eligieron las otras**, no con uno nuevo que convenga al resultado.

EL CRITERIO, ESCRITO ANTES DE LA PRIMERA CORRIDA (D71 en adelante):

1. **Largo 300 nt**, el de los dos genes del insecto en el conjunto vigente (`BicC_Dm`
   922-1221 y `ATPaseD_Dm` 72-371). No se busca el largo optimo: cambiar el largo
   cambiaria la comparacion con las regiones ya publicadas.
2. **Perfil de eficiencia en el contexto del gen entero**, modo `corregido`, backend
   `vienna`. Es lo que hizo C7: `ranking` recibe el perfil del gen completo y recorta
   regiones sobre el. El modo `corregido` es el de los numeros publicados de C7 y C13.
3. **Marco 1 de `D63`** —«contexto, todos los arranques»—, que es el que usa
   `ranking.conteo_por_region`: la region [i, i+299] puntua las 300 ventanas cuyo
   **inicio** cae en ese tramo, de las cuales las ultimas 20 se extienden hasta 20 nt mas
   alla del final de la region. Es la convencion del original (`sifi21_reproduccion.md`
   §2) y el marco en el que `C7` eligio las regiones publicadas, asi que se respeta para
   que el orden sea comparable. **La cifra que se publica de una region es la del marco 3**
   (molecula recortada), y no sale de aca: la calcula
   `research/ola5/N3_marcos/scripts/tres_marcos.py`, que `O3` corrio para esta region con
   su bandera `--gen`. Que el ranking se arme en un marco y se publique otro es lo que
   `D63` dejo escrito; este script no lo cambia.
4. **Riesgo con el panel de seis de W7 y `ranking.pesos_base()`**, sin tocar los pesos.
   El genoma de *Dalbulus maidis* sale del computo por on-target, que es lo que hace
   `ranking.excluidas_de` con `estrategia: insecto`.
5. **Regla conservadora** (`solo_eficientes=False`): el riesgo de una ventana cuenta sea
   o no eficiente. Es la que usa `ranking_v2` para las regiones recomendadas. La regla
   mecanicista (D2) se informa al lado como sensibilidad, no decide.
6. **Forma `cascada`**: veto duro por coincidencia perfecta de 21 nt y orden por
   `buenos_limpios` (eficientes sin ningun acierto). La forma `geometrica` se informa
   como sensibilidad. Si las dos formas no coinciden en el primer puesto, se declara.
7. **No pisarse**: entre las regiones que se listan hay al menos 150 nt de separacion,
   la regla de `ranking.alternativas` (`largo * 0.5`), porque el top-k de una ventana
   deslizante son k desplazamientos de 1 pb de la misma region.

LO QUE ESTE PASO **NO** PRODUCE. Una region recomendada. `ranking.region_recomendada()`
exige que las alertas de la region esten decididas, pero no distingue «se tamizo y no hay
alertas» de «no se tamizo» (es la pregunta abierta que D70 y el issue #30 cierran). Esta
region no tiene fila en el inventario de doce de `M6`, asi que pasaria la compuerta por
ausencia de datos, no por estar limpia. Se llama **region candidata de O3** y asi viaja a
todas las tablas. Convertirla en recomendacion pide el tamizado del inventario de #30.

Entradas (ninguna sale de la maquina):
  work/O3/sifi/full_corregido/<nombre>_corregido_vienna.tsv   perfil del CDS entero
  work/O3/offtarget/offtarget_por_sirna.tsv                    tamizado del panel de seis

Uso:
    python research/ola6/O3_quimera_bicc_vatpaseb/scripts/01_region_vatpase_b.py
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[4]
BLOQUE = Path(__file__).resolve().parents[1]
RESULTADOS = BLOQUE / "resultados"
TRABAJO = RAIZ / "work/O3"

sys.path.insert(0, str(RAIZ / "tools/sifi21_port"))
import ranking as R  # noqa: E402  el motor de W7, sin tocarlo

LARGO = 300
MODO, BACKEND = "corregido", "vienna"


def perfil_del_tsv(ruta: Path) -> tuple[np.ndarray, np.ndarray]:
    pos, efi = [], []
    with ruta.open(encoding="utf-8") as fh:
        for f in csv.DictReader(fh, delimiter="\t"):
            pos.append(int(f["pos"]))
            efi.append(str(f["is_efficient"]).strip().lower() in ("true", "1", "yes"))
    return np.array(pos, dtype=int), np.array(efi, dtype=bool)


def riesgo_del_tsv(ruta: Path, consulta: str, n: int) -> dict:
    """Matriz de riesgo con la forma que espera `ranking.ejes`."""
    riesgo: dict[str, dict[str, np.ndarray]] = {}
    with ruta.open(encoding="utf-8") as fh:
        r = csv.DictReader(fh, delimiter="\t")
        cols = [c for c in (r.fieldnames or []) if "|" in c]
        for c in cols:
            ref, crit = c.split("|", 1)
            riesgo.setdefault(ref, {})[crit] = np.zeros(n, dtype=bool)
        vistas = 0
        for fila in r:
            if fila["consulta"] != consulta:
                continue
            p = int(fila["pos"])
            if not 1 <= p <= n:
                continue
            vistas += 1
            for c in cols:
                if int(fila[c] or 0) > 0:
                    ref, crit = c.split("|", 1)
                    riesgo[ref][crit][p - 1] = True
    if vistas != n:
        raise SystemExit("el tamizado trae %d ventanas de %s y el perfil %d"
                         % (vistas, consulta, n))
    for ref in riesgo:
        for crit in R.CRITERIOS:
            riesgo[ref].setdefault(crit, np.zeros(n, dtype=bool))
    return riesgo


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--largo", type=int, default=LARGO)
    a = ap.parse_args(argv)

    tsv_perfil = next((TRABAJO / "sifi" / "full_corregido").glob("*_%s_%s.tsv"
                                                                % (MODO, BACKEND)))
    consulta = tsv_perfil.name.rsplit("_%s_%s.tsv" % (MODO, BACKEND), 1)[0]
    pos, efi = perfil_del_tsv(tsv_perfil)
    n = int(pos.max())
    if len(pos) != n:
        raise SystemExit("el perfil no es contiguo: %d filas, maximo %d" % (len(pos), n))

    g = {"gen": "VATPaseB_Dm", "n": n,
         "eficiente": np.zeros(n, dtype=bool), "presente": np.ones(n, dtype=bool),
         "riesgo": riesgo_del_tsv(TRABAJO / "offtarget" / "offtarget_por_sirna.tsv",
                                  consulta, n)}
    g["eficiente"][pos - 1] = efi

    wr, wc = R.pesos_base()
    cand = {"gen": "VATPaseB_Dm", "estrategia": "insecto",
            "region": (1, a.largo), "largo": a.largo}
    excluir = R.excluidas_de(cand, "off")

    print("CDS %s" % consulta)
    print("  ventanas de 21 nt: %d   eficientes: %d (%.1f %%)"
          % (n, int(efi.sum()), 100.0 * efi.sum() / n))
    print("  referencias en el riesgo: %s" % ", ".join(
        sorted(R.corto(r) for r in g["riesgo"] if r not in excluir)))
    print("  excluida por on-target: %s" % ", ".join(sorted(R.corto(r) for r in excluir)))
    print("  criterio: %d nt, regla conservadora, forma cascada (veto por 21/21)\n"
          % a.largo)

    por_forma = {}
    for forma in ("cascada", "geometrica"):
        alt = R.alternativas(g, a.largo, cand, wr, wc, False, "off", 0.5, forma, tope=5)
        por_forma[forma] = alt
        print("forma %s: %d regiones posibles, %d no vetadas"
              % (forma, alt["regiones_posibles"], alt["no_vetadas"]))
        print("  %-14s %9s %6s %6s %7s %8s %9s" % (
            "region", "puntaje", "efic", "off", "21/21", "lim+ef", "limpieza"))
        for m in alt["mejores"]:
            print("  %-14s %9.4f %6d %6d %7d %8d %9.4f" % (
                m["region"], m["puntaje"], m["eficientes"], m["con_off_target"],
                m["con_21_perfecto"], m["buenos_limpios"], m["limpieza"]))
        print()

    elegida = por_forma["cascada"]["mejores"][0]["region"]
    primera_geom = por_forma["geometrica"]["mejores"][0]["region"]
    ini, fin = (int(x) for x in elegida.split("-"))

    # Percentil de la elegida por el camino publicado: `alternativas` lo calcula para
    # la region que recibe en `cand`, asi que se la vuelve a llamar con la ganadora.
    cand_e = dict(cand, region=(ini, fin))
    ficha = R.alternativas(g, a.largo, cand_e, wr, wc, False, "off", 0.5, "cascada")
    mec = R.ejes(g, ini, ini + a.largo - 1, wr, wc, excluir, True)
    cons = R.ejes(g, ini, ini + a.largo - 1, wr, wc, excluir, False)

    print("REGION CANDIDATA DE O3: %s  (no es region recomendada: ver encabezado)" % elegida)
    print("  percentil de la elegida entre las %d regiones del mismo largo: %.1f"
          % (ficha["regiones_posibles"], ficha["percentil_elegida"]))
    print("  vetada: %s" % ("SI" if cons["vetada"] else "no"))
    print("  regla conservadora: %d eficientes, %d limpios y eficientes, limpieza %.4f"
          % (cons["eficientes"], cons["buenos_limpios"], cons["limpieza"]))
    print("  regla mecanicista:  %d eficientes, %d limpios y eficientes, limpieza %.4f"
          % (mec["eficientes"], mec["buenos_limpios"], mec["limpieza"]))
    print("  la forma geometrica pone primera a %s: %s" % (
        primera_geom, "coincide" if primera_geom == elegida else "NO coincide"))

    RESULTADOS.mkdir(parents=True, exist_ok=True)
    salida = {
        "paso": "O3 paso 1 — region candidata de V-ATPase B",
        "consulta": consulta, "cds_nt": int(n + R.VENTANA - 1), "ventanas": n,
        "eficientes_cds": int(efi.sum()),
        "criterio": {
            "largo_nt": a.largo, "modo": MODO, "backend": BACKEND,
            "regla": "conservadora (solo_eficientes=False)",
            "forma": "cascada (veto por perfecto_21, orden por buenos_limpios)",
            "contexto_del_perfil": "gen entero",
            "marco": "marco 1 de D63, contexto todos los arranques: 300 ventanas por "
                     "inicio. La cifra publicable de la region es la del marco 3 y la "
                     "calcula research/ola5/N3_marcos/scripts/tres_marcos.py",
            "panel": sorted(R.corto(r) for r in g["riesgo"] if r not in excluir),
            "excluidas_on_target": sorted(R.corto(r) for r in excluir),
            "pesos": "ranking.pesos_base(), sin tocar",
        },
        "region_candidata": {
            "coordenadas": elegida, "inicio": ini, "fin": fin,
            "percentil": ficha["percentil_elegida"],
            "conservadora": {k: cons[k] for k in (
                "n_ventanas", "eficientes", "eficacia", "limpieza", "buenos_limpios",
                "con_off_target", "con_21_perfecto", "vetada")},
            "mecanicista": {k: mec[k] for k in (
                "n_ventanas", "eficientes", "eficacia", "limpieza", "buenos_limpios",
                "con_off_target", "con_21_perfecto", "vetada")},
            "es_region_recomendada": False,
            "por_que_no": "no tiene fila en el inventario de doce de M6; la compuerta "
                          "de D69 la dejaria pasar por ausencia de datos, no por estar "
                          "limpia (D70, issue #30)",
        },
        "sensibilidad": {f: por_forma[f]["mejores"] for f in por_forma},
        "coincide_cascada_geometrica": primera_geom == elegida,
        "python": sys.version.split()[0],
    }
    (RESULTADOS / "region_vatpase_b.json").write_text(
        json.dumps(salida, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\nescrito en %s" % (RESULTADOS / "region_vatpase_b.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

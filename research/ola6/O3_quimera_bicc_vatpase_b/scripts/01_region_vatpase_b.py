"""O3 paso 1 — la region de 300 nt de `V-ATPase B`, por el criterio de `PREREGISTRO.md`.

**El criterio no lo elige este script: lo fija `PREREGISTRO.md` §2, escrito y commiteado
antes de medir.** Este archivo lo ejecuta y nada mas. Si alguna pieza de aca no coincide
con el preregistro, el preregistro manda y esto es un error a corregir.

Las piezas, con el punto del preregistro al que corresponden:

1. **Largo 300 nt** (§2.1), como `BicC_Dm` y `ATPaseD_Dm`. No se busca el largo optimo.
2. **Forma `cascada`** (§2.2): una region queda vetada si alguna de sus ventanas tiene
   coincidencia perfecta de 21 nt contra el panel, y entre las no vetadas ordena por
   `buenos_limpios`. Se llaman `ranking.ejes()` y `ranking.puntaje()` **importados sin
   modificarlos**.
3. **Pesos base** (§2.3), `ranking.pesos_base()`, sin sortear.
4. **Panel de seis con la humana a 1,00** (§2.4), via
   `ranking_v2.con_panel(sin_humano=False)`, y el genoma de *D. maidis* **excluido** por
   on-target, que es lo que hace `ranking.excluidas_de()` con `estrategia="insecto"`.
   La humana es la referencia de mayor peso junto con el maiz y la nombro el investigador.
5. **Banda de 59 nt en cada extremo excluida de antemano** (§2.5): el CDS viene del genoma
   y no tiene UTR, asi que una ventana cerca de un extremo se pliega contra un contexto que
   en el ARNm real existe y aca falta. El alcance esta derivado del codigo en `C13` §4.
   Inicios admisibles **60 a 1.145**, o sea regiones de 60-359 a 1.145-1.444.
6. **Se reportan los dos top-3** (§3): el de la lista restringida, que es el que define la
   quimera, y el de la lista **sin** la restriccion de borde, para que se vea cuanto pesa.

Dos cosas que este paso NO produce:

- **Una region recomendada.** Es el insumo de la medicion de `O3` (§3). Recomendar una
  region no es de esta linea. Desde `D72` la compuerta de alertas **rechaza** una region
  ausente del inventario de `M6` con `alertas.RegionNoTamizada`, asi que esta region no
  puede presentarse como recomendada ni por descuido: primero hay que tamizarla.
- **La cifra publicable del conteo.** El orden de la cascada corre en el marco 1 de `D63`,
  que es el marco en el que `C7` eligio las regiones publicadas. La cifra que se publica es
  la del marco 3 (molecula recortada) y la calcula
  `research/ola5/N3_marcos/scripts/tres_marcos.py`.

Como se verifica que la restriccion de borde esta bien aplicada: el ordenador restringido,
corrido **sin** restriccion, tiene que reproducir el top-3 de `ranking.alternativas()` celda
por celda. Si no lo reproduce, el script aborta y no hay region.

Entradas (ninguna sale de la maquina):
  work/O3/sifi/full_corregido/<nombre>_corregido_vienna.tsv   perfil del CDS entero
  work/O3/offtarget/offtarget_por_sirna.tsv                    las seis de work/offtarget_db
  work/O3/offtarget_humano/offtarget_por_sirna.tsv             la humana

Uso:
    python research/ola6/O3_quimera_bicc_vatpase_b/scripts/01_region_vatpase_b.py
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
import ranking as R      # noqa: E402  el motor de W7, sin tocarlo
import ranking_v2 as V   # noqa: E402  solo para fijar el panel

LARGO = 300
MODO, BACKEND = "corregido", "vienna"
#: §2.5 del preregistro. `C13` §4: la secuencia vecina influye hasta 59 nt corriente
#: arriba del comienzo de una ventana.
BANDA_BORDE = 59
TOPE = 3


def perfil_del_tsv(ruta: Path) -> tuple[np.ndarray, np.ndarray]:
    pos, efi = [], []
    with ruta.open(encoding="utf-8") as fh:
        for f in csv.DictReader(fh, delimiter="\t"):
            pos.append(int(f["pos"]))
            efi.append(str(f["is_efficient"]).strip().lower() in ("true", "1", "yes"))
    return np.array(pos, dtype=int), np.array(efi, dtype=bool)


def riesgo_de_los_tsv(rutas: list[Path], consulta: str, n: int) -> dict:
    """Matriz de riesgo con la forma que espera `ranking.ejes`, de varios tamizados.

    Cada corrida de `offtarget_21nt.py` escribe una columna por referencia; el panel de
    seis esta repartido en dos corridas porque la humana vive en otro directorio.
    """
    riesgo: dict[str, dict[str, np.ndarray]] = {}
    for ruta in rutas:
        if not ruta.exists():
            raise SystemExit("falta el tamizado %s" % ruta)
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
            raise SystemExit("%s trae %d ventanas de %s y el perfil %d"
                             % (ruta, vistas, consulta, n))
    for ref in riesgo:
        for crit in R.CRITERIOS:
            riesgo[ref].setdefault(crit, np.zeros(n, dtype=bool))
    return riesgo


def ordenar_regiones(g, largo, wr, wc, excluir, inicios, tope=TOPE):
    """La cascada sobre un conjunto de inicios, con `ejes` y `puntaje` sin tocar.

    Replica la seleccion de `ranking.alternativas`: descarta las vetadas, ordena por
    puntaje y se queda con las que no se pisan mas de la mitad. La unica diferencia es
    que recibe los inicios admisibles en vez de enumerar todos, que es lo que pide §2.5
    del preregistro. La fidelidad se verifica corriendola sin restriccion.
    """
    puntos = []
    for ini in inicios:
        e = R.ejes(g, ini, ini + largo - 1, wr, wc, excluir, False)
        puntos.append((ini, R.puntaje(e, 0.5, "cascada"), e))
    vivos = [(i, p, e) for i, p, e in puntos if not e["vetada"]]
    elegidas = []
    for i, p, e in sorted(vivos, key=lambda t: -t[1]):
        if all(abs(i - j) >= largo * 0.5 for j, _, _ in elegidas):
            elegidas.append((i, p, e))
        if len(elegidas) == tope:
            break
    return {
        "regiones_posibles": len(puntos),
        "no_vetadas": len(vivos),
        "mejores": [{"region": "%d-%d" % (i, i + largo - 1), "puntaje": round(p, 4),
                     "eficientes": e["eficientes"], "con_off_target": e["con_off_target"],
                     "con_21_perfecto": e["con_21_perfecto"],
                     "buenos_limpios": e["buenos_limpios"],
                     "eficacia": round(e["eficacia"], 4),
                     "limpieza": round(e["limpieza"], 4)}
                    for i, p, e in elegidas],
    }


def imprimir(titulo, d):
    print("%s: %d regiones posibles, %d no vetadas"
          % (titulo, d["regiones_posibles"], d["no_vetadas"]))
    print("  %-14s %9s %6s %6s %7s %8s %9s"
          % ("region", "puntaje", "efic", "off", "21/21", "lim+ef", "limpieza"))
    for m in d["mejores"]:
        print("  %-14s %9.4f %6d %6d %7d %8d %9.4f"
              % (m["region"], m["puntaje"], m["eficientes"], m["con_off_target"],
                 m["con_21_perfecto"], m["buenos_limpios"], m["limpieza"]))
    print()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--largo", type=int, default=LARGO)
    # `--resultados` existe por el issue #37. El censo de generadores de `R11` corre este
    # script para ver si termina, y **cada corrida reescribe `region_vatpase_b.json`**: no
    # mueve ninguna cifra —verificado, las cuatro diferencias son el nombre de la consulta,
    # dos separadores de ruta de Windows y la version de Python— pero deja el arbol sucio y
    # hace que un `git status` despues del censo parezca un cambio de resultados. Es el
    # defecto que `sensibilidad_reparto.py` pago mas caro, con dos archivos de M5
    # reemplazados (entrada 90 de PREGUNTAS_ABIERTAS.md).
    ap.add_argument("--resultados", type=Path, default=None,
                    help="directorio de salida; el default es el del bloque, que es el que "
                         "se versiona. Una corrida que no sea para publicar deberia "
                         "escribir en work/.")
    a = ap.parse_args(argv)

    # §2.4: el panel de seis, con la humana a 1,00. Se fija ANTES de pedir los pesos.
    V.con_panel(sin_humano=False)

    tsv_perfil = next((TRABAJO / "sifi" / "full_corregido").glob("*_%s_%s.tsv"
                                                                % (MODO, BACKEND)))
    consulta = tsv_perfil.name.rsplit("_%s_%s.tsv" % (MODO, BACKEND), 1)[0]
    pos, efi = perfil_del_tsv(tsv_perfil)
    n = int(pos.max())
    if len(pos) != n:
        raise SystemExit("el perfil no es contiguo: %d filas, maximo %d" % (len(pos), n))

    tamizados = [TRABAJO / "offtarget" / "offtarget_por_sirna.tsv",
                 TRABAJO / "offtarget_humano" / "offtarget_por_sirna.tsv"]
    g = {"gen": "VATPaseB_Dm", "n": n,
         "eficiente": np.zeros(n, dtype=bool), "presente": np.ones(n, dtype=bool),
         "riesgo": riesgo_de_los_tsv(tamizados, consulta, n)}
    g["eficiente"][pos - 1] = efi

    wr, wc = R.pesos_base()
    cand = {"gen": "VATPaseB_Dm", "estrategia": "insecto",
            "region": (1, a.largo), "largo": a.largo}
    excluir = R.excluidas_de(cand, "off")
    en_riesgo = sorted(R.corto(r) for r in g["riesgo"] if r not in excluir)
    if len(en_riesgo) != 6:
        raise SystemExit("el panel tiene %d referencias y el preregistro pide seis: %s"
                         % (len(en_riesgo), ", ".join(en_riesgo)))

    cds_nt = n + R.VENTANA - 1
    ini_min = BANDA_BORDE + 1
    ini_max = cds_nt - BANDA_BORDE - a.largo + 1

    print("CDS %s  (%d nt, %d ventanas, %d eficientes)"
          % (consulta, cds_nt, n, int(efi.sum())))
    print("  panel de seis: %s" % ", ".join(en_riesgo))
    print("  excluida por on-target: %s" % ", ".join(sorted(R.corto(r) for r in excluir)))
    print("  pesos: %s" % ", ".join("%s %.2f" % (R.corto(k), v)
                                    for k, v in sorted(wr.items(), key=lambda t: -t[1])
                                    if k not in excluir))
    print("  banda de borde excluida: %d nt; inicios admisibles %d a %d\n"
          % (BANDA_BORDE, ini_min, ini_max))

    # Fidelidad: sin restriccion tiene que dar lo mismo que `alternativas`.
    todos = list(range(1, n - a.largo + 2))
    mio_sin = ordenar_regiones(g, a.largo, wr, wc, excluir, todos)
    alt = R.alternativas(g, a.largo, cand, wr, wc, False, "off", 0.5, "cascada", tope=TOPE)
    if mio_sin["mejores"] != alt["mejores"] or \
            (mio_sin["regiones_posibles"], mio_sin["no_vetadas"]) != \
            (alt["regiones_posibles"], alt["no_vetadas"]):
        print("MIO:", json.dumps(mio_sin["mejores"], ensure_ascii=False))
        print("ALT:", json.dumps(alt["mejores"], ensure_ascii=False))
        raise SystemExit("el ordenador restringido no reproduce ranking.alternativas()")
    print("VERIFICACION: sin restriccion reproduce ranking.alternativas() celda por celda\n")

    imprimir("sin la restriccion de borde (sensibilidad, §3)", mio_sin)
    restringido = ordenar_regiones(g, a.largo, wr, wc, excluir,
                                   list(range(ini_min, ini_max + 1)))
    imprimir("con la restriccion de borde (§2.5, la que define la quimera)", restringido)

    if not restringido["mejores"]:
        raise SystemExit("ninguna region admisible sobrevive al veto")
    elegida = restringido["mejores"][0]["region"]
    ini, fin = (int(x) for x in elegida.split("-"))
    mec = R.ejes(g, ini, ini + a.largo - 1, wr, wc, excluir, True)
    cons = R.ejes(g, ini, ini + a.largo - 1, wr, wc, excluir, False)
    cambia = elegida != mio_sin["mejores"][0]["region"]

    print("REGION DE O3: %s  (insumo de la medicion, no region recomendada)" % elegida)
    print("  regla conservadora: %d eficientes, %d limpias y eficientes, limpieza %.4f"
          % (cons["eficientes"], cons["buenos_limpios"], cons["limpieza"]))
    print("  regla mecanicista:  %d eficientes, %d limpias y eficientes, limpieza %.4f"
          % (mec["eficientes"], mec["buenos_limpios"], mec["limpieza"]))
    print("  la restriccion de borde %s la eleccion%s"
          % ("CAMBIA" if cambia else "no cambia",
             ": sin ella seria %s" % mio_sin["mejores"][0]["region"] if cambia else ""))

    # Cuanto pesa cada referencia en el veto, que es lo que vuelve legible el resultado.
    por_ref = {}
    for ref in sorted(g["riesgo"]):
        if ref in excluir:
            continue
        v21 = int(g["riesgo"][ref]["perfecto_21"].sum())
        por_ref[R.corto(ref)] = {
            "ventanas_perfecto_21": v21,
            "ventanas_perfecto_ge19": int(g["riesgo"][ref]["perfecto_ge19"].sum()),
            "ventanas_mm1_21": int(g["riesgo"][ref]["mm1_21"].sum()),
            "peso": wr[ref]}
    print("\n  veto por referencia, en el CDS entero (ventanas con 21/21):")
    for corto, d in sorted(por_ref.items(), key=lambda t: -t[1]["ventanas_perfecto_21"]):
        print("    %-14s peso %.2f   21/21 %4d   >=19 %4d   1mm %4d"
              % (corto, d["peso"], d["ventanas_perfecto_21"],
                 d["ventanas_perfecto_ge19"], d["ventanas_mm1_21"]))

    # Una ruta relativa se resuelve contra la raiz del repositorio y no contra el
    # directorio de trabajo de quien llama: el censo de `R11` la pasa relativa.
    destino = (RAIZ / a.resultados) if a.resultados else RESULTADOS
    destino.mkdir(parents=True, exist_ok=True)
    (destino / "region_vatpase_b.json").write_text(json.dumps({
        "paso": "O3 paso 1 — region de V-ATPase B segun PREREGISTRO.md §2",
        "consulta": consulta, "cds_nt": cds_nt, "ventanas": n,
        "eficientes_cds": int(efi.sum()),
        "criterio": {
            "fuente": "research/ola6/O3_quimera_bicc_vatpase_b/PREREGISTRO.md §2",
            "largo_nt": a.largo, "modo": MODO, "backend": BACKEND, "tabla_nn": "NN3",
            "regla": "conservadora (solo_eficientes=False)",
            "forma": "cascada (veto por perfecto_21, orden por buenos_limpios)",
            "panel": en_riesgo, "panel_con_humano": True,
            "excluidas_on_target": sorted(R.corto(r) for r in excluir),
            "pesos": {R.corto(k): v for k, v in wr.items() if k not in excluir},
            "banda_borde_nt": BANDA_BORDE,
            "inicios_admisibles": [ini_min, ini_max],
            "marco": "marco 1 de D63; la cifra publicable es el marco 3, en tres_marcos",
        },
        "verificacion": "el ordenador restringido, sin restriccion, reproduce "
                        "ranking.alternativas() celda por celda",
        "region_de_o3": {
            "coordenadas": elegida, "inicio": ini, "fin": fin,
            "conservadora": {k: cons[k] for k in (
                "n_ventanas", "eficientes", "eficacia", "limpieza", "buenos_limpios",
                "con_off_target", "con_21_perfecto", "vetada")},
            "mecanicista": {k: mec[k] for k in (
                "n_ventanas", "eficientes", "eficacia", "limpieza", "buenos_limpios",
                "con_off_target", "con_21_perfecto", "vetada")},
            "es_region_recomendada": False,
            "por_que_no": "es el insumo de la medicion de O3 (PREREGISTRO §3). Desde D72 "
                          "la compuerta rechaza una region ausente del inventario de M6 "
                          "con alertas.RegionNoTamizada: para recomendarla hay que "
                          "tamizarla primero",
        },
        "con_restriccion_de_borde": restringido,
        "sin_restriccion_de_borde": mio_sin,
        "la_restriccion_cambia_la_eleccion": cambia,
        "veto_por_referencia_en_el_cds": por_ref,
        "tamizados": [str(p.relative_to(RAIZ)) for p in tamizados],
        "python": sys.version.split()[0],
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\nescrito en %s" % (destino / "region_vatpase_b.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

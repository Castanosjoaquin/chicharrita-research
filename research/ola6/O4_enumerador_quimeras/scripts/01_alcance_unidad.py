"""O4 — cuanto cambia cada conteo publicado segun la unidad del largo de region.

Por que existe este script. El ancla 3 del preregistro no paso, y la causa no fue una
medicion sino una unidad: `ranking.ejes()` corta los vectores indexados por ventana con
`slice(ini - 1, fin)`, asi que una region «a-b» son `b - a + 1` **ventanas** y consume
`b - a + 21` nt de secuencia, mientras que `quimeras_v2.recortar()` y `tres_marcos.py`
cortan `full[a - 1:b]`, que son `b - a + 1` **nucleotidos** y contienen `b - a - 19`
ventanas (`PREGUNTAS_ABIERTAS.md` 46). Las dos convenciones se escriben igual.

**Las dos unidades ya tienen nombre, y es el aporte de esta correccion.** Son el marco 1 y
el marco 2 de `D63`, tal como los definio `N3`: el marco 1 cuenta los `L` arranques que
caen en la region, con las ultimas veinte ventanas completadas por nucleotidos de afuera, y
el marco 2 cuenta los `L - 20` 21-meros que existen fisicamente en la molecula. Asi que en
el eje de **eficacia** esto no es un hallazgo: es un ancla, y la corrida la verifica contra
las cifras que `N3` publico. Donde la unidad **no** esta declarada es en el eje de
**riesgo**, porque `ranking.ejes()` calcula el veto sobre el tramo del marco 1 y entonces
una region puede quedar vetada por un 21-mero que la molecula no contiene
(`PREGUNTAS_ABIERTAS.md` 46).

Que contesta, y que no. Contesta **cuanto** se mueve cada conteo de las regiones vigentes
al cambiar de marco, y si alguna region gana o pierde una coincidencia perfecta de 21 nt
—que es lo unico que podria mover una fila del inventario de alertas de `M6`—. **No corrige
ninguna cifra publicada** ni decide cual marco adopta el eje de riesgo: eso es de la linea
que toca cifras publicadas y lo decide el equipo.

Alcance declarado: los cuatro genes de EPILAB, que son los que tienen perfil y tamizado del
panel de seis en disco. `eth_Dm` y `bursA_Dm`, las otras dos regiones vigentes, necesitan
las bases de `work/C11/`, que **no estan en esta maquina** (es el mismo faltante que
registro `D71`), asi que quedan sin medir y declarado.

Entradas (ninguna sale de la maquina, ninguna se versiona):
  work/sifi_check/salida/<gen>_full_corregido_vienna.tsv        perfil del gen entero
  work/sifi_check/offtarget_full/offtarget_por_sirna.tsv        el panel de seis (O3)

Uso:
    python research/ola6/O4_enumerador_quimeras/scripts/01_alcance_unidad.py
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[4]
BLOQUE = Path(__file__).resolve().parents[1]
RESULTADOS = BLOQUE / "resultados"
PERFILES = RAIZ / "work/sifi_check/salida"
TAMIZADO = RAIZ / "work/sifi_check/offtarget_full/offtarget_por_sirna.tsv"

sys.path.insert(0, str(RAIZ / "tools/sifi21_port"))
import ranking as R      # noqa: E402
import ranking_v2 as V   # noqa: E402

VENTANA = 21

#: Las regiones vigentes del proyecto, tal como las publica `entregables/`. Las dos que
#: faltan, `eth_Dm` 114-313 y `bursA_Dm` 13-212, no tienen insumo en esta maquina.
VIGENTES = {
    "MP_MRFV": (72, 271, "viral"),
    "CP_MRFV": (99, 298, "viral"),
    "BicC_Dm": (922, 1221, "insecto"),
    "ATPaseD_Dm": (72, 371, "insecto"),
}
SIN_INSUMO = {"eth_Dm": (114, 313), "bursA_Dm": (13, 212)}

#: Lo que `N3` publico para estas cuatro regiones: (marco 1, marco 2). Es el ancla de esta
#: corrida: si no reproduce estas ocho celdas, el que esta mal es este script y no `N3`.
#: Fuente: `research/ola5/N3_marcos/resultados/tres_marcos.json`, claves
#: `marco1_contexto_todos` y `marco2_contexto_comparables`.
N3 = {"MP_MRFV": (38, 31), "CP_MRFV": (21, 20),
      "BicC_Dm": (36, 29), "ATPaseD_Dm": (21, 17)}


def perfil_de(gen: str) -> np.ndarray:
    """Etiqueta de eficiente por ventana del gen entero, del TSV de `run_sifi.py`."""
    ruta = PERFILES / ("%s_full_corregido_vienna.tsv" % gen)
    if not ruta.exists():
        raise SystemExit("falta el perfil %s" % ruta)
    pos, efi = [], []
    with ruta.open(encoding="utf-8") as fh:
        for fila in csv.DictReader(fh, delimiter="\t"):
            pos.append(int(fila["pos"]))
            efi.append(str(fila["is_efficient"]).strip().lower() in ("true", "1", "yes"))
    v = np.zeros(max(pos), dtype=bool)
    v[np.array(pos) - 1] = efi
    return v


def veto_de(gen: str, n: int, estrategia: str) -> dict[int, set[str]]:
    """Ventanas con coincidencia perfecta de 21 nt, y contra que referencia del panel."""
    V.con_panel(sin_humano=False)
    refs = list(R.REFERENCIAS)
    if len(refs) != 6:
        raise SystemExit("el panel tiene %d referencias y hacen falta seis" % len(refs))
    # El genoma del vector **no** es una de las seis: va aparte y es on-target para los
    # genes del insecto, mientras que para los virales cuenta como off-target con el
    # default de D5. Por eso el admitido se arma sumando y despues restando, y no
    # restando de seis.
    excluidas = R.excluidas_de({"estrategia": estrategia}, "off")
    admitidas = (set(refs) | {R.DMAIDIS}) - excluidas
    if not TAMIZADO.exists():
        raise SystemExit("falta el tamizado %s" % TAMIZADO)
    golpes: dict[int, set[str]] = {}
    with TAMIZADO.open(encoding="utf-8") as fh:
        lector = csv.DictReader(fh, delimiter="\t")
        cols = [c for c in (lector.fieldnames or [])
                if c.endswith("|perfecto_21") and c.split("|", 1)[0] in admitidas]
        if len(cols) != len(admitidas):
            raise SystemExit("%s: el tamizado trae %d referencias de las %d admitidas"
                             % (gen, len(cols), len(admitidas)))
        for fila in lector:
            if fila["consulta"] != "%s_full" % gen:
                continue
            p = int(fila["pos"])
            if not 1 <= p <= n:
                continue
            for c in cols:
                if int(fila[c] or 0) > 0:
                    golpes.setdefault(p, set()).add(R.corto(c.split("|", 1)[0]))
    return golpes


def main() -> int:
    filas, resumen, fallas = [], {}, []
    print("Los dos marcos de D63 sobre las regiones vigentes. El marco 1 es el tramo que")
    print("corta ranking.ejes(); el marco 2 son los 21-meros que existen en la molecula.\n")
    print("%-12s %-10s %7s %7s %6s %6s %7s %7s" % (
        "gen", "region", "vent_m2", "vent_m1", "ef_m2", "ef_m1", "21_m2", "21_m1"))
    for gen, (a, b, estrategia) in VIGENTES.items():
        efi = perfil_de(gen)
        n = len(efi)
        golpes = veto_de(gen, n, estrategia)
        largo = b - a + 1

        # Convencion nucleotidos: la region son `largo` nt y contiene las ventanas a..b-20.
        v_nt = list(range(a, b - VENTANA + 2))
        # Convencion ventanas: la region son `largo` ventanas, a..b, y consume largo+20 nt.
        v_vt = list(range(a, b + 1))
        if v_vt[-1] > n:
            raise SystemExit("%s: la region %d-%d en ventanas se pasa del gen (%d)"
                             % (gen, a, b, n))

        ef_nt = int(sum(efi[p - 1] for p in v_nt))
        ef_vt = int(sum(efi[p - 1] for p in v_vt))
        g_nt = {p: sorted(golpes[p]) for p in v_nt if p in golpes}
        g_vt = {p: sorted(golpes[p]) for p in v_vt if p in golpes}

        print("%-12s %-10s %7d %7d %6d %6d %7d %7d" % (
            gen, "%d-%d" % (a, b), len(v_nt), len(v_vt), ef_nt, ef_vt, len(g_nt), len(g_vt)))
        esperado = N3.get(gen)
        if esperado is not None and (ef_vt, ef_nt) != esperado:
            fallas.append("%s: N3 publica marco1=%d y marco2=%d, y aca salen %d y %d"
                          % (gen, esperado[0], esperado[1], ef_vt, ef_nt))
        filas.append({
            "gen": gen, "region": "%d-%d" % (a, b), "largo_declarado": largo,
            "estrategia": estrategia,
            "nt_que_consume_en_marco2": largo,
            "nt_que_consume_en_marco1": largo + VENTANA - 1,
            "ventanas_marco2": len(v_nt),
            "ventanas_marco1": len(v_vt),
            "eficientes_marco2": ef_nt,
            "eficientes_marco1": ef_vt,
            "delta_eficientes": ef_vt - ef_nt,
            "n3_marco1": esperado[0] if esperado else "",
            "n3_marco2": esperado[1] if esperado else "",
            "con_21_perfecto_marco2": len(g_nt),
            "con_21_perfecto_marco1": len(g_vt),
            "aciertos_solo_en_la_cola": json.dumps(
                {p: r for p, r in g_vt.items() if p not in g_nt}, ensure_ascii=False),
        })
        resumen[gen] = {"region": "%d-%d" % (a, b), "eficientes": [ef_nt, ef_vt],
                        "con_21_perfecto": [len(g_nt), len(g_vt)]}

    RESULTADOS.mkdir(parents=True, exist_ok=True)
    with (RESULTADOS / "alcance_unidad_region.tsv").open(
            "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()), delimiter="\t")
        w.writeheader(); w.writerows(filas)
    (RESULTADOS / "alcance_unidad_region.json").write_text(json.dumps({
        "que_mide": "cuanto cambia cada conteo de las regiones vigentes segun la unidad "
                    "del largo de region; no corrige ninguna cifra publicada",
        "convenciones": {
            "ventanas": "ranking.ejes(): la region a-b son b-a+1 ventanas y consume "
                        "b-a+21 nt",
            "nucleotidos": "quimeras_v2 y tres_marcos: la region a-b son b-a+1 nt y "
                           "contiene b-a-19 ventanas"},
        "modo": "corregido", "backend": "vienna", "panel": "seis con la humana a 1,00",
        "regiones": resumen,
        "sin_insumo_en_esta_maquina": {g: "%d-%d" % r for g, r in SIN_INSUMO.items()},
        "python": sys.version.split()[0],
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    cola = [f for f in filas if f["aciertos_solo_en_la_cola"] != "{}"]
    print("\nregiones que ganan un acierto perfecto de 21 nt al leerse en marco 1: %d"
          % len(cola))
    for f in cola:
        print("  %s %s  %s" % (f["gen"], f["region"], f["aciertos_solo_en_la_cola"]))
    print("\nsin insumo en esta maquina (necesitan work/C11/): %s"
          % ", ".join("%s %d-%d" % (g, *r) for g, r in SIN_INSUMO.items()))
    for f in fallas:
        print("ANCLA FALLA  %s" % f)
    print("ancla contra N3 (ocho celdas, marcos 1 y 2): %s"
          % ("PASA" if not fallas else "FALLA"))
    print("escrito en %s" % RESULTADOS)
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main())

"""M6: qué transcripto impacta cada coincidencia. El cuarto campo de D48.

El cuarto campo que pide D48 —«qué gen está involucrado»— no se puede leer de ningún
TSV que ya exista: `offtarget_21nt.py` calcula el conjunto de referencias impactadas en
`escanear()` y `main()` escribe sólo `len(refs)`, así que la identidad se computa y se
tira. Este script la conserva con `offtarget_21nt.escanear_con_identidad()` y la anota
con la cabecera del FASTA de referencia, que ya está en disco. **Nada sale de la
máquina** (CLAUDE.md): el tamizaje es local y por coincidencia exacta.

Qué corre:

  * las **anclas de M5** (`anclas.correr()`), que abortan el proceso si el motor dejó de
    reproducir `ranking_v2.json`. Corren antes de cualquier medición de esta línea;
  * el tamizaje de los seis genes contra las **seis referencias del panel** de C7 v2, y
    el de los dos genes virales contra el **genoma del vector**, que para los genes del
    insecto es on-target y `ranking.excluidas_de()` lo saca del cómputo;
  * el **ancla A3**, propia de esta línea: colapsar la tabla de identidad a booleanos
    por ventana × referencia × criterio tiene que reproducir **celda por celda** la
    matriz de `work/sifi_v2/`, que es la que alimenta todos los números publicados. Si
    no coincide, aborta.

No se corre `--mm1`: D28 decide sobre 21/21 perfecto y bloque de ≥ 19 nt, y la tabla de
alertas no usa el tercer criterio.

    python research/ola4/M6_alertas/scripts/identidad.py
"""
from __future__ import annotations

import csv
import json
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "tools" / "sifi21_port"))
sys.path.insert(0, str(RAIZ / "research/ola4/M5_dos_ejes/scripts"))

import offtarget_21nt as O   # noqa: E402
import ranking as R          # noqa: E402
import ranking_v2 as V       # noqa: E402
import anclas as A           # noqa: E402

REF = RAIZ / "work" / "W5" / "ref"
FASTA = RAIZ / "work" / "sifi_v2" / "fasta"
SALIDA = RAIZ / "work" / "m6_alertas"
PANEL = ["GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna.fna.gz",
         "GCF_914767665.1_icHarAxyr1.1_rna.fna.gz",
         "GCF_003254395.2_Amel_HAv3.1_rna.fna.gz",
         "GCF_021130785.1_UT_GWSS_2.1_rna.fna.gz",
         "GCF_002217175.1_ASM221717v1_rna.fna.gz",
         "humano_rna.fna.gz"]
GENOMA_VECTOR = "GCA_975739785.1_ihDalMaid1.1_genomic.fna.gz"
GENES = V.GENES_EPILAB + V.GENES_NUEVOS
VIRALES = ["MP_MRFV", "CP_MRFV"]
CRITERIOS = ("perfecto_21", "perfecto_ge19")


def base_de(ruta: str) -> str:
    return Path(ruta).name.replace(".fna.gz", "").replace(".fasta", "")


def tamizar(genes: list[str], bases: list[Path]) -> tuple[list[dict], dict]:
    """Filas (gen, pos, referencia, criterio, transcripto) y la anotación por accesión."""
    consultas = [FASTA / ("%s_full.fasta" % g) for g in genes]
    aut, sirnas = O.construir(consultas, con_mm1=False)
    print("  %d ventanas, %d patrones" % (len(sirnas), len(aut)), flush=True)
    filas, anotaciones = [], {}
    for ruta in bases:
        t0 = time.time()
        hits, anot = O.escanear_con_identidad(aut, sirnas, ruta)
        base = base_de(ruta)
        anotaciones.update({(base, a): d for a, d in anot.items()})
        n = 0
        for crit in CRITERIOS:
            for idx, accs in hits[crit].items():
                s = sirnas[idx]
                for acc in sorted(accs):
                    filas.append({"gen": s["consulta"].replace("_full", ""),
                                  "pos": s["pos"], "referencia": base,
                                  "corto": R.corto(base) if base != base_de(GENOMA_VECTOR)
                                  else R.DMAIDIS_INFO["corto"],
                                  "criterio": crit, "transcripto": acc,
                                  "anotacion": anot.get(acc, "")})
                    n += 1
        print("  %-55s %6d filas  (%.0f s)" % (base, n, time.time() - t0), flush=True)
    return filas, anotaciones


def a3_contra_la_matriz(filas: list[dict]) -> list[dict]:
    """Colapsar la identidad a booleanos reproduce la matriz de `work/sifi_v2/`."""
    mio: set[tuple] = set()
    for f in filas:
        mio.add((f["gen"], f["pos"], f["referencia"], f["criterio"]))
    suyo: set[tuple] = set()
    for sub in ("offtarget_k21", "offtarget_dm_k21"):
        ruta = RAIZ / "work" / "sifi_v2" / sub / "offtarget_por_sirna.tsv"
        with ruta.open(encoding="utf-8") as fh:
            for fila in csv.DictReader(fh, delimiter="\t"):
                gen = fila["consulta"].replace("_full", "")
                for col, val in fila.items():
                    if "|" not in col or not val or int(val) == 0:
                        continue
                    ref, crit = col.split("|")
                    if crit in CRITERIOS:
                        suyo.add((gen, int(fila["pos"]), ref, crit))
    faltan, sobran = suyo - mio, mio - suyo
    return [{"ancla": "A3", "celdas_matriz": len(suyo), "celdas_mias": len(mio),
             "faltan": sorted(faltan)[:20], "sobran": sorted(sobran)[:20],
             "n_faltan": len(faltan), "n_sobran": len(sobran),
             "coincide": not faltan and not sobran}]


def main() -> int:
    print("anclas de M5 (abortan si fallan)...", flush=True)
    A.correr()
    print("tamizaje contra el panel de seis referencias...", flush=True)
    filas, anot = tamizar(GENES, [REF / p for p in PANEL])
    print("tamizaje de los dos genes virales contra el genoma del vector...", flush=True)
    f2, anot2 = tamizar(VIRALES, [REF / GENOMA_VECTOR])
    filas += f2
    anot.update(anot2)

    a3 = a3_contra_la_matriz(filas)
    print("A3  identidad vs matriz de work/sifi_v2: %s (%d celdas, faltan %d, sobran %d)"
          % ("coincide" if a3[0]["coincide"] else "NO COINCIDE", a3[0]["celdas_matriz"],
             a3[0]["n_faltan"], a3[0]["n_sobran"]), flush=True)

    SALIDA.mkdir(parents=True, exist_ok=True)
    campos = ["gen", "pos", "referencia", "corto", "criterio", "transcripto", "anotacion"]
    with (SALIDA / "identidad_por_ventana.tsv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=campos, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        for f in sorted(filas, key=lambda d: (d["gen"], d["pos"], d["referencia"],
                                              d["criterio"], d["transcripto"])):
            w.writerow(f)
    (SALIDA / "identidad_anclas.json").write_text(
        json.dumps({"A3": a3, "n_filas": len(filas),
                    "transcriptos_distintos": len({(f["referencia"], f["transcripto"])
                                                   for f in filas})},
                   indent=1, ensure_ascii=False), encoding="utf-8")
    print("escrito en %s" % (SALIDA / "identidad_por_ventana.tsv").relative_to(RAIZ))
    if not a3[0]["coincide"]:
        sys.exit("ANCLA A3 ROTA: la tabla de identidad no reproduce la matriz publicada")
    return 0


if __name__ == "__main__":
    sys.exit(main())

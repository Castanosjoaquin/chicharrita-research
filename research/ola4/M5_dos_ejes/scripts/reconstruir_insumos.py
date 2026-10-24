"""Reconstruye `work/sifi_v2/` a 21 nt, que es lo que `ranking_v2.cargar()` espera.

En esta maquina `work/sifi_v2/` no existia (M5, 2026-10-24) y sin el no se puede
reproducir ningun numero de `research/ola3/C7_ranking_v2/resultados/ranking_v2.json`.
La receta es la del encabezado de ese REPORT.md, con dos diferencias declaradas:

  * solo k = 21. El ranking v2 publica 21 y 22; esta linea mide a 21 nt, que es el
    largo con el que C9 T1 bis midio la fragilidad del tercer puesto. k = 22 queda
    NO CORRIDO, no en cero.
  * el escaneo contra el genoma de *Dalbulus maidis* se corre solo con los dos genes
    virales. Para los cuatro genes del insecto esa referencia es on-target y
    `ranking.excluidas_de()` la saca del computo, asi que sus filas no entran a
    ningun numero. Verificado por las anclas del gen entero.

Nada sale de la maquina: las referencias se leen de disco (CLAUDE.md).

    python research/ola4/M5_dos_ejes/scripts/reconstruir_insumos.py --paso fasta
    python research/ola4/M5_dos_ejes/scripts/reconstruir_insumos.py --paso perfil
    python research/ola4/M5_dos_ejes/scripts/reconstruir_insumos.py --paso panel
    python research/ola4/M5_dos_ejes/scripts/reconstruir_insumos.py --paso dm
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
TRABAJO = RAIZ / "work" / "sifi_v2"
FASTA = TRABAJO / "fasta"
REF = RAIZ / "work" / "W5" / "ref"
PORT = RAIZ / "tools" / "sifi21_port"

EPILAB = ["MP_MRFV", "CP_MRFV", "BicC_Dm", "ATPaseD_Dm"]
# Los dos nuevos salen del FASTA publico de C5, que si se versiona.
NUEVOS = {"eth_Dm": "eth_Dmaidis_PZ371507", "bursA_Dm": "bursA_Dmaidis_PZ371508"}
C5 = RAIZ / "research/ola3/C5_estructura_genes_ingenieria_inversa/resultados/candidatos_c5.fa"
# Las seis referencias del panel de C7 v2 (D23 deja a *Macrosteles* afuera a proposito).
PANEL = ["GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna.fna.gz",
         "GCF_914767665.1_icHarAxyr1.1_rna.fna.gz",
         "GCF_003254395.2_Amel_HAv3.1_rna.fna.gz",
         "GCF_021130785.1_UT_GWSS_2.1_rna.fna.gz",
         "GCF_002217175.1_ASM221717v1_rna.fna.gz",
         "humano_rna.fna.gz"]
GENOMA_VECTOR = "GCA_975739785.1_ihDalMaid1.1_genomic.fna.gz"
VIRALES = ["MP_MRFV", "CP_MRFV"]
# Segundo cicadelido, SOLO para el eje de conservacion. *Macrosteles quadrilineatus*
# esta fuera del panel por D23, y el motivo que dio D23 es de exposicion («no esta en
# Argentina»), no de conservacion: la propia D23 anota que se lo habia incorporado como
# sustituto filogenetico. Entra aca como sensibilidad del eje de conservacion, NO al
# panel de exposicion ni a ningun numero de orden.
MACROSTELES = RAIZ / "work/C5/refs/Macrosteles_quadrilineatus_rna.fna"


def leer_fasta(ruta: Path) -> dict[str, str]:
    out, nombre, buf = {}, None, []
    for linea in ruta.read_text().splitlines():
        if linea.startswith(">"):
            if nombre:
                out[nombre] = "".join(buf)
            nombre, buf = linea[1:].strip().split()[0], []
        else:
            buf.append(linea.strip())
    if nombre:
        out[nombre] = "".join(buf)
    return out


def paso_fasta() -> None:
    FASTA.mkdir(parents=True, exist_ok=True)
    for g in EPILAB:
        src = RAIZ / "work" / "W5" / "fasta" / ("%s_full.fasta" % g)
        seq = "".join(leer_fasta(src).values())
        (FASTA / ("%s_full.fasta" % g)).write_text(">%s_full\n%s\n" % (g, seq))
        print("%-12s %5d nt  (insumo local, de %s)" % (g, len(seq), src.relative_to(RAIZ)))
    c5 = leer_fasta(C5)
    for g, cab in NUEVOS.items():
        seq = c5[cab]
        (FASTA / ("%s_full.fasta" % g)).write_text(">%s_full\n%s\n" % (g, seq))
        print("%-12s %5d nt  (publico, de %s)" % (g, len(seq), C5.relative_to(RAIZ)))


def paso_perfil(k: int = 21) -> None:
    sys.path.insert(0, str(PORT))
    from sifi_core import SifiEngine, to_tsv  # noqa: E402
    out = TRABAJO / ("salida_k%d" % k)
    out.mkdir(parents=True, exist_ok=True)
    for f in sorted(FASTA.glob("*_full.fasta")):
        g = f.name.replace("_full.fasta", "")
        destino = out / ("%s_full_corregido_vienna.tsv" % g)
        if destino.exists():
            print("%-12s ya estaba" % g, flush=True)
            continue
        t0 = time.time()
        seq = "".join(l.strip() for l in f.read_text().splitlines() if not l.startswith(">"))
        w, _ = SifiEngine(mode="corregido", sirna_size=k).run(seq, backend="vienna")
        to_tsv(w, destino)
        print("%-12s %5d ventanas  %4d eficientes  %5.0fs"
              % (g, len(w), sum(x.is_efficient for x in w), time.time() - t0), flush=True)


def correr_offtarget(consultas: list[Path], dbs: list[Path], salida: Path) -> None:
    cmd = [sys.executable, str(PORT / "offtarget_21nt.py"), "--size", "21", "--mm1",
           "--consulta", *[str(c) for c in consultas],
           "--db", *[str(d) for d in dbs], "--salida", str(salida)]
    print(" ".join(cmd), flush=True)
    t0 = time.time()
    subprocess.run(cmd, check=True)
    print("  %.0f s" % (time.time() - t0), flush=True)


def paso_panel() -> None:
    correr_offtarget(sorted(FASTA.glob("*_full.fasta")),
                     [REF / n for n in PANEL], TRABAJO / "offtarget_k21")


def paso_dm() -> None:
    correr_offtarget([FASTA / ("%s_full.fasta" % g) for g in VIRALES],
                     [REF / GENOMA_VECTOR], TRABAJO / "offtarget_dm_k21")


def paso_conservacion() -> None:
    correr_offtarget(sorted(FASTA.glob("*_full.fasta")), [MACROSTELES],
                     TRABAJO / "offtarget_cicadelidos_k21")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--paso", required=True, choices=("fasta", "perfil", "panel", "dm", "conservacion"))
    a = ap.parse_args()
    {"fasta": paso_fasta, "perfil": paso_perfil, "panel": paso_panel, "dm": paso_dm,
     "conservacion": paso_conservacion}[a.paso]()
    return 0


if __name__ == "__main__":
    sys.exit(main())

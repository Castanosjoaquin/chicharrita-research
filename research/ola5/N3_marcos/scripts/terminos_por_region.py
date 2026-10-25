"""N3 - Que termino cruza el corte en las tres regiones que no son de `BicC_Dm`.

El ultimo hueco que N3 dejo declarado. `N3` mide cuantas ventanas cambian de veredicto al
recortar la molecula y da sus posiciones; lo que no desagrega es **cual de los cuatro terminos
del veredicto cruzo el corte** en cada una. Para las tres regiones de `BicC_Dm` eso ya esta
medido en `M7/resultados/recorte_*_cambios.tsv`; para `MP_MRFV` 72-271, `CP_MRFV` 99-298 y
`ATPaseD_Dm` 72-371 no.

No reimplementa nada: usa `comparar_ventanas.py` de M2 --el comparador que el investigador pidio
en su carta del 22 de octubre-- exactamente como lo maneja `M7/scripts/recorte_vs_contexto.py`,
con `offset_b` en el inicio de la region, de modo que las 20 ultimas posiciones de arranque, que
el gen tiene y la molecula no, se informan como `solo_contexto` y no entran a la matriz.

Dos efectos conocidos se esperan y conviene no confundirlos, como dice M7: el **borde de
plegado**, que cambia la accesibilidad en todo el perfil porque la molecula recortada no tiene
el contexto que estabilizaba los extremos, y el **borde de dG**, que afecta solo a las dos
primeras posiciones del recorte, donde el original calcula los extremos sin nucleotidos
colgantes porque el siRNA de dos posiciones antes no existe.

Las anclas son los conteos de `N3`: el comparador tiene que dar el marco 2 del lado del contexto
y el marco 3 del lado del recorte, y la cantidad de cambios tiene que ser la suma de las que
ganan y las que pierden. Aborta si alguna falla.

Los FASTA de los recortes y los TSV por ventana se escriben **fuera del repositorio**: son
secuencia del gen y columnas de 21-meros solapados.

Uso (desde la raiz del repositorio):
    python research/ola5/N3_marcos/scripts/terminos_por_region.py [--trabajo DIR]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve()
RAIZ = AQUI.parents[4]
SALIDA = AQUI.parents[1] / "resultados"
sys.path.insert(0, str(RAIZ / "research" / "ola4" / "M2_ventana_a_ventana" / "scripts"))
sys.path.insert(0, str(AQUI.parent))

from comparar_ventanas import comparar, escribir, leer  # noqa: E402
from tres_marcos import FASTA, K, leer_fasta  # noqa: E402

PORT = RAIZ / "tools" / "sifi21_port" / "run_sifi.py"
MODOS = ["corregido", "fiel"]

#: Las tres regiones vigentes que `M7` no cubrio, con su nombre de archivo.
REGIONES = [("MP_MRFV", 72, 271), ("CP_MRFV", 99, 298), ("ATPaseD_Dm", 72, 371)]

#: Anclas de N3, modo `corregido`: (marco 2, marco 3, pierden, ganan).
ANCLA_N3 = {"MP_MRFV": (31, 27, 5, 1), "CP_MRFV": (20, 23, 3, 6),
            "ATPaseD_Dm": (17, 20, 1, 4)}


def correr(fasta: Path, modo: str, destino: Path) -> None:
    destino.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, str(PORT), str(fasta), "--modo", modo,
                    "--backend", "vienna", "--salida", str(destino)],
                   check=True, capture_output=True, text=True)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--trabajo", default=None,
                    help="carpeta fuera del repositorio para los FASTA y TSV intermedios")
    a = ap.parse_args(argv)

    faltan = [g for g, _, _ in REGIONES if not FASTA[g].exists()]
    if faltan:
        raise SystemExit("faltan los FASTA de %s en work/sifi_check/; `work/` no esta en git"
                         % ", ".join(faltan))

    trabajo = Path(a.trabajo) if a.trabajo else Path(tempfile.mkdtemp(prefix="n3_terminos_"))
    trabajo.mkdir(parents=True, exist_ok=True)
    SALIDA.mkdir(parents=True, exist_ok=True)

    recortes = {}
    for gen, ini, fin in REGIONES:
        seq = leer_fasta(FASTA[gen])
        nombre = "%s_%d_%d" % (gen, ini, fin)
        f = trabajo / ("%s.fa" % nombre)
        f.write_text(">%s\n%s\n" % (nombre, seq[ini - 1:fin]), encoding="utf-8")
        recortes[gen] = (f, nombre)

    resumen = {"motor": "ViennaRNA 2.7.2, tabla NN3, punto por defecto",
               "fuente_del_comparador":
                   "research/ola4/M2_ventana_a_ventana/scripts/comparar_ventanas.py",
               "anclas_n3": {k: list(v) for k, v in ANCLA_N3.items()},
               "pares": {}}
    roto = []
    for modo in MODOS:
        for gen, ini, fin in REGIONES:
            dir_gen = trabajo / ("gen_%s_%s" % (gen, modo))
            correr(FASTA[gen], modo, dir_gen)
            tsv_gen = dir_gen / ("%s_full_%s_vienna.tsv" % (gen, modo))
            f, nombre = recortes[gen]
            dir_rec = trabajo / ("rec_%s_%s" % (nombre, modo))
            correr(f, modo, dir_rec)
            tsv_rec = dir_rec / ("%s_%s_vienna.tsv" % (nombre, modo))

            res, cambios = comparar(leer(tsv_gen), leer(tsv_rec), offset_b=ini,
                                    etiquetas=("contexto", "recorte"))
            prefijo = SALIDA / ("terminos_%s_%s" % (nombre, modo))
            escribir(prefijo, res, cambios)

            pierden = sum(1 for c in cambios if c["contexto"] and not c["recorte"])
            ganan = sum(1 for c in cambios if c["recorte"] and not c["contexto"])
            bordes = [c for c in cambios if c["pos_recorte"] in (1, 2)]
            res["pierden"] = pierden
            res["ganan"] = ganan
            res["cambios_en_las_dos_primeras_posiciones"] = len(bordes)
            resumen["pares"]["%s %d-%d/%s" % (gen, ini, fin, modo)] = res

            if modo == "corregido":
                esp = ANCLA_N3[gen]
                obt = (res["eficientes_contexto"], res["eficientes_recorte"],
                       pierden, ganan)
                if obt != esp:
                    roto.append("%s %d-%d: %s, N3 publico %s" % (gen, ini, fin, obt, esp))

            print("%-12s %-10s %-10s contexto %3d  recorte %3d  cambian %2d "
                  "(pierden %d, ganan %d; en las dos primeras: %d)  terminos: %s"
                  % (gen, "%d-%d" % (ini, fin), modo, res["eficientes_contexto"],
                     res["eficientes_recorte"], res["cambian"], pierden, ganan,
                     len(bordes), ",".join(res["terminos"]) or "-"), flush=True)

    if roto:
        raise SystemExit("anclas de N3 rotas:\n  " + "\n  ".join(roto))

    # El recuento por termino, que es lo que esta linea venia a producir.
    por_termino: dict[str, dict[str, int]] = {}
    for clave, res in resumen["pares"].items():
        modo = clave.split("/")[-1]
        for t in res["terminos"]:
            por_termino.setdefault(modo, {}).setdefault(t, 0)
    for modo in MODOS:
        for gen, ini, fin in REGIONES:
            nombre = "%s_%d_%d" % (gen, ini, fin)
            tsv = SALIDA / ("terminos_%s_%s_cambios.tsv" % (nombre, modo))
            if not tsv.exists():
                continue
            import csv
            with open(tsv, newline="", encoding="utf-8") as fh:
                for fila in csv.DictReader(fh, delimiter="\t"):
                    for t in (fila.get("terminos_que_cruzan") or "").split(","):
                        if t:
                            d = por_termino.setdefault(modo, {})
                            d[t] = d.get(t, 0) + 1
    resumen["ventanas_por_termino"] = por_termino

    (SALIDA / "terminos_por_region.json").write_text(
        json.dumps(resumen, ensure_ascii=False, indent=1), encoding="utf-8")

    print("\nVentanas que cambian, por termino que cruzo el corte:")
    for modo, d in por_termino.items():
        print("  %-10s %s" % (modo, d or "ninguna"))
    print("\nlas anclas de N3 se reprodujeron en los tres pares del modo corregido")
    print("FASTA y TSV intermedios en %s (fuera del repositorio)" % trabajo)
    print("resultados en %s" % SALIDA)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

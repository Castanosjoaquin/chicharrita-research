"""Quimeras de a dos con las cuatro regiones de EPILAB: eficiencia y empalme.

Qué contesta (Q3 de C4): si se pegan dos regiones de genes distintos, ¿la
eficiencia total es la suma de las partes salvo en la unión, como dijo el
investigador en el Checkpoint 1?

Qué hace, y qué NO hace:
  - Arma las 12 quimeras ordenadas (4x3) concatenando las regiones elegidas.
  - Llama a `tools/sifi21_port/run_sifi.py` por línea de comandos, SIN modificarlo,
    sobre las 4 regiones sueltas y las 12 quimeras.
  - Compara, ventana por ventana, el veredicto de la quimera contra el de la
    región de origen, y separa tres clases de ventana:
      * heredada   la ventana existe igual en una de las dos regiones;
      * empalme    los 20 lugares que quedan a caballo de la unión: secuencia nueva;
      * (dentro de las heredadas) las que cambiaron de veredicto, con su distancia
        a la unión, que es lo que mide si el efecto de contexto se limita o no al
        empalme.
  - No toca el motor de si-Fi21 ni reimplementa su criterio.

Uso:
    python research/ola3/C4_offtargets_quimeras_largo/scripts/quimeras_sifi.py \
        --modo fiel --backend vienna
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]          # raíz del repositorio
FASTA = RAIZ / "work/C4/fasta"
SALIDA_TRABAJO = RAIZ / "work/C4"
RESULTADOS = Path(__file__).resolve().parents[1] / "resultados"
REGIONES = ["MP_MRFV", "CP_MRFV", "BicC_Dm", "ATPaseD_Dm"]
VENTANA = 21


def leer_fasta_simple(ruta: Path) -> str:
    return "".join(l.strip() for l in ruta.read_text().splitlines()
                   if not l.startswith(">"))


def escribir_fasta(ruta: Path, registros):
    with open(ruta, "w", encoding="utf-8") as fh:
        for nombre, seq in registros:
            fh.write(">%s\n" % nombre)
            for i in range(0, len(seq), 60):
                fh.write(seq[i:i + 60] + "\n")


def leer_tsv(ruta: Path):
    with open(ruta, encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def es_eficiente(fila) -> bool:
    v = fila.get("is_efficient", "")
    return str(v).strip().lower() in ("true", "1", "yes")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--modo", choices=("fiel", "corregido"), default="fiel")
    ap.add_argument("--backend", choices=("exe", "vienna"), default="vienna")
    a = ap.parse_args(argv)

    dir_q = SALIDA_TRABAJO / "quimeras"
    dir_q.mkdir(parents=True, exist_ok=True)
    dir_sifi = SALIDA_TRABAJO / "sifi" / ("%s_%s" % (a.modo, a.backend))
    dir_sifi.mkdir(parents=True, exist_ok=True)
    RESULTADOS.mkdir(parents=True, exist_ok=True)

    regiones = {g: leer_fasta_simple(FASTA / ("%s_sel.fasta" % g)) for g in REGIONES}
    for g, s in regiones.items():
        print("region %-12s %4d nt" % (g, len(s)))

    # --- las 12 quimeras ordenadas -------------------------------------------
    quimeras = {}
    for a1, b1 in itertools.permutations(REGIONES, 2):
        nombre = "Q_%s__%s" % (a1, b1)
        quimeras[nombre] = {"izq": a1, "der": b1,
                            "seq": regiones[a1] + regiones[b1],
                            "corte": len(regiones[a1])}
    escribir_fasta(dir_q / "quimeras.fasta",
                   [(n, d["seq"]) for n, d in quimeras.items()])
    escribir_fasta(dir_q / "regiones.fasta",
                   [("%s_sel" % g, s) for g, s in regiones.items()])
    print("escritas %d quimeras en %s" % (len(quimeras), dir_q / "quimeras.fasta"))

    # --- si-Fi21 portado, por línea de comandos, sin modificarlo --------------
    cmd = [sys.executable, str(RAIZ / "tools/sifi21_port/run_sifi.py"),
           str(dir_q / "regiones.fasta"), str(dir_q / "quimeras.fasta"),
           "--modo", a.modo, "--backend", a.backend,
           "--salida", str(dir_sifi)]
    print("\n$ " + " ".join(cmd) + "\n", flush=True)
    r = subprocess.run(cmd, cwd=str(RAIZ), text=True, capture_output=True)
    (SALIDA_TRABAJO / "logs").mkdir(parents=True, exist_ok=True)
    (SALIDA_TRABAJO / "logs" / ("run_sifi_%s_%s.log" % (a.modo, a.backend))).write_text(
        r.stdout + "\n--- stderr ---\n" + r.stderr, encoding="utf-8")
    if r.returncode != 0:
        print(r.stdout[-3000:]); print(r.stderr[-3000:])
        raise SystemExit("run_sifi.py falló con código %d" % r.returncode)
    print(r.stdout[-1500:])

    def tsv_de(nombre):
        return dir_sifi / ("%s_%s_%s.tsv" % (nombre, a.modo, a.backend))

    perfil = {}
    for g in REGIONES:
        filas = leer_tsv(tsv_de("%s_sel" % g))
        perfil[g] = {int(f["pos"]): es_eficiente(f) for f in filas}
    for n in quimeras:
        filas = leer_tsv(tsv_de(n))
        quimeras[n]["perfil"] = {int(f["pos"]): es_eficiente(f) for f in filas}

    # --- comparación ----------------------------------------------------------
    filas_out, detalle_flip = [], []
    for n, d in quimeras.items():
        izq, der, corte = d["izq"], d["der"], d["corte"]
        p_izq, p_der, p_q = perfil[izq], perfil[der], d["perfil"]
        n_izq = sum(p_izq.values())
        n_der = sum(p_der.values())

        heredadas_izq = [p for p in p_q if p <= corte - VENTANA + 1]
        empalme = [p for p in p_q if corte - VENTANA + 1 < p <= corte]
        heredadas_der = [p for p in p_q if p > corte]

        ef_h_izq = sum(1 for p in heredadas_izq if p_q[p])
        ef_emp = sum(1 for p in empalme if p_q[p])
        ef_h_der = sum(1 for p in heredadas_der if p_q[p])

        # ventanas heredadas que cambiaron de veredicto respecto de su región
        flips = []
        for p in heredadas_izq:
            if p_q[p] != p_izq.get(p):
                flips.append((p, "izq", p_izq.get(p), p_q[p], corte - 20 - p))
        for p in heredadas_der:
            po = p - corte
            if p_q[p] != p_der.get(po):
                flips.append((p, "der", p_der.get(po), p_q[p], p - corte - 1))
        for p, lado, antes, ahora, dist in flips:
            detalle_flip.append({"quimera": n, "pos_quimera": p, "lado": lado,
                                 "antes": antes, "ahora": ahora,
                                 "nt_hasta_la_union": dist})

        filas_out.append({
            "quimera": n, "izquierda": izq, "derecha": der,
            "largo_nt": len(d["seq"]), "corte_nt": corte,
            "ventanas_quimera": len(p_q),
            "ef_region_izq": n_izq, "ef_region_der": n_der,
            "suma_de_partes": n_izq + n_der,
            "ef_quimera_total": sum(p_q.values()),
            "ef_heredadas_izq": ef_h_izq, "ef_heredadas_der": ef_h_der,
            "ventanas_empalme": len(empalme), "ef_empalme": ef_emp,
            "delta_total_menos_suma": sum(p_q.values()) - (n_izq + n_der),
            "delta_explicado_por_empalme": ef_emp,
            "ventanas_heredadas_que_cambiaron": len(flips),
        })

    suf = "%s_%s" % (a.modo, a.backend)
    cols = list(filas_out[0].keys())
    with open(RESULTADOS / ("quimeras_eficiencia_%s.tsv" % suf), "w", encoding="utf-8",
              newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t")
        w.writeheader()
        w.writerows(filas_out)
    with open(RESULTADOS / ("quimeras_ventanas_cambiadas_%s.tsv" % suf), "w",
              encoding="utf-8", newline="") as fh:
        if detalle_flip:
            w = csv.DictWriter(fh, fieldnames=list(detalle_flip[0].keys()),
                               delimiter="\t")
            w.writeheader(); w.writerows(detalle_flip)
        else:
            fh.write("sin_cambios\n")

    (RESULTADOS / ("quimeras_meta_%s.json" % suf)).write_text(json.dumps({
        "modo": a.modo, "backend": a.backend,
        "regiones": {g: len(s) for g, s in regiones.items()},
        "eficientes_region_suelta": {g: sum(perfil[g].values()) for g in REGIONES},
        "n_quimeras": len(quimeras),
        "comando_run_sifi": " ".join(cmd),
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n%-26s %5s %5s %6s %6s %6s %7s %6s" % (
        "quimera", "largo", "suma", "total", "delta", "empal", "ef_emp", "flips"))
    for f in filas_out:
        print("%-26s %5d %5d %6d %6d %6d %7d %6d" % (
            f["quimera"], f["largo_nt"], f["suma_de_partes"], f["ef_quimera_total"],
            f["delta_total_menos_suma"], f["ventanas_empalme"], f["ef_empalme"],
            f["ventanas_heredadas_que_cambiaron"]))
    print("\nescrito en %s" % RESULTADOS)
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Quimeras de a dos con las regiones que recomienda C7, no con las de EPILAB.

Por que existe este script, habiendo uno en C4. C4 contesto la pregunta del
Checkpoint 1 --si la eficiencia de una quimera es la suma de las partes salvo en la
union-- y para eso concateno las cuatro regiones **tal como las eligio EPILAB**
(`MP_MRFV` 1-200, `CP_MRFV` 201-400, `BicC_Dm` 264-563, `ATPaseD_Dm` 151-450).
Despues de eso, C7 movio las cuatro regiones a la mejor que encuentra la cascada
(`MP_MRFV` 72-271, `CP_MRFV` 99-298, `BicC_Dm` 2121-2420, `ATPaseD_Dm` 72-371), y
esas son las regiones que el entregable recomienda. Una quimera armada con las
regiones nuevas **no es la misma molecula**: el empalme es secuencia distinta, asi
que las 20 ventanas nuevas y la banda de contexto de ~60 nt a cada lado hay que
volver a calcularlas. Eso es lo que corre aca.

Que hace, y que NO hace:
  - Recorta las regiones del gen completo (work/sifi_check/<gen>_full.fasta) con
    las coordenadas del conjunto pedido, 1-based inclusive.
  - Arma las 12 quimeras ordenadas (4x3) y las escribe en FASTA.
  - Llama a tools/sifi21_port/run_sifi.py por linea de comandos, SIN modificarlo,
    sobre las 4 regiones sueltas y las 12 quimeras.
  - Clasifica cada ventana de la quimera en heredada / de empalme, y marca las
    heredadas que cambiaron de veredicto, con su distancia a la union. La
    contabilidad es la misma de C4 (scripts/quimeras_sifi.py), a proposito: con
    --conjunto epilab este script tiene que reproducir la tabla de C4 fila por
    fila, y lo verifica solo. Si no la reproduce, aborta.
  - No toca el motor de si-Fi21 ni reimplementa su criterio.

Uso:
    python research/ola3/C13_quimeras_region_recomendada/scripts/quimeras_v2.py \
        --conjunto epilab       --modo fiel --backend vienna   # verificacion
    python research/ola3/C13_quimeras_region_recomendada/scripts/quimeras_v2.py \
        --conjunto recomendadas --modo fiel --backend vienna   # lo nuevo
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
BLOQUE = Path(__file__).resolve().parents[1]
RESULTADOS = BLOQUE / "resultados"
SALIDA_TRABAJO = RAIZ / "work/C13"
FULL = RAIZ / "work/sifi_check"
VENTANA = 21

REGIONES = ["MP_MRFV", "CP_MRFV", "BicC_Dm", "ATPaseD_Dm"]

# Coordenadas 1-based inclusive sobre el gen completo. Las de EPILAB estan
# verificadas contra work/sifi_check/<gen>_sel.fasta: el recorte coincide base por
# base con el archivo que uso W5. Las recomendadas son las del nivel 3 de C7
# (research/ola3/C7_ranking_v2/REPORT.md seccion 4).
CONJUNTOS = {
    "epilab": {"MP_MRFV": (1, 200), "CP_MRFV": (201, 400),
               "BicC_Dm": (264, 563), "ATPaseD_Dm": (151, 450)},
    "recomendadas": {"MP_MRFV": (72, 271), "CP_MRFV": (99, 298),
                     "BicC_Dm": (2121, 2420), "ATPaseD_Dm": (72, 371)},
    # Las vigentes al 2026-10-22: iguales a las de C7 salvo `BicC_Dm`, que D25 movio
    # de 2121-2420 a 922-1221 por conservacion (C8). Es el conjunto que recomienda
    # `entregables/para-el-investigador.md`, y por lo tanto el que hay que concatenar
    # si la quimera se arma con lo que el equipo recomienda hoy.
    "vigentes": {"MP_MRFV": (72, 271), "CP_MRFV": (99, 298),
                 "BicC_Dm": (922, 1221), "ATPaseD_Dm": (72, 371)},
}
# Tablas de C4 contra las que se verifica el conjunto epilab, una por modo.
DIR_C4 = RAIZ / "research/ola3/C4_offtargets_quimeras_largo/resultados"


def tabla_c4(modo: str, backend: str) -> Path:
    return DIR_C4 / ("quimeras_eficiencia_%s_%s.tsv" % (modo, backend))


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
    return str(fila.get("is_efficient", "")).strip().lower() in ("true", "1", "yes")


def recortar(conjunto: str) -> dict:
    """Recorta las cuatro regiones del gen completo y, si se puede, se autocontrola."""
    coords = CONJUNTOS[conjunto]
    regiones = {}
    for g, (a, b) in coords.items():
        full = leer_fasta_simple(FULL / ("%s_full.fasta" % g))
        if b > len(full):
            raise SystemExit("%s: la region %d-%d no cabe en %d nt" % (g, a, b, len(full)))
        regiones[g] = full[a - 1:b]
        sel = FULL / ("%s_sel.fasta" % g)
        if conjunto == "epilab" and sel.exists():
            if regiones[g] != leer_fasta_simple(sel):
                raise SystemExit("%s: el recorte %d-%d no coincide con %s" % (g, a, b, sel))
    return regiones


def verificar_contra_c4(filas_out, modo: str, backend: str):
    """El conjunto epilab tiene que dar la misma tabla que C4, fila por fila."""
    ruta = tabla_c4(modo, backend)
    if not ruta.exists():
        print("AVISO: no esta %s; no se pudo verificar contra C4" % ruta)
        return
    c4 = {f["quimera"]: f for f in leer_tsv(ruta)}
    cols = [c for c in filas_out[0] if c in next(iter(c4.values()))]
    malas = []
    for f in filas_out:
        v = c4.get(f["quimera"])
        if v is None:
            malas.append((f["quimera"], "no esta en C4", "", ""))
            continue
        for c in cols:
            if str(f[c]) != str(v[c]):
                malas.append((f["quimera"], c, v[c], f[c]))
    if malas:
        for q, c, esperado, obtenido in malas:
            print("  DISTINTO %-26s %-32s C4=%s  aca=%s" % (q, c, esperado, obtenido))
        raise SystemExit("no reproduce la tabla de C4 en %d celdas" % len(malas))
    print("VERIFICACION: reproduce la tabla de C4 en %d filas x %d columnas"
          % (len(filas_out), len(cols)))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--conjunto", choices=tuple(CONJUNTOS), default="recomendadas")
    ap.add_argument("--modo", choices=("fiel", "corregido"), default="fiel")
    ap.add_argument("--backend", choices=("exe", "vienna"), default="vienna")
    a = ap.parse_args(argv)
    suf = "%s_%s_%s" % (a.conjunto, a.modo, a.backend)

    dir_q = SALIDA_TRABAJO / "fasta" / a.conjunto
    dir_q.mkdir(parents=True, exist_ok=True)
    dir_sifi = SALIDA_TRABAJO / "sifi" / suf
    dir_sifi.mkdir(parents=True, exist_ok=True)
    RESULTADOS.mkdir(parents=True, exist_ok=True)

    regiones = recortar(a.conjunto)
    for g in REGIONES:
        a1, b1 = CONJUNTOS[a.conjunto][g]
        print("region %-12s %d-%d  %4d nt" % (g, a1, b1, len(regiones[g])))

    quimeras = {}
    for izq, der in itertools.permutations(REGIONES, 2):
        quimeras["Q_%s__%s" % (izq, der)] = {
            "izq": izq, "der": der,
            "seq": regiones[izq] + regiones[der], "corte": len(regiones[izq])}
    escribir_fasta(dir_q / "quimeras.fasta",
                   [(n, d["seq"]) for n, d in quimeras.items()])
    escribir_fasta(dir_q / "regiones.fasta",
                   [("%s_sel" % g, regiones[g]) for g in REGIONES])
    print("escritas %d quimeras en %s" % (len(quimeras), dir_q / "quimeras.fasta"))

    cmd = [sys.executable, str(RAIZ / "tools/sifi21_port/run_sifi.py"),
           str(dir_q / "regiones.fasta"), str(dir_q / "quimeras.fasta"),
           "--modo", a.modo, "--backend", a.backend, "--salida", str(dir_sifi)]
    print("\n$ " + " ".join(cmd) + "\n", flush=True)
    r = subprocess.run(cmd, cwd=str(RAIZ), text=True, capture_output=True)
    (SALIDA_TRABAJO / "logs").mkdir(parents=True, exist_ok=True)
    (SALIDA_TRABAJO / "logs" / ("run_sifi_%s.log" % suf)).write_text(
        r.stdout + "\n--- stderr ---\n" + r.stderr, encoding="utf-8")
    if r.returncode != 0:
        print(r.stdout[-3000:]); print(r.stderr[-3000:])
        raise SystemExit("run_sifi.py fallo con codigo %d" % r.returncode)
    print(r.stdout[-800:])

    def tsv_de(nombre):
        return dir_sifi / ("%s_%s_%s.tsv" % (nombre, a.modo, a.backend))

    perfil = {g: {int(f["pos"]): es_eficiente(f)
                  for f in leer_tsv(tsv_de("%s_sel" % g))} for g in REGIONES}
    for n in quimeras:
        quimeras[n]["perfil"] = {int(f["pos"]): es_eficiente(f)
                                 for f in leer_tsv(tsv_de(n))}

    filas_out, detalle_flip = [], []
    for n, d in quimeras.items():
        izq, der, corte = d["izq"], d["der"], d["corte"]
        p_izq, p_der, p_q = perfil[izq], perfil[der], d["perfil"]
        n_izq, n_der = sum(p_izq.values()), sum(p_der.values())

        heredadas_izq = [p for p in p_q if p <= corte - VENTANA + 1]
        empalme = [p for p in p_q if corte - VENTANA + 1 < p <= corte]
        heredadas_der = [p for p in p_q if p > corte]

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

        ef_emp = sum(1 for p in empalme if p_q[p])
        filas_out.append({
            "quimera": n, "izquierda": izq, "derecha": der,
            "largo_nt": len(d["seq"]), "corte_nt": corte,
            "ventanas_quimera": len(p_q),
            "ef_region_izq": n_izq, "ef_region_der": n_der,
            "suma_de_partes": n_izq + n_der,
            "ef_quimera_total": sum(p_q.values()),
            "ef_heredadas_izq": sum(1 for p in heredadas_izq if p_q[p]),
            "ef_heredadas_der": sum(1 for p in heredadas_der if p_q[p]),
            "ventanas_empalme": len(empalme), "ef_empalme": ef_emp,
            "delta_total_menos_suma": sum(p_q.values()) - (n_izq + n_der),
            "delta_explicado_por_empalme": ef_emp,
            "ventanas_heredadas_que_cambiaron": len(flips),
        })

    with open(RESULTADOS / ("quimeras_eficiencia_%s.tsv" % suf), "w",
              encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas_out[0].keys()), delimiter="\t")
        w.writeheader(); w.writerows(filas_out)
    with open(RESULTADOS / ("quimeras_ventanas_cambiadas_%s.tsv" % suf), "w",
              encoding="utf-8", newline="") as fh:
        if detalle_flip:
            w = csv.DictWriter(fh, fieldnames=list(detalle_flip[0].keys()),
                               delimiter="\t")
            w.writeheader(); w.writerows(detalle_flip)
        else:
            fh.write("sin_cambios\n")
    (RESULTADOS / ("quimeras_meta_%s.json" % suf)).write_text(json.dumps({
        "conjunto": a.conjunto, "coordenadas": CONJUNTOS[a.conjunto],
        "modo": a.modo, "backend": a.backend,
        "regiones": {g: len(s) for g, s in regiones.items()},
        "eficientes_region_suelta": {g: sum(perfil[g].values()) for g in REGIONES},
        "n_quimeras": len(quimeras), "comando_run_sifi": " ".join(cmd),
        "python": sys.version.split()[0],
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n%-26s %5s %5s %6s %6s %6s %7s %6s" % (
        "quimera", "largo", "suma", "total", "delta", "empal", "ef_emp", "flips"))
    for f in sorted(filas_out, key=lambda x: -x["delta_total_menos_suma"]):
        print("%-26s %5d %5d %6d %6d %6d %7d %6d" % (
            f["quimera"], f["largo_nt"], f["suma_de_partes"], f["ef_quimera_total"],
            f["delta_total_menos_suma"], f["ventanas_empalme"], f["ef_empalme"],
            f["ventanas_heredadas_que_cambiaron"]))
    if a.conjunto == "epilab":
        print()
        verificar_contra_c4(filas_out, a.modo, a.backend)
    print("\nescrito en %s" % RESULTADOS)
    return 0


if __name__ == "__main__":
    sys.exit(main())

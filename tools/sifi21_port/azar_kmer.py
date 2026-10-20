"""Cuanto de los off-targets que aparecen al acortar la ventana lo explica el azar.

El investigador lo pidio explicito en el checkpoint: hacer la cuenta de probabilidad
para 18, 19 y 20 nt y compararla con lo que devuelve el programa, porque es el
soporte de su argumento de que **la biologia no es random** —«no vas a encontrar lo
que te dice la estadistica que deberias encontrar por azar»—. Tenemos el lado
observado y faltaba el esperado.

Se compara observado contra esperado bajo tres nulos, y el orden importa porque cada
uno le quita al anterior una explicacion:

1. **Uniforme**, 1/4^k por posicion. Es «lo que dice la estadistica» en su version
   mas cruda: las cuatro bases equiprobables e independientes.
2. **Ajustado por composicion** de cada referencia. Las bases no son equiprobables
   —un genoma con 60 % de AT hace mucho mas probable un k-mero rico en AT— asi que
   este es el nulo honesto minimo: sigue suponiendo independencia entre posiciones,
   pero ya no equiprobabilidad.
3. **Empirico por barajado** de la referencia, preservando la composicion de
   mononucleotidos. Conserva exactamente la composicion y destruye toda la
   estructura: repeticiones, familias de genes, baja complejidad, sesgo de codones.
   Lo que quede de diferencia entre este nulo y lo observado es estructura, y es el
   efecto que el investigador describio.

Para los tres, la cantidad reportada es la misma que cuenta `offtarget_21nt.py`:
**cuantas ventanas de la consulta tienen al menos un acierto exacto** en la
referencia, en las dos hebras. No el numero de aciertos, que es otra cosa y no es la
que se usa para descartar una ventana.

Todo local, en una sola pasada por base de cada referencia y de su version barajada.
Nada sale de la maquina.

Uso:
    python azar_kmer.py --consulta work/sifi_check/*_full.fasta \\
        --db work/offtarget_db/*.fna.gz --k 15 16 17 18 19 20 21 \\
        --salida research/ola2/W7_ranking/azar_por_k.json
"""

from __future__ import annotations

import argparse
import glob
import gzip
import json
import math
import sys
from pathlib import Path

import ahocorasick
import numpy as np

COMP = str.maketrans("ACGT", "TGCA")
BASES = "ACGT"


def rc(s: str) -> str:
    return s.translate(COMP)[::-1]


def leer_fasta(ruta):
    nombre, buf = None, []
    for linea in Path(ruta).read_text().splitlines():
        if linea.startswith(">"):
            if nombre is not None:
                yield nombre, "".join(buf)
            nombre, buf = linea[1:].strip().split()[0], []
        else:
            buf.append(linea.strip())
    if nombre is not None:
        yield nombre, "".join(buf)


def iter_db(ruta):
    abrir = gzip.open if str(ruta).endswith(".gz") else open
    nombre, buf = None, []
    with abrir(ruta, "rt") as fh:
        for linea in fh:
            if linea.startswith(">"):
                if nombre is not None:
                    yield nombre, "".join(buf)
                nombre, buf = linea[1:].strip().split()[0], []
            else:
                buf.append(linea.strip().upper())
    if nombre is not None:
        yield nombre, "".join(buf)


def ventanas_consulta(consultas, ks):
    """{k: [(gen, pos, kmero)]} de todas las ventanas de todos los genes."""
    out = {k: [] for k in ks}
    for ruta in consultas:
        for nombre, seq in leer_fasta(ruta):
            seq = seq.upper().replace("U", "T")
            for k in ks:
                for i in range(len(seq) - k + 1):
                    w = seq[i:i + k]
                    if all(b in BASES for b in w):
                        out[k].append((nombre, i + 1, w))
    return out


def construir(vent):
    """Un solo automata con los k-meros de todos los k, para una pasada por base."""
    aut = ahocorasick.Automaton()
    indice = {}
    for k, filas in vent.items():
        for j, (_gen, _pos, w) in enumerate(filas):
            indice[(k, j)] = w
            for p in (w, rc(w)):
                if aut.exists(p):
                    if (k, j) not in aut.get(p):
                        aut.get(p).append((k, j))
                else:
                    aut.add_word(p, [(k, j)])
    aut.make_automaton()
    return aut


def barajar(seq: str, rng) -> str:
    """Baraja las bases de la secuencia. Preserva la composicion exacta, incluidas
    las N, de modo que el numero de posiciones de la referencia no cambia."""
    a = np.frombuffer(seq.encode("ascii"), dtype=np.uint8).copy()
    rng.shuffle(a)
    return a.tobytes().decode("ascii")


def escanear(aut, seqs) -> set[tuple[int, int]]:
    """Pasada por una referencia. Devuelve el conjunto de (k, j) con al menos un
    acierto. Se corta la acumulacion por ventana: solo interesa «hubo o no».

    `seqs` es un iterable perezoso a proposito: con el genoma de *D. maidis*
    —972 Mb— tener a la vez la referencia y su version barajada en memoria no entra
    comodo, asi que se lee de disco una vez por pasada y nunca se retiene todo.
    """
    vistos: set[tuple[int, int]] = set()
    for seq in seqs:
        if not seq:
            continue
        for _, cargas in aut.iter(seq):
            vistos.update(cargas)
    return vistos


def resumir_referencia(ruta, ks) -> tuple[dict[str, float], int, dict[int, int]]:
    """Una pasada que no retiene nada: composicion, bases y posiciones por k."""
    cuenta = {b: 0 for b in BASES}
    total = 0
    pos = {k: 0 for k in ks}
    for _n, seq in iter_db(ruta):
        a = np.frombuffer(seq.encode("ascii"), dtype=np.uint8)
        total += len(a)
        for b in BASES:
            cuenta[b] += int((a == ord(b)).sum())
        for k in ks:
            pos[k] += max(0, len(a) - k + 1)
    n = sum(cuenta.values())
    frec = {b: cuenta[b] / n for b in BASES} if n else {b: 0.25 for b in BASES}
    return frec, total, pos


def esperado_uniforme(n_ventanas: int, posiciones: int, k: int) -> float:
    """Ventanas con al menos un acierto si las cuatro bases fueran equiprobables.

    Cada una de las `posiciones` de la referencia coincide con probabilidad 4^-k, y
    se mira en las dos hebras, de ahi el factor 2. P(al menos uno) = 1 - exp(-lambda)
    con lambda = 2 * posiciones * 4^-k; la aproximacion de Poisson es buena porque
    4^-k es diminuto y el numero de pruebas es enorme.
    """
    lam = 2.0 * posiciones * (0.25 ** k)
    return n_ventanas * (1.0 - math.exp(-lam))


def esperado_composicion(kmeros, posiciones: int, frec: dict[str, float]) -> float:
    """Igual, pero con la probabilidad de CADA k-mero segun la composicion.

    Sigue suponiendo independencia entre posiciones del k-mero: lo unico que cambia
    respecto del uniforme es que las bases dejan de ser equiprobables. Las dos hebras
    entran con su propia probabilidad, porque p(w) y p(rc(w)) no son iguales cuando
    f(A) != f(T).
    """
    total = 0.0
    for w in kmeros:
        p = 1.0
        q = 1.0
        for b in w:
            p *= frec[b]
        for b in rc(w):
            q *= frec[b]
        total += 1.0 - math.exp(-posiciones * (p + q))
    return total


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--consulta", nargs="+", required=True)
    ap.add_argument("--db", nargs="+", required=True)
    ap.add_argument("--k", nargs="+", type=int, default=[18, 19, 20, 21])
    ap.add_argument("--semilla", type=int, default=7)
    ap.add_argument("--salida", default=None)
    a = ap.parse_args(argv)

    dbs = []
    for patron in a.db:
        dbs.extend(sorted(glob.glob(patron)) or [patron])
    ks = sorted(a.k)
    rng = np.random.default_rng(a.semilla)

    print("ventanas de consulta por k ...", flush=True)
    vent = ventanas_consulta(a.consulta, ks)
    for k in ks:
        print("  k=%-3d %d ventanas" % (k, len(vent[k])), flush=True)
    genes = sorted({g for k in ks for g, _, _ in vent[k]})

    print("construyendo automata (todos los k en una pasada) ...", flush=True)
    aut = construir(vent)
    print("  %d patrones" % len(aut), flush=True)

    filas = []
    for ruta in dbs:
        base = Path(ruta).name.replace(".fna.gz", "").replace(".fasta", "")
        print("\n%s" % base, flush=True)
        frec, bases_totales, posiciones = resumir_referencia(ruta, ks)
        print("  %d bases, composicion A %.3f C %.3f G %.3f T %.3f"
              % (bases_totales, frec["A"], frec["C"], frec["G"], frec["T"]), flush=True)

        print("  observado ...", flush=True)
        obs = escanear(aut, (s for _n, s in iter_db(ruta)))
        print("  barajando y escaneando el nulo ...", flush=True)
        nulo = escanear(aut, (barajar(s, rng) for _n, s in iter_db(ruta)))

        for k in ks:
            pos_k = posiciones[k]
            for gen in genes:
                idx = [j for j, (g, _p, _w) in enumerate(vent[k]) if g == gen]
                if not idx:
                    continue
                n_v = len(idx)
                o = sum(1 for j in idx if (k, j) in obs)
                u = sum(1 for j in idx if (k, j) in nulo)
                e_uni = esperado_uniforme(n_v, pos_k, k)
                e_comp = esperado_composicion(
                    [vent[k][j][2] for j in idx], pos_k, frec)
                filas.append({
                    "referencia": base, "gen": gen, "k": k, "ventanas": n_v,
                    "posiciones_referencia": pos_k,
                    "observado": o,
                    "esperado_uniforme": round(e_uni, 2),
                    "esperado_composicion": round(e_comp, 2),
                    "nulo_barajado": u,
                    "composicion": {b: round(frec[b], 4) for b in BASES},
                })
        del obs, nulo

    print("\n%-46s%4s%7s%9s%11s%11s%9s" % (
        "referencia", "k", "vent", "observado", "unif", "composic", "barajado"))
    for f in filas:
        if f["gen"] != genes[0] and len(genes) > 1:
            continue
        print("%-46s%4d%7d%9d%11.2f%11.2f%9d" % (
            f["referencia"][:46], f["k"], f["ventanas"], f["observado"],
            f["esperado_uniforme"], f["esperado_composicion"], f["nulo_barajado"]))

    # Agregado sobre los cuatro genes, que es la tabla que se reporta.
    print("\nSobre los cuatro genes juntos")
    print("%-46s%4s%8s%10s%12s%12s%10s" % (
        "referencia", "k", "vent", "observado", "unif", "composic", "barajado"))
    agreg = []
    for base in sorted({f["referencia"] for f in filas}):
        for k in ks:
            sel = [f for f in filas if f["referencia"] == base and f["k"] == k]
            if not sel:
                continue
            fila = {"referencia": base, "k": k,
                    "ventanas": sum(f["ventanas"] for f in sel),
                    "observado": sum(f["observado"] for f in sel),
                    "esperado_uniforme": round(sum(f["esperado_uniforme"] for f in sel), 2),
                    "esperado_composicion": round(
                        sum(f["esperado_composicion"] for f in sel), 2),
                    "nulo_barajado": sum(f["nulo_barajado"] for f in sel)}
            agreg.append(fila)
            print("%-46s%4d%8d%10d%12.2f%12.2f%10d" % (
                base[:46], k, fila["ventanas"], fila["observado"],
                fila["esperado_uniforme"], fila["esperado_composicion"],
                fila["nulo_barajado"]))

    if a.salida:
        Path(a.salida).parent.mkdir(parents=True, exist_ok=True)
        Path(a.salida).write_text(json.dumps(
            {"k": ks, "semilla": a.semilla, "por_gen": filas, "agregado": agreg},
            indent=2, ensure_ascii=False), encoding="utf-8")
        print("\nescrito en %s" % a.salida)
    return 0


if __name__ == "__main__":
    sys.exit(main())

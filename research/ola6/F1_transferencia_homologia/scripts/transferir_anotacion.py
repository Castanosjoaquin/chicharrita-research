#!/usr/bin/env python3
"""F1 — transferencia de anotacion por homologia, a nivel proteina y por ortologia reciproca.

Toma un transcriptoma sin anotar (FASTA de nucleotidos) y devuelve, por contig, el ortologo
reciproco en un proteoma anotado, con su identidad, sus dos coberturas y la banda de
concordancia que C12 midio para esa identidad. Metodo y umbrales: ../PREREGISTRO.md.

CORTAFUEGO (D37): esta feature contesta *que gen considerar*. La tabla de salida NO lleva
secuencia de nucleotidos y ningun modulo de diseno de ARNdc la importa ni la lee. Lo verifica
test_transferir_anotacion.py.

Uso (raiz del repo, env conda f1_homologia con diamond 2.2.8):
    python transferir_anotacion.py <consulta.fas> <salida_dir> <ETIQUETA=proteoma.faa> [...]
La primera referencia es la principal; las siguientes se usan solo para el contraste.
Todo corre local: nada se sube a ningun servicio.
"""
from __future__ import annotations

import collections
import hashlib
import json
import random
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

MIN_AA = 100
EVALUE = "1e-10"
HITS_POR_CONSULTA = 5
COB_ALTA, COB_FRAGMENTO = 0.70, 0.30
FRAGMENTO_FMT = "qseqid sseqid pident length qlen slen evalue bitscore qcovhsp scovhsp"

# Banda de concordancia de C12 (Validacion A), tal cual esta en
# research/ola3/C12_validacion_homologia/resultados/concordancia_por_identidad.tsv [M]
BANDAS_C12 = [  # (techo exclusivo de identidad %, etiqueta, concordancia, lo, hi, pares)
    (40.0, "<40", 0.250, 0.102, 0.495, 16),
    (60.0, "40-60", 0.761, 0.682, 0.825, 134),
    (80.0, "60-80", 0.768, 0.727, 0.804, 456),
    (90.0, "80-90", 0.786, 0.739, 0.826, 336),
    (101.0, ">=90", 0.862, 0.809, 0.902, 210),
]

CATEGORIAS = [
    "a_sin_orf", "b_sin_hit", "c_hit_no_reciproco", "d_empate",
    "e_reciproco_sin_nombre", "f_reciproco_con_nombre",
]
NO_INFORMATIVO = re.compile(r"uncharacteri[sz]ed|hypothetical|low quality", re.I)

# ---------------------------------------------------------------- traduccion
_BASE = np.full(256, 4, dtype=np.uint8)
for _i, _b in enumerate("ACGT"):
    _BASE[ord(_b)] = _i
    _BASE[ord(_b.lower())] = _i
_AA_TABLA = "KNKNTTTTRSRSIIMIQHQHPPPPRRRRLLLLEDEDAAAAGGGGVVVV*Y*YSSSS*CWCLFLF"  # orden ACGT en las tres posiciones


def _tabla_codones() -> np.ndarray:
    """Indice (a*25+b*5+c) con alfabeto {A,C,G,T,N}; cualquier N -> 'X'."""
    aa = np.full(125, ord("X"), dtype=np.uint8)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                aa[a * 25 + b * 5 + c] = ord(_AA_TABLA[a * 16 + b * 4 + c])
    return aa


_CODONES = _tabla_codones()


def traducir_marco(codigos: np.ndarray, marco: int) -> np.ndarray:
    """Traduce `codigos` (0-3 = ACGT, 4 = ambiguo) en el marco 0/1/2; devuelve bytes ASCII."""
    n = (len(codigos) - marco) // 3
    if n <= 0:
        return np.zeros(0, dtype=np.uint8)
    t = codigos[marco:marco + 3 * n].reshape(n, 3).astype(np.int32)
    return _CODONES[t[:, 0] * 25 + t[:, 1] * 5 + t[:, 2]]


def orf_mas_largo(seq: str) -> tuple[str, str, int, int] | None:
    """ORF de parada a parada mas largo de los seis marcos.

    Devuelve (proteina, hebra, inicio_nt, fin_nt) con coordenadas 1-based sobre el contig tal
    como esta escrito, o None si ninguno llega a MIN_AA. Un empate se resuelve por el primero
    que se encuentra (hebra +, marco 0..2, despues -)."""
    cod = _BASE[np.frombuffer(seq.encode("ascii"), dtype=np.uint8)]
    largo = len(cod)
    mejor = None
    for hebra, c in (("+", cod), ("-", np.where(cod < 4, 3 - cod, 4)[::-1])):
        for marco in range(3):
            aa = traducir_marco(c, marco)
            if len(aa) < MIN_AA:
                continue
            paradas = np.flatnonzero(aa == ord("*"))
            lim = np.concatenate(([-1], paradas, [len(aa)]))
            tramos = np.diff(lim) - 1
            k = int(np.argmax(tramos))
            if tramos[k] < MIN_AA or (mejor is not None and tramos[k] <= mejor[0]):
                continue
            i0, i1 = int(lim[k]) + 1, int(lim[k + 1])  # [i0, i1) en aminoacidos
            ini = marco + 3 * i0
            fin = marco + 3 * i1
            if hebra == "+":
                a, b = ini + 1, fin
            else:
                a, b = largo - fin + 1, largo - ini
            mejor = (int(tramos[k]), aa[i0:i1].tobytes().decode("ascii"), hebra, a, b)
    return None if mejor is None else (mejor[1], mejor[2], mejor[3], mejor[4])


def leer_fasta(ruta: Path):
    nombre, partes = None, []
    with open(ruta) as fh:
        for linea in fh:
            if linea.startswith(">"):
                if nombre is not None:
                    yield nombre, "".join(partes)
                nombre, partes = linea[1:].strip(), []
            else:
                partes.append(linea.strip())
    if nombre is not None:
        yield nombre, "".join(partes)


# ------------------------------------------------------------------- nombres
def producto_refseq(cabecera: str) -> str:
    """'XP_1.1 nombre [Especie]' -> 'nombre'."""
    resto = cabecera.split(" ", 1)[1] if " " in cabecera else ""
    return re.sub(r"\s*\[[^\]]*\]\s*$", "", resto).strip()


def normalizar_nombre(nombre: str) -> str:
    """Regla descrita en C12/PREREGISTRO.md: sin 'isoform Xn', '-like', 'homolog', numeros de
    isoforma ni mayusculas. El codigo original de C12 no quedo versionado: es una
    reimplementacion desde esa descripcion (desvio declarado en el informe)."""
    n = nombre.lower()
    n = re.sub(r"\bisoform\s+\w+\b", "", n)
    n = re.sub(r"[-\s]like\b", "", n)
    n = re.sub(r"\bhomolog(ue)?\b", "", n)
    n = re.sub(r"\btranscript variant\s+\w+\b", "", n)
    n = re.sub(r"\s+\d+$", "", n.strip())
    return re.sub(r"\s+", " ", n).strip(" ,;-")


def es_informativo(nombre: str) -> bool:
    return bool(nombre) and not NO_INFORMATIVO.search(nombre)


def banda(identidad: float) -> tuple[str, float, float, float, int]:
    for techo, et, c, lo, hi, n in BANDAS_C12:
        if identidad < techo:
            return et, c, lo, hi, n
    raise ValueError(identidad)


def rotulo_cobertura(qcov: float, scov: float) -> str:
    menor = min(qcov, scov) / 100.0
    if qcov / 100.0 >= COB_ALTA and scov / 100.0 >= COB_ALTA:
        return "cobertura_alta"
    return "parcial" if menor >= COB_FRAGMENTO else "fragmento"


# ----------------------------------------------------------------- alineador
def correr(cmd: list[str]) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"FALLA {' '.join(cmd)}\n{r.stderr}")
    return r.stdout


def diamond_blastp(diamond: str, consulta: Path, db: Path, salida: Path) -> None:
    correr([diamond, "blastp", "--more-sensitive", "-e", EVALUE, "-k", str(HITS_POR_CONSULTA),
            "--max-hsps", "1", "-d", str(db), "-q", str(consulta), "-o", str(salida),
            "--outfmt", "6", *FRAGMENTO_FMT.split()])


def mejores(tsv: Path) -> dict[str, dict]:
    """Mejor hit por consulta (bitscore) y si el primer puesto esta empatado."""
    por_q: dict[str, list[tuple]] = collections.defaultdict(list)
    with open(tsv) as fh:
        for linea in fh:
            f = linea.rstrip("\n").split("\t")
            por_q[f[0]].append((float(f[7]), f[1], float(f[2]), float(f[6]),
                                float(f[8]), float(f[9]), int(f[3])))
    out = {}
    for q, hits in por_q.items():
        hits.sort(key=lambda h: -h[0])
        # un empate es mismo bitscore con OTRO sujeto en el primer puesto
        empate = len(hits) > 1 and hits[1][0] == hits[0][0] and hits[1][1] != hits[0][1]
        b = hits[0]
        out[q] = dict(sujeto=b[1], bitscore=b[0], pident=b[2], evalue=b[3],
                      qcov=b[4], scov=b[5], longitud=b[6], empate=empate)
    return out


def clasificar(orf_id: str | None, directo: dict, inverso: dict, productos: dict) -> dict:
    """Categoria exclusiva de un contig segun el preregistro (a..f)."""
    if orf_id is None:
        return dict(categoria="a_sin_orf")
    h = directo.get(orf_id)
    if h is None:
        return dict(categoria="b_sin_hit")
    inv = inverso.get(h["sujeto"])
    if h["empate"] or (inv is not None and inv["empate"]):
        return dict(categoria="d_empate", **_campos(h, productos))
    if inv is None or inv["sujeto"] != orf_id:
        return dict(categoria="c_hit_no_reciproco", **_campos(h, productos))
    nombre = productos[h["sujeto"]]
    cat = "f_reciproco_con_nombre" if es_informativo(nombre) else "e_reciproco_sin_nombre"
    return dict(categoria=cat, **_campos(h, productos))


def _campos(h: dict, productos: dict) -> dict:
    nombre = productos[h["sujeto"]]
    et, c, lo, hi, n = banda(h["pident"])
    return dict(ref_id=h["sujeto"], ref_producto=nombre,
                nombre_normalizado=normalizar_nombre(nombre) if es_informativo(nombre) else "",
                pident=h["pident"], cob_orf=h["qcov"], cob_ref=h["scov"],
                rotulo_cobertura=rotulo_cobertura(h["qcov"], h["scov"]),
                evalue=h["evalue"], bitscore=h["bitscore"], banda_identidad=et,
                banda_concordancia=c, banda_ic_lo=lo, banda_ic_hi=hi, banda_pares_c12=n)


COLUMNAS = ["contig", "orf_aa", "orf_hebra", "orf_ini", "orf_fin", "categoria", "ref_id",
            "ref_producto", "nombre_normalizado", "pident", "cob_orf", "cob_ref",
            "rotulo_cobertura", "evalue", "bitscore", "banda_identidad",
            "banda_concordancia", "banda_ic_lo", "banda_ic_hi", "banda_pares_c12"]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for bloque in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def main(argv: list[str]) -> None:
    consulta, salida = Path(argv[0]), Path(argv[1])
    refs = [a.split("=", 1) for a in argv[2:]]
    junto = Path(sys.executable).parent / "diamond"
    diamond = str(junto) if junto.exists() else "diamond"
    salida.mkdir(parents=True, exist_ok=True)
    trabajo = Path("work/F1/corrida")
    trabajo.mkdir(parents=True, exist_ok=True)

    orfs, n_contigs = {}, 0
    orf_faa = trabajo / "orfs.faa"
    with open(orf_faa, "w") as fo:
        for cab, seq in leer_fasta(consulta):
            n_contigs += 1
            contig = cab.split()[0]
            r = orf_mas_largo(seq)
            orfs[contig] = None if r is None else dict(
                proteina=r[0], hebra=r[1], ini=r[2], fin=r[3], id=f"{contig}|{r[1]}|{r[2]}-{r[3]}")
            if r is not None:
                fo.write(f">{orfs[contig]['id']}\n{r[0]}\n")
    print(f"{n_contigs} contigs, {sum(v is not None for v in orfs.values())} con ORF >= {MIN_AA} aa")
    run(diamond, trabajo / "orfs.faa", "ORFS", trabajo)

    resumen = dict(consulta=str(consulta), consulta_sha256=sha256(consulta), contigs=n_contigs,
                   diamond=correr([diamond, "version"]).strip(),
                   parametros=dict(min_aa=MIN_AA, evalue=EVALUE, hits=HITS_POR_CONSULTA,
                                   sensibilidad="--more-sensitive", max_hsps=1), referencias={})
    for et, ruta in refs:
        ruta = Path(ruta)
        productos = {c.split()[0]: producto_refseq(c) for c, _ in leer_fasta(ruta)}
        db = trabajo / f"db_{et}"
        correr([diamond, "makedb", "--in", str(ruta), "-d", str(db)])
        fwd, rev = trabajo / f"fwd_{et}.tsv", trabajo / f"rev_{et}.tsv"
        diamond_blastp(diamond, orf_faa, db, fwd)
        diamond_blastp(diamond, ruta, trabajo / "db_ORFS", rev)
        directo, inverso = mejores(fwd), mejores(rev)
        filas, cuenta = [], collections.Counter()
        for contig, o in orfs.items():
            c = clasificar(None if o is None else o["id"], directo, inverso, productos)
            cuenta[c["categoria"]] += 1
            fila = dict(contig=contig, orf_aa=0 if o is None else len(o["proteina"]),
                        orf_hebra="" if o is None else o["hebra"],
                        orf_ini="" if o is None else o["ini"],
                        orf_fin="" if o is None else o["fin"], **c)
            filas.append(fila)
        if sum(cuenta.values()) != n_contigs:
            sys.exit("ABORTA: las categorias no suman el total de contigs")
        with open(salida / f"transferencia_{et}.tsv", "w") as fo:
            fo.write("\t".join(COLUMNAS) + "\n")
            for f in filas:
                fo.write("\t".join(_fmt(f.get(k, "")) for k in COLUMNAS) + "\n")
        recip = [f for f in filas if f["categoria"].startswith(("e_", "f_"))]
        resumen["referencias"][et] = dict(
            proteoma=str(ruta), proteoma_sha256=sha256(ruta), proteinas=len(productos),
            categorias={k: cuenta.get(k, 0) for k in CATEGORIAS},
            proteinas_de_referencia_distintas_con_recip=len({f["ref_id"] for f in recip}))
    (trabajo / "resumen_parcial.json").write_text(json.dumps(resumen, indent=1))
    (salida / "resumen.json").write_text(json.dumps(resumen, indent=1, ensure_ascii=False))
    print(json.dumps({k: v["categorias"] for k, v in resumen["referencias"].items()}, indent=1))


def run(diamond: str, faa: Path, etiqueta: str, trabajo: Path) -> None:
    correr([diamond, "makedb", "--in", str(faa), "-d", str(trabajo / f"db_{etiqueta}")])


def _fmt(v) -> str:
    if isinstance(v, float):
        return f"{v:.6g}"
    return str(v)


if __name__ == "__main__":
    main(sys.argv[1:])

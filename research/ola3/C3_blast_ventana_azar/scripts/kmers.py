"""Conteo exacto de k-meros sobre referencias grandes, con numpy y por bloques.

Por que esta aca: Q3 necesita el numero OBSERVADO de coincidencias exactas de cada
ventana en genomas y transcriptomas reales, y la consigna pide que el observado NO
salga de una heuristica (BLAST puede perder casos). Un automata o un indice entero
del genoma de 972 Mb no entra comodo en 16 GiB, asi que se recorre la referencia por
bloques y se mantiene en memoria solo el bloque.

Estrategia, en tres pasos por bloque:

1. Se codifica la secuencia a enteros 0-3 (A,C,G,T); todo lo demas es invalido.
2. Se calcula el codigo entero del 12-mero que empieza en cada posicion y se filtra
   con una tabla booleana de 4^12 = 16.777.216 entradas (16 MB) que marca los
   prefijos de 12 nt de las consultas. Sobreviven unos pocos miles de posiciones por
   bloque, y solo esas se verifican a largo completo. Es exacto: todo k-mero de la
   consulta (k >= 12) tiene su prefijo de 12 en la tabla, asi que no se pierde ninguno.
3. En las posiciones candidatas se arma el codigo de largo k y se compara contra el
   arreglo ordenado de codigos de consulta con busqueda binaria.

Las dos hebras se cubren agregando el complemento reverso de cada consulta al
conjunto de patrones, que es equivalente a recorrer la hebra opuesta de la referencia.

De paso, en la misma pasada se acumulan los conteos de m-meros para m = 1..6, que
son los que alimentan el modelo de Markov de orden 3 a 5.
"""

from __future__ import annotations

import gzip
import numpy as np

PREFIX = 12          # largo del prefijo del filtro
MAXORDER = 6         # m-meros contados para el modelo de Markov (orden hasta 5)

_LUT = np.full(256, 255, dtype=np.uint8)
for _i, _b in enumerate(b"ACGT"):
    _LUT[_b] = _i
for _i, _b in enumerate(b"acgt"):
    _LUT[_b] = _i

_COMP = bytes.maketrans(b"ACGTacgtN", b"TGCATGCAN")


def rc(s: str) -> str:
    return s.encode().translate(_COMP).decode()[::-1]


def code_of(s: str) -> int:
    """Codigo entero base-4 de una cadena ACGT (A=0, C=1, G=2, T=3)."""
    c = 0
    for ch in s:
        c = c * 4 + "ACGT".index(ch)
    return c


def iter_fasta(path):
    """(nombre, secuencia_bytes) de un FASTA, con o sin gzip, un registro por vez."""
    op = gzip.open if str(path).endswith(".gz") else open
    name, buf = None, []
    with op(path, "rb") as fh:
        for line in fh:
            if line.startswith(b">"):
                if name is not None:
                    yield name, b"".join(buf)
                name, buf = line[1:].split()[0].decode(), []
            else:
                buf.append(line.strip())
    if name is not None:
        yield name, b"".join(buf)


class Consultas:
    """Conjunto de consultas: para cada k, los codigos de las ventanas y sus RC."""

    def __init__(self, por_k: dict[int, list[str]]):
        self.ks = sorted(por_k)
        self.seqs = {k: list(por_k[k]) for k in self.ks}
        self.codes = {}       # k -> arreglo ordenado de codigos unicos (ambas hebras)
        self.idx = {}         # k -> para cada codigo unico, indice de la ventana
        prefijos = set()
        for k in self.ks:
            pares = []
            for j, w in enumerate(self.seqs[k]):
                pares.append((code_of(w), j))
                pares.append((code_of(rc(w)), j))
                prefijos.add(code_of(w[:PREFIX]))
                prefijos.add(code_of(rc(w)[:PREFIX]))
            pares.sort()
            self.codes[k] = np.array([p[0] for p in pares], dtype=np.int64)
            self.idx[k] = np.array([p[1] for p in pares], dtype=np.int64)
        self.tabla = np.zeros(4 ** PREFIX, dtype=bool)
        self.tabla[np.fromiter(prefijos, dtype=np.int64)] = True


def _codes_en(a_valid: np.ndarray, pos: np.ndarray, k: int) -> np.ndarray:
    """Codigo de largo k que empieza en cada posicion de `pos`."""
    out = np.zeros(pos.shape, dtype=np.int64)
    for j in range(k):
        out = (out << 2) | a_valid[pos + j]
    return out


def escanear(ruta, consultas: Consultas, bloque: int = 8_000_000, verbose=True):
    """Una pasada por la referencia. Devuelve dict con observados, N y m-meros."""
    ks = consultas.ks
    kmax = max(ks)
    obs = {k: np.zeros(len(consultas.seqs[k]), dtype=np.int64) for k in ks}
    # en cuantos registros distintos (cromosomas o transcriptos) aparece cada ventana
    nrec = {k: np.zeros(len(consultas.seqs[k]), dtype=np.int64) for k in ks}
    neff = {k: 0 for k in ks}
    mcount = {m: np.zeros(4 ** m, dtype=np.int64) for m in range(1, MAXORDER + 1)}
    total_bases = 0
    n_registros = 0

    for name, seq in iter_fasta(ruta):
        n = len(seq)
        total_bases += n
        n_registros += 1
        if n < min(ks):
            continue
        antes = {k: obs[k].copy() for k in ks}
        pos0 = 0
        while pos0 < n:
            fin = min(pos0 + bloque, n)
            # se leen kmax-1 bases extra para no cortar ventanas en el borde
            hasta = min(n, fin + kmax - 1)
            sub = np.frombuffer(seq[pos0:hasta], dtype=np.uint8)
            cod = _LUT[sub]
            valido = cod < 4
            a = np.where(valido, cod, 0).astype(np.int64)
            cinv = np.concatenate(([0], np.cumsum(~valido)))
            L = len(a)
            n_nuevos = fin - pos0      # ventanas que arrancan en este bloque

            # m-meros para Markov (solo los que arrancan en el bloque)
            for m in range(1, MAXORDER + 1):
                lim = min(n_nuevos, L - m + 1)
                if lim <= 0:
                    continue
                c = np.zeros(lim, dtype=np.int64)
                for j in range(m):
                    c = (c << 2) | a[j:j + lim]
                ok = (cinv[m:m + lim] - cinv[0:lim]) == 0
                if ok.any():
                    mcount[m] += np.bincount(c[ok], minlength=4 ** m)

            # N efectivo por k
            for k in ks:
                lim = min(n_nuevos, L - k + 1)
                if lim <= 0:
                    continue
                ok = (cinv[k:k + lim] - cinv[0:lim]) == 0
                neff[k] += int(ok.sum())

            # filtro por prefijo de 12
            limp = min(n_nuevos, L - PREFIX + 1)
            if limp > 0:
                c12 = np.zeros(limp, dtype=np.int64)
                for j in range(PREFIX):
                    c12 = (c12 << 2) | a[j:j + limp]
                okp = (cinv[PREFIX:PREFIX + limp] - cinv[0:limp]) == 0
                cand = np.nonzero(okp & consultas.tabla[c12])[0]
                if len(cand):
                    for k in ks:
                        c2 = cand[(cand + k) <= L]
                        if not len(c2):
                            continue
                        okk = (cinv[c2 + k] - cinv[c2]) == 0
                        c2 = c2[okk]
                        if not len(c2):
                            continue
                        ck = _codes_en(a, c2, k)
                        Q = consultas.codes[k]
                        p = np.searchsorted(Q, ck)
                        p = np.clip(p, 0, len(Q) - 1)
                        hit = Q[p] == ck
                        if hit.any():
                            obs[k] += np.bincount(consultas.idx[k][p[hit]],
                                                  minlength=len(obs[k]))
            pos0 = fin
        for k in ks:
            nrec[k] += (obs[k] > antes[k]).astype(np.int64)
        if verbose and n_registros % 5000 == 0:
            print("   ... %d registros, %d bases" % (n_registros, total_bases), flush=True)

    return {"observado": obs, "registros_distintos": nrec, "neff": neff,
            "mcount": mcount, "bases": total_bases, "registros": n_registros}

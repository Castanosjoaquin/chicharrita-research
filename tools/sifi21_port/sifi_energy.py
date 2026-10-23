"""Energia libre de hibridacion por vecinos mas cercanos, port del free_energy.py de si-Fi21.

Origen: si-Fi21 (Luck et al. 2019, Front Plant Sci 10:1023), modulo free_energy.py,
que a su vez es una copia de Bio.SeqUtils.MeltingTemp de Biopython con un retorno
de deltaG agregado. Repositorio: github.com/snowformatics/siFi21-

Las tablas NO se copian: se toman de Biopython, que las mantiene y las publica con
los mismos valores (verificado contra el fuente de si-Fi en test_sifi.py). La unica
excepcion es RNA_DE2, que si-Fi agrego y Biopython no trae; se deriva de RNA_DE1
invirtiendo cada clave, que es exactamente la relacion que tienen en el fuente.

Diferencias respecto del original, todas justificadas en CAMBIOS.md:
  - Python 3 (el original es Python 2.7 y no importa).
  - La temperatura es un argumento en vez de estar fijada en 22 C.
  - Las tablas de mismatch son argumentos y su uso se puede contabilizar (`track`),
    porque el original mezcla tablas de ADN en un calculo de ARN.
  - Se elimino el calculo de Tm, que el original computaba y descartaba.
"""

from __future__ import annotations

import math
from Bio.Seq import Seq
from Bio.SeqUtils import gc_fraction
from Bio.SeqUtils import MeltingTemp as _mt

# --- Tablas -----------------------------------------------------------------

# Apilamientos canonicos de ARN. si-Fi usa RNA_NN3 por defecto.
RNA_NN1 = _mt.RNA_NN1   # Freier et al. 1986   (definida en si-Fi, NO usada)
RNA_NN2 = _mt.RNA_NN2   # Xia et al. 1998      (definida en si-Fi, NO usada)
RNA_NN3 = _mt.RNA_NN3   # Chen et al. 2012     <- el default real de si-Fi

# La tabla propia de sifi21INTA, y la unica que NO sale de Biopython.
#
# Es el unico parametro de quimica que el laboratorio cambio respecto del original:
# `calculateFreeEnergy` de `sifi21INTA/freeEnergy.py:306` la usa por defecto, mientras
# que el original usa RNA_NN3. Transcrita literal de `freeEnergy.py:61-74` del fuente
# (commit 92df4449, cabeza de main al 2024-03-27).
#
# Atribucion: el comentario del fuente la asigna a Zuber et al. (2022), Nucleic Acids
# Research 50(9):5251-5262. **El articulo no se abrio**, asi que la atribucion esta
# identificada pero no verificada contra su fuente `[?]`; esta anotado como pregunta
# abierta en `00_meta/PREGUNTAS_ABIERTAS.md`. Lo que si esta verificado es que la tabla
# es distinta de RNA_NN3 en 22 de sus 28 entradas, asi que no es un retoque menor y no
# se puede aproximar con la de Biopython.
RNA_NN4 = {
    "init": (4.66, 1.78), "init_A/T": (4.36, 13.35), "init_G/C": (0, 0),
    "init_oneG/C": (0, 0), "init_allA/T": (0, 0), "init_5T/A": (0, 0),
    "sym": (0, -1.38),
    "AA/TT": (-7.44, -20.98), "AT/TA": (-8.91, -25.22), "TA/AT": (-9.16, -25.4),
    "CA/GT": (-10.47, -27.08), "GT/CA": (-11.98, -31.37),
    "CT/GA": (-10.90, -28.5), "GA/CT": (-13.21, -34.9),
    "CG/GC": (-9.61, -23.46), "GC/CG": (-16.52, -42.13),
    "GG/CC": (-13.94, -34.41), "GT/TG": (-7.66, -24.11),
    "GG/TT": (-9.06, -28.57), "AG/TT": (-5.1, -16.53),
    "TG/AT": (-2.72, -8.08), "TT/AG": (-10.58, -32.19), "TG/GT": (-8.76, -27.04),
    "AT/TG": (-9.23, -27.32), "CG/GT": (-5.64, -14.83), "CT/GG": (-9.26, -23.64),
    "GG/CT": (-12.41, -34.23), "GT/CG": (-14.73, -40.32),
}

TABLAS_NN = {"NN1": RNA_NN1, "NN2": RNA_NN2, "NN3": RNA_NN3, "NN4": RNA_NN4}

# Mismatches. si-Fi usa las de ADN; ver CAMBIOS.md, cambio C3.
DNA_IMM1 = _mt.DNA_IMM1  # Allawi & SantaLucia 1998, mismatches internos ADN/ADN
DNA_TMM1 = _mt.DNA_TMM1  # mismatches terminales ADN/ADN

# Extremos colgantes de ARN, Turner & Mathews 2010.
#
# Cuidado con los nombres: lo que si-Fi llama RNA_DE2 (y usa por defecto) es
# exactamente la tabla que Biopython llama RNA_DE1, con el mismo formato de clave
# ('.G/CC'). Lo que si-Fi llama RNA_DE1 es la misma tabla con las claves invertidas
# ('CC/G.') y no se usa en ninguna parte del programa. Verificado clave por clave
# contra el fuente en test_sifi.py.
RNA_DE2 = _mt.RNA_DE1                                      # <- el default real de si-Fi
RNA_DE1_SIFI = {k[::-1]: v for k, v in _mt.RNA_DE1.items()}  # variante no usada

R_GAS = 1.987  # cal/(K*mol)


def _check(seq: str) -> str:
    """Normaliza como el original: mayusculas, U->T y filtrado a ACGTI."""
    seq = "".join(str(seq).split()).upper()
    seq = str(Seq(seq).back_transcribe())
    return "".join(b for b in seq if b in ("A", "C", "G", "T", "I"))


def salt_correction(Na=0, K=0, Tris=0, Mg=0, dNTPs=0, method=5, seq=None) -> float:
    """Correccion de fuerza ionica. Solo se implementan los metodos que si-Fi puede usar.

    El metodo 5 (el default de si-Fi) es la correccion entropica de SantaLucia:
    depende unicamente del largo de la secuencia y de la concentracion de monovalentes.
    """
    if method in (5, 6, 7) and not seq:
        raise ValueError("el metodo %r necesita la secuencia" % method)
    if not method:
        return 0.0

    mon = Na + K + Tris / 2.0  # milimolar
    if sum((K, Mg, Tris, dNTPs)) > 0 and method != 7 and dNTPs < Mg:
        # Equivalente de Na+ segun von Ahsen et al. 2001.
        mon += 120 * math.sqrt(Mg - dNTPs)
    mon *= 1e-3  # molar
    if not mon:
        raise ValueError("concentracion ionica total de cero no admitida")

    if method == 1:
        return 16.6 * math.log10(mon)
    if method == 2:
        return 16.6 * math.log10(mon / (1.0 + 0.7 * mon))
    if method == 3:
        return 12.5 * math.log10(mon)
    if method == 4:
        return 11.7 * math.log10(mon)
    if method == 5:
        return 0.368 * (len(seq) - 1) * math.log(mon)
    if method == 6:
        return (4.29 * gc_fraction(seq) - 3.95) * 1e-5 * math.log(mon) + \
               9.40e-6 * math.log(mon) ** 2
    raise ValueError("metodo %r no implementado en este port" % method)


def free_energy(
    seq,
    c_seq=None,
    shift: int = 0,
    temp_c: float = 22.0,
    nn_table=None,
    de_table=None,
    imm_table=None,
    tmm_table=None,
    Na: float = 20,
    K: float = 50,
    Tris: float = 0,
    Mg: float = 0,
    dNTPs: float = 0,
    saltcorr: int = 5,
    check: bool = True,
    strict: bool = True,
    track: dict | None = None,
) -> float:
    """deltaG (kcal/mol) de hibridacion a `temp_c`, por vecinos mas cercanos.

    Reproduce el calculo de si-Fi paso por paso. `track`, si se pasa, acumula
    cuantas veces se consulto cada tabla de mismatch: es la instrumentacion que
    permite medir si la mezcla ADN/ARN del original afecta a un caso concreto.
    """
    nn_table = RNA_NN3 if nn_table is None else nn_table
    de_table = RNA_DE2 if de_table is None else de_table
    imm_table = DNA_IMM1 if imm_table is None else imm_table
    tmm_table = DNA_TMM1 if tmm_table is None else tmm_table

    seq = str(seq)
    if c_seq is None:
        c_seq = str(Seq(seq).complement())
    c_seq = str(c_seq)
    if check:
        seq = _check(seq)
        c_seq = _check(c_seq)

    tmpseq, tmp_cseq = seq, c_seq
    dH = dS = 0.0

    # --- Extremos colgantes -------------------------------------------------
    if shift or len(seq) != len(c_seq):
        if shift > 0:
            tmpseq = "." * shift + seq
        if shift < 0:
            tmp_cseq = "." * abs(shift) + c_seq
        if len(tmp_cseq) > len(tmpseq):
            tmpseq += (len(tmp_cseq) - len(tmpseq)) * "."
        if len(tmp_cseq) < len(tmpseq):
            tmp_cseq += (len(tmpseq) - len(tmp_cseq)) * "."
        while tmpseq.startswith("..") or tmp_cseq.startswith(".."):
            tmpseq, tmp_cseq = tmpseq[1:], tmp_cseq[1:]
        while tmpseq.endswith("..") or tmp_cseq.endswith(".."):
            tmpseq, tmp_cseq = tmpseq[:-1], tmp_cseq[:-1]

        if tmpseq.startswith(".") or tmp_cseq.startswith("."):
            left_de = tmpseq[:2] + "/" + tmp_cseq[:2]
            dH += de_table[left_de][0]
            dS += de_table[left_de][1]
            tmpseq, tmp_cseq = tmpseq[1:], tmp_cseq[1:]
        if tmpseq.endswith(".") or tmp_cseq.endswith("."):
            right_de = tmp_cseq[-2:][::-1] + "/" + tmpseq[-2:][::-1]
            dH += de_table[right_de][0]
            dS += de_table[right_de][1]
            tmpseq, tmp_cseq = tmpseq[:-1], tmp_cseq[:-1]

    # --- Mismatches terminales ---------------------------------------------
    left_tmm = tmp_cseq[:2][::-1] + "/" + tmpseq[:2][::-1]
    if left_tmm in tmm_table:
        if track is not None:
            track["tmm"] = track.get("tmm", 0) + 1
        dH += tmm_table[left_tmm][0]
        dS += tmm_table[left_tmm][1]
        tmpseq, tmp_cseq = tmpseq[1:], tmp_cseq[1:]
    right_tmm = tmpseq[-2:] + "/" + tmp_cseq[-2:]
    if right_tmm in tmm_table:
        if track is not None:
            track["tmm"] = track.get("tmm", 0) + 1
        dH += tmm_table[right_tmm][0]
        dS += tmm_table[right_tmm][1]
        tmpseq, tmp_cseq = tmpseq[:-1], tmp_cseq[:-1]

    # --- Iniciacion ---------------------------------------------------------
    dH += nn_table["init"][0]
    dS += nn_table["init"][1]
    key = "init_allA/T" if gc_fraction(seq) == 0 else "init_oneG/C"
    dH += nn_table[key][0]
    dS += nn_table[key][1]
    # El original aplica la misma penalizacion dos veces, una por cada extremo.
    if seq.startswith("T"):
        dH += nn_table["init_5T/A"][0]
        dS += nn_table["init_5T/A"][1]
    if seq.endswith("A"):
        dH += nn_table["init_5T/A"][0]
        dS += nn_table["init_5T/A"][1]
    ends = seq[0] + seq[-1]
    n_at = ends.count("A") + ends.count("T")
    n_gc = ends.count("G") + ends.count("C")
    dH += nn_table["init_A/T"][0] * n_at
    dS += nn_table["init_A/T"][1] * n_at
    dH += nn_table["init_G/C"][0] * n_gc
    dS += nn_table["init_G/C"][1] * n_gc

    # --- Apilamiento --------------------------------------------------------
    for i in range(len(tmpseq) - 1):
        nb = tmpseq[i:i + 2] + "/" + tmp_cseq[i:i + 2]
        if nb in imm_table:
            if track is not None:
                track["imm"] = track.get("imm", 0) + 1
            dH += imm_table[nb][0]
            dS += imm_table[nb][1]
        elif nb[::-1] in imm_table:
            if track is not None:
                track["imm"] = track.get("imm", 0) + 1
            dH += imm_table[nb[::-1]][0]
            dS += imm_table[nb[::-1]][1]
        elif nb in nn_table:
            dH += nn_table[nb][0]
            dS += nn_table[nb][1]
        elif nb[::-1] in nn_table:
            dH += nn_table[nb[::-1]][0]
            dS += nn_table[nb[::-1]][1]
        else:
            if strict:
                raise ValueError("sin datos para los vecinos %r" % nb)
            if track is not None:
                track["sin_datos"] = track.get("sin_datos", 0) + 1

    if saltcorr:
        corr = salt_correction(Na=Na, K=K, Tris=Tris, Mg=Mg, dNTPs=dNTPs,
                               method=saltcorr, seq=seq)
        if saltcorr == 5:
            dS += corr

    tao = 273.15 + temp_c
    return (dH * 1000 - tao * dS) / 1000

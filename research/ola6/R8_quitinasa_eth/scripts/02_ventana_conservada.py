#!/usr/bin/env python3
"""R8 paso 2 — ¿la ventana de la posición 347 cae en zona conservada o variable?

El paso 1 contestó qué referencias tienen ortólogo de `LOC124369889`. Falta la otra mitad
de lo que `D73` declaró faltante, y son dos preguntas distintas que conviene no mezclar:

1. **¿La ventana cae en un tramo conservado de la familia?** Se mide sobre la proteína,
   alineando la quitinasa de *H. vitripennis* contra cada ortólogo recíproco y comparando
   la identidad **en los residuos que cubre la ventana** contra la identidad de toda la
   proteína. Un acierto en un dominio conservado y uno en un tramo variable no tienen el
   mismo riesgo.

2. **¿Algún ortólogo tiene una casi-coincidencia con la ventana, en nucleótido?** Es la
   pregunta que de verdad decide el riesgo y la que el tamizaje exacto no puede contestar:
   un ortólogo que difiera en unos pocos nucleótidos no aparece en `offtarget_21nt.py` y un
   ARNdc sí podría silenciarlo. Se barre el transcripto ortólogo entero, en las dos hebras,
   y se reporta el **mínimo de desajustes** contra el 21-mero de `eth_Dm`.

Las dos usan `Bio.Align.PairwiseAligner` y el barrido exacto de desajustes; no hace falta un
MSA para tres secuencias y una ventana. Nada sale de la máquina y la salida no lleva
nucleótidos: sólo coordenadas, identidades y conteos de desajustes.

Uso:
    python3 research/ola6/R8_quitinasa_eth/scripts/02_ventana_conservada.py
"""
from __future__ import annotations

import csv
import gzip
import json
import sys
from pathlib import Path

from Bio import Align
from Bio.Align import substitution_matrices

RAIZ = Path(__file__).resolve().parents[4]
TRABAJO = RAIZ / "work/R8"
SALIDA = Path(__file__).resolve().parents[1] / "resultados"
REF = RAIZ / "work/W5/ref"

#: La ventana del acierto: `eth_Dm`, inicio 347 (1-based), 21 nt (M6, D73).
GEN, POS, K = "eth_Dm", 347, 21
#: El transcripto de la quitinasa del que sale la consulta, y su ORF (paso 1).
TR_ORIGEN, ORF_INICIO = "XM_046828031.1", 133
COMP = str.maketrans("ACGTacgt", "TGCAtgca")


def rc(s: str) -> str:
    return s.translate(COMP)[::-1]


def leer_fasta(ruta: Path) -> dict[str, str]:
    abrir = gzip.open if ruta.suffix == ".gz" else open
    out, nombre, buf = {}, None, []
    with abrir(ruta, "rt") as fh:
        for l in fh:
            if l.startswith(">"):
                if nombre:
                    out[nombre] = "".join(buf)
                nombre, buf = l[1:].split()[0], []
            else:
                buf.append(l.strip())
    if nombre:
        out[nombre] = "".join(buf)
    return out


def min_desajustes(ventana: str, secuencia: str) -> tuple[int, int, str]:
    """Mínimo de desajustes de `ventana` contra `secuencia`, en las dos hebras.

    Devuelve (desajustes, posicion_1based, hebra). Sin indels a propósito: un siRNA que
    dirige el corte necesita apareamiento contiguo, y un hueco rompe el dúplex.
    """
    mejor = (len(ventana) + 1, 0, "")
    s = secuencia.upper()
    for hebra, q in (("directa", ventana), ("revcomp", rc(ventana))):
        for i in range(len(s) - len(q) + 1):
            d = 0
            for a, b in zip(q, s[i:i + len(q)]):
                if a != b:
                    d += 1
                    if d >= mejor[0]:
                        break
            if d < mejor[0]:
                mejor = (d, i + 1, hebra)
    return mejor


def main() -> int:
    SALIDA.mkdir(parents=True, exist_ok=True)
    eth = "".join(l.strip() for l in
                  open(RAIZ / "work/sifi_v2/fasta/eth_Dm_full.fasta") if not l.startswith(">"))
    ventana = eth[POS - 1:POS - 1 + K]
    if len(ventana) != K:
        raise SystemExit("la ventana no entra en el gen")

    orto = {f["referencia"]: f for f in csv.DictReader(
        open(SALIDA / "ortologos_quitinasa.tsv", encoding="utf-8"), delimiter="\t")}
    archivos = {r: f["archivo"] for r, f in orto.items()}

    # --- dónde cae la ventana dentro del transcripto y de su CDS
    hv = leer_fasta(REF / archivos["H_vitripennis"])
    tr = hv[TR_ORIGEN]
    ini_tr = tr.find(rc(ventana))
    if ini_tr < 0:
        raise SystemExit("la ventana no aparece en %s" % TR_ORIGEN)
    ini_tr += 1
    off_cds = ini_tr - ORF_INICIO
    cod_ini = off_cds // 3 + 1
    cod_fin = (off_cds + K - 1) // 3 + 1
    print("ventana %s %d-%d  ->  %s nt %d-%d (hebra revcomp), codones %d-%d del ORF"
          % (GEN, POS, POS + K - 1, TR_ORIGEN, ini_tr, ini_tr + K - 1, cod_ini, cod_fin))

    # --- 1. conservación de proteína en esos residuos
    prot = leer_fasta(TRABAJO / "quitinasa_prot.faa")
    consulta = prot["%s_orf" % TR_ORIGEN]
    al = Align.PairwiseAligner(scoring="blastp")
    al.substitution_matrix = substitution_matrices.load("BLOSUM62")
    al.open_gap_score, al.extend_gap_score, al.mode = -11, -1, "global"

    filas = []
    for ref_corto, f in orto.items():
        if ref_corto == "H_vitripennis":
            continue
        recip = f["reciproco"] == "si"
        sec = leer_fasta(REF / archivos[ref_corto]).get(f["mejor_acierto"], "")
        p_otro = (TRABAJO / ("vuelta_%s.faa" % ref_corto))
        otro = leer_fasta(p_otro)[list(leer_fasta(p_otro))[0]] if p_otro.exists() else ""
        fila = {"referencia": ref_corto, "ortologo_reciproco": f["reciproco"],
                "transcripto": f["mejor_acierto"], "identidad_proteina_pct": "",
                "identidad_ventana_pct": "", "residuos_ventana_alineados": "",
                "min_desajustes_21nt": "", "pos_min_desajustes": "", "hebra": ""}
        if otro:
            aln = al.align(consulta, otro)[0]
            a, b = aln[0], aln[1]
            # columnas del alineamiento que corresponden a los codones de la ventana
            idx_q, cols = 0, []
            for col, ch in enumerate(a):
                if ch != "-":
                    idx_q += 1
                    if cod_ini <= idx_q <= cod_fin:
                        cols.append(col)
            ident_tot = sum(1 for x, y in zip(a, b) if x == y and x != "-")
            largo_tot = sum(1 for x in a if x != "-")
            ident_v = sum(1 for c in cols if a[c] == b[c])
            fila["identidad_proteina_pct"] = round(100.0 * ident_tot / largo_tot, 1)
            fila["identidad_ventana_pct"] = (round(100.0 * ident_v / len(cols), 1)
                                             if cols else "")
            fila["residuos_ventana_alineados"] = len(cols)
        if sec:
            d, pos, hebra = min_desajustes(ventana, sec)
            fila.update({"min_desajustes_21nt": d, "pos_min_desajustes": pos,
                         "hebra": hebra})
        filas.append(fila)
        print("%-14s recip=%-3s ident_prot=%-6s ident_ventana=%-6s min_desajustes=%s"
              % (ref_corto, f["reciproco"], fila["identidad_proteina_pct"],
                 fila["identidad_ventana_pct"], fila["min_desajustes_21nt"]), flush=True)

    # --- control y nulo: sin esto, «8 desajustes» no se puede leer
    # El mismo número en las cinco referencias pide dos controles. El positivo: la ventana
    # contra su propio transcripto tiene que dar 0. El nulo: 21-meros al azar contra el
    # mismo ortologo, para saber cuantos desajustes da el azar y si 8 es poco o es lo
    # esperable. Con semilla fija para que el numero sea reproducible.
    import random
    control = min_desajustes(ventana, tr)[0]
    if control != 0:
        raise SystemExit("control positivo fallido: %d desajustes contra %s"
                         % (control, TR_ORIGEN))
    ref_nulo = orto["H_axyridis"]["mejor_acierto"]
    sec_nulo = leer_fasta(REF / archivos["H_axyridis"])[ref_nulo]
    random.seed(0)
    nulo = sorted(min_desajustes("".join(random.choice("ACGT") for _ in range(K)),
                                 sec_nulo)[0] for _ in range(40))
    print("\ncontrol positivo: %d desajustes contra %s (esperado 0)" % (control, TR_ORIGEN))
    print("nulo sobre %s: 40 ventanas al azar -> min %d, mediana %d, max %d"
          % (ref_nulo, nulo[0], nulo[len(nulo) // 2], nulo[-1]))

    with open(SALIDA / "ventana_conservacion.tsv", "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()), delimiter="\t")
        w.writeheader()
        w.writerows(filas)
    (SALIDA / "ventana_meta.json").write_text(json.dumps({
        "gen": GEN, "posicion_1based": POS, "k": K,
        "transcripto_origen": TR_ORIGEN, "orf_inicio_nt": ORF_INICIO,
        "ventana_en_transcripto_nt": [ini_tr, ini_tr + K - 1],
        "codones_del_orf": [cod_ini, cod_fin],
        "metodo_proteina": "PairwiseAligner global, BLOSUM62, gap -11/-1",
        "metodo_nucleotido": "barrido exacto de desajustes, dos hebras, sin indels",
        "control_positivo_desajustes": control,
        "nulo_ortologo": ref_nulo, "nulo_n": len(nulo),
        "nulo_min": nulo[0], "nulo_mediana": nulo[len(nulo) // 2], "nulo_max": nulo[-1],
        "python": sys.version.split()[0],
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\nescrito en %s" % SALIDA)
    return 0


if __name__ == "__main__":
    sys.exit(main())

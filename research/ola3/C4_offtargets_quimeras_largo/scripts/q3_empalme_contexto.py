"""Por qué una ventana de empalme puede acertar igual en el genoma del blanco.

Verificación puntual para Q3. El tamizaje de 21 nt sobre las quimeras devolvió
aciertos de empalme sólo contra el genoma de *Dalbulus maidis*, y en la quimera
ATPaseD_Dm+BicC_Dm devolvió además tres aciertos de 21/21. La hipótesis mecánica es
que el empalme reconstruye, base por base, el contexto genómico del gen de origen:
la base pegada coincide con la base vecina en el ADN. Esto se comprueba leyendo el
flanco real en el ensamblado, no se supone.

Uso:
    python research/ola3/C4_offtargets_quimeras_largo/scripts/q3_empalme_contexto.py
"""

from __future__ import annotations

import gzip
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
RESULTADOS = Path(__file__).resolve().parents[1] / "resultados"
GENOMA = RAIZ / "work/W5/ref/GCA_975739785.1_ihDalMaid1.1_genomic.fna.gz"
FASTA = RAIZ / "work/C4/fasta"
COMP = str.maketrans("ACGT", "TGCA")


def rc(s): return s.translate(COMP)[::-1]


def leer(nombre):
    return "".join(l.strip() for l in (FASTA / nombre).read_text().splitlines()
                   if not l.startswith(">")).upper()


def main():
    bicc, atp = leer("BicC_Dm_sel.fasta"), leer("ATPaseD_Dm_sel.fasta")
    sondas = {
        "inicio_BicC_20nt": bicc[:20],
        "fin_ATPaseD_20nt": atp[-20:],
        "inicio_ATPaseD_20nt": atp[:20],
        "fin_BicC_20nt": bicc[-20:],
    }
    hallazgos = {k: [] for k in sondas}
    nombre, buf = None, []

    def revisar(ref, s):
        for k, p in sondas.items():
            for hebra, pat in (("+", p), ("-", rc(p))):
                i = s.find(pat)
                while i != -1:
                    izq = s[max(0, i - 3):i]
                    der = s[i + len(pat):i + len(pat) + 3]
                    hallazgos[k].append({"ref": ref, "pos": i + 1, "hebra": hebra,
                                         "flanco_anterior_3nt": izq, "flanco_posterior_3nt": der})
                    i = s.find(pat, i + 1)

    with gzip.open(GENOMA, "rt") as fh:
        for linea in fh:
            if linea.startswith(">"):
                if nombre is not None:
                    revisar(nombre, "".join(buf))
                nombre, buf = linea[1:].strip().split()[0], []
            else:
                buf.append(linea.strip().upper())
    if nombre is not None:
        revisar(nombre, "".join(buf))

    print("base pegada en la quimera ATPaseD_Dm + BicC_Dm:")
    print("   última base de ATPaseD_sel : %s" % atp[-1])
    print("   primera base de BicC_sel   : %s" % bicc[0])
    for k, v in hallazgos.items():
        print("\n%s -> %d aciertos en el ensamblado" % (k, len(v)))
        for h in v[:4]:
            print("   %s:%d (%s)  vecina anterior %s | vecina posterior %s" % (
                h["ref"], h["pos"], h["hebra"], h["flanco_anterior_3nt"] or "-",
                h["flanco_posterior_3nt"] or "-"))

    # la pregunta concreta: ¿la base que precede al inicio de BicC en el genoma
    # es la misma que la última base de ATPaseD que quedó pegada?
    veredicto = []
    for h in hallazgos["inicio_BicC_20nt"]:
        vecina = h["flanco_anterior_3nt"][-1:] if h["hebra"] == "+" else (
            rc(h["flanco_posterior_3nt"])[:1] if h["flanco_posterior_3nt"] else "")
        veredicto.append({"ref": h["ref"], "hebra": h["hebra"], "vecina_genomica": vecina,
                          "base_pegada": atp[-1], "coincide": vecina == atp[-1]})
    print("\n¿coincide la base pegada con la vecina genómica de BicC?")
    for v in veredicto:
        print("   %s (%s): genómica %s vs pegada %s -> %s" % (
            v["ref"], v["hebra"], v["vecina_genomica"] or "-", v["base_pegada"],
            "sí" if v["coincide"] else "no"))

    (RESULTADOS / "q3_empalme_contexto.json").write_text(json.dumps(
        {"ultima_base_ATPaseD_sel": atp[-1], "primera_base_BicC_sel": bicc[0],
         "hallazgos": hallazgos, "veredicto_base_pegada": veredicto},
        indent=2, ensure_ascii=False), encoding="utf-8")
    print("\nescrito en %s" % (RESULTADOS / "q3_empalme_contexto.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

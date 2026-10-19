"""Tests de las features biofisicas de sirna_enumerar.py.

Por que existe: todo el ranking se apoya en que asimetria, accesibilidad y GC esten bien
calculadas. Si la asimetria tiene el signo invertido, el pipeline entero rankea al reves y
no hay forma de darse cuenta mirando la salida, porque no tenemos datos de eficacia contra
que comparar.

No se valida biologia aca (para eso harian falta datos de eficacia que para esta especie no
existen). Se valida que **la implementacion haga lo que dice hacer**, con casos construidos
donde la respuesta correcta se sabe de antemano.

Uso:
    python3 test_features.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from sirna_enumerar import (VENTANA, accesibilidad, corrida_maxima, deseabilidad_gc,  # noqa: E402
                            dg_extremo, enumerar, revcomp)

fallos: list[str] = []


def check(nombre: str, condicion: bool, detalle: str = "") -> None:
    print(f"  {'OK  ' if condicion else 'FALLA'}  {nombre}" + (f"  [{detalle}]" if detalle else ""))
    if not condicion:
        fallos.append(nombre)


def main() -> None:
    print("revcomp")
    check("complementa y revierte", revcomp("ACGT") == "ACGT", "palindromo")
    check("no es solo reversa", revcomp("AAAA") == "TTTT")
    check("es su propia inversa", revcomp(revcomp("ACGTTGCA")) == "ACGTTGCA")

    print("\ncorridas de nucleotidos iguales")
    check("detecta corrida de 5", corrida_maxima("ACGTAAAAACG") == 5)
    check("sin corridas da 1", corrida_maxima("ACGTACGT") == 1)
    check("toda igual", corrida_maxima("GGGG") == 4)

    print("\ndeseabilidad del GC")
    check("dentro del rango ideal vale 1", deseabilidad_gc(0.45) == 1.0)
    check("cae fuera del rango", deseabilidad_gc(0.20) < 1.0)
    check("nunca es negativa", deseabilidad_gc(0.0) >= 0.0 and deseabilidad_gc(1.0) >= 0.0)
    check("es simetrica hacia los dos lados",
          abs(deseabilidad_gc(0.36 - 0.1) - deseabilidad_gc(0.52 + 0.1)) < 1e-9)

    print("\nestabilidad de extremos (ViennaRNA)")
    # Un extremo AU es mas debil (menos negativo) que uno GC. Si esto se invierte, la
    # asimetria cambia de signo y el ranking entero sale al reves.
    dg_au = dg_extremo("ATAT")
    dg_gc = dg_extremo("GCGC")
    check("extremo GC es mas estable que AU", dg_gc < dg_au, f"GC={dg_gc:.2f} AU={dg_au:.2f}")

    print("\nasimetria termodinamica, el signo importa")
    # Guia con 5' debil (AU) y 3' fuerte (GC) = la hebra guia se carga bien = asimetria positiva.
    buena = "ATATATATATATAGCGCGCGC"      # sitio blanco; la guia es su reverso complementario
    guia_buena = revcomp(buena)
    asim_buena = dg_extremo(guia_buena[:4]) - dg_extremo(buena[:4])
    mala = revcomp(buena)                 # el caso espejo
    guia_mala = revcomp(mala)
    asim_mala = dg_extremo(guia_mala[:4]) - dg_extremo(mala[:4])
    check("el caso bueno y el espejo tienen signo opuesto",
          asim_buena * asim_mala < 0, f"{asim_buena:+.2f} vs {asim_mala:+.2f}")

    print("\naccesibilidad (RNAplfold)")
    # Una horquilla fuerte deberia estar menos accesible que una region sin estructura.
    horquilla = "GGGGCCCCGGGGCCCCGGGGCCCCGGGGCCCC" * 3
    suelta = "AAAAAAAATTTTTTTTAAAAAAAATTTTTTTT" * 3
    acc_horquilla = sum(accesibilidad(horquilla)) / len(accesibilidad(horquilla))
    acc_suelta = sum(accesibilidad(suelta)) / len(accesibilidad(suelta))
    check("region estructurada es menos accesible que una suelta",
          acc_horquilla < acc_suelta, f"horquilla={acc_horquilla:.3f} suelta={acc_suelta:.3f}")

    print("\nenumeracion de ventanas")
    cds = "ATGGCTAGCTAGCTAGCATCGATCGTAGCTAGCTAGCATCGATCGATCGTAGCTAGCATCG"
    filas = enumerar(cds)
    check("saca todas las ventanas posibles", len(filas) == len(cds) - VENTANA + 1,
          f"{len(filas)} de {len(cds) - VENTANA + 1}")
    check("la guia es el reverso complementario del sitio",
          all(f["guia"] == revcomp(f["sitio"]) for f in filas))
    check("todas las ventanas miden 21 nt", all(len(f["sitio"]) == VENTANA for f in filas))
    check("las posiciones arrancan en 1 y son consecutivas",
          [f["pos"] for f in filas] == list(range(1, len(filas) + 1)))
    check("el GC esta entre 0 y 1", all(0 <= f["gc"] <= 1 for f in filas))
    check("hay ventana con N descartada",
          not any("N" in f["sitio"] for f in enumerar("ATGNNNGCTAGCTAGCATCGATCGTAGCTAGCTAGC")))

    print(f"\n{'TODO OK' if not fallos else 'FALLARON: ' + ', '.join(fallos)}")
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()

"""O4 paso 0 — el FASTA de consultas con los dos genes **enteros**, para el tamizado.

Por que existe. El tamizado del panel de seis que dejo `O3` cubre `V-ATPase B` entero pero
de `BicC_Dm` solo su region de 300 nt (`BicC_Dm_sel`, 280 ventanas), y para enumerar
fragmentos a lo largo del gen hace falta la mascara de veto del **gen completo**: 2.500
ventanas. `mascara.py` aborta si el tamizado no cubre el gen entero, justamente para que
este faltante no pase en silencio y no se lea una grilla podada con una mascara parcial.

Que hace: concatena los dos FASTA de gen completo en una consulta unica, con el nombre de
cabecera que `offtarget_21nt.py` usa como identificador de la consulta. Nada mas.

**La salida no se versiona**: son las secuencias de los dos genes, y `BicC_Dm` es una de las
cuatro de EPILAB. Vive en `work/O4/fasta/`, que `work/` no versiona, y el `.gitignore` del
bloque rechaza `*.fasta` por si alguien la copia adentro del arbol.

Uso (desde la raiz del repositorio):
    python research/ola6/O4_enumerador_quimeras/scripts/00_consultas.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
SALIDA = RAIZ / "work/O4/fasta/consultas_genes_enteros.fasta"
#: Los dos genes de la quimera de `D67`: reproduccion y movilidad. El CDS de `V-ATPase B`
#: lo regenera `research/ola6/O2_vatpase_b/scripts/02_extraer_cds.py` si no esta.
GENES = ["work/O3/fasta/BicC_Dm_full.fasta",
         "work/O3/fasta/VATPaseB_Dm_full.fasta"]
VENTANA = 21


def main() -> int:
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    with SALIDA.open("w", encoding="utf-8") as fh:
        for ruta in GENES:
            p = RAIZ / ruta
            if not p.exists():
                raise SystemExit(
                    "falta %s. El CDS de V-ATPase B no se versiona: regeneralo con "
                    "research/ola6/O2_vatpase_b/scripts/02_extraer_cds.py" % p)
            lineas = p.read_text().splitlines()
            nombre = lineas[0][1:].split()[0]
            seq = "".join(l.strip() for l in lineas[1:] if not l.startswith(">"))
            fh.write(">%s\n" % nombre)
            for i in range(0, len(seq), 60):
                fh.write(seq[i:i + 60] + "\n")
            print("%-46s %5d nt  %5d ventanas" % (nombre, len(seq), len(seq) - VENTANA + 1))
    print("escrito en %s (no se versiona)" % SALIDA)
    return 0


if __name__ == "__main__":
    sys.exit(main())

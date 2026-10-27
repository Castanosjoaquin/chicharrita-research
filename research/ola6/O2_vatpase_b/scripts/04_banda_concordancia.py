#!/usr/bin/env python3
"""O2 paso 4 — la banda de concordancia del CDS candidato contra los dos parientes.

Compara el CDS de V-ATPase B recuperado del genoma de *D. maidis* con el CDS anotado
de la misma subunidad en los dos cicadelidos con genoma anotado. La comparacion es
**codon a codon sin huecos**, y eso se puede hacer solo porque las tres secuencias
codificantes miden lo mismo y el alineamiento de proteina no tiene inserciones ni
deleciones; el script lo verifica antes de medir y aborta si no se cumple.

Unidades, para que el numero sea comparable con lo ya medido en el repo:
  - identidad de nucleotido sobre el CDS completo (C5 midio 77-84 % entre generos de
    cicadelidos; C11 midio 83,0-92,5 % en 11 familias, 88,2 % para V-ATPase B);
  - tramo exacto maximo en nt (C11: 74 nt para V-ATPase B);
  - ventanas de 21 nt identicas, en las dos hebras (C11: 233, el 10,9 %).

Uso: python3 04_banda_concordancia.py <dir_O2>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

COMP = str.maketrans("ACGTacgtNn", "TGCAtgcaNn")


def leer(p: Path) -> str:
    return "".join(l.strip() for l in p.read_text().splitlines()[1:]
                   if l.strip() and not l.startswith(">")).upper()


def ventanas(seq: str, k: int = 21) -> set[str]:
    return {seq[i:i + k] for i in range(len(seq) - k + 1)}


def medir(dm: str, otro: str) -> dict:
    if len(dm) != len(otro):
        sys.exit(f"ABORTA: largos distintos ({len(dm)} vs {len(otro)}); "
                 "la comparacion sin huecos no es valida")
    iguales = sum(1 for a, b in zip(dm, otro) if a == b)
    racha = mejor = 0
    for a, b in zip(dm, otro):
        racha = racha + 1 if a == b else 0
        mejor = max(mejor, racha)
    vdm = ventanas(dm)
    votro = ventanas(otro) | ventanas(otro.translate(COMP)[::-1])
    comunes = len(vdm & votro)
    return {
        "largo_nt": len(dm),
        "identidad_nt_pct": round(100 * iguales / len(dm), 2),
        "nt_iguales": iguales,
        "tramo_exacto_max_nt": mejor,
        "ventanas21_identicas": comunes,
        "ventanas21_totales": len(dm) - 20,
        "pct_ventanas21": round(100 * comunes / (len(dm) - 20), 2),
    }


def main() -> None:
    o2 = Path(sys.argv[1])
    dm = leer(o2 / "resultados" / "VATPaseB_Dm_cds.fna")
    pares = {
        "Macrosteles_quadrilineatus_XM_054432770.1":
            o2 / "consultas" / "Mq_XM_054432770.1_cds.fna",
        "Homalodisca_vitripennis_XM_046812795.1":
            o2 / "consultas" / "Hv_XM_046812795.1_cds.fna",
    }
    salida = {"cds_dmaidis_nt": len(dm), "comparaciones": {}}
    for nombre, ruta in pares.items():
        salida["comparaciones"][nombre] = medir(dm, leer(ruta))

    destino = o2 / "resultados" / "banda_concordancia.json"
    destino.write_text(json.dumps(salida, indent=2, ensure_ascii=True) + "\n", newline="\n")
    print(json.dumps(salida, indent=2))


if __name__ == "__main__":
    main()

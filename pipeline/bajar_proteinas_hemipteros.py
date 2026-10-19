"""Baja de UniProt las proteinas de los blancos de RNAi curados en hemipteros.

La tabla curada (`datos/rnai_hemipteros.csv`) tiene especie + nombre de gen tal
como lo escribe cada paper. UniProt no siempre los tiene con ese nombre, asi que
se prueban varias consultas, de la mas estricta a la mas laxa, y **se anota cual
funciono**. Eso importa: una secuencia tomada de otra especie que la del paper no
es la misma evidencia, y la columna `fuente_secuencia` lo deja ver en la tabla
final en vez de esconderlo.

Orden de intentos por fila:
  1. misma especie + gene:<nombre>           -> "especie exacta, por gen"
  2. misma especie + nombre largo en texto   -> "especie exacta, por nombre"
  3. misma especie + nombre de gen sin prefijo (Nl/Sf/Ls/Ap/Dc/Rp/Nc/Btab)
  4. cualquier Hemiptera + nombre largo      -> "otro hemiptero" (degradado)

Uso:
    python3 bajar_proteinas_hemipteros.py <tabla.csv> <salida.faa> [--mapa mapa.csv]
"""

from __future__ import annotations

import csv
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://rest.uniprot.org/uniprotkb/search"
PREFIJOS = re.compile(r"^(Nl|Sf|Ls|Ap|Apis|Dc|Rp|Nc|Btab|Pm)[-_]?", re.I)


def consultar(query: str, limite: int = 1) -> list[tuple[str, str]]:
    url = f"{API}?" + urllib.parse.urlencode({
        "query": query, "format": "fasta", "size": str(limite)})
    try:
        with urllib.request.urlopen(url, timeout=120) as r:
            texto = r.read().decode("utf-8", "replace")
    except Exception:
        return []
    salida = []
    for bloque in texto.split(">")[1:]:
        lineas = bloque.split("\n")
        salida.append((lineas[0], "".join(lineas[1:]).strip().rstrip("*")))
    return salida


def intentos(fila: dict) -> list[tuple[str, str]]:
    sp = fila["especie"]
    gen = fila["gen"].strip()
    largo = fila["nombre_largo"].strip()
    desnudo = PREFIJOS.sub("", gen)
    # El nucleo del nombre largo: sin numeros de copia ni parentesis. "beta-N-
    # acetylhexosaminidase 3" -> "acetylhexosaminidase". Sirve de red de arrastre.
    nucleo = re.sub(r"[\d()/:,].*$", "", largo).strip()
    nucleo = nucleo.split()[-1] if nucleo.split() else largo
    return [
        (f'(organism_name:"{sp}") AND (gene:{gen})', "especie exacta, por gen"),
        (f'(organism_name:"{sp}") AND (gene:{desnudo})', "especie exacta, gen sin prefijo"),
        (f'(organism_name:"{sp}") AND ("{gen}")', "especie exacta, simbolo en texto"),
        (f'(organism_name:"{sp}") AND (protein_name:"{largo}")', "especie exacta, por nombre"),
        (f'(organism_name:"{sp}") AND ("{largo}")', "especie exacta, texto libre"),
        (f'(organism_name:"{sp}") AND ("{nucleo}")', "especie exacta, nucleo del nombre"),
        (f'(taxonomy_name:Hemiptera) AND (protein_name:"{largo}") AND (reviewed:false)',
         "OTRO HEMIPTERO (degradado)"),
        (f'(taxonomy_name:Hemiptera) AND ("{nucleo}") AND (reviewed:false)',
         "OTRO HEMIPTERO (degradado)"),
    ]


def main() -> int:
    tabla = Path(sys.argv[1])
    salida = Path(sys.argv[2])
    mapa_ruta = None
    if "--mapa" in sys.argv:
        mapa_ruta = Path(sys.argv[sys.argv.index("--mapa") + 1])

    filas = list(csv.DictReader(tabla.open(encoding="utf-8")))
    mapa = []
    secuencias: dict[str, str] = {}

    for i, fila in enumerate(filas, 1):
        # Un id corto y estable por fila, que es lo que va al FASTA y despues
        # sale en el GFF de miniprot.
        ident = f"H{i:03d}"
        encontrado = None
        for query, etiqueta in intentos(fila):
            res = consultar(query)
            time.sleep(0.25)
            if res:
                encontrado = (etiqueta, res[0])
                break
        if encontrado is None:
            print(f"[--] {ident} {fila['especie']:<24}{fila['gen']:<22}sin secuencia")
            mapa.append({**fila, "id": ident, "uniprot": "", "fuente_secuencia": "no encontrada",
                         "largo_aa": 0})
            continue
        etiqueta, (header, seq) = encontrado
        acc = header.split("|")[1] if "|" in header else header.split()[0]
        secuencias[ident] = seq
        mapa.append({**fila, "id": ident, "uniprot": acc,
                     "fuente_secuencia": etiqueta, "largo_aa": len(seq)})
        marca = "!!" if etiqueta.startswith("OTRO") else "ok"
        print(f"[{marca}] {ident} {fila['especie']:<24}{fila['gen']:<22}"
              f"{acc:<12}{len(seq):>5} aa  {etiqueta}")

    with salida.open("w") as f:
        for ident, seq in secuencias.items():
            f.write(f">{ident}\n")
            for j in range(0, len(seq), 60):
                f.write(seq[j:j + 60] + "\n")

    print(f"\n{len(secuencias)} de {len(filas)} filas con secuencia -> {salida}")
    degradadas = sum(1 for m in mapa if m["fuente_secuencia"].startswith("OTRO"))
    print(f"de otra especie que la del paper (degradadas): {degradadas}")

    if mapa_ruta:
        with mapa_ruta.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(mapa[0].keys()))
            w.writeheader()
            w.writerows(mapa)
        print(f"mapa escrito en {mapa_ruta}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

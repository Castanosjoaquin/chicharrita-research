#!/usr/bin/env python3
"""W4 - busqueda dirigida de genes en un ensamblado SIN anotacion, por proteina ortologa.

Selecciona de un proteoma de referencia anotado (RefSeq de un cicadelido) las
proteinas cuyo nombre coincide con una lista de patrones, y las alinea con
miniprot contra el ensamblado del vector. Sirve para mostrar que un genoma sin
anotacion igual permite ubicar genes concretos.

Uso: python3 07_busqueda_ortologos.py <genoma.fna> <proteoma.faa> <prefijo> <patron1,patron2,...> [hilos]
"""
import json, re, subprocess, sys

def seleccionar(faa, patrones, destino):
    pats = [re.compile(p, re.I) for p in patrones]
    n, escr = 0, 0
    escribir = False
    with open(faa) as fh, open(destino, "w") as out:
        for linea in fh:
            if linea.startswith(">"):
                n += 1
                escribir = any(p.search(linea) for p in pats)
                escr += escribir
            if escribir:
                out.write(linea)
    return n, escr

def main():
    genoma, faa, pref, patrones = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4].split(",")
    hilos = sys.argv[5] if len(sys.argv) > 5 else "8"
    sel = pref + "_consulta.faa"
    n, escr = seleccionar(faa, patrones, sel)
    print(f"proteoma {faa}: {n} proteinas, {escr} seleccionadas por nombre", flush=True)
    paf = pref + ".paf"
    with open(paf, "w") as fh:
        subprocess.run(["miniprot", "-t", hilos, "--outn", "3", genoma, sel], stdout=fh, check=True)
    filas = []
    for linea in open(paf):
        if linea.startswith("##") or not linea.strip():
            continue
        c = linea.rstrip("\n").split("\t")
        if len(c) < 12:
            continue
        ident = [x for x in c if x.startswith("ms:i:")]
        filas.append({"consulta": c[0], "largo_prot": int(c[1]),
                      "cobertura": round((int(c[3]) - int(c[2])) / int(c[1]), 3),
                      "scaffold": c[5], "inicio": int(c[7]), "fin": int(c[8]),
                      "hebra": c[4], "coincidencias_aa": int(c[9]), "bloque_aa": int(c[10])})
    mejor = {}
    for f in filas:
        if f["consulta"] not in mejor or f["cobertura"] > mejor[f["consulta"]]["cobertura"]:
            mejor[f["consulta"]] = f
    json.dump({"genoma": genoma, "proteoma": faa, "n_consultas": escr,
               "n_con_alineacion": len(mejor), "mejores": list(mejor.values())},
              open(pref + ".json", "w"), indent=1)
    print(f"consultas con alineacion: {len(mejor)}/{escr}")
    for f in sorted(mejor.values(), key=lambda x: -x["cobertura"])[:40]:
        print(f'{f["cobertura"]:.2f}\t{f["scaffold"]}:{f["inicio"]}-{f["fin"]}\t{f["consulta"][:90]}')

if __name__ == "__main__":
    main()

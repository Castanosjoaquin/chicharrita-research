#!/usr/bin/env python3
"""C5 / Q3 — Cuantos genes recupera el circuito en el genoma NO anotado.

Entrada: el CSV de pipeline/resumir_miniprot.py sobre el GFF de la corrida 01
(proteoma RefSeq de Macrosteles quadrilineatus vs GCA_975739785.1).

Define y cuenta tres cosas distintas, porque "genes recuperados" es ambiguo:
  (a) proteinas consulta con al menos un locus  -> incluye isoformas del mismo gen
  (b) loci distintos: intervalos solapados del mejor hit de cada proteina, fusionados
      por cromosoma y hebra -> aproximacion a "genes"
  (c) lo mismo que (b) filtrando por identidad del alineamiento

Uso: python3 05_contar_genes_recuperados.py <loci.csv> [--json salida.json]
"""
import csv, json, sys
from collections import defaultdict

def cargar(ruta):
    with open(ruta, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))

def mejor_por_proteina(filas):
    mejor = {}
    for f in filas:
        p = f["proteina"]
        if p not in mejor or float(f["score"]) > float(mejor[p]["score"]):
            mejor[p] = f
    return mejor

def fusionar(hits, min_ident=0.0, por_hebra=True):
    """Fusiona intervalos solapados; devuelve la lista de loci."""
    por_clave = defaultdict(list)
    for h in hits:
        if float(h["identidad"]) < min_ident:
            continue
        clave = (h["cromosoma"], h["hebra"]) if por_hebra else (h["cromosoma"],)
        por_clave[clave].append((int(h["inicio"]), int(h["fin"]), h["proteina"]))
    loci = []
    for clave, iv in por_clave.items():
        iv.sort()
        ini, fin, prots = iv[0][0], iv[0][1], [iv[0][2]]
        for a, b, p in iv[1:]:
            if a <= fin:                 # solapan
                fin = max(fin, b); prots.append(p)
            else:
                loci.append((clave, ini, fin, prots)); ini, fin, prots = a, b, [p]
        loci.append((clave, ini, fin, prots))
    return loci

def main():
    ruta = sys.argv[1]
    filas = cargar(ruta)
    mejor = mejor_por_proteina(filas)
    hits = list(mejor.values())
    out = {
        "archivo": ruta,
        "alineamientos_totales": len(filas),
        "proteinas_consulta_con_locus": len(mejor),
        "loci_fusionados_por_hebra": len(fusionar(hits)),
        "loci_fusionados_sin_hebra": len(fusionar(hits, por_hebra=False)),
    }
    for u in (0.5, 0.7, 0.8, 0.9, 0.99):
        out[f"loci_identidad_ge_{u}"] = len(fusionar(hits, min_ident=u))
        out[f"proteinas_identidad_ge_{u}"] = sum(1 for h in hits if float(h["identidad"]) >= u)
    ident = sorted(float(h["identidad"]) for h in hits)
    out["identidad_mediana"] = ident[len(ident)//2]
    out["identidad_p10"], out["identidad_p90"] = ident[len(ident)//10], ident[9*len(ident)//10]
    out["loci_limpios"] = sum(1 for h in hits if h["frameshift"] == "0" and h["stop_interno"] == "0")
    for k, v in out.items():
        print(f"{k:<34} {v}")
    if "--json" in sys.argv:
        json.dump(out, open(sys.argv[sys.argv.index("--json")+1], "w"), indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()

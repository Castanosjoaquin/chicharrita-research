#!/usr/bin/env python3
"""W4 - completitud estilo BUSCO calculada localmente con miniprot (proxy, NO es BUSCO oficial).

Alinea las proteinas 'ancestral_variants' del linaje insecta_odb10 contra un
ensamblado y clasifica cada uno de los 1.367 ortologos del linaje segun la
cobertura de la mejor alineacion:

  completo    cobertura de la proteina de referencia >= 0.70
  fragmentado 0.30 <= cobertura < 0.70
  ausente     cobertura < 0.30 o sin alineacion
  duplicado   dos o mas loci sin solapamiento con cobertura >= 0.70

Los umbrales son nuestros y estan declarados: compleasm/BUSCO usan cortes por
ortologo derivados de 'lengths_cutoff', de modo que los numeros son comparables
en orden de magnitud pero no identicos a un BUSCO oficial.

Uso: python3 06_completitud_miniprot.py <genoma.fna> <linaje_dir> <salida_prefijo> [hilos]
"""
import json, os, subprocess, sys
from collections import defaultdict

COMPLETO, FRAG = 0.70, 0.30

def correr_miniprot(genoma, prots, paf, hilos):
    with open(paf, "w") as fh:
        subprocess.run(["miniprot", "-t", str(hilos), "--outn", "5", genoma, prots],
                       stdout=fh, check=True)

def parsear(paf):
    """PAF de miniprot: qname qlen qstart qend strand tname tlen tstart tend ..."""
    hits = defaultdict(list)
    with open(paf) as fh:
        for linea in fh:
            if linea.startswith("##") or not linea.strip():
                continue
            c = linea.rstrip("\n").split("\t")
            if len(c) < 12:
                continue
            qname, qlen, qs, qe = c[0], int(c[1]), int(c[2]), int(c[3])
            tname, ts, te = c[5], int(c[7]), int(c[8])
            busco = qname.split("_")[0]
            hits[busco].append({"var": qname, "cob": (qe - qs) / qlen,
                                "t": tname, "ts": ts, "te": te})
    return hits

def clasificar(hits, n_total):
    res = {"completo": 0, "duplicado": 0, "fragmentado": 0, "ausente": 0}
    detalle = {}
    for busco, hs in hits.items():
        mejor = max(h["cob"] for h in hs)
        if mejor >= COMPLETO:
            loci, buenos = [], sorted([h for h in hs if h["cob"] >= COMPLETO],
                                      key=lambda h: -h["cob"])
            for h in buenos:
                if not any(h["t"] == l["t"] and h["ts"] < l["te"] and l["ts"] < h["te"] for l in loci):
                    loci.append(h)
            clase = "duplicado" if len(loci) > 1 else "completo"
        elif mejor >= FRAG:
            clase = "fragmentado"
        else:
            clase = "ausente"
        res[clase] += 1
        detalle[busco] = {"clase": clase, "cobertura_mejor": round(mejor, 3)}
    res["ausente"] += n_total - len(hits)
    return res, detalle

def main():
    genoma, linaje, pref = sys.argv[1], sys.argv[2], sys.argv[3]
    hilos = sys.argv[4] if len(sys.argv) > 4 else "8"
    prots = os.path.join(linaje, "ancestral_variants")
    n_total = int([l.split("=")[1] for l in open(os.path.join(linaje, "dataset.cfg"))
                   if l.startswith("number_of_BUSCOs")][0])
    paf = pref + ".paf"
    if not os.path.exists(paf):
        correr_miniprot(genoma, prots, paf, hilos)
    hits = parsear(paf)
    res, detalle = clasificar(hits, n_total)
    res_pct = {k: round(100 * v / n_total, 2) for k, v in res.items()}
    salida = {"genoma": genoma, "linaje": os.path.basename(linaje.rstrip("/")),
              "n_ortologos_linaje": n_total, "conteos": res, "porcentajes": res_pct,
              "umbral_completo": COMPLETO, "umbral_fragmentado": FRAG,
              "herramienta": "miniprot (proxy declarado; no es BUSCO ni compleasm oficial)"}
    with open(pref + ".json", "w") as fh:
        json.dump({"resumen": salida, "detalle": detalle}, fh, indent=1)
    print(json.dumps(salida, ensure_ascii=False))

if __name__ == "__main__":
    main()

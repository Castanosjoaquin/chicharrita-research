#!/usr/bin/env python3
"""W4 - recorre work/W4/downloads y calcula metricas de cada FASTA y cada GFF.

Uso:  python3 05_inventario_metricas.py <dir_descargas> <salida.jsonl>
Llama a las funciones de 04_metricas.py (mismo directorio).
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location(
    "m04", os.path.join(os.path.dirname(os.path.abspath(__file__)), "04_metricas.py"))
m04 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m04)

CLASE = {"_genomic.fna": "genoma", "rna.fna": "transcriptos",
         "cds_from_genomic.fna": "cds", "protein.faa": "proteinas", "genomic.gff": "anotacion_gff"}

def clasificar(nombre):
    if nombre.startswith("cds_from_genomic"):
        return "cds"
    if nombre.endswith("_genomic.fna"):
        return "genoma"
    for k, v in CLASE.items():
        if nombre == k or nombre.endswith(k):
            return v
    return None

def main(raiz, dest):
    salida = []
    for acc in sorted(os.listdir(raiz)):
        d = os.path.join(raiz, acc, "ncbi_dataset", "data", acc)
        if not os.path.isdir(d):
            continue
        for nombre in sorted(os.listdir(d)):
            clase = clasificar(nombre)
            if not clase:
                continue
            ruta = os.path.join(d, nombre)
            t0 = time.time()
            if clase == "anotacion_gff":
                res = m04.metricas_gff(ruta)
            elif clase == "proteinas":
                res = m04.metricas_fasta(ruta, alfabeto="aa")
            else:
                res = m04.metricas_fasta(ruta)
            res = {"accesion": acc, "clase": clase, "segundos": round(time.time() - t0, 1), **res}
            salida.append(res)
            print(f"{acc:18s} {clase:14s} {res.get('n_secuencias', res.get('n_genes'))}", flush=True)
    with open(dest, "w") as fh:
        for r in salida:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

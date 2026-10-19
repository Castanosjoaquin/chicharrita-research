import csv, sys, time
from pathlib import Path
P = "/mnt/c/Proyectos/yHat/pipeline"
sys.path.insert(0, P)
from cadena_completa import (indexar_gff_por_locus, buscar_mrna, leer_cromosoma, armar_cds, enumerar, puntuar,
                             GENOMA, GFF_TCAS, NO_OBJETIVO, SALIDA)
from sirna_offtarget import K, K_ALERTA, cargar_candidatos, escanear, semillas_alerta
N = int(sys.argv[1]); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
cands = list(csv.DictReader((SALIDA / "candidatos_alto.csv").open(encoding="utf-8")))
indice = indexar_gff_por_locus(GFF_TCAS)
cache = {}; todas = []
t0 = time.time()
for cand in cands:
    if len({f["locus"] for f in todas}) >= N: break
    h = buscar_mrna(indice, cand["cromosoma"], int(cand["inicio"]), int(cand["fin"]))
    if not h: continue
    ident, hebra, exones = h
    if cand["cromosoma"] not in cache:
        cache[cand["cromosoma"]] = leer_cromosoma(GENOMA, cand["cromosoma"])
    cds = armar_cds(cache[cand["cromosoma"]], hebra, exones)
    if len(cds) < 600: continue
    filas = enumerar(cds); puntuar(filas)
    for f in filas:
        f["locus"] = cand["locus"]; f["gen"] = cand["gen_drosophila"] or cand["mejor_hit_tribolium"]
        f["tcas_frameshift"] = cand["tcas_frameshift"]; f["tcas_stop_interno"] = cand["tcas_stop_interno"]
    todas.extend(filas)
    (out / f"{cand['locus']}.fasta").write_text(">" + cand["locus"] + "\n" + cds + "\n")
    print(cand["locus"], len(cds), len(filas), round(time.time() - t0), flush=True)
tmp = out / "_todas.csv"
with tmp.open("w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(todas[0].keys())); w.writeheader(); w.writerows(todas)
print("off-target sobre", len(todas), "ventanas", flush=True)
exactos = cargar_candidatos(tmp); semillas = semillas_alerta(exactos)
secuencias = {}
for k, cl in exactos.items():
    for c in cl: secuencias.setdefault(c, []).append(k)
peor = {}
for ruta in NO_OBJETIVO:
    if ruta.exists():
        r = escanear(ruta, exactos, semillas, secuencias, peor); print(r["archivo"], len(r["exactos"]), round(time.time() - t0), flush=True)
for f in todas:
    f["off_target_max"] = peor.get(f"{f['locus']}|{f['pos']}", 0)
    f["riesgo"] = "descartar" if f["off_target_max"] >= K else "alerta" if f["off_target_max"] >= 17 else "ok"
with (out / "ventanas_multigen.csv").open("w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(todas[0].keys())); w.writeheader(); w.writerows(todas)
print("listo", len(todas), round(time.time() - t0))

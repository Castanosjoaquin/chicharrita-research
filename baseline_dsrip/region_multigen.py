"""Region de 300 pb en 20 genes: agregaciones, off-target a nivel region, y contra dsRIP (con y sin ORF)."""
import csv
import json
import sys
from collections import defaultdict

import numpy as np
from scipy import stats

sys.path.insert(0, r"C:\Proyectos\yHat\pipeline")
import region_scoring as rs  # noqa: E402

M = r"C:\Proyectos\yHat\investigathon\dsrip_baseline\multigen"
LARGO = 301
genes = rs.leer_ventanas(__import__("pathlib").Path(M + r"\ventanas_multigen.csv"))
resumen = json.load(open(M + r"\dsrip_resumen.json"))

print(f"{len(genes)} genes, {sum(len(v) for v in genes.values())} ventanas")
tot = defaultdict(int)
for filas in genes.values():
    for f in filas:
        tot[f["riesgo"]] += 1
print("riesgo off-target por ventana:", dict(tot))

filas_rep = []
for locus, filas in genes.items():
    d = {int(r["code"].split("_")[-2]): r for r in csv.DictReader(open(M + rf"\dsrip_{locus}.csv"))}
    reg = rs.regiones_de_un_gen(filas, LARGO, 1, 75, "score")
    # puntaje dsRIP por ventana, mismas posiciones
    fd = [{"pos": f["pos"], "score": float(d[int(f["pos"])]["total_score"]), "descarte": ""} for f in filas]
    dreg = rs.regiones_de_un_gen(fd, LARGO, 1, 75, "score")
    mej = {a: max(reg, key=lambda r: float(r[a])) for a in ("media", "frac_buenos", "buenos_limpios")}
    dm = max(dreg, key=lambda r: float(r["media"]))
    dsr_json = resumen[locus]["regiones"]
    def rango_dsrip(k):
        r = dsr_json[k]
        a = int(r["start_siRNA"].split("_")[-2]); b = int(r["end_siRNA"].split("_")[-2])
        return (a, b + 20)
    dr_orf, dr_all = rango_dsrip("only_ORF=True"), rango_dsrip("only_ORF=False")
    # nuestra mejor region restringida a las ventanas que dsRIP marca como ORF
    orf_pos = {p for p, r in d.items() if r["ORF_info"] == "ORF"}
    filas_orf = [f for f in filas if int(f["pos"]) in orf_pos]
    reg_orf = rs.regiones_de_un_gen(filas_orf, LARGO, 1, 75, "score") if len(filas_orf) > 281 else []
    mej_orf = max(reg_orf, key=lambda r: float(r["media"])) if reg_orf else None
    # off-target a nivel region
    n_desc_en_mejor = mej["media"]["n_off_descartar"]
    frac_regiones_con_desc = np.mean([1 if r["n_off_descartar"] > 0 else 0 for r in reg])
    frac_regiones_con_alerta = np.mean([1 if r["n_off_alerta"] > 0 else 0 for r in reg])
    # correlacion de ventanas y de regiones con dsRIP
    rho_v = stats.spearmanr([float(f["score"]) for f in filas], [x["score"] for x in fd])[0]
    rho_r = stats.spearmanr([r["media"] for r in reg], [r["media"] for r in dreg])[0]
    ov = lambda a, b: rs.solape((a["inicio"], a["fin"]), b)
    filas_rep.append({
        "locus": locus, "cds": len(filas) + 20, "ventanas_5UTR": resumen[locus]["etiquetas"].get("5_UTR", 0),
        "rho_ventanas": rho_v, "rho_regiones": rho_r,
        "solape_media_dsrip": ov(mej["media"], dr_all) / LARGO,
        "solape_buenos_dsrip": ov(mej["frac_buenos"], dr_all) / LARGO,
        "solape_limpios_dsrip": ov(mej["buenos_limpios"], dr_all) / LARGO,
        "dsrip_orf_vs_todo": rs.solape(dr_orf, dr_all) / LARGO,
        "solape_nuestra_orf_vs_todo": (ov(mej_orf, (mej["media"]["inicio"], mej["media"]["fin"])) / LARGO) if mej_orf else None,
        "solape_nuestra_orf_vs_dsrip_orf": (ov(mej_orf, dr_orf) / LARGO) if mej_orf else None,
        "solape_media_vs_buenos": rs.solape((mej["media"]["inicio"], mej["media"]["fin"]), (mej["frac_buenos"]["inicio"], mej["frac_buenos"]["fin"])) / LARGO,
        "solape_buenos_vs_limpios": rs.solape((mej["frac_buenos"]["inicio"], mej["frac_buenos"]["fin"]), (mej["buenos_limpios"]["inicio"], mej["buenos_limpios"]["fin"])) / LARGO,
        "desc_en_mejor_media": n_desc_en_mejor, "desc_en_mejor_limpios": mej["buenos_limpios"]["n_off_descartar"],
        "alerta_en_mejor_media": mej["media"]["n_off_alerta"], "alerta_en_mejor_limpios": mej["buenos_limpios"]["n_off_alerta"],
        "frac_regiones_con_desc": frac_regiones_con_desc, "frac_regiones_con_alerta": frac_regiones_con_alerta,
        "mejor_vs_media_gen": mej["media"]["media"] / (sum(float(f["score"]) for f in filas) / len(filas)) - 1,
    })

with open(M + r"\..\region_multigen_resultados.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(filas_rep[0].keys())); w.writeheader(); w.writerows(filas_rep)

def col(k): return np.array([r[k] for r in filas_rep if r[k] is not None], dtype=float)
def res(k, f=lambda x: x):
    v = col(k); print(f"  {k:<34} mediana {f(np.median(v)):.2f}  media {f(v.mean()):.2f}  min {f(v.min()):.2f}  max {f(v.max()):.2f}  (n={len(v)})")

print("\n-- acuerdo con dsRIP --")
res("rho_ventanas"); res("rho_regiones")
for k in ("solape_media_dsrip", "solape_buenos_dsrip", "solape_limpios_dsrip"): res(k)
print("  genes con solape >=75 %:", {k: int((col(k) >= .75).sum()) for k in ("solape_media_dsrip", "solape_buenos_dsrip", "solape_limpios_dsrip")})
print("  genes con solape 0 :", {k: int((col(k) == 0).sum()) for k in ("solape_media_dsrip", "solape_buenos_dsrip", "solape_limpios_dsrip")})
print("\n-- efecto de restringir a ORF --")
print("  genes con ventanas '5_UTR' segun dsRIP:", sum(1 for r in filas_rep if r["ventanas_5UTR"] > 0), "de", len(filas_rep))
res("dsrip_orf_vs_todo"); res("solape_nuestra_orf_vs_todo"); res("solape_nuestra_orf_vs_dsrip_orf")
for r in filas_rep:
    if r["ventanas_5UTR"] > 0 or (r["dsrip_orf_vs_todo"] < 1):
        print(f"    {r['locus']}: 5UTR {r['ventanas_5UTR']}  dsRIP ORF vs todo {r['dsrip_orf_vs_todo']:.2f}  nuestra ORF vs todo {r['solape_nuestra_orf_vs_todo']}  nuestra ORF vs dsRIP ORF {r['solape_nuestra_orf_vs_dsrip_orf']}")
print("\n-- agregaciones --")
res("solape_media_vs_buenos"); res("solape_buenos_vs_limpios")
print("\n-- off-target a nivel region --")
res("frac_regiones_con_desc"); res("frac_regiones_con_alerta")
print("  mejor region (por media) con >=1 ventana 'descartar' :", int((col("desc_en_mejor_media") > 0).sum()), "de", len(filas_rep))
print("  mejor region (por media) con >=1 ventana 'alerta'    :", int((col("alerta_en_mejor_media") > 0).sum()), "de", len(filas_rep))
print("  mejor region (buenos_limpios) con >=1 'descartar'    :", int((col("desc_en_mejor_limpios") > 0).sum()), "de", len(filas_rep))
print("  mejor region (buenos_limpios) con >=1 'alerta'       :", int((col("alerta_en_mejor_limpios") > 0).sum()), "de", len(filas_rep))
print("\n-- ganancia de la mejor region sobre la media del gen --")
res("mejor_vs_media_gen", lambda x: x * 100)

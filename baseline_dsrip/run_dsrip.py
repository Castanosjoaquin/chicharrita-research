import numpy as _np
_np.float = float  # shim: RNAtweaks 0.0.2 usa np.float, removido en numpy>=1.24
import os, sys, csv, json
code = os.path.expanduser("~/dsrip_dl/code")
work = os.path.expanduser("~/dsrip_dl/work")
os.makedirs(work + "/constant_files", exist_ok=True)
for f in ("lookup.db", "siRNA_parameters.txt"):
    dst = work + "/constant_files/" + f
    if not os.path.exists(dst):
        os.symlink(code + "/" + f, dst)
os.chdir(work)
sys.path.insert(0, code)
import dsRNA_efficiency as d

fasta = sys.argv[1]; out = sys.argv[2]
name, seq = d.read_fasta_file(fasta)[0]
print("gene", name, len(seq), "valid", d.check_valid_dna(seq))
cor = seq.replace("T", "U")
orf = d.ORF_siRNA(cor)
print("ORF_info", orf)
siRNAs, _ = d.generate_siRNA(cor, 21)
print("n siRNAs", len(siRNAs), "first", siRNAs[0])
acc = d.mRNA_accessibility(cor, 21)
feats = d.siRNA_feature_prediction(siRNAs, cor, name, 21, acc, orf, [])
res = d.score_and_update_siRNA_features({"siRNA_features": feats}, safety=False, safety_essential_coeff=20)["siRNA_features"]
rows = []
for k, v in res.items():
    r = {"code": k}; r.update({kk: vv for kk, vv in v.items() if kk not in ("self_fold_structure",)})
    rows.append(r)
with open(out, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("wrote", out, len(rows))

# etapa 2: seleccion de region, llamando a la funcion real de dsRIP
os.makedirs(work + "/u/efficiency", exist_ok=True)
sc = {"siRNA_features": res}
out2 = {}
for etiqueta, mn, mx in (("fijo_300pb", 281, 281), ("rango_defecto_300_800", 281, 781)):
    for only_orf in (True, False):
        r = d.find_best_siRNA_region(sc, mn, mx, only_orf, False, 50, 50, work + "/u")
        out2[f"{etiqueta}_onlyORF={only_orf}"] = {k: (str(v) if not isinstance(v, (int, float, type(None))) else v) for k, v in r.items()}
json.dump(out2, open(out.replace(".csv", "_regiones.json"), "w"), indent=1)
print(json.dumps(out2, indent=1))

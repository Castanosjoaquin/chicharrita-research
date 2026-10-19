import numpy as _np
_np.float = float
import os, sys, csv, json, glob
code = os.path.expanduser("~/dsrip_dl/code"); work = os.path.expanduser("~/dsrip_dl/work")
os.chdir(work); sys.path.insert(0, code)
import dsRNA_efficiency as d
os.makedirs(work + "/u/efficiency", exist_ok=True)
md = sys.argv[1]
resumen = {}
for fa in sorted(glob.glob(md + "/L*.fasta")):
    locus = os.path.basename(fa)[:-6]
    name, seq = d.read_fasta_file(fa)[0]
    name = locus
    cor = seq.replace("T", "U")
    orf = d.ORF_siRNA(cor)
    siRNAs, _ = d.generate_siRNA(cor, 21)
    acc = d.mRNA_accessibility(cor, 21)
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        feats = d.siRNA_feature_prediction(siRNAs, cor, name, 21, acc, orf, [])
    res = d.score_and_update_siRNA_features({"siRNA_features": feats}, safety=False, safety_essential_coeff=20)["siRNA_features"]
    rows = []
    for k, v in res.items():
        r = {"code": k, "locus": locus}; r.update({kk: vv for kk, vv in v.items() if kk != "self_fold_structure"}); rows.append(r)
    with open(f"{md}/dsrip_{locus}.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    reg = {}
    for only in (True, False):
        r = d.find_best_siRNA_region({"siRNA_features": res}, 281, 281, only, False, 50, 50, work + "/u")
        reg[f"only_ORF={only}"] = {k: (v if isinstance(v, (int, float, type(None))) else str(v)) for k, v in r.items()}
    labels = {}
    for r in rows: labels[r["ORF_info"]] = labels.get(r["ORF_info"], 0) + 1
    resumen[locus] = {"cds": len(seq), "orf_info": [str(x) if i in (1, 2, 3) else "" for i, x in enumerate(orf)][1:4], "etiquetas": labels, "regiones": reg}
    print(locus, len(seq), labels, flush=True)
json.dump(resumen, open(md + "/dsrip_resumen.json", "w"), indent=1)

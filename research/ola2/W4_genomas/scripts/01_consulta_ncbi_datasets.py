#!/usr/bin/env python3
"""W4 - consulta de metadatos de ensamblados en NCBI Datasets v2alpha.

Uso:  python3 01_consulta_ncbi_datasets.py <salida.json>
No sube ninguna secuencia: sólo consulta metadatos públicos por nombre de taxón.
"""
import json, sys, time, requests

API = "https://api.ncbi.nlm.nih.gov/datasets/v2alpha"

TAXA = [
    ("Dalbulus maidis",            "vector"),
    ("Dalbulus",                   "vector_genero"),
    ("Zea mays",                   "cultivo"),
    ("Spiroplasma kunkelii",       "patogeno"),
    # OJO: "maize bushy stunt phytoplasma" es el NOMBRE COMUN y devuelve 0 ensamblados.
    # El taxon es 'Candidatus Phytoplasma zeae', taxid 202462. Se consulta por taxid.
    ("202462",                     "patogeno"),
    ("Candidatus Phytoplasma zeae", "patogeno"),
    ("Candidatus Phytoplasma asteris", "patogeno"),
    ("Maize rayado fino virus",    "patogeno"),
    ("Mastrevirus striatis",       "patogeno"),
    ("Apis mellifera",             "no_objetivo"),
    ("Coccinella septempunctata",  "no_objetivo"),
    ("Chrysoperla carnea",         "no_objetivo"),
    ("Folsomia candida",           "no_objetivo"),
    ("Cicadellidae",               "cicadelidos"),
    ("Nilaparvata lugens",         "hemiptero_referencia"),
]

def report(taxon, page_size=200):
    out, token = [], None
    while True:
        p = {"page_size": page_size}
        if token:
            p["page_token"] = token
        r = requests.get(f"{API}/genome/taxon/{requests.utils.quote(taxon)}/dataset_report",
                         params=p, timeout=120)
        r.raise_for_status()
        d = r.json()
        out += d.get("reports", [])
        token = d.get("next_page_token")
        if not token:
            return d.get("total_count", len(out)), out
        time.sleep(0.4)

def resumen(a):
    st, inf = a.get("assembly_stats", {}), a.get("assembly_info", {})
    an = a.get("annotation_info")
    return {
        "accession": a.get("accession"),
        "organismo": a.get("organism", {}).get("organism_name"),
        "taxid": a.get("organism", {}).get("tax_id"),
        "nombre_ensamblado": inf.get("assembly_name"),
        "nivel": inf.get("assembly_level"),
        "tipo": inf.get("assembly_type"),
        "refseq_category": a.get("assembly_info", {}).get("refseq_category"),
        "fecha": inf.get("release_date"),
        "bioproject": (inf.get("bioproject_accession")),
        "enviado_por": inf.get("submitter"),
        "largo_total_ncbi": st.get("total_sequence_length"),
        "n_contigs_ncbi": st.get("number_of_contigs"),
        "n_scaffolds_ncbi": st.get("number_of_scaffolds"),
        "contig_n50_ncbi": st.get("contig_n50"),
        "scaffold_n50_ncbi": st.get("scaffold_n50"),
        "gc_percent_ncbi": st.get("gc_percent"),
        "anotado": bool(an),
        "anotacion_proveedor": (an or {}).get("provider"),
        "anotacion_nombre": (an or {}).get("name"),
        "anotacion_fecha": (an or {}).get("release_date"),
        "anotacion_genes": ((an or {}).get("stats", {}).get("gene_counts") or {}),
    }

def main(dest):
    res = {}
    for taxon, rol in TAXA:
        try:
            total, reps = report(taxon)
            res[taxon] = {"rol": rol, "total_ensamblados": total,
                          "ensamblados": [resumen(a) for a in reps]}
            print(f"{taxon:34s} rol={rol:20s} n={total}")
        except Exception as e:
            res[taxon] = {"rol": rol, "error": f"{type(e).__name__}: {e}"}
            print(f"{taxon:34s} ERROR {e}")
        time.sleep(0.4)
    with open(dest, "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "ncbi_datasets_metadatos.json")

#!/usr/bin/env python3
"""Manifiesto unico de las secuencias que alimentan el eje 3 de F3 (issue #43).

Junta en una sola tabla versionada todo lo que hoy esta repartido en cuatro salidas: que fila del
catalogo de C5, que secuencia, de donde sale, con que referencia, su sha256 y con que lectura entra
al eje 3 (`D_maidis`, `proxy_especie_del_paper`, `proxy_sustituto_declarado`). No recalcula nada:
lee las salidas ya publicadas y falla si alguna no esta.

El manifiesto NO lleva nucleotidos: identifica cada secuencia por accesion o nombre y por su sha256,
que es lo que permite comprobar que la que esta en work/ es la misma sin versionarla.

Uso: python research/ola6/F3_recomendador_genes/scripts/12_manifiesto_secuencias.py
"""
import csv, hashlib, json, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parents[1] / "resultados"
CAT = RAIZ / "research/ola3/C5_estructura_genes_ingenieria_inversa/catalogo_genes_blanco.json"


def leer(nombre):
    with (OUT / nombre).open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def sha_de(ruta):
    """sha256 de la secuencia (sin cabecera ni saltos), o '' si el archivo no esta en disco."""
    p = RAIZ / ruta
    if not p.exists():
        return ""
    s = "".join(l.strip() for l in p.read_text().splitlines() if not l.startswith(">")).upper()
    return hashlib.sha256(s.encode()).hexdigest()


def main():
    cat = {r["id"]: r for r in json.loads(CAT.read_text())["filas"]}
    filas = []

    # 1. Las cinco filas DM: secuencias de D. maidis ya en work/, tamizadas en eje3_offtarget.tsv
    DM = {"DM-01": ("BicC_Dm", "work/sifi_v2/fasta/BicC_Dm_full.fasta", "planilla de EPILAB (no publica)"),
          "DM-02": ("VATPaseB_Dm", "research/ola6/O2_vatpase_b/resultados/VATPaseB_Dm_cds.fna",
                    "CDS predicho por miniprot sobre el genoma OZ319705.1 (O2)"),
          "DM-03": ("ATPaseD_Dm", "work/sifi_v2/fasta/ATPaseD_Dm_full.fasta", "planilla de EPILAB (no publica)"),
          "DM-05": ("eth_Dm", "work/sifi_v2/fasta/eth_Dm_full.fasta", "ARNm publico PZ371507.1"),
          "DM-06": ("bursA_Dm", "work/sifi_v2/fasta/bursA_Dm_full.fasta", "ARNm publico PZ371508.1")}
    e3 = {r["id"]: r for r in leer("eje3_offtarget.tsv")}
    for i, (nom, ruta, origen) in DM.items():
        filas.append({"id": i, "especie_catalogo": cat[i]["especie"], "gen": cat[i]["gen"],
                      "secuencia": nom, "accesion": "", "origen": origen, "ruta_en_work": ruta,
                      "sha256_secuencia": sha_de(ruta), "lectura_eje3": "D_maidis",
                      "eje3_fraccion_limpia": e3[i]["fraccion_limpia"] if i in e3 else "",
                      "paper": "", "paper_doi": "", "paper_pmid": "",
                      "nota": "especie del catalogo = D. maidis: la secuencia es del propio vector"})

    # 2. Filas recuperadas de papers y verificadas en NCBI
    ver = leer("recuperacion_6filas_verificacion.tsv")
    nue = {r["id"]: r for r in leer("eje3_filas_nuevas.tsv")}
    for r in ver:
        i = r["id"]
        ruta = f"work/F3_recuperacion/{i}_{r['accesion'].split('.')[0]}.fasta"
        filas.append({"id": i, "especie_catalogo": cat[i]["especie"], "gen": cat[i]["gen"],
                      "secuencia": r["accesion"], "accesion": r["accesion"],
                      "origen": "accesion citada en el paper, verificada en NCBI", "ruta_en_work": ruta,
                      "sha256_secuencia": r["sha256_secuencia"], "lectura_eje3": "proxy_especie_del_paper",
                      "eje3_fraccion_limpia": nue[i]["fraccion_limpia"] if i in nue else "",
                      "paper": r["paper"], "paper_doi": r["paper_doi"], "paper_pmid": r["paper_pmid"],
                      "nota": f"organismo NCBI {r['organismo_ncbi']} ({r['organismo_coincide']}); "
                              f"largo {r['largo_nt_ncbi']} nt"
                              + (f", el paper declara {r['largo_nt_que_declara_el_paper']}"
                                 if r["largo_nt_que_declara_el_paper"] else "")})

    # 3. DE-03: desde el suplementario del paper, sin accesion
    refs = {r["fila"]: r for r in leer("referencias_recuperacion.tsv")}
    for r in leer("recuperacion_suplementarios.tsv"):
        i = r["fila"]; ref = refs.get(i, {})
        filas.append({"id": i, "especie_catalogo": cat[i]["especie"], "gen": cat[i]["gen"],
                      "secuencia": r["secuencia"], "accesion": "",
                      "origen": r["origen"], "ruta_en_work": "work/F3_recuperacion/DE-03_S1File.fasta",
                      "sha256_secuencia": r["sha256"], "lectura_eje3": "proxy_especie_del_paper",
                      "eje3_fraccion_limpia": nue[i]["fraccion_limpia"] if i in nue else "",
                      "paper": f"{ref.get('autores','')} ({ref.get('anio','')}) {ref.get('revista','')}",
                      "paper_doi": ref.get("doi", ""), "paper_pmid": ref.get("pmid", ""),
                      "nota": f"sin accesion; identidad por los cebadores del paper ({r['cebadores_del_paper_hallados']}), "
                              f"ORF mas largo {r['orf_mas_largo_aa']} aa"})

    # 4. Las seis filas de C5 con secuencia sustituta declarada
    for r in leer("eje3_filas_c5.tsv"):
        i = r["id"]
        filas.append({"id": i, "especie_catalogo": r["especie_catalogo"], "gen": r["gen"],
                      "secuencia": r["secuencia_usada"], "accesion": r["secuencia_usada"].split("_")[-1],
                      "origen": "secuencia sustituta declarada por C5 en `secuencia_usada`; FASTA versionado "
                                "en research/ola3/C5_.../resultados/candidatos_c5.fa",
                      "ruta_en_work": "research/ola3/C5_estructura_genes_ingenieria_inversa/resultados/candidatos_c5.fa",
                      "sha256_secuencia": r["sha256"], "lectura_eje3": r["lectura"],
                      "eje3_fraccion_limpia": r["fraccion_limpia"], "paper": "", "paper_doi": "", "paper_pmid": "",
                      "nota": "la secuencia NO es de la especie del catalogo; C5 la publicaba contra un panel de "
                              "cinco que incluia M. quadrilineatus (autoacierto, D99)"})

    # 4b. Segunda vuelta: accesiones leidas de los papers y bajadas de NCBI
    for r in leer("eje3_filas_resto.tsv"):
        i = r["id"]
        auto = r["autoacierto_especie_en_el_panel"] != "no"
        filas.append({"id": i, "especie_catalogo": r["especie_catalogo"], "gen": r["gen_catalogo"],
                      "secuencia": r["accesion"], "accesion": r["accesion"],
                      "origen": r["origen_de_la_accesion"],
                      "ruta_en_work": f"work/F3_eje3_resto/{i}_{r['accesion'].split('.')[0]}.fasta",
                      "sha256_secuencia": r["sha256"], "lectura_eje3": r["lectura"],
                      "eje3_fraccion_limpia": "" if auto else r["fraccion_limpia"],
                      "paper": "", "paper_doi": "", "paper_pmid": "",
                      "nota": ("AUTOACIERTO: la especie de la secuencia esta en el panel de seis, su fraccion "
                               f"limpia ({r['fraccion_limpia']}) NO es riesgo y no entra al puntaje" if auto
                               else f"{r['largo_nt']} nt; ver recuperacion_resto_REPORT.md")})

    # 5. Lo que no tiene secuencia: se declara, no se rellena
    con = {f["id"] for f in filas}
    for i, r in sorted(cat.items()):
        if i in con:
            continue
        filas.append({"id": i, "especie_catalogo": r["especie"], "gen": r["gen"], "secuencia": "", "accesion": "",
                      "origen": "sin secuencia: ver recuperacion_6filas_REPORT.md y recuperacion_resto_REPORT.md",
                      "ruta_en_work": "", "sha256_secuencia": "", "lectura_eje3": "", "eje3_fraccion_limpia": "",
                      "paper": "", "paper_doi": "", "paper_pmid": "",
                      "nota": "eje 3 ausente, declarado; el equipo decidio no rellenar con secuencias sustitutas nuevas"})

    campos = ["id", "especie_catalogo", "gen", "secuencia", "accesion", "origen", "ruta_en_work",
              "sha256_secuencia", "lectura_eje3", "eje3_fraccion_limpia", "paper", "paper_doi", "paper_pmid", "nota"]
    with (OUT / "manifiesto_secuencias_eje3.tsv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=campos, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(filas)
    conseq = [f for f in filas if f["secuencia"]]
    print(f"manifiesto: {len(filas)} entradas, {len(conseq)} con secuencia, "
          f"{len({f['id'] for f in conseq})} filas del catalogo cubiertas de {len(cat)}")
    for f in conseq:
        if not f["sha256_secuencia"]:
            print("  OJO sin sha256 (archivo no esta en disco):", f["id"], f["secuencia"])
    return 0


if __name__ == "__main__":
    sys.exit(main())

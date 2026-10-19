"""Catalogo razonado de organismos no objetivo, y chequeo de que existe en NCBI.

Para cada especie pregunta a la API de NCBI Datasets si hay un ensamblado RefSeq
(GCF_) con anotacion. Si lo hay, arma la URL del transcriptoma (`_rna.fna.gz`),
que es lo correcto para off-target de RNAi: un orden de magnitud mas chico que el
genoma y es lo que el insecto efectivamente transcribe.

Cuando una especie NO tiene genoma anotado, eso tambien es resultado: significa
que el riesgo sobre ese organismo NO SE PUEDE evaluar hoy, y hay que decirlo.

Uso:
    python3 no_objetivo_catalogo.py [--csv salida.csv]
"""

from __future__ import annotations

import csv
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/taxon/{}/dataset_report"

# ---------------------------------------------------------------------------
# El catalogo. Cada entrada: (clave, especie, grupo, por que tiene que estar).
#
# Las justificaciones etiquetadas [paper] salen de:
#  - Luft Albarracin et al. 2017, Neotrop Entomol (PMID 28643143): complejo de
#    parasitoides de huevos de D. maidis EN ARGENTINA, 16 especies, dominan
#    Anagrus (incarnatus, despues redescripto como A. virlai) y Pseudoligosita
#    longifrangiata, que juntos son el 83,6 % de los individuos colectados.
#  - Moya-Raygoza 2026, J Insect Sci (PMID 42024807, PMC13105290): revision de
#    control biologico. 40 especies de artropodos depredadores documentadas en
#    America (Araneae, Dermaptera, Hemiptera, Coleoptera, Neuroptera, Diptera,
#    Hymenoptera; Casuso et al. 2025). Ninfas y adultos parasitados por 6 sp. de
#    Dryinidae, 3 de Pipunculidae (Diptera) y 1 de Halictophagidae (Strepsiptera).
#    Gonatopus bartletti es depredador Y parasitoide. Hongos entomopatogenos:
#    Beauveria, Metarhizium, Cordyceps.
# ---------------------------------------------------------------------------
CATALOGO = [
    # --- el cultivo que se quiere proteger -------------------------------
    ("maiz", "Zea mays", "cultivo",
     "El cultivo. Si el dsRNA silencia un gen del maiz, el remedio es el dano. Ya estaba."),

    # --- polinizadores ---------------------------------------------------
    ("abeja", "Apis mellifera", "polinizador",
     "Especie centinela universal de toxicidad a polinizadores y la que pide cualquier "
     "regulador. Ya estaba."),
    ("abejorro", "Bombus terrestris", "polinizador",
     "Polinizador manejado y silvestre. Apidae pero otro genero: cubre el hueco de suponer "
     "que Apis representa a todas las abejas."),
    ("abeja_solitaria", "Megachile rotundata", "polinizador",
     "Abeja solitaria, otra familia (Megachilidae). La mayoria de las abejas del mundo son "
     "solitarias y no estan representadas por Apis."),
    ("mariposa", "Danaus plexippus", "polinizador",
     "Lepidoptero polinizador, de otro orden. Caso emblematico de dano no intencional por "
     "tecnologia agricola (Bt y la monarca), asi que su ausencia se nota."),

    # --- enemigos naturales de la chicharrita ----------------------------
    ("parasitoide_mymaridae", "Anagrus", "enemigo natural",
     "[paper] Anagrus virlai (antes identificado como A. incarnatus) es el parasitoide de "
     "huevos MAS ABUNDANTE de D. maidis en Argentina. Matar al parasitoide junto con la "
     "plaga es el peor resultado posible del producto."),
    ("parasitoide_trichogramma", "Trichogramma", "enemigo natural",
     "[paper] Trichogrammatidae es la familia mas representada en el complejo argentino "
     "(8 de 16 especies). Los Trichogramma son ademas los parasitoides mas liberados del "
     "mundo en control biologico."),
    ("parasitoide_dryinidae", "Gonatopus", "enemigo natural",
     "[paper] Gonatopus bartletti es depredador Y parasitoide de ninfas y adultos de "
     "D. maidis. Ninfas y adultos son atacados por 6 especies de Dryinidae."),
    ("vaquita", "Harmonia axyridis", "enemigo natural",
     "[paper] Coleoptera figura entre los 7 ordenes de depredadores documentados. Las "
     "vaquitas (Coccinellidae) son el depredador generalista tipico del maiz."),
    ("vaquita_nativa", "Coccinella septempunctata", "enemigo natural",
     "Segunda vaquita, para no depender de una sola especie de la familia."),
    ("crisopa", "Chrysoperla carnea", "enemigo natural",
     "[paper] Neuroptera figura entre los ordenes de depredadores. Chrysoperla es el "
     "depredador de Neuroptera que se cria y libera comercialmente."),
    ("chinche_depredadora", "Orius", "enemigo natural",
     "[paper] Hemiptera figura entre los ordenes de depredadores. Orius es depredador de "
     "hemipteros pequenos y ademas es un hemiptero: el riesgo de parentesco con el blanco "
     "es alto."),
    ("tijereta", "Forficula auricularia", "enemigo natural",
     "[paper] Dermaptera figura entre los ordenes de depredadores documentados."),
    ("arana", "Parasteatoda tepidariorum", "enemigo natural",
     "[paper] Araneae es el primero de los ordenes de depredadores listados. Es ademas un "
     "quelicerado: chequea un linaje de artropodo muy alejado."),

    # --- hemipteros no objetivo (el riesgo mas alto por parentesco) ------
    ("cicadelido_cercano", "Macrosteles quadrilineatus", "hemiptero no objetivo",
     "EL CONTROL POSITIVO BUENO. Cicadellidae, subfamilia Deltocephalinae, la misma que "
     "Dalbulus: es el pariente mas cercano a la chicharrita con genoma anotado en todo NCBI. "
     "Ademas es vector de fitoplasmas, o sea que comparte biologia con el blanco. Si el filtro "
     "no marca nada aca sobre un gen esencial, el filtro no esta midiendo parentesco."),
    ("cicadelido_pariente", "Homalodisca vitripennis", "hemiptero no objetivo",
     "El cicadelido mas cercano a D. maidis con genoma anotado. Es el control positivo del "
     "ensayo: si el filtro no marca nada aca, el filtro no esta midiendo parentesco."),
    ("delfacido", "Nilaparvata lugens", "hemiptero no objetivo",
     "Hemiptera, otro familia. Tambien es plaga, pero sirve de segundo control positivo de "
     "cercania filogenetica."),
    ("pulgon", "Acyrthosiphon pisum", "hemiptero no objetivo",
     "Hemiptera de otro suborden (Sternorrhyncha). Marca hasta donde llega el parentesco."),

    ("sirfido", "Episyrphus balteatus", "polinizador",
     "Doble funcion: el adulto es polinizador y la larva es depredadora de pulgones. [paper] "
     "Diptera figura entre los ordenes de depredadores documentados sobre D. maidis. Cubre dos "
     "casilleros con una especie."),
    ("parasitoide_braconido", "Aphidius gifuensis", "enemigo natural",
     "Suplente del parasitoide que no tenemos. Ningun parasitoide de D. maidis esta anotado; "
     "Braconidae es la familia de parasitoides con mas genomas anotados (9) y este es un "
     "parasitoide de plagas agricolas. No es el animal correcto, es lo mas cercano que existe, "
     "y hay que decirlo asi."),
    ("escarabajo_suelo", "Dalotia coriaria", "enemigo natural",
     "[paper] Coleoptera figura entre los ordenes de depredadores. Staphylinidae vive en el "
     "suelo y en la hojarasca, que es donde va a parar el dsRNA aplicado."),

    # --- organismos del suelo y ecotoxicologia estandar ------------------
    ("colembolo", "Folsomia candida", "suelo",
     "Especie de ensayo estandar OECD 232 para toxicidad en suelo. Si el regulador pide un "
     "organismo del suelo, pide este."),
    ("lombriz", "Eisenia fetida", "suelo",
     "Especie de ensayo estandar OECD 207/222 para lombrices. El dsRNA aplicado a campo "
     "termina en el suelo."),
    ("nematodo", "Caenorhabditis elegans", "suelo",
     "Nematodo del suelo y el organismo donde se descubrio el RNAi: tiene amplificacion de "
     "la senal y absorcion sistemica, o sea que es de los mas sensibles que existen."),
    ("acaro_suelo", "Tetranychus urticae", "suelo",
     "Quelicerado con genoma anotado y RNAi sensible. Cubre otro linaje de artropodo."),

    # --- acuatico ---------------------------------------------------------
    ("daphnia", "Daphnia magna", "acuatico",
     "Crustaceo, especie de ensayo estandar OECD 202/211. El escurrimiento del lote llega "
     "al agua."),
    ("pez", "Danio rerio", "acuatico",
     "Vertebrado acuatico de ensayo estandar. Cubre vertebrado no mamifero."),

    # --- humano y ganado ---------------------------------------------------
    ("humano", "Homo sapiens", "humano/ganado",
     "Quien aplica el producto y quien come el maiz. Que el riesgo sea bajo no exime de "
     "medirlo: es lo primero que va a preguntar un regulador."),
    ("vaca", "Bos taurus", "humano/ganado",
     "El maiz argentino va mayoritariamente a alimentacion animal. Es la via de exposicion "
     "mas grande en volumen."),
    ("gallina", "Gallus gallus", "humano/ganado",
     "Segunda via de exposicion por alimentacion animal."),
]


def consultar(nombre: str) -> list[dict]:
    url = API.format(urllib.parse.quote(nombre))
    url += "?filters.assembly_source=refseq&page_size=20"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            datos = json.load(r)
    except Exception as e:  # la API se cae o rate-limitea; no es motivo para abortar todo
        return [{"_error": str(e)}]
    return datos.get("reports", []) or []


def elegir(reports: list[dict]) -> dict | None:
    """Mejor ensamblado RefSeq anotado: prioriza 'reference genome' y nivel cromosoma."""
    niveles = {"Complete Genome": 4, "Chromosome": 3, "Scaffold": 2, "Contig": 1}
    candidatos = []
    for r in reports:
        if "_error" in r:
            continue
        acc = r.get("accession", "")
        if not acc.startswith("GCF_"):
            continue
        anot = r.get("annotation_info") or {}
        if not anot:
            continue
        info = r.get("assembly_info") or {}
        candidatos.append((
            1 if info.get("refseq_category") == "reference genome" else 0,
            niveles.get(info.get("assembly_level", ""), 0),
            r,
        ))
    if not candidatos:
        return None
    candidatos.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return candidatos[0][2]


def url_rna(report: dict) -> str:
    acc = report["accession"]
    nombre = (report.get("assembly_info") or {}).get("assembly_name", "")
    base = acc[:3] + "/" + acc[4:7] + "/" + acc[7:10] + "/" + acc[10:13]
    carpeta = f"{acc}_{nombre}".replace(" ", "_")
    return (f"https://ftp.ncbi.nlm.nih.gov/genomes/all/{base}/{carpeta}/"
            f"{carpeta}_rna.fna.gz")


def main() -> int:
    filas = []
    for clave, especie, grupo, razon in CATALOGO:
        reports = consultar(especie)
        mejor = elegir(reports)
        if mejor is None:
            n_gca = sum(1 for r in reports if r.get("accession", "").startswith("GCA_"))
            filas.append({
                "clave": clave, "especie": especie, "grupo": grupo,
                "refseq": "", "nombre_ensamblado": "", "nivel": "",
                "organismo_encontrado": "", "url_rna": "",
                "estado": "SIN REFSEQ ANOTADO",
                "razon": razon,
            })
            print(f"[  ] {especie:<32}{grupo:<22}sin RefSeq anotado "
                  f"({len(reports)} ensamblados, {n_gca} solo GenBank)")
        else:
            info = mejor.get("assembly_info") or {}
            org = (mejor.get("organism") or {}).get("organism_name", "")
            filas.append({
                "clave": clave, "especie": especie, "grupo": grupo,
                "refseq": mejor["accession"],
                "nombre_ensamblado": info.get("assembly_name", ""),
                "nivel": info.get("assembly_level", ""),
                "organismo_encontrado": org,
                "url_rna": url_rna(mejor),
                "estado": "ok",
                "razon": razon,
            })
            print(f"[ok] {especie:<32}{grupo:<22}{mejor['accession']:<18}"
                  f"{info.get('assembly_level',''):<16}{org}")
        time.sleep(0.4)

    hay = sum(1 for f in filas if f["estado"] == "ok")
    print(f"\ncon RefSeq anotado: {hay} de {len(filas)}")
    print("sin RefSeq:")
    for f in filas:
        if f["estado"] != "ok":
            print(f"  - {f['especie']} ({f['grupo']})")

    if "--csv" in sys.argv:
        destino = Path(sys.argv[sys.argv.index("--csv") + 1])
        destino.parent.mkdir(parents=True, exist_ok=True)
        with destino.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
            w.writeheader()
            w.writerows(filas)
        print(f"csv escrito en {destino}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Paso 2 de F3 — el eje de esencialidad, por vía, con la fuente abierta al lado.

La escala, los cuatro niveles y las cinco reglas están en
`resultados/escala_esencialidad.md`, commiteado ANTES de abrir la primera fuente
(commit 35d1b9f). Este script es su aplicación.

Lo que hace distinto a este archivo
-----------------------------------
Cada vía trae su cita completa, la especie donde se demostró, el número que sostiene el
nivel, y un campo `primaria_abierta` que dice si la fuente que se cita es la que se leyó o
si es una fuente secundaria que cita a una primaria que NO se pudo abrir. Esa distinción
existe porque `CLAUDE.md` prohíbe citar una fuente que no se abrió, y la forma honesta de
usar un dato que viene de una revisión o de una base de datos es decir que viene de ahí.

La regla 3 de la escala —que una vía no puede puntuarse con evidencia del propio catálogo de
C5, porque eso convertiría al eje 2 en el eje 1 con otro nombre y 0,25 más de peso— se
verifica abajo: toda vía puntuada declara `independiente_del_catalogo=True` y el script falla
si alguna no lo hace.

Uso:
    python research/ola6/F3_recomendador_genes/scripts/02_eje_esencialidad.py
"""

import csv
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
CATALOGO = RAIZ / "research/ola3/C5_estructura_genes_ingenieria_inversa/catalogo_genes_blanco.json"
EJE_FENOTIPO = Path(__file__).resolve().parents[1] / "resultados/eje_fenotipo.tsv"
SALIDA = Path(__file__).resolve().parents[1] / "resultados/eje_esencialidad.tsv"

PUNTAJE = {"E3": 1.00, "E2": 0.66, "E1": 0.33, "E0": None}

# Cada vía: los candidatos que la heredan, el nivel, la cita de lo que se abrió, la especie,
# el número que sostiene el nivel, si la primaria quedó sin abrir, y la nota.
VIAS = [
    {
        "via": "V-ATPasa (bomba de protones vacuolar)",
        "candidatos": ["DM-02", "DM-03", "DE-01", "HE-02"],
        "nivel": "E3",
        "fuente": "Wang X, Zhao D, Wang Q, Liu Y, Lu X, Guo W (2024). Identification and "
                  "Functional Analysis of V-ATPaseA and C Genes in Hyphantria cunea. Insects "
                  "15(7):515. doi:10.3390/insects15070515",
        "especie_demostrada": "Hyphantria cunea (Lepidoptera)",
        "numero": "mortalidad 61,7 % (dsV-ATPase A) y 46,7 % (dsC) a 120 h, por microinyeccion "
                  "de 10 ug de ARNdc en larva de tercer estadio; knockdown 62,7 % y 71,0 %",
        "primaria_abierta": True,
        "independiente_del_catalogo": True,
        "apoyo_secundario": "Buer et al. 2024 (doi:10.1002/ps.8505) ubica subunidades de "
                            "V-ATPasa en sus conjuntos de 905, 145 y 91 blancos efectivos en "
                            "Tribolium castaneum",
        "nota": "la via mejor sostenida del catalogo: letalidad medida en un insecto y "
                "presencia en el tamizaje genomico, por dos fuentes abiertas distintas",
    },
    {
        "via": "Proteasoma 26S (tapa, Rpn6)",
        "candidatos": ["CI-01", "CI-02"],
        "nivel": "E3",
        "fuente": "Ulrich J, Dao VA, Majumdar U, et al. (2015). Large scale RNAi screen in "
                  "Tribolium reveals novel target genes for pest control and the proteasome as "
                  "prime target. BMC Genomics 16:674. doi:10.1186/s12864-015-1880-y",
        "especie_demostrada": "Tribolium castaneum (Coleoptera)",
        "numero": "de ~5.000 genes del tamizaje iBeetle, 100 dieron >=90 % de mortalidad; los 11 "
                  "mejores llegaron a 100 % al dia 8 y a >=80 % al dia 6. Los terminos GO del "
                  "proteasoma fueron el grupo mas predictivo de letalidad",
        "primaria_abierta": True,
        "independiente_del_catalogo": True,
        "apoyo_secundario": "Buer et al. 2024 (doi:10.1002/ps.8505): 22 de 35 genes de la via "
                            "KEGG del proteasoma quedaron entre los blancos, 62,9 %",
        "nota": "la conclusion del titulo —el proteasoma como blanco de primera linea— sale de "
                "agrupamiento por GO de los genes mas eficientes, no de un experimento dedicado "
                "a genes del proteasoma; los autores aclaran que faltan ensayos de ingesta",
    },
    {
        "via": "Fosforilacion oxidativa (ATP sintasa beta)",
        "candidatos": ["CI-03", "CI-04", "CI-06"],
        "nivel": "E3",
        "fuente": "Buer B, Donitz J, Milner M, et al. (2024). Superior target genes and pathways "
                  "for RNAi-mediated pest control revealed by genome-wide analysis in the beetle "
                  "Tribolium castaneum. Pest Manag Sci 81(2):1026-1036. doi:10.1002/ps.8505",
        "especie_demostrada": "Tribolium castaneum (Coleoptera)",
        "numero": "la via KEGG de fosforilacion oxidativa aparece enriquecida entre los blancos "
                  "efectivos con 30 de 58 genes, P = 2,50e-10. Tamizaje de 10.193 genes nuevos "
                  "sobre ~15.530 totales, letalidad leida al dia 7 en larva y al dia 16 en "
                  "adulto, 1 ug/uL por inyeccion; la mayoria mato entre los dias 6 y 8 a "
                  "300 ng/uL",
        "primaria_abierta": True,
        "independiente_del_catalogo": True,
        "apoyo_secundario": "",
        "nota": "el nivel es de la VIA. La subunidad beta de la ATP sintasa, que es la que el "
                "catalogo usa, NO esta nombrada individualmente en el trabajo: lo que esta "
                "medido es el enriquecimiento de la via entre los blancos letales",
    },
    {
        "via": "Endocitosis mediada por clatrina",
        "candidatos": ["CI-07"],
        "nivel": "E3",
        "fuente": "Buer B, Donitz J, Milner M, et al. (2024). Pest Manag Sci 81(2):1026-1036. "
                  "doi:10.1002/ps.8505",
        "especie_demostrada": "Tribolium castaneum (Coleoptera)",
        "numero": "la cadena pesada de clatrina (TC015014) esta en la tabla 3 de blancos mas "
                  "efectivos, junto con dinamina (TC011058). De 66 genes del grupo 1 probados "
                  "por ingesta en Phaedon cochleariae, 34 subieron la letalidad mas de 50 %",
        "primaria_abierta": True,
        "independiente_del_catalogo": True,
        "apoyo_secundario": "",
        "nota": "el candidato CI-07 entro al catalogo por un fenotipo de transmision, no de "
                "letalidad; este eje dice algo distinto y por eso no es redundante: la via "
                "ademas es letal cuando se la silencia en otro insecto",
    },
    {
        "via": "Transporte dependiente de ATP (transportadores ABC)",
        "candidatos": ["DE-04"],
        "nivel": "E3",
        "fuente": "Buer B, Donitz J, Milner M, et al. (2024). Pest Manag Sci 81(2):1026-1036. "
                  "doi:10.1002/ps.8505",
        "especie_demostrada": "Tribolium castaneum (Coleoptera)",
        "numero": "el miembro 1 de la subfamilia ABCE (TC010519) esta entre los blancos "
                  "efectivos de la tabla 3",
        "primaria_abierta": True,
        "independiente_del_catalogo": True,
        "apoyo_secundario": "",
        "nota": "la coincidencia es parcial y conviene decirla: el que aparece es ABCE, que no "
                "es un transportador de membrana, y la fila DE-04 agrupa tres genes ABC de los "
                "cuales ABCE y ABCF son los que el catalogo reporta como letales",
    },
    {
        "via": "Ecdisis (hormona disparadora, ETH)",
        "candidatos": ["DM-05"],
        "nivel": "E3",
        "fuente": "InteractiveFly / Society for Developmental Biology, ficha del gen Ecdysis "
                  "triggering hormone, sdbonline.org/sites/fly/dbzhnsky/ecdhor1.htm (leida el "
                  "2026-10-27), que cita a Park et al. 2002, Development",
        "especie_demostrada": "Drosophila melanogaster",
        "numero": "los nulos de eth tienen el fenotipo 'buttoned-up', con 98 % de mortalidad en "
                  "la transicion del primer al segundo estadio larval",
        "primaria_abierta": False,
        "independiente_del_catalogo": True,
        "apoyo_secundario": "",
        "nota": "FUENTE PRIMARIA NO ABIERTA: Park et al. 2002 (Development) devolvio HTTP 403. "
                "El 98 % se cita de la ficha secundaria que se leyo, no del trabajo original, y "
                "queda como pendiente en PREGUNTAS_ABIERTAS. El dato es independiente del "
                "catalogo: la fila DM-05 mide eth en D. maidis y esto es el nulo en Drosophila",
    },
    {
        "via": "Citoesqueleto muscular (actina)",
        "candidatos": ["CI-05"],
        "nivel": "E2",
        "fuente": "Ulrich J, Dao VA, Majumdar U, et al. (2015). BMC Genomics 16:674. "
                  "doi:10.1186/s12864-015-1880-y",
        "especie_demostrada": "Tribolium castaneum (Coleoptera)",
        "numero": "el grupo 7, organizacion del citoesqueleto, fue el tercero mas predictivo de "
                  "letalidad: 37 de 66 genes nuevos resultaron letales",
        "primaria_abierta": True,
        "independiente_del_catalogo": True,
        "apoyo_secundario": "",
        "nota": "CONTRADICCION DECLARADA, y por eso E2 y no E3: Buer et al. 2024, el tamizaje "
                "genomico de la misma especie, dice explicitamente que la beta-actina NO quedo "
                "en ninguno de sus conjuntos de blancos efectivos. O sea que la via es letal "
                "como grupo y el gen puntual del candidato quedo afuera del conjunto efectivo "
                "en el trabajo mas grande. [?]",
    },
    {
        "via": "Esclerotizacion tras la muda (bursicon alfa)",
        "candidatos": ["DM-06"],
        "nivel": "E2",
        "fuente": "Loveall BJ, Deitcher DL (2010). The essential role of bursicon during "
                  "Drosophila development. BMC Dev Biol 10:92. doi:10.1186/1471-213X-10-92",
        "especie_demostrada": "Drosophila melanogaster; el dato de ARNi citado es de Tribolium "
                              "castaneum",
        "numero": "del texto leido: inyectar ARNi de burs/pburs o de rk en pupa faringea dio "
                  "contracciones de pre-ecdisis de fuerza disminuida. No se extrajo una cifra "
                  "de mortalidad",
        "primaria_abierta": True,
        "independiente_del_catalogo": True,
        "apoyo_secundario": "",
        "nota": "E2 y no E3 por una razon de método y no de biologia: la fuente abierta "
                "establece un papel esencial en el desarrollo —lo dice su titulo— pero de lo "
                "que se leyo no se extrajo una medicion de letalidad por perdida de funcion. "
                "Un titulo que dice 'essential' no es una cifra",
    },
    {
        "via": "Oogenesis (Bicaudal-C)",
        "candidatos": ["DM-01", "HE-01", "HE-05"],
        "nivel": "E1",
        "fuente": "Pascual A, Vilardo ES, Taibo C, Sabio y Garcia J, Rivera Pomar R (2020). "
                  "Bicaudal C is required for the function of the follicular epithelium during "
                  "oogenesis in Rhodnius prolixus. bioRxiv. doi:10.1101/2020.02.14.949222",
        "especie_demostrada": "Rhodnius prolixus (Hemiptera)",
        "numero": "el ARNi de Rp-BicC da hembras esteriles que ponen huevos pocos, chicos y no "
                  "viables; ovarios reducidos y epitelio folicular desorganizado. La fuente NO "
                  "reporta mortalidad ni supervivencia de las hembras silenciadas",
        "primaria_abierta": True,
        "independiente_del_catalogo": True,
        "apoyo_secundario": "",
        "nota": "E1 porque es exactamente una funcion condicional: esteriliza y no mata. Es el "
                "nivel que le corresponde y a la vez la evidencia mas pertinente de todas, "
                "porque es un hemiptero. Version publicada en Dev Genes Evol 2021 "
                "(doi:10.1007/s00427-021-00673-0) NO abierta; se cita el preprint, que es el "
                "que se leyo",
    },
    # --- E0: sin fuente abierta. Se declaran, no se puntuan. ---
    {
        "via": "Esclerotizacion y pigmentacion (lacasa-2)",
        "candidatos": ["CI-11", "CI-12"],
        "nivel": "E0",
        "fuente": "",
        "especie_demostrada": "",
        "numero": "",
        "primaria_abierta": False,
        "independiente_del_catalogo": True,
        "apoyo_secundario": "",
        "nota": "la busqueda apunta a Arakane et al. 2005 (lacasa 2 como la fenoloxidasa del "
                "curtido de la cuticula) y a un trabajo en Bemisia tabaci, que seria el mas "
                "pertinente por ser hemiptero; la pagina del segundo devolvio HTTP 403 y la "
                "revision de Frontiers vino como PDF binario ilegible. Pendiente",
    },
    {
        "via": "Contraccion muscular (troponina C)",
        "candidatos": ["CI-10"],
        "nivel": "E0",
        "fuente": "", "especie_demostrada": "", "numero": "",
        "primaria_abierta": False, "independiente_del_catalogo": True, "apoyo_secundario": "",
        "nota": "no se encontro fuente de esencialidad; Buer et al. 2024 no menciona troponina. "
                "Pendiente",
    },
    {
        "via": "Remodelado de cromatina (RuvBL1 / pontin)",
        "candidatos": ["DE-02"],
        "nivel": "E0",
        "fuente": "", "especie_demostrada": "", "numero": "",
        "primaria_abierta": False, "independiente_del_catalogo": True, "apoyo_secundario": "",
        "nota": "la ficha de FlyBase de pontin se descargo vacia. Hay indicios de letalidad "
                "embrionaria en raton y de nulo no viable en levadura, que alcanzarian para E2, "
                "pero ninguna de las dos fuentes se abrio. Pendiente",
    },
    {
        "via": "Determinacion sexual (transformer-2)",
        "candidatos": ["DE-03"],
        "nivel": "E0",
        "fuente": "", "especie_demostrada": "", "numero": "",
        "primaria_abierta": False, "independiente_del_catalogo": True, "apoyo_secundario": "",
        "nota": "no se busco fuente propia en esta pasada. Pendiente",
    },
    {
        "via": "Exporte nucleo-citoplasma (exportina 1 / XPO1)",
        "candidatos": ["DE-05"],
        "nivel": "E0",
        "fuente": "", "especie_demostrada": "", "numero": "",
        "primaria_abierta": False, "independiente_del_catalogo": True, "apoyo_secundario": "",
        "nota": "la ficha de VirtualFlyBrain del ortologo emb no reporta fenotipo letal, y "
                "Collier et al. 2000 (Genetics), que segun la busqueda describe alelos letales "
                "recesivos que mueren sin pasar al tercer estadio, no se abrio. Pendiente",
    },
    {
        "via": "Proteinas del intestino (natterina, legumaina)",
        "candidatos": ["CI-09"],
        "nivel": "E0",
        "fuente": "", "especie_demostrada": "", "numero": "",
        "primaria_abierta": False, "independiente_del_catalogo": True, "apoyo_secundario": "",
        "nota": "no se busco fuente propia en esta pasada. La propia fila mide que ninguno de "
                "los tres genes afecto la supervivencia, pero eso es del catalogo y la regla 3 "
                "lo excluye de este eje. Pendiente",
    },
    {
        "via": "Proteina salival de la ingestion de floema (NcSP75)",
        "candidatos": ["HE-07"],
        "nivel": "E0",
        "fuente": "", "especie_demostrada": "", "numero": "",
        "primaria_abierta": False, "independiente_del_catalogo": True, "apoyo_secundario": "",
        "nota": "no se busco fuente propia en esta pasada. Pendiente",
    },
]


def main() -> int:
    cat = {f["id"]: f for f in json.loads(CATALOGO.read_text(encoding="utf-8"))["filas"]}
    with EJE_FENOTIPO.open(encoding="utf-8") as fh:
        fenotipo = {r["id"]: r for r in csv.DictReader(fh, delimiter="\t")}

    con_mecanismo = {i for i, r in fenotipo.items() if r["mecanismos"]}

    errores = []
    asignados = []
    for v in VIAS:
        if v["nivel"] not in PUNTAJE:
            errores.append(f"{v['via']}: nivel desconocido {v['nivel']!r}")
        if v["nivel"] != "E0":
            # Regla 1: un nivel con puntaje exige cita, especie y numero.
            for campo in ("fuente", "especie_demostrada", "numero"):
                if not v[campo]:
                    errores.append(f"{v['via']}: nivel {v['nivel']} sin {campo}")
            # Regla 3: la evidencia no puede venir del catalogo.
            if not v["independiente_del_catalogo"]:
                errores.append(f"{v['via']}: puntuada con evidencia del catalogo (regla 3)")
        for c in v["candidatos"]:
            if c not in cat:
                errores.append(f"{v['via']}: candidato inexistente {c}")
            asignados.append(c)

    repetidos = sorted({c for c in asignados if asignados.count(c) > 1})
    if repetidos:
        errores.append(f"candidatos en mas de una via: {repetidos}")
    sin_via = sorted(con_mecanismo - set(asignados))
    if sin_via:
        errores.append(f"candidatos con mecanismo y sin via: {sin_via}")
    de_mas = sorted(set(asignados) - con_mecanismo)
    if de_mas:
        errores.append(f"vias que incluyen candidatos sin mecanismo de fenotipo: {de_mas}")

    if errores:
        print("ERROR: el eje de esencialidad no se verifica.", file=sys.stderr)
        for e in errores:
            print(f"  {e}", file=sys.stderr)
        return 1

    registros = []
    for v in VIAS:
        for c in sorted(v["candidatos"]):
            p = PUNTAJE[v["nivel"]]
            registros.append({
                "id": c,
                "gen": cat[c]["gen"],
                "via": v["via"],
                "nivel": v["nivel"],
                "puntaje": "" if p is None else f"{p:.2f}",
                "entra_al_orden_por_esencialidad": "no" if p is None else "si",
                "especie_donde_se_demostro": v["especie_demostrada"],
                "numero_que_sostiene_el_nivel": v["numero"],
                "fuente": v["fuente"],
                "fuente_primaria_abierta": "si" if v["primaria_abierta"] else "no",
                "apoyo_secundario": v["apoyo_secundario"],
                "nota": v["nota"],
            })
    registros.sort(key=lambda r: r["id"])

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    with SALIDA.open("w", encoding="utf-8", newline="") as fh:
        esc = csv.DictWriter(fh, fieldnames=list(registros[0]), delimiter="\t",
                             lineterminator="\n")
        esc.writeheader()
        esc.writerows(registros)

    print(f"eje de esencialidad: {len(VIAS)} vias, {len(registros)} candidatos")
    for nivel in ("E3", "E2", "E1", "E0"):
        vs = [v for v in VIAS if v["nivel"] == nivel]
        n = sum(len(v["candidatos"]) for v in vs)
        print(f"  {nivel}: {len(vs):2d} vias, {n:2d} candidatos")
    con = sum(1 for r in registros if r["puntaje"])
    print(f"  con puntaje: {con} de {len(registros)}; declarados sin fuente abierta: "
          f"{len(registros) - con}")
    sin_prim = {v["via"] for v in VIAS if v["nivel"] != "E0" and not v["primaria_abierta"]}
    if sin_prim:
        print(f"  puntuadas desde una fuente secundaria, con la primaria sin abrir: {sin_prim}")
    print(f"escrito: {SALIDA.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

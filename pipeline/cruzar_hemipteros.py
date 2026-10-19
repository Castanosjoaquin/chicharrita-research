"""Cruza los blancos de RNAi de hemipteros con nuestra tabla de candidatos.

La debilidad mas grande del proyecto es que el 100 % de los fenotipos de
`tabla_unificada.csv` viene de *Tribolium castaneum*, que es Coleoptera. La
chicharrita es Hemiptera. Si el fenotipo de RNAi no transfiere entre ordenes, el
ranking entero se apoya en nada.

Este script mide cuanto baja ese 100 %: mapea al genoma los blancos con RNAi ya
publicado EN HEMIPTEROS y ve cuales caen sobre loci que ya teniamos.

Un locus con respaldo en las dos fuentes &mdash;Tribolium y un hemiptero&mdash;
es el candidato mas defendible que podemos presentar, porque el supuesto de
transferencia entre ordenes deja de ser necesario para ese locus.

Uso:
    python3 cruzar_hemipteros.py <hemip.gff> <mapa.csv> <tabla_unificada.csv> [--csv salida.csv]
"""

from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from resumir_miniprot import parsear  # noqa: E402

# Fraccion del intervalo mas corto que tienen que compartir dos loci para que los
# tratemos como el mismo gen. Mismo criterio que `tabla_unificada.py`.
SOLAPE_MINIMO = 0.5


def solapan(a_ini: int, a_fin: int, b_ini: int, b_fin: int) -> bool:
    solape = min(a_fin, b_fin) - max(a_ini, b_ini) + 1
    if solape <= 0:
        return False
    corto = min(a_fin - a_ini + 1, b_fin - b_ini + 1)
    return corto > 0 and solape / corto >= SOLAPE_MINIMO


def main() -> int:
    gff = Path(sys.argv[1])
    mapa_ruta = Path(sys.argv[2])
    unificada = Path(sys.argv[3])

    curado = {f["id"]: f for f in csv.DictReader(mapa_ruta.open(encoding="utf-8"))}

    # Mejor hit por proteina consultada
    hits = parsear(gff)
    mejor: dict[str, dict] = {}
    cuantos: Counter[str] = Counter()
    for h in hits:
        cuantos[h["proteina"]] += 1
        prev = mejor.get(h["proteina"])
        if prev is None or h["score"] > prev["score"]:
            mejor[h["proteina"]] = h
    print(f"proteinas de hemipteros consultadas : {len(curado)}")
    print(f"con al menos un locus en D. maidis  : {len(mejor)}")
    print(f"alineamientos totales               : {len(hits)}")

    # Loci de la tabla unificada, indexados por cromosoma
    loci_por_crom: dict[str, list[dict]] = defaultdict(list)
    total_loci = 0
    with unificada.open(encoding="utf-8") as fh:
        for fila in csv.DictReader(fh):
            fila["inicio"] = int(fila["inicio"])
            fila["fin"] = int(fila["fin"])
            loci_por_crom[fila["cromosoma"]].append(fila)
            total_loci += 1
    print(f"loci en la tabla unificada          : {total_loci}")

    filas = []
    for ident, h in sorted(mejor.items()):
        info = curado.get(ident, {})
        candidatos = [l for l in loci_por_crom.get(h["cromosoma"], [])
                      if solapan(h["inicio"], h["fin"], l["inicio"], l["fin"])]
        # Si solapa con varios, se queda el de mayor solape.
        elegido = None
        if candidatos:
            elegido = max(candidatos, key=lambda l: min(h["fin"], l["fin"]) - max(h["inicio"], l["inicio"]))
        filas.append({
            "id_hemiptero": ident,
            "especie_hemiptero": info.get("especie", ""),
            "familia_hemiptero": info.get("familia_insecto", ""),
            "gen_hemiptero": info.get("gen", ""),
            "familia_gen": info.get("familia_gen", ""),
            "fenotipo_hemiptero": info.get("fenotipo", ""),
            "categoria_hemiptero": info.get("categoria", ""),
            "magnitud": info.get("magnitud", ""),
            "pmid": info.get("pmid", ""),
            "uniprot": info.get("uniprot", ""),
            "fuente_secuencia": info.get("fuente_secuencia", ""),
            "cromosoma": h["cromosoma"],
            "inicio": h["inicio"],
            "fin": h["fin"],
            "hebra": h["hebra"],
            "identidad_hemiptero": h["identidad"],
            "exones": h["exones"],
            "frameshift": h["frameshift"],
            "stop_interno": h["stop_interno"],
            "n_hits": cuantos[ident],
            # --- lo que ya teniamos en ese locus
            "locus": elegido["locus"] if elegido else "",
            "nivel_evidencia_previo": elegido["nivel_evidencia"] if elegido else "",
            "categoria_tribolium": elegido["fenotipo_categoria"] if elegido else "",
            "mejor_hit_tribolium": elegido["mejor_hit_tribolium"] if elegido else "",
            "gen_drosophila": elegido["gen_drosophila"] if elegido else "",
            "letalidad_tribolium": elegido["letalidad_pct_max"] if elegido else "",
            "identidad_tribolium": elegido["tcas_identidad"] if elegido else "",
        })

    con_locus_nuestro = [f for f in filas if f["locus"]]
    print(f"\nde esos, caen sobre un locus que ya teniamos: {len(con_locus_nuestro)}")
    nuevos = len(filas) - len(con_locus_nuestro)
    print(f"caen en una parte del genoma que no estaba en la tabla: {nuevos}")

    # ------------------------------------------------------------------
    print("\n=== cuanto baja el '100 % viene de otro orden' ===")
    loci_con_hemiptero = {f["locus"] for f in con_locus_nuestro if f["locus"]}
    print(f"loci de la tabla unificada: {total_loci}")
    print(f"loci con respaldo de un hemiptero: {len(loci_con_hemiptero)} "
          f"({len(loci_con_hemiptero)/total_loci*100:.2f} %)")

    # Sobre los de alta confianza, que son los que se presentan
    altos = set()
    ruta_altos = unificada.parent / "candidatos_alto.csv"
    if ruta_altos.exists():
        with ruta_altos.open(encoding="utf-8") as fh:
            altos = {f["locus"] for f in csv.DictReader(fh)}
        cruce = loci_con_hemiptero & altos
        print(f"\ncandidatos de nivel alto: {len(altos)}")
        print(f"de esos, con respaldo ADEMAS en un hemiptero: {len(cruce)} "
              f"({len(cruce)/max(len(altos),1)*100:.1f} %)")

    print("\n=== por familia de insecto que aporta la evidencia ===")
    for fam, n in Counter(f["familia_hemiptero"] for f in con_locus_nuestro).most_common():
        print(f"  {fam:<18}{n:>4}")

    print("\n=== por categoria de fenotipo del hemiptero ===")
    for cat, n in Counter(f["categoria_hemiptero"] for f in con_locus_nuestro).most_common():
        print(f"  {cat:<18}{n:>4}")

    print("\n=== concuerda el fenotipo del hemiptero con el de Tribolium? ===")
    comparables = [f for f in con_locus_nuestro
                   if f["categoria_tribolium"] and f["categoria_hemiptero"]]
    pares = Counter((f["categoria_hemiptero"], f["categoria_tribolium"]) for f in comparables)
    print(f"(loci donde hay fenotipo de los dos lados: {len(comparables)})")
    print(f"  {'hemiptero':<18}{'Tribolium':<20}{'loci':>5}")
    for (a, b), n in pares.most_common():
        print(f"  {a:<18}{b:<20}{n:>5}")
    letal_ambos = sum(n for (a, b), n in pares.items()
                      if a == "letal" and b in ("letal", "letal_embrionario"))
    if comparables:
        print(f"\n  letal en los dos: {letal_ambos} de {len(comparables)} "
              f"({letal_ambos/len(comparables)*100:.0f} %)")

    print("\n=== los loci con doble respaldo y nivel alto ===")
    dobles = [f for f in con_locus_nuestro if f["locus"] in altos]
    dobles.sort(key=lambda f: -float(f["identidad_hemiptero"] or 0))
    print(f"{'locus':<9}{'gen hemip.':<16}{'especie':<24}{'fenotipo':<12}"
          f"{'id.hem':>7}{'let%Tcas':>9}  gen Dmel")
    for f in dobles[:30]:
        print(f"{f['locus']:<9}{f['gen_hemiptero'][:15]:<16}{f['especie_hemiptero'][:23]:<24}"
              f"{f['categoria_hemiptero'][:11]:<12}{float(f['identidad_hemiptero']):>7.3f}"
              f"{(f['letalidad_tribolium'] or '-'):>9}  {f['gen_drosophila']}")

    if "--csv" in sys.argv:
        destino = Path(sys.argv[sys.argv.index("--csv") + 1])
        with destino.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
            w.writeheader()
            w.writerows(filas)
        print(f"\ncsv escrito en {destino}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

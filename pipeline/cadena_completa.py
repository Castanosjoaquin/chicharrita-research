"""La cadena entera: de la tabla de genes candidatos a los siRNA finales, filtrados por riesgo.

Junta las tres piezas que estaban sueltas:
  1. la tabla unificada de loci con fenotipo de RNAi conocido  (que gen atacar)
  2. la enumeracion y el scoring de ventanas de 21 nt          (que tramo de ese gen)
  3. el filtro de off-target contra organismos no objetivo     (cual no nos vuelve en contra)

Decision de diseno: el off-target se corre UNA sola vez, sobre todas las ventanas de todos los
genes juntos. Cada transcriptoma no objetivo pesa cientos de Mb; leerlo una vez por gen seria
tirar el tiempo.

Uso:
    python3 cadena_completa.py <N_genes> [--csv salida.csv]
"""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from sirna_enumerar import armar_cds, enumerar, leer_cromosoma, puntuar  # noqa: E402
from sirna_offtarget import (K, K_ALERTA, cargar_candidatos, escanear,  # noqa: E402
                             revcomp, semillas_alerta)

DATOS = Path.home() / "yhat" / "data"
SALIDA = Path(__file__).parent / "salida"
GENOMA = DATOS / "genome.fna.gz"
GFF_TCAS = DATOS / "tcas.gff"
GFF_DSRNASA = DATOS / "dsrnasas.gff"
NO_OBJETIVO = [DATOS / "maiz_rna.fna.gz", DATOS / "abeja_rna.fna.gz"]
VENTANAS_POR_GEN = 25


def indexar_gff_por_locus(gff: Path) -> dict[tuple[str, int, int], tuple[str, str, list]]:
    """mRNA del GFF indexado por (cromosoma, inicio, fin), mas sus exones CDS."""
    mrnas: dict[str, dict] = {}
    for linea in gff.read_text(encoding="utf-8").splitlines():
        if linea.startswith("#") or "\t" not in linea:
            continue
        c = linea.split("\t")
        if len(c) < 9:
            continue
        if c[2] == "mRNA":
            ident = c[8].split("ID=")[1].split(";")[0]
            mrnas[ident] = {"cromosoma": c[0], "ini": int(c[3]), "fin": int(c[4]),
                            "hebra": c[6], "exones": []}
        elif c[2] == "CDS" and "Parent=" in c[8]:
            padre = c[8].split("Parent=")[1].split(";")[0]
            if padre in mrnas:
                mrnas[padre]["exones"].append((int(c[3]), int(c[4])))
    salida = {}
    for ident, d in mrnas.items():
        if d["exones"]:
            d["exones"].sort(reverse=d["hebra"] == "-")
            salida[(d["cromosoma"], d["ini"], d["fin"])] = (ident, d["hebra"], d["exones"])
    return salida


def buscar_mrna(indice: dict, cromosoma: str, ini: int, fin: int, margen: int = 50):
    exacto = indice.get((cromosoma, ini, fin))
    if exacto:
        return exacto
    for (c, i, f), v in indice.items():
        if c == cromosoma and abs(i - ini) <= margen and abs(f - fin) <= margen:
            return v
    return None


def elegir_candidatos(objetivo: str, n_genes: int) -> list[dict]:
    """Rankea la tabla completa segun el objetivo de control pedido.

    Antes esto leia `candidatos_alto.csv`, que tenia "que mate" cableado. La validacion
    retrospectiva mostro el costo: el blanco que el grupo de Catalano eligio para esterilizar
    quedaba afuera, y no por error de calculo sino por tener un solo objetivo escondido.
    """
    from objetivo_candidatos import puntuar

    filas = list(csv.DictReader((SALIDA / "tabla_unificada.csv").open(encoding="utf-8")))
    con_score = [(puntuar(f, objetivo), f) for f in filas]
    elegidos = [f for s, f in sorted((x for x in con_score if x[0] > 0), key=lambda x: -x[0])]
    print(f"objetivo '{objetivo}': {len(elegidos)} loci con evidencia a favor, "
          f"tomo los primeros {n_genes}")
    return elegidos[:n_genes]


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    n_genes = int(args[0]) if args and args[0].isdigit() else 15
    objetivo = next((a for a in args if not a.isdigit()), "letal")
    con_par = "--con-par" in sys.argv

    candidatos = elegir_candidatos(objetivo, n_genes)
    if con_par:
        # El candidato deja de ser una secuencia sola: se suma el locus de la dsRNasa, que es
        # lo que despeja la barrera de entrega oral. Evidencia en 4 hemipteros, la nuestra
        # incluida (Dmai-dsRNase-2, 2023).
        candidatos.append({"locus": "DSRNASA", "cromosoma": "OZ319704.1",
                           "inicio": "60967170", "fin": "60973305",
                           "gen_drosophila": "anti-dsRNasa", "mejor_hit_tribolium": "",
                           "letalidad_pct_max": "", "hebra": "+"})
        print("modo par: se agrega el locus de dsRNasa como companero de entrega")

    print("indexando anotacion...", flush=True)
    indice = indexar_gff_por_locus(GFF_TCAS)
    if GFF_DSRNASA.exists():
        indice.update(indexar_gff_por_locus(GFF_DSRNASA))

    # candidatos ya viene recortado por elegir_candidatos; recortar de nuevo aca comia el par
    elegidos = candidatos
    cache_cromosoma: dict[str, str] = {}
    todas: list[dict] = []

    for cand in elegidos:
        hallado = buscar_mrna(indice, cand["cromosoma"], int(cand["inicio"]), int(cand["fin"]))
        if not hallado:
            print(f"  {cand['locus']}: sin estructura de exones en el GFF, lo salteo")
            continue
        ident, hebra, exones = hallado
        if cand["cromosoma"] not in cache_cromosoma:
            cache_cromosoma[cand["cromosoma"]] = leer_cromosoma(GENOMA, cand["cromosoma"])
        cds = armar_cds(cache_cromosoma[cand["cromosoma"]], hebra, exones)
        if len(cds) < 100:
            continue
        filas = enumerar(cds)
        puntuar(filas)
        mejores = sorted((f for f in filas if not f["descarte"]),
                         key=lambda f: -f["score_geom"])[:VENTANAS_POR_GEN]
        for f in mejores:
            f["locus"] = cand["locus"]
            f["gen_drosophila"] = cand["gen_drosophila"]
            f["tribolium"] = cand["mejor_hit_tribolium"]
            f["letalidad"] = cand["letalidad_pct_max"]
            f["identidad"] = cand.get("tcas_identidad", "")
        todas.extend(mejores)
        print(f"  {cand['locus']} ({cand['gen_drosophila'] or cand['mejor_hit_tribolium']}): "
              f"CDS {len(cds)} nt, {len(filas)} ventanas, me quedo con {len(mejores)}")

    if not todas:
        sys.exit("no quedo ninguna ventana")

    tmp = SALIDA / "_cadena_tmp.csv"
    with tmp.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(todas[0].keys()))
        w.writeheader()
        w.writerows(todas)

    print(f"\n{len(todas)} ventanas de {len(set(f['locus'] for f in todas))} genes. "
          f"Chequeando off-target en una sola pasada...", flush=True)

    exactos = cargar_candidatos(tmp)
    semillas = semillas_alerta(exactos)
    secuencias: dict[str, list[str]] = {}
    for kmero, claves in exactos.items():
        for c in claves:
            secuencias.setdefault(c, []).append(kmero)

    # Un maximo sobre todos los organismos juntos oculta algo que importa: una ventana que pega
    # fuerte en UNA especie no es lo mismo que una que pega en varias a la vez. Se guarda el
    # peor por organismo y despues se reporta tambien en cuantos pega.
    por_organismo: dict[str, dict[str, int]] = {}
    for ruta in NO_OBJETIVO:
        if not ruta.exists():
            continue
        peor_aca: dict[str, int] = {}
        r = escanear(ruta, exactos, semillas, secuencias, peor_aca)
        por_organismo[ruta.name.replace("_rna.fna.gz", "")] = peor_aca
        print(f"  {r['archivo']}: {len(r['exactos'])} ventanas con coincidencia de {K} nt")

    for f in todas:
        clave = f"{f['locus']}|{f['pos']}|{f['sitio'].upper()}"
        por_esp = {org: peor.get(clave, 0) for org, peor in por_organismo.items()}
        f["off_target_max"] = max(por_esp.values(), default=0)
        f["off_target_n_especies"] = sum(1 for v in por_esp.values() if v >= 17)
        f["off_target_peor_especie"] = max(por_esp, key=por_esp.get) if por_esp else ""
        f["off_target_detalle"] = ";".join(f"{o}:{v}" for o, v in sorted(por_esp.items()) if v > 0)
        # Pegar en varias especies a la vez es peor que pegar fuerte en una sola: sugiere que
        # el tramo toca algo conservado en todo el grupo, no una coincidencia puntual.
        f["riesgo"] = ("descartar" if f["off_target_max"] >= K or f["off_target_n_especies"] >= 3
                       else "alerta" if f["off_target_max"] >= 17 else "ok")

    limpias = [f for f in todas if f["riesgo"] == "ok"]
    print(f"\nventanas ok: {len(limpias)} · en alerta: "
          f"{sum(1 for f in todas if f['riesgo'] == 'alerta')} · descartadas: "
          f"{sum(1 for f in todas if f['riesgo'] == 'descartar')}")

    print(f"\nLos 12 siRNA finales (mejor ventana por gen, ya filtrados por riesgo):")
    print(f"{'locus':<9}{'gen':<10}{'let%':>6}{'pos':>7}  {'guia (5->3)':<23}{'score':>7}{'off':>5}")
    vistos: set[str] = set()
    for f in sorted(limpias, key=lambda f: -f["score_geom"]):
        if f["locus"] in vistos:
            continue
        vistos.add(f["locus"])
        gen = (f["gen_drosophila"] or f["tribolium"] or "")[:9]
        print(f"{f['locus']:<9}{gen:<10}{float(f['letalidad'] or 0):>6.0f}{f['pos']:>7}  "
              f"{f['guia']:<23}{f['score_geom']:>7.3f}{f['off_target_max']:>5}")
        if len(vistos) >= 12:
            break

    destino = SALIDA / "sirna_finales.csv"
    with destino.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(todas[0].keys()))
        w.writeheader()
        w.writerows(sorted(todas, key=lambda f: -f["score_geom"]))
    tmp.unlink(missing_ok=True)
    print(f"\ntabla final en {destino}")


if __name__ == "__main__":
    main()

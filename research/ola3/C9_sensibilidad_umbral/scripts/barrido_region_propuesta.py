"""C9 T1 bis - el barrido de umbrales sobre la region propuesta, con el veto.

Que pregunta contesta, y por que no la contestaba `barrido_umbral.py`. El barrido
original elige en cada punto de la grilla la mejor ventana de 200 posiciones del gen,
libre: sin veto de off-target y con el mismo largo para los cuatro genes. Eso mide
la fragilidad de "elegir la region mas densa", que no es la regla del ranking. La
regla del ranking (W7 nivel 3, C7 v2) elige la region mas densa **que escapa al veto
de coincidencia perfecta** y **conserva el largo al que fue elegida**: 200 posiciones
en los dos genes virales y 300 en los dos del insecto, que es el largo del amplicon
de la planilla de EPILAB. Con la region libre de 200 el par `ATPaseD_Dm`/`CP_MRFV`
queda a dos o tres ventanas y se da vuelta en media grilla; la pregunta abierta era
si eso tambien pasa con las regiones que efectivamente proponemos.

Cuatro escenarios por punto de la grilla, por modo y por largo de ventana:

  epilab            region de la planilla, fija.
  propuesta         region que proponemos (C7 v2 `regiones_recomendadas`), fija.
  reelegida_propio  se vuelve a elegir la region en cada punto con la regla del
                    ranking: largo propio del gen y veto aplicado.
  libre_200         mejor region de 200 sin veto = el escenario de `barrido_umbral.py`.
                    Esta de ancla: en los cuatro genes de EPILAB tiene que reproducir
                    `resultados/grilla_umbral.tsv` fila por fila.

El veto no depende de los umbrales de si-Fi21 (es coincidencia perfecta de k nt
contra el panel de referencias), asi que las posiciones vetadas se leen una vez de
`C7_ranking_v2/resultados/ranking_v2.json` y valen para toda la grilla. Panel de C7
v2, siete referencias, con el on-target ya excluido en ese archivo.

Motor: ViennaRNA 2.7.2 (backend `vienna`), 22 C, u = 8. Los conteos absolutos no
son comparables con RNAplfold 2.1.5; las comparaciones internas si, porque los dos
lados usan el mismo motor. Ninguna salida lleva columna de secuencia (ver la nota de
confidencialidad del REPORT: el TSV por ventana permite reconstruir el gen).

Uso (desde la raiz del repositorio):
    python research/ola3/C9_sensibilidad_umbral/scripts/barrido_region_propuesta.py
"""
import itertools
import json
import sys
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve()
RAIZ = AQUI.parents[4]
sys.path.insert(0, str(RAIZ / "tools" / "sifi21_port"))
from sifi_core import primitives, apply_rules  # noqa: E402

SALIDA = AQUI.parents[1] / "resultados"
RANKING = RAIZ / "research" / "ola3" / "C7_ranking_v2" / "resultados" / "ranking_v2.json"
GRILLA_VIEJA = SALIDA / "grilla_umbral.tsv"

# Los cuatro de EPILAB viven en work/ (dos son secuencias no publicadas); eth y
# burs-alpha son publicos y estan versionados con C5. La carpeta de work/ cambia de
# nombre entre maquinas, asi que se prueban las dos que existieron.
FASTA_EPILAB = [RAIZ / "work" / "sifi_check", RAIZ / "work" / "W5" / "fasta"]
FASTA_NUEVOS = (RAIZ / "research" / "ola3" / "C5_estructura_genes_ingenieria_inversa"
                / "resultados" / "candidatos_c5.fa")
NOMBRE_EN_C5 = {"eth_Dm": "eth_Dmaidis_PZ371507", "bursA_Dm": "bursA_Dmaidis_PZ371508"}

EPILAB = ["ATPaseD_Dm", "BicC_Dm", "CP_MRFV", "MP_MRFV"]
GENES = EPILAB + ["eth_Dm", "bursA_Dm"]
MODOS = ["fiel", "corregido"]
KS = [21, 22]
U = 8
TEMP = 22.0
END_GRID = [round(0.1 * i, 2) for i in range(21)]          # 0,0 .. 2,0 kcal/mol
ACC_GRID = [round(0.05 + 0.01 * i, 2) for i in range(26)]  # 0,05 .. 0,30
DEF_END, DEF_ACC = 1.0, 0.1
ESCENARIOS = ["epilab", "propuesta", "reelegida_propio", "libre_200"]


def leer_fasta_simple(ruta):
    return "".join(l.strip() for l in Path(ruta).read_text().splitlines()
                   if not l.startswith(">"))


def leer_multifasta(ruta):
    seqs, nombre = {}, None
    for linea in Path(ruta).read_text().splitlines():
        if linea.startswith(">"):
            nombre = linea[1:].split()[0]
            seqs[nombre] = []
        elif nombre:
            seqs[nombre].append(linea.strip())
    return {k: "".join(v) for k, v in seqs.items()}


def cargar_secuencias():
    carpeta = next((c for c in FASTA_EPILAB if (c / "ATPaseD_Dm_full.fasta").exists()), None)
    if carpeta is None:
        raise SystemExit("No estan los FASTA de EPILAB. Probe: %s"
                         % ", ".join(str(c) for c in FASTA_EPILAB))
    seqs = {g: leer_fasta_simple(carpeta / f"{g}_full.fasta") for g in EPILAB}
    c5 = leer_multifasta(FASTA_NUEVOS)
    for gen, nom in NOMBRE_EN_C5.items():
        seqs[gen] = c5[nom]
    return seqs, carpeta


def cargar_ranking():
    """Regiones y posiciones vetadas de C7 v2, por largo de ventana."""
    d = json.loads(RANKING.read_text(encoding="utf-8"))
    out = {}
    for k in KS:
        blk = d["k"][str(k)]
        regiones = {}
        for etiqueta, clave in (("epilab", "regiones"), ("propuesta", "regiones_recomendadas")):
            regiones[etiqueta] = {g: tuple(int(x) for x in blk[clave][g].split("-"))
                                  for g in GENES}
        veto = {}
        for g in GENES:
            pos = set()
            for crits in blk["gen_entero"][g]["por_referencia"].values():
                pos.update(crits.get("perfecto_21_posiciones") or [])
            veto[g] = np.array(sorted(pos), dtype=int)
        ancla = {f["gen"]: (f["eficientes_gen"], f["ventanas_gen"],
                            f["mecanicista"]["eficientes"])
                 for f in blk["fichas_recomendadas"]}
        out[k] = {"regiones": regiones, "veto": veto, "ancla": ancla}
    return out


def mascara_veto(n, posiciones, largo):
    """True en los arranques cuya region de `largo` posiciones NO contiene vetada."""
    ultimo = max(1, n - largo + 1)
    ok = np.ones(ultimo, dtype=bool)
    for p in posiciones:
        lo = max(1, p - largo + 1)
        hi = min(ultimo, p)
        if lo <= hi:
            ok[lo - 1:hi] = False
    return ok


def conteos_por_region(eff, largo):
    n = len(eff)
    cs = np.concatenate([[0], np.cumsum(eff)])
    ultimo = max(1, n - largo + 1)
    arranques = np.arange(1, ultimo + 1)
    return cs[np.minimum(arranques - 1 + largo, n)] - cs[arranques - 1]


def mejor_region(eff, largo, permitidas=None):
    """Primer maximo gana, igual que `sifi_core.best_region`; solo regiones completas."""
    cuenta = conteos_por_region(eff, largo)
    if permitidas is not None:
        cuenta = np.where(permitidas, cuenta, -1)
        if cuenta.max() < 0:
            return None
    i = int(np.argmax(cuenta))
    return i + 1, i + largo, int(cuenta[i])


def solapamiento(a, b):
    return max(0, min(a[1], b[1]) - max(a[0], b[0]) + 1)


def intervalo(valores, vale, defecto):
    """Tramo contiguo alrededor del valor por defecto donde `vale(v)` es verdadero.

    Mide hasta donde se puede mover un umbral, con el otro en su valor por defecto,
    sin que cambie lo que se afirma. Devuelve None si falla en el propio defecto.
    """
    i = valores.index(defecto)
    if not vale(valores[i]):
        return None
    lo = hi = i
    while lo > 0 and vale(valores[lo - 1]):
        lo -= 1
    while hi < len(valores) - 1 and vale(valores[hi + 1]):
        hi += 1
    return [valores[lo], valores[hi]]


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    seqs, carpeta = cargar_secuencias()
    rk = cargar_ranking()
    print("FASTA de EPILAB:", carpeta, flush=True)

    prims = {}
    for k in KS:
        for g in GENES:
            prims[(k, g)] = primitives(seqs[g], temp_c=TEMP, backend="vienna", sirna_size=k)
        print("k=%d: %s" % (k, ", ".join("%s %d ventanas" % (g, len(prims[(k, g)]))
                                         for g in GENES)), flush=True)

    filas, eficacias = [], {}
    for k, modo, e, a in itertools.product(KS, MODOS, END_GRID, ACC_GRID):
        defecto = int(e == DEF_END and a == DEF_ACC)
        for g in GENES:
            eff = np.array([apply_rules([p], mode=modo, u=U, end_thr=e, access_thr=a,
                                        sirna_size=k) for p in prims[(k, g)]], dtype=float)
            n = len(eff)
            prop = rk[k]["regiones"]["propuesta"][g]
            largo_propio = prop[1] - prop[0] + 1
            permitidas = mascara_veto(n, rk[k]["veto"][g], largo_propio)
            regiones = {}
            for esc in ("epilab", "propuesta"):
                ini, fin = rk[k]["regiones"][esc][g]
                regiones[esc] = (ini, fin, int(eff[ini - 1:fin].sum()))
            regiones["reelegida_propio"] = mejor_region(eff, largo_propio, permitidas)
            regiones["libre_200"] = mejor_region(eff, 200)
            for esc, reg in regiones.items():
                if reg is None:
                    continue
                ini, fin, cnt = reg
                largo = fin - ini + 1
                vetada = bool(((rk[k]["veto"][g] >= ini) & (rk[k]["veto"][g] <= fin)).any())
                filas.append({"k": k, "modo": modo, "end_thr": e, "access_thr": a,
                              "escenario": esc, "gen": g, "region_inicio": ini,
                              "region_fin": fin, "largo_region": largo,
                              "n_ventanas_gen": n, "n_eficientes_gen": int(eff.sum()),
                              "region_eficientes": cnt,
                              "eficacia_region": round(cnt / largo, 6),
                              "vetada": int(vetada), "es_defecto": defecto})
                eficacias[(k, modo, e, a, esc, g)] = (cnt / largo, (ini, fin))

    cols = list(filas[0].keys())
    with open(SALIDA / "grilla_region_propuesta.tsv", "w", encoding="utf-8") as fh:
        fh.write("\t".join(cols) + "\n")
        for f in filas:
            fh.write("\t".join(str(f[c]) for c in cols) + "\n")
    print("grilla escrita: %d filas" % len(filas), flush=True)

    # ---------------------------------------------------------------- analisis
    puntos = [(e, a) for e in END_GRID for a in ACC_GRID]
    resumen = {"grilla": {"end_thr": [END_GRID[0], END_GRID[-1]],
                          "access_thr": [ACC_GRID[0], ACC_GRID[-1]],
                          "puntos_por_modo_y_k": len(puntos)},
               "motor": {"backend": "vienna", "version": "ViennaRNA 2.7.2",
                         "temp_c": TEMP, "u": U},
               "fuente_regiones_y_veto": str(RANKING.relative_to(RAIZ)).replace("\\", "/"),
               "pares": {}, "orden": {}, "estabilidad_region": {}, "anclas": {}}

    for k, modo, esc in itertools.product(KS, MODOS, ESCENARIOS):
        clave = "k%d/%s/%s" % (k, modo, esc)
        pares = {}
        for g1, g2 in itertools.combinations(GENES, 2):
            d0 = (eficacias[(k, modo, DEF_END, DEF_ACC, esc, g1)][0]
                  - eficacias[(k, modo, DEF_END, DEF_ACC, esc, g2)][0])
            signo0 = np.sign(round(d0, 9))
            invertidos = empates = 0
            for e, a in puntos:
                d = (eficacias[(k, modo, e, a, esc, g1)][0]
                     - eficacias[(k, modo, e, a, esc, g2)][0])
                s = np.sign(round(d, 9))
                if s == 0:
                    empates += 1
                elif signo0 != 0 and s != signo0:
                    invertidos += 1
            def mismo_signo(e_, a_, g1=g1, g2=g2, signo0=signo0):
                d_ = (eficacias[(k, modo, e_, a_, esc, g1)][0]
                      - eficacias[(k, modo, e_, a_, esc, g2)][0])
                return np.sign(round(d_, 9)) == signo0
            pares["%s - %s" % (g1, g2)] = {
                "dif_en_defecto": round(d0, 6),
                "invertido_pct": round(100 * invertidos / len(puntos), 1),
                "empate_exacto_pct": round(100 * empates / len(puntos), 1),
                "intervalo_end_thr": intervalo(END_GRID, lambda v: mismo_signo(v, DEF_ACC), DEF_END),
                "intervalo_access_thr": intervalo(ACC_GRID, lambda v: mismo_signo(DEF_END, v), DEF_ACC)}
        resumen["pares"][clave] = pares

        # Quien queda primero, y el orden completo, en cada punto de la grilla.
        primero, ordenes = {g: 0 for g in GENES}, {}
        empate_arriba = 0
        for e, a in puntos:
            vals = {g: eficacias[(k, modo, e, a, esc, g)][0] for g in GENES}
            top = max(vals.values())
            arriba = [g for g in GENES if vals[g] == top]
            if len(arriba) == 1:
                primero[arriba[0]] += 1
            else:
                empate_arriba += 1
            orden = tuple(sorted(GENES, key=lambda g: (-vals[g], g)))
            ordenes[orden] = ordenes.get(orden, 0) + 1
        modal = max(ordenes.items(), key=lambda kv: kv[1])
        resumen["orden"][clave] = {
            "primero_pct": {g: round(100 * n / len(puntos), 1) for g, n in primero.items()},
            "empate_en_el_primer_puesto_pct": round(100 * empate_arriba / len(puntos), 1),
            "orden_modal": list(modal[0]),
            "orden_modal_pct": round(100 * modal[1] / len(puntos), 1),
            "ordenes_distintos": len(ordenes)}

        est = {}
        for g in GENES:
            ref = eficacias[(k, modo, DEF_END, DEF_ACC, esc, g)][1]
            iguales = sol = 0
            minimo = 10 ** 9
            for e, a in puntos:
                reg = eficacias[(k, modo, e, a, esc, g)][1]
                iguales += int(reg == ref)
                s = solapamiento(reg, ref)
                minimo = min(minimo, s)
                sol += int(s >= 100)
            est[g] = {"region_en_defecto": "%d-%d" % ref,
                      "identica_pct": round(100 * iguales / len(puntos), 1),
                      "solapa_100_pct": round(100 * sol / len(puntos), 1),
                      "solapamiento_minimo": minimo}
        resumen["estabilidad_region"][clave] = est

    # Ancla 1: `libre_200` tiene que reproducir grilla_umbral.tsv (k=21, 4 genes).
    indice = {(f["k"], f["modo"], f["end_thr"], f["access_thr"], f["escenario"], f["gen"]): f
              for f in filas}
    coinciden = comparadas = 0
    for linea in GRILLA_VIEJA.read_text(encoding="utf-8").splitlines()[1:]:
        c = linea.split("\t")
        f = indice.get((21, c[0], float(c[1]), float(c[2]), "libre_200", c[3]))
        if f is None:
            continue
        comparadas += 1
        coinciden += int((f["region_inicio"], f["region_fin"], f["region_eficientes"])
                         == (int(c[6]), int(c[7]), int(c[8])))
    resumen["anclas"]["libre_200_contra_grilla_umbral"] = {
        "filas_comparadas": comparadas, "identicas": coinciden}

    # Ancla 2: el punto por defecto, modo corregido, contra las fichas de C7 v2.
    ancla_c7 = {}
    for k in KS:
        for g in GENES:
            esperado = rk[k]["ancla"][g]
            f = indice[(k, "corregido", DEF_END, DEF_ACC, "propuesta", g)]
            ancla_c7["k%d/%s" % (k, g)] = {
                "eficientes_gen": [f["n_eficientes_gen"], esperado[0]],
                "ventanas_gen": [f["n_ventanas_gen"], esperado[1]],
                "eficientes_region": [f["region_eficientes"], esperado[2]],
                "coincide": bool(f["n_eficientes_gen"] == esperado[0]
                                 and f["n_ventanas_gen"] == esperado[1]
                                 and f["region_eficientes"] == esperado[2])}
    resumen["anclas"]["propuesta_defecto_contra_C7"] = ancla_c7

    (SALIDA / "pares_region_propuesta.json").write_text(
        json.dumps(resumen, ensure_ascii=False, indent=1), encoding="utf-8")

    ok1 = resumen["anclas"]["libre_200_contra_grilla_umbral"]
    ok2 = sum(v["coincide"] for v in ancla_c7.values())
    print("ancla libre_200 contra grilla_umbral.tsv: %d de %d filas identicas"
          % (ok1["identicas"], ok1["filas_comparadas"]))
    print("ancla punto por defecto contra fichas de C7 v2: %d de %d genes"
          % (ok2, len(ancla_c7)))
    for k in KS:
        p = resumen["pares"]["k%d/corregido/propuesta" % k]["ATPaseD_Dm - CP_MRFV"]
        q = resumen["pares"]["k%d/corregido/libre_200" % k]["ATPaseD_Dm - CP_MRFV"]
        print("k=%d corregido  ATPaseD-CP   propuesta: dif %+.4f, invertido %.1f%% | "
              "libre_200: dif %+.4f, invertido %.1f%%"
              % (k, p["dif_en_defecto"], p["invertido_pct"],
                 q["dif_en_defecto"], q["invertido_pct"]))


if __name__ == "__main__":
    main()

"""Ranking de candidatos: combina el perfil de eficiencia de si-Fi21 con el de off-targets.

Consume los mismos TSV que `cruce.py` —el perfil por ventana que escribe `run_sifi.py`
y la matriz por ventana que escribe `offtarget_21nt.py`— y produce un orden de
candidatos con el criterio de combinacion explicito y barrido.

Dos subcomandos:

  nulo      La medicion que adjudica si elegir region dentro de un gen discrimina.
            Para cada gen calcula la distribucion COMPLETA del conteo de eficientes
            sobre todas las regiones deslizantes del largo que uso EPILAB, y ubica en
            esa distribucion la region elegida y la mejor. El resultado es un
            percentil, que es falsable; «21 % por debajo del optimo» no lo es, porque
            el maximo sobre cientos de regiones superpuestas esta sesgado hacia
            arriba por construccion y este script mide cuanto.
            Dos nulos por permutacion, para que la comparacion con el resultado
            negativo de `pipeline/REPORT.md` §6 sea una medicion y no una analogia:
            barajar la etiqueta de eficiente entre ventanas (destruye toda
            estructura local) y permutar bloques de 30 ventanas (el mismo nulo que
            uso el 7,2 %, que preserva la estructura local).

  ranking   El orden de candidatos. Dos ejes por candidato:
              eficacia  = ventanas eficientes / ventanas de la region           [0,1]
              limpieza  = 1 - exposicion ponderada normalizada                  [0,1]
            Tres formas de combinarlos, porque no dicen lo mismo sobre el problema
            (ver D1 en `00_meta/DECISIONS.md`):
              geometrica  media geometrica ponderada: un eje cerca de cero no se
                          compensa con el otro. Es el metodo que ya resolvio esta
                          misma pregunta en `pipeline/REPORT.md` §5.
              suma        suma ponderada: una region muy eficiente compra su riesgo.
              cascada     veto duro mas conteo de eficientes limpios, que es la
                          posicion que ya tomo `pipeline/region_scoring.py`.
            El resultado reportado es el barrido: con 2.000 juegos de pesos sobre el
            simplex se informa la frecuencia de cada candidato en cada posicion, no
            un orden puntual bajo pesos elegidos a dedo.

El paso de «esta region gana el orden» a «esta region es la que recomendamos» pasa por
`region_recomendada()`, y esa funcion llama a la compuerta de alertas de D48
(`alertas.exigir_decidida`): una region con una fila de alerta en «pendiente» no sale de
ahi, y desde D72 tampoco sale una region que **no este en el inventario de regiones
tamizadas** de M6, porque cero filas de alerta significa «no se tamizo» tanto como «se
tamizo y no hay». El umbral de D28 con el que la compuerta exige decision es
`UMBRAL_COMPUERTA` y se mueve con `--umbral-compuerta` (D69).

Uso:
    python ranking.py nulo --dir work/sifi_check --perfil work/sifi_check/salida
    python ranking.py ranking --dir work/sifi_check --perfil work/sifi_check/salida \
        --offtarget work/sifi_check/offtarget_full/offtarget_por_sirna.tsv \
        --mm1 work/sifi_check/offtarget_mm1_{gen}/offtarget_por_sirna.tsv \
        --json research/ola2/W7_ranking/ranking.json
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import alertas as AL  # noqa: E402

# Los cuatro candidatos de la planilla de EPILAB. La region es la que declara la
# planilla; `CP_MRFV` dice «200-400», que son 201 posiciones para una secuencia de
# 200 nt, y se resolvio localizando la subcadena exacta: es 201-400. Ver
# `research/ola2/W5_secuencias_epilab/sifi21_reproduccion.md`.
CANDIDATOS = [
    {"gen": "MP_MRFV",    "region": (1, 200),    "estrategia": "virus",
     "organismo": "Maize rayado fino virus", "funcion": "proteina de movimiento"},
    {"gen": "CP_MRFV",    "region": (201, 400),  "estrategia": "virus",
     "organismo": "Maize rayado fino virus", "funcion": "proteina de capside"},
    {"gen": "BicC_Dm",    "region": (264, 563),  "estrategia": "insecto",
     "organismo": "Dalbulus maidis", "funcion": "Bicaudal C"},
    {"gen": "ATPaseD_Dm", "region": (151, 450),  "estrategia": "insecto",
     "organismo": "Dalbulus maidis", "funcion": "subunidad D de V-ATPasa"},
]

# Nombre corto de cada referencia del panel, y por que esta en el panel. El peso
# base es nuestro y se justifica por consecuencia, no por simetria (D3); el barrido
# lo mueve sobre todo el simplex, asi que el orden que sobrevive no depende de el.
REFERENCIAS = {
    "GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna":
        {"corto": "maiz", "especie": "Zea mays", "rol": "el cultivo que se protege",
         "peso": 1.00},
    "GCF_914767665.1_icHarAxyr1.1_rna":
        {"corto": "H_axyridis", "especie": "Harmonia axyridis",
         "rol": "enemigo natural del propio blanco", "peso": 0.80},
    "GCF_003254395.2_Amel_HAv3.1_rna":
        {"corto": "A_mellifera", "especie": "Apis mellifera",
         "rol": "polinizador; el costo es regulatorio antes que ecologico", "peso": 0.80},
    "GCF_021130785.1_UT_GWSS_2.1_rna":
        {"corto": "H_vitripennis", "especie": "Homalodisca vitripennis",
         "rol": "cicadelido no objetivo; sustituto medible de los nativos que no lo son",
         "peso": 0.60},
    "GCF_002217175.1_ASM221717v1_rna":
        {"corto": "F_candida", "especie": "Folsomia candida",
         "rol": "fauna del suelo, especie modelo de ecotoxicologia", "peso": 0.40},
}
# El genoma del vector. Para los genes del insecto es ON-target y se excluye del
# computo de riesgo; para los genes virales es una decision de signo, no un dato
# (D5), y entra por el parametro `--dmaidis-viral`.
DMAIDIS = "GCA_975739785.1_ihDalMaid1.1_genomic"
DMAIDIS_INFO = {"corto": "D_maidis", "especie": "Dalbulus maidis",
                "rol": "el vector; on-target de los genes del insecto y de signo "
                       "discutible para los virales (D5)",
                "peso": 0.60}


def corto(ref: str) -> str:
    return REFERENCIAS[ref]["corto"] if ref in REFERENCIAS else DMAIDIS_INFO["corto"]

# Los tres criterios de riesgo, del mas fuerte al mas debil. El peso base es
# nuestro (D4). El orden SI esta sostenido: un bloque perfecto mas largo no puede
# ser menos riesgoso que uno mas corto. Las magnitudes no lo estan, y por eso el
# barrido las mueve conservando el orden.
CRITERIOS = ["perfecto_21", "perfecto_ge19", "mm1_21"]
PESO_CRITERIO = {"perfecto_21": 1.00, "perfecto_ge19": 0.60, "mm1_21": 0.30}

VENTANA = 21


# --------------------------------------------------------------------------- datos

def leer_perfil(perfil: Path, gen: str) -> tuple[np.ndarray, np.ndarray]:
    """Posiciones de inicio y etiqueta de eficiente, del TSV de `run_sifi.py`."""
    ruta = perfil / ("%s_full_corregido_vienna.tsv" % gen)
    pos, efi = [], []
    with ruta.open(encoding="utf-8") as fh:
        for fila in csv.DictReader(fh, delimiter="\t"):
            pos.append(int(fila["pos"]))
            efi.append(fila["is_efficient"] == "True")
    if not pos:
        sys.exit("perfil vacio: %s" % ruta)
    return np.array(pos), np.array(efi, dtype=bool)


def leer_offtarget(ruta: Path, consulta: str, n_pos: int) -> dict[str, np.ndarray]:
    """Matriz (referencia, criterio) -> vector booleano por posicion de inicio.

    Indexado 1..n_pos en la posicion 0..n_pos-1 del vector; una posicion sin fila en
    el TSV queda en False, que es lo correcto: `offtarget_21nt.py` saltea las
    ventanas con bases ambiguas.
    """
    out: dict[str, np.ndarray] = {}
    with ruta.open(encoding="utf-8") as fh:
        r = csv.DictReader(fh, delimiter="\t")
        cols = [c for c in (r.fieldnames or []) if "|" in c]
        for c in cols:
            out[c] = np.zeros(n_pos, dtype=bool)
        for fila in r:
            if fila["consulta"] != consulta:
                continue
            i = int(fila["pos"]) - 1
            if not 0 <= i < n_pos:
                continue
            for c in cols:
                if int(fila[c] or 0) > 0:
                    out[c][i] = True
    return out


def cargar_gen(gen: str, perfil: Path, off: Path | None, mm1: str | None) -> dict:
    """Perfil de eficiencia y matriz de riesgo de un gen, alineados por posicion."""
    pos, efi = leer_perfil(perfil, gen)
    n = int(pos.max())
    eficiente = np.zeros(n, dtype=bool)
    eficiente[pos - 1] = efi
    presente = np.zeros(n, dtype=bool)
    presente[pos - 1] = True

    riesgo: dict[str, dict[str, np.ndarray]] = {}
    if off is not None:
        cols = leer_offtarget(off, "%s_full" % gen, n)
        for clave, vec in cols.items():
            ref, crit = clave.split("|")
            riesgo.setdefault(ref, {})[crit] = vec
    if mm1:
        ruta = Path(mm1.replace("{gen}", gen))
        if ruta.exists():
            for clave, vec in leer_offtarget(ruta, "%s_full" % gen, n).items():
                ref, crit = clave.split("|")
                if crit == "mm1_21":
                    riesgo.setdefault(ref, {})[crit] = vec
    for ref in riesgo:
        for crit in CRITERIOS:
            riesgo[ref].setdefault(crit, np.zeros(n, dtype=bool))
    return {"gen": gen, "n": n, "eficiente": eficiente, "presente": presente,
            "riesgo": riesgo}


# ------------------------------------------------------------------- T1: el nulo

def conteo_por_region(marca: np.ndarray, largo: int) -> np.ndarray:
    """Conteo de marcas por region deslizante, indexado por inicio 1..n-largo+1.

    La convencion es la de `sifi_core.best_region` y la de la columna «en contexto»
    de `sifi21_reproduccion.md` §2: una region [i, i+largo-1] cuenta las ventanas
    cuya posicion de INICIO cae en ese intervalo.
    """
    acum = np.concatenate([[0], np.cumsum(marca.astype(int))])
    inicios = np.arange(1, len(marca) - largo + 2)
    return acum[inicios + largo - 1] - acum[inicios - 1]


def nulo_etiquetas(marca: np.ndarray, largo: int, reps: int,
                   rng) -> tuple[np.ndarray, np.ndarray]:
    """Maximo del conteo por region barajando la etiqueta entre todas las ventanas.

    Destruye toda estructura local y conserva solo cuantas ventanas eficientes hay.
    Contesta: estan agrupadas las eficientes mas de lo que agruparia el azar?

    Devuelve (maximos, ganancias), donde la ganancia de cada repeticion es su propio
    maximo sobre su propia media. Dividir el maximo nulo por la media OBSERVADA
    seria mezclar dos distribuciones: la media de las regiones nulas no es la
    observada, porque las eficientes de verdad no estan repartidas uniformemente a
    lo largo del gen y las regiones del centro cubren mas ventanas que las del borde.
    """
    n, k = len(marca), int(marca.sum())
    maxs, gan = np.empty(reps), np.empty(reps)
    for i in range(reps):
        e = np.zeros(n, dtype=bool)
        e[rng.choice(n, k, replace=False)] = True
        c = conteo_por_region(e, largo)
        maxs[i] = c.max()
        gan[i] = c.max() / c.mean() - 1 if c.mean() else 0.0
    return maxs, gan


def nulo_bloques(marca: np.ndarray, largo: int, reps: int, rng,
                 bloque: int = 30) -> tuple[np.ndarray, np.ndarray]:
    """Maximo del conteo permutando bloques contiguos de `bloque` ventanas.

    Es el nulo que uso el resultado del 7,2 % (`baseline_dsrip/region_nulo_multigen.py`).
    Preserva la estructura local dentro de cada bloque y solo reordena los bloques.
    """
    bl = [marca[i:i + bloque] for i in range(0, len(marca), bloque)]
    maxs, gan = np.empty(reps), np.empty(reps)
    for i in range(reps):
        e = np.concatenate([bl[j] for j in rng.permutation(len(bl))])
        c = conteo_por_region(e, largo)
        maxs[i] = c.max()
        gan[i] = c.max() / c.mean() - 1 if c.mean() else 0.0
    return maxs, gan


def correlacion_con_pipeline(perfil: Path, raiz: Path) -> list[dict]:
    """Los dos puntajes sobre las MISMAS regiones de los mismos genes.

    La adjudicacion de T1 necesita saber si el puntaje biofisico del pipeline y la
    densidad de eficientes de si-Fi21 miden lo mismo. Si correlacionan, una es
    sustituta de la otra y las dos mediciones no se contradicen; si no, hay que
    elegir cual manda.

    Advertencia que vale mas que el numero: las regiones deslizantes se superponen
    casi del todo, asi que el n efectivo es del orden de las regiones
    independientes —el largo del gen dividido el largo de la region— y no de las
    cientos que se promedian. El signo y la magnitud significan algo; un valor p
    sobre estos pares no significaria nada y por eso no se calcula.
    """
    sys.path.insert(0, str(raiz / "pipeline"))
    import sirna_enumerar as se

    def spearman(x, y):
        rx = np.argsort(np.argsort(x)).astype(float)
        ry = np.argsort(np.argsort(y)).astype(float)
        return float(np.corrcoef(rx, ry)[0, 1])

    filas = []
    for c in CANDIDATOS:
        gen = c["gen"]
        ini, fin = c["region"]
        largo = fin - ini + 1
        ruta = raiz / "work" / "sifi_check" / ("%s_full.fasta" % gen)
        seq = "".join(l.strip() for l in ruta.read_text().splitlines()
                      if not l.startswith(">")).upper().replace("U", "T")
        ventanas = se.enumerar(seq)
        se.puntuar(ventanas)
        n = max(int(f["pos"]) for f in ventanas)
        # Las descartadas cuentan 0, que es la convencion de `region_scoring.py`.
        puntos = np.zeros(n)
        for f in ventanas:
            puntos[int(f["pos"]) - 1] = (0.0 if f.get("descarte")
                                         else float(f["score"] or 0.0))
        acum = np.concatenate([[0.0], np.cumsum(puntos)])
        ini_p = np.arange(1, n - largo + 2)
        media_p = (acum[ini_p + largo - 1] - acum[ini_p - 1]) / largo

        g = cargar_gen(gen, perfil, None, None)
        cuenta = conteo_por_region(g["eficiente"], largo)
        ini_s = np.arange(1, len(cuenta) + 1)

        lo, hi = max(ini_p[0], ini_s[0]), min(ini_p[-1], ini_s[-1])
        mp = media_p[(ini_p >= lo) & (ini_p <= hi)]
        cs = cuenta[(ini_s >= lo) & (ini_s <= hi)]
        filas.append({"gen": gen, "regiones_comparadas": int(len(mp)),
                      "regiones_independientes": round(n / largo, 1),
                      "spearman": round(spearman(mp, cs), 3),
                      "pearson": round(float(np.corrcoef(mp, cs)[0, 1]), 3)})
    return filas


def cmd_nulo(a) -> int:
    perfil = Path(a.perfil)
    rng = np.random.default_rng(a.semilla)
    filas = []
    for c in CANDIDATOS:
        g = cargar_gen(c["gen"], perfil, None, None)
        ini, fin = c["region"]
        largo = fin - ini + 1
        conteo = conteo_por_region(g["eficiente"], largo)
        inicios = np.arange(1, len(conteo) + 1)
        n_eleg = int(conteo[ini - 1])
        n_mejor = int(conteo.max())
        ini_mejor = int(inicios[int(conteo.argmax())])

        obs = n_mejor
        ne, ne_gan = nulo_etiquetas(g["eficiente"], largo, a.reps, rng)
        nb, nb_gan = nulo_bloques(g["eficiente"], largo, a.reps, rng)
        filas.append({
            "gen": c["gen"], "largo_region": largo,
            "region_elegida": "%d-%d" % (ini, fin),
            "regiones_posibles": int(len(conteo)),
            "eficientes_gen": int(g["eficiente"].sum()),
            "ventanas_gen": int(g["presente"].sum()),
            "eficientes_elegida": n_eleg,
            "eficientes_mejor": n_mejor,
            "region_mejor": "%d-%d" % (ini_mejor, ini_mejor + largo - 1),
            "percentil_elegida": round(float((conteo <= n_eleg).mean() * 100), 1),
            "mediana_regiones": float(np.median(conteo)),
            "media_regiones": round(float(conteo.mean()), 2),
            "minimo_regiones": int(conteo.min()),
            # Los cuartiles dicen dónde está la masa de la distribución, que es lo
            # que el mínimo y el máximo solos no dicen: entre dos genes con el mismo
            # rango, uno puede tener casi todas las regiones apiladas y el otro
            # repartidas. Es lo que hace legible el percentil de la región elegida.
            "p25_regiones": float(np.percentile(conteo, 25)),
            "p75_regiones": float(np.percentile(conteo, 75)),
            "brecha_vs_mejor_pct": round(-100.0 * (n_mejor - n_eleg) / n_mejor, 1),
            "ganancia_max_observada_pct": round(100.0 * (obs / conteo.mean() - 1), 1),
            "ganancia_max_nulo_etiquetas_pct": round(100.0 * float(ne_gan.mean()), 1),
            "ganancia_max_nulo_bloques30_pct": round(100.0 * float(nb_gan.mean()), 1),
            "nulo_etiquetas_max_medio": round(float(ne.mean()), 1),
            "nulo_etiquetas_z": round(float((obs - ne.mean()) / ne.std()), 2),
            "nulo_etiquetas_p": round(float((ne >= obs).mean()), 4),
            "nulo_bloques30_max_medio": round(float(nb.mean()), 1),
            "nulo_bloques30_z": round(float((obs - nb.mean()) / nb.std()), 2),
            "nulo_bloques30_p": round(float((nb >= obs).mean()), 4),
        })

    print("Distribucion del conteo de eficientes sobre TODAS las regiones del mismo largo")
    print("%-12s%5s%9s%9s%7s%8s%9s%8s%7s" % (
        "gen", "L", "regiones", "elegida", "pct", "mejor", "mediana", "media", "min"))
    for f in filas:
        print("%-12s%5d%9d%9d%7.1f%8d%9.1f%8.1f%7d" % (
            f["gen"], f["largo_region"], f["regiones_posibles"],
            f["eficientes_elegida"], f["percentil_elegida"], f["eficientes_mejor"],
            f["mediana_regiones"], f["media_regiones"], f["minimo_regiones"]))

    print("\nCuanto de la ventaja del maximo es artefacto de maximizar sobre regiones"
          " superpuestas")
    print("%-12s%14s%16s%12s" % ("gen", "ganancia obs", "ganancia nula", "resto"))
    for f in filas:
        o, u = f["ganancia_max_observada_pct"], f["ganancia_max_nulo_etiquetas_pct"]
        print("%-12s%13.1f%%%15.1f%%%11.1f%%" % (f["gen"], o, u, o - u))

    print("\nDos nulos sobre el mismo maximo observado (%d repeticiones)" % a.reps)
    print("%-12s%8s%12s%7s%8s%12s%7s%8s" % (
        "gen", "obs", "etiq medio", "z", "p", "bloq medio", "z", "p"))
    for f in filas:
        print("%-12s%8d%12.1f%7.2f%8.4f%12.1f%7.2f%8.4f" % (
            f["gen"], f["eficientes_mejor"], f["nulo_etiquetas_max_medio"],
            f["nulo_etiquetas_z"], f["nulo_etiquetas_p"],
            f["nulo_bloques30_max_medio"], f["nulo_bloques30_z"],
            f["nulo_bloques30_p"]))

    sig_e = sum(1 for f in filas if f["nulo_etiquetas_p"] < 0.05)
    sig_b = sum(1 for f in filas if f["nulo_bloques30_p"] < 0.05)
    print("\ngenes con p<0,05: %d de %d con el nulo de etiquetas, %d de %d con el de"
          " bloques de 30" % (sig_e, len(filas), sig_b, len(filas)))

    corr = None
    if a.correlacion:
        raiz = Path(a.raiz).resolve()
        corr = correlacion_con_pipeline(Path(a.perfil), raiz)
        print("\nLos dos puntajes sobre las mismas regiones (n efectivo bajo: las"
              " regiones se superponen)")
        print("%-12s%11s%14s%10s%10s" % (
            "gen", "regiones", "independ.", "Spearman", "Pearson"))
        for f in corr:
            print("%-12s%11d%14.1f%10.3f%10.3f" % (
                f["gen"], f["regiones_comparadas"], f["regiones_independientes"],
                f["spearman"], f["pearson"]))

    if a.json:
        Path(a.json).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json).write_text(json.dumps(
            {"reps": a.reps, "semilla": a.semilla, "genes": filas,
             "correlacion_con_pipeline": corr},
            indent=2, ensure_ascii=False), encoding="utf-8")
        print("\nescrito en %s" % a.json)
    return 0


# ---------------------------------------------------------------- T2: el ranking

def peso_por_ventana(g: dict, pesos_ref: dict[str, float],
                     pesos_crit: dict[str, float], excluir: set[str]) -> np.ndarray:
    """Riesgo por ventana: el PEOR acierto de esa ventana, en [0, max(w)*max(c)].

    Dos veces «el peor» y las dos tienen motivo distinto.

    Entre criterios se toma el mas fuerte porque estan anidados por construccion:
    un 21-mero perfecto contiene bloques perfectos de 19, de modo que sumar los tres
    criterios contaria el mismo hecho tres veces.

    Entre referencias tambien se toma el maximo y no la suma, y esta es una decision
    de contenido: una ventana es peligrosa por su peor coincidencia, no por la suma
    de sus coincidencias. Si una ventana pega perfecto en maiz, que ademas pegue en
    *Folsomia candida* no la hace cualitativamente peor —ya hay que sacarla—, y
    sumar haria que seis aciertos leves pesaran como uno grave.
    """
    peor = np.zeros(g["n"])
    for ref, crits in g["riesgo"].items():
        if ref in excluir:
            continue
        w = pesos_ref.get(ref)
        if not w:
            continue
        fuerza = np.zeros(g["n"])
        for crit in reversed(CRITERIOS):          # del mas debil al mas fuerte
            fuerza = np.where(crits[crit], pesos_crit[crit], fuerza)
        peor = np.maximum(peor, w * fuerza)
    return peor


def ejes(g: dict, ini: int, fin: int, pesos_ref, pesos_crit, excluir,
         solo_eficientes: bool) -> dict:
    """Los dos ejes de una region, mas lo que hace falta para la cascada.

    Los dos son tasas sobre las ventanas de la region, y por eso son comparables
    entre candidatos de largo distinto:
      eficacia  fraccion de ventanas eficientes.
      limpieza  fraccion de ventanas limpias, descontando cada ventana sucia en
                proporcion a la gravedad de su peor acierto. Una ventana con
                coincidencia perfecta de 21 nt en la referencia de mayor peso
                descuenta 1 entera; una con un bloque de 19 en la de menor peso
                descuenta una fraccion.
    """
    sl = slice(ini - 1, fin)
    efi = g["eficiente"][sl]
    n_vent = int(g["presente"][sl].sum())
    if n_vent == 0:
        return {"n_ventanas": 0, "eficientes": 0, "eficacia": 0.0, "limpieza": 1.0,
                "exposicion": 0.0, "buenos_limpios": 0, "con_off_target": 0,
                "con_21_perfecto": 0, "vetada": False}

    riesgo = peso_por_ventana(g, pesos_ref, pesos_crit, excluir)[sl]
    if solo_eficientes:
        riesgo = np.where(efi, riesgo, 0.0)       # regla mecanicista (D2)
    activas = [r for r in g["riesgo"] if r not in excluir and pesos_ref.get(r)]
    tope = max((pesos_ref[r] for r in activas), default=0.0) * max(pesos_crit.values())
    exposicion = float(riesgo.sum()) / n_vent / (tope if tope > 0 else 1.0)
    limpieza = 1.0 - exposicion

    # Para la cascada: veto duro y conteo de eficientes limpios, con las mismas
    # definiciones que `pipeline/region_scoring.py` (veto por 21/21 perfecto;
    # limpia = sin riesgo bajo ningun criterio).
    hay21 = np.zeros(g["n"], dtype=bool)
    hayalgo = np.zeros(g["n"], dtype=bool)
    for ref, crits in g["riesgo"].items():
        if ref in excluir:
            continue
        hay21 |= crits["perfecto_21"]
        for crit in CRITERIOS:
            hayalgo |= crits[crit]
    return {"n_ventanas": n_vent, "eficientes": int(efi.sum()),
            "eficacia": float(efi.sum()) / n_vent,
            "limpieza": max(0.0, min(1.0, limpieza)),
            "exposicion": round(exposicion, 6),
            "buenos_limpios": int((efi & ~hayalgo[sl]).sum()),
            "con_off_target": int(hayalgo[sl].sum()),
            "con_21_perfecto": int(hay21[sl].sum()),
            "vetada": bool(hay21[sl].any())}


def normalizar_conjunto(ejes_list: list[dict]) -> list[tuple[float, float]]:
    """Min-max de los dos ejes sobre el conjunto que se esta rankeando.

    Es la convencion de `pipeline/motor.py:valores_normalizados`, con su misma
    advertencia: **depende del conjunto**, asi que agregar o sacar un candidato
    cambia los valores normalizados y puede cambiar el orden. Se incluye porque es
    el antecedente citado y porque es la escala en la que el eje de exposicion tiene
    palanca real; la escala absoluta es la que no depende del conjunto. El reporte
    informa las dos.
    """
    out = []
    for clave in ("eficacia", "limpieza"):
        v = [e[clave] for e in ejes_list]
        lo, hi = min(v), max(v)
        out.append([(x - lo) / (hi - lo) if hi > lo else 1.0 for x in v])
    return list(zip(out[0], out[1]))


def puntaje(e: dict, w_ef: float, forma: str,
            norm: tuple[float, float] | None = None) -> float:
    """Puntaje de un candidato. `norm` trae los dos ejes ya normalizados al conjunto.

    El veto de la cascada resta 1.000: una region vetada queda por debajo de
    cualquier no vetada, y entre vetadas el orden relativo NO es informativo. Quien
    lea el barrido tiene la lista de vetadas aparte, justamente para no leer como
    ranking lo que es un empate en «descartada».
    """
    if forma == "cascada":
        return float(e["buenos_limpios"]) - (1000.0 if e["vetada"] else 0.0)
    ef, li = (norm if norm is not None else (e["eficacia"], e["limpieza"]))
    if forma == "suma":
        return w_ef * ef + (1 - w_ef) * li
    # Piso de 1e-6 como en `motor.py`: con min-max el peor candidato de un eje vale
    # exactamente 0 y el producto se anularia sin dejar ver cuanto le falta.
    return max(ef, 1e-6) ** w_ef * max(li, 1e-6) ** (1 - w_ef)


def excluidas_de(cand: dict, dmaidis_viral: str) -> set[str]:
    """Que referencias no entran al riesgo de este candidato.

    Para los genes del insecto el genoma de *D. maidis* es on-target y sale siempre.
    Para los virales es la asimetria de signo de D5 y la decide el parametro.
    """
    if cand["estrategia"] == "insecto":
        return {DMAIDIS}
    return set() if dmaidis_viral == "off" else {DMAIDIS}


def pesos_base() -> tuple[dict, dict]:
    pr = {k: v["peso"] for k, v in REFERENCIAS.items()}
    pr[DMAIDIS] = DMAIDIS_INFO["peso"]
    return pr, dict(PESO_CRITERIO)


def sortear_pesos(rng) -> tuple[float, dict, dict]:
    """Un juego de pesos del barrido.

    - w_ef uniforme en [0,1], que es Dirichlet(1,1) sobre el simplex de dos ejes.
    - pesos por referencia Dirichlet(1,...,1) sobre el simplex de las seis. El
      genoma de *D. maidis* entra al sorteo y despues lo saca `excluidas_de` segun
      la estrategia del candidato, asi que su peso solo mueve a los genes virales.
    - pesos por criterio Dirichlet(1,1,1) ORDENADO de mayor a menor, porque el
      unico orden que la evidencia sostiene es que un bloque perfecto mas largo no
      es menos riesgoso; las magnitudes quedan libres.
    """
    refs = list(REFERENCIAS) + [DMAIDIS]
    wr = rng.dirichlet(np.ones(len(refs)))
    wc = np.sort(rng.dirichlet(np.ones(3)))[::-1]
    return (float(rng.random()),
            {r: float(w) for r, w in zip(refs, wr)},
            {c: float(w) for c, w in zip(CRITERIOS, wc)})


def ordenar(candidatos: list[dict], genes: dict, w_ef, wr, wc, forma: str,
            solo_eficientes: bool, dmaidis_viral: str,
            escala: str = "absoluta") -> list[tuple[str, float]]:
    es = [ejes(genes[c["gen"]], c["region"][0], c["region"][1], wr, wc,
               excluidas_de(c, dmaidis_viral), solo_eficientes) for c in candidatos]
    norms = normalizar_conjunto(es) if escala == "minmax" else [None] * len(es)
    out = [(c["gen"], puntaje(e, w_ef, forma, nm))
           for c, e, nm in zip(candidatos, es, norms)]
    # Desempate por nombre, no por el orden de entrada: un empate exacto no debe
    # heredar un orden que nadie eligio. Es la convencion de `motor.py:rankear`.
    out.sort(key=lambda kv: (-kv[1], kv[0]))
    return out


def barrer(candidatos, genes, forma, solo_eficientes, dmaidis_viral, muestras, rng,
           escala: str = "absoluta"):
    """Frecuencia de cada candidato en cada posicion sobre el barrido de pesos.

    Lo que se reporta es esta frecuencia y no un orden puntual: con pesos que nadie
    justifico, un orden puntual no dice si el candidato aguanta o si lo puso ahi la
    eleccion de pesos.
    """
    nombres = [c["gen"] for c in candidatos]
    frec = {n: [0] * len(nombres) for n in nombres}
    primeros = {n: 0 for n in nombres}
    ordenes: dict[tuple, int] = {}
    for _ in range(muestras):
        w_ef, wr, wc = sortear_pesos(rng)
        orden = ordenar(candidatos, genes, w_ef, wr, wc, forma, solo_eficientes,
                        dmaidis_viral, escala)
        for i, (n, _s) in enumerate(orden):
            frec[n][i] += 1
        primeros[orden[0][0]] += 1
        clave = tuple(n for n, _ in orden)
        ordenes[clave] = ordenes.get(clave, 0) + 1
    # Las vetadas no se ordenan entre si: se listan. Con los pesos base, porque el
    # veto no depende de los pesos (es un umbral de 21/21 perfecto).
    wr0, wc0 = pesos_base()
    vetadas = [c["gen"] for c in candidatos
               if ejes(genes[c["gen"]], c["region"][0], c["region"][1], wr0, wc0,
                       excluidas_de(c, dmaidis_viral), solo_eficientes)["vetada"]]
    return {"frecuencia": {n: [round(100.0 * v / muestras, 1) for v in frec[n]]
                           for n in nombres},
            "primero_pct": {n: round(100.0 * primeros[n] / muestras, 1)
                            for n in nombres},
            "ordenes": sorted(({"orden": list(k), "pct": round(100.0 * v / muestras, 1)}
                               for k, v in ordenes.items()),
                              key=lambda d: -d["pct"]),
            "vetadas_por_21_perfecto": vetadas,
            "muestras": muestras}


def alternativas(g: dict, largo: int, cand: dict, wr, wc, solo_eficientes: bool,
                 dmaidis_viral: str, w_ef: float, forma: str, tope: int = 3) -> dict:
    """Nivel 2: las regiones alternativas dentro del gen, por el mismo criterio.

    Solo se devuelven regiones que no se pisan mas de la mitad entre si, porque el
    top-k de una ventana deslizante son k desplazamientos de 1 pb de la misma region.
    """
    excluir = excluidas_de(cand, dmaidis_viral)
    n_reg = g["n"] - largo + 1
    puntos = []
    for ini in range(1, n_reg + 1):
        e = ejes(g, ini, ini + largo - 1, wr, wc, excluir, solo_eficientes)
        puntos.append((ini, puntaje(e, w_ef, forma), e))
    ini_c, fin_c = cand["region"]
    p_eleg, e_eleg = next((p, e) for i, p, e in puntos if i == ini_c)
    vivos = ([(i, p, e) for i, p, e in puntos if not e["vetada"]]
             if forma == "cascada" else puntos)
    elegidas = []
    for i, p, e in sorted(vivos, key=lambda t: -t[1]):
        if all(abs(i - j) >= largo * 0.5 for j, _, _ in elegidas):
            elegidas.append((i, p, e))
        if len(elegidas) == tope:
            break
    return {
        "regiones_posibles": n_reg,
        "no_vetadas": sum(1 for _, _, e in puntos if not e["vetada"]),
        "elegida_vetada": bool(e_eleg["vetada"]),
        "percentil_elegida": round(100.0 * sum(1 for _, p, _ in puntos if p <= p_eleg)
                                   / len(puntos), 1),
        "puntaje_elegida": round(p_eleg, 4),
        "mejores": [{"region": "%d-%d" % (i, i + largo - 1), "puntaje": round(p, 4),
                     "eficientes": e["eficientes"], "con_off_target": e["con_off_target"],
                     "con_21_perfecto": e["con_21_perfecto"],
                     "buenos_limpios": e["buenos_limpios"],
                     "eficacia": round(e["eficacia"], 4),
                     "limpieza": round(e["limpieza"], 4)}
                    for i, p, e in elegidas],
    }


# ------------------------------------------- la compuerta de alertas de D48 (ver D69)
#
# `alternativas()` devuelve un orden de regiones; convertir su primer puesto en «la
# region que recomendamos» es un paso aparte, y es **el** paso que esta funcion
# centraliza. Hasta D69 estaba escrito tres veces —una en el nivel 3 de `cmd_ranking` y
# dos en `ranking_v2` (`completar_regiones` y `recomendadas`)— como la misma expresion
# copiada, y ninguna de las tres consultaba la tabla de alertas. O sea que el port podia
# recomendar una region cuya fila de alerta nadie habia leido, que es exactamente el
# default invertido que D48 dejo abierto y que `alertas.exigir_decidida()` existe para
# cerrar.
#
# Lo que esta funcion SI garantiza, desde D72: ninguna de las tres rutas del port
# devuelve una region recomendada sin que la region **este tamizada** y sin que sus filas
# de alerta esten decididas en el umbral vigente. Hasta D71 garantizaba solo la segunda
# mitad, y la primera faltaba: una region que nunca se tamizo no tiene filas, asi que
# `exigir_decidida()` la dejaba pasar como «sin alertas» —no podia distinguir «se miro y
# no hay» de «no se miro»—. Lo protegido eran las doce regiones del inventario de M6 y no
# una propuesta nueva. Desde D72 la compuerta recibe tambien el inventario y una region
# ausente de el levanta `alertas.RegionNoTamizada`.
#
# Lo que sigue sin garantizar: entre el cometido de esta funcion y el numero que aparece
# en un documento de `entregables/` hay una persona copiandolo, y eso ninguna compuerta
# del port lo cubre. Esta en `00_meta/PREGUNTAS_ABIERTAS.md`.

#: Donde vive la tabla de alertas de M6. Es **entrada** de la recomendacion.
TABLA_ALERTAS = (Path(__file__).resolve().parents[2]
                 / "research" / "ola4" / "M6_alertas" / "resultados" / "alertas.tsv")

#: Y el inventario de regiones tamizadas, que es la otra salida del mismo generador y
#: vive al lado de la tabla. Por eso no se configura aparte: `--alertas` mueve las dos, y
#: una tabla sin su inventario al lado es media entrada, no una entrada valida (D72).
NOMBRE_INVENTARIO = "estado_regiones.tsv"

#: Umbral de D28 con el que la compuerta decide que alertas obligan a justificar.
#: `perfecto_21` es D48 literal («cada coincidencia perfecta de 21 nt ... genera una
#: fila»); `perfecto_ge19` es el umbral laxo de D28, sobre el que D48 no se pronuncia.
#: D69 adopta el literal y deja este nombre configurable: lo mueven `--umbral-compuerta`
#: y el parametro `umbral` de `region_recomendada()`, no una edicion del cuerpo.
UMBRAL_COMPUERTA = "perfecto_21"

_ALERTAS_LEIDAS: dict[Path, list[dict]] = {}


def alertas_de(tabla: Path | None = None) -> list[dict]:
    """Las filas de alerta de M6, leidas y validadas una sola vez por ruta.

    Si la tabla no esta en disco **no** se devuelve una lista vacia: una lista vacia
    haria pasar la compuerta a todo, que es el modo de fallar en silencio que D48
    corrige. Falta la tabla, falta la entrada, no hay recomendacion.
    """
    ruta = Path(tabla) if tabla is not None else TABLA_ALERTAS
    if ruta not in _ALERTAS_LEIDAS:
        if not ruta.exists():
            raise FileNotFoundError(
                "no esta la tabla de alertas de M6 (%s) y sin ella no se puede recomendar "
                "ninguna region: D48 pide que cada alerta este decidida antes de usar la "
                "region. Corre research/ola4/M6_alertas/scripts/tabla_alertas.py o pasa "
                "--alertas con la ruta." % ruta)
        _ALERTAS_LEIDAS[ruta] = AL.leer(ruta)
    return _ALERTAS_LEIDAS[ruta]


def inventario_de(tabla: Path | None = None) -> set:
    """Las regiones tamizadas, leidas de `estado_regiones.tsv` al lado de la tabla (D72).

    `AL.leer_inventario()` levanta `FileNotFoundError` si el archivo no esta, y eso es lo
    correcto por el mismo motivo que para la tabla: un inventario vacio haria pasar a
    toda region como tamizada, que es exactamente el default invertido que se cierra.
    """
    ruta = Path(tabla) if tabla is not None else TABLA_ALERTAS
    return AL.leer_inventario(ruta.parent / NOMBRE_INVENTARIO)


def region_recomendada(alt: dict, gen: str, umbral: str | None = None,
                       tabla: Path | None = None) -> tuple[int, int]:
    """El primer puesto de `alternativas()` convertido en recomendacion, con compuerta.

    Levanta `alertas.RegionNoTamizada` si la region no esta en el inventario de M6 (D72)
    y `alertas.AlertaSinDecidir` si alguna fila de alerta de esa region sigue en
    «pendiente» en `umbral`, y en los dos casos **no devuelve region**: no hay forma de
    obtener la recomendacion saltandose el tamizado ni la lectura de la alerta. Una
    region decidida pasa, incluso si la decision es `bloqueante` —bloquear es decidir, y
    el que llama tiene que descartarla: lo dice el estado que devuelve
    `estado_decision()`—.
    """
    region = alt["mejores"][0]["region"]
    AL.exigir_decidida(alertas_de(tabla), gen, region,
                       umbral if umbral is not None else UMBRAL_COMPUERTA,
                       inventario=inventario_de(tabla))
    ini, fin = (int(x) for x in region.split("-"))
    return ini, fin


def cmd_ranking(a) -> int:
    perfil, off = Path(a.perfil), Path(a.offtarget)
    genes = {c["gen"]: cargar_gen(c["gen"], perfil, off, a.mm1) for c in CANDIDATOS}
    wr_base, wc_base = pesos_base()
    rng = np.random.default_rng(a.semilla)

    # Ficha por candidato con los pesos base, bajo las dos reglas de D2.
    fichas = []
    for c in CANDIDATOS:
        g = genes[c["gen"]]
        ini, fin = c["region"]
        excluir = excluidas_de(c, a.dmaidis_viral)
        ficha = dict(c)
        ficha["region"] = "%d-%d" % (ini, fin)
        ficha["largo_region"] = fin - ini + 1
        ficha["eficientes_gen"] = int(g["eficiente"].sum())
        ficha["ventanas_gen"] = int(g["presente"].sum())
        for regla, solo in (("mecanicista", True), ("conservadora", False)):
            e = ejes(g, ini, fin, wr_base, wc_base, excluir, solo)
            ficha[regla] = {k: (round(v, 4) if isinstance(v, float) else v)
                            for k, v in e.items()}
            ficha[regla]["puntaje_geometrico_w05"] = round(puntaje(e, 0.5, "geometrica"), 4)
            ficha[regla]["puntaje_suma_w05"] = round(puntaje(e, 0.5, "suma"), 4)
            ficha[regla]["puntaje_cascada"] = puntaje(e, 0.5, "cascada")
        ficha["riesgo_por_referencia"] = {}
        for ref, crits in g["riesgo"].items():
            if ref in excluir:
                continue
            d = {}
            for crit in CRITERIOS:
                v = crits[crit][ini - 1:fin]
                if v.any():
                    d[crit] = {"ventanas": int(v.sum()),
                               "de_esas_eficientes": int((v & g["eficiente"][ini - 1:fin]).sum())}
            if d:
                ficha["riesgo_por_referencia"][corto(ref)] = d
        fichas.append(ficha)

    print("=== Los dos ejes por candidato (pesos base, regla %s de D2) ===" % a.regla)
    solo = a.regla == "mecanicista"
    print("%-12s%10s%7s%6s%8s%9s%10s%7s%6s" % (
        "gen", "region", "vent", "efic", "eficacia", "exposic", "limpieza",
        "lim+ef", "veto"))
    for f in fichas:
        e = f["mecanicista" if solo else "conservadora"]
        print("%-12s%10s%7d%6d%8.4f%9.4f%10.4f%7d%6s" % (
            f["gen"], f["region"], e["n_ventanas"], e["eficientes"], e["eficacia"],
            e["exposicion"], e["limpieza"], e["buenos_limpios"],
            "si" if e["vetada"] else "no"))

    salida = {"candidatos": fichas,
              "pesos_base_referencia": {corto(k): v for k, v in wr_base.items()},
              "pesos_base_criterio": wc_base,
              "referencias": {v["corto"]: {"accesion": k, "especie": v["especie"],
                                           "rol": v["rol"]}
                              for k, v in list(REFERENCIAS.items())
                              + [(DMAIDIS, DMAIDIS_INFO)]},
              "dmaidis_viral": a.dmaidis_viral}

    # Niveles de ranking: los cuatro juntos, y uno por estrategia (D5).
    conjuntos = {"los_cuatro": CANDIDATOS,
                 "insecto": [c for c in CANDIDATOS if c["estrategia"] == "insecto"],
                 "virus": [c for c in CANDIDATOS if c["estrategia"] == "virus"]}
    salida["barridos"] = {}
    for nombre, conj in conjuntos.items():
        salida["barridos"][nombre] = {}
        for forma in ("geometrica", "suma", "cascada"):
            for regla, s in (("mecanicista", True), ("conservadora", False)):
                for escala in ("absoluta", "minmax"):
                    if forma == "cascada" and escala == "minmax":
                        continue        # la cascada no usa los ejes normalizados
                    r = barrer(conj, genes, forma, s, a.dmaidis_viral, a.muestras,
                               np.random.default_rng(a.semilla), escala)
                    clave = ("%s/%s" % (forma, regla) if forma == "cascada"
                             else "%s/%s/%s" % (forma, regla, escala))
                    salida["barridos"][nombre][clave] = r

    print("\n=== Barrido de pesos: frecuencia por posicion (%d juegos, simplex"
          " completo) ===" % a.muestras)
    for nombre in ("los_cuatro", "insecto", "virus"):
        print("\n-- %s --" % nombre)
        for clave in sorted(salida["barridos"][nombre]):
            r = salida["barridos"][nombre][clave]
            nombres = list(r["frecuencia"])
            print("  %-34s %s" % (clave, "  ".join(
                "%s %s" % (n, "/".join("%.0f" % x for x in r["frecuencia"][n]))
                for n in nombres)))
            for o in r["ordenes"][:3]:
                print("      %5.1f %%  %s" % (o["pct"], " > ".join(o["orden"])))
            if len(r["ordenes"]) > 3:
                print("      (%d ordenes distintos en total)" % len(r["ordenes"]))
            if r["vetadas_por_21_perfecto"]:
                print("      vetadas por 21/21 perfecto (su orden relativo no es "
                      "informativo): %s" % ", ".join(r["vetadas_por_21_perfecto"]))

    # Nivel 2: regiones alternativas dentro de cada gen. Se informan las dos formas
    # que importan: la geometrica, que pondera, y la cascada, que veta. No dan la
    # misma recomendacion y esa diferencia es el contenido de D2.
    print("\n=== Nivel 2: regiones alternativas dentro de cada gen"
          " (pesos base, regla %s, w_ef 0,5) ===" % a.regla)
    salida["alternativas"] = {}
    for c in CANDIDATOS:
        g = genes[c["gen"]]
        largo = c["region"][1] - c["region"][0] + 1
        salida["alternativas"][c["gen"]] = {}
        print("\n  %s  region elegida %s, de %d nt" % (
            c["gen"], "%d-%d" % c["region"], largo))
        for forma in ("geometrica", "cascada"):
            alt = alternativas(g, largo, c, wr_base, wc_base, solo, a.dmaidis_viral,
                               0.5, forma)
            salida["alternativas"][c["gen"]][forma] = alt
            print("    %-10s puntaje de la elegida %9.4f   percentil %5.1f de %d"
                  " regiones%s" % (
                      forma, alt["puntaje_elegida"], alt["percentil_elegida"],
                      alt["regiones_posibles"],
                      "   (VETADA)" if alt["elegida_vetada"] else ""))
            print("      %-12s%9s%7s%9s%9s%9s" % (
                "mejores", "puntaje", "efic", "con off", "21/21", "lim+ef"))
            for m in alt["mejores"]:
                print("      %-12s%9.4f%7d%9d%9d%9d" % (
                    m["region"], m["puntaje"], m["eficientes"], m["con_off_target"],
                    m["con_21_perfecto"], m["buenos_limpios"]))
            if forma == "cascada":
                print("      regiones que escapan al veto: %d de %d"
                      % (alt["no_vetadas"], alt["regiones_posibles"]))

    # Nivel 3: el mismo ranking pero con las regiones recomendadas en lugar de las
    # que eligio EPILAB. Contesta si la recomendacion cambia el orden, que no es
    # obvio: mover una region cambia los dos ejes a la vez y no por igual en todos
    # los genes. El nivel 1 sigue siendo el que el investigador pidio —los cuatro
    # candidatos tal como estan—; esto es lo que pasaria si acepta moverlos.
    # La compuerta de D48 esta en `region_recomendada()`: si una fila de alerta de la
    # region que gana sigue en «pendiente», esto levanta y el nivel 3 no se produce.
    recomendados = []
    for c in CANDIDATOS:
        d = dict(c)
        d["region"] = region_recomendada(salida["alternativas"][c["gen"]]["cascada"],
                                         c["gen"], a.umbral_compuerta, a.alertas)
        recomendados.append(d)
    salida["regiones_recomendadas"] = {
        c["gen"]: {"elegida": "%d-%d" % dict(o)["region"],
                   "recomendada": "%d-%d" % c["region"]}
        for c, o in zip(recomendados, CANDIDATOS)}
    salida["barridos"]["los_cuatro_recomendados"] = {}
    for forma in ("geometrica", "suma", "cascada"):
        for regla, s in (("mecanicista", True), ("conservadora", False)):
            for escala in ("absoluta", "minmax"):
                if forma == "cascada" and escala == "minmax":
                    continue
                r2 = barrer(recomendados, genes, forma, s, a.dmaidis_viral, a.muestras,
                            np.random.default_rng(a.semilla), escala)
                clave = ("%s/%s" % (forma, regla) if forma == "cascada"
                         else "%s/%s/%s" % (forma, regla, escala))
                salida["barridos"]["los_cuatro_recomendados"][clave] = r2

    print("\n=== Nivel 3: el mismo ranking con las regiones recomendadas ===")
    for c, o in zip(recomendados, CANDIDATOS):
        print("  %-12s %s  ->  %s" % (c["gen"], "%d-%d" % o["region"],
                                      "%d-%d" % c["region"]))
    print()
    for clave in sorted(salida["barridos"]["los_cuatro_recomendados"]):
        r2 = salida["barridos"]["los_cuatro_recomendados"][clave]
        print("  %-34s %s" % (clave, "  ".join(
            "%s %s" % (n2, "/".join("%.0f" % x for x in v))
            for n2, v in r2["frecuencia"].items())))
        for o2 in r2["ordenes"][:2]:
            print("      %5.1f %%  %s" % (o2["pct"], " > ".join(o2["orden"])))
        if r2["vetadas_por_21_perfecto"]:
            print("      vetadas: %s" % ", ".join(r2["vetadas_por_21_perfecto"]))

    if a.json:
        Path(a.json).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json).write_text(json.dumps(salida, indent=2, ensure_ascii=False),
                                encoding="utf-8")
        print("\nescrito en %s" % a.json)
    return 0


# ----------------------------------------------------------------------- interfaz

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    n = sub.add_parser("nulo", help="T1: percentil de la region elegida y dos nulos")
    n.add_argument("--dir", default="work/sifi_check")
    n.add_argument("--perfil", default="work/sifi_check/salida")
    n.add_argument("--reps", type=int, default=2000)
    n.add_argument("--semilla", type=int, default=7)
    n.add_argument("--correlacion", action="store_true",
                   help="ademas, correlacionar el puntaje biofisico del pipeline con"
                        " la densidad de eficientes sobre las mismas regiones")
    n.add_argument("--raiz", default=".",
                   help="raiz del repositorio, para importar pipeline/")
    n.add_argument("--json", default=None)
    n.set_defaults(func=cmd_nulo)

    r = sub.add_parser("ranking", help="T2: el ranking y el barrido de pesos")
    r.add_argument("--dir", default="work/sifi_check")
    r.add_argument("--perfil", default="work/sifi_check/salida")
    r.add_argument("--offtarget",
                   default="work/sifi_check/offtarget_full/offtarget_por_sirna.tsv")
    r.add_argument("--mm1", default=None,
                   help="patron con {gen}, p.ej. work/sifi_check/offtarget_mm1_{gen}/"
                        "offtarget_por_sirna.tsv")
    r.add_argument("--forma", choices=("geometrica", "suma", "cascada"),
                   default="geometrica")
    r.add_argument("--regla", choices=("mecanicista", "conservadora"),
                   default="conservadora")
    r.add_argument("--dmaidis-viral", choices=("off", "neutro"), default="off",
                   dest="dmaidis_viral",
                   help="si el genoma de D. maidis cuenta como off-target para los "
                        "genes virales (D5)")
    r.add_argument("--muestras", type=int, default=2000)
    r.add_argument("--semilla", type=int, default=7)
    r.add_argument("--alertas", default=None, type=Path,
                   help="tabla de alertas de M6 que consulta la compuerta de D48, con su "
                        "estado_regiones.tsv al lado, que es el inventario de regiones "
                        "tamizadas que la compuerta exige desde D72; por "
                        "defecto %s" % TABLA_ALERTAS)
    r.add_argument("--umbral-compuerta", dest="umbral_compuerta",
                   choices=("perfecto_21", "perfecto_ge19"), default=UMBRAL_COMPUERTA,
                   help="umbral de D28 con el que la compuerta exige decision; por "
                        "defecto %s, que es D48 literal (D69)" % UMBRAL_COMPUERTA)
    r.set_defaults(func=cmd_ranking)

    a = ap.parse_args(argv)
    return a.func(a)


if __name__ == "__main__":
    sys.exit(main())

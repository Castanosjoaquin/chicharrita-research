"""O4 — el enumerador de quimeras: dos genes, un largo total y un objetivo declarado.

**El criterio no lo elige este script: lo fija `PREREGISTRO.md`, escrito y commiteado antes
de enumerar, con la enmienda de su §10.** Si alguna pieza de aca no coincide con el
preregistro, el preregistro manda y esto es un error a corregir.

Que hace. Pasale dos genes y un largo total y devuelve **todas** las combinaciones de la
grilla, cada una con sus tres cuentas separadas, ordenadas bajo el objetivo que vos declares.
No devuelve «la mejor quimera»: `D67` decidio que una quimera no se evalua por densidad de
ventanas eficientes, asi que «mejor» no es una opcion disponible y hay que decir mejor para
que.

**El objetivo es obligatorio y no tiene default** (§2 del preregistro), igual que el
parametro `inventario` de la compuerta desde `D72` y por el mismo motivo: un default se
adopta olvidandolo. Los tres valores, con lo que ordena cada uno:

- `cobertura_fenotipica` — el de `D67`. Exige que los dos genes traigan **eje de fenotipo
  declarado y distinto**, con la fila del catalogo de `C5` que lo respalda. Ordena por el eje
  de riesgo —primero las combinaciones cuyo empalme no fabrica ningun bloque— y usa las
  ventanas heredadas eficientes como **desempate**, no como puntaje.
- `riesgo_minimo` — ordena solo por lo que fabrica el empalme. No mira eficiencia.
- `eficiencia_heredada` — ordena por ventanas heredadas eficientes y por nada mas. Es el que
  el issue #24 pide **no vender**, y existe para poder medir cuanto se pierde al no usarlo.
  Toda salida bajo este objetivo lleva al lado que el criterio de eficiencia de si-Fi21 **no
  esta validado** en hemipteros: rho = +0,142, IC95 [-0,247, +0,492], n = 29 `[M]`.

La grilla (§3). Para dos genes y un largo total `L` los parametros libres son tres —el
arranque y el largo del fragmento izquierdo, y el arranque del derecho, con
`l2 = L - l1`— mas el **orden**, que es discreto con dos valores y entra porque esta medido
que cambia el resultado (`C13`: +3 y -3; `O3`: 41 contra 40, y solo un orden fabrica riesgo).
Eso es una grilla y se enumera: **no hay metaheuristica, no hay muestreo y no hay
optimizador** (`W2` §4). El paso engruesa la grilla y se declara en la salida.

El orden de poda (§4): **el riesgo primero** (`D70`, `D74`). La mascara de veto por gen sale
de `mascara.py` y se calcula una vez por gen, porque el estado de off-target de una ventana
depende solo de sus 21 nt (`C13` §6). Lo que **no** se hereda es lo que fabrica el empalme, y
eso se tamiza por candidato en una sola pasada sobre el panel.

Las unidades (§10). La grilla enumera en **marco 2** —el `--largo-total` son nucleotidos,
porque es lo que se sintetiza— y cada candidato reporta tambien su lectura de **marco 1**,
con los nombres de `D63`. El eje de riesgo tambien se lee en marco 2, que es una desviacion
declarada respecto de `ranking.ejes()`: ver `PREGUNTAS_ABIERTAS.md` 46.

Lo que este script **no** hace: no recomienda ninguna quimera, no afirma eficacia y no emite
la fila completa del inventario de `M6` para una juntura —esa la produce
`research/ola6/O3_quimera_bicc_vatpase_b/scripts/03_alerta_d48.py`, que ya resuelve las
anotaciones de cada acierto, y duplicarla aca seria reimplementarla—. Sobre el inventario:
`D78` ya le dio a la juntura una clave propia, `(quimera <nombre>, "juntura")`, pero esa
decision **no esta implementada** por falta de insumo, asi que una quimera todavia puede
pasar la compuerta con su empalme sin tamizar (`PREGUNTAS_ABIERTAS.md` 41). La salida
declara la clave que le corresponde en vez de dar el hueco por cerrado.

Uso:
    python research/ola6/O4_enumerador_quimeras/scripts/enumerar_quimeras.py \\
        --gen BicC_Dm=work/O3/fasta/BicC_Dm_full.fasta \\
        --gen VATPaseB_Dm=work/O3/fasta/VATPaseB_Dm_full.fasta \\
        --eje BicC_Dm=reproduccion:C5/DM-01 \\
        --eje VATPaseB_Dm=movilidad:C5/DM-02 \\
        --largo-total 600 --objetivo cobertura_fenotipica
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import sys
from pathlib import Path

import ahocorasick

RAIZ = Path(__file__).resolve().parents[4]
BLOQUE = Path(__file__).resolve().parents[1]
RESULTADOS = BLOQUE / "resultados"

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(RAIZ / "tools/sifi21_port"))
import mascara as MA            # noqa: E402  la mascara de veto de esta misma linea
import ranking as R             # noqa: E402  solo para los nombres cortos del panel
import offtarget_21nt as OT     # noqa: E402  el tamizador, sin tocarlo
from sifi_core import DEFAULTS, SifiEngine  # noqa: E402  el motor, sin tocarlo

VENTANA = 21
MODO, BACKEND, TEMP, TABLA_NN = "corregido", "vienna", 22.0, "NN3"
#: Largos de bloque que se buscan en el empalme, de mayor a menor. El piso de 19 es el de
#: `D28`, que al fijarlo declaro que a ese largo la convencion del campo no tiene
#: experimento detras.
LARGOS_BLOQUE = (VENTANA, VENTANA - 1, VENTANA - 2)
OBJETIVOS = ("cobertura_fenotipica", "riesgo_minimo", "eficiencia_heredada")
#: La advertencia que viaja con `eficiencia_heredada`. Es `[M]` de `W8`.
SIN_VALIDAR = ("el criterio de eficiencia de si-Fi21 no esta validado en hemipteros: "
               "rho = +0,142, IC95 [-0,247, +0,492], n = 29")
#: Las bases del panel. La humana vive aparte y el nombre del archivo es el identificador.
DBS = sorted((RAIZ / "work/offtarget_db").glob("*.fna.gz")) + \
      [RAIZ / "work/W5/ref/humano_rna.fna.gz"]


def hash_corto(seq: str) -> str:
    """Doce caracteres del sha256. Identifica una molecula sin escribir una sola base."""
    return hashlib.sha256(seq.encode()).hexdigest()[:12]


def leer_gen(spec: str) -> dict:
    """`NOMBRE=ruta[:a-b]`: el gen entero, con el tramo donde se permite buscar."""
    if "=" not in spec:
        raise SystemExit("--gen pide NOMBRE=ruta[:a-b], llego '%s'" % spec)
    nombre, resto = spec.split("=", 1)
    ruta, _, tramo = resto.partition(":")
    p = Path(ruta) if Path(ruta).is_absolute() else RAIZ / ruta
    if not p.exists():
        raise SystemExit("%s: no esta %s" % (nombre, p))
    consulta, seq = MA.leer_fasta_simple(p)
    desde, hasta = 1, len(seq)
    if tramo:
        if "-" not in tramo:
            raise SystemExit("%s: el tramo pide a-b, llego '%s'" % (nombre, tramo))
        desde, hasta = (int(x) for x in tramo.split("-", 1))
        if not 1 <= desde <= hasta <= len(seq):
            raise SystemExit("%s: el tramo %d-%d no cabe en %d nt"
                             % (nombre, desde, hasta, len(seq)))
    return {"nombre": nombre, "consulta": consulta, "seq": seq, "n": len(seq),
            "desde": desde, "hasta": hasta, "ruta": str(p.relative_to(RAIZ))}


def leer_eje(spec: str) -> tuple[str, dict]:
    """`NOMBRE=eje[:fuente]`. El eje es entrada declarada, nunca inferida (§2)."""
    if "=" not in spec:
        raise SystemExit("--eje pide NOMBRE=eje[:fuente], llego '%s'" % spec)
    nombre, resto = spec.split("=", 1)
    eje, _, fuente = resto.partition(":")
    if not eje:
        raise SystemExit("%s: el eje no puede estar vacio" % nombre)
    return nombre, {"eje": eje, "fuente": fuente or "sin fuente declarada"}


def enumerar(genes: dict, mascaras: dict, largo_total: int, l1_min: int, l1_max: int,
             paso: int) -> tuple[list[dict], dict]:
    """La grilla completa, en marco 2 y con el riesgo ya podado. Sin plegar nada todavia."""
    nombres = list(genes)
    candidatos, bruto = [], 0
    for izq, der in itertools.permutations(nombres, 2):
        for l1 in range(l1_min, l1_max + 1, paso):
            l2 = largo_total - l1
            if l2 < VENTANA:
                continue
            gi, gd = genes[izq], genes[der]
            bruto += (max(0, min(gi["hasta"], gi["n"]) - l1 + 1 - gi["desde"] + 1)
                      * max(0, min(gd["hasta"], gd["n"]) - l2 + 1 - gd["desde"] + 1))
            a1s = MA.fragmentos_admisibles(mascaras[izq], l1, paso,
                                           desde=gi["desde"], hasta=gi["hasta"], marco=2)
            a2s = MA.fragmentos_admisibles(mascaras[der], l2, paso,
                                           desde=gd["desde"], hasta=gd["hasta"], marco=2)
            for a1, a2 in itertools.product(a1s, a2s):
                candidatos.append({"izq": izq, "der": der, "a1": a1, "l1": l1,
                                   "a2": a2, "l2": l2})
    cuentas = {"combinaciones_antes_de_podar": bruto,
               "combinaciones_admisibles": len(candidatos),
               "paso": paso, "l1_min": l1_min, "l1_max": l1_max,
               "largo_total": largo_total, "marco_de_la_grilla": 2}
    return candidatos, cuentas


def perfil(seq: str) -> dict[int, bool]:
    """Veredicto por ventana, con el motor en proceso y la configuracion de §6.

    Un motor por secuencia, como hace `run_sifi.py`: `SifiEngine.track` acumula y
    compartirlo entre candidatos mezclaria el registro de tablas consultadas.
    """
    eng = SifiEngine(mode=MODO, temp_c=TEMP, tabla_nn=TABLA_NN, **dict(DEFAULTS))
    ventanas, _ = eng.run(seq, backend=BACKEND)
    return {w.pos: w.is_efficient for w in ventanas}


def bloques_que_cruzan(mero: str) -> list[tuple[int, int]]:
    """Los `(offset, largo)` de los bloques del 40-mero que **cruzan** la union.

    La definicion es la del paso 2 de `O3`, que a su vez es la de `empalme_maiz_detalle.py`
    de `C13`: **fabricado es el bloque que toma al menos un nucleotido de cada uno de los
    dos genes**. Un bloque de 19 nt que entra entero en el aporte de un solo gen no lo
    fabrica el empalme: ya existia en ese gen y la quimera lo hereda. En un 40-mero —veinte
    nucleotidos de cola y veinte de cabeza— eso da 20 bloques de 21 nt, 19 de 20 y 18 de
    19: **57** por juntura.
    """
    salida = []
    for largo in LARGOS_BLOQUE:
        for s in range(0, len(mero) - largo + 1):
            if s + 1 <= 20 < s + largo:      # arranca en la cola y termina en la cabeza
                salida.append((s, largo))
    return salida


def tamizar_junturas(candidatos: list[dict], genes: dict) -> dict:
    """Los bloques que **fabrica** cada empalme, en una sola pasada sobre el panel.

    Dos cosas que no hace el tamizado de ventanas de `offtarget_21nt.py`, y por las que
    este paso existe: ese tamizado dice si una ventana tiene un bloque de 19 nt o mas en
    una referencia, pero **no dice cual bloque ni donde cae**, asi que no puede distinguir
    un bloque fabricado por la union de uno que la quimera hereda de un gen. Aca el
    automata se arma con los bloques que cruzan la union y con nada mas, de modo que todo
    acierto es, por construccion, fabricado.

    Las junturas se deduplican por su 40-mero: muchas combinaciones comparten empalme,
    porque depende solo del final del fragmento izquierdo y del arranque del derecho.

    Limitacion declarada, la misma que declaro el paso 2 de `O3`: busca coincidencia
    **exacta** en las dos hebras y **no localiza** los aciertos con un desajuste
    (`mm1_21`), porque un desajuste no tiene bloque contiguo que localizar. El criterio
    `mm1_21` queda fuera de esta cuenta, y eso es una desviacion del §4 del preregistro.
    """
    por_40mero: dict[str, list[int]] = {}
    for i, c in enumerate(candidatos):
        izq, der = genes[c["izq"]]["seq"], genes[c["der"]]["seq"]
        cola = izq[c["a1"] + c["l1"] - VENTANA:c["a1"] + c["l1"] - 1]
        cabeza = der[c["a2"] - 1:c["a2"] + VENTANA - 2]
        if len(cola) != VENTANA - 1 or len(cabeza) != VENTANA - 1:
            raise SystemExit("la juntura de %s no tiene 20+20 nt" % c)
        por_40mero.setdefault(cola + cabeza, []).append(i)
    claves = sorted(por_40mero)
    print("junturas distintas: %d sobre %d combinaciones" % (len(claves), len(candidatos)))

    aut = ahocorasick.Automaton()
    n_pat = 0
    for j, mero in enumerate(claves):
        for s, largo in bloques_que_cruzan(mero):
            bloque = mero[s:s + largo]
            if any(b not in "ACGT" for b in bloque):
                continue
            for patron in (bloque, OT.rc(bloque)):
                carga = (j, s, largo)
                if aut.exists(patron):
                    aut.get(patron).append(carga)
                else:
                    aut.add_word(patron, [carga])
                    n_pat += 1
    aut.make_automaton()
    print("automata: %d patrones de bloque que cruzan la union" % n_pat)

    # (juntura, offset, largo) -> referencias en las que cae
    golpes: dict[tuple[int, int, int], set[str]] = {}
    for db in DBS:
        if not db.exists():
            raise SystemExit("falta la base %s" % db)
        base = db.name.split(".fna")[0]
        for _, seq in OT.iter_db(db):
            if not seq:
                continue
            for _, cargas in aut.iter(seq):
                for carga in cargas:
                    golpes.setdefault(carga, set()).add(base)
        print("  escaneada %s" % base, flush=True)

    salida: dict[int, dict] = {}
    for (j, s, largo), refs in golpes.items():
        # Cuanto aporta cada gen a este bloque. Importa leerlo: un bloque de 19 nt que
        # toma 18 de un gen y 1 del otro es casi el gen solo, y **tiene una chance de uno
        # en cuatro de existir en cualquier referencia que contenga al gen padre**, porque
        # basta con que el nucleotido siguiente del padre coincida. Un bloque repartido
        # 10/9 es otra cosa. `D74` reporto justamente el aporte: 18 y 1.
        izq_nt = VENTANA - 1 - s
        aporte = min(izq_nt, largo - izq_nt)
        # El aporte se registra **solo** para los bloques que coinciden en alguna
        # referencia del panel. Un bloque que coincide unicamente en el genoma del vector
        # no es riesgo: es el blanco, porque los dos genes son del insecto. Mezclarlo
        # dejaba filas con `alerta_juntura_nueva = no` y un aporte alto al lado, que es
        # pedirle al lector que distinga on-target de off-target comparando columnas.
        del_panel = bool(refs - {R.DMAIDIS})
        for i in por_40mero[claves[j]]:
            d = salida.setdefault(i, {"por_largo": {}, "ventanas": set(), "aportes": []})
            d["por_largo"].setdefault(largo, set()).update(refs)
            if del_panel:
                d["aportes"].append(aporte)
            # Ventanas de juntura (1 a 20) que contienen enteramente a este bloque.
            for j_vent in range(1, VENTANA):
                if j_vent - 1 <= s and s + largo <= j_vent - 1 + VENTANA:
                    d["ventanas"].add(j_vent)
    return salida


def cuentas_de(c: dict, genes: dict, perf_q: dict, perf_izq: dict, perf_der: dict,
               juntura: dict | None) -> dict:
    """Las tres cuentas de `D67`, separadas, y **nunca** sumadas en una sola cifra."""
    corte, L = c["l1"], c["l1"] + c["l2"]
    her_izq = [p for p in perf_q if p <= corte - VENTANA + 1]
    empalme = [p for p in perf_q if corte - VENTANA + 1 < p <= corte]
    her_der = [p for p in perf_q if p > corte]

    flips_izq = [p for p in her_izq if perf_q[p] != perf_izq.get(p)]
    flips_der = [p for p in her_der if perf_q[p] != perf_der.get(p - corte)]
    dist = [corte - 20 - p for p in flips_izq] + [p - corte - 1 for p in flips_der]

    # Cuantas ventanas de juntura tienen blanco continuo de 21 nt en alguno de los dos
    # genes, en cualquiera de las dos hebras (metodo de `N4`). La union es secuencia que
    # fabrica el ensamblado, asi que lo normal es cero: si alguna aparece, es que el
    # 21-mero existe igual en un gen y entonces esa ventana si silencia algo.
    qseq = (genes[c["izq"]]["seq"][c["a1"] - 1:c["a1"] + c["l1"] - 1]
            + genes[c["der"]]["seq"][c["a2"] - 1:c["a2"] + c["l2"] - 1])
    con_blanco = 0
    for p in empalme:
        mero = qseq[p - 1:p + VENTANA - 1]
        if any(mero in g["seq"] or OT.rc(mero) in g["seq"] for g in genes.values()):
            con_blanco += 1

    jj = juntura or {"por_largo": {}, "ventanas": set(), "aportes": []}
    # El genoma del vector es on-target de los dos genes del insecto: un acierto ahi no es
    # riesgo, es el blanco, y se informa aparte para no contarlo como off-target.
    vector = {R.DMAIDIS}
    fab21 = jj["por_largo"].get(VENTANA, set()) - vector
    fab_ge19 = set().union(*(jj["por_largo"].get(k, set())
                             for k in (VENTANA - 1, VENTANA - 2))) - vector \
        if jj["por_largo"] else set()
    en_vector = any(vector & refs for refs in jj["por_largo"].values())
    ef_juntura = [p for p in empalme if perf_q[p]]
    ventanas_con_bloque = jj["ventanas"]
    return {
        "ventanas_molecula": len(perf_q),
        "ventanas_marco1_del_fragmento_izq": c["l1"],
        "ventanas_marco1_del_fragmento_der": c["l2"],
        # La comparacion contra las regiones sueltas, que es lo que pide el issue #24. La
        # suma de las partes **no** es la cifra de la quimera: es la referencia contra la
        # que se la compara, y por eso viaja en su propia columna.
        "ef_fragmento_izq_solo": sum(perf_izq.values()),
        "ef_fragmento_der_solo": sum(perf_der.values()),
        "suma_de_las_partes": sum(perf_izq.values()) + sum(perf_der.values()),
        "delta_heredadas_menos_suma": (sum(1 for p in her_izq + her_der if perf_q[p])
                                       - sum(perf_izq.values()) - sum(perf_der.values())),
        "ef_heredadas_izq": sum(1 for p in her_izq if perf_q[p]),
        "ef_heredadas_der": sum(1 for p in her_der if perf_q[p]),
        "ef_heredadas": sum(1 for p in her_izq + her_der if perf_q[p]),
        "heredadas_que_cambiaron": len(flips_izq) + len(flips_der),
        "max_nt_hasta_la_union_de_un_cambio": max(dist) if dist else "",
        "ventanas_juntura": len(empalme),
        "ef_juntura": len(ef_juntura),
        "juntura_con_blanco_continuo": con_blanco,
        "fabricados_21_refs": len(fab21),
        "fabricados_ge19_refs": len(fab_ge19),
        "fabricados_refs": ",".join(sorted(R.corto(r) for r in fab21 | fab_ge19)),
        # Cuanto aporta el gen menos representado en el bloque fabricado mas repartido, y
        # cuantos bloques estan repartidos de verdad. Un bloque con aporte 1 es el gen
        # solo mas un nucleotido: existe por azar en una de cada cuatro referencias que
        # contengan al padre, asi que no se lee igual que uno repartido.
        "aporte_del_bloque_mas_repartido": max(jj['aportes']) if jj['aportes'] else 0,
        "bloques_fabricados_con_aporte_ge5": sum(1 for x in jj["aportes"] if x >= 5),
        # La ventana de juntura que arranca en `p` es la numero `p - (corte - 20)` del
        # 40-mero, porque su primer nucleotido es el `corte - 19` de la quimera.
        "fabricados_en_ventana_eficiente": sum(
            1 for p in ef_juntura if (p - (corte - VENTANA + 1)) in ventanas_con_bloque),
        "existe_en_el_genoma_del_vector": "si" if en_vector else "no",
        "alerta_juntura_nueva": "si" if fab21 | fab_ge19 else "no",
    }


def clave_de_orden(objetivo: str, f: dict):
    """El orden de cada objetivo, explicito. No existe un objetivo que los combine."""
    riesgo = (f["fabricados_21_refs"], f["fabricados_ge19_refs"])
    coords = (f["izquierda"], f["derecha"], f["a1"], f["l1"], f["a2"])
    if objetivo == "cobertura_fenotipica":
        return (*riesgo, -f["ef_heredadas"], *coords)
    if objetivo == "riesgo_minimo":
        return (*riesgo, *coords)
    return (-f["ef_heredadas"], *coords)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gen", action="append", default=[], metavar="NOMBRE=ruta[:a-b]",
                    help="se repite por gen; hacen falta exactamente dos")
    ap.add_argument("--eje", action="append", default=[], metavar="NOMBRE=eje[:fuente]",
                    help="eje de fenotipo declarado, con su fila del catalogo de C5")
    ap.add_argument("--largo-total", type=int, required=True, dest="largo_total")
    ap.add_argument("--objetivo", choices=OBJETIVOS, required=True,
                    help="obligatorio y sin default (§2 del preregistro)")
    ap.add_argument("--paso", type=int, default=10)
    ap.add_argument("--l1-min", type=int, default=None, dest="l1_min")
    ap.add_argument("--l1-max", type=int, default=None, dest="l1_max")
    ap.add_argument("--tope-plegados", type=int, default=5000, dest="tope")
    ap.add_argument("--nombre", default="o4")
    ap.add_argument("--resultados", default=None, type=Path)
    a = ap.parse_args(argv)

    if len(a.gen) != 2:
        raise SystemExit("hacen falta exactamente dos --gen y llegaron %d" % len(a.gen))
    genes = {}
    for spec in a.gen:
        g = leer_gen(spec)
        if g["nombre"] in genes:
            raise SystemExit("%s aparece dos veces" % g["nombre"])
        genes[g["nombre"]] = g
    ejes = dict(leer_eje(s) for s in a.eje)
    L = a.largo_total
    l1_min = a.l1_min if a.l1_min is not None else 100
    l1_max = a.l1_max if a.l1_max is not None else L - 100
    if l1_min > l1_max:
        raise SystemExit("--l1-min %d es mayor que --l1-max %d" % (l1_min, l1_max))

    if a.objetivo == "cobertura_fenotipica":
        faltan = [n for n in genes if n not in ejes]
        if faltan:
            raise SystemExit(
                "el objetivo cobertura_fenotipica exige eje de fenotipo declarado para los "
                "dos genes y falta el de %s. Un gen sin fila en el catalogo de C5 entra "
                "como sin_fenotipo_publicado y no puede correr bajo este objetivo (§2)."
                % ", ".join(faltan))
        if len({e["eje"] for e in ejes.values()}) < 2:
            raise SystemExit(
                "el objetivo cobertura_fenotipica exige ejes **distintos** (D67) y los dos "
                "genes declaran '%s'" % next(iter(ejes.values()))["eje"])

    print("objetivo declarado: %s" % a.objetivo)
    if a.objetivo == "eficiencia_heredada":
        print("  AVISO que viaja con este objetivo: %s" % SIN_VALIDAR)
    for n, g in genes.items():
        print("  %-14s %5d nt  tramo %d-%d  eje %s"
              % (n, g["n"], g["desde"], g["hasta"],
                 ejes.get(n, {"eje": "sin_fenotipo_publicado"})["eje"]))

    mascaras = {}
    for n, g in genes.items():
        v, det = MA.mascara_de(g["consulta"], g["n"] - VENTANA + 1)
        mascaras[n] = v
        print("  mascara %-14s %d ventanas, %d vetadas, %s"
              % (n, len(v), det["vetadas"], det["por_referencia"] or "sin aciertos"))

    candidatos, cuentas = enumerar(genes, mascaras, L, l1_min, l1_max, a.paso)
    print("\ngrilla: %d combinaciones antes de podar, %d admisibles en marco 2"
          % (cuentas["combinaciones_antes_de_podar"], cuentas["combinaciones_admisibles"]))
    if not candidatos:
        raise SystemExit("ninguna combinacion admisible: el veto poda la grilla entera")
    fragmentos = {(c["izq"], c["a1"], c["l1"]) for c in candidatos} | \
                 {(c["der"], c["a2"], c["l2"]) for c in candidatos}
    plegados = len(candidatos) + len(fragmentos)
    print("plegados que hacen falta: %d combinaciones + %d fragmentos = %d"
          % (len(candidatos), len(fragmentos), plegados))
    if plegados > a.tope:
        # El paso que alcanzaria se **mide**, no se extrapola: enumerar es indices y no
        # cuesta nada, y la relacion entre paso y plegados no es la que uno estima a ojo
        # —doblar el paso no divide por cuatro, porque la poda de riesgo no es uniforme a
        # lo largo del gen—.
        sugerencias = []
        for p in (a.paso * 2, a.paso * 5, a.paso * 10):
            cs, _ = enumerar(genes, mascaras, L, l1_min, l1_max, p)
            fr = {(c["izq"], c["a1"], c["l1"]) for c in cs} | \
                 {(c["der"], c["a2"], c["l2"]) for c in cs}
            sugerencias.append((p, len(cs) + len(fr)))
        cabe = [p for p, n in sugerencias if n <= a.tope]
        raise SystemExit(
            "la grilla pide %d plegados y el tope declarado es %d. La corrida se detiene y "
            "no muestrea ni cambia de algoritmo (§3). Medido para esta grilla: %s. %s"
            % (plegados, a.tope,
               "; ".join("--paso %d pide %d" % s for s in sugerencias),
               ("El paso mas fino que entra en el tope es %d." % min(cabe)) if cabe else
               "Ninguno de esos pasos entra en el tope: subi --tope-plegados a conciencia."))

    perf_frag = {}
    for k, (gen, ini, largo) in enumerate(sorted(fragmentos), 1):
        perf_frag[(gen, ini, largo)] = perfil(
            genes[gen]["seq"][ini - 1:ini + largo - 1])
        if k % 50 == 0 or k == len(fragmentos):
            print("  fragmentos plegados %d/%d" % (k, len(fragmentos)), flush=True)

    junturas = tamizar_junturas(candidatos, genes)

    filas = []
    for i, c in enumerate(candidatos):
        qseq = (genes[c["izq"]]["seq"][c["a1"] - 1:c["a1"] + c["l1"] - 1]
                + genes[c["der"]]["seq"][c["a2"] - 1:c["a2"] + c["l2"] - 1])
        f = {"objetivo": a.objetivo,
             "quimera": "Q_%s_%d-%d__%s_%d-%d" % (
                 c["izq"], c["a1"], c["a1"] + c["l1"] - 1,
                 c["der"], c["a2"], c["a2"] + c["l2"] - 1),
             "izquierda": c["izq"], "derecha": c["der"],
             "a1": c["a1"], "l1": c["l1"], "a2": c["a2"], "l2": c["l2"],
             "largo_total_nt": L, "hash12": hash_corto(qseq),
             "eje_izq": ejes.get(c["izq"], {"eje": "sin_fenotipo_publicado"})["eje"],
             "eje_der": ejes.get(c["der"], {"eje": "sin_fenotipo_publicado"})["eje"]}
        f.update(cuentas_de(c, genes, perfil(qseq),
                            perf_frag[(c["izq"], c["a1"], c["l1"])],
                            perf_frag[(c["der"], c["a2"], c["l2"])],
                            junturas.get(i)))
        filas.append(f)
        if (i + 1) % 50 == 0 or i + 1 == len(candidatos):
            print("  combinaciones plegadas %d/%d" % (i + 1, len(candidatos)), flush=True)

    filas.sort(key=lambda f: clave_de_orden(a.objetivo, f))
    res = a.resultados or RESULTADOS
    res.mkdir(parents=True, exist_ok=True)
    suf = "%s_%s_%s" % (a.nombre, MODO, BACKEND)
    with (res / ("quimeras_enumeradas_%s.tsv" % suf)).open(
            "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()), delimiter="\t")
        w.writeheader(); w.writerows(filas)
    (res / ("quimeras_enumeradas_%s.json" % suf)).write_text(json.dumps({
        "objetivo": a.objetivo, "advertencia": SIN_VALIDAR,
        "genes": {n: {k: g[k] for k in ("ruta", "n", "desde", "hasta")}
                  for n, g in genes.items()},
        "ejes_declarados": ejes, "grilla": cuentas, "plegados": plegados,
        "tamizado_de_juntura": {
            "que_se_busca": "bloques de 19, 20 y 21 nt que cruzan la union, exactos y en "
                            "las dos hebras; fabricado es el bloque que toma al menos un "
                            "nucleotido de cada gen (paso 2 de O3, C13)",
            "bloques_por_juntura": 57,
            "mm1_21": "fuera de esta cuenta: un desajuste no tiene bloque contiguo que "
                      "localizar. Es desviacion declarada del §4 del preregistro"},
        "modo": MODO, "backend": BACKEND, "temp_c": TEMP, "tabla_nn": TABLA_NN,
        "marcos": {"grilla": 2, "riesgo": 2,
                   "nota": "el largo total es nucleotidos (marco 2 de D63); la lectura de "
                           "marco 1 de cada fragmento viaja en sus dos columnas"},
        "clave_de_la_juntura_en_el_inventario_de_M6": {
            "clave": "(quimera <nombre>, \"juntura\")",
            "quien_la_decidio": "D78, con granularidad quimera x organismo x gen impactado "
                                "y los j fuera de la clave",
            "estado": "decidida y NO implementada por falta de insumo "
                      "(PREGUNTAS_ABIERTAS 41), asi que una quimera todavia puede pasar la "
                      "compuerta con su empalme sin tamizar",
            "la_fila_completa": "la produce research/ola6/O3_quimera_bicc_vatpase_b/"
                                "scripts/03_alerta_d48.py, que resuelve las anotaciones"},
        "python": sys.version.split()[0],
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\nlas diez primeras bajo el objetivo '%s'" % a.objetivo)
    print("  las tres cuentas van separadas y no se suman en una sola cifra (D67):")
    print("  'her' son ventanas heredadas eficientes, 'ef_jun' son de juntura, y")
    print("  'fab21'/'fab19' son referencias con un bloque fabricado por el empalme.\n")
    print("%-44s %5s %5s %6s %5s %6s %7s" % (
        "quimera", "her", "junt", "ef_jun", "fab21", "fab19", "blanco"))
    for f in filas[:10]:
        print("%-44s %5d %5d %6d %5d %6d %7d" % (
            f["quimera"], f["ef_heredadas"], f["ventanas_juntura"], f["ef_juntura"],
            f["fabricados_21_refs"], f["fabricados_ge19_refs"],
            f["juntura_con_blanco_continuo"]))
    con_alerta = sum(1 for f in filas if f["alerta_juntura_nueva"] == "si")
    print("\ncombinaciones con alerta de juntura nueva: %d de %d" % (con_alerta, len(filas)))
    print("escrito en %s" % res)
    return 0


if __name__ == "__main__":
    sys.exit(main())

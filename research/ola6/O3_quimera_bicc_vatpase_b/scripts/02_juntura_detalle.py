"""O3 paso 2 — que bloque de la juntura coincide, en que referencia, y si es nuevo.

Que pregunta contesta, y por que no la contesta el tamizado. `offtarget_21nt.py` dice si
una ventana tiene un bloque perfecto de 19 nt o mas en una referencia; no dice cual
bloque ni donde cae. Para la alerta que pide el issue #23 --si la union fabrica una
coincidencia que ninguno de los dos padres tenia-- hace falta el detalle, porque un
bloque de 19 nt que entra entero en el aporte de un solo gen **no lo fabrica el empalme**:
ya existia en ese gen y la quimera lo hereda. Fabricado es el bloque que toma al menos
un nucleotido de cada uno de los dos genes. Esa es la distincion que decide la alerta, y
es la misma que `empalme_maiz_detalle.py` hizo para C13 en un caso.

Que hace: por cada una de las 20 ventanas de cada juntura, enumera sus bloques de 19, 20
y 21 nt, los busca **exactos y en las dos hebras** en las seis referencias del panel
—incluida la humana, que el preregistro §2.4 exige y que no vive en `work/offtarget_db/`—
con un automata de Aho-Corasick, y reporta de cada acierto el largo del bloque, su offset,
el aporte de cada gen, si cruza la union y en que secuencias de la referencia cae.

**Blanco continuo** se mide con el metodo de `research/ola5/N4_quimeras/scripts/junturas.py`,
que es el que manda el preregistro §5.2: un 21-mero tiene blanco continuo si existe como
tramo contiguo en **uno de los dos genes que se quieren silenciar**, en cualquiera de las
dos hebras. No es lo mismo que buscarlo en el genoma entero del vector: un 21-mero de
juntura puede existir en otra parte del genoma sin que eso silencie el blanco pretendido.

Que NO hace, y conviene leerlo al lado del resultado:

  - **No localiza los aciertos de un desapareo** (`mm1_21`). Busca coincidencia exacta.
    Los `mm1_21` que cuenta el tamizado quedan como cuenta, sin bloque ni transcripto.
  - **No escribe secuencias.** Ni la ventana, ni el bloque. `BicC_Dm` es una de las
    cuatro secuencias de EPILAB, que por la regla de confidencialidad de `CLAUDE.md` no
    se publican, y una columna de ventanas solapadas reconstruye el gen: es el incidente
    de C9 y el motivo de `tools/verificacion/sin_secuencias.py`. De cada bloque van su
    largo, su offset, su aporte por gen, su hash corto y donde cae. Para ver la secuencia
    hay que regenerarla con el paso 1.
  - **No decide.** Emite la fila de alerta cuando corresponde; la justificacion la
    escribe el usuario (D48).

Nada sale de la maquina: las seis referencias se leen de disco.

Uso:
    python research/ola6/O3_quimera_bicc_vatpaseb/scripts/02_juntura_detalle.py \
        --modo corregido
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import sys
from pathlib import Path

import ahocorasick

RAIZ = Path(__file__).resolve().parents[4]
BLOQUE = Path(__file__).resolve().parents[1]
RESULTADOS = BLOQUE / "resultados"
DB = RAIZ / "work/offtarget_db"
#: La humana no esta en `work/offtarget_db/` y el preregistro la exige en el panel (§2.4).
HUMANA = RAIZ / "work/W5/ref/humano_rna.fna.gz"
SIFI = RAIZ / "work/C13/sifi"

sys.path.insert(0, str(RAIZ / "tools/sifi21_port"))
sys.path.insert(0, str(RAIZ / "research/ola3/C13_quimeras_region_recomendada/scripts"))
import ranking as R       # noqa: E402  los nombres y los pesos del panel
import ranking_v2 as V    # noqa: E402  solo para registrar el panel de seis
import quimeras_v2 as QV  # noqa: E402  los recortes y los conjuntos

COMP = str.maketrans("ACGT", "TGCA")
VENTANA = 21
#: El conjunto de O3, con las mismas coordenadas con las que corrio el evaluador.
GEN_SPEC = ["BicC_Dm=922-1221",
            "VATPaseB_Dm=517-816:work/O3/fasta/VATPaseB_Dm_full.fasta"]


def rc(s: str) -> str:
    return s.translate(COMP)[::-1]


def hash_corto(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()[:12]


def perfil_juntura(nombre: str, modo: str, backend: str, n: int) -> dict:
    """is_efficient por posicion de la quimera, de la corrida de quimeras_v2.py."""
    ruta = SIFI / ("o3_%s_%s" % (modo, backend)) / ("%s_%s_%s.tsv" % (nombre, modo, backend))
    if not ruta.exists():
        raise SystemExit("falta %s; corre primero quimeras_v2.py con --nombre o3" % ruta)
    return {int(f["pos"]): QV.es_eficiente(f) for f in QV.leer_tsv(ruta)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--modo", choices=("fiel", "corregido"), default="corregido")
    ap.add_argument("--backend", choices=("exe", "vienna"), default="vienna")
    ap.add_argument("--min-bloque", type=int, default=19, dest="min_bloque")
    a = ap.parse_args(argv)

    # Sin esto `R.corto()` no reconoce `humano_rna` y lo etiqueta como el vector, que es
    # on-target: un acierto en la humana quedaria clasificado como blanco y no como riesgo.
    V.con_panel(sin_humano=False)

    conjunto = QV.registrar_conjunto("o3", GEN_SPEC)
    genes = QV.regiones_de(conjunto)
    regiones = QV.recortar(conjunto)

    # Los blancos pretendidos, enteros y en las dos hebras. Es el metodo de
    # `research/ola5/N4_quimeras/scripts/junturas.py`, que es el que manda el preregistro
    # (§5.2): un 21-mero «tiene blanco continuo» si existe como tramo contiguo en el gen
    # que se quiere silenciar, no en cualquier parte del genoma.
    blancos = {}
    for g in genes:
        s = QV.leer_fasta_simple(QV.fasta_full(g)).upper()
        blancos[g] = (s, rc(s))

    fichas, buscar = [], {}
    for izq, der in ((genes[0], genes[1]), (genes[1], genes[0])):
        nombre = "Q_%s__%s" % (izq, der)
        corte = len(regiones[izq])
        seq = regiones[izq] + regiones[der]
        perfil = perfil_juntura(nombre, a.modo, a.backend, len(seq) - VENTANA + 1)
        tramo = seq[corte - 20:corte + 20]
        assert len(tramo) == 40, nombre
        for j in range(1, 21):
            vent = tramo[j - 1:j + 20]
            n_izq = 21 - j
            pos_q = corte - 20 + j            # posicion de la ventana en la quimera
            for largo in range(a.min_bloque, VENTANA + 1):
                for off in range(0, VENTANA - largo + 1):
                    bloque = vent[off:off + largo]
                    desde_izq = max(0, min(largo, n_izq - off))
                    fichas.append({
                        "quimera": nombre, "izquierda": izq, "derecha": der,
                        "j": j, "pos_en_la_quimera": pos_q,
                        "ventana_eficiente": bool(perfil.get(pos_q, False)),
                        "ventana_hash": hash_corto(vent),
                        "bloque_largo": largo, "bloque_offset": off,
                        "bloque_hash": hash_corto(bloque),
                        "nt_de_izquierda": desde_izq,
                        "nt_de_derecha": largo - desde_izq,
                        "cruza_la_union": 0 < desde_izq < largo,
                        "blanco_continuo_en": [g for g, (d, r) in blancos.items()
                                               if vent in d or vent in r]
                        if largo == VENTANA else []})
                    i = len(fichas) - 1
                    buscar.setdefault(bloque, []).append(i)
                    buscar.setdefault(rc(bloque), []).append(i)

    print("%d fichas de bloque, %d patrones distintos (dos hebras)"
          % (len(fichas), len(buscar)))

    aut = ahocorasick.Automaton()
    for pat, idxs in buscar.items():
        aut.add_word(pat, (pat, idxs))
    aut.make_automaton()

    aciertos: dict[int, dict[str, set]] = {}
    refs = sorted(DB.glob("*.fna.gz")) + [HUMANA]
    if not HUMANA.exists():
        raise SystemExit("falta la referencia humana en %s; el panel del "
                         "preregistro es de seis" % HUMANA)
    for ruta in refs:
        ref = ruta.name.replace(".fna.gz", "")
        n_rec = n_hit = 0
        nombre_rec, buf = None, []

        def cerrar(nombre_rec, buf):
            if nombre_rec is None:
                return 0
            seq = "".join(buf)
            vistos = set()
            for _, (pat, idxs) in aut.iter(seq):
                for i in idxs:
                    aciertos.setdefault(i, {}).setdefault(ref, set()).add(nombre_rec)
                    vistos.add(i)
            return len(vistos)

        with gzip.open(ruta, "rt") as fh:
            for linea in fh:
                if linea.startswith(">"):
                    n_hit += cerrar(nombre_rec, buf)
                    n_rec += 1
                    nombre_rec, buf = linea[1:].strip().split()[0], []
                else:
                    buf.append(linea.strip().upper())
        n_hit += cerrar(nombre_rec, buf)
        print("  %-28s %7d secuencias, %3d fichas con acierto"
              % (R.corto(ref), n_rec, n_hit))

    # ---------------------------------------------------------------- las tres cuentas
    salida, alertas = [], []
    for i, f in enumerate(fichas):
        if i not in aciertos:
            continue
        f = dict(f)
        f["aciertos"] = {R.corto(ref): sorted(ids)
                         for ref, ids in sorted(aciertos[i].items())}
        f["on_target_del_vector"] = list(f["aciertos"]) == [R.corto(R.DMAIDIS)]
        salida.append(f)

    resumen = {}
    for nombre in sorted({f["quimera"] for f in fichas}):
        del_q = [f for f in fichas if f["quimera"] == nombre]
        con_acierto = [f for f in salida if f["quimera"] == nombre]
        ventanas_ef = sorted({f["j"] for f in del_q if f["ventana_eficiente"]})
        # blanco continuo por el metodo de N4: el 21-mero existe en un gen blanco
        blanco = sorted({f["j"] for f in del_q
                         if f["bloque_largo"] == VENTANA and f["blanco_continuo_en"]})
        # fabricado por el empalme: bloque que cruza la union, en una referencia que no
        # es el vector (en el vector seria blanco, no riesgo)
        fabricados = [f for f in con_acierto if f["cruza_la_union"]
                      and not f["on_target_del_vector"]]
        resumen[nombre] = {
            "ventanas_de_juntura": len(set(f["j"] for f in del_q)),
            "juntura_eficientes": len(ventanas_ef),
            "juntura_eficientes_j": ventanas_ef,
            "juntura_con_blanco_continuo_21nt": len(blanco),
            "juntura_eficientes_con_blanco_continuo": len(
                [j for j in blanco if j in ventanas_ef]),
            "bloques_con_acierto": len(con_acierto),
            "bloques_fabricados_por_el_empalme": len(fabricados),
            "referencias_fabricadas": sorted({r for f in fabricados
                                              for r in f["aciertos"]}),
        }
        for f in fabricados:
            for ref, ids in f["aciertos"].items():
                alertas.append({
                    "quimera": nombre, "j": f["j"],
                    "pos_en_la_quimera": f["pos_en_la_quimera"],
                    "ventana_eficiente": f["ventana_eficiente"],
                    "bloque_largo": f["bloque_largo"],
                    "bloque_hash": f["bloque_hash"],
                    "nt_de_izquierda": f["nt_de_izquierda"],
                    "nt_de_derecha": f["nt_de_derecha"],
                    "organismo_corto": ref, "secuencias": ids})

    RESULTADOS.mkdir(parents=True, exist_ok=True)
    suf = "o3_%s_%s" % (a.modo, a.backend)
    (RESULTADOS / ("juntura_detalle_%s.json" % suf)).write_text(json.dumps({
        "modo": a.modo, "backend": a.backend, "min_bloque": a.min_bloque,
        "coordenadas": {g: list(QV.CONJUNTOS[conjunto][g]) for g in genes},
        "panel": sorted(R.corto(r.name.replace(".fna.gz", "")) for r in refs),
        "limite": "localiza coincidencia exacta de 19 a 21 nt; los aciertos de un "
                  "desapareo (mm1_21) quedan como cuenta del tamizado, sin bloque",
        "sin_secuencias": "las ventanas y los bloques van por hash: BicC_Dm es una de "
                          "las cuatro secuencias de EPILAB (CLAUDE.md, incidente de C9)",
        "resumen": resumen, "bloques_con_acierto": salida,
        "python": sys.version.split()[0],
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    with open(RESULTADOS / ("juntura_resumen_%s.tsv" % suf), "w", encoding="utf-8",
              newline="") as fh:
        cols = ["quimera"] + [k for k in next(iter(resumen.values()))]
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        for nombre, d in resumen.items():
            w.writerow({"quimera": nombre, **{k: (v if not isinstance(v, list)
                                                  else ",".join(map(str, v)))
                                              for k, v in d.items()}})

    print("\nlas dos cuentas de la juntura, por quimera")
    for nombre, d in resumen.items():
        print("  %-26s eficientes %d/%d (j=%s), con blanco continuo de 21 nt %d, "
              "de esas eficientes %d"
              % (nombre, d["juntura_eficientes"], d["ventanas_de_juntura"],
                 ",".join(map(str, d["juntura_eficientes_j"])) or "-",
                 d["juntura_con_blanco_continuo_21nt"],
                 d["juntura_eficientes_con_blanco_continuo"]))
        print("  %-26s bloques con acierto %d, fabricados por el empalme %d %s"
              % ("", d["bloques_con_acierto"],
                 d["bloques_fabricados_por_el_empalme"],
                 "(" + ", ".join(d["referencias_fabricadas"]) + ")"
                 if d["referencias_fabricadas"] else ""))

    if alertas:
        print("\nALERTA: el empalme fabrica %d coincidencia(s) que ningun gen tenia"
              % len(alertas))
        for al in alertas:
            print("  %s j=%d  bloque de %d nt (%d+%d)  en %s: %s  [ventana %s]"
                  % (al["quimera"], al["j"], al["bloque_largo"],
                     al["nt_de_izquierda"], al["nt_de_derecha"],
                     al["organismo_corto"], ", ".join(al["secuencias"]),
                     "eficiente" if al["ventana_eficiente"] else "no eficiente"))
        (RESULTADOS / ("juntura_alertas_%s.json" % suf)).write_text(
            json.dumps(alertas, indent=2, ensure_ascii=False), encoding="utf-8")
        print("\n  las filas van a juntura_alertas_%s.json; los cuatro campos de D48 "
              "los completa el usuario" % suf)
    else:
        print("\nel empalme no fabrica ninguna coincidencia fuera del vector")
    print("\nescrito en %s" % RESULTADOS)
    return 0


if __name__ == "__main__":
    sys.exit(main())

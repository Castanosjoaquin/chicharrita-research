"""N3 - El marco intermedio cruzado con el eje de referencia, hasta donde la maquina permite.

El ultimo hueco de computo de la ola 5. `M7` §4 recalculo la eficiencia de las tres regiones de
`BicC_Dm` **sobre la molecula recortada tal como la escribe cada fuente** --el marco 3-- contra
cuatro fuentes. Lo que falta es el marco intermedio: los `L - 20` 21-meros que existen en la
molecula, pero con la accesibilidad evaluada sobre el **gen completo tal como lo escribe esa
fuente**. Para eso hay que reconstruir el gen entero por fuente, no solo la region.

**Tres de las cuatro fuentes no se pueden correr en esta maquina, y conviene decir por que.**
`eje_referencia.py` alinea con `blastn` local contra las bases de `work/W5/db/`. En esta maquina
no hay `blastn` ni `makeblastdb` --verificado con `shutil.which`-- y `work/W5/` no esta en el
arbol, asi que de las cuatro fuentes:

  GHCC01 (Pergamino)   la base no esta en disco. **No corrida.**
  GCWP01 (Illinois)    la base no esta en disco. **No corrida.** Ademas cubre fragmentos y no
                       cubre un solo nucleotido de 922-1221, asi que esa region no se compara
                       ahi ni con la base presente.
  genoma del Reino     `GCA_975739785.1` si esta en `work/offtarget_db/`, pero son 984 MB y
  Unido                ubicar el gen y sus exones sin un alineador de consultas largas no es
                       viable. **No corrida.**
  GITV01 (Ohio State)  los dos contigs que la ola 3 identifico como blanco principal estan en
                       `work/M1/bases/gitv01_blancos.fa`. **Esta es la que se corre.**

Que se gana con esa sola fuente. Es la menos favorable a la region que recomendamos: es la unica
de las cuatro donde los conteos recalculados **bajan** --25, 19 y 17 contra 26, 22 y 17-- y donde
2121-2420 conserva una fraccion mayor de sus eficientes que 922-1221 (33 de 35 contra 32 de 36).
Si el marco intermedio tiene que aguantar en algun lugar, es ahi.

El metodo del alineamiento no es el de `M7` y eso es a favor. Aca se alinea con
`PairwiseAligner` de Biopython, que es el metodo de `C8`, contra los contigs que la ola 3 ya
habia ubicado. El script **exige** que el gen quede cubierto por un solo bloque sin huecos y en
sus 2.520 posiciones, y aborta si no: sin eso la reconstruccion tendria que rellenar posiciones
con las bases de EPILAB, que seria una quimera y no una fuente. Y el ancla es que el marco 3
reproduzca los tres conteos que `M7` publico con blastn: si dos metodos de alineamiento distintos
dan los mismos tres numeros, la reconstruccion no depende del alineador.

Configuracion: punto por defecto, modo `corregido`, ViennaRNA 2.7.2, tabla `RNA_NN3`.

Uso (desde la raiz del repositorio):
    python research/ola5/N3_marcos/scripts/marco2_por_fuente.py
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

AQUI = Path(__file__).resolve()
RAIZ = AQUI.parents[4]
SALIDA = AQUI.parents[1] / "resultados"
sys.path.insert(0, str(AQUI.parent))

from tres_marcos import eficientes, leer_fasta  # noqa: E402

K = 21
GEN = "BicC_Dm"
FASTA_GEN = RAIZ / "work" / "sifi_check" / f"{GEN}_full.fasta"
CONTIGS = RAIZ / "work" / "M1" / "bases" / "gitv01_blancos.fa"
FUENTE = "GITV01000968.1"

REGIONES = {"922-1221": (922, 1221), "2121-2420": (2121, 2420), "264-563": (264, 563)}

#: Conteos de EPILAB en los tres marcos (N3 §2), que son la columna de referencia.
EPILAB = {"922-1221": (36, 29, 26), "2121-2420": (35, 27, 22), "264-563": (20, 15, 17)}

#: Ancla: lo que M7 §4 publico para GITV01 con blastn, marco 3, modo corregido.
ANCLA_M7_MARCO3 = {"922-1221": 25, "2121-2420": 19, "264-563": 17}

#: Las tres fuentes que no se pueden correr aca, con el motivo exacto.
NO_CORRIDAS = {
    "GHCC01": "la base no esta en disco en esta maquina (work/W5/db/ no esta en el arbol)",
    "GCWP01": "la base no esta en disco; ademas no cubre un solo nucleotido de 922-1221",
    "genoma_GCA_975739785.1":
        "esta en work/offtarget_db/ pero son 984 MB y no hay blastn ni makeblastdb en esta "
        "maquina para ubicar el gen y sus exones",
}


def leer_multi(ruta: Path) -> list[tuple[str, str]]:
    out, nom, buf = [], None, []
    for l in ruta.read_text().splitlines():
        if l.startswith(">"):
            if nom is not None:
                out.append((nom, "".join(buf)))
            nom, buf = l[1:].split()[0], []
        else:
            buf.append(l.strip())
    if nom is not None:
        out.append((nom, "".join(buf)))
    return out


def main() -> int:
    for p in (FASTA_GEN, CONTIGS):
        if not p.exists():
            raise SystemExit("falta %s; `work/` no esta en git" % p)
    if shutil.which("blastn"):
        print("AVISO: hay blastn en el PATH. Corre `eje_referencia.py` de M7, que hace las "
              "cuatro fuentes; este script existe para la maquina que no lo tiene.")

    try:
        from Bio import Align
    except ImportError as e:                                  # pragma: no cover
        raise SystemExit("hace falta Biopython para el alineamiento local: %s" % e)

    gen = leer_fasta(FASTA_GEN)
    contigs = dict(leer_multi(CONTIGS))
    if FUENTE not in contigs:
        raise SystemExit("%s no esta en %s" % (FUENTE, CONTIGS))
    fuente = contigs[FUENTE].upper().replace("U", "T")

    al = Align.PairwiseAligner(mode="local", match_score=2, mismatch_score=-3,
                               open_gap_score=-7, extend_gap_score=-2)
    aln = al.align(gen, fuente)[0]
    bloques_gen, bloques_src = aln.aligned[0], aln.aligned[1]

    # La compuerta: un solo bloque, sin huecos, y las 2.520 posiciones del gen.
    cubierto = sum(e - i for i, e in bloques_gen)
    if len(bloques_gen) != 1 or cubierto != len(gen):
        raise SystemExit(
            "la reconstruccion no es limpia: %d bloques y %d de %d posiciones cubiertas. "
            "Rellenar con bases de EPILAB daria una quimera y no una fuente; esta corrida "
            "queda declarada no hecha." % (len(bloques_gen), cubierto, len(gen)))

    ini_src = bloques_src[0][0]
    reconstruido = fuente[ini_src:ini_src + len(gen)]
    if len(reconstruido) != len(gen):
        raise SystemExit("el bloque del contig se queda corto: %d contra %d"
                         % (len(reconstruido), len(gen)))
    desajustes = [i + 1 for i, (a, b) in enumerate(zip(gen, reconstruido)) if a != b]

    # Los tres marcos sobre el gen reconstruido.
    efic_gen = eficientes(reconstruido)
    filas = {}
    for nom, (i, f) in REGIONES.items():
        ult = f - (K - 1)
        m1 = sum(1 for p in efic_gen if i <= p <= f)
        m2 = sum(1 for p in efic_gen if i <= p <= ult)
        m3 = len(eficientes(reconstruido[i - 1:f]))
        filas[nom] = {"marco1": m1, "marco2": m2, "marco3": m3,
                      "epilab": list(EPILAB[nom]),
                      "desajustes_en_la_region": sum(1 for d in desajustes if i <= d <= f)}

    roto = [("%s marco 3: %d, M7 publico %d" % (n, filas[n]["marco3"], esp))
            for n, esp in ANCLA_M7_MARCO3.items() if filas[n]["marco3"] != esp]
    if roto:
        raise SystemExit("el ancla de M7 no se reprodujo:\n  " + "\n  ".join(roto))

    orden = {}
    for marco in ("marco1", "marco2", "marco3"):
        v = {n: filas[n][marco] for n in REGIONES}
        orden[marco] = {"valores": v,
                        "orden": sorted(v, key=lambda n: -v[n]),
                        "gana_922_a_2121": v["922-1221"] > v["2121-2420"],
                        "empate_922_2121": v["922-1221"] == v["2121-2420"]}

    out = {"fuente": FUENTE, "metodo": "PairwiseAligner local (el de C8), un bloque sin huecos",
           "cobertura_del_gen": "%d/%d" % (cubierto, len(gen)),
           "desajustes_contra_epilab": len(desajustes),
           "posiciones_con_desajuste": desajustes,
           "ancla_m7_marco3": ANCLA_M7_MARCO3,
           "configuracion": {"modo": "corregido", "backend": "vienna", "tabla_nn": "NN3"},
           "regiones": filas, "orden": orden, "fuentes_no_corridas": NO_CORRIDAS}
    SALIDA.mkdir(parents=True, exist_ok=True)
    (SALIDA / "marco2_por_fuente.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    print("%s reconstruye el gen entero: %d/%d posiciones, %d desajustes contra EPILAB"
          % (FUENTE, cubierto, len(gen), len(desajustes)))
    print("\n%-10s %-28s %-28s" % ("region", "EPILAB (m1/m2/m3)", "GITV01 (m1/m2/m3)"))
    for nom in REGIONES:
        d = filas[nom]
        print("%-10s %-28s %-28s  desajustes en la region: %d"
              % (nom, "%d / %d / %d" % tuple(d["epilab"]),
                 "%d / %d / %d" % (d["marco1"], d["marco2"], d["marco3"]),
                 d["desajustes_en_la_region"]))
    print("\nOrden de las tres regiones con la secuencia de GITV01:")
    for marco, d in orden.items():
        print("  %-7s %s -> %s%s" % (marco, d["valores"], d["orden"],
                                     "  (EMPATE 922 vs 2121)" if d["empate_922_2121"] else ""))
    print("\nancla de M7 reproducida con otro alineador: marco 3 da %s"
          % [filas[n]["marco3"] for n in REGIONES])
    print("fuentes no corridas: %s" % ", ".join(NO_CORRIDAS))
    print("resultados en %s" % (SALIDA / "marco2_por_fuente.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

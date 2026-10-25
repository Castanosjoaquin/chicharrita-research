"""N4 - Las ventanas de juntura de una quimera: dos preguntas que no son la misma.

Lo que pide la carta del investigador del 2026-10-25 `[R]`: «que un siRNA atraviese una
juntura no significa que encuentre una region complementaria continua en alguno de los
targets. Son aspectos diferentes que convendria evaluar por separado.»

Lo que el repositorio ya tenia, y por eso esta linea es corta. C4 y C13 midieron las 240
ventanas de empalme de las doce quimeras: cuantas son eficientes (48 con las regiones de
EPILAB, **4** con las vigentes, en modo `corregido`) y que off-targets fabrica la union
contra las seis referencias no objetivo —incluido un bloque de 19 nt en maiz que no existe
en ninguno de los dos genes— `[M]`. Eso contesta «que produce la molecula» y «a que no
objetivo pega».

Lo que faltaba es la otra mitad de la pregunta, que nadie habia mirado: de esas ventanas de
juntura, **cuantas tienen un blanco**. Un 21-mero a caballo de la union no existe como tramo
continuo en ningun transcrito, porque la union es secuencia que el ensamblado fabrica. Si
ademas es eficiente, es capacidad de silenciamiento gastada: ocupa la maquinaria del insecto
con un siRNA que no tiene a que unirse de forma continua. El conteo de eficientes de una
quimera lo cuenta como si valiera.

La contabilidad de una quimera, que conviene escribir una vez. Con fragmentos de largo `L_i`
y ventanas de 21 nt, la molecula ensamblada tiene `sum(L_i) - 20` ventanas, y se reparten
asi: por cada fragmento, los `L_i - 20` arranques que existen tambien en el gen —los mismos
del marco 2 de N3—, y por cada union, 20 ventanas nuevas. O sea que **una quimera cambia los
20 arranques de la cola de cada fragmento por 20 ventanas de juntura**, y las de juntura no
existen en ningun blanco. No es un detalle de borde: son 20 ventanas por union, el mismo
orden de magnitud que la diferencia entre los marcos de conteo de N3.

Alcance. Esto mide perdida de eficacia sobre los blancos propios y gasto de molecula. No es,
y no se lee como, una via para ampliar el rango de nada: una ventana sin blanco continuo es
una ventana que no silencia, y las coincidencias con no objetivo son las que ya miden C4, C13
y M6.

Configuracion: punto por defecto, modo `corregido` —el del ranking—, ViennaRNA 2.7.2, tabla
`RNA_NN3`. Los blancos pretendidos son los cuatro genes de EPILAB.

Uso (desde la raiz del repositorio):
    python research/ola5/N4_quimeras/scripts/junturas.py
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve()
RAIZ = AQUI.parents[4]
SALIDA = AQUI.parents[1] / "resultados"
sys.path.insert(0, str(RAIZ / "tools" / "sifi21_port"))

from sifi_core import DEFAULTS, SifiEngine  # noqa: E402

K = 21
GENES = ["MP_MRFV", "CP_MRFV", "BicC_Dm", "ATPaseD_Dm"]
FASTA = {g: RAIZ / "work" / "sifi_check" / f"{g}_full.fasta" for g in GENES}

#: Las cuatro regiones vigentes, que son las partes de las doce quimeras de C13.
VIGENTES = {"MP_MRFV": (72, 271), "CP_MRFV": (99, 298),
            "BicC_Dm": (922, 1221), "ATPaseD_Dm": (72, 371)}

#: Ancla de C13 §5: eficientes del empalme por quimera, modo `corregido` `[M]`.
ANCLA_C13 = {
    ("ATPaseD_Dm", "MP_MRFV"): 0, ("MP_MRFV", "CP_MRFV"): 0,
    ("MP_MRFV", "BicC_Dm"): 0, ("ATPaseD_Dm", "BicC_Dm"): 1,
    ("CP_MRFV", "BicC_Dm"): 1, ("BicC_Dm", "CP_MRFV"): 1,
    ("ATPaseD_Dm", "CP_MRFV"): 1, ("BicC_Dm", "MP_MRFV"): 0,
    ("CP_MRFV", "ATPaseD_Dm"): 0, ("BicC_Dm", "ATPaseD_Dm"): 0,
    ("MP_MRFV", "ATPaseD_Dm"): 0, ("CP_MRFV", "MP_MRFV"): 0,
}
ANCLA_TOTAL = 4

COMP = str.maketrans("ACGTacgt", "TGCAtgca")


def rc(s: str) -> str:
    return s.translate(COMP)[::-1]


def leer_fasta(ruta: Path) -> str:
    return "".join(l.strip() for l in ruta.read_text().splitlines()
                   if not l.startswith(">"))


def eficientes(seq: str) -> set[int]:
    eng = SifiEngine(mode="corregido", temp_c=22.0, tabla_nn="NN3", **DEFAULTS)
    ventanas, _ = eng.run(seq, backend="vienna")
    return {w.pos for w in ventanas if w.is_efficient}


def main() -> int:
    faltan = [g for g in GENES if not FASTA[g].exists()]
    if faltan:
        raise SystemExit("faltan los FASTA de %s en work/sifi_check/; `work/` no esta en git"
                         % ", ".join(faltan))

    genes = {g: leer_fasta(FASTA[g]).upper().replace("U", "T") for g in GENES}
    # Los blancos pretendidos, en las dos hebras: un 21-mero "tiene blanco continuo" si
    # aparece como tramo contiguo en alguno. Con 240 consultas la busqueda directa da la
    # misma respuesta que el automata de `offtarget_21nt.py` y no agrega una dependencia.
    blancos = {g: (s, rc(s)) for g, s in genes.items()}
    frag = {g: genes[g][VIGENTES[g][0] - 1:VIGENTES[g][1]] for g in GENES}

    filas, roto = [], []
    tot = {"junturas": 0, "eficientes": 0, "con_blanco": 0, "efic_sin_blanco": 0}
    for a, b in itertools.permutations(GENES, 2):
        quimera = frag[a] + frag[b]
        la = len(frag[a])
        efic = eficientes(quimera)
        # La ventana que arranca en p cubre p..p+20; cruza la union si p <= la < p+20.
        junturas = list(range(la - (K - 2), la + 1))
        assert len(junturas) == K - 1 == 20

        detalle = []
        for p in junturas:
            w = quimera[p - 1:p - 1 + K]
            con_blanco = [g for g, (d, r) in blancos.items() if w in d or w in r]
            detalle.append({"pos_en_quimera": p, "eficiente": p in efic,
                            "blancos_continuos": con_blanco})

        n_efic = sum(1 for d in detalle if d["eficiente"])
        n_blanco = sum(1 for d in detalle if d["blancos_continuos"])
        n_efic_sin = sum(1 for d in detalle
                         if d["eficiente"] and not d["blancos_continuos"])

        if ANCLA_C13.get((a, b)) != n_efic:
            roto.append("%s + %s: empalme con %d eficientes, C13 publico %s"
                        % (a, b, n_efic, ANCLA_C13.get((a, b))))

        filas.append({
            "quimera": "%s + %s" % (a, b), "primera": a, "segunda": b,
            "largo": len(quimera), "ventanas": len(quimera) - (K - 1),
            "ventanas_propias": (la - (K - 1)) + (len(frag[b]) - (K - 1)),
            "ventanas_de_juntura": len(junturas),
            "juntura_eficientes": n_efic,
            "juntura_con_blanco_continuo": n_blanco,
            "juntura_eficientes_sin_blanco": n_efic_sin,
            "ancla_c13": ANCLA_C13.get((a, b)),
            "detalle": detalle,
        })
        tot["junturas"] += len(junturas)
        tot["eficientes"] += n_efic
        tot["con_blanco"] += n_blanco
        tot["efic_sin_blanco"] += n_efic_sin

    if roto:
        raise SystemExit("anclas rotas:\n  " + "\n  ".join(roto))
    if tot["eficientes"] != ANCLA_TOTAL:
        raise SystemExit("el total del empalme da %d y C13 publico %d"
                         % (tot["eficientes"], ANCLA_TOTAL))

    SALIDA.mkdir(parents=True, exist_ok=True)
    cols = ["quimera", "largo", "ventanas", "ventanas_propias", "ventanas_de_juntura",
            "juntura_eficientes", "juntura_con_blanco_continuo",
            "juntura_eficientes_sin_blanco"]
    lineas = ["\t".join(cols)]
    for f in sorted(filas, key=lambda x: -x["juntura_eficientes"]):
        lineas.append("\t".join(str(f[c]) for c in cols))
    (SALIDA / "junturas.tsv").write_text("\n".join(lineas) + "\n", encoding="utf-8")
    (SALIDA / "junturas.json").write_text(
        json.dumps({"configuracion": {"modo": "corregido", "backend": "vienna",
                                      "tabla_nn": "NN3", "sirna_size": K},
                    "regiones": {g: list(VIGENTES[g]) for g in GENES},
                    "blancos_pretendidos": GENES,
                    "ancla_c13_total": ANCLA_TOTAL, "totales": tot, "filas": filas},
                   indent=2, ensure_ascii=False), encoding="utf-8")

    print("%-26s %6s %8s %9s %12s" % ("quimera", "vent.", "juntura", "eficien.",
                                      "sin blanco"))
    for f in sorted(filas, key=lambda x: -x["juntura_eficientes"]):
        print("%-26s %6d %8d %9d %12d"
              % (f["quimera"], f["ventanas"], f["ventanas_de_juntura"],
                 f["juntura_eficientes"], f["juntura_eficientes_sin_blanco"]))
    print("\n240 ventanas de juntura en las doce quimeras:")
    print("  eficientes:                        %3d  (ancla de C13: %d)"
          % (tot["eficientes"], ANCLA_TOTAL))
    print("  con blanco continuo en algun gen:  %3d" % tot["con_blanco"])
    print("  eficientes y sin blanco continuo:  %3d" % tot["efic_sin_blanco"])
    print("\nresultados en %s" % SALIDA)
    return 0


if __name__ == "__main__":
    sys.exit(main())

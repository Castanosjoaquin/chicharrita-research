"""N3 - Los tres marcos de conteo de una region, y de donde sale cada diferencia.

La carta del investigador del 2026-10-25 confirma el marco que ya publicabamos y propone un
tercero `[R]`:

  1. **contexto, todos los arranques.** Las `L` posiciones de arranque que caen dentro de la
     region, con la accesibilidad calculada sobre el gen completo. Las ultimas 20 ventanas
     se completan con nucleotidos que estan afuera de la region.
  2. **contexto, los arranques comparables.** Solo los `L - 20` 21-meros que existen
     fisicamente en la molecula que se sintetiza, pero con la accesibilidad evaluada en el
     transcrito en su contexto. Es el marco que el investigador propone explorar: «los
     21-mers que existen fisicamente en la molecula, pero evaluando su accesibilidad en el
     transcrito blanco».
  3. **molecula recortada.** Los mismos `L - 20` arranques, con la molecula de `L` nt
     plegada sola. Es la cifra que se publica, porque es la molecula que existe.

Con eso la diferencia entre la cifra mas alta y la mas baja se parte en dos causas que no se
parecen, y es la particion que pide el punto 5 de su carta:

  - **limite fisico de la molecula**: marco 1 menos marco 2. Son arranques que el gen tiene
    y la molecula no. No opina el modelo de eficiencia: la ventana no existe.
  - **contexto de accesibilidad**: marco 2 menos marco 3. Son ventanas que existen en los
    dos lados y cambian de veredicto porque el plegado cambia.

Del **modelo de eficiencia** no sale ninguna de las dos: es el mismo criterio, los mismos
umbrales y la misma tabla en los tres marcos. Lo que cambia es que se le da de comer.

Por que este script y no el de M7. `M7/scripts/recorte_vs_contexto.py` ya mide el par de las
tres regiones de `BicC_Dm` y emite el termino que cruza en cada ventana que cambia, pero lee
los FASTA de `work/W5/plfold/`, que no esta en esta maquina. Este script hace la cuenta de
los tres marcos para las seis regiones —las cuatro vigentes mas las dos rivales de
`BicC_Dm`— desde `work/sifi_check/`, y **no** reimplementa el comparador: el detalle por
termino de las tres regiones de `BicC_Dm` sigue siendo el de
`M7/resultados/recorte_*_cambios.tsv`.

Configuracion: punto por defecto, modo `corregido` —el del ranking—, ViennaRNA 2.7.2 y tabla
`RNA_NN3`, que es la que produjo los numeros publicados de M7.

Uso (desde la raiz del repositorio):
    python research/ola5/N3_marcos/scripts/tres_marcos.py
"""

from __future__ import annotations

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

#: (gen, inicio, fin) 1-based inclusive. Las cuatro vigentes al 2026-10-23 (`BicC_Dm` por
#: D25) y las dos rivales de `BicC_Dm` que compara el eje 1 de M7.
REGIONES = [
    ("MP_MRFV", 72, 271, "vigente"),
    ("CP_MRFV", 99, 298, "vigente"),
    ("BicC_Dm", 922, 1221, "vigente, D25"),
    ("ATPaseD_Dm", 72, 371, "vigente"),
    ("BicC_Dm", 2121, 2420, "rival, la de C7"),
    ("BicC_Dm", 264, 563, "rival, la que eligio EPILAB"),
]

#: Anclas publicadas. Marco 1 de las cuatro vigentes: M7 §1. Los tres marcos de las tres
#: regiones de `BicC_Dm`: M7 §3.
ANCLA_MARCO1 = {("MP_MRFV", 72): 38, ("CP_MRFV", 99): 21,
                ("BicC_Dm", 922): 36, ("ATPaseD_Dm", 72): 21,
                ("BicC_Dm", 2121): 35, ("BicC_Dm", 264): 20}
ANCLA_TRES = {("BicC_Dm", 922): (36, 29, 26), ("BicC_Dm", 2121): (35, 27, 22),
              ("BicC_Dm", 264): (20, 15, 17)}


def leer_fasta(ruta: Path) -> str:
    return "".join(l.strip() for l in ruta.read_text().splitlines()
                   if not l.startswith(">"))


def eficientes(seq: str) -> set[int]:
    """Arranques eficientes (1-based) del criterio en el punto por defecto."""
    eng = SifiEngine(mode="corregido", temp_c=22.0, tabla_nn="NN3", **DEFAULTS)
    ventanas, _ = eng.run(seq, backend="vienna")
    return {w.pos for w in ventanas if w.is_efficient}


def main() -> int:
    faltan = [g for g in GENES if not FASTA[g].exists()]
    if faltan:
        raise SystemExit("faltan los FASTA de %s en work/sifi_check/; `work/` no esta en git"
                         % ", ".join(faltan))

    en_gen = {}
    for gen in GENES:
        en_gen[gen] = eficientes(leer_fasta(gen and FASTA[gen]))

    filas, roto = [], []
    for gen, ini, fin in [(g, i, f) for g, i, f, _ in REGIONES]:
        nota = next(n for g, i, _, n in REGIONES if g == gen and i == ini)
        largo = fin - ini + 1
        seq = leer_fasta(FASTA[gen])
        molecula = leer_fasta(FASTA[gen])[ini - 1:fin]
        assert len(molecula) == largo

        gen_efic = en_gen[gen]
        ult_comparable = fin - (K - 1)              # el ultimo arranque con 21 nt propios

        marco1 = sorted(p for p in gen_efic if ini <= p <= fin)
        marco2 = sorted(p for p in gen_efic if ini <= p <= ult_comparable)
        mol_efic = eficientes(molecula)
        marco3 = sorted(ini + q - 1 for q in mol_efic)

        s2, s3 = set(marco2), set(marco3)
        pierden = sorted(s2 - s3)
        ganan = sorted(s3 - s2)

        fila = {
            "gen": gen, "inicio": ini, "fin": fin, "largo": largo, "nota": nota,
            "arranques_marco1": largo,
            "arranques_comparables": ult_comparable - ini + 1,
            "marco1_contexto_todos": len(marco1),
            "marco2_contexto_comparables": len(marco2),
            "marco3_molecula": len(marco3),
            "limite_fisico": len(marco1) - len(marco2),
            "contexto_neto": len(marco2) - len(marco3),
            "pierden": len(pierden), "ganan": len(ganan),
            "posiciones_que_pierden": pierden, "posiciones_que_ganan": ganan,
        }
        clave = (gen, ini)
        if clave in ANCLA_MARCO1 and fila["marco1_contexto_todos"] != ANCLA_MARCO1[clave]:
            roto.append("%s %d-%d marco 1: %d, publicado %d"
                        % (gen, ini, fin, fila["marco1_contexto_todos"],
                           ANCLA_MARCO1[clave]))
        if clave in ANCLA_TRES:
            esperado = ANCLA_TRES[clave]
            obtenido = (fila["marco1_contexto_todos"], fila["marco2_contexto_comparables"],
                        fila["marco3_molecula"])
            fila["ancla_m7"] = list(esperado)
            if obtenido != esperado:
                roto.append("%s %d-%d tres marcos: %s, publicado %s"
                            % (gen, ini, fin, obtenido, esperado))
        filas.append(fila)

    if roto:
        raise SystemExit("anclas rotas:\n  " + "\n  ".join(roto))

    SALIDA.mkdir(parents=True, exist_ok=True)
    cols = ["gen", "inicio", "fin", "largo", "nota", "arranques_marco1",
            "arranques_comparables", "marco1_contexto_todos",
            "marco2_contexto_comparables", "marco3_molecula", "limite_fisico",
            "contexto_neto", "pierden", "ganan"]
    lineas = ["\t".join(cols)]
    for f in filas:
        lineas.append("\t".join(str(f[c]) for c in cols))
    (SALIDA / "tres_marcos.tsv").write_text("\n".join(lineas) + "\n", encoding="utf-8")
    (SALIDA / "tres_marcos.json").write_text(
        json.dumps({"configuracion": {"modo": "corregido", "backend": "vienna",
                                      "tabla_nn": "NN3", "temp_c": 22.0,
                                      "criterio": dict(DEFAULTS)},
                    "anclas_marco1": {"%s_%d" % k: v for k, v in ANCLA_MARCO1.items()},
                    "anclas_tres_marcos": {"%s_%d" % k: list(v)
                                           for k, v in ANCLA_TRES.items()},
                    "filas": filas}, indent=2, ensure_ascii=False),
        encoding="utf-8")

    print("%-12s %-10s %6s %6s %6s | %6s %6s %5s %5s"
          % ("gen", "region", "m1", "m2", "m3", "fisico", "contxt", "pierd", "ganan"))
    for f in filas:
        print("%-12s %-10s %6d %6d %6d | %6d %6d %5d %5d"
              % (f["gen"], "%d-%d" % (f["inicio"], f["fin"]),
                 f["marco1_contexto_todos"], f["marco2_contexto_comparables"],
                 f["marco3_molecula"], f["limite_fisico"], f["contexto_neto"],
                 f["pierden"], f["ganan"]))
    print("\ntodas las anclas publicadas se reprodujeron")
    print("resultados en %s" % SALIDA)
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Driver de N1: del FASTA al conteo historico, en un comando.

Corre el criterio de eficiencia con la configuracion que reconstruye las curvas historicas
—modo `fiel`, motor ViennaRNA, tabla de apilamiento `RNA_NN4` de `sifi21INTA`— sobre los
cuatro genes de EPILAB, y le aplica la funcion de conteo de `conteo_por_curva.py` con tres
anchos de cobertura. Escribe `resultados/conteo_por_curva.{tsv,json}` y
`resultados/procedencia.json`.

Por que esa configuracion y no la del si-Fi21 original. La carta del 2026-10-25 dice que
las curvas almacenadas reconstruyen 138, 40, 218 y 35 ventanas eficientes `[R]`, que son
los cuatro valores que la corrida 1 de la ola 3 obtuvo con `sifi21INTA` por defecto
(`research/ola3/C2_codigo_apolo_inta/corridas/README.md`) `[M]`. El si-Fi21 original con su
propio RNAplfold da 133, 32, 212 y 42, que es otro punto de partida: la regla de conteo se
mide sobre el conjunto de ventanas del que salieron las curvas, no sobre otro.

Los TSV por ventana se escriben **fuera del repositorio** (`--trabajo`, por omision una
carpeta temporal del sistema): son la entrada del contador, no un resultado, y una columna
de 21-meros solapados reconstruye el gen entero.

Uso (desde la raiz del repositorio):

    python research/ola5/N1_regla_de_conteo/scripts/correr_n1.py
    python research/ola5/N1_regla_de_conteo/scripts/correr_n1.py --trabajo /ruta/libre
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve()
RAIZ = AQUI.parents[4]
SALIDA = AQUI.parents[1] / "resultados"
sys.path.insert(0, str(AQUI.parent))
sys.path.insert(0, str(RAIZ / "tools" / "sifi21_port"))

from conteo_por_curva import (ANCHO_HISTORICO, PLANILLA, contar_por_incrementos,  # noqa: E402
                              curva_de_cobertura, medir,
                              suma_de_incrementos_positivos, tramos)
from sifi_core import DEFAULTS, SifiEngine  # noqa: E402

GENES = ["MP_MRFV", "CP_MRFV", "BicC_Dm", "ATPaseD_Dm"]
FASTA = {g: RAIZ / "work" / "sifi_check" / f"{g}_full.fasta" for g in GENES}
ANCHOS = (19, ANCHO_HISTORICO, 21)

#: El ancla de esta linea: el conjunto de ventanas del que salen las curvas historicas.
ANCLA_EFICIENTES = {"MP_MRFV": 138, "CP_MRFV": 40, "BicC_Dm": 218, "ATPaseD_Dm": 35}


def leer_fasta(ruta: Path) -> str:
    """Igual que `run_sifi.leer_fastas`: sin normalizar, para no mover el conteo."""
    return "".join(l.strip() for l in ruta.read_text().splitlines()
                   if not l.startswith(">"))


def md5(ruta: Path) -> str:
    return hashlib.md5(ruta.read_bytes()).hexdigest()


def versiones() -> dict:
    out = {"python": sys.version.split()[0], "plataforma": platform.platform()}
    try:
        import RNA
        out["viennarna"] = RNA.__version__
    except Exception as e:                                    # pragma: no cover
        out["viennarna"] = "no disponible (%s)" % e
    try:
        import Bio
        out["biopython"] = Bio.__version__
    except Exception as e:                                    # pragma: no cover
        out["biopython"] = "no disponible (%s)" % e
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--trabajo", default=None,
                    help="carpeta fuera del repositorio para los TSV por ventana")
    a = ap.parse_args(argv)

    faltan = [g for g in GENES if not FASTA[g].exists()]
    if faltan:
        raise SystemExit(
            "faltan los FASTA de %s en work/sifi_check/. `work/` no esta en git "
            "(research/ola3/C2_codigo_apolo_inta/corridas/README.md): esta linea no corre "
            "sin el corpus local." % ", ".join(faltan))

    trabajo = Path(a.trabajo) if a.trabajo else Path(tempfile.mkdtemp(prefix="n1_"))
    trabajo.mkdir(parents=True, exist_ok=True)
    SALIDA.mkdir(parents=True, exist_ok=True)

    filas, detalle = [], {}
    for gen in GENES:
        seq = leer_fasta(FASTA[gen])
        eng = SifiEngine(mode="fiel", temp_c=22.0, tabla_nn="NN4", **DEFAULTS)
        ventanas, resumen = eng.run(seq, backend="vienna")
        efic = [w.pos for w in ventanas if w.is_efficient]

        if len(efic) != ANCLA_EFICIENTES[gen]:
            raise SystemExit(
                "ancla rota en %s: %d ventanas eficientes, se esperaban %d. Sin ese "
                "conjunto el conteo por incrementos no se puede leer."
                % (gen, len(efic), ANCLA_EFICIENTES[gen]))

        # Verificacion cruzada: la cuenta por conjunto y la lectura de la curva coinciden.
        largo = resumen["largo"]
        curva = curva_de_cobertura(efic, largo + ANCHO_HISTORICO, ANCHO_HISTORICO)
        if suma_de_incrementos_positivos(curva) != contar_por_incrementos(efic):
            raise SystemExit("la curva y el conjunto no dan lo mismo en %s" % gen)

        fila = medir(gen, efic, resumen["ventanas"], ANCHOS)
        fila["largo"] = largo
        fila["tramos"] = len(tramos(curva))
        filas.append(fila)
        detalle[gen] = {"eficientes": efic, "tapados": fila["arranques_tapados"]}

        # Los TSV por ventana van afuera del repositorio.
        (trabajo / f"{gen}_fiel_vienna_nn4.tsv").write_text(
            "pos\tis_efficient\n" + "".join(
                "%d\t%s\n" % (w.pos, w.is_efficient) for w in ventanas),
            encoding="utf-8")

    ok = [f for f in filas if f.get("reproduce_planilla")]
    cols = ["gen", "largo", "ventanas", "eficientes", "tapadas",
            "a=19", "a=20", "a=21", "planilla", "sesgo_relativo"]
    lineas = ["\t".join(cols)]
    for f in filas:
        lineas.append("\t".join([
            f["nombre"], str(f["largo"]), str(f["ventanas"]), str(f["eficientes"]),
            str(f["tapadas"])] + [str(f["conteo"][str(x)]) for x in ANCHOS]
            + [str(f.get("planilla", "-")), "%.4f" % f["sesgo_relativo"]]))
    (SALIDA / "conteo_por_curva.tsv").write_text("\n".join(lineas) + "\n",
                                                 encoding="utf-8")
    (SALIDA / "conteo_por_curva.json").write_text(
        json.dumps({"ancho_historico": ANCHO_HISTORICO, "anchos": list(ANCHOS),
                    "planilla": PLANILLA, "ancla_eficientes": ANCLA_EFICIENTES,
                    "filas": filas, "detalle": detalle}, indent=2, ensure_ascii=False),
        encoding="utf-8")
    (SALIDA / "procedencia.json").write_text(
        json.dumps({"versiones": versiones(),
                    "configuracion": {"modo": "fiel", "backend": "vienna",
                                      "tabla_nn": "NN4", "temp_c": 22.0,
                                      "criterio": dict(DEFAULTS)},
                    "entradas": {g: {"ruta": str(FASTA[g].relative_to(RAIZ)),
                                     "md5": md5(FASTA[g])} for g in GENES},
                    "trabajo": str(trabajo)}, indent=2, ensure_ascii=False),
        encoding="utf-8")

    for f in filas:
        print("%-12s eficientes %3d  tapadas %2d  a=19 %3d  a=20 %3d  a=21 %3d  planilla %3d  %s"
              % (f["nombre"], f["eficientes"], f["tapadas"],
                 f["conteo"]["19"], f["conteo"]["20"], f["conteo"]["21"],
                 f["planilla"], "coincide" if f["reproduce_planilla"] else "NO coincide"))
    print("\n%d de %d genes reproducidos con ancho %d" % (len(ok), len(filas),
                                                          ANCHO_HISTORICO))
    print("TSV por ventana en %s (fuera del repositorio)" % trabajo)
    print("resultados en %s" % SALIDA)
    return 0 if len(ok) == len(filas) else 1


if __name__ == "__main__":
    sys.exit(main())

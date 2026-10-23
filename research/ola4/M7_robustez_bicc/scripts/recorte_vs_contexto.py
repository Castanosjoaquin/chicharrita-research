"""M7 - la cifra que se publica: la molecula recortada, para las tres regiones.

El issue #11 pide reportar el conteo **de la molecula recortada** y no el de la region
dentro del gen: en contexto 922-1221 tiene 36 ventanas eficientes y recortada 26, y es la
recortada la que se sintetizaria. M2 lo remidio para las cuatro regiones vigentes; lo que
falta —y lo que hace falta para que la comparacion del eje 1 sea justa— es el mismo par
para las dos regiones rivales de `BicC_Dm`, 2121-2420 y 264-563.

Cuidado con las dos bases de conteo, que no son la misma. En contexto la region cuenta los
**300 arranques** 922..1221 y da 36; el comparador solo puede mirar los **280 arranques**
que existen de los dos lados, y sobre esos 280 el contexto da 29 y el recorte 26. O sea que
de los 10 que separan 36 de 26, siete son arranques que la molecula no tiene (los ultimos
20 del tramo, que en el gen siguen teniendo 21 nt por delante) y tres son ventanas que
cambian de veredicto al plegarse sola. Las tres cifras valen; lo que no vale es mezclarlas.

Por cada region se comparan dos perfiles de las mismas 280 ventanas: el de la region
dentro del gen de 2.520 nt y el de la molecula de 300 nt plegada sola. La comparacion usa
`comparar_ventanas.py` de M2 (issue #6), que ademas dice **que termino cruzo el corte** en
cada ventana que cambia de clase. Las 20 ultimas posiciones de arranque existen en el gen
y no en la molecula, y se informan como `solo_contexto`.

Dos efectos conocidos se esperan acá, y conviene no confundirlos:

  - borde de plegado: la molecula recortada no tiene el contexto que estabilizaba los
    extremos, asi que la accesibilidad cambia en todo el perfil (C13 §4);
  - borde de dG: en las dos primeras posiciones del recorte el original calcula los
    extremos **sin nucleotidos colgantes**, porque el siRNA de dos posiciones antes no
    existe (`n2 = None if pos <= 2`). Es el artefacto que M2 encontro, y por eso el eje 1
    reporta tambien el recorte sin sus dos primeras posiciones.

Motor ViennaRNA 2.7.2, tabla NN3, punto por defecto, los dos modos. Los TSV por ventana se
escriben fuera del repositorio porque son la entrada del comparador, no un resultado.

Uso (desde la raiz del repositorio):
    python research/ola4/M7_robustez_bicc/scripts/recorte_vs_contexto.py
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve()
RAIZ = AQUI.parents[4]
SALIDA = AQUI.parents[1] / "resultados"
TRABAJO = Path("/tmp/m7_recorte")
sys.path.insert(0, str(RAIZ / "research" / "ola4" / "M2_ventana_a_ventana" / "scripts"))
sys.path.insert(0, str(AQUI.parent))
from comparar_ventanas import comparar, escribir, leer  # noqa: E402
from grilla_parametros import MODOS, REGIONES, leer_fasta  # noqa: E402

GEN = RAIZ / "work" / "W5" / "plfold" / "BicC_Dm.rna.fa"
PORT = RAIZ / "tools" / "sifi21_port" / "run_sifi.py"


def correr(fasta: Path, modo: str, destino: Path) -> None:
    destino.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, str(PORT), str(fasta), "--modo", modo,
                    "--backend", "vienna", "--salida", str(destino)],
                   check=True, capture_output=True, text=True)


def main() -> int:
    SALIDA.mkdir(parents=True, exist_ok=True)
    TRABAJO.mkdir(parents=True, exist_ok=True)
    gen = leer_fasta(GEN)

    # FASTA de cada recorte. Quedan en /tmp: son secuencia del gen y no se versionan.
    fastas = {}
    for nom, (ini, fin) in REGIONES.items():
        f = TRABAJO / ("BicC_%s.fa" % nom.replace("-", "_"))
        f.write_text(">BicC_%s\n%s\n" % (nom.replace("-", "_"), gen[ini - 1:fin]))
        fastas[nom] = f

    resumen = {"motor": "ViennaRNA 2.7.2, tabla NN3, punto por defecto",
               "fuente_del_comparador":
                   "research/ola4/M2_ventana_a_ventana/scripts/comparar_ventanas.py",
               "pares": {}}
    for modo in MODOS:
        dir_gen = TRABAJO / ("gen_%s" % modo)
        correr(GEN, modo, dir_gen)
        tsv_gen = dir_gen / ("BicC_Dm_full_%s_vienna.tsv" % modo)
        a = leer(tsv_gen)
        for nom, (ini, fin) in REGIONES.items():
            dir_rec = TRABAJO / ("rec_%s_%s" % (nom.replace("-", "_"), modo))
            correr(fastas[nom], modo, dir_rec)
            tsv_rec = dir_rec / ("BicC_%s_%s_vienna.tsv" % (nom.replace("-", "_"), modo))
            b = leer(tsv_rec)
            res, cambios = comparar(a, b, offset_b=ini, etiquetas=("contexto", "recorte"))
            prefijo = SALIDA / ("recorte_%s_%s" % (nom.replace("-", "_"), modo))
            escribir(prefijo, res, cambios)
            # Las dos primeras posiciones del recorte son las del artefacto de dG.
            bordes = [c for c in cambios if c["pos_recorte"] in (1, 2)]
            res["cambios_en_las_dos_primeras_posiciones"] = len(bordes)
            resumen["pares"]["%s/%s" % (nom, modo)] = res
            print("%-10s %-10s contexto %3d  recorte %3d  cambian %2d (en las dos primeras: %d)"
                  % (nom, modo, res["eficientes_contexto"], res["eficientes_recorte"],
                     res["cambian"], len(bordes)), flush=True)

    (SALIDA / "recorte_resumen.json").write_text(
        json.dumps(resumen, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

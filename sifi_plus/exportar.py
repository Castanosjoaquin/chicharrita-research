"""Las salidas de datos. Los formatos, no el dibujo.

El informe HTML no se arma aca: lo serializa el navegador desde el SVG que ya esta en
pantalla (`estatico/app.js`). Asi el archivo exportado es exactamente lo que el usuario vio,
y no hay un segundo dibujante que pueda discrepar del primero.

Tres defectos del original que esto corrige:

  1. **No se pueden guardar las secuencias de los siRNA.** El README oficial de si-Fi21 dice,
     textual, que la funcion «no esta implementada» y manda al usuario a buscar un
     `tmpXXXX.json` en `%TEMP%` y parsearlo a mano. Aca salen en FASTA.
  2. **La tabla de resultados nunca se ve**: en el original el numero de eficientes sale solo
     por `Save as -> Table (CSV)`, escribiendo la extension a mano. Aca se ve en pantalla y
     ademas se exporta.
  3. **La exportacion corrompe el nombre del archivo**: `export_table` hace
     `filename += filename + '.csv'`, o sea concatena la ruta consigo misma. Aca el nombre se
     arma con `with_suffix` y se verifica.

Todo se escribe bajo `work/sifi_plus/`, fuera del control de versiones. Las dos salidas que
llevan secuencia —el FASTA de siRNA y el TSV con `--con-seq`— reconstruyen el gen entero,
porque las ventanas se solapan de a 1 nt: fue el incidente de C9 del repositorio. Van con un
encabezado que lo dice.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "tools" / "sifi21_port"))
sys.path.insert(0, str(AQUI))

from sifi_core import COLUMNAS_FEATURES, to_tsv  # noqa: E402

from api import SALIDAS  # noqa: E402

AVISO_SECUENCIA = (
    "# ATENCION: este archivo contiene las secuencias de las ventanas. Como se solapan de a "
    "1 nt,\n# la columna reconstruye el gen entero. No lo versiones ni lo subas a ningun "
    "servicio web.\n# Ver tools/verificacion/sin_secuencias.py y el ADR D54.\n")


def destino(nombre: str, sufijo: str, carpeta="exportado") -> Path:
    """Arma la ruta de salida y crea la carpeta. Nunca concatena la ruta consigo misma.

    La extension se **agrega**, no se reemplaza con `with_suffix`. Toda accesion del NCBI
    lleva un punto (`NC_002786.2`), y `with_suffix` toma todo lo que sigue al ultimo punto
    como extension: `NC_002786.2_ventanas` y `NC_002786.2_features` terminaban los dos en
    `NC_002786.tsv`, uno pisando al otro. Es la misma clase de error que el
    `filename += filename + '.csv'` del original, que es lo que esto venia a corregir.
    """
    d = SALIDAS / carpeta
    d.mkdir(parents=True, exist_ok=True)
    seguro = "".join(c if (c.isalnum() or c in "-_.") else "_" for c in nombre) or "salida"
    return d / (seguro + sufijo)


def tsv_por_ventana(ventanas, nombre: str, *, con_seq=False, solo_features=False) -> Path:
    """Una fila por ventana con todos los terminos del veredicto.

    Es la tabla que el original no muestra ni exporta: lo unico que se puede sacar de si-Fi
    es el total por gen.
    """
    p = destino(nombre + ("_features" if solo_features else "_ventanas"), ".tsv")
    cols = (COLUMNAS_FEATURES + ["is_efficient"]) if solo_features else None
    to_tsv(ventanas, p, con_seq=con_seq, columnas=cols)
    if con_seq:
        p.write_text(AVISO_SECUENCIA + p.read_text(encoding="utf-8"), encoding="utf-8")
    return p


def csv_resumen(resumenes: list[dict], nombre: str) -> Path:
    """El formato exacto del original: punto y coma y tres columnas.

    `Targets;Total siRNA hits;Efficient siRNA hits`. Se conserva para que el investigador
    pueda poner nuestra salida al lado de la suya sin convertir nada.

    Advertencia que va en el propio archivo: la columna del original cuenta **un registro por
    acierto de Bowtie, no una ventana** (`general_helpers.py:113`), asi que un 21-mero
    repetido dentro del gen aporta dos. Nuestra columna cuenta ventanas. Los dos numeros
    coinciden cuando no hay repetidos, y `BicC_Dm` es el caso donde no: 2.504 aciertos sobre
    2.500 ventanas. Para reproducir la regla del original esta
    `research/ola4/M1_conteo_y_referencia/scripts/conteo_por_acierto.py`.
    """
    p = destino(nombre + "_resumen", ".csv")
    with open(p, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["Targets", "Total siRNA hits", "Efficient siRNA hits"])
        for r in resumenes:
            w.writerow([r["nombre"], r["ventanas"], r["eficientes"]])
    return p


def fasta_sirnas(ventanas, nombre: str, *, solo_eficientes=True, rango=None) -> Path:
    """Las secuencias de los siRNA. La funcion que el original declara no implementada.

    El encabezado de cada registro lleva la posicion y el veredicto, para que el archivo sea
    utilizable sin volver a la tabla.
    """
    a, b = rango if rango else (1, 10 ** 9)
    sel = [w for w in ventanas
           if a <= w.pos <= b and (w.is_efficient or not solo_eficientes)]
    etq = "eficientes" if solo_eficientes else "todas"
    p = destino("%s_sirna_%s" % (nombre, etq), ".fasta")
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(AVISO_SECUENCIA)
        for w in sel:
            fh.write(">%s_pos%d %s ddg=%.4f acc=%.6f\n%s\n" % (
                nombre, w.pos, "eficiente" if w.is_efficient else "no_eficiente",
                w.ddg, w.accessibility, w.seq))
    return p

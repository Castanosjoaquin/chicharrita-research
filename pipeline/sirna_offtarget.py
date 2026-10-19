"""Chequeo de off-target por coincidencia exacta de 21-meros contra organismos no objetivo.

Por que exacto y no BLAST: para consultas de 21 nt, BLAST con E-value no sirve. megablast usa
semillas de 28 nt y blastn de 11; hace falta blastn-short con semilla 7, y aun asi el E-value
no es la pregunta correcta. La pregunta correcta es binaria: hay un tramo de 21 nt identico
en el transcriptoma de una especie que no queremos tocar, si o no.

Diseno: el conjunto de candidatos es chico (miles de 21-meros) y los transcriptomas no objetivo
son grandes (cientos de Mb). Entonces se indexan los CANDIDATOS en memoria y se hace streaming
de cada transcriptoma. Memoria constante, una sola pasada por archivo.

Se chequean las dos hebras, porque un siRNA puede silenciar un transcripto de cualquier sentido.

Uso:
    python3 sirna_offtarget.py <candidatos.csv> <no_objetivo_1.fna.gz> [<no_objetivo_2.fna.gz> ...]
"""

from __future__ import annotations

import csv
import gzip
import sys
from collections import defaultdict
from pathlib import Path

K = 21
# Un tramo identico mas corto tambien puede silenciar. La evidencia apunta a 21 nt contiguos
# como riesgo confirmado; entre 15 y 20 conviene tratarlo como alerta, no como descarte.
K_ALERTA = 15
COMPLEMENTO = str.maketrans("ACGTNacgtn", "TGCANtgcan")


def revcomp(s: str) -> str:
    return s.translate(COMPLEMENTO)[::-1]


def clave_de(fila: dict) -> str:
    """Identificador unico de una ventana: locus + posicion + SECUENCIA.

    Tres iteraciones hasta llegar aca, y cada una arreglo un problema real:

    1. `pos` sola: es relativa al CDS de cada gen, asi que dos genes se pisaban y una ventana
       heredaba el riesgo de otra. Descartaba 475 ventanas buenas de 2.750.
    2. `locus|pos`: unica dentro de una corrida, pero **no entre corridas**. Si la cadena cambia
       cuantas ventanas se queda por gen, `L01300|278` ya no es la misma ventana, y el riesgo
       medido sobre una secuencia se atribuye en silencio a otra. Sin error visible.
    3. `locus|pos|sitio`: la secuencia esta en la clave, asi que un desajuste entre corridas
       **no matchea** en vez de matchear mal. Falla ruidosa en vez de silenciosa.
    """
    locus = (fila.get("locus") or "").strip()
    sitio = (fila.get("sitio") or "").strip().upper()
    return f"{locus}|{fila['pos']}|{sitio}"


def cargar_candidatos(ruta: Path) -> dict[str, list[str]]:
    """Mapea cada 21-mero (y su reverso complementario) a las ventanas que lo usan."""
    indice: dict[str, list[str]] = defaultdict(list)
    with ruta.open(encoding="utf-8") as fh:
        for fila in csv.DictReader(fh):
            if fila.get("descarte"):
                continue
            sitio = fila["sitio"].upper()
            clave = clave_de(fila)
            indice[sitio].append(clave)
            indice[revcomp(sitio)].append(clave)
    return indice


def semillas_alerta(indice: dict[str, list[str]]) -> dict[str, set[str]]:
    """Sub-tramos de K_ALERTA nt de cada candidato, para la zona gris."""
    semillas: dict[str, set[str]] = defaultdict(set)
    for kmero, claves in indice.items():
        for i in range(len(kmero) - K_ALERTA + 1):
            semillas[kmero[i:i + K_ALERTA]].update(claves)
    return semillas


def recorrer(ruta: Path):
    """Itera (nombre, secuencia) de un FASTA, con o sin gzip."""
    abrir = gzip.open if ruta.suffix == ".gz" else open
    nombre, trozos = None, []
    with abrir(ruta, "rt") as fh:
        for linea in fh:
            if linea.startswith(">"):
                if nombre:
                    yield nombre, "".join(trozos).upper()
                nombre, trozos = linea[1:].split()[0], []
            else:
                trozos.append(linea.strip())
    if nombre:
        yield nombre, "".join(trozos).upper()


def escanear(ruta: Path, exactos: dict[str, list[str]], semillas: dict[str, set[str]],
             secuencias: dict[str, list[str]], peor: dict[str, int]) -> dict:
    """Una pasada. Para cada candidato guarda el tramo identico MAS LARGO que encontro.

    Guardar el maximo, y no un si/no contra un umbral fijo, es lo que despues permite
    dibujar la curva de cuantos candidatos sobreviven a cada umbral posible.
    """
    golpes_exactos: dict[str, set[str]] = defaultdict(set)
    transcriptos = bases = 0

    for nombre, seq in recorrer(ruta):
        transcriptos += 1
        bases += len(seq)
        for i in range(len(seq) - K_ALERTA + 1):
            semilla = seq[i:i + K_ALERTA]
            candidatos = semillas.get(semilla)
            if not candidatos:
                continue
            for p in candidatos:
                mejor = K_ALERTA
                for variante in secuencias[p]:
                    j = variante.find(semilla)
                    if j < 0:
                        continue
                    largo = K_ALERTA
                    while (j + largo < len(variante) and i + largo < len(seq)
                           and variante[j + largo] == seq[i + largo]):
                        largo += 1
                    mejor = max(mejor, largo)
                if mejor > peor.get(p, 0):
                    peor[p] = mejor
                if mejor >= K:
                    golpes_exactos[p].add(nombre)

    return {"archivo": ruta.name, "transcriptos": transcriptos, "bases": bases,
            "exactos": golpes_exactos}


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    candidatos = Path(sys.argv[1])
    exactos = cargar_candidatos(candidatos)
    semillas = semillas_alerta(exactos)
    # El denominador son las VENTANAS distintas, no los sitios: con varios genes, dos ventanas
    # pueden compartir secuencia y antes eso descuadraba los porcentajes de la curva.
    distintos = len({c for claves in exactos.values() for c in claves})
    print(f"candidatos: {distintos} ventanas distintas · {len(semillas)} semillas de {K_ALERTA} nt")

    secuencias: dict[str, list[str]] = defaultdict(list)
    for kmero, claves in exactos.items():
        for c in claves:
            secuencias[c].append(kmero)

    peor: dict[str, int] = {}
    total_exactos: set[str] = set()
    for arg in sys.argv[2:]:
        ruta = Path(arg)
        if not ruta.exists():
            print(f"  falta {ruta}, lo salteo")
            continue
        r = escanear(ruta, exactos, semillas, secuencias, peor)
        total_exactos |= set(r["exactos"])
        print(f"\n{r['archivo']}: {r['transcriptos']:,} transcriptos, {r['bases']:,} nt")
        print(f"  candidatos con coincidencia exacta de {K} nt: {len(r['exactos'])}")
        for pos, nombres in sorted(r["exactos"].items())[:5]:
            print(f"    pos {pos}: {len(nombres)} transcripto(s), ej. {sorted(nombres)[0]}")

    print(f"\nCurva de umbral: cuantos candidatos sobreviven segun donde se corte")
    print(f"{'umbral':>8}{'descartados':>14}{'sobreviven':>13}{'% del espacio':>15}")
    for umbral in range(K_ALERTA, K + 1):
        caen = sum(1 for v in peor.values() if v >= umbral)
        viven = distintos - caen
        print(f"{umbral:>5} nt{caen:>14}{viven:>13}{viven / distintos * 100:>14.1f}%")
    print("\nLa evidencia publicada pone el riesgo confirmado en 21 nt contiguos, con reportes")
    print("de actividad desde 15. El corte correcto esta adentro de esa curva, y lo tiene que")
    print("poner alguien que sepa biologia: nosotros mostramos la curva, no elegimos el numero.")


if __name__ == "__main__":
    main()

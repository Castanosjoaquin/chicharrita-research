"""Cuanta lista de no objetivo hace falta de verdad, y que sobrevive a nivel GEN.

Tres preguntas que no contestaba el reporte por ventana:

  1. **A nivel gen**: de los 438 genes, cuantos conservan al menos una ventana
     limpia? Esa es la pregunta de decision. Perder 7.000 ventanas no importa si
     cada gen conserva alguna; perder un gen entero si.

  2. **Cobertura**: si *Macrosteles* sola explica la mayoria de los descartes,
     cuantas especies hacen falta para encontrar casi todos? Si bastan cuatro, el
     chequeo se puede correr en minutos en vez de horas, y eso es una
     recomendacion practica, no una curiosidad.

  3. **La curva de umbral** de las tres listas, una al lado de la otra.

No reescanea nada: cruza los CSV que ya produjeron las tres corridas.

Uso:
    python3 no_objetivo_cobertura.py
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

SALIDA = Path(__file__).parent / "salida"
K = 21          # descarte: tramo identico de 21 nt
K_ALERTA = 15   # piso de la zona gris
UMBRAL_OK = 17  # por encima de esto la ventana no es "ok"

# (nombre, archivo, columna, cuanto cuesta correrlo)
JUEGOS = [
    ("maiz + abeja (2 sp)", "sirna_no_objetivo_ampliado.csv", "off_target_previo",
     "0,26 Gnt"),
    ("solo hemipteros (4 sp)", "sirna_cercanos.csv", "off_target_ampliado",
     "0,37 Gnt"),
    ("catalogo completo (25 sp)", "sirna_no_objetivo_ampliado.csv", "off_target_ampliado",
     "3,86 Gnt"),
]


def clave(fila: dict) -> str:
    """locus|pos|sitio. La secuencia va adentro a proposito.

    En estos CSV `locus|pos` ya es unica (verificado: 0 colisiones en 10.950
    ventanas), porque `pos` es la posicion dentro del CDS de ese gen y cada locus
    aparece una sola vez. Igual se usa la clave de tres partes para que sea la
    misma que usa el resto del pipeline: si dos corridas distintas enumeraran el
    mismo locus con otro CDS, `pos` sola podria apuntar a secuencias distintas y
    el cruce entre archivos seria silenciosamente incorrecto.
    """
    return f"{fila['locus']}|{fila['pos']}|{fila['sitio']}"


def numero(v) -> int:
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return 0


def cargar(archivo: str, columna: str) -> dict[str, int]:
    valores: dict[str, int] = {}
    with (SALIDA / archivo).open(encoding="utf-8") as fh:
        for fila in csv.DictReader(fh):
            valores[clave(fila)] = numero(fila.get(columna))
    return valores


def genes_de(archivo: str) -> dict[str, str]:
    """clave de ventana -> locus, y locus -> nombre de gen."""
    de_ventana: dict[str, str] = {}
    nombre: dict[str, str] = {}
    with (SALIDA / archivo).open(encoding="utf-8") as fh:
        for fila in csv.DictReader(fh):
            de_ventana[clave(fila)] = fila["locus"]
            nombre[fila["locus"]] = fila.get("gen_drosophila") or fila.get("tribolium") or ""
    return de_ventana, nombre


def main() -> None:
    de_ventana, nombre_gen = genes_de("sirna_no_objetivo_ampliado.csv")
    por_gen: dict[str, list[str]] = defaultdict(list)
    for k, locus in de_ventana.items():
        por_gen[locus].append(k)

    juegos = {}
    for nombre, archivo, columna, costo in JUEGOS:
        if not (SALIDA / archivo).exists():
            print(f"[falta {archivo}, salteo '{nombre}']")
            continue
        juegos[nombre] = (cargar(archivo, columna), costo)

    print(f"ventanas: {len(de_ventana)}  ·  genes: {len(por_gen)}")

    # ------------------------------------------------------------------
    print("\n" + "=" * 78)
    print("SUPERVIVENCIA, POR VENTANA Y POR GEN")
    print("=" * 78)
    print(f"{'lista de no objetivo':<28}{'costo':>9}{'ventanas ok':>13}"
          f"{'genes con >=1 ok':>19}{'genes sin salida':>18}")
    resumen = {}
    for nombre, (valores, costo) in juegos.items():
        ok = {k for k, v in valores.items() if v < UMBRAL_OK}
        genes_ok = sum(1 for g, ks in por_gen.items() if any(k in ok for k in ks))
        sin_salida = [g for g, ks in por_gen.items() if not any(k in ok for k in ks)]
        resumen[nombre] = {"ok": ok, "genes_ok": genes_ok, "sin_salida": sin_salida,
                           "valores": valores}
        print(f"{nombre:<28}{costo:>9}{len(ok):>8} ({len(ok)/len(de_ventana)*100:>4.1f}%)"
              f"{genes_ok:>12} ({genes_ok/len(por_gen)*100:>4.1f}%)"
              f"{len(sin_salida):>18}")

    completo = "catalogo completo (25 sp)"
    if completo in resumen:
        sin = resumen[completo]["sin_salida"]
        if sin:
            print(f"\nLos {len(sin)} genes que pierden TODAS sus ventanas limpias "
                  f"con el catalogo completo:")
            for g in sorted(sin):
                n = len(por_gen[g])
                peor = max(resumen[completo]["valores"].get(k, 0) for k in por_gen[g])
                print(f"  {g}  {nombre_gen.get(g, ''):<14}{n:>4} ventanas, "
                      f"la mejor con {peor} nt identicos")

    # ------------------------------------------------------------------
    print("\n" + "=" * 78)
    print("COBERTURA: ALCANZA CON POCAS ESPECIES BIEN ELEGIDAS?")
    print("=" * 78)
    if completo in juegos and "solo hemipteros (4 sp)" in juegos:
        full = juegos[completo][0]
        descartes_full = {k for k, v in full.items() if v >= K}
        riesgo_full = {k for k, v in full.items() if v >= UMBRAL_OK}
        print(f"referencia (25 especies): {len(descartes_full)} descartes, "
              f"{len(riesgo_full)} ventanas con riesgo >= {UMBRAL_OK} nt")
        print()
        print(f"{'subconjunto':<28}{'costo':>9}{'descartes que encuentra':>26}"
              f"{'riesgo que encuentra':>23}")
        for nombre, (valores, costo) in juegos.items():
            if nombre == completo:
                continue
            d = {k for k, v in valores.items() if v >= K} & descartes_full
            r = {k for k, v in valores.items() if v >= UMBRAL_OK} & riesgo_full
            print(f"{nombre:<28}{costo:>9}"
                  f"{len(d):>11} de {len(descartes_full)} ({len(d)/max(len(descartes_full),1)*100:>5.1f}%)"
                  f"{len(r):>10} de {len(riesgo_full)} ({len(r)/max(len(riesgo_full),1)*100:>5.1f}%)")

        # Los genomas crudos de los enemigos naturales, aparte: miden distinto.
        ruta_en = SALIDA / "sirna_enemigos_naturales.csv"
        if ruta_en.exists():
            en = cargar("sirna_enemigos_naturales.csv", "off_target_genomas")
            d = {k for k, v in en.items() if v >= K}
            nuevos = d - descartes_full
            print(f"\n3 genomas crudos de enemigos naturales (1,45 Gnt), reportados aparte")
            print(f"  porque miden sobre genoma completo y no sobre transcriptoma:")
            print(f"  {len(d)} descartes, de los cuales {len(nuevos)} NO los encuentra")
            print(f"  ninguna de las 25 especies con transcriptoma.")

    # ------------------------------------------------------------------
    print("\n" + "=" * 78)
    print("CURVA DE UMBRAL: CUANTAS VENTANAS SOBREVIVEN SEGUN DONDE SE CORTE")
    print("=" * 78)
    nombres = list(juegos)
    print(f"{'umbral':>8}" + "".join(f"{n[:24]:>26}" for n in nombres))
    total = len(de_ventana)
    for umbral in range(K_ALERTA, K + 1):
        fila = f"{umbral:>5} nt"
        for n in nombres:
            valores = juegos[n][0]
            viven = sum(1 for v in valores.values() if v < umbral)
            fila += f"{viven:>14} ({viven/total*100:>5.1f}%)"
        print(fila)

    print("\nLa evidencia publicada pone el riesgo confirmado en 21 nt contiguos, con reportes")
    print("de actividad desde 15. Nosotros mostramos la curva; el numero lo pone un biologo.")


if __name__ == "__main__":
    main()

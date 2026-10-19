"""Selecciona candidatos segun el OBJETIVO de control, no segun un unico supuesto.

Por que existe: nuestro primer ranking tenia "que mate" cableado. La validacion retrospectiva
mostro el costo de eso. El grupo de Catalano eligio `BicC` a proposito por dar un fenotipo
**visible no letal** &mdash; esterilidad &mdash; para bajar la tasa de crecimiento poblacional
en vez de matar. Nuestro ranking lo descartaba, y no por error de calculo: por tener un solo
objetivo escondido en el codigo.

Matar no es la unica estrategia de control, y para cada estrategia los buenos blancos son otros:

  letal        matar al insecto. Efecto rapido, presion de seleccion alta.
  esteril      cortar la reproduccion. Efecto mas lento pero sostenido, y es lo que eligieron
               los autores del unico paper argentino sobre la especie.
  morfologico  incapacitar (alas, movilidad). Baja la capacidad de transmitir sin matar.
  cualquiera   cualquier fenotipo distinto de normal.

Uso:
    python3 objetivo_candidatos.py <objetivo> [--n 500] [--csv salida.csv]
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

SALIDA = Path(__file__).parent / "salida"
TABLA = SALIDA / "tabla_unificada.csv"

OBJETIVOS = {
    "letal": ["n_letal", "n_letal_embrionario"],
    "esteril": ["n_esteril"],
    "morfologico": ["n_morfologico"],
    "cualquiera": ["n_letal", "n_letal_embrionario", "n_esteril", "n_morfologico", "n_otro"],
}

# La evidencia no vale lo mismo segun de que tan lejos venga el fenotipo. La distancia la trae
# la tabla (2 = misma clase otro orden, 1 = mismo orden, 0 = misma familia).
PESO_DISTANCIA = {"0": 1.0, "1": 0.85, "2": 0.6, "3": 0.4}
PESO_EVIDENCIA = {"alto": 1.0, "medio": 0.7, "bajo": 0.45}


def numero(valor: str | None, por_defecto: float = 0.0) -> float:
    try:
        return float(valor)
    except (TypeError, ValueError):
        return por_defecto


def calidad_alineamiento(fila: dict) -> float:
    """Que tan confiable es que ese locus sea realmente ese gen.

    OJO con el sesgo que esto introduce, que descubrimos validando: un frameshift o un stop
    interno en un alineamiento entre ordenes distintos de insectos es **esperable** cuando el
    gen evoluciona rapido, y no quiere decir que la asignacion sea incorrecta. Penalizarlos
    fuerte expulsa justamente a los genes regulatorios de evolucion rapida &mdash; que son los
    blancos especificos de reproduccion y desarrollo &mdash; y deja solo ribosomales y factores
    de traduccion, que se alinean facil porque casi no cambiaron.

    Caso concreto: `BicC`, el blanco que el grupo de Catalano valido experimentalmente en la
    chicharrita, quedaba en 0,292 contra un umbral de 0,30. Afuera por un pelo, y por la razon
    equivocada.

    Entonces: penalizaciones suaves, y el numero de hits (que si habla de parálogos reales)
    pesa mas que los artefactos de alineamiento.
    """
    mejor = max(numero(fila.get(f"{p}_identidad")) for p in ("tcas", "dmel", "nlug"))
    limpio = 1.0
    for prefijo in ("tcas", "dmel", "nlug"):
        if numero(fila.get(f"{prefijo}_identidad")) <= 0:
            continue
        if numero(fila.get(f"{prefijo}_frameshift")) > 0:
            limpio -= 0.05
        if numero(fila.get(f"{prefijo}_stop_interno")) > 0:
            limpio -= 0.05
        # Mas de un hit de la misma proteina = parálogos o duplicacion: eso si es senal real
        if numero(fila.get(f"{prefijo}_n_hits_de_esa_proteina"), 1) > 1:
            limpio -= 0.12
    return mejor * max(limpio, 0.4)


CONFIANZA_MINIMA = 0.30


def puntuar(fila: dict, objetivo: str) -> float:
    """Que tan bueno es el blanco PARA ESTE OBJETIVO.

    Decision de diseno, corregida despues de validar: la calidad del alineamiento **no entra
    en el score**. Esa calidad mide cuanta confianza tenemos en que el locus sea realmente ese
    gen; no mide si el gen sirve como blanco. Mezclarlas premia a los genes mas conservados
    (ribosomales, factores de traduccion) por el solo hecho de ser faciles de alinear, y
    entierra a genes regulatorios de evolucion rapida que son justamente los blancos
    especificos de reproduccion.

    La confianza ahora **filtra** (ver CONFIANZA_MINIMA) y se reporta aparte, pero no ordena.
    """
    columnas = OBJETIVOS[objetivo]
    a_favor = sum(numero(fila.get(c)) for c in columnas)
    if a_favor == 0 or calidad_alineamiento(fila) < CONFIANZA_MINIMA:
        return 0.0
    otras = sum(numero(fila.get(c)) for c in ("n_letal", "n_letal_embrionario", "n_esteril",
                                              "n_morfologico", "n_otro") if c not in columnas)
    total = a_favor + numero(fila.get("n_normal")) + otras
    consistencia = a_favor / total if total else 0.0
    # Un solo reporte a favor vale menos que tres que coinciden
    volumen = min(a_favor / 3.0, 1.0)
    distancia = PESO_DISTANCIA.get(str(fila.get("fenotipo_distancia", "")).strip(), 0.5)
    evidencia = PESO_EVIDENCIA.get((fila.get("nivel_evidencia") or "").strip(), 0.5)
    penetrancia = numero(fila.get("penetrancia_max_letal")) if objetivo == "letal" else 0.5

    return round(
        0.40 * consistencia
        + 0.25 * volumen
        + 0.18 * distancia
        + 0.12 * evidencia
        + 0.05 * min(penetrancia, 1.0), 4)


def main() -> None:
    objetivo = sys.argv[1] if len(sys.argv) > 1 else "letal"
    if objetivo not in OBJETIVOS:
        sys.exit(f"objetivo debe ser uno de: {', '.join(OBJETIVOS)}")
    tope = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 500

    filas = list(csv.DictReader(TABLA.open(encoding="utf-8")))
    for f in filas:
        f["score_objetivo"] = puntuar(f, objetivo)
    elegidos = sorted((f for f in filas if f["score_objetivo"] > 0),
                      key=lambda f: -f["score_objetivo"])[:tope]

    print(f"objetivo: {objetivo}  ·  loci en la tabla: {len(filas)}  ·  con evidencia a favor: "
          f"{sum(1 for f in filas if f['score_objetivo'] > 0)}")
    print(f"\n{'#':>4}  {'locus':<9}{'gen':<14}{'score':>7}{'categoria':>14}{'dist':>6}{'evid':>8}")
    for i, f in enumerate(elegidos[:15], start=1):
        gen = (f.get("gen_drosophila") or f.get("mejor_hit_tribolium") or "")[:13]
        print(f"{i:>4}  {f['locus']:<9}{gen:<14}{f['score_objetivo']:>7.3f}"
              f"{(f.get('fenotipo_categoria') or '')[:13]:>14}"
              f"{str(f.get('fenotipo_distancia') or '-'):>6}"
              f"{(f.get('nivel_evidencia') or '-'):>8}")

    # Donde cae cada blanco publicado, para no perder de vista la validacion
    publicados = {"Vha55": "V-ATPase B (Texas A&M)", "Vha36-1": "V-ATPase D (Texas A&M)",
                  "BicC": "Bicaudal C (Catalano)"}
    print(f"\nblancos publicados en este ranking de {objetivo}:")
    for i, f in enumerate(elegidos, start=1):
        gen = f.get("gen_drosophila")
        if gen in publicados:
            print(f"  puesto {i:>4} de {len(elegidos)}  {gen:<10} {publicados[gen]}")
    faltan = [g for g in publicados if not any(f.get("gen_drosophila") == g for f in elegidos)]
    for g in faltan:
        print(f"  {'fuera del tope':>14}  {g:<10} {publicados[g]}")

    if "--csv" in sys.argv:
        destino = Path(sys.argv[sys.argv.index("--csv") + 1])
        with destino.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(elegidos[0].keys()))
            w.writeheader()
            w.writerows(elegidos)
        print(f"\ncsv en {destino}")


if __name__ == "__main__":
    main()

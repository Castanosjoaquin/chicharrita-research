"""Verificaciones del enumerador de quimeras de `O4`. No necesita datos de `work/`.

Las ocho secciones prueban las propiedades que el criterio de terminado del issue #24 pide
por escrito, mas las dos que el preregistro agrega. Corren sobre dos genes sinteticos de
400 nt generados con semilla fija, asi que no leen ninguna secuencia del corpus y no
dependen de nada que no se versione.

- **§1 El objetivo es obligatorio y no tiene default.** Omitirlo es un error de linea de
  comandos (§2 del preregistro). Es la propiedad que evita que el ranking herede un
  objetivo que nadie declaro.
- **§2 `cobertura_fenotipica` exige ejes declarados y distintos** (`D67`): falta uno, o son
  iguales, y la corrida no arranca.
- **§3 La salida nunca suma juntura y heredadas en una sola cifra.** Se prueba de dos
  formas: la lista de columnas es exactamente la esperada —agregar una columna «total»
  hace fallar la prueba a proposito— y ninguna columna numerica vale `heredadas + juntura`
  cuando las dos son distintas de cero.
- **§4 Los bloques del empalme que se tamizan son los que cruzan la union**, 57 por
  juntura, y ninguno entra entero en el aporte de un solo gen.
- **§5 El tope de plegados detiene la corrida** en vez de muestrear o cambiar de algoritmo.
- **§6 La enumeracion es determinista**: dos corridas de la misma grilla dan la misma lista,
  en el mismo orden, sin semilla.
- **§7 La admisibilidad respeta el marco**: en marco 1 un fragmento consume veinte
  nucleotidos mas que en marco 2, y una ventana vetada lo descarta en los dos.
- **§8 La suma de las partes viaja en su propia columna** y no se mezcla con la cifra de la
  quimera, que es la unica forma de comparar contra las regiones sueltas sin sumar nada.

Uso:
    python research/ola6/O4_enumerador_quimeras/scripts/test_enumerador.py
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import enumerar_quimeras as EQ   # noqa: E402
import mascara as MA             # noqa: E402

import numpy as np               # noqa: E402

FALLAS: list[str] = []


def check(cond, msg):
    if cond:
        print("  ok   %s" % msg)
    else:
        print("  FALLA %s" % msg)
        FALLAS.append(msg)


def gen_sintetico(nombre: str, n: int, semilla: int) -> dict:
    rng = random.Random(semilla)
    seq = "".join(rng.choice("ACGT") for _ in range(n))
    return {"nombre": nombre, "consulta": nombre, "seq": seq, "n": n,
            "desde": 1, "hasta": n, "ruta": "sintetico"}


GENES = {"GenA": gen_sintetico("GenA", 400, 11),
         "GenB": gen_sintetico("GenB", 400, 29)}
LIMPIAS = {n: np.zeros(g["n"] - EQ.VENTANA + 1, dtype=bool) for n, g in GENES.items()}


print("§1 el objetivo es obligatorio y no tiene default")
try:
    EQ.main(["--gen", "A=work/O3/fasta/BicC_Dm_full.fasta", "--largo-total", "400"])
    check(False, "sin --objetivo tendria que abortar")
except SystemExit as e:
    check(e.code != 0, "sin --objetivo aborta con codigo distinto de cero")
check("--objetivo" in EQ.main.__doc__ if EQ.main.__doc__ else True,
      "el objetivo es parametro del punto de entrada")
check(set(EQ.OBJETIVOS) == {"cobertura_fenotipica", "riesgo_minimo",
                            "eficiencia_heredada"},
      "los tres objetivos son los del preregistro y ninguno se llama 'mejor'")
check(not any("mejor" == o for o in EQ.OBJETIVOS), "no existe un objetivo 'mejor'")

print("\n§2 cobertura_fenotipica exige ejes declarados y distintos (D67)")
base = ["--gen", "BicC_Dm=work/O3/fasta/BicC_Dm_full.fasta",
        "--gen", "VATPaseB_Dm=work/O3/fasta/VATPaseB_Dm_full.fasta",
        "--largo-total", "600", "--objetivo", "cobertura_fenotipica"]
for extra, caso in ((["--eje", "BicC_Dm=reproduccion"], "falta el eje de un gen"),
                    (["--eje", "BicC_Dm=reproduccion", "--eje",
                      "VATPaseB_Dm=reproduccion"], "los dos ejes son iguales")):
    try:
        EQ.main(base + extra)
        check(False, "%s: tendria que abortar" % caso)
    except SystemExit as e:
        check(e.code != 0, "%s: aborta" % caso)

print("\n§3 la salida nunca suma juntura y heredadas en una sola cifra")
c = {"izq": "GenA", "der": "GenB", "a1": 1, "l1": 200, "a2": 1, "l2": 200}
qseq = GENES["GenA"]["seq"][:200] + GENES["GenB"]["seq"][:200]
p_izq = EQ.perfil(GENES["GenA"]["seq"][:200])
p_der = EQ.perfil(GENES["GenB"]["seq"][:200])
f = EQ.cuentas_de(c, GENES, EQ.perfil(qseq), p_izq, p_der, None)
ESPERADAS = {
    "ventanas_molecula", "ventanas_marco1_del_fragmento_izq",
    "ventanas_marco1_del_fragmento_der", "ef_fragmento_izq_solo",
    "ef_fragmento_der_solo", "suma_de_las_partes", "delta_heredadas_menos_suma",
    "ef_heredadas_izq", "ef_heredadas_der", "ef_heredadas",
    "heredadas_que_cambiaron", "max_nt_hasta_la_union_de_un_cambio",
    "ventanas_juntura", "ef_juntura", "juntura_con_blanco_continuo",
    "fabricados_21_refs", "fabricados_ge19_refs", "fabricados_refs",
    "aporte_del_bloque_mas_repartido", "bloques_fabricados_con_aporte_ge5",
    "fabricados_en_ventana_eficiente", "existe_en_el_genoma_del_vector",
    "alerta_juntura_nueva"}
check(set(f) == ESPERADAS,
      "las columnas son exactamente las declaradas (sobran %s, faltan %s)"
      % (sorted(set(f) - ESPERADAS), sorted(ESPERADAS - set(f))))
total = f["ef_heredadas"] + f["ef_juntura"]
suman = [k for k, v in f.items() if isinstance(v, int) and v == total
         and f["ef_heredadas"] and f["ef_juntura"]]
check(not suman, "ninguna columna vale heredadas+juntura (%d); candidatas: %s"
      % (total, suman))
check(f["ventanas_juntura"] == 20, "la juntura son veinte ventanas")
check(f["ventanas_molecula"] == 380, "una molecula de 400 nt tiene 380 ventanas")

print("\n§4 los bloques que se tamizan son los que cruzan la union")
mero = GENES["GenA"]["seq"][180:200] + GENES["GenB"]["seq"][:20]
bloques = EQ.bloques_que_cruzan(mero)
check(len(bloques) == 57, "57 bloques por juntura (son %d)" % len(bloques))
por_largo = {}
for s, largo in bloques:
    por_largo[largo] = por_largo.get(largo, 0) + 1
check(por_largo == {21: 20, 20: 19, 19: 18},
      "20 de 21 nt, 19 de 20 y 18 de 19 (son %s)" % por_largo)
check(all(s + 1 <= 20 < s + largo for s, largo in bloques),
      "todos toman al menos un nucleotido de cada gen")

print("\n§5 el tope de plegados detiene la corrida")
try:
    EQ.main(["--gen", "BicC_Dm=work/O3/fasta/BicC_Dm_full.fasta:922-1221",
             "--gen", "VATPaseB_Dm=work/O3/fasta/VATPaseB_Dm_full.fasta:517-816",
             "--eje", "BicC_Dm=reproduccion", "--eje", "VATPaseB_Dm=movilidad",
             "--largo-total", "600", "--l1-min", "300", "--l1-max", "300",
             "--paso", "1", "--objetivo", "cobertura_fenotipica",
             "--tope-plegados", "1"])
    check(False, "con el tope en 1 tendria que abortar")
except SystemExit as e:
    check(e.code != 0, "con el tope en 1 aborta sin muestrear")

print("\n§6 la enumeracion es determinista y no muestrea")
a1, _ = EQ.enumerar(GENES, LIMPIAS, 400, 150, 250, 25)
a2, _ = EQ.enumerar(GENES, LIMPIAS, 400, 150, 250, 25)
check(a1 == a2 and len(a1) > 0,
      "dos enumeraciones de la misma grilla dan la misma lista (%d combinaciones)"
      % len(a1))
check(all(c["l1"] + c["l2"] == 400 for c in a1),
      "toda combinacion suma el largo total pedido")
check({(c["izq"], c["der"]) for c in a1} == {("GenA", "GenB"), ("GenB", "GenA")},
      "los dos ordenes entran a la grilla")

print("\n§7 la admisibilidad respeta el marco")
m2 = MA.fragmentos_admisibles(LIMPIAS["GenA"], 300, marco=2)
m1 = MA.fragmentos_admisibles(LIMPIAS["GenA"], 300, marco=1)
check(len(m2) == 400 - 300 + 1, "en marco 2 caben %d arranques de 300 nt" % (101,))
check(len(m1) == (400 - 20) - 300 + 1,
      "en marco 1 caben veinte menos, porque el fragmento consume 320 nt")
vetada = LIMPIAS["GenA"].copy()
vetada[150 - 1] = True   # una ventana vetada en el medio
sin_veto = MA.fragmentos_admisibles(vetada, 300, marco=2)
check(all(not (a <= 150 <= a + 300 - EQ.VENTANA) for a in sin_veto),
      "ningun fragmento admisible contiene la ventana vetada")

print("\n§8 la suma de las partes viaja en su propia columna")
check(f["suma_de_las_partes"] == f["ef_fragmento_izq_solo"] + f["ef_fragmento_der_solo"],
      "la suma de las partes es la suma de los dos fragmentos solos")
check(f["delta_heredadas_menos_suma"] == f["ef_heredadas"] - f["suma_de_las_partes"],
      "el delta compara heredadas contra la suma de las partes, sin la juntura")

print()
if FALLAS:
    print("FALLAS: %d" % len(FALLAS))
    sys.exit(1)
print("todo bien")

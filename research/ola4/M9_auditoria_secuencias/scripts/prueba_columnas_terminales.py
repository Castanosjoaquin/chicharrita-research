"""Mide si las columnas `nt19` y `nt2` que propone M3 (#7) reconstruyen el gen.

El issue #7 afirma que «son dos letras y un entero: no reconstruyen secuencia, asi que no
chocan con la regla de confidencialidad». Como las ventanas del port se solapan de a 1 nt,
la columna de un nucleotido fijo de la ventana, concatenada en orden, es una subcadena
literal del gen. Esto lo mide sobre un gen sintetico, asi que no usa ningun dato real.

    python3 research/ola4/M9_auditoria_secuencias/scripts/prueba_columnas_terminales.py
"""
import random

random.seed(11)
LARGO_GEN = 500
VENTANA = 21

gen = "".join(random.choice("ACGT") for _ in range(LARGO_GEN))
ventanas = [gen[i : i + VENTANA] for i in range(len(gen) - VENTANA + 1)]

# Posiciones de la regla terminal de si-Fi21, en base 1: 19 y 2.
columnas = {"nt19": "".join(v[18] for v in ventanas), "nt2": "".join(v[1] for v in ventanas)}

print(f"gen sintetico de {len(gen)} nt, {len(ventanas)} ventanas de {VENTANA} nt")
cubierto: set[int] = set()
for nombre, col in columnas.items():
    off = gen.find(col)
    print(f"  columna {nombre}: {len(col)} nt concatenados, subcadena del gen: {col in gen}, desplazamiento {off}")
    assert col in gen, f"{nombre} deberia ser subcadena literal del gen"
    cubierto |= set(range(off, off + len(col)))

print(f"  nt del gen reconstruibles con las dos columnas: {len(cubierto)} de {len(gen)}"
      f" ({100 * len(cubierto) / len(gen):.1f} %)")

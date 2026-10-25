"""Casos sinteticos del detector de `tools/verificacion/sin_secuencias.py`.

Reproduce el incidente de C9 y sus variantes, y dos controles negativos. Ningun dato real:
el gen es sintetico. Lo que verifica es que la pasada 2 atrape lo que la pasada 1 no ve
—k-meros de menos de 21 nt y columnas antisentido— y que no invente hallazgos donde no los
hay.

    python3 research/ola4/M9_auditoria_secuencias/scripts/prueba_detector.py
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3].parent / "tools" / "verificacion"))
import sin_secuencias as S  # noqa: E402

random.seed(7)
gen = "".join(random.choice("ACGT") for _ in range(300))
rc = lambda s: s.translate(str.maketrans("ACGT", "TGCA"))[::-1]  # noqa: E731

casos = {
    "C9: columna seq de 21-meros": ("x.tsv", "pos\tseq\tefi\n" + "\n".join(f"{i}\t{gen[i:i+21]}\t1" for i in range(60)), 60, 1),
    "dos columnas (sitio y guia)": ("x.tsv", "pos\tsitio\tguia\n" + "\n".join(f"{i}\t{gen[i:i+21]}\t{rc(gen[i:i+21])}" for i in range(60)), 120, 2),
    "solo columna antisentido": ("x.csv", "code,antisense\n" + "\n".join(f"w{i},{rc(gen[i:i+21])}" for i in range(60)), 60, 1),
    "15-meros solapados (sin rachas)": ("x.tsv", "pos\tseq\n" + "\n".join(f"{i}\t{gen[i:i+15]}" for i in range(60)), 0, 1),
    "NEGATIVO: 15-meros al azar": ("x.tsv", "pos\tseq\n" + "\n".join(f"{i}\t{''.join(random.choice('ACGT') for _ in range(15))}" for i in range(60)), 0, 0),
    "NEGATIVO: sin columna de secuencia": ("x.tsv", "pos\tddg\tacc\n" + "\n".join(f"{i}\t1.23\t0.089" for i in range(60)), 0, 0),
}

fallas = 0
for nombre, (ruta, txt, n_rachas, n_cadenas) in casos.items():
    r = S.buscar_rachas(txt, ruta)
    k = S.buscar_kmeros_solapados(txt, ruta)
    ok = len(r) == n_rachas and len(k) == n_cadenas
    fallas += not ok
    detalle = "; ".join(
        f"{h['n_kmeros']}x{h['largo_kmero']}->{h['nt_reconstruidos']}nt{' antisentido' if h.get('sentido') else ''}"
        for h in k
    )
    print(f"{'ok ' if ok else 'FALLA'} {nombre:34s} rachas={len(r):3d} cadenas={len(k)}  {detalle}")

print("falsos positivos de base64:",
      len(S.buscar_rachas('src:url(data:font/woff2;base64,d09GMgABAAAAAFY4' + gen[:40] + 'YagSwbga9OHIEO)', 'x.html')))

# «No pude mirar» no es «mire y no encontre»: el gancho rechaza en los dos casos, pero el
# mensaje tiene que distinguirlos, y para eso necesita saber por que no corrio la pasada.
import tempfile  # noqa: E402

with tempfile.TemporaryDirectory() as tmp:
    vacia = Path(tmp)
    motivo = S.motivo_sin_epilab(vacia)
    ok = motivo is not None and "no esta en disco" in motivo
    fallas += not ok
    print(f"{'ok ' if ok else 'FALLA'} {'planilla ausente':34s} motivo={motivo!r}")

    (vacia / S.RUTA_EPILAB).parent.mkdir(parents=True, exist_ok=True)
    (vacia / S.RUTA_EPILAB).touch()
    motivo = S.motivo_sin_epilab(vacia)
    try:
        import openpyxl  # noqa: F401
        esperado = motivo is None
    except ImportError:
        esperado = motivo is not None and "openpyxl" in motivo
    fallas += not esperado
    print(f"{'ok ' if esperado else 'FALLA'} {'planilla presente':34s} motivo={motivo!r}")

sys.exit(1 if fallas else 0)

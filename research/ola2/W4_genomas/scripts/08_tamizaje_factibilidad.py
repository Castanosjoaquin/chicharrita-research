#!/usr/bin/env python3
"""W4 - prueba de factibilidad del tamizaje fuera de blanco, con secuencias publicas.

Toma un FASTA de consulta (secuencia publica de referencia; NUNCA secuencias del
corpus de EPILAB), deriva todos sus k-meros de 21 nt -la unidad que carga RISC- y
cuenta coincidencias exactas de 21/21, en las dos hebras, contra transcriptomas o
genomas locales. No es un diseno ni una evaluacion de seguridad: mide si el
tamizaje se puede correr con los datos que tenemos, con que cobertura y en cuanto
tiempo.

Uso: python3 08_tamizaje_factibilidad.py <consulta.fna> <salida.json> <etiqueta=archivo> [...]
"""
import json, sys, time
from collections import defaultdict

COMP = str.maketrans("ACGT", "TGCA")
K = 21


def revcomp(s):
    return s.translate(COMP)[::-1]


def leer_fasta(ruta):
    nom, seq, out = None, [], {}
    for l in open(ruta):
        if l.startswith(">"):
            if nom:
                out[nom] = "".join(seq)
            nom, seq = l[1:].split()[0], []
        else:
            seq.append(l.strip().upper().replace("U", "T"))
    if nom:
        out[nom] = "".join(seq)
    return out


def main():
    consulta, dest, refs = sys.argv[1], sys.argv[2], sys.argv[3:]
    qs = leer_fasta(consulta)
    km = set()
    for s in qs.values():
        for i in range(len(s) - K + 1):
            w = s[i:i + K]
            if "N" not in w:
                km.add(w)
    consulta_mas_rc = km | {revcomp(k) for k in km}
    print(f"consulta: {len(qs)} secuencias, {len(km)} 21-meros unicos "
          f"({len(consulta_mas_rc)} contando la hebra complementaria)", flush=True)
    res = {"consulta": consulta, "k": K, "n_secuencias_consulta": len(qs),
           "n_kmeros_21": len(km), "referencias": {}}
    for r in refs:
        etiqueta, ruta = r.split("=", 1)
        t0, bases, golpes = time.time(), 0, defaultdict(int)
        buf = ""
        with open(ruta) as fh:
            for linea in fh:
                if linea.startswith(">"):
                    buf = ""
                    continue
                s = linea.strip().upper()
                bases += len(s)
                buf += s
                for i in range(len(buf) - K + 1):
                    w = buf[i:i + K]
                    if w in consulta_mas_rc:
                        golpes[w] += 1
                buf = buf[-(K - 1):]
        tocados = {k for k in golpes if k in km} | {revcomp(k) for k in golpes if revcomp(k) in km}
        res["referencias"][etiqueta] = {
            "archivo": ruta, "bases_escaneadas": bases,
            "kmeros_consulta_con_coincidencia_exacta": len(tocados),
            "fraccion_kmeros_consulta": round(len(tocados) / len(km), 5) if km else None,
            "coincidencias_totales": sum(golpes.values()),
            "segundos": round(time.time() - t0, 1)}
        print(etiqueta, json.dumps(res["referencias"][etiqueta]), flush=True)
    json.dump(res, open(dest, "w"), indent=1)


if __name__ == "__main__":
    main()

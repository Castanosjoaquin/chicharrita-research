#!/usr/bin/env python3
"""C5 / Q3 — Baja las proteinas revisadas de UniProt que sirven para resolver a que
familia pertenece un gen publicado, en vez de confiar en el nombre de la anotacion.

Caso de uso: el transcrito que un trabajo de 2025 llama `Rpn6` en Scaphoideus titanus.
En UniProt, el gen Rpn6 de Drosophila melanogaster es la subunidad 11 del proteasoma
(PSMD11) y Rpn7 es la subunidad 6 (PSMD6); los nombres no son intercambiables.

Salida: work/C5/circuito/ref_rpn_uniprot.faa (lo consume scripts/04).
"""
import pathlib, urllib.parse, urllib.request

CONSULTA = ('(reviewed:true) AND ('
            '(organism_id:7227 AND (gene:Rpn6 OR gene:Rpn7 OR gene:Rpn5)) OR '
            '(organism_id:9606 AND (gene:PSMD11 OR gene:PSMD6 OR gene:PSMD12)))')
DESTINO = pathlib.Path("work/C5/circuito/ref_rpn_uniprot.faa")

def main():
    url = ("https://rest.uniprot.org/uniprotkb/stream?"
           + urllib.parse.urlencode({"query": CONSULTA, "format": "fasta"}))
    texto = urllib.request.urlopen(url, timeout=90).read().decode()
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_text(texto, encoding="utf-8")
    print(f"{texto.count('>')} proteinas en {DESTINO}")
    for linea in texto.splitlines():
        if linea.startswith(">"):
            print("  " + linea[:110])

if __name__ == "__main__":
    main()

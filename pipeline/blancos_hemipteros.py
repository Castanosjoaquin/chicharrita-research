"""Catalogo curado de blancos de RNAi con resultado reportado en HEMIPTEROS.

Por que importa: el 100 % de los fenotipos de nuestra tabla viene del cribado de *Tribolium*,
que es un coleoptero &mdash; otro orden. Ese es el supuesto que puede voltear todo el ranking.
Cada blanco que podamos respaldar con un resultado en un hemiptero baja ese riesgo.

Las fuentes son las que leimos de primera mano o las que citan los dos papers de *Dalbulus
maidis*. No hay busqueda nueva ni nada inventado: si una fila esta aca es porque aparece citada
en un trabajo que verificamos. La columna `fuente` dice de donde sale cada una.

Cada fila es: especie, gen, familia de proteina para buscar el ortologo, via de entrega,
que se observo, y de donde sale el dato.

Uso:
    python3 blancos_hemipteros.py            # imprime el catalogo y lo cruza con nuestra tabla
    python3 blancos_hemipteros.py --mapear   # ademas baja proteinas y las mapea al genoma
"""

from __future__ import annotations

import csv
import subprocess
import sys
import urllib.parse
from pathlib import Path

SALIDA = Path(__file__).parent / "salida"
DATOS = Path.home() / "yhat" / "data"
MINIPROT = Path.home() / "yhat" / "tools" / "miniprot" / "miniprot"
HEMIPTERA_TAXID = 7524

# (especie, gen, familia, via, observado, fuente)
CATALOGO = [
    ("Dalbulus maidis", "BicC", "bicaudal C", "inyeccion e ingesta",
     "oviposicion casi nula; transcripto baja >170x por inyeccion al dia 7",
     "Dalaison-Fuentes et al. 2022, leido completo"),
    ("Dalbulus maidis", "V-ATPase B", "V-type proton ATPase subunit B", "ingesta",
     "supervivencia 16 % a dia 4 contra 37 % del control de GFP; alas deformes",
     "Jones, Bernal y Medina 2021, leido completo"),
    ("Dalbulus maidis", "V-ATPase D", "V-type proton ATPase subunit D", "ingesta",
     "supervivencia 18 % a dia 4; efecto en alas no significativo",
     "Jones, Bernal y Medina 2021, leido completo"),
    ("Dalbulus maidis", "Dmai-dsRNase-2", "dsRNase", "ingesta",
     "silenciarla mejora la respuesta al dsRNA del gen de interes",
     "Pest. Biochem. Physiol. 2023, via frente f14"),
    ("Peregrinus maidis", "V-ATPase", "V-type proton ATPase", "inyeccion e ingesta",
     "silenciamiento confirmado; es el antecedente directo del trabajo en D. maidis",
     "Yao et al. 2013, citado por Jones 2021"),
    ("Nilaparvata lugens", "Bicaudal-C", "bicaudal C", "no detallada",
     "papel vital en oogenesis; es parte del fundamento para elegir BicC",
     "Zhang et al. 2015, citado por Dalaison-Fuentes 2022"),
    ("Rhodnius prolixus", "BicC", "bicaudal C", "inyeccion",
     "necesario para el epitelio folicular durante la oogenesis",
     "Pascual et al. 2021, citado por Dalaison-Fuentes 2022"),
    ("Nezara viridula", "V-ATPase A", "V-type proton ATPase catalytic subunit A", "ingesta",
     "45 % de mortalidad",
     "Sharma et al. 2020, citado por Jones 2021"),
    ("Halyomorpha halys", "JHAMT", "juvenile hormone acid O-methyltransferase",
     "pulverizacion foliar, riego a raiz, inyeccion al tronco, granulos de arcilla",
     "silenciamiento por varias vias de entrega",
     "Ghosh et al. 2018, citado por Jones 2021"),
    ("Halyomorpha halys", "Vitelogenina", "vitellogenin", "idem",
     "silenciamiento por varias vias de entrega",
     "Ghosh et al. 2018, citado por Jones 2021"),
    ("Diaphorina citri", "Catepsina D", "cathepsin D", "ingesta",
     "inhibicion de la expresion",
     "Galdeano et al. 2017, citado por Jones 2021"),
    ("Diaphorina citri", "Quitina sintasa", "chitin synthase", "ingesta",
     "inhibicion de la expresion",
     "Galdeano et al. 2017, citado por Jones 2021"),
    ("Diaphorina citri", "IAP", "inhibitor of apoptosis", "ingesta",
     "inhibicion de la expresion",
     "Galdeano et al. 2017, citado por Jones 2021"),
    ("Homalodisca vitripennis", "Actina", "actin", "celulas y organismo",
     "efecto sobre el mRNA de actina; es un cicadelido, la familia de nuestra especie",
     "Rosa et al. 2010 y 2012, citados por Dalaison-Fuentes 2022"),
    ("Nephotettix cincticeps", "NcSP75", "salivary protein", "no detallada",
     "proteina salival clave para la ingestion de floema; cicadelido",
     "Matsumoto y Hattori 2018, citado por Dalaison-Fuentes 2022"),
    ("Nephotettix cincticeps", "dosis alta de dsRNA", "", "ingesta",
     "mortalidad alta por dosis alta de dsRNA, no por el blanco; util como control",
     "Tomizawa y Noda 2013, citado por Dalaison-Fuentes 2022"),
    ("Circulifer haematoceps", "Hexamerina", "hexamerin", "no detallada",
     "necesaria para la respuesta inmune y la supervivencia frente a Spiroplasma; cicadelido",
     "Eliautout et al. 2016, citado por Dalaison-Fuentes 2022"),
    ("Amrasca biguttula", "varios", "", "no detallada",
     "demostracion de RNAi en cicadelido del algodon",
     "Singh et al. 2018, citado por Dalaison-Fuentes 2022"),
    ("Graminella nigrifrons", "respuesta inmune", "", "no detallada",
     "RNAi en la interaccion con Maize fine streak virus; cicadelido",
     "Chen, Redinbaugh y Michel 2015, citado por Dalaison-Fuentes 2022"),
]

# Familias que ya tenemos mapeadas al genoma por otra via
YA_MAPEADAS = {"bicaudal C", "V-type proton ATPase subunit B", "V-type proton ATPase subunit D",
               "V-type proton ATPase catalytic subunit A", "dsRNase", "actin"}


def familias_a_buscar() -> list[str]:
    vistas, salida = set(), []
    for fila in CATALOGO:
        fam = fila[2]
        if fam and fam not in YA_MAPEADAS and fam not in vistas:
            vistas.add(fam)
            salida.append(fam)
    return salida


def bajar_proteinas(familias: list[str]) -> Path:
    """Proteinas de hemipteros para cada familia. Se restringe a Hemiptera a proposito:
    un ortologo de hemiptero alinea mucho mejor que uno de mosca (medido en el frente f7)."""
    destino = DATOS / "blancos_hemipteros.faa"
    partes = []
    for fam in familias:
        consulta = f'(taxonomy_id:{HEMIPTERA_TAXID}) AND (protein_name:"{fam}")'
        url = ("https://rest.uniprot.org/uniprotkb/stream?"
               + urllib.parse.urlencode({"query": consulta, "format": "fasta"}))
        r = subprocess.run(["curl", "-sS", url], capture_output=True, text=True)
        n = r.stdout.count(">")
        print(f"  {fam:<42} {n:>4} proteinas de hemipteros")
        if n:
            partes.append(r.stdout)
    destino.write_text("".join(partes), encoding="utf-8")
    return destino


def main() -> None:
    print(f"catalogo: {len(CATALOGO)} blancos con resultado reportado en hemipteros")
    especies = sorted({f[0] for f in CATALOGO})
    cicadelidos = [e for e in especies if e in {
        "Dalbulus maidis", "Homalodisca vitripennis", "Nephotettix cincticeps",
        "Circulifer haematoceps", "Amrasca biguttula", "Graminella nigrifrons"}]
    print(f"especies: {len(especies)}  ·  de ellas cicadelidos (nuestra familia): {len(cicadelidos)}")
    print(f"\n{'especie':<26}{'gen':<18}{'via':<22}observado")
    for esp, gen, _fam, via, obs, _fuente in CATALOGO:
        print(f"{esp[:25]:<26}{gen[:17]:<18}{via[:21]:<22}{obs[:46]}")

    destino = SALIDA / "blancos_hemipteros.csv"
    with destino.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["especie", "gen", "familia", "via_entrega", "observado", "fuente"])
        w.writerows(CATALOGO)
    print(f"\ncatalogo en {destino}")

    if "--mapear" not in sys.argv:
        print("(agregar --mapear para bajar proteinas y alinearlas al genoma)")
        return

    familias = familias_a_buscar()
    print(f"\nfamilias sin mapear todavia: {len(familias)}")
    faa = bajar_proteinas(familias)
    if faa.stat().st_size < 100:
        print("no se bajo ninguna proteina")
        return
    gff = DATOS / "blancos_hemipteros.gff"
    with gff.open("wb") as fh:
        subprocess.run([str(MINIPROT), "-t", "20", "--gff", str(DATOS / "genome.mpi"), str(faa)],
                       stdout=fh, stderr=subprocess.DEVNULL, check=True)
    print(f"mapeado a {gff.name}; resumir con resumir_miniprot.py")


if __name__ == "__main__":
    main()

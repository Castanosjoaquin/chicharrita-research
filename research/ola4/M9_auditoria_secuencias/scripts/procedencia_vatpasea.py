"""Contesta de donde sale el CDS de `baseline_dsrip/dsrip_vatpaseA.csv`.

El REPORT de M9 (§3.3) dejo ese archivo sin exceptuar a proposito: reconstruye 1.845 nt
—el CDS completo de V-ATPase A— y el LEEME de la carpeta solo dice que se armo desde
`pipeline/salida/sirna_vatpaseA.csv`, que no se versiona. La pasada 3 de la verificacion
ya habia dado cero contra las cuatro regiones de EPILAB, pero cero no es una procedencia.

La procedencia se reconstruye sin red y sin tocar ningun servicio: las ventanas del CDS
que sobrevivieron al tamizaje aparecen en las salidas del pipeline con su columna
`locus`, y el locus lleva cromosoma y coordenadas del ensamblado sobre el que corrio
miniprot. Si el cromosoma es un contig `OZ3197xx.1`, el CDS salio del genoma publico de
*Dalbulus maidis* `GCA_975739785.1` (ihDalMaid1.1, Wellcome Sanger, 10 cromosomas) y no
de material de EPILAB.

Corre con insumos locales: `pipeline/salida/` esta en `.gitignore` porque sus derivados
llevan fenotipos de iBeetle-Base. Si falta, el script lo dice y no devuelve nada. La
salida que si se versiona guarda **solo las columnas de mapeo** de `candidatos_alto.csv`
—locus, cromosoma, coordenadas, hebra, ortologos y exones, todo producto de miniprot
sobre genomas publicos—; ninguna columna de fenotipo (`fenotipo_categoria`,
`letalidad_pct_max`, `penetrancia_max_letal`, `estructuras_afectadas`) entra al JSON.

    python3 research/ola4/M9_auditoria_secuencias/scripts/procedencia_vatpasea.py
"""
import csv
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
SALIDA = RAIZ / "pipeline" / "salida"
DESTINO = Path(__file__).resolve().parent.parent / "resultados" / "procedencia_vatpasea.json"

VENTANA = 21
STOPS = {"TAA", "TAG", "TGA"}
# Los diez cromosomas de GCA_975739785.1 ihDalMaid1.1, que es el ensamblado publico
# sobre el que el pipeline mapeo las proteinas de referencia con miniprot.
PREFIJO_IHDALMAID = "OZ3197"


def exigir(ruta: Path) -> Path:
    if not ruta.exists():
        sys.exit(
            f"falta {ruta.relative_to(RAIZ)}, que no se versiona.\n"
            "Se regenera con pipeline/correr_todo.py. La corrida queda pendiente, no en cero."
        )
    return ruta


def reconstruir_cds(filas: list[dict]) -> str:
    """Concatena las ventanas solapadas de a 1 nt en el CDS del que salieron."""
    filas = sorted(filas, key=lambda r: int(r["pos"]))
    cds = filas[0]["sitio"]
    previa = int(filas[0]["pos"])
    for fila in filas[1:]:
        # Las dos condiciones hacen falta. En un homopolimero o en un tramo repetido, una
        # ventana salteada igual cierra el solape de 20 nt y el CDS saldria corto sin que
        # nada se queje; la continuidad de `pos` es lo que lo atrapa.
        if int(fila["pos"]) != previa + 1:
            sys.exit(f"falta la ventana {previa + 1}: despues de {previa} viene {fila['pos']}")
        if fila["sitio"][:-1] != cds[-(VENTANA - 1) :]:
            sys.exit(f"las ventanas no se solapan de a 1 nt en pos {fila['pos']}")
        cds += fila["sitio"][-1]
        previa = int(fila["pos"])
    return cds


def marco_abierto(cds: str) -> dict:
    codones = [cds[i : i + 3] for i in range(0, len(cds), 3)]
    return {
        "largo_nt": len(cds),
        "empieza_en_ATG": cds[:3] == "ATG",
        "termina_en_stop": codones[-1] in STOPS,
        "stops_internos": sum(1 for c in codones[:-1] if c in STOPS),
        "aminoacidos": len(codones) - 1,
    }


def loci_de_las_ventanas(sitios: set[str]) -> dict[str, dict[str, int]]:
    """Cuenta en que locus cae cada ventana del CDS, segun las salidas del pipeline."""
    conteo: dict[str, dict[str, int]] = {}
    for nombre in ("sirna_finales.csv", "sirna_cercanos.csv"):
        porloc: dict[str, int] = {}
        with open(exigir(SALIDA / nombre), newline="", encoding="utf-8") as fh:
            for fila in csv.DictReader(fh):
                if fila["sitio"] in sitios:
                    porloc[fila["locus"]] = porloc.get(fila["locus"], 0) + 1
        conteo[nombre] = porloc
    return conteo


def ficha_del_locus(locus: str) -> dict | None:
    with open(exigir(SALIDA / "candidatos_alto.csv"), newline="", encoding="utf-8") as fh:
        for fila in csv.DictReader(fh):
            if fila["locus"] == locus:
                return {
                    k: fila[k]
                    for k in (
                        "locus", "cromosoma", "inicio", "fin", "hebra",
                        "gen_drosophila", "mejor_hit_tribolium", "mejor_hit_nilaparvata",
                        "tcas_exones",
                    )
                }
    return None


def main() -> None:
    with open(exigir(SALIDA / "sirna_vatpaseA.csv"), newline="", encoding="utf-8") as fh:
        filas = list(csv.DictReader(fh))

    cds = reconstruir_cds(filas)
    orf = marco_abierto(cds)
    conteo = loci_de_las_ventanas({f["sitio"] for f in filas})

    todos = {loc for porloc in conteo.values() for loc in porloc}
    if len(todos) != 1:
        sys.exit(f"se esperaba un solo locus y hay {len(todos)}: {sorted(todos)}")
    locus = todos.pop()
    ficha = ficha_del_locus(locus)
    if ficha is None:
        sys.exit(f"{locus} no esta en candidatos_alto.csv")

    publico = ficha["cromosoma"].startswith(PREFIJO_IHDALMAID)
    ubicadas = max(sum(porloc.values()) for porloc in conteo.values())
    informe = {
        "entrada": "pipeline/salida/sirna_vatpaseA.csv (no versionada)",
        "ventanas": len(filas),
        "ventanas_ubicadas": ubicadas,
        "cobertura": round(100 * ubicadas / len(filas), 2),
        "cds": orf,
        "ventanas_por_locus": conteo,
        "locus": ficha,
        "cromosoma_de_ihDalMaid1_1": publico,
        "conclusion": (
            f"las {ubicadas} ventanas del CDS que sobreviven al tamizaje caen todas en "
            f"{ficha['locus']}, en un cromosoma de ihDalMaid1.1 (GCA_975739785.1), "
            "publico. Las demas no aparecen en las salidas del pipeline porque el "
            "tamizaje las descarto, no porque se hayan ubicado en otro lado."
            if publico
            else "el cromosoma no es de ihDalMaid1.1: la procedencia sigue abierta"
        ),
    }

    print(f"CDS reconstruido: {orf['largo_nt']} nt, {orf['aminoacidos']} aa, "
          f"ATG inicial {orf['empieza_en_ATG']}, stop final {orf['termina_en_stop']}, "
          f"stops internos {orf['stops_internos']}")
    print(f"ventanas ubicadas: {ubicadas} de {len(filas)} "
          f"({informe['cobertura']} %; el resto las descarto el tamizaje)")
    print(f"ventanas que sobreviven al tamizaje: {conteo}")
    print(f"locus {ficha['locus']} en {ficha['cromosoma']}:{ficha['inicio']}-{ficha['fin']} "
          f"({ficha['hebra']}), ortologo de Drosophila {ficha['gen_drosophila']}, "
          f"{ficha['tcas_exones']} exones")
    print(informe["conclusion"])

    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_text(json.dumps(informe, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"-> {DESTINO.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()

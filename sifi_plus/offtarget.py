"""Un gen contra varias bases, en una sola corrida, con progreso.

Por que es la vista principal y no «varios genes contra una base»: `CLAUDE.md` exige que toda
propuesta de diseno lleve su contracara de riesgo —off-targets en maiz, en polinizadores, en
enemigos naturales, en fauna del suelo—, y eso es exactamente una consulta contra varias
bases. El original no puede hacerlo: elige UNA base de datos en un desplegable, y para
comparar seis hay que correrlo seis veces y pegar los numeros a mano. Ademas su grafico topea
en cinco objetivos («Maximum of 5 targets will be displayed», manual p. 12).

Por que es un trabajo con progreso y no un pedido comun: el genoma de *Dalbulus maidis* son
984 MB descomprimidos. Un pedido HTTP sincronico deja el navegador colgado sin decir nada,
que es justo el defecto del original que estamos corrigiendo.

El motor es el tamizaje exacto de `tools/sifi21_port/offtarget_21nt.py` (Aho-Corasick, una
pasada por base, las dos hebras), importado tal cual: `construir` y `escanear` no se tocan.
Su salida esta verificada contra la corrida de BLAST+ de W5 —los criterios de bloque perfecto
coinciden en las 20 celdas— y es estable byte a byte.

El camino Bowtie no esta aca: es el unico que reproduce la regla de conteo del original (un
registro por acierto, no por ventana) y vive en
`research/ola4/M1_conteo_y_referencia/scripts/conteo_por_acierto.py`. Son dos preguntas
distintas y mezclarlas en un mismo numero fue el error que M1 desarmo.
"""

from __future__ import annotations

import sys
import threading
import time
import uuid
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "tools" / "sifi21_port"))
sys.path.insert(0, str(AQUI))

from offtarget_21nt import construir, escanear  # noqa: E402

import complejidad  # noqa: E402
from api import RAIZ, SALIDAS  # noqa: E402

CRITERIOS = ("perfecto_21", "perfecto_ge19", "mm1_21")

# El papel de cada referencia del panel. Importa para leer la tabla: un acierto en el maiz no
# significa lo mismo que uno en el genoma del propio vector, que es el blanco.
PANEL = {
    "GCA_975739785.1_ihDalMaid1.1_genomic":
        ("Dalbulus maidis (genoma)", "el vector: es el blanco, no un off-target"),
    "GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna":
        ("Zea mays", "el cultivo que se quiere proteger"),
    "GCF_021130785.1_UT_GWSS_2.1_rna":
        ("Homalodisca vitripennis", "cicadelido no objetivo, el pariente mas cercano"),
    "GCF_003254395.2_Amel_HAv3.1_rna":
        ("Apis mellifera", "polinizador"),
    "GCF_914767665.1_icHarAxyr1.1_rna":
        ("Harmonia axyridis", "enemigo natural"),
    "GCF_002217175.1_ASM221717v1_rna":
        ("Folsomia candida", "fauna del suelo"),
}


# Las bases de `work/M1/bases/` son las mismas referencias descomprimidas, con nombre corto
# (el mapeo esta en `research/ola4/M1_conteo_y_referencia/resultados/procedencia.json`, clave
# `que_es_cada_base`). Ofrecer las dos copias del mismo transcriptoma no agrega una
# referencia: agrega una forma de medir dos veces lo mismo y creer que son dos evidencias.
ALIAS = {
    "amel": "GCF_003254395.2_Amel_HAv3.1_rna",
    "zmays": "GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna",
    "fcandida": "GCF_002217175.1_ASM221717v1_rna",
    "hvitri": "GCF_021130785.1_UT_GWSS_2.1_rna",
    "haxyr": "GCF_914767665.1_icHarAxyr1.1_rna",
    "dmaid_genoma": "GCA_975739785.1_ihDalMaid1.1_genomic",
}

# Las que no estan en el panel de riesgo pero sirven como consulta o como control.
OTRAS = {
    "mrfv_nc": ("MRFV NC_002786.2", "genoma de referencia del virus"),
    "mrfv_all": ("MRFV, 65 registros", "los aislamientos publicos de GenBank"),
    "gitv01_blancos": ("D. maidis TSA GITV01", "los 2 contigs identificados como blanco"),
    "epilab4": ("Los 4 genes de EPILAB", "la celda de verificacion, no una referencia"),
    "epilab4_rc": ("Los 4 genes de EPILAB, revcomp", "control de orientacion"),
}


def _nombre_base(ruta: Path) -> str:
    return ruta.name.replace(".fna.gz", "").replace(".fasta", "").replace(".fa", "")


def bases_disponibles() -> list[dict]:
    """Las referencias que hay en esta maquina, con su papel y su tamano.

    Se listan las que estan, no las que deberia haber. Si falta una, la interfaz lo muestra en
    vez de dar un cero tranquilizador: «no hay aciertos» y «no se miro» no son lo mismo.
    """
    out: list[dict] = []
    vistos: set[str] = set()
    for d in (RAIZ / "work" / "offtarget_db", RAIZ / "work" / "M1" / "bases"):
        if not d.is_dir():
            continue
        for p in sorted(d.iterdir()):
            if p.suffix not in (".gz", ".fa", ".fasta", ".fna"):
                continue
            n = _nombre_base(p)
            canon = ALIAS.get(n, n)
            if canon in vistos:
                continue
            vistos.add(canon)
            nombre, papel = PANEL.get(canon, OTRAS.get(n, (n, "")))
            out.append({"id": n, "archivo": str(p), "nombre": nombre, "papel": papel,
                        "mb": round(p.stat().st_size / 1e6, 1),
                        "en_panel": canon in PANEL})
    # El panel de riesgo primero, y el genoma del vector al final del panel: es el on-target.
    out.sort(key=lambda b: (not b["en_panel"], "genomic" in b["id"], b["nombre"]))
    return out


# --- Trabajos --------------------------------------------------------------

TRABAJOS: dict[str, dict] = {}
_LOCK = threading.Lock()


def estado(ident: str) -> dict | None:
    with _LOCK:
        t = TRABAJOS.get(ident)
        return dict(t) if t else None


def lanzar(*, nombre: str, secuencia: str, bases: list[str], size=21, min_block=19,
           mm1=False, ontarget=None) -> str:
    """Arranca el tamizaje en un hilo y devuelve el identificador del trabajo."""
    disponibles = {b["id"]: b["archivo"] for b in bases_disponibles()}
    faltan = [b for b in bases if b not in disponibles]
    if faltan:
        raise ValueError("no estan en disco: %s" % ", ".join(faltan))
    if not bases:
        raise ValueError("hay que elegir al menos una base de referencia")

    ident = uuid.uuid4().hex[:12]
    with _LOCK:
        TRABAJOS[ident] = {"id": ident, "estado": "arrancando", "hecho": 0,
                           "total": len(bases), "base_actual": "", "mensaje": "",
                           "resultado": None, "error": None,
                           "arranque": time.time(), "segundos": 0.0}

    hilo = threading.Thread(
        target=_correr, daemon=True,
        kwargs=dict(ident=ident, nombre=nombre, secuencia=secuencia,
                    rutas=[(b, disponibles[b]) for b in bases],
                    size=size, min_block=min_block, mm1=mm1, ontarget=ontarget))
    hilo.start()
    return ident


def _actualizar(ident: str, **kw) -> None:
    with _LOCK:
        t = TRABAJOS.get(ident)
        if t is not None:
            t.update(kw)
            t["segundos"] = round(time.time() - t["arranque"], 1)


def _correr(*, ident, nombre, secuencia, rutas, size, min_block, mm1, ontarget):
    try:
        # `construir` lee FASTA de disco. En vez de cambiar su firma —esta verificada y su
        # salida es estable byte a byte— se le escribe la consulta a un temporal en work/.
        tmp = SALIDAS / "tmp"
        tmp.mkdir(parents=True, exist_ok=True)
        fa = tmp / ("consulta_%s.fasta" % ident)
        fa.write_text(">%s\n%s\n" % (nombre, secuencia), encoding="utf-8")

        _actualizar(ident, estado="construyendo", mensaje="armando el automata de patrones")
        aut, sirnas = construir([str(fa)], mm1, size, min_block)
        _actualizar(ident, mensaje="%d ventanas, %d patrones%s" % (
            len(sirnas), len(aut), " (con 1 desajuste)" if mm1 else ""))

        # Las ventanas de baja complejidad se marcan una vez, acá, y cada conteo se informa en
        # dos cifras. La cola de poli-A de un ARNm pega en cualquier transcriptoma y no es una
        # homología: sumarla al riesgo sin decirlo es lo que hace el original.
        bajas = {s["pos"] for s in sirnas if complejidad.es_baja(s["sirna"])}

        por_base: dict[str, dict] = {}
        for i, (base, ruta) in enumerate(rutas):
            _actualizar(ident, estado="escaneando", base_actual=base, hecho=i)
            hits = escanear(aut, sirnas, ruta)

            pos = {}
            for crit in CRITERIOS:
                pos[crit] = sorted(sirnas[idx]["pos"] for idx in hits[crit])
            p21 = set(pos["perfecto_21"])
            mm1_pos_base = [p for p in pos["mm1_21"] if p not in p21]
            refs = set()
            for crit in ("perfecto_21", "perfecto_ge19"):
                for s in hits[crit].values():
                    refs |= s
            por_base[base] = {
                "base": base,
                "nombre": PANEL.get(base, (base, ""))[0],
                "papel": PANEL.get(base, (base, ""))[1],
                "es_ontarget": (base == ontarget),
                "perfecto_21": len(pos["perfecto_21"]),
                "perfecto_ge19": len(pos["perfecto_ge19"]),
                "mm1_21": len(mm1_pos_base) if mm1 else None,
                # cuanto de cada cifra es cola de poli-A o repeticion simple
                "perfecto_21_baja": len(p21 & bajas),
                "perfecto_ge19_baja": len(set(pos["perfecto_ge19"]) & bajas),
                "mm1_21_baja": (len(set(mm1_pos_base) & bajas) if mm1 else None),
                "referencias_distintas": len(refs),
                "posiciones": pos,
            }
            _actualizar(ident, hecho=i + 1)

        # Las tiras del grafico: la union sobre las bases que NO son el blanco. Excluir el
        # on-target es lo que hace `cruce.py`, y sin eso el gen entero aparece como riesgo
        # porque sus propias ventanas pegan en su propio genoma.
        off_pos, mm1_pos = set(), set()
        hubo_mm1 = False
        for base, d in por_base.items():
            if d["es_ontarget"]:
                continue
            off_pos |= set(d["posiciones"]["perfecto_ge19"])
            if mm1:
                hubo_mm1 = True
                mm1_pos |= set(d["posiciones"]["mm1_21"])

        fa.unlink(missing_ok=True)
        _actualizar(ident, estado="listo", base_actual="", mensaje="",
                    resultado={
                        "consulta": nombre, "size": size, "min_block": min_block,
                        "mm1": mm1, "ontarget": ontarget,
                        "ventanas": len(sirnas),
                        "ventanas_baja": len(bajas),
                        "criterio_baja": ("racha de un mismo nucleotido >= %d nt, o <= %d "
                                          "nucleotidos distintos en la ventana"
                                          % (complejidad.HOMOPOLIMERO_MAX,
                                             complejidad.BASES_MIN)),
                        "bases": [por_base[b] for b, _ in rutas],
                        "off_perfecto": sorted(off_pos),
                        "off_perfecto_baja": sorted(off_pos & bajas),
                        "off_mm1": sorted(mm1_pos - off_pos) if hubo_mm1 else None,
                    })
    except Exception as e:  # noqa: BLE001 - el hilo no puede dejar el trabajo sin estado
        _actualizar(ident, estado="error", error="%s: %s" % (type(e).__name__, e))

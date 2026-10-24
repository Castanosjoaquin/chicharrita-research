"""Las anclas de conteo, por el camino de codigo de la aplicacion.

Que prueba esto y por que importa: la interfaz no tiene que haber movido ni un numero. El port
ya esta verificado contra el programa original, pero esa verificacion corrio por
`run_sifi.py`. Si la aplicacion llama al motor de otra forma —otro default, otro orden, otra
conversion— puede dar numeros distintos y nadie se enteraria. Asi que estas verificaciones
entran por `api.correr_diseno`, que es exactamente lo que ejecuta el servidor cuando alguien
aprieta «Correr».

Las anclas, publicadas en `tools/sifi21_port/CAMBIOS.md` y
`research/ola4/M2_ventana_a_ventana/scripts/correr_pares.py`:

    RNAplfold 2.1.5 (el de si-Fi21)   fiel: 133, 32, 212, 42   corregido: 114, 25, 162, 34
    ViennaRNA 2.7.2                   fiel: 142, 39, 223, 35   corregido: 123, 30, 171, 29

Y la mas externa, que no es nuestra: los cuatro conteos que imprimio el **programa original**
con su interfaz y sus defaults, en `research/ola2/W5_secuencias_epilab/analisis/
sifi21_original_*.csv`.

Si faltan los FASTA de `work/` o el binario de RNAplfold, el bloque correspondiente se declara
**no corrido** y se dice en el resumen. Un cero tranquilizador que en realidad significa «no se
miro» es el patron que este repositorio evita a proposito.

Uso:
    python test_api.py
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import api
import complejidad
import perfil
import proyecto

FALLAS: list[str] = []
NO_CORRIDO: list[str] = []
HECHAS = 0

W5 = api.RAIZ / "research" / "ola2" / "W5_secuencias_epilab" / "analisis"
CHECK = api.RAIZ / "work" / "sifi_check"

GENES = ["MP_MRFV", "CP_MRFV", "BicC_Dm", "ATPaseD_Dm"]

ANCLAS = {
    ("exe", "fiel"): [133, 32, 212, 42],
    ("exe", "corregido"): [114, 25, 162, 34],
    ("vienna", "fiel"): [142, 39, 223, 35],
    ("vienna", "corregido"): [123, 30, 171, 29],
}


def check(cond, etiqueta):
    global HECHAS
    HECHAS += 1
    if not cond:
        FALLAS.append(etiqueta)
        print("  FALLA  %s" % etiqueta)
    return bool(cond)


def igual(obtenido, esperado, etiqueta):
    return check(obtenido == esperado,
                 "%s: esperaba %r y dio %r" % (etiqueta, esperado, obtenido))


def leer(gen):
    p = CHECK / ("%s_full.fasta" % gen)
    if not p.is_file():
        return None
    pares = api.leer_fasta(p.read_text(encoding="utf-8"))
    return pares[0] if pares else None


def leer_ejemplo():
    """El dato de ejemplo que viaja con la carpeta: publico y sin relacion con EPILAB.

    Las pruebas del contrato entran por aca y no por `work/`, para que corran en cualquier
    maquina y no dependan de datos que no se versionan.
    """
    rutas = sorted((AQUI / "datos_ejemplo").glob("*.fasta"))
    if not rutas:
        raise FileNotFoundError("no hay datos de ejemplo en sifi_plus/datos_ejemplo")
    return api.leer_fasta(rutas[0].read_text(encoding="utf-8"))[0]


# --------------------------------------------------------------- las anclas


def test_anclas_de_conteo():
    """Los cuatro conteos, en los dos modos y con los dos motores, por el camino de la app."""
    disponibles = {m["id"]: m["disponible"] for m in api.motores()}

    for (backend, modo), esperados in sorted(ANCLAS.items()):
        if not disponibles.get(backend):
            NO_CORRIDO.append("anclas %s/%s: el motor %s no esta en esta maquina"
                              % (backend, modo, backend))
            continue
        obtenidos = []
        for gen in GENES:
            par = leer(gen)
            if par is None:
                NO_CORRIDO.append("anclas %s/%s: falta %s_full.fasta en work/sifi_check"
                                  % (backend, modo, gen))
                obtenidos = None
                break
            _, resumen, _ = api.correr_diseno(par[1], nombre=par[0], modo=modo,
                                              backend=backend)
            obtenidos.append(resumen["eficientes"])
        if obtenidos is None:
            continue
        igual(obtenidos, esperados, "anclas %s/%s sobre %s" % (backend, modo, GENES))


def test_ancla_del_programa_original():
    """Los cuatro conteos que imprimio si-Fi21 con su interfaz, leidos de su propio CSV."""
    disponibles = {m["id"]: m["disponible"] for m in api.motores()}
    if not disponibles.get("exe"):
        NO_CORRIDO.append("ancla del original: hace falta su RNAplfold 2.1.5")
        return

    for gen in GENES:
        # El CSV de ATPaseD quedo con el nombre corto, como lo escribio el programa.
        cands = [W5 / ("sifi21_original_%s.csv" % gen),
                 W5 / ("sifi21_original_%s.csv" % gen.replace("_Dm", ""))]
        ruta = next((c for c in cands if c.is_file()), None)
        if ruta is None:
            NO_CORRIDO.append("ancla del original: no esta el CSV de %s" % gen)
            continue
        with open(ruta, encoding="utf-8") as fh:
            filas = list(csv.DictReader(fh, delimiter=";"))
        if not filas:
            NO_CORRIDO.append("ancla del original: el CSV de %s esta vacio" % gen)
            continue
        del_original = int(filas[0]["Efficient siRNA hits"])

        par = leer(gen)
        if par is None:
            NO_CORRIDO.append("ancla del original: falta el FASTA de %s" % gen)
            continue
        _, resumen, _ = api.correr_diseno(par[1], nombre=par[0], modo="fiel", backend="exe")
        igual(resumen["eficientes"], del_original,
              "%s: el modo fiel reproduce el conteo del programa original" % gen)


def test_curva_del_rnai_design_plot():
    """La curva roja del original: ocho tramos, maximo 9 en 150-156 y 8 en 287-297.

    Es la verificacion del grafico, independiente del total: dos perfiles distintos pueden dar
    el mismo conteo. Se reprodujo tramo por tramo contra la pantalla del programa
    (`research/ola2/W5_secuencias_epilab/sifi21_reproduccion.md`, lineas 85-89).
    """
    disponibles = {m["id"]: m["disponible"] for m in api.motores()}
    if not disponibles.get("exe"):
        NO_CORRIDO.append("curva del design plot: hace falta su RNAplfold 2.1.5")
        return
    par = leer("ATPaseD_Dm")
    if par is None:
        NO_CORRIDO.append("curva del design plot: falta ATPaseD_Dm_full.fasta")
        return

    _, _, c = api.correr_diseno(par[1], nombre=par[0], modo="fiel", backend="exe")
    s = c["solapamiento"]

    tramos = []
    ini = None
    for i, v in enumerate(s, start=1):
        if v > 0 and ini is None:
            ini = i
        elif v == 0 and ini is not None:
            tramos.append((ini, i - 1, max(s[ini - 1:i - 1])))
            ini = None
    if ini is not None:
        tramos.append((ini, len(s), max(s[ini - 1:])))

    igual(len(tramos), 8, "la curva tiene ocho tramos separados")
    igual(max(s), 9, "el maximo de la curva")

    def altura_en(p):
        return next((alt for a, b, alt in tramos if a <= p <= b), None)

    igual(altura_en(150), 9, "el tramo que contiene la posicion 150 mide 9")
    igual(altura_en(156), 9, "el tramo que contiene la posicion 156 mide 9")
    igual(altura_en(287), 8, "el tramo que contiene la posicion 287 mide 8")
    igual(altura_en(297), 8, "el tramo que contiene la posicion 297 mide 8")


# --------------------------------------------------------------- el contrato


def test_contrato_de_curvas():
    """Las dos curvas viven en escalas distintas, y cada una tiene su largo."""
    nombre, seq = leer_ejemplo()
    _, resumen, c = api.correr_diseno(seq, nombre=nombre, modo="corregido")

    igual(len(c["solapamiento"]), c["largo"],
          "la curva de solapamiento tiene un punto por posicion del gen")
    igual(len(c["todos"]), c["largo"], "la curva de referencia tambien")
    igual(len(c["densidad"]), c["n_ventanas"],
          "la curva de densidad tiene un punto por ventana")
    igual(c["n_ventanas"], c["largo"] - c["size"] + 1, "cuantas ventanas entran")
    # La referencia es plana en el tamano de la ventana en todo el interior del gen.
    interior = c["todos"][c["size"]:-c["size"]]
    igual(set(interior), {c["size"]},
          "la referencia de todos los siRNA es plana en %d" % c["size"])
    check(max(c["solapamiento"]) <= c["size"],
          "el solapamiento nunca pasa el tamano de la ventana")
    igual(len(c["eficientes"]), resumen["eficientes"],
          "las posiciones eficientes del contrato son las del resumen")
    check(c["off_perfecto"] is None and c["off_mm1"] is None,
          "sin tamizaje, las tiras de off-target son None y no listas vacias")


def test_densidad_contra_informe_html():
    """`perfil.densidad` da lo mismo que el algoritmo de `informe_html.py:577-585`.

    Son los dos dibujantes del mismo contrato. Si alguien cambia uno, esto falla.
    """
    eficientes = [3, 4, 5, 20, 21, 60, 61, 62, 63, 140]
    n_vent, L = 150, 40

    pre = [0] * (n_vent + 1)
    efic_set = set(eficientes)
    for i in range(1, n_vent + 1):
        pre[i] = pre[i - 1] + (1 if i in efic_set else 0)
    media = (L - 1) // 2
    referencia = []
    for x in range(1, n_vent + 1):
        ini = max(1, x - media)
        fin = min(n_vent, x - media + L - 1)
        referencia.append(pre[fin] - pre[ini - 1])

    igual(perfil.densidad(eficientes, n_vent, L), referencia,
          "la densidad coincide con la de informe_html.py")


def test_solapamiento_de_una_ventana():
    """Una sola ventana eficiente cubre exactamente `size` posiciones."""
    s = perfil.solapamiento([10], largo=100, size=21)
    igual(sum(1 for v in s if v == 1), 21, "una ventana cubre 21 posiciones")
    igual(s[9], 1, "cubre su propia posicion de arranque")
    igual(s[8], 0, "no cubre la anterior")
    igual(s[29], 1, "cubre hasta 21 nt despues")
    igual(s[30], 0, "y no mas")
    # Contra el borde se recorta y no se sale del array.
    igual(len(perfil.solapamiento([95], largo=100, size=21)), 100,
          "una ventana contra el borde no desborda")


# --------------------------------------------------------------- parametros


def test_cadena_de_configuracion():
    """La cadena del investigador vuelve igual, y una mal escrita explica que falta."""
    igual(api.cadena_config(api.parsear_config("siFi21_8_1.0_0.1_1111")),
          "siFi21_8_1.0_0.1_1111", "la configuracion declarada por el investigador (D45)")
    p = api.parsear_config("siFi21_8_1.0_0.1_1111")
    igual([p["accessibility_window"], p["end_stability_threshold"],
           p["accessibility_threshold"]], [8, 1.0, 0.1], "los tres numeros")
    igual(all(p[c] for c in api.CASILLAS), True, "las cuatro casillas en verdadero")
    # Los bits son, en el orden del panel: hebra, extremos, accesibilidad, regla terminal.
    # El perfil de off-target del manual (p. 11) deja tildadas la primera y la ultima.
    igual(api.cadena_config(api.PRESETS["diseno"]), "siFi21_8_1.0_0.1_1111",
          "el preset de diseno tilda las cuatro casillas")
    igual(api.cadena_config(api.PRESETS["offtarget"]), "siFi21_8_1.0_0.1_1001",
          "el preset de off-target apaga extremos y accesibilidad")

    for mala in ("", "siFi21_8_1.0_0.1", "nada_8_1.0_0.1_1111", "siFi21_8_1.0_0.1_11",
                 "siFi21_8_1.0_0.1_1112", "siFi21_x_1.0_0.1_1111"):
        try:
            api.parsear_config(mala)
            check(False, "%r tendria que ser rechazada" % mala)
        except ValueError as e:
            check(len(str(e)) > 20, "%r se rechaza con un mensaje que explica" % mala)


def test_validacion_de_parametros():
    """Un parametro fuera de rango se rechaza aca, no dentro de ViennaRNA."""
    casos = [
        ({"sirna_size": 3}, "tamano de siRNA chico"),
        ({"sirna_size": 500}, "tamano de siRNA grande"),
        ({"accessibility_window": 0}, "ventana de accesibilidad en cero"),
        ({"accessibility_window": 99}, "ventana mayor que el siRNA"),
        ({"accessibility_threshold": 1.5}, "umbral de accesibilidad fuera de [0,1]"),
        ({"accessibility_threshold": -0.1}, "umbral de accesibilidad negativo"),
    ]
    for crudo, etq in casos:
        try:
            api.normalizar(crudo)
            check(False, "%s tendria que ser rechazado" % etq)
        except ValueError:
            check(True, "%s se rechaza" % etq)

    p = api.normalizar({})
    igual([p["sirna_size"], p["accessibility_window"]], [21, 8],
          "sin parametros quedan los defaults del original")


def test_modos_son_subconjunto():
    """El corregido es un subconjunto estricto del fiel: ninguna ventana va al revés."""
    par = leer("CP_MRFV")
    if par is None:
        NO_CORRIDO.append("subconjunto de modos: falta CP_MRFV_full.fasta")
        return
    vf, rf, _ = api.correr_diseno(par[1], nombre=par[0], modo="fiel")
    vc, rc, _ = api.correr_diseno(par[1], nombre=par[0], modo="corregido")
    sf = {w.pos for w in vf if w.is_efficient}
    sc = {w.pos for w in vc if w.is_efficient}
    igual(sc - sf, set(), "el corregido no agrega ninguna ventana que el fiel rechace")
    check(len(sf - sc) > 0, "el fiel agrega ventanas por el atajo de la regla terminal")
    check(rf["eficientes"] > rc["eficientes"], "y por eso cuenta mas")


# --------------------------------------------------------------- complejidad


def test_baja_complejidad():
    """El criterio atrapa la cola de poli-A y no toca una secuencia normal."""
    igual(complejidad.es_baja("A" * 21), True, "un 21-mero de poli-A es baja complejidad")
    igual(complejidad.es_baja("C" + "A" * 20), True, "casi todo poli-A tambien")
    igual(complejidad.es_baja("AT" * 10 + "A"), True,
          "dos nucleotidos alternados tambien (<= 2 distintos)")
    igual(complejidad.es_baja("ACGTTGCAAGCTTGACCTAGG"), False,
          "una ventana de composicion normal no")
    igual(complejidad.homopolimero("AACCCGGGGT"), 4, "la racha mas larga")
    igual(complejidad.homopolimero(""), 0, "la racha de la cadena vacia")

    # Un ARNm de RefSeq con composicion normal no tiene casi nada marcado: el criterio no
    # puede estar marcando secuencia comun.
    nombre, seq = leer_ejemplo()
    ventanas, _, _ = api.correr_diseno(seq, nombre=nombre, modo="corregido")
    bajas = complejidad.posiciones_bajas(ventanas)
    check(len(bajas) <= 0.01 * len(ventanas),
          "en el ARNm de maiz del ejemplo se marca casi nada: %d de %d ventanas"
          % (len(bajas), len(ventanas)))

    # El caso real que motivo el criterio: la cola de poli-A del genoma del MRFV, que hace
    # que nueve «coincidencias perfectas de 21/21 nt» en un no objetivo no sean homologia.
    # El archivo vive en work/ y no viaja con la entrega, asi que si no esta, no se corrio.
    mrfv = CHECK / "NC_002786.2.fasta"
    if not mrfv.is_file():
        NO_CORRIDO.append("cola de poli-A del MRFV: falta work/sifi_check/NC_002786.2.fasta")
        return
    nombre, seq = api.leer_fasta(mrfv.read_text(encoding="utf-8"))[0]
    ventanas, _, _ = api.correr_diseno(seq, nombre=nombre, modo="corregido")
    bajas = complejidad.posiciones_bajas(ventanas)
    check(len(bajas) > 0, "el genoma del MRFV tiene ventanas de baja complejidad")
    check(max(bajas) >= len(ventanas) - 2,
          "y estan al final del genoma, que es donde esta la cola de poli-A")
    check(len(bajas) < 0.01 * len(ventanas),
          "son una fraccion chica: %d de %d" % (len(bajas), len(ventanas)))


# --------------------------------------------------------------- rangos


def test_rango_no_guarda_secuencias():
    """Un rango guardado son coordenadas y conteos. La contencion se impone, no se recuerda."""
    guardado = proyecto.guardar({
        "nombre": "prueba de test_api", "gen": "GEN_DE_PRUEBA",
        "inicio": 264, "fin": 563, "eficientes": 199, "modo": "fiel", "motor": "exe",
        # esto no tiene que sobrevivir
        "seq": "ACGTTGCAAGCTTGACCTAGG", "nota": "ACGTACGTACGTACGTACGTACGT",
    })
    check("seq" not in guardado, "la clave seq no se guarda")
    check("nota" not in guardado, "un campo permitido con pinta de secuencia tampoco")
    igual(guardado["largo"], 300, "el largo se calcula")

    texto = (proyecto.CARPETA / guardado["id"]).read_text(encoding="utf-8")
    check("ACGTTGCAAGCTTGACCTAGG" not in texto, "el archivo no contiene la secuencia")
    check(guardado["id"] in {r["id"] for r in proyecto.listar()}, "aparece en el listado")

    invertido = proyecto.guardar({"gen": "G", "inicio": 500, "fin": 100})
    igual([invertido["inicio"], invertido["fin"]], [100, 500],
          "un rango al reves se ordena")

    for r in (guardado["id"], invertido["id"]):
        proyecto.borrar(r)
    check(guardado["id"] not in {x["id"] for x in proyecto.listar()}, "y se puede borrar")

    for falta in ({"inicio": 1, "fin": 2}, {"gen": "G", "fin": 2}, {"gen": "G", "inicio": 1}):
        try:
            proyecto.guardar(falta)
            check(False, "un rango sin %s tendria que ser rechazado" % list(falta))
        except ValueError:
            check(True, "un rango incompleto se rechaza")


def test_tamizaje_contra_dos_bases():
    """Control de cordura del tamizaje: el ejemplo se encuentra a si mismo y nada mas.

    El dato de ejemplo es un ARNm de *Zea mays*, asi que contra el transcriptoma del maiz
    **todas** sus ventanas tienen coincidencia perfecta, y contra un transcriptoma de insecto
    ninguna. Si esos dos numeros dejan de dar eso, el tamizaje esta roto. Es ademas la unica
    cobertura de `offtarget.py`.
    """
    import time

    import offtarget

    disp = {b["id"]: b for b in offtarget.bases_disponibles()}
    maiz = "GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna"
    bicho = "GCF_914767665.1_icHarAxyr1.1_rna"
    faltan = [b for b in (maiz, bicho) if b not in disp]
    if faltan:
        NO_CORRIDO.append("tamizaje: no estan en work/offtarget_db: %s" % ", ".join(faltan))
        return

    nombre, seq = leer_ejemplo()
    ident = offtarget.lanzar(nombre=nombre, secuencia=seq, bases=[bicho, maiz])
    limite = time.time() + 600
    while time.time() < limite:
        est = offtarget.estado(ident)
        if est["estado"] in ("listo", "error"):
            break
        time.sleep(1)
    else:
        NO_CORRIDO.append("tamizaje: no termino en 10 minutos")
        return

    if est["estado"] == "error":
        check(False, "el tamizaje termino con error: %s" % est["error"])
        return

    r = est["resultado"]
    por_base = {b["base"]: b for b in r["bases"]}
    igual(r["ventanas"], len(seq) - 21 + 1, "una ventana por posicion alcanzable")
    igual(por_base[maiz]["perfecto_21"], r["ventanas"],
          "contra el maiz, el ARNm de maiz se encuentra entero a si mismo")
    igual(por_base[bicho]["perfecto_21"], 0,
          "contra Harmonia axyridis no hay ninguna coincidencia perfecta")
    igual(por_base[bicho]["perfecto_ge19"], 0, "ni un bloque perfecto de 19 nt")
    check(por_base[maiz]["referencias_distintas"] > 0,
          "y el maiz devuelve al menos un registro de referencia")
    # Sin pedir el criterio de un desajuste, la cifra es None y no cero.
    check(por_base[maiz]["mm1_21"] is None and por_base[bicho]["mm1_21"] is None,
          "sin pedirlo, el criterio de un desajuste queda en None y no en cero")
    check(r["off_mm1"] is None, "y la tira del grafico tambien")

    # Una base que no esta en disco se rechaza con su nombre, no con un cero.
    try:
        offtarget.lanzar(nombre="x", secuencia=seq, bases=["no_existe_esta_base"])
        check(False, "una base inexistente tendria que ser rechazada")
    except ValueError as e:
        check("no_existe_esta_base" in str(e), "y el error dice cual falta")
    try:
        offtarget.lanzar(nombre="x", secuencia=seq, bases=[])
        check(False, "tamizar contra ninguna base tendria que ser rechazado")
    except ValueError:
        check(True, "tamizar contra ninguna base se rechaza")


def test_nombres_de_archivo_exportado():
    """Dos exportaciones distintas del mismo gen no pueden caer en el mismo archivo.

    Regresion: `with_suffix` toma todo lo que sigue al ultimo punto como extension, y toda
    accesion del NCBI tiene un punto. `NC_002786.2_ventanas` y `NC_002786.2_features`
    terminaban los dos en `NC_002786.tsv`, uno pisando al otro.
    """
    import exportar

    a = exportar.destino("NC_002786.2_ventanas", ".tsv")
    b = exportar.destino("NC_002786.2_features", ".tsv")
    check(a != b, "dos exportaciones del mismo gen van a archivos distintos")
    igual(a.name, "NC_002786.2_ventanas.tsv", "la accesion sobrevive entera en el nombre")
    igual(exportar.destino("MP_MRFV_full_sirna", ".fasta").name,
          "MP_MRFV_full_sirna.fasta", "un nombre sin puntos tambien")
    igual(exportar.destino("con/barra\\y:dos puntos", ".csv").name,
          "con_barra_y_dos_puntos.csv", "los caracteres de ruta se neutralizan")
    check(exportar.destino("..\\..\\fuera", ".csv").parent == exportar.SALIDAS / "exportado",
          "no se puede escribir fuera de la carpeta de salidas")


def test_lectura_de_fasta():
    """FASTA simple, multiple, con CRLF, y secuencia pelada."""
    igual(api.leer_fasta(">a desc\nACGT\nACGT\n"), [("a", "ACGTACGT")], "FASTA simple")
    igual(api.leer_fasta(">a\nAC\n>b\nGT\n"), [("a", "AC"), ("b", "GT")], "FASTA multiple")
    igual(api.leer_fasta(">a\r\nAC\r\nGT\r\n"), [("a", "ACGT")], "FASTA con CRLF")
    igual(api.leer_fasta("ACGT\nACGT"), [("secuencia_pegada", "ACGTACGT")],
          "secuencia sin encabezado")
    igual(api.leer_fasta("   "), [], "texto vacio no da ninguna secuencia")
    igual(api.leer_fasta(">solo_encabezado\n"), [], "un encabezado sin secuencia no cuenta")


def main():
    pruebas = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for f in pruebas:
        print("== %s" % f.__name__)
        try:
            f()
        except Exception as e:  # noqa: BLE001
            FALLAS.append("%s levanto %s: %s" % (f.__name__, type(e).__name__, e))
            print("  EXCEPCION %s: %s" % (type(e).__name__, e))

    print()
    print("%d verificaciones" % HECHAS)
    if NO_CORRIDO:
        print()
        print("NO CORRIDO (%d). Un cero aca no significa que este bien: significa que no se "
              "miro." % len(NO_CORRIDO))
        for x in NO_CORRIDO:
            print("   %s" % x)
    if FALLAS:
        print()
        print("FALLARON %d:" % len(FALLAS))
        for x in FALLAS:
            print("   %s" % x)
        return 1
    print("todas las verificaciones pasaron")
    return 0


if __name__ == "__main__":
    sys.exit(main())

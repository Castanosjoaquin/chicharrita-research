"""Genera las figuras del informe en entregables/informe/figuras/.

Cada cifra sale de un archivo versionado y la ruta va en el comentario de la figura.
Donde no hay un archivo de datos tabular (la cifra vive en un REPORT), se declara en
el comentario, y el valor se copia tal cual del documento citado.

Uso (desde la raiz del repositorio):
    python entregables/informe/figuras.py
"""
import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = Path(__file__).resolve().parent / "figuras"
SALIDA.mkdir(exist_ok=True)

AZUL = "#2a78d6"
NARANJA = "#eb6834"
GRIS = "#a9a8a2"
GRIS_OSC = "#6f6e69"
GRIS_CLARO = "#ecebe6"
TINTA = "#1a1a19"

plt.rcParams.update({
    "font.family": ["Arial", "Helvetica Neue", "DejaVu Sans"],
    "font.size": 9,
    "axes.edgecolor": GRIS,
    "axes.linewidth": 0.8,
    "axes.labelcolor": GRIS_OSC,
    "xtick.color": GRIS_OSC,
    "ytick.color": TINTA,
    "xtick.major.size": 0,
    "ytick.major.size": 0,
    "text.color": TINTA,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 100,
    "savefig.dpi": 220,
    "savefig.facecolor": "white",
})


def guardar(fig, nombre):
    fig.savefig(SALIDA / f"{nombre}.png", bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


def limpiar_eje_y(ax):
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)


def rotulo_panel(ax, letra):
    ax.text(0, 1.06, letra, transform=ax.transAxes, fontsize=9, color=GRIS_OSC, va="bottom", ha="left", fontweight="bold")


# --------------------------------------------------------------------------------------
# Figura 1. Flujo de trabajo (diagrama; no lleva datos)
# --------------------------------------------------------------------------------------
def fig_flujo():
    fig, ax = plt.subplots(figsize=(7.0, 2.7))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 40)
    ax.axis("off")

    def caja(x, w, titulo, texto, relleno="#eef2f0"):
        ax.add_patch(FancyBboxPatch((x, 17), w, 21, boxstyle="round,pad=0,rounding_size=1.6", fc=relleno, ec="none"))
        ax.text(x + w / 2, 34.2, titulo, ha="center", va="center", fontsize=8.6, fontweight="bold")
        ax.text(x + w / 2, 25.2, texto, ha="center", va="center", fontsize=7.2, color=GRIS_OSC, linespacing=1.4)

    xs = [0, 20.5, 41, 61.5, 82]
    caja(xs[0], 18, "Insumos", "4 diseños de\nEPILAB, 7 artículos,\ngenomas y\ntranscriptomas")
    caja(xs[1], 18, "Benchmark", "3 herramientas\nsobre los 4 genes")
    caja(xs[2], 18, "Motor", "criterio de si-Fi21\nreimplementado\ny verificado")
    caja(xs[3], 18, "Riesgo y\nconservación", "6 organismos\nno objetivo\n3 transcriptomas\n2 genomas")
    caja(xs[4], 18, "Sensibilidad", "4.368 configu-\nraciones y 2.000\nsorteos de pesos")
    for x in xs[:-1]:
        ax.annotate("", xy=(x + 20.2, 27.5), xytext=(x + 18.4, 27.5),
                    arrowprops=dict(arrowstyle="-|>", color=GRIS, lw=0.9, mutation_scale=8))
    ax.add_patch(FancyBboxPatch((0, 4.5), 100, 8.5, boxstyle="round,pad=0,rounding_size=1.6", fc="#fbeee8", ec="none"))
    ax.text(50, 8.7, "Recomendación defendida, con su riesgo, sus incertidumbres y lo que la refutaría",
            ha="center", va="center", fontsize=8.4, fontweight="bold")
    ax.text(50, 0.4, "Anclas que reproducen cifras publicadas  ·  criterio escrito antes de calcular  ·  sin secuencias de EPILAB en el repositorio",
            ha="center", va="center", fontsize=6.8, color=GRIS_OSC)
    guardar(fig, "fig1_flujo")


# --------------------------------------------------------------------------------------
# Figura 2. Benchmark de off-target en los dos genes virales
# --------------------------------------------------------------------------------------
def fig_benchmark():
    # research/ola2/W7_ranking/benchmark_tres_herramientas.md §3 (tablas de MP_MRFV y CP_MRFV):
    # columna «dsRNA-Engineer» y columna «exacto bloque >=19». Referencias no objetivo, sin D. maidis
    # (otro ensamblado en cada herramienta, no comparable).
    refs = ["maíz", "colémbolo", "abeja", "H. vitripennis", "vaquita"]
    datos = {
        "MP_MRFV": ([215, 63, 56, 50, 9], [3, 7, 0, 3, 0]),
        "CP_MRFV": ([87, 49, 31, 29, 9], [0, 0, 0, 0, 0]),
    }
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.6), sharex=True)
    for ax, (gen, (herr, exacto)) in zip(axs, datos.items()):
        ys = range(len(refs))
        ax.barh([y - 0.19 for y in ys], herr, height=0.34, color=GRIS)
        ax.barh([y + 0.19 for y in ys], exacto, height=0.34, color=AZUL)
        for y in ys:
            ax.text(herr[y] + 4, y - 0.19, str(herr[y]), va="center", fontsize=7.6, color=GRIS_OSC)
            ax.text(exacto[y] + 4, y + 0.19, str(exacto[y]), va="center", fontsize=7.6, color=AZUL)
        ax.set_yticks(list(ys))
        ax.set_yticklabels(refs, fontsize=8)
        ax.invert_yaxis()
        ax.set_xlim(0, 245)
        ax.set_xticks([])
        ax.spines["bottom"].set_visible(False)
        ax.set_title(gen, fontsize=8.8, loc="left", fontweight="bold", color=TINTA)
        limpiar_eje_y(ax)
    axs[1].set_yticklabels([])
    fig.legend(handles=[Rectangle((0, 0), 1, 1, color=GRIS), Rectangle((0, 0), 1, 1, color=AZUL)],
               labels=["lo que informa dsRNA-Engineer", "coincidencias exactas de ≥ 19 nt (nuestro tamizaje)"],
               loc="upper center", ncol=2, frameon=False, fontsize=8, bbox_to_anchor=(0.5, 1.07))
    fig.tight_layout(w_pad=1.5)
    guardar(fig, "fig2_benchmark")


# --------------------------------------------------------------------------------------
# Figura 3. El motor reproduce el original; y la brecha con la planilla
# --------------------------------------------------------------------------------------
def fig_verificacion():
    # research/ola2/W5_secuencias_epilab/sifi21_reproduccion.md §0 y tools/sifi21_port/README.md:
    # si-Fi21 con su interfaz y RNAplfold 2.1.5 -> 212, 133, 42, 32; el port en modo fiel, los mismos.
    genes_a = ["BicC_Dm", "MP_MRFV", "ATPaseD_Dm", "CP_MRFV"]
    valor_a = [212, 133, 42, 32]
    # research/ola5/N1_regla_de_conteo/REPORT.md: 138,40,218,35 -> 114,35,199,33 (orden MP, CP, BicC, ATPaseD)
    genes_b = ["MP_MRFV", "CP_MRFV", "BicC_Dm", "ATPaseD_Dm"]
    antes = [138, 40, 218, 35]
    despues = [114, 35, 199, 33]

    fig, (a, b) = plt.subplots(1, 2, figsize=(7.0, 2.5), gridspec_kw={"width_ratios": [1, 1.05]})
    ys = range(len(genes_a))
    a.barh(list(ys), valor_a, height=0.5, color=AZUL)
    for y, v in zip(ys, valor_a):
        a.text(v + 5, y, f"{v}, igual al original", va="center", fontsize=7.8, color=GRIS_OSC)
    a.set_yticks(list(ys))
    a.set_yticklabels(genes_a, fontsize=8.4)
    a.invert_yaxis()
    a.set_xlim(0, 380)
    a.set_xticks([])
    a.spines["bottom"].set_visible(False)
    limpiar_eje_y(a)
    a.set_title("Ventanas que pasan el criterio", fontsize=8.6, loc="left", color=TINTA)

    ys = range(len(genes_b))
    for y, x0, x1 in zip(ys, antes, despues):
        b.plot([x1, x0], [y, y], color=GRIS, lw=1.6, zorder=1)
        b.scatter([x0], [y], s=34, color=GRIS, zorder=2)
        b.scatter([x1], [y], s=34, color=AZUL, zorder=2)
        b.text(x0 + 6, y, str(x0), va="center", fontsize=7.8, color=GRIS_OSC)
        b.text(x1 - 6, y, str(x1), va="center", ha="right", fontsize=7.8, color=AZUL)
    b.set_yticks(list(ys))
    b.set_yticklabels(genes_b, fontsize=8.4)
    b.invert_yaxis()
    b.set_xlim(15, 262)
    b.set_ylim(4.0, -0.6)
    b.set_xticks([])
    b.spines["bottom"].set_visible(False)
    limpiar_eje_y(b)
    b.set_title("De las curvas a la planilla de EPILAB", fontsize=8.6, loc="left", color=TINTA)
    b.scatter([140], [3.75], s=26, color=GRIS)
    b.text(146, 3.75, "valor de las curvas", va="center", fontsize=7, color=GRIS_OSC)
    b.scatter([140], [3.3], s=26, color=AZUL)
    b.text(146, 3.3, "tras la función de conteo", va="center", fontsize=7, color=AZUL)
    fig.tight_layout(w_pad=2.2)
    guardar(fig, "fig3_verificacion")


# --------------------------------------------------------------------------------------
# Figura 4. Validacion retrospectiva con 29 siRNA
# --------------------------------------------------------------------------------------
def fig_validacion():
    d = json.loads((RAIZ / "research/ola3/C9_sensibilidad_umbral/resultados/validacion_resumen.json").read_text())
    filas = [
        ("29 siRNA, criterio principal", d["primario"]["rho"], d["primario"]["ic95"], True),
        ("29 siRNA, conteo de reglas", d["sensibilidades"]["conteo_ordinal"]["rho"], d["sensibilidades"]["conteo_ordinal"]["ic95"], False),
        ("29 siRNA, modo corregido", d["sensibilidades"]["booleano_corregido"]["rho"], d["sensibilidades"]["booleano_corregido"]["ic95"], False),
        ("28 ARNdc, confirmatorio", d["confirmatorio_28_dsrna"]["agrupado_fiel"]["rho"], d["confirmatorio_28_dsrna"]["agrupado_fiel"]["ic95"], False),
    ]
    pr = d["precision_recall"]
    base = pr["base_precision"]
    pts = pr["pr"]

    fig, (a, b) = plt.subplots(1, 2, figsize=(7.0, 2.6), gridspec_kw={"width_ratios": [1.1, 1]})
    for i, (nombre, rho, ic, principal) in enumerate(filas):
        col = AZUL if principal else GRIS_OSC
        a.plot(ic, [i, i], color=col, lw=2.2 if principal else 1.5, solid_capstyle="round")
        a.scatter([rho], [i], s=46 if principal else 30, color=col, zorder=3)
    a.axvline(0, color=GRIS, lw=0.8)
    a.axvline(0.35, color=NARANJA, lw=0.9, ls=(0, (3, 3)))
    a.text(0.37, -0.45, "0,35: lo esperable de\nun criterio bueno", fontsize=7, color=NARANJA, va="center")
    a.set_ylim(3.5, -0.9)
    a.set_yticks(range(len(filas)))
    a.set_yticklabels([f[0] for f in filas], fontsize=8)
    a.set_xlim(-0.6, 0.95)
    a.set_xlabel("correlación de Spearman con la eficacia medida (IC 95 %)", fontsize=7.8)
    limpiar_eje_y(a)
    rotulo_panel(a, "a")

    umb = [p["umbral"] for p in pts]
    prec = [p["precision"] for p in pts]
    lo = [p["ic_lo"] for p in pts]
    hi = [p["ic_hi"] for p in pts]
    b.fill_between(umb, lo, hi, color=GRIS_CLARO, lw=0)
    b.plot(umb, prec, color=AZUL, lw=1.8, marker="o", ms=3.5)
    b.axhline(base, color=NARANJA, lw=0.9, ls=(0, (3, 3)))
    b.text(0.30, base + 0.03, "aprobar todas las ventanas", fontsize=7, color=NARANJA, ha="right", va="bottom")
    b.set_ylim(0, 1.05)
    b.set_xlabel("umbral de accesibilidad", fontsize=7.8)
    b.set_ylabel("precisión del filtro", fontsize=7.8)
    rotulo_panel(b, "b")
    fig.tight_layout(w_pad=2.0)
    guardar(fig, "fig4_validacion")


# --------------------------------------------------------------------------------------
# Figura 5. Conteo frente a densidad
# --------------------------------------------------------------------------------------
def fig_densidad():
    # research/ola4/M8_que_compara_el_conteo/REPORT.md: conteo y densidad = conteo / (largo - 20) * 100
    genes = {"BicC_Dm": (212, 2520), "MP_MRFV": (133, 1263), "ATPaseD_Dm": (42, 491), "CP_MRFV": (32, 528)}
    dens = {g: c / (L - 20) * 100 for g, (c, L) in genes.items()}
    por_conteo = sorted(genes, key=lambda g: -genes[g][0])
    por_dens = sorted(genes, key=lambda g: -dens[g])

    fig, ax = plt.subplots(figsize=(5.2, 2.5))
    ax.set_xlim(-0.9, 1.9)
    ax.set_ylim(4.5, 0.3)
    ax.axis("off")
    for g in genes:
        r0, r1 = por_conteo.index(g) + 1, por_dens.index(g) + 1
        res = g == "BicC_Dm"
        ax.plot([0, 1], [r0, r1], color=AZUL if res else GRIS_CLARO, lw=2.4 if res else 1.6, zorder=2 if res else 1)
        ax.plot([0, 1], [r0, r1], "o", color=AZUL if res else GRIS, ms=4.5, zorder=3)
        ax.text(-0.05, r0, f"{g}   {genes[g][0]}", ha="right", va="center", fontsize=8.4, color=TINTA if res else GRIS_OSC)
        ax.text(1.05, r1, f"{dens[g]:.2f}   {g}".replace(".", ","), ha="left", va="center", fontsize=8.4, color=TINTA if res else GRIS_OSC)
    ax.text(-0.05, 0.4, "por conteo", ha="right", va="center", fontsize=7.6, color=GRIS_OSC)
    ax.text(1.05, 0.4, "por densidad (cada 100 ventanas)", ha="left", va="center", fontsize=7.6, color=GRIS_OSC)
    guardar(fig, "fig5_densidad")


# --------------------------------------------------------------------------------------
# Figura 6. Las tres regiones de BicC_Dm: mapa y robustez
# --------------------------------------------------------------------------------------
def fig_bicc():
    # Robustez: research/ola4/M7_robustez_bicc/resultados/tabla_unica.md (fila «en conjunto»)
    # Coincidencias perfectas con H. vitripennis: 264-563 -> 22; 922-1221 -> 0; 2121-2420 -> 0
    #   (entregables/checkpoint2-una-pagina.md y recomendacion-defendida.md §4).
    fig = plt.figure(figsize=(7.0, 3.2))
    gs = fig.add_gridspec(2, 1, height_ratios=[0.8, 1.15], hspace=0.5)
    a = fig.add_subplot(gs[0])
    a.set_xlim(0, 2520)
    a.set_ylim(0, 1)
    a.axis("off")
    a.add_patch(Rectangle((0, 0.42), 2520, 0.05, fc=GRIS_CLARO, ec="none"))
    regiones = [("264-563", 264, 563, NARANJA, "22 coincidencias perfectas"),
                ("922-1221", 922, 1221, AZUL, "0 coincidencias perfectas"),
                ("2121-2420", 2121, 2420, GRIS, "0 coincidencias perfectas")]
    for nombre, i, f, col, riesgo in regiones:
        a.add_patch(Rectangle((i, 0.36), f - i, 0.17, fc=col, ec="none"))
        a.text((i + f) / 2, 0.66, nombre, ha="center", va="bottom", fontsize=8.2, fontweight="bold")
        a.text((i + f) / 2, 0.24, riesgo, ha="center", va="top", fontsize=7.2, color=GRIS_OSC)
    a.text(2520, 0.0, "2.520 nt", fontsize=7, color=GRIS_OSC, ha="right")

    b = fig.add_subplot(gs[1])
    filas = [("922-1221 contra 264-563, molécula recortada", 99.6),
             ("922-1221 contra 264-563, en contexto", 99.1),
             ("922-1221 contra 2121-2420, molécula recortada", 75.6),
             ("922-1221 contra 2121-2420, en contexto", 36.4)]
    ys = list(range(len(filas)))
    b.barh(ys, [f[1] for f in filas], color=[AZUL, AZUL, AZUL, NARANJA], height=0.55)
    for y, f in zip(ys, filas):
        b.text(f[1] + 1.2, y, f"{f[1]:.1f} %".replace(".", ","), va="center", fontsize=7.8, color=TINTA)
    b.axvline(50, color=GRIS, lw=0.8, ls=(0, (3, 3)))
    b.set_yticks(ys)
    b.set_yticklabels([f[0] for f in filas], fontsize=7.8)
    b.invert_yaxis()
    b.set_xlim(0, 112)
    b.set_xticks([0, 50, 100])
    b.set_xticklabels(["0", "50", "100 %"], fontsize=7.4)
    b.set_xlabel("de 4.368 configuraciones de parámetros, en cuántas 922-1221 tiene más ventanas eficientes", fontsize=7.6)
    limpiar_eje_y(b)
    guardar(fig, "fig6_bicc")


# --------------------------------------------------------------------------------------
# Figura 7. La tension de la V-ATPasa
# --------------------------------------------------------------------------------------
def fig_vatpasa():
    # Supervivencia a cuatro dias por dieta: ~18 % (ARNdc de V-ATPasa D) contra ~37 % (control GFP);
    #   Jones, Bernal y Medina 2021 (preprint) -> research/ola3/C5_estructura_genes_ingenieria_inversa/catalogo_genes_blanco.md
    # Bloques perfectos >= 19 nt contra humano en 72-371: 7 observados, 2,4 esperados por azar;
    #   entregables/recomendacion-defendida.md §3 y research/ola4/M5_dos_ejes/.
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.6, 2.0))
    a.barh([0, 1], [18, 37], color=[AZUL, GRIS], height=0.5)
    for i, v in enumerate([18, 37]):
        a.text(v + 1.2, i, f"~{v} %", va="center", fontsize=8)
    a.set_yticks([0, 1])
    a.set_yticklabels(["ARNdc de V-ATPasa D", "control (GFP)"], fontsize=8)
    a.invert_yaxis()
    a.set_xlim(0, 50)
    a.set_xticks([])
    a.spines["bottom"].set_visible(False)
    limpiar_eje_y(a)
    a.set_title("Supervivencia a 4 días, por dieta", fontsize=8.4, loc="left")
    b.barh([0, 1], [7, 2.4], color=[NARANJA, GRIS], height=0.5)
    for i, v in enumerate([7, 2.4]):
        b.text(v + 0.2, i, str(v).replace(".", ","), va="center", fontsize=8)
    b.set_yticks([0, 1])
    b.set_yticklabels(["observados", "esperados por azar"], fontsize=8)
    b.invert_yaxis()
    b.set_xlim(0, 9)
    b.set_xticks([])
    b.spines["bottom"].set_visible(False)
    limpiar_eje_y(b)
    b.set_title("Bloques de ≥ 19 nt idénticos a humano (72-371)", fontsize=8.4, loc="left")
    fig.tight_layout(w_pad=2.4)
    guardar(fig, "fig7_vatpasa")


# --------------------------------------------------------------------------------------
# Figura 8. Quimeras: la juntura
# --------------------------------------------------------------------------------------
def fig_quimeras():
    tot = json.loads((RAIZ / "research/ola5/N4_quimeras/resultados/junturas.json").read_text())["totales"]
    ruta = RAIZ / ("research/ola3/C13_quimeras_region_recomendada/resultados/"
                   "quimeras_ventanas_cambiadas_vigentes_corregido_vienna.tsv")
    filas = list(csv.DictReader(open(ruta, encoding="utf-8"), delimiter="\t"))
    pierden = [int(f["nt_hasta_la_union"]) for f in filas if f["antes"] == "True" and f["ahora"] == "False"]
    ganan = [int(f["nt_hasta_la_union"]) for f in filas if f["antes"] == "False" and f["ahora"] == "True"]
    assert len(pierden) + len(ganan) == 61

    fig, (a, b) = plt.subplots(1, 2, figsize=(7.0, 2.5), gridspec_kw={"width_ratios": [1, 1.2]})
    etiquetas = ["ventanas de juntura", "con blanco continuo", "eficientes", "eficientes y con blanco"]
    valores = [tot["junturas"], tot["con_blanco"], tot["eficientes"], tot["eficientes"] - tot["efic_sin_blanco"]]
    cols = [GRIS, AZUL, AZUL, NARANJA]
    a.barh(range(4), valores, color=cols, height=0.52)
    for i, v in enumerate(valores):
        a.text(v + 4, i, str(v), va="center", fontsize=8.6, fontweight="bold")
    a.set_yticks(range(4))
    a.set_yticklabels(etiquetas, fontsize=8)
    a.invert_yaxis()
    a.set_xlim(0, 280)
    a.set_xticks([])
    a.spines["bottom"].set_visible(False)
    limpiar_eje_y(a)
    a.set_title("12 quimeras, 240 ventanas de juntura", fontsize=8.4, loc="left")

    bins = list(range(0, 72, 6))
    b.hist([pierden, ganan], bins=bins, stacked=True, color=[NARANJA, AZUL], rwidth=0.82,
           label=[f"pierden la eficiencia ({len(pierden)})", f"la ganan ({len(ganan)})"])
    b.set_xlabel("distancia a la unión (nt)", fontsize=7.8)
    b.set_yticks([0, 5, 10, 15])
    b.legend(frameon=False, fontsize=7.6, loc="upper right")
    b.set_title("61 ventanas heredadas cambian de veredicto", fontsize=8.4, loc="left")
    fig.tight_layout(w_pad=2.4)
    guardar(fig, "fig8_quimeras")


# --------------------------------------------------------------------------------------
# Figura 9. Asimetria temporal
# --------------------------------------------------------------------------------------
def fig_tiempo():
    # Latencia de S. kunkelii: 18 a 22 dias (Jones y Medina 2020, Plants 9(6):747); la cifra de ~20 dias para el
    # patogeno que importa es del investigador (checkpoint 1) y no tiene fuente abierta para el MRFV.
    # Ensayos abiertos en la especie: desenlace a los 4 o 5 dias (Jones et al. 2021; Andrada et al. 2026).
    fig, ax = plt.subplots(figsize=(6.4, 1.7))
    ax.barh(1, 5, left=0, color=AZUL, height=0.42)
    ax.barh(1, 17, left=5, color=GRIS_CLARO, height=0.42)
    ax.barh(0, 18, left=0, color="#f3e3b6", height=0.42)
    ax.barh(0, 4, left=18, color=NARANJA, height=0.42)
    ax.text(2.5, 1, "4-5 d", va="center", ha="center", fontsize=7.6, color="white", fontweight="bold")
    ax.text(13.5, 1, "sin seguimientos publicados", va="center", ha="center", fontsize=7.6, color=GRIS_OSC)
    ax.text(9, 0, "el insecto ya tiene el patógeno y todavía no transmite", va="center", ha="center", fontsize=7.4)
    ax.text(20, 0, "18-22 d", va="center", ha="center", fontsize=7.4, color="white", fontweight="bold")
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["período latente", "seguimiento de los ensayos"], fontsize=8)
    ax.set_xlim(0, 24)
    ax.set_ylim(-0.5, 1.5)
    ax.set_xlabel("días", fontsize=8)
    limpiar_eje_y(ax)
    guardar(fig, "fig9_tiempo")


if __name__ == "__main__":
    for viejo in SALIDA.glob("fig*.png"):
        viejo.unlink()
    fig_flujo()
    fig_benchmark()
    fig_verificacion()
    fig_validacion()
    fig_densidad()
    fig_bicc()
    fig_vatpasa()
    fig_quimeras()
    fig_tiempo()
    print("figuras en", SALIDA)

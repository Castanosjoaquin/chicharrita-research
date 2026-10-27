"""Genera estado.html: que esta hecho, que falta y que decisiones estan abiertas.

Por que es un script y no HTML escrito a mano: el estado del entregable ya se
declara en tres lugares de PLAN_DESARROLLO.md (la tabla de los cinco pedidos, la
cobertura de §1 bis y el cuerpo de T1 a T6). Una cuarta copia a mano se
desincroniza sola. Esta pagina NO es fuente de verdad: enlaza a la que lo es, y
verifica contra el disco que cada entregable que nombra existe de verdad.

Uso (desde la raiz del repositorio):
    python tools/generar_estado.py
"""
import html
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CSS = re.search(r"<style>(.*?)</style>",
                (RAIZ / "index.html").read_text(encoding="utf-8"), re.S).group(1)


def existe(rel):
    return (RAIZ / rel).exists()


# ---------------------------------------------------------------- contenido
# (titulo, descripcion, [rutas que respaldan la afirmacion])
HECHO = [
    ("Pedido 1 · Entender si-Fi21",
     "El port verificado contra el original, el método del artículo con la fuente de cada umbral, "
     "y la nota de método que explica que «eficiente» es un booleano por ventana de 21 nt y no un puntaje.",
     ["entregables/que-significa-eficiente.md", "research/ola3/C1_sifi21_paper_metodo", "tools/sifi21_port"]),
    ("Pedido 2 · Benchmarking de las tres herramientas",
     "si-Fi21, dsRNA-Engineer y BLAST sobre los cuatro genes, en un eje común y con el panel de "
     "referencias verificado como idéntico entre las tres.",
     ["research/ola2/W7_ranking/benchmark_tres_herramientas.md"]),
    ("Pedido 3 · Ranking con criterio explícito",
     "El orden, las cinco decisiones declaradas, la ficha por candidato y el barrido de 2.000 juegos "
     "de pesos. La segunda versión suma el panel ampliado, dos genes nuevos y los dos largos de ventana.",
     ["research/ola2/W7_ranking/REPORT.md", "research/ola3/C7_ranking_v2/REPORT.md"]),
    ("Pedido 4 · Evaluación de las regiones elegidas",
     "La región dentro de cada gen contra la distribucion de su propio gen, y la conservación entre aislados.",
     ["research/ola3/C8_conservacion"]),
    ("Pedido 5 · Crítica de las herramientas",
     "Cada crítica va con su medición o su línea de código. Lo más fuerte: la accesibilidad del sitio "
     "blanco es una de las tres condiciones de si-Fi21 y es la que no mostró valor predictivo sobre la "
     "eficacia medida.",
     ["entregables/critica-herramientas.md"]),
    ("C9 · Tarea 1 · Sensibilidad del umbral, sin etiquetas",
     "Barrido de los dos umbrales sin fuente primaria sobre 546 puntos por modo (4.368 filas). "
     "El candidato superior aguanta; la región exacta de 200 nt no. Mide fragilidad de la "
     "recomendación, no calidad del umbral.",
     ["research/ola3/C9_sensibilidad_umbral/REPORT.md",
      "research/ola3/C9_sensibilidad_umbral/resultados/grilla_umbral.tsv"]),
    ("C9 · Tarea 1 bis · El mismo barrido, sobre la región que proponemos",
     "El barrido anterior elegía en cada punto la ventana libre de 200 nt, que no es la regla con "
     "la que se eligieron las regiones del entregable. Repetido sobre la región propuesta y con el "
     "veto aplicado, a 21 y 22 nt y sobre los seis candidatos: el candidato superior sale más "
     "robusto, y el empate del tercer puesto se deshace y aparece en otros pares.",
     ["research/ola3/C9_sensibilidad_umbral/REPORT.md",
      "research/ola3/C9_sensibilidad_umbral/resultados/grilla_region_propuesta.tsv"]),
    ("C9 · Tarea 2 · Corregida la lectura del barrido de pesos",
     "La diagonal de B.3 mide la escala, no la robustez del orden. La afirmación vieja queda dicha y "
     "tachada, con la nueva y su fuente al lado, en W7 y en el ranking v2.",
     ["research/ola2/W7_ranking/REPORT.md", "research/ola3/C7_ranking_v2/REPORT.md"]),
    ("Las cuatro decisiones del checkpoint, formalizadas",
     "D33 a D36: las bacterias salen del alcance del diseño por ARNi, el objetivo es el insecto como "
     "vector, la ventana se fija en 21 y 22 nt por evidencia biológica y el ejercicio sobre los cuatro "
     "candidatos es una auditoría y no la reproducción de un resultado validado.",
     ["00_meta/DECISIONS.md"]),
    ("Validación retrospectiva corrida: no concluyente",
     "Pre-registro con tres enmiendas fechadas y la validación corrida el 2026-10-21. Primario: los 31 "
     "siRNA de <i>Tc-gawky</i>, n = 29, ρ = +0,142 con IC95 [−0,247, +0,492]; confirmatorio sobre los 28 "
     "ARNdc, ρ = +0,236. La curva precisión-recall sólo supera la base de 82,8 % en el umbral más bajo del barrido (0,02: precisión 0,875, con IC95 [0,529, 0,978] que contiene la base), y en el umbral por defecto de 0,1 queda por debajo (0,800). "
     "<b>Un nulo no refuta el puntaje</b>, y eso estaba declarado antes de mirar los datos.",
     ["research/ola3/C9_sensibilidad_umbral/RESULTADOS_validacion_retrospectiva.md",
      "research/ola3/C9_sensibilidad_umbral/PREREGISTRO_validacion_retrospectiva.md"]),
    ("C12 · ¿Cuánto vale la homología como regla?",
     "La concordancia de anotación entre cicadélidos sube de 76 % a 86 % con la identidad y no llega a 100 %. La función de la poliproteína del MRFV se transfiere a 11 de 11 marafivirus y la de la proteína de movimiento a 2 de 11; las ventanas de 21 nt compartidas con parientes son menos del 1 %. Sirve para inferir función, no para diseñar sobre otra especie (D37).",
     ["research/ola3/C12_validacion_homologia/REPORT_A.md", "research/ola3/C12_validacion_homologia/REPORT_B.md", "research/ola3/C12_validacion_homologia/PREREGISTRO.md"]),
    ("Fase 2 · ¿Cuántos genes blanco llegan a un ortólogo utilizable en <i>D. maidis</i>?",
     "Veredicto (b): viable sólo para 2 genes nominales. Ortología recíproca por secuencia resuelta en 11 de 14 familias (Swiss-Prot de artrópodos contra el proteoma de <i>M. quadrilineatus</i>). Sólo ATP synthase beta y actina superan el criterio de nucleótido (≥ 300 nt con ≥ 90 %) contra los TSA de <i>D. maidis</i>, y la actina es multigénica. Criterio fijado antes de buscar.",
     ["research/ola3/C11_diseno_nuevo/REPORT.md", "research/ola3/C11_diseno_nuevo/criterio.md", "research/ola3/C11_diseno_nuevo/sources.json"]),
    ("C10 · ¿Hay datos de ARN pequeños virales para nuestro blanco?",
     "No, y es un vacío documentado: cero registros en SRA y GEO para el <i>Maize rayado fino virus</i> y "
     "para <i>Dalbulus maidis</i> con estrategia de ARN pequeño. Los dos sustitutos abiertos que sí existen "
     "muestran que los puntos calientes no siguen la estructura del ARN y dependen del hospedador, lo que "
     "desaconseja copiarlos como selector de región blanco.",
     ["research/ola3/C10_vsirna_virus/REPORT.md", "research/ola3/C10_vsirna_virus/sources.json"]),
    ("C9 · Tarea 3 · Pre-registro de la validación retrospectiva",
     "Escrito antes de mirar los datos: que conjunto, que estadistico, qué contaría como éxito y como "
     "fracaso, y la decisión de reportar el intervalo y no el valor p. La validación no se corrió.",
     ["research/ola3/C9_sensibilidad_umbral/PREREGISTRO_validacion_retrospectiva.md"]),
    ("Checkpoint 2 · Página de siete casillas",
     "La página que se lee en diez minutos, con las siete casillas de la guía y las cifras verificadas contra sus archivos. El protagonista (D42) es el veto y el movimiento de región: las dos regiones que EPILAB eligió para los genes del insecto contienen ventanas de 21 nt idénticas a <i>H. vitripennis</i>, y moviendo la región dentro del mismo gen <code>BicC_Dm</code> pasa de 20 a 36 ventanas que pasan el filtro y de 22 a 0 coincidencias (región 922-1221, vigente por D25), con lo que queda primero de la lista del insecto en las diez combinaciones de agregación a 21 nt. Se presenta en dos listas por mecanismo (D38).",
     ["entregables/checkpoint2-una-pagina.md", "docs/plan_checkpoint2/salidas/F4_checklist_guia.md"]),
    ("Checkpoint 2 · Entrega y mecanismo (Fase 2)",
     "Qué dicen las fuentes abiertas sobre la entrega oral y el mecanismo de RNAi en insectos, con el estado de apertura de cada fuente. Las que no se pudieron abrir se declaran y no se citan.",
     ["docs/plan_checkpoint2/salidas/F2_entrega_y_mecanismo.md"]),
    ("Checkpoint 2 · Hipótesis, alternativas y validación (Fase 3)",
     "Diseño conceptual: pregunta, hipótesis con la condición que la refutaría, cinco alternativas, controles y una tabla de interpretación con el criterio de descarte escrito de antemano. No es una recomendación experimental.",
     ["docs/plan_checkpoint2/salidas/F3_hipotesis_alternativas_validacion.md"]),
    ("Checkpoint 2 · Decisiones de ranking y de etiquetas (Fase 1)",
     "D38 (dos listas por mecanismo), D39 (marcador [M] para lo medido por nosotros) y D40 (matar y esterilizar como dos ejes). Incluye la corrección de la lectura del par eth–burs-α.",
     ["docs/plan_checkpoint2/salidas/F1_decision_ranking.md", "00_meta/DECISIONS.md"]),
    ("Robustez de la región <code>BicC_Dm</code> 922-1221 en los tres ejes (M7)",
     "Sobre <strong>4.368 configuraciones</strong> —umbrales, modos, tablas de apilamiento y los dos motores de plegado— "
     "922-1221 le gana a la región que eligió el laboratorio (264-563) en el 99,1 % contando dentro del gen y en el "
     "99,6 % contando la molécula recortada, pero a 2121-2420 sólo en el 36,4 % en contexto y en el 75,6 % recortada: "
     "el marco de conteo decide tanto como los umbrales. Al cambiar de referencia queda primera en las tres fuentes que "
     "permiten compararla, y <code>GCWP01</code> no cubre un solo nucleótido de la región. El criterio de riesgo no "
     "cambia quién gana, y bajo la regla mecanicista el riesgo de las tres regiones es cero.",
     ["research/ola4/M7_robustez_bicc/REPORT.md", "research/ola4/M7_robustez_bicc/resultados/tabla_unica.md"]),
    ("Exposici\u00f3n y conservaci\u00f3n, separadas y medidas como sensibilidad (M5)",
     "El peso \u00fanico de D18 se parte en dos vectores que el motor <strong>no puede</strong> combinar, y se mide en qu\u00e9 "
     "fracci\u00f3n del espacio de repartos se sostiene cada afirmaci\u00f3n publicada: 2.000 sorteos en cada uno de nueve "
     "valores del peso de exposici\u00f3n de <i>H. vitripennis</i>. <strong>Seis de siete aguantan</strong> entre el 96,0 % y el "
     "100 %, incluido el orden de los dos primeros. La que se cae es el desempate del tercer puesto: en la cascada "
     "<code>CP_MRFV</code> va antes que <code>ATPaseD_Dm</code> en el 100 % de los sorteos mientras esa referencia "
     "conserve cualquier exposici\u00f3n, y en el <strong>0 %</strong> cuando es exactamente cero. No hay transici\u00f3n: el "
     "efecto es binario y pasa entero por el veto, no por la ponderaci\u00f3n. Con exposici\u00f3n cero vuelven a la mesa tres "
     "regiones hoy vetadas, entre ellas <code>ATPaseD_Dm</code> 137-436, la m\u00e1s conservada del gen. "
     "<strong>Mide y propone; no aplica nada.</strong>",
     ["research/ola4/M5_dos_ejes/REPORT.md",
      "research/ola4/M5_dos_ejes/resultados/tabla_afirmaciones.tsv",
      "tools/sifi21_port/ejes_separados.py"]),
    ("Las 28 secuencias de Cedden: se dejan publicadas y declaradas (D41)",
     "La tabla unida a su razón de riesgo ya estaba en el remoto desde el 2026-10-21. Son datos públicos CC BY y no secuencias de EPILAB. "
     "Se decidió dejarla publicada con la advertencia de que la unión no tiene clave publicada.",
     ["research/ola3/C9_sensibilidad_umbral/datos/LEEME.md", "00_meta/DECISIONS.md"]),

    # ----------------------------------------------------------- ola 4 (M1-M9)
    ("Reconciliación de conteos: la matriz de once bases (M1)",
     "La columna «Efficient siRNA hits» del si-Fi21 original <strong>cuenta aciertos de Bowtie en la hebra +, no "
     "ventanas</strong>, así que comparar nuestros conteos contra los de la planilla fue desde el principio comparar "
     "dos unidades distintas. La matriz corrió: once bases, treinta y ocho celdas, y una base genómica puede borrar "
     "un gen entero de la tabla —<code>ATPaseD_Dm</code> da 0—. <strong>Leer con la nota del 25-10:</strong> la "
     "discrepancia de los cuatro conteos quedó explicada por otra vía (N1, D62), y el «200 contra 199» de "
     "<code>BicC_Dm</code> era coincidencia y no un acierto parcial de la hipótesis.",
     ["research/ola4/M1_conteo_y_referencia/REPORT.md"]),
    ("Comparador ventana por ventana (M2)",
     "Lo que él pidió textualmente: no el conteo final sino <strong>cuáles ventanas cambian de clasificación</strong>. "
     "Los cuatro pares corridos, con la matriz de confusión, las posiciones que cambian y cuál de los cuatro booleanos "
     "del veredicto cambió en cada una. En <code>MP_MRFV</code> el par de modos da 142 contra 123 con 19 ventanas que "
     "cambian. El par de motores pedía un binario que no estaba en la máquina: se compiló RNAplfold 2.1.5 del fuente "
     "oficial y reproduce los cuatro conteos del binario del instalador.",
     ["research/ola4/M2_ventana_a_ventana/REPORT.md"]),
    ("La tercera vía: los términos continuos sin corte (M3)",
     "Su tercera alternativa, implementada: conservar los valores termodinámicos, las preferencias terminales y la "
     "accesibilidad como variables independientes de la clasificación. Con una corrección al propio pedido: las "
     "columnas <code>nt19</code> y <code>nt2</code> <strong>no son inocuas</strong> —sobre un gen sintético de 500 nt "
     "reconstruyen 497, el 99,4 %, sin producir una sola racha de 21 nt—, así que se publican las categorías que la "
     "regla usa y no los nucleótidos.",
     ["research/ola4/M3_features/REPORT.md"]),
    ("Cuánta evidencia haría falta para distinguir los dos modelos (M4)",
     "Del orden de <strong>2.800 siRNA</strong> con eficacia medida replicando el diseño de Cedden —2.784 en la "
     "estimación honesta, noventa y seis veces los 29 que existen—. Y un resultado más fuerte que el número: con los "
     "29 actuales la prueba <strong>no puede rechazar nunca</strong>, cualquiera sea el dato, porque los dos modos "
     "discrepan en un solo siRNA. El ensayo que sí discrimina no mide siRNA al azar: elige los discordantes, y pide "
     "32 por brazo.",
     ["research/ola4/M4_evidencia_y_potencia/REPORT.md",
      "research/ola4/M4_evidencia_y_potencia/PREREGISTRO_tercera_via.md"]),
    ("Del veto binario a la alerta justificada, y su compuerta (M6)",
     "La tabla de alertas con los cuatro campos de D48, validada, y el estado de las doce regiones bajo la regla "
     "nueva. Más <code>alertas.exigir_decidida()</code>, que se niega a tratar como usable una región con alguna "
     "fila en «pendiente» — <strong>implementada sin adoptar</strong>: ningún entregable la llama todavía. "
     "Cuando M6 la corrió, en octubre 25 y con las 17 filas sin firmar, el umbral decidía casi todo: con D48 literal "
     "pasaban <strong>9 de 12</strong> y ninguna región vigente se movía; con el umbral laxo de D28 pasaban "
     "<strong>3 de 12</strong> y se frenaban cuatro de las seis vigentes. <strong>Con las firmas puestas (D68) pasan "
     "las 12 en los dos umbrales</strong>, tres de ellas como «bloqueante» —que pasa la compuerta porque alguien las "
     "decidió, y el que llama tiene que descartarlas—. O sea que hoy los dos umbrales dan el mismo resultado "
     "operativo, y elegir uno dejó de mover nada. Qué umbral se adopta sigue siendo pregunta abierta.",
     ["research/ola4/M6_alertas/REPORT.md",
      "research/ola4/M6_alertas/resultados/alertas.tsv",
      "tools/sifi21_port/alertas.py"]),
    ("Hasta dónde compara el número de eficientes (M8)",
     "La pregunta que él dejó para pensar, contestada sin correr nada. El número compara <strong>regiones dentro de "
     "un mismo gen, con la misma configuración, la misma referencia y la misma unidad</strong>, y no compara genes "
     "entre sí: cuatro cosas que no son el blanco biológico lo mueven lo suficiente para invertir el orden de los "
     "candidatos, y las cuatro ya estaban medidas en este repositorio sin habérnoslo propuesto. Para comparar "
     "estrategias contra genes distintos el conteo es, como máximo, uno de los términos; el que decide es la "
     "evidencia de fenotipo.",
     ["research/ola4/M8_que_compara_el_conteo/REPORT.md"]),
    ("Auditoría de secuencia antes de compartir nada (M9)",
     "La verificación promovida a <code>tools/verificacion/sin_secuencias.py</code>, con tres pasadas, corrida sobre "
     "el árbol y sobre el historial y dejada como gancho de pre-commit fail-closed. Árbol e historial dan "
     "<strong>cero hallazgos no exceptuados</strong> (D61). La salvedad viaja con el cero: la pasada 3 necesita la "
     "planilla de EPILAB y <code>openpyxl</code>, y donde no están el gancho rechaza en vez de declarar un cero "
     "incompleto.",
     ["research/ola4/M9_auditoria_secuencias/REPORT.md",
      "tools/verificacion/sin_secuencias.py"]),

    # ---------------------------------------------------------- ola 5 (N1-N10)
    ("La función histórica de conteo, reproducida con insumos propios (N1)",
     "Su explicación es correcta y <strong>se verificó sin pedirle un archivo</strong>: la curva asigna 20 posiciones "
     "de cobertura a cada ventana de 21 nt y el contador registra los incrementos positivos, de modo que cuando una "
     "ventana eficiente termina donde otra empieza los dos efectos se compensan y la segunda no se cuenta. Aplicada a "
     "las ventanas eficientes de nuestro propio port, los cuatro valores de la planilla salen exactos. Es D62.",
     ["research/ola5/N1_regla_de_conteo/REPORT.md"]),
    ("El ancho de cobertura: son dos curvas distintas (N2)",
     "Duda propia que abrió N1: si la función histórica asigna 20 posiciones por ventana y nuestro módulo asigna 21, "
     "¿cuál está mal? <strong>Ninguna.</strong> Las tres marcas que la pantalla del original dejó registradas "
     "coinciden con ancho 21 y caen un nucleótido antes con ancho 20. El «20 por ventana» de su carta describe la "
     "curva que EPILAB guarda en su base, no el gráfico del si-Fi21.",
     ["research/ola5/N2_ancho_de_cobertura/REPORT.md"]),
    ("Los tres marcos de conteo, y la partición de la diferencia (N3)",
     "El tercer marco que él propuso —las ventanas de la molécula con la accesibilidad evaluada en el transcrito "
     "blanco— medido: da <strong>29</strong>, contra 36 en contexto y 26 en la molécula. Y la diferencia queda "
     "partida: 36 = 29 + 7 y 26 = 29 − 3. Cada conteo se publica con su marco declarado (D63). Dos de las cuatro "
     "fuentes del eje de referencia no tienen marco intermedio y el motivo está escrito: una necesita un contig que "
     "no está en la máquina y <code>GCWP01</code> no es un pendiente sino un límite.",
     ["research/ola5/N3_marcos/REPORT.md"]),
    ("Las ventanas de juntura: eficientes y sin blanco (N4)",
     "La segunda mitad de su punto 3, que nadie había mirado: de las <strong>240</strong> ventanas de juntura de las "
     "doce quimeras, <strong>4 son eficientes y ninguna de esas 4 tiene blanco continuo</strong> de 21 nt; las 8 que "
     "sí tienen blanco son todas de los extremos de la unión y ninguna es eficiente. Una quimera no agrega ventanas: "
     "<strong>canjea</strong> los veinte arranques de cola de cada fragmento por veinte de juntura. Y la otra mitad, "
     "que la intuición da por segura: la banda de contexto cambió el veredicto de <strong>61 ventanas heredadas</strong>, "
     "quince veces más que el empalme.",
     ["research/ola5/N4_quimeras/REPORT.md",
      "entregables/quimeras-juntura-y-contexto.md"]),
    ("Ficha: las 4.368 configuraciones y la identidad de C7 (N5)",
     "Sus dos pedidos explícitos del punto 5, sin correr nada: qué son exactamente las 4.368 configuraciones —el "
     "producto de cinco ejes, medidas además en dos marcos, de donde salen las 13.104 filas de la grilla— y cuál es "
     "la región de C7 que entra en la comparación.",
     ["research/ola5/N5_ficha_grilla/REPORT.md"]),
    ("El port, empaquetado y auditado para mostrárselo (N9)",
     "La auditoría del paquete autocontenido en verde: <strong>36 archivos</strong>, cuatro con nucleótidos y los "
     "cuatro con su fuente pública escrita, <strong>cero hallazgos sin exceptuar</strong>. Lo pidió dos veces y "
     "queda listo; lo único que falta es el canal, que es una acción hacia afuera.",
     ["research/ola5/N9_paquete_port/REPORT.md"]),
    ("La función histórica aplicada a regiones: el 36 contra 35 es un empate (N10)",
     "No sale de la carta: sale de la pregunta que abrió N1 y que no estaba en el plan. Si la planilla construyó "
     "también los conteos de región con el contador histórico, el orden entre candidatas podría no ser el mismo. "
     "Medido: <strong>lo es en dos de los tres marcos y no en el tercero</strong>. En el marco de contexto la ventaja "
     "de <code>BicC_Dm</code> 922-1221 sobre la región de C7 —36 contra 35, una ventana— <strong>se convierte en un "
     "empate, 33 a 33</strong>. Contra la región del laboratorio la ventaja no se mueve en ningún marco.",
     ["research/ola5/N10_conteo_historico_por_region/REPORT.md"]),

    ("Las 17 alertas de off-target, firmadas (D68)",
     "D48 había invertido el default: el veto descartaba por omisión y la tabla que lo reemplazó no descartaba "
     "nada, así que <strong>una alerta no leída quedaba operativamente igual que una aceptada</strong>. Las 17 "
     "filas quedan decididas: <strong>14 aceptadas y 3 bloqueantes</strong>. Las tres bloqueantes son las únicas "
     "con coincidencia perfecta de 21 nt, las tres contra el ortólogo del gen que se silencia en "
     "<i>H. vitripennis</i>, y las tres sobre regiones que no recomendamos. La de <code>ATPaseD_Dm</code> 137-436 "
     "lleva su condición escrita, porque aceptarla adoptaría exposición cero por la ventana y eso es justo lo que "
     "D66 decidió no hacer. <strong>Y la firma dejó de vivir en la tabla:</strong> "
     "<code>tabla_alertas.py</code> la reescribía entera en cada corrida, así que una firma a mano se perdía sin "
     "aviso; ahora es un archivo de entrada y regenerar la tabla da un resultado idéntico byte a byte.",
     ["00_meta/DECISIONS.md", "research/ola4/M6_alertas/decisiones.tsv",
      "research/ola4/M6_alertas/REPORT.md"]),

    # -------------------------------------------------------------- checkpoint 2
    ("Checkpoint 2 · La reunión, transcripta y mapeada",
     "El acta de la reunión del 26 de octubre, con las transcripciones crudas auditables al lado —cinco audios "
     "transcriptos localmente con <code>faster-whisper large-v3</code>—. <strong>No corrigió nada de fondo:</strong> "
     "validó la lectura de <code>BicC_Dm</code> como gen poblacional, volvió a validar la ruta de homología y pidió "
     "el análisis de sensibilidad a los pesos que ya estaba hecho. De los ocho puntos que salieron, "
     "<strong>cinco ya estaban cerrados</strong>, uno depende del transcriptoma que ofreció mandar, uno es de "
     "presentación y <strong>uno solo es trabajo nuevo</strong>: las quimeras por combinación de fenotipos (D67). "
     "Dos salvedades declaradas: cuatro de los cinco audios no son su voz sino la propuesta de un compañero, y la "
     "primera parte de la reunión no tiene registro.",
     ["research/checkpoints/checkpoint2.md", "docs/plan_cierre/PLAN_CIERRE.md",
      "docs/plan_ola6/PLAN_OLA6.md"]),
]

FALTA = [
    ("Las dos cifras viejas de los entregables (issue #19)", "decision", True,
     "<strong>La decisión ya está tomada; falta aplicarla.</strong> D63 fijó que la cifra que se publica para una "
     "región candidata es la del marco de la molécula, que es <strong>26</strong>; D64 retiró el «32 idénticas contra "
     "22» y lo reemplazó por la cobertura declarada por fuente, porque <code>GCWP01</code> no cubre un solo "
     "nucleótido de 922-1221; y D65 le retiró al conteo el papel de argumento entre 922-1221 y 2121-2420. Pero "
     "<code>entregables/checkpoint2-una-pagina.md</code> y <code>entregables/para-el-investigador.md</code> siguen "
     "diciendo «pasa de 20 a 36» y «32 de sus 36», mientras <code>recomendacion-defendida.md</code> y "
     "<code>reunion-lunes.html</code> publican 26. No se corrige por cuenta propia: <strong>cambia cifras "
     "publicadas</strong>, y la convención del repositorio es dejar la frase vieja tachada con la nueva al lado."),
    ("El tercer marco y el empate declarado (issue #20)", "decision", True,
     "Dos decisiones chicas, las dos con la medición hecha. <strong>El tercer marco:</strong> él lo propuso en la "
     "carta del 25 y N3 lo midió —da <strong>29</strong>, contra 36 en contexto y 26 en la molécula—; se sigue "
     "publicando 26 y la adopción quedó sin decidir. En la reunión del 26 no lo volvió a mencionar, así que la "
     "decisión es nuestra. <strong>El tercer puesto:</strong> si se reporta como empate declarado o se sigue "
     "ordenando. D66 cerró lo que bloqueaba a las dos: la exposición de <i>H. vitripennis</i> se declara como "
     "decisión abierta y <strong>no se le pide un número</strong> —dijo que el organismo no está en la Argentina y "
     "«puede no importar», y también que «puede venir eventualmente»—. Lo que pidió es que la decisión esté "
     "explicitada, con los dos extremos a la vista."),
    ("Que un entregable llame de verdad a la compuerta (issue #16)", "trabajo", False,
     "<code>alertas.exigir_decidida()</code> está implementada y probada, pero <strong>ningún entregable la "
     "llama</strong>: las únicas referencias fuera de la prueba están en un script de la ola 4 y en los REPORT. Una "
     "compuerta que nadie llama no es una compuerta, y hoy nada en el código impide usar una región sin mirar su "
     "fila. <strong>Dejó de estar bloqueada el 2026-10-26:</strong> esperaba a que las 17 alertas estuvieran "
     "firmadas, y lo están (D68), así que la compuerta ya pasa sobre las seis regiones vigentes en los dos umbrales "
     "de D28 y se puede llamar sin congelar nada. Lo que sigue sin decidirse es <em>qué umbral</em> adopta."),
    ("La secuencia de <code>V-ATPase B</code> (issue #22)", "trabajo", False,
     "Es el único insumo que bloquea lo único realmente nuevo que dejó el checkpoint 2. <code>DM-02</code> está en "
     "el catálogo de C5 con fenotipo publicado en la especie —<strong>alas deformes</strong>, supervivencia 16 % al "
     "día 4 contra 37 % del control— pero <strong>sin secuencia en el panel de trabajo</strong>. Dos vías: el zip "
     "que él ofreció mandar, o <strong>recuperarla por homología a nivel proteína</strong> contra los tres "
     "transcriptomas públicos, que ya están en disco como bases de búsqueda. La segunda no espera a nadie, y si no "
     "sale, el resultado útil es saber que esos transcriptomas no la contienen."),
    ("La quimera <code>BicC_Dm</code> + <code>V-ATPase B</code> (issue #23)", "trabajo", False,
     "D67 decidió que las quimeras se arman por <strong>combinación de fenotipos que no se solapan</strong> y no por "
     "densidad de ventanas eficientes. La combinación cubre los dos ejes que a <code>BicC_Dm</code> le faltan, y los "
     "candidatos ya estaban en el catálogo: no hay que salir a buscarlos. Es la única línea de cómputo nueva. Dos "
     "obstáculos declarados: el evaluador de quimeras tiene los cuatro genes de EPILAB <strong>fijos</strong> y hay "
     "que generalizarlo, y la corrida <strong>necesita ViennaRNA</strong>, que no está en esta máquina."),
    ("<code>UMBRAL_OFF_ALERTA = 17</code> contra el piso de D28 (issue #18)", "trabajo", False,
     "<code>pipeline/region_scoring.py</code> tiene el umbral en 17 y D28 decidió no reportar coincidencias de 16 a "
     "18 nt. M6 lo dejó <em>medido y declarado, no corregido</em>. El alcance está verificado y es chico: <strong>no "
     "mueve ninguna cifra publicada</strong> y el cambio queda contenido en ese módulo. Si al correr alguna cifra se "
     "mueve, hay que parar: entonces el alcance no era el verificado."),
    ("Fecha y texto del correo enviado (issue #28)", "decision", True,
     "El correo se envió, como confirmó el usuario, pero el repo no registra la fecha ni el texto enviado. El "
     "borrador tiene siete preguntas y <code>PLAN_DESARROLLO.md</code> §8 decía cinco: sin el texto efectivamente "
     "enviado <strong>no se puede cotejar ninguna numeración</strong>, y varios documentos citan «la pregunta 4» o "
     "«el pedido 6» sin una fuente que los fije."),
    ("El canal por el que se le entrega el port (issue #28)", "decision", False,
     "La auditoría está hecha y en verde (N9) y lo pidió dos veces. Falta elegir el canal: paquete autocontenido —la "
     "recomendación, porque no arrastra nada derivado de las secuencias de EPILAB— o acceso al repositorio privado. "
     "<strong>El canal se abrió solo en la reunión:</strong> él va a escribir para mandar el zip, y responder ese "
     "correo con el paquete es el momento natural."),
    ("Escribir el criterio de commits como enmienda a D5", "decision", False,
     "D5 decidió que las investigaciones no commitean y que el orquestador hace un commit por informe integrado. "
     "Desde la ola 4 la práctica es otra y está asentada —un commit por línea, con el issue asignado antes de "
     "empezar— y funciona. Lo que falta no es decidir: es escribirlo como enmienda a D5 para que el historial y la "
     "regla digan lo mismo."),
]

LIMITES = [
    ("No hay etiquetas de eficacia para el vector",
     "Ningún dato experimental de silenciamiento en <i>Dalbulus maidis</i> respalda el umbral. Por eso el "
     "barrido mide fragilidad de la recomendación y no si el umbral es correcto: lo segundo necesita "
     "etiquetas que no existen."),
    ("Los conteos absolutos de los dos motores no son comparables entre sí",
     "<s>No hay RNAplfold 2.1.5 en la máquina (el que instala si-Fi21 es un ejecutable de Windows), así que "
     "todo corre con ViennaRNA 2.7.2.</s> <strong>Corregido el 2026-10-24:</strong> M2 compiló RNAplfold 2.1.5 "
     "desde el fuente oficial y reproduce los cuatro conteos publicados del binario del instalador, así que los "
     "dos motores corren en esta máquina y M7 los usó como eje. Sigue valiendo lo esencial: los conteos de un "
     "motor no se comparan con los del otro, y el motor mueve el resultado —en <code>BicC_Dm</code> da vuelta la "
     "comparación entre 922-1221 y 2121-2420 en el punto por defecto—. Cada número declara su motor, su tabla de "
     "apilamiento y su modo."),
    ("La validación está sub-potenciada por un factor 2,4 en n",
     "Dos ARNdc contra el mismo gen correlacionan 0,245, de modo que una correlación verdadera de 0,7 se "
     "observa como 0,35 y la potencia con n = 28 es 0,42; para 80 % harían falta n = 67. Comparar dos "
     "proxies entre si es inviable: 0,11 con atenuacion."),
    ("La unión de secuencias y desenlace no tiene clave publicada",
     "Los dos archivos adicionales de Cedden no comparten identificador. La unión es por orden dentro de "
     "cada gen y pasó 20 de 20 chequeos de consistencia con las etiquetas de predicción, pero si el orden "
     "de las dos hojas no fuera el mismo, el error no se detectaria con esos chequeos."),
]


RANKING = "research/ola3/C7_ranking_v2/resultados/ranking_v2.json"
ORDEN_GENES = ["MP_MRFV", "BicC_Dm", "CP_MRFV", "eth_Dm", "bursA_Dm", "ATPaseD_Dm"]
NUEVOS = {"eth_Dm", "bursA_Dm"}   # los dos que agrego C5; no tienen region de planilla
SIN_PLANILLA = "gen nuevo: no estaba en la planilla"


def tabla_regiones():
    """Las seis regiones, leidas del JSON del ranking v2 en vez de copiadas a mano."""
    if not existe(RANKING):
        return ('<p class="lead" style="color:var(--stop)">No se encontró %s en disco.</p>'
                % html.escape(RANKING))
    d = json.loads((RAIZ / RANKING).read_text(encoding="utf-8"))
    filas = []
    for g in ORDEN_GENES:
        planilla = d["k"]["21"]["regiones"][g]
        prop21 = d["k"]["21"]["regiones_recomendadas"][g]
        prop22 = d["k"]["22"]["regiones_recomendadas"][g]
        nueva = g not in NUEVOS
        filas.append(
            "<tr><td><code>%s</code></td><td>%s</td><td><strong>%s</strong></td>"
            "<td>%s</td><td>%s</td></tr>"
            % (html.escape(g),
               html.escape(planilla) if nueva else "—",
               html.escape(prop21), html.escape(prop22),
               "" if nueva else SIN_PLANILLA))
    return ('<div class="tw"><table>\n<thead><tr><th>Gen</th><th>Región de la planilla</th>'
            "<th>La que proponemos, 21 nt</th><th>22 nt</th><th></th></tr></thead>\n"
            "<tbody>\n%s\n</tbody></table></div>" % "\n".join(filas))


def tarjeta(titulo, desc, rutas):
    faltantes = [r for r in rutas if not existe(r)]
    def etiqueta(r):
        q = Path(r)
        # REPORT.md hay uno por investigacion: sin la carpeta, dos enlaces quedan
        # indistinguibles ("REPORT.md · REPORT.md").
        return "%s/%s" % (q.parent.name, q.name) if q.name in ("REPORT.md", "index.html") else q.name
    enlaces = " · ".join(
        '<a href="%s">%s</a>' % (html.escape(r), html.escape(etiqueta(r)))
        for r in rutas if existe(r))
    aviso = ("" if not faltantes else
             '<p class="f" style="color:var(--stop)">No encontrado en disco: %s</p>'
             % html.escape(", ".join(faltantes)))
    return ('<div class="card"><p class="t">%s</p><p class="d">%s</p>'
            '<p class="f">%s</p>%s</div>' % (html.escape(titulo), desc, enlaces, aviso))


hechos = "\n".join(tarjeta(t, d, r) for t, d, r in HECHO)
sin_disco = sum(1 for _, _, rs in HECHO for r in rs if not existe(r))

filas = "\n".join(
    '<tr><td>%s%s</td><td>%s</td><td>%s</td></tr>'
    % ('<strong>' + html.escape(t) + '</strong>' if urg else html.escape(t),
       ' <span class="tag q">?</span>' if urg else '',
       'decisión del equipo' if k == 'decision' else 'trabajo',
       d)
    for t, k, urg, d in FALTA)

regiones = tabla_regiones()

limites = "\n".join('<h3>%s</h3><p>%s</p>' % (html.escape(t), d) for t, d in LIMITES)

# No se incrusta el último commit ni el estado de la rama. La página se genera antes de
# commitearse, así que el hash que mostraría es siempre el del commit anterior y la rama
# siempre figura como desincronizada: no puede estar al día consigo misma. Para eso está
# `git log`, que además no miente.

n_dec = sum(1 for _, k, _, _ in FALTA if k == "decision")
n_tra = len(FALTA) - n_dec


CUENTA = {2: "dos", 3: "tres", 4: "cuatro", 5: "cinco", 6: "seis", 7: "siete", 8: "ocho"}


def contar(n, singular, plural):
    """«tres decisiones», «un trabajo chico»: el número en letras hasta ocho.

    El singular llega con su artículo, porque el género lo decide el sustantivo
    y no el contador: «una decisión» pero «un trabajo».
    """
    return singular if n == 1 else "%s %s" % (CUENTA.get(n, str(n)), plural)


doc = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Estado del entregable — que esta hecho y que falta</title>
<style>{CSS}</style></head><body>
<div class="wrap">
<header>
  <p class="eyebrow">Investigathón Y-Hat · track chicharrita del maíz</p>
  <h1>Qué está hecho y qué falta</h1>
  <p class="sub">Foto del entregable al <strong>2026-10-26</strong>, después del checkpoint 2.
  Generada con <code>tools/generar_estado.py</code>, que comprueba contra el disco que cada archivo
  nombrado existe. <strong>Esta página no es fuente de verdad</strong>: el estado se declara en
  <a href="PLAN_DESARROLLO.md">PLAN_DESARROLLO.md</a> (§1 bis y §3 ter), el plan vigente está en
  <a href="docs/plan_ola6/PLAN_OLA6.md">PLAN_OLA6.md</a>, y cada afirmación vive en el informe que
  enlaza.</p>
  <p class="sub"><a href="index.html">← Volver a la portada</a></p>
</header>

<div class="verdict">
<p><strong>Los cinco pedidos del Checkpoint 1 están cerrados</strong>, más los dos opcionales, y las
cinco olas de investigación tienen entregable: las nueve líneas de la ola 4 y las siete de la ola 5
están cerradas. <strong>No queda ninguna medición grande pendiente</strong>, y de los ocho puntos
que dejó el checkpoint 2, cinco ya estaban cerrados. Lo que sigue son
<strong>{contar(n_dec, "una decisión", "decisiones")} y
{contar(n_tra, "un trabajo chico", "trabajos chicos")}</strong>, no producir el
entregable.</p>
<p><strong>Lo que bloquea de verdad es una sola cosa, y no es una medición:</strong> cuatro
entregables no dicen la misma cifra para la misma región. D63 a D65 ya decidieron que se publica
26 y dos documentos viejos siguen diciendo 36, así que alguien que abra el repositorio ve números
que se contradicen entre sí. Las 17 alertas de off-target, que eran el otro bloqueo, quedaron
firmadas el 26 de octubre (D68). Lo único realmente nuevo que dejó la reunión es la quimera por
combinación de fenotipos, y su único insumo faltante es la secuencia de <code>V-ATPase B</code>.
El tablero completo, features de plataforma incluidas, está en el
<a href="https://github.com/Castanosjoaquin/chicharrita-research/issues/29">índice de la ola 6</a>.</p>
</div>

<h2>Lo que está hecho</h2>
<p class="lead">Cada tarjeta enlaza el archivo que la respalda. Verificación automática de esta
corrida: <strong>{"todos los archivos existen" if sin_disco == 0 else f"{sin_disco} archivo(s) nombrados no están en disco"}</strong>.</p>
<div class="toc">
{hechos}
</div>

<h2>Lo que falta</h2>
<p class="lead">Ordenado por lo que bloquea. Lo marcado con <span class="tag q">?</span> es lo que
hay que decidir antes de seguir.</p>
<div class="tw"><table>
<thead><tr><th>Qué</th><th>Tipo</th><th>Por qué</th></tr></thead>
<tbody>
{filas}
</tbody></table></div>

<h2>Los límites que viajan con todo lo anterior</h2>
<p class="lead">Ninguno invalida el entregable; todos cambian cómo se leen sus números, y están
declarados en cada informe.</p>
{limites}

<h2>Las regiones que proponemos</h2>
<p class="lead">Lo que cambia respecto de la planilla de EPILAB no es el conjunto de genes sino
<strong>qué tramo de cada uno se sintetiza</strong>. La tabla se arma leyendo
<code>ranking_v2.json</code>, no a mano. Los dos genes del insecto van a 300 nt, que es el largo
del amplicón de la planilla; los otros cuatro, a 200. <strong>Salvedad para
<code>BicC_Dm</code>:</strong> la tabla muestra lo que devolvió el ranking (2121-2420), pero la
recomendación vigente es <strong>922-1221</strong> desde D25, elegida por conservación entre
fuentes; cambiarla no mueve el orden (94,2 % de los sorteos lo conservan). La tabla no se edita a
mano, así que la salvedad va acá.</p>
{regiones}
<p class="lead" style="margin-top:14px">Las dos recomendaciones que importan, las del insecto, no
se apoyan en la densidad sino en el <strong>veto</strong>: la región de <code>BicC_Dm</code> que
eligió la planilla contiene 22 ventanas con coincidencia perfecta de 21 nt en
<i>Homalodisca vitripennis</i> y la que proponemos, cero
(<a href="research/ola2/W7_ranking/REPORT.md">W7 §2.2</a>). El orden que sale de ellas, con los dos
genes nuevos y los dos largos de ventana, está en
<a href="research/ola3/C7_ranking_v2/REPORT.md">C7 v2</a>.</p>

<h2>El resultado de C9 en una línea</h2>
<p class="lead">El <strong>candidato</strong> superior es robusto al umbral y las
<strong>coordenadas exactas</strong> no lo son. Reeligiendo la región con la regla del ranking
—largo propio del gen y veto aplicado— <code>MP_MRFV</code> queda primero en el
<strong>100 %</strong> de la grilla a 21 nt y en el 98,0–99,6 % a 22 nt. Lo que no aguanta es
congelar las coordenadas: con las regiones fijas y el umbral moviéndose queda primero en el 62 %.
Lo defendible es entregar una <strong>región candidata, no un sitio</strong>, y declarar con qué
umbral se corrió.</p>
<p class="lead">El par <code>ATPaseD_Dm</code> contra <code>CP_MRFV</code> <strong>no</strong> es
un empate práctico a 21 nt: se da vuelta en el 3,3 % de la grilla. El 48,9 % que decía la primera
versión de C9 salía de medir la ventana libre de 200 nt, que en <code>ATPaseD_Dm</code> cae sobre
una región <strong>vetada</strong>. Los empates que sí quedan son <code>CP_MRFV</code> contra
<code>burs-alpha</code> y <code>eth</code> contra <code>burs-alpha</code>: el orden de los tres
últimos puestos no se sostiene.
<a href="research/ola3/C9_sensibilidad_umbral/index.html">Leer C9</a>.</p>

<footer>
  <p>Marcadores de evidencia: <span class="tag e">E</span> establecido ·
  <span class="tag r">R</span> reportado · <span class="tag">H</span> hipótesis nuestra ·
  <span class="tag q">?</span> incierto o en conflicto entre fuentes.</p>
  <p>Las secuencias de EPILAB y cualquier dato no publicado del corpus no se suben a servicios web
  de terceros ni al repositorio público. Todo análisis de esas secuencias corre con herramientas
  locales.</p>
</footer>
</div>
</body></html>
"""

(RAIZ / "estado.html").write_text(doc, encoding="utf-8")
print("escrito estado.html (%d bytes); archivos nombrados que faltan en disco: %d"
      % (len(doc), sin_disco))

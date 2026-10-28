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
     "La página que se lee en diez minutos, con las siete casillas de la guía y las cifras verificadas contra sus archivos. El protagonista (D42) es el veto y el movimiento de región: las dos regiones que EPILAB eligió para los genes del insecto contienen ventanas de 21 nt idénticas a <i>H. vitripennis</i>, y moviendo la región dentro del mismo gen <code>BicC_Dm</code> pasa de 17 a <strong>26</strong> ventanas que pasan el filtro en la molécula de 300 nt (D63; 20 a 36 contando los arranques en el gen) y de 22 a 0 coincidencias (región 922-1221, vigente por D25), con lo que queda primero de la lista del insecto en las diez combinaciones de agregación a 21 nt. Se presenta en dos listas por mecanismo (D38).",
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
     "fila en «pendiente» — implementada sin adoptar entonces, y <strong>adoptada el 27 de octubre</strong> por D69. "
     "Cuando M6 la corrió, en octubre 25 y con las 17 filas sin firmar, el umbral decidía casi todo: con D48 literal "
     "pasaban <strong>9 de 12</strong> y ninguna región vigente se movía; con el umbral laxo de D28 pasaban "
     "<strong>3 de 12</strong> y se frenaban cuatro de las seis vigentes. <strong>Con las firmas puestas (D68) pasan "
     "las 12 en los dos umbrales</strong>, tres de ellas como «bloqueante» —que pasa la compuerta porque alguien las "
     "decidió, y el que llama tiene que descartarlas—. O sea que hoy los dos umbrales dan el mismo resultado "
     "operativo, y elegir uno dejó de mover nada. <strong>D69 eligió el literal</strong> y dejó el otro medido.",
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

    ("La compuerta de alertas deja de ser una función que nadie llama (D69)",
     "<code>alertas.exigir_decidida()</code> tenía prueba desde M6 y <strong>ninguna ruta la llamaba</strong>: fuera "
     "de la prueba, la única llamada estaba en un script de inventario de la ola 4. Ahora la llama "
     "<code>ranking.region_recomendada()</code>, que es <strong>el único lugar del port donde el primer puesto del "
     "orden se convierte en una región recomendada</strong>: antes esa conversión estaba escrita tres veces, idéntica "
     "y sin consultar la tabla. Una región con una fila en «pendiente» no sale de ahí. <strong>El umbral quedó "
     "decidido:</strong> <code>perfecto_21</code>, que es D48 literal, como nombre configurable y no escrito en el "
     "cuerpo de la llamada; con las 17 firmas los dos umbrales de D28 dan el mismo resultado, y sin firmas el literal "
     "frenaba 3 de 12 regiones y el laxo 9 de 12, cuatro de ellas vigentes. <strong>Lo que la compuerta no puede "
     "hacer cumplir</strong> quedó escrito: no distingue «se tamizó y no hay alertas» de «no se tamizó», así que "
     "protege las doce regiones evaluadas y no una propuesta nueva.",
     ["00_meta/DECISIONS.md", "tools/sifi21_port/ranking.py",
      "research/ola4/M6_alertas/resultados/umbral_compuerta.json"]),

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

    # ------------------------------------------------------- ola 6, lo que se cerro
    ("Ola 6 · Las dos cifras viejas de los entregables (issue #19)",
     "Los cuatro entregables dicen ahora la misma cifra para la misma región y el mismo marco, con "
     "<strong>la frase vieja tachada y la nueva al lado</strong>, que es la convención del repositorio. La cifra "
     "de <code>BicC_Dm</code> 922-1221 es <strong>26</strong>, del marco de la molécula (D63), y 36 queda "
     "declarada como el conteo de arranques en el gen; el «32 de 36 contra 22» se reemplazó por la cobertura "
     "declarada por fuente (D64): 36 de 36 en el transcriptoma argentino, 32 de 36 en el de Ohio y "
     "<strong>sin datos</strong> en el de Illinois, que no cubre esa región. Queda dicho que el conteo ya no "
     "arbitra entre 922-1221 y 2121-2420 (D65). <code>recomendacion-defendida.md</code> y "
     "<code>reunion-lunes.html</code> no necesitaron cambio: el «36 contra 35» de la segunda está dentro del "
     "párrafo que <em>retira</em> ese argumento, no es una cifra vieja sin corregir.",
     ["entregables/checkpoint2-una-pagina.md", "entregables/para-el-investigador.md"]),
    ("Ola 6 · El tercer marco y el empate declarado (issue #20)",
     "Las dos decisiones, escritas sin correr ningún cálculo: las cifras se leyeron de los resultados "
     "versionados de N3 y M5. <strong>D79 — el tercer marco:</strong> no se adopta; se sigue publicando "
     "<strong>26</strong> (la molécula sola) y se declaran 29 y 36 al lado, cada uno con su nombre, porque "
     "adoptar 29 cambiaría la cifra de las seis regiones medidas y en direcciones distintas, y compraría una "
     "decisión que el conteo ya no toma. <strong>D80 — el tercer puesto:</strong> se reporta como empate "
     "declarado, con los dos extremos y la decisión que los separa. Y contesta lo que el investigador preguntó: "
     "<strong>los pesos casi no importan, salvo el cero</strong> —el orden de los dos primeros aguanta entre "
     "96,0 y 97,4 % en todo el rango, y en la cascada nada cambia entre 0,05 y 1,00 porque el veto es binario—.",
     ["00_meta/DECISIONS.md", "research/ola4/M5_dos_ejes/REPORT.md",
      "research/ola5/N3_marcos/resultados/tres_marcos.tsv"]),
    ("Ola 6 · La secuencia de <code>V-ATPase B</code> (issue #22)",
     "El insumo que bloqueaba lo único realmente nuevo del checkpoint 2 <strong>dejó de estar bloqueado</strong>, "
     "y sin esperar el zip: se recuperó por homología local a nivel proteína (D71). Locus "
     "<code>OZ319705.1</code>, diez exones, CDS de <strong>1.503 nt</strong> y <strong>500 aa</strong>, con la "
     "traducción verificada letra por letra contra la proteína predicha; el extractor <strong>aborta</strong> si "
     "no coincide. El CDS no se versiona —la regla de confidencialidad rechaza toda racha de 21 nt— y se "
     "regenera con un comando desde los archivos que sí están versionados.",
     ["research/ola6/O2_vatpase_b/REPORT.md", "00_meta/DECISIONS.md"]),
    ("Ola 6 · La quimera <code>BicC_Dm</code> + <code>V-ATPase B</code> (issue #23)",
     "La única línea de cómputo nueva que dejó el checkpoint 2, medida bajo un preregistro escrito "
     "<strong>antes</strong> de ver ningún conteo (D74). La región de <code>V-ATPase B</code> "
     "<strong>no se eligió entre varias</strong>: de las 1.184 regiones de 300 nt que caben en su CDS "
     "<strong>sobrevive exactamente una</strong> al veto, 517-816, y lo hace sin un nucleótido de holgura —a 301 nt "
     "el gen no tiene ninguna región admisible—, porque el gen acumula 71 ventanas con coincidencia perfecta de "
     "21 nt contra el panel, mientras <code>BicC_Dm</code> en su región vigente tiene cero. El orden es "
     "<code>BicC_Dm</code> + <code>V-ATPase B</code>, decidido por el empalme y no por el conteo. La región viaja "
     "como insumo de la medición, <strong>no como región recomendada</strong>.",
     ["research/ola6/O3_quimera_bicc_vatpase_b/REPORT.md", "00_meta/DECISIONS.md"]),
    ("Ola 6 · El transcriptoma del investigador, leído (issue #25)",
     "Llegó <code>GITV01</code> —el TSA público de Ohio State, 56.117 contigs— y se le transfirió la "
     "anotación por <strong>ortología recíproca a nivel proteína</strong>, nunca por nombre de gen (D84). "
     "Cada anotación viaja con su identidad, sus dos coberturas y su banda de concordancia, y los contigs "
     "sin anotación informativa quedan <strong>contados, no filtrados</strong>. Con la regla estricta "
     "preregistrada, <strong>4.110 contigs (7,3 %)</strong> tienen recíproco con nombre informativo; con la "
     "lectura inclusiva de empates, declarada post hoc y rotulada como tal porque se escribió después de "
     "ver fallar el control positivo, <strong>7.832 (14,0 %)</strong>. "
     "El supuesto del que colgaba la única cifra de calidad —que las bandas medidas entre proteomas "
     "curados valgan para ORF de un transcriptoma— <strong>dejó de ser supuesto</strong>: se midió leyendo "
     "el mismo organismo de las dos maneras y <strong>no hay diferencia</strong> (85,0 % contra 85,0 % "
     "sobre 11.727 genes; 0,3 puntos de brecha máxima entre las cuatro bandas que deciden y 0,6 en la quinta, que por preregistro no decide; D86). De paso quedó que el "
     "<strong>81 %</strong> publicado es una <strong>cota conservadora</strong> —lo medido da 87,4 %— y no "
     "se corrigió hacia arriba, porque el preregistro lo prohibía. Ninguna salida de esta línea entra al "
     "diseño del ARNdc, y hay una prueba que lo verifica.",
     ["research/ola6/F1_transferencia_homologia/REPORT.md",
      "research/ola6/F1_transferencia_homologia/validacion_bandas/REPORT.md",
      "00_meta/DECISIONS.md"]),
    ("Ola 6 · El nivel de alerta alineado con el piso de D28 (issue #18)",
     "La contradicción que <code>M6</code> midió y dejó declarada se cierra en el código: "
     "<code>UMBRAL_OFF_ALERTA</code> pasa de <strong>17 a 19</strong> en <code>pipeline/region_scoring.py</code>, "
     "con el motivo escrito arriba de la constante, y el nivel de descarte queda en 21. Así el módulo implementa "
     "los dos niveles de D28 y <strong>deja de contar como riesgo la banda de 16 a 18 nt</strong> que D28 decidió "
     "no reportar: sobre las 23.612 ventanas de <code>baseline_dsrip/ventanas_multigen.csv</code> el umbral 17 "
     "marcaba 2.338 ventanas en alerta y el 19 marca 436, o sea que <strong>1.902 alertas, el 81,4 %</strong>, "
     "eran ruido por debajo del piso. Lo que se mueve está medido y es acotado: de las 18.032 regiones cambian "
     "sólo dos columnas, <code>n_off_alerta</code> y <code>buenos_limpios</code>; <strong>ninguna región pasa a "
     "ser apta o inapta</strong> y ninguna recomendación publicada cambia, porque el veto no depende de esta "
     "constante. El trabajo es de la sesión <code>R4</code> y quedó fuera de <code>main</code> hasta hoy; se "
     "integró renumerando su decisión a D90 y reverificando sus cuatro mediciones antes de aplicarla.",
     ["pipeline/region_scoring.py", "00_meta/DECISIONS.md", "00_meta/CAMINOS_PROBADOS.md"]),
    ("Ola 6 · De dónde salía la brecha con <code>C12</code> (pregunta 62)",
     "Al validar las bandas de <code>F1</code>, el mismo par de proteomas corrido completo dio "
     "<strong>84,7 %</strong> donde <code>C12</code> había publicado <strong>78,2 %</strong>, y eso dejaba en "
     "duda la tabla que <code>F1</code> usa para rotular cada anotación. Separado en tres pasos que cambian una "
     "sola cosa por vez, <strong>la brecha es enteramente el normalizador de nombres</strong>: aporta "
     "+7,0 puntos, el alineador +0,2 y la submuestra −0,7. <code>C12</code> no midió mal — midió con una regla "
     "que cuenta <em>isoform X1</em> e <em>isoform X8</em> como anotaciones distintas: de los 515 desacuerdos "
     "que el criterio de <code>F1</code> convierte en acuerdos, el <strong>77,9 % se separaba sólo por el "
     "sufijo de isoforma</strong> y el 21,6 % por <code>-like</code>, y no rompe ninguno. "
     "<strong>La tabla de <code>C12</code> no se tocó</strong>: es correcta para su propio criterio y es una "
     "cota inferior de la concordancia de nombre de gen; lo que se corrigió es el acople, anotado donde se usa. "
     "No se corrió ningún alineamiento nuevo: salió de archivos que ya estaban en disco.",
     ["research/ola6/R13_brecha_c12/REPORT.md", "research/ola3/C12_validacion_homologia/REPORT_A.md",
      "00_meta/DECISIONS.md"]),
    ("Ola 6 · El eje de conservación del recomendador, calculado (issues #27 y #37)",
     "El eje que <code>F3</code> había declarado no calculable se corrió en la máquina que sí tiene los tres "
     "transcriptomas de <i>D. maidis</i>. Con la regla preregistrada —presencia exacta en los <strong>tres</strong> "
     "TSA— puntuaba <strong>una</strong> de cinco filas: <code>eth</code> y <code>burs-alpha</code> no están en "
     "<code>GCWP01</code>, el ensamblado más viejo, y <code>V-ATPase B</code> quedaba a 0,033 del umbral de "
     "cobertura. La <strong>enmienda 1</strong> (dato en al menos dos de tres TSA, umbral intacto) puntúa las "
     "cinco: 0,8876, 0,9575, 0,9554, 0,9143 y 0,6706. La enmienda se escribió <strong>sabiendo el resultado</strong> "
     "y por eso las dos reglas se publican lado a lado (D94). <strong>El empate de tres del primer puesto sigue "
     "declarado</strong>: hacía falta una diferencia de más de 0,375 y la mayor es 0,043.",
     ["research/ola6/F3_recomendador_genes/PREREGISTRO_EJE4.md",
      "research/ola6/F3_recomendador_genes/resultados/eje4_REPORT.md",
      "00_meta/DECISIONS.md"]),
    ("Ola 6 · El eje de off-target, con su nulo, y lo que el nulo corrigió (issue #43)",
     "El eje más sólido del recomendador —el único que no depende del criterio de eficiencia sin validar en "
     "hemípteros— se calculó para <strong>19 de las 36 filas</strong> del catálogo, en tres lecturas que "
     "<strong>no se comparan entre sí</strong> (D97, D98, D99, D100). Y el nulo cambió cómo se lee: una secuencia "
     "sin homología trae <strong>0,5 % de ventanas con coincidencia</strong>, no cero, así que "
     "<code>eth</code> y <code>burs-alpha</code> <strong>no se distinguen del azar</strong> y sólo "
     "<code>V-ATPase B</code> (0,8827) queda claramente por encima. <strong>La conclusión que importa para el "
     "entregable:</strong> el eje <strong>no cambió ningún primer puesto</strong> —el empate de tres sigue y los "
     "cuatro primeros de la cohorte nueva caen dentro de 0,021 contra un umbral de 0,05—, lo que refuerza por otra "
     "vía lo que D65 ya había decidido sobre el conteo.",
     ["research/ola6/F3_recomendador_genes/PREREGISTRO_EJE3.md",
      "research/ola6/F3_recomendador_genes/resultados/eje3_REPORT.md",
      "research/ola6/F3_recomendador_genes/resultados/manifiesto_secuencias_eje3.tsv",
      "00_meta/DECISIONS.md"]),
    ("Ola 6 · El panel se autoacierta si contiene la especie de la secuencia (D99, D100)",
     "Apareció <strong>dos veces</strong> y por eso es una regla y no una anécdota. Cuatro filas de <code>C5</code> "
     "usan una secuencia sustituta de <i>Macrosteles quadrilineatus</i> y el panel de cinco con el que se midieron "
     "<strong>incluía</strong> esa especie: publicaban el <strong>100 %</strong> de sus ventanas como coincidencia "
     "perfecta —1835/1835, 663/663, 1487/1487, 4409/4409— que no era off-target sino la secuencia contra sí misma. "
     "El segundo caso es la actina de <code>HE-06</code>, de <i>Homalodisca vitripennis</i>, que está en el panel "
     "de seis: <strong>98,6 %</strong> de sus ventanas contra su propia especie. Ninguno es un error de quien lo "
     "midió —la sustitución estaba declarada fila por fila—: es lo que pasa cuando el panel contiene la especie de "
     "la que se tomó prestada la secuencia. <strong>La regla queda escrita y verificable:</strong> antes de tamizar, "
     "comprobar que la especie de la secuencia no esté en el panel; el valor se publica rotulado y no entra al puntaje.",
     ["research/ola6/F3_recomendador_genes/resultados/eje3_filas_c5_REPORT.md",
      "research/ola6/F3_recomendador_genes/resultados/eje3_filas_resto_REPORT.md",
      "00_meta/CAMINOS_PROBADOS.md"]),
    ("Ola 6 · La grilla fina de quimeras, archivada con su costo escrito (issue #42, D95)",
     "La retícula de <code>--paso 1</code> del enumerador <strong>no se corre</strong>, y el motivo quedó medido: "
     "no pide los 136.446 plegados que decía la prosa sino <strong>129.761.738</strong>, unos <strong>71 días</strong> "
     "de una máquina sola a los 21 plegados/s medidos. El costo de las cuatro retículas queda escrito para que nadie "
     "lo vuelva a estimar. Lo que sí se corrió, la de paso 10, dejó un resultado propio: <strong>el paso mueve el "
     "primer puesto</strong> —por <strong>una ventana</strong> sobre 65—, así que lo medido es que el orden de esa "
     "grilla <strong>no es estable al paso</strong>, no que la gruesa eligiera mal. Condición para reabrir: sólo si "
     "alguien vuelve a usar el conteo como argumento entre candidatos, y entonces <code>--paso 2</code> repartido.",
     ["00_meta/DECISIONS.md", "00_meta/CAMINOS_PROBADOS.md",
      "research/ola6/O4_enumerador_quimeras/REPORT.md"]),
    ("Ola 6 · F2 declara su límite donde se lee el código (issue #44, D96)",
     "<code>F2</code> sólo puede resumir <strong>el nombre de producto</strong>: los términos GO, los dominios "
     "conservados y los papers que su issue nombraba como entrada <strong>no están en ninguna salida versionada</strong>, "
     "porque <code>F1</code> entrega nombre de producto, identidad, cobertura y banda y nada más. La limitación se "
     "escribió en el encabezado del módulo y no en una nota al pie —<code>F2</code> no tiene <code>REPORT.md</code>, "
     "así que el lugar equivalente es el docstring—, con la regla explícita de que no se infiere función del nombre "
     "del gen: «V-ATPase» no se convierte en «letalidad». Ampliar la entrada exige una fuente nueva con su versión y "
     "su verificación de procedencia declaradas <strong>antes</strong> de correr, y eso sería una línea propia.",
     ["pipeline/evidencia_en_prosa.py", "pipeline/fichas_desde_f1.py", "00_meta/DECISIONS.md"]),
]

FALTA = [
    ("Firmar las 13 filas de alertas que siguen en «pendiente»", "decision", True,
     "La tabla de alertas tiene <strong>32 filas: 14 aceptadas, 5 bloqueantes y 13 en «pendiente»</strong>, entre "
     "ellas las <strong>cuatro de <code>V-ATPase B</code> 517-816</strong> que dejó el barrido del inventario. "
     "Ninguna la firma el motor (D48, D68, D73) y una región con alerta sin firmar <strong>no sale como "
     "recomendada</strong>, así que esto bloquea de hecho a la compuerta. El argumento que la firma tiene que "
     "atender está escrito: la de <i>H. vitripennis</i> es la única que además aporta ventanas eficientes, y el "
     "peso de exposición de ese organismo es justo la decisión que D47 dejó abierta."),
    ("Nueve filas del eje 3 cuya ausencia de accesión es provisional (entrada 102)", "insumo", False,
     "<code>HE-01</code>, <code>HE-02</code>, <code>HE-03</code>, <code>HE-09</code>, <code>HE-11</code>, "
     "<code>DM-04</code>, <code>CI-09</code>, <code>CI-11</code> y <code>CI-12</code> se cerraron leyendo "
     "<strong>sólo el resumen</strong>: el texto completo está tras un muro de pago y ninguna vía abierta lo "
     "devolvió. <strong>«No está en el resumen» no es «no está en el paper»</strong>, así que esas nueve "
     "<strong>no cuentan como evidencia</strong> de que el trabajo no depositó secuencias. Tres filas más "
     "—<code>CI-04</code>, <code>CI-05</code> y <code>DE-04</code>— tienen <strong>el PDF abierto</strong> pero su "
     "dominio no está en la lista permitida del entorno: se destraban autorizando dos dominios, no consiguiendo el paper."),
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
    ("Un conteo de off-target sin su nulo puede estar leyendo un piso, no una señal",
     "Medido al cerrar el eje 3 de <code>F3</code>: una secuencia <strong>sin homología</strong> —permutada "
     "conservando su composición— trae <strong>0,5 a 0,7 % de ventanas con un bloque de 19 nt o más coincidente</strong> "
     "contra el panel de seis, y en el peor caso 3,4 %. No es cero, que es lo que la intuición supone. Por eso "
     "<code>eth</code> (0,9815) y <code>burs-alpha</code> (1,0000) <strong>no se distinguen del azar</strong> y sólo "
     "<code>V-ATPase B</code> (0,8827) queda claramente por encima. La causa del piso no se averiguó (entrada 100); "
     "la lectura que sí vale es la regla: todo conteo de off-target se publica con su nulo al lado."),
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
    # El titulo se escapa, pero varias tarjetas lo escriben con <code> o <i> (un gen, un nombre
    # cientifico). Sin esto esas etiquetas se ven literales en la pagina.
    t = html.escape(titulo)
    for etq in ("code", "i"):
        t = t.replace("&lt;%s&gt;" % etq, "<%s>" % etq).replace("&lt;/%s&gt;" % etq, "</%s>" % etq)
    return ('<div class="card"><p class="t">%s</p><p class="d">%s</p>'
            '<p class="f">%s</p>%s</div>' % (t, desc, enlaces, aviso))


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

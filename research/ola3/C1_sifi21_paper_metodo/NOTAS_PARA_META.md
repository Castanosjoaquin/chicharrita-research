# Notas para la memoria del proyecto — C1 (ola 3)

Para que el orquestador integre a `00_meta/`. No se editó nada de `00_meta/` ni ningún
REPORT.md ajeno, y no se hizo ningún commit (D5).

## Decisiones candidatas para DECISIONS.md

**D-c1. El criterio de «eficiente» se reporta siempre con sus tres términos continuos, no sólo
con el booleano.** Fundamento: de los seis filtros que componen el veredicto, dos no tienen
ninguna fuente primaria (1 kcal/mol y 22 °C) y dos la tienen sólo para el principio, no para el
número (asimetría y accesibilidad). Consecuencia: el entregable de priorización publica por
ventana la brecha de ΔG, la probabilidad de apertura y los dos nucleótidos de la regla terminal,
y deja el booleano de si-Fi como columna de compatibilidad con lo que usa el laboratorio.

**D-c2. Corregir el índice de la regla terminal en el modo «corregido» del port, o declarar por
qué no.** El fuente comprueba la posición 2 del 21-mero (`sifi_pipeline.py:528` y `:543`) donde
Ui-Tei 2004 y la propia geometría de si-Fi ponen la posición 1 —la que su cálculo de ΔG usa como
extremo 5' del sentido, `sifi_pipeline.py:377`—. El port hereda el índice en los dos modos
(`tools/sifi21_port/sifi_core.py:192` y `:344`). Medido sobre `NC_002786.2`: cambia la rama en el
51,4 % de las ventanas y el booleano terminal en el 31,4 %. Falta medir cuántos veredictos finales
cambian, que requiere correr el port con ViennaRNA.

**D-c3. Al citar la licencia de si-Fi21, citar las tres declaraciones.** Artículo (página 9):
CC BY-SA 4.0. README del repositorio oficial: CC BY-NC-SA 2.0. Última página del manual:
CC BY-NC-SA. Las dos últimas tienen cláusula NonCommercial, incompatible con la primera. La
afirmación previa del repositorio («SourceForge dice CC BY-NC 2.0») no se pudo verificar y, además,
no coincide exactamente con lo que dice el README, que sí se verificó.

## Caminos probados y resultados para CAMINOS_PROBADOS.md

- **Cerrado el pendiente 4 del checkpoint 1** (qué umbral usa si-Fi21 y cómo combina energía
  libre, identidad y estructura secundaria). La respuesta está en la tabla de P1 de
  `research/ola3/C1_sifi21_paper_metodo/REPORT.md` y en `filtros.json`. Resumen: conjunción de tres
  booleanos más una regla de dos nucleótidos; «identidad» no es un filtro, es el presupuesto de
  desajustes de Bowtie (cero por defecto) más una observación experimental del propio artículo
  (la eficacia cae por debajo del 92 % de similitud global).
- **El manual del programa existía y no estaba leído.** `Quick_help.pdf`, 13 páginas, viaja dentro
  del repositorio oficial. Contesta los defaults de cada modo y por qué la eficiencia se apaga
  cuando se permiten desajustes. Copia de trabajo en `work/C1/siFi21--d6296b7/Quick_help.pdf` y
  texto extraído en `work/C1/quick_help.txt`.
- **si-Fi21 no busca regiones.** El único rastro es un parámetro `region_plot_lst` documentado como
  «Plot for suggested RNAi design region» que nunca se usa (`show_plot.py:27` y `:41`,
  `create_plots.py:13` y `:23`). La búsqueda de la región de 200 nt más densa es un agregado del
  port, y conviene presentarlo así ante el investigador.
- **Verificada por medición propia la versión de ViennaRNA que trae si-Fi:** las cadenas internas
  de `ToCopy/RNAplfold/RNAplfold.exe` declaran 2.1.5.
- **Descartado:** medir cuántos veredictos finales cambian al corregir el índice de la regla
  terminal. Requiere correr el port con ViennaRNA y pertenece al módulo de eficiencia, no a esta
  investigación. Se midió en cambio el efecto sobre la rama y sobre el booleano terminal, que acota
  el problema.

## Preguntas abiertas para PREGUNTAS_ABIERTAS.md

1. **De dónde sale el rango de 150 a 250 nt y «con largos no funciona».** No está en el artículo
   (las construcciones son de 500 pb y las ventanas de prueba de 100 pb), no está en el manual y no
   está en el código. La práctica publicada con si-Fi21 en insecto usa 400 y 500 pb. Pregunta para
   el investigador: especie, vía de entrega, largos comparados y medida.
2. **¿Modo diseño (HE) o modo off-target (HS)?** Los defaults son distintos —HS apaga estabilidad
   de extremos y accesibilidad— y el conteo de eficientes cambia por completo. Sin esto, los
   conteos declarados y los nuestros no son comparables.
3. **¿Corren con desajustes permitidos?** Si se permite ≥ 1, si-Fi **desactiva** el cálculo de
   eficiencia por completo (`main.py:114-118` → `sifi_pipeline.py:513-514`), y el manual explica que
   es porque no hay datos confiables. Es una explicación candidata para conteos que no reproducimos.
4. **Licencia del software:** cuál de las tres declaraciones rige.
5. **Vacío de validación:** no existe ninguna validación experimental del criterio de eficiencia de
   si-Fi21 en un insecto, ni ningún uso publicado en cicadélidos. La evidencia primaria de las
   reglas de secuencia viene de células de mamífero, y los propios autores de esa evidencia
   (Ui-Tei 2004) reportan que en *Drosophila* in vivo casi no hay preferencia de secuencia.
6. **Defecto editorial del artículo:** su entrada bibliográfica de Tafer 2008 está fusionada con la
   de RNAplex, con volúmenes y páginas mezclados. Si se cita, citar por DOI.

## Fuentes para FUENTES.md

Las 23 entradas de `research/ola3/C1_sifi21_paper_metodo/sources.json`, con el nivel de lectura
declarado: **15 en texto completo** (artículo de si-Fi, manual, fuente de GitHub, Elbashir 2001,
Ui-Tei 2004, Langmead 2009, Chen 2012 y Turner y Mathews 2010 —ocho—, más las lecturas dirigidas de
los siete trabajos citantes en XML de Europe PMC), **6 sólo en resumen** (Schwarz 2003,
Khvorova 2003, Reynolds 2004, Tafer 2008, Bernhart 2006 y Ameres 2007, porque sus editoriales están
fuera de la lista de dominios permitidos) y **2 que no son lecturas bibliográficas**: la consulta
programática a Europe PMC y el genoma público `NC_002786.2` usado localmente.

De las once fuentes primarias de los umbrales en particular, cinco se leyeron en texto completo y
seis sólo en resumen.

## Bloqueos y rechazos

- **Bloqueos de red, sin espejos ni proxies:** `sourceforge.net`, `zenodo.org`,
  `doi.ipk-gatersleben.de`, `cell.com`, `nature.com` y `academic.oup.com`. Consecuencias: no se
  pudo verificar la licencia declarada en SourceForge, ni abrir el código depositado en Zenodo
  (`10.5281/zenodo.845056`), ni el instalador de e!DAL (`10.5447/ipk/2017/9`), ni el conjunto de
  calibración de la validación (`10.5447/IPK/2018/2`); y seis fuentes primarias quedaron en nivel
  de resumen. No se pidió apertura de dominios: ninguno era fatal para las tres preguntas.
- **Rechazos de filtro de seguridad:** ninguno en esta investigación.
- **Nota operativa del entorno, por si otra sesión tropieza:** dentro de la carpeta concedida no se
  pueden crear directorios ocultos, así que `git clone` falla al crear `.git`. Se resolvió bajando
  el tarball del commit con `curl` desde `codeload.github.com` y descomprimiéndolo excluyendo
  `*/.idea/*`.
- **Contenido con apariencia de instrucción:** no se encontró ninguno. El README del repositorio
  oficial incluye un texto que pide buscar archivos temporales en el directorio del usuario para
  recuperar las secuencias de siRNA; es una nota de uso de los autores, no una instrucción dirigida
  a un agente, y no se ejecutó nada a partir de ella.

# F6 Parte 2 — La respuesta del investigador, y qué cambia

**Procedencia.** Correo de Diego, recibido el 22 de octubre de 2026, en respuesta al correo del
equipo (`entregables/correo-investigador.md`, siete bloques de preguntas). El texto lo pegó el
usuario en la sesión; la fecha y hora exactas del mensaje y el encabezado no se registraron. Va
dirigido a los cuatro integrantes y cierra con «nos vemos el lunes», o sea el **26 de octubre**,
la fecha del checkpoint 2.

**Qué es este documento.** La Fase 6 Parte 2 pide tres cosas: pegar la respuesta, completar la
tabla de qué cambia, y documentar en `CAMINOS_PROBADOS.md` cualquier contradicción **antes** de
editar un entregable. Las tres están acá. El plan de ejecución, que es más largo que esta tabla,
vive aparte en `docs/plan_ola4/PLAN_OLA4.md`.

---

## 1. El texto, tal como llegó

> Hola Joaquín, Lorenzo, Luca y Santino:
>
> Estuve revisando el informe con bastante detenimiento y también volví al código original y al
> paper de si-Fi21. Muy interesante el trabajo que hicieron, especialmente que hayan auditado los
> criterios del algoritmo, explorado su sensibilidad a los parámetros y propuesto regiones
> alternativas.
>
> Les comento algunas cosas sobre las preguntas.
>
> **1. Regla de nucleótidos terminales**
>
> Efectivamente, la rama que identificaron existe en el código original.
>
> La preferencia por determinados nucleótidos en el extremo 5′ de la hebra guía tiene fundamento
> biológico y puede influir en su selección y carga en AGO. Lo interesante de lo que encontraron
> es que, para determinadas combinaciones de nucleótidos, el algoritmo utiliza esa preferencia
> para prescindir de los filtros de estabilidad de extremos y selección de hebra, dejando
> únicamente el criterio de accesibilidad.
>
> Me parece razonable cuestionar esa excepción y evaluar una versión en la que la regla terminal
> sea un filtro adicional, en lugar de sustituir a la termodinámica del dúplex.
>
> Sin embargo, tampoco asumiría todavía que esa modificación mejora la predicción de eficiencia.
> Sería interesante conservar ambos modelos y pensar qué evidencia experimental permitiría
> compararlos.
>
> Incluso podría explorarse una tercera alternativa: en lugar de clasificar cada ventana mediante
> cortes binarios, conservar los valores termodinámicos, las preferencias terminales y la
> accesibilidad como variables independientes del proceso de clasificación, para evaluar
> posteriormente cómo contribuyen a la eficiencia.
>
> **2. Diferencias con nuestros conteos**
>
> Pude confirmar que los resultados que les compartimos corresponden a ejecuciones con la
> configuración identificada como:
>
> siFi21_8_1.0_0.1_1111
>
> Es decir, el umbral de estabilidad de extremos configurado fue 1,0, no 1,75.
>
> Los valores de nuestra planilla corresponden a los conteos de siRNAs predichos como eficientes
> en el análisis de diseño. No son conteos de eficientes después de eliminar todos los posibles
> off-targets; esa evaluación la realizamos por separado.
>
> Por lo tanto, la proximidad que encontraron utilizando 1,75 es interesante, pero no explica por
> sí sola las diferencias.
>
> Antes de modificar parámetros, convendría verificar que las implementaciones utilicen
> exactamente las mismas secuencias, orientación, referencias y criterios de contabilización.
> También sería útil comparar cuáles son las ventanas específicas que cambian de clasificación, en
> lugar de considerar únicamente el conteo final.
>
> Me interesa también lo que observaron sobre el contexto de secuencia al utilizar RNAplfold.
> Entiendo que compararon calcular la accesibilidad sobre el gen completo con recalcularla sobre
> una región previamente recortada. Es razonable que aparezcan diferencias, especialmente cerca de
> los extremos, pero sería bueno confirmar cuánto de ese efecto corresponde al plegamiento y
> cuánto podría deberse al tratamiento de las posiciones.
>
> Aprovecho para preguntarles de dónde obtuvieron la versión que denominan sifi21INTA. ¿Tienen el
> enlace al repositorio y la versión exacta? También me interesaría conocer el port que
> desarrollaron.
>
> **3. Homalodisca vitripennis**
>
> Coincido con la distinción que plantean.
>
> Si bien es un organismo que no está reportado como presente en Argentina y su exposición local
> no sería equivalente a la de otras especies, sigue siendo un cicadélido que puede aportar
> información relevante sobre la conservación de regiones entre organismos relacionados.
>
> Por eso mantendría esa información, pero separaría el riesgo de exposición ecológica de la señal
> de conservación de secuencia. No necesariamente deberían tener el mismo peso en la decisión
> final.
>
> **4. Off-targets y selección de regiones**
>
> Nuestro enfoque actual es conservador. Evaluamos la identidad de secuencia de los posibles
> off-targets independientemente de que esas ventanas sean clasificadas como siRNAs eficientes por
> el modelo.
>
> Esto responde a que una predicción negativa de eficiencia no garantiza que un siRNA carezca de
> actividad biológica.
>
> Una coincidencia perfecta de 21 nt es una señal importante para evaluar el riesgo, aunque no
> demuestra por sí sola que vaya a producir silenciamiento. También importa qué organismo presenta
> esa coincidencia, su posibilidad de exposición, qué gen está involucrado y la evidencia
> biológica disponible.
>
> Por lo tanto, no trataría todas las coincidencias de 21 nt como equivalentes ni las convertiría
> automáticamente en un veto ecológico universal. Sí las conservaría como alertas fuertes que
> deben ser consideradas y justificadas.
>
> **5. Regiones alternativas**
>
> Me parecen interesantes las cuatro propuestas, particularmente la de BicC 922–1221, donde
> informan un aumento importante en la cantidad de siRNAs eficientes predichos y una reducción de
> coincidencias perfectas con organismos del panel no objetivo.
>
> Es una alternativa que vale la pena seguir explorando. Antes de considerarla superior a la
> original, sería importante comprobar la robustez de esa ventaja frente a los parámetros del
> modelo, la referencia utilizada y los criterios de riesgo.
>
> También me resultó interesante la diferencia que encontraron entre la estabilidad del ranking de
> genes y la estabilidad de las coordenadas seleccionadas. Son dos niveles distintos de robustez y
> está bueno que los hayan separado.
>
> Finalmente, les dejo una pregunta más general para pensar: ¿hasta qué punto el número de siRNAs
> eficientes predichos permite comparar estrategias dirigidas a genes diferentes? ¿Qué otras
> variables biológicas incorporarían para evaluar la probabilidad de que cada diseño produzca el
> efecto buscado?
>
> Me parece muy valioso que hayan ido más allá de ejecutar el programa y se hayan puesto a
> investigar sus supuestos. Es justamente el tipo de análisis crítico que esperamos de este
> desafío.
>
> ¡Saludos y nos vemos el lunes!
>
> Diego

---

## 2. Qué contestó de las siete preguntas del correo

La Fase 6 dejó esta tabla armada por anticipado. Completada, queda así. Lo importante es la
columna del medio: de siete preguntas, contestó **una**.

| Pregunta del correo | ¿Contestó? | Qué dijo, y qué cambia |
| --- | --- | --- |
| 1. Modo de si-Fi21 y umbral de extremos; y si la columna es «eficientes» o «sin off-targets» | **Sí, las dos mitades** | Configuración `siFi21_8_1.0_0.1_1111`: umbral 1,0, no 1,75. Los conteos son «eficientes» del análisis de diseño; los off-targets los evalúan por separado. Cambia: se retira el 1,75 como explicación (ADR D45) y se descarta la hipótesis de la segunda columna (ADR D46). Reabre la pregunta de **por qué** difieren los conteos, que es la línea M1 |
| 2. ¿Región 1–200 por off-targets o por densidad? | No | Sigue abierta. Es pedido 5 del lunes |
| 3. Transcriptoma de *D. maidis* | No | Sigue abierta, y es lo que bloquea la conservación de `eth` y `burs-alpha` y la referencia que M7 necesita. Pedido 2 del lunes |
| 4. Pesos del ranking y peso de un hemíptero no objetivo | Parcial, reformulada | No dio números, pero cambió la pregunta: en §3 pide **separar** exposición de conservación, así que lo que hay que pedirle son dos pesos y no uno (ADR D47, línea M5). Pedido 4 del lunes |
| 5. ¿Matar o esterilizar? | No | Sigue abierta y sigue siendo decisión suya. Pedido 3 del lunes |
| 6. Origen del rango 150–250 nt | No | Sigue abierta. Nuestra lectura —convención compatible con la evidencia, no conclusión de ella (ADR D29)— queda como estaba |
| 7. BLAST por defecto y «HCP» | No | Sigue abierta. La medición de C3 y el ADR D27 no cambian |

## 3. Lo que nos preguntó él

| Pregunta | Respuesta | Dónde está |
| --- | --- | --- |
| ¿De dónde sacaron `sifi21INTA`? Enlace y versión exacta | `github.com/bioinformaticaInta/sifi21INTA`, commit `92df44494373551d86eb1aee1b72d82858c581b2`, cabeza de `main` al 2024-03-27, verificado con `git ls-remote`. Comparado contra `github.com/snowformatics/siFi21-`, commit `d6296b73c08a2176e9d0257e0a175278cff8c231`, cabeza de `master` al 2025-03-18 | `research/ola3/C2_codigo_apolo_inta/diff_sifi21INTA_vs_original.md` |
| Conocer el port | `tools/sifi21_port/`, con `CAMBIOS.md` y la verificación contra el original en los cuatro genes | Antes de compartirlo corre la auditoría de secuencia de la línea M9: el repositorio tuvo un incidente de 21-meros commiteados y no se manda nada sin verificar |

## 4. Las tres contradicciones, y de qué lado quedó cada una

`CLAUDE.md` y la Fase 6 piden que una respuesta que contradiga algo entregado se documente antes
de editar. Son tres y están las tres en `00_meta/CAMINOS_PROBADOS.md` con la entrada del
2026-10-22.

**La primera la perdimos nosotros, y limpio.** Afirmábamos, en el correo y en
`entregables/critica-herramientas.md`, que subir el umbral de estabilidad de extremos a 1,75 era
lo que más acercaba a su planilla, y que «dos barridos independientes apuntan al mismo
parámetro». Él declaró el umbral en 1,0. La medición sigue en pie —esa celda de la grilla da
117, 35, 199 y 32, con dos valores exactos `[M]`— pero la lectura causal no: con un barrido de
22.176 configuraciones, que una celda se acerque a cuatro números no es evidencia de nada. Es el
error de confundir el mejor punto de un barrido grande con un hallazgo.

**La segunda es una posición nuestra que él confirma.** El ADR D17 decidió, contra la regla
mecanicista, que una ventana con coincidencia en un no objetivo cuenta como riesgo aunque el
modelo no la prediga eficiente. Él corre el mismo criterio y por el mismo motivo: «una predicción
negativa de eficiencia no garantiza que un siRNA carezca de actividad biológica». D17 queda
confirmado por una fuente independiente.

**La tercera es una corrección de consecuencia, no de criterio.** Sobre ese mismo criterio
conservador nosotros construimos un **veto**: una coincidencia perfecta de 21 nt con un organismo
del panel descarta la región. Él no hace eso: «no trataría todas las coincidencias de 21 nt como
equivalentes ni las convertiría automáticamente en un veto ecológico universal. Sí las
conservaría como alertas fuertes que deben ser consideradas y justificadas». Y la consecuencia
tiene nombre y número: el veto de `ATPaseD_Dm` por tres coincidencias con *Homalodisca
vitripennis* en 392–394 es lo que había resuelto el empate del tercer puesto, que sin él se
invierte en el 47,4 % y el 48,9 % de la grilla `[M]`. **Aplicar su corrección nos devuelve el
empate.** Eso es la línea M5 y la M6, y no se toca el entregable sin que el usuario lo confirme.

## 5. Lo que su carta abre, y que no estaba en ninguna de nuestras listas

**Que los conteos no comparan la misma unidad.** Siguiendo su pista de «referencias y criterios
de contabilización» hasta el fuente apareció que la columna «Efficient siRNA hits» del original
no cuenta ventanas: cuenta registros de acierto de Bowtie, agrupados por nombre de referencia
(`general_helpers.py:107-123`), y la eficiencia sólo se calcula para aciertos en la hebra `+`
(`sifi_pipeline.py:195-221`) `[R]`. Una ventana eficiente que no pega en la referencia no cuenta;
una que pega dos veces cuenta dos veces, y que eso ocurre está medido —2.504 aciertos para 2.500
ventanas en `BicC_Dm` `[M]`—. Es la primera explicación disponible que puede mover los conteos en
los dos sentidos, que es la forma que tiene el desajuste: contra las mismas secuencias, su
planilla baja en tres genes y sube en uno `[H]`. Es la línea M1 y es lo que más rinde de todo el
plan.

**Cuánto del efecto del recorte es plegamiento y cuánto es tratamiento de posiciones.** Lo
pregunta en §2 y está contestado a medias. Lo medido en C13 §4 ya separa una parte aritmética
—dentro del gen la región tiene 200 posiciones de inicio y recortada tiene 180— de 27 cambios de
veredicto por borde, y de esos hay dos identificados a 64 y 66 nt cuyos 21 nucleótidos son
idénticos en los dos cálculos y a los que sólo les cambió la accesibilidad `[M]`. Lo que falta es
hacer esa partición para los 27 y no para dos: cuántos cambian con el 21-mero idéntico (eso es
plegamiento) y cuántos cambian porque la ventana no es la misma (eso es posiciones). Es un
análisis sobre un TSV que ya existe, y es la tarea 2 de la línea M2.

**Qué evidencia experimental distinguiría los dos modelos.** Lo pregunta como invitación y
nosotros ya tenemos la mitad de la respuesta, en negativo: la validación retrospectiva
preregistrada contra *Tribolium castaneum* da ρ = +0,142 [−0,247, +0,492] para el modo fiel y
+0,024 [−0,356, +0,397] para el corregido, con n = 29 `[M]`. Con los datos abiertos que existen
los dos modelos no se distinguen. Lo que falta es el número: cuántas etiquetas harían falta, y
cuál es el ensayo prospectivo mínimo que discrimina. Línea M4, y tiene una ventaja de diseño: los
dos modelos difieren en un conjunto identificable de 19, 7, 50 y 8 ventanas, y ninguna va en
sentido contrario `[M]`, así que el ensayo mide discordantes contra concordantes y no siRNA al
azar.

## 6. Qué se actualiza, y en qué orden

| Qué | Dónde | Estado |
| --- | --- | --- |
| ADR D45: el 1,75 se retira como explicación | `00_meta/DECISIONS.md` | hecho |
| ADR D46: la columna de la planilla es «eficientes» del diseño | idem | hecho |
| ADR D47: exposición y conservación son dos ejes | idem | hecho, **implementación pendiente** (M5) |
| ADR D48: el veto pasa a alerta justificada | idem | hecho, **implementación pendiente** (M6) |
| ADR D49: se conservan los dos modos y se agrega la vía continua | idem | hecho (M3) |
| Las tres contradicciones | `00_meta/CAMINOS_PROBADOS.md` | hecho |
| Tres cerradas, seis abiertas, cinco nuevas | `00_meta/PREGUNTAS_ABIERTAS.md` | hecho |
| Borrador de respuesta y pedidos del lunes | `entregables/respuesta-al-mentor.md` | hecho, **aprobado para envio antes del lunes** (D50), pendiente de revision del equipo |
| La sección de la planilla de `critica-herramientas.md` | `entregables/` | **pendiente**, y espera M1: hoy afirma el 1,75 como la mejor explicación y eso ya no se sostiene |
| El ranking y la casilla de riesgo | `entregables/`, `tablero/` | **pendiente**, y espera M5 y M6, que el usuario tiene que confirmar |
| El plan de ejecución, nueve líneas | `docs/plan_ola4/PLAN_OLA4.md` | hecho |

**Lo que no se tocó a propósito.** Ningún entregable. Dos de los cinco ADR cambian el ranking que
ya está entregado, y la Fase 6 dice que eso se aplica sólo con la confirmación del usuario. El
único entregable que hay que corregir sí o sí es la sección de la planilla de
`critica-herramientas.md`, porque hoy afirma como explicación algo que el autor del dato
desmintió; pero conviene corregirla **con** el resultado de M1 y no sólo quitando la afirmación,
que sería cambiar una explicación equivocada por un agujero.

## 7. Qué quedó sin hacer y por qué

- La Parte 1 de la Fase 6 —el ensayo de las diez preguntas anticipadas y la agenda de cinco
  minutos— sigue sin hacerse. No depende de la respuesta y es para el fin de semana.
- No se verificó el texto del correo realmente enviado contra el borrador de siete preguntas. La
  respuesta de Diego numera sus cinco puntos con su propia numeración, no con la nuestra, así que
  el mapeo de la sección 2 se hizo por contenido y no por número. Si el correo enviado tenía otra
  numeración, el mapeo no cambia.
- No se regeneró `estado.html`: nada de HECHO o FALTA cambió todavía, porque no se tocó ningún
  entregable.

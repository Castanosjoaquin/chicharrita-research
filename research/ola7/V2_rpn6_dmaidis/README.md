# V2 — `Rpn6` recuperado en *D. maidis*, y medido con las mismas pruebas que `BicC_Dm`

> ## ⚠ CORREGIDO — leer [`REPORT_CORRECCION_IDENTIDAD.md`](REPORT_CORRECCION_IDENTIDAD.md) primero
>
> El gen que este informe trata como candidato, `GITV01002940.1` (subunidad 11), **no es el del
> fenotipo publicado**. Elegí por nombre y no por secuencia: el paper lo llama `Rpn6` y en
> *Drosophila* ese nombre es la subunidad 11, pero `C5` ya había medido que la secuencia del gen
> silenciado es **PSMD6**. Verificado con `tblastx`: los transcritos del paper en *S. titanus* y
> *E. variegatus* alinean al **96,7 %** y **96,5 %** con `GITV01002972.1` —el que acá figura como
> control de parálogo— y **no** con `GITV01002940.1`. Con el gen correcto, `BicC_Dm` 922-1221
> **gana en eficacia** (79,3 % y 96,1 % de las configuraciones) y la ventaja de limpieza no se
> sostiene (percentil 9,8 del nulo). Todo lo que estos informes dicen de `GITV01002940.1` sigue
> siendo una medición válida **de la subunidad 11**, que no es el candidato.



> **Choque de identificador.** Esta carpeta y `research/ola7/V2_quimeras_y_homologia/` usan las
> dos el prefijo `V2`, por sesiones distintas que trabajaron en paralelo sobre el mismo árbol.
> Son **líneas distintas**; ninguna referencia cruzada entre ellas. Quien integre la ola 7
> debería renumerar una de las dos.

**Fecha: 2026-10-29. Sin issue asignado** (el ID se eligió en la sesión). Todo corrió en local;
ninguna secuencia salió de la máquina.

## Qué preguntaba esta línea

`F3` dejó a `Rpn6` **primero de su cohorte** (0,8403 y 0,8383, por encima del 0,8128 de `BicC`)
pero en la cohorte `A+3`, con el eje de off-target calculado sobre **secuencia de otra especie**.
La pregunta era si, recuperando el gen en *D. maidis*, el candidato aguanta las mismas pruebas que
`BicC_Dm` 922-1221.

## Los dos informes

| Archivo | Qué contesta |
| --- | --- |
| [`PREREGISTRO.md`](PREREGISTRO.md) (`486aeb1`) | criterio de recuperación y de región, **antes** del primer cálculo |
| [`REPORT.md`](REPORT.md) | la recuperación, la ortología recíproca, los dos ejes y la conservación |
| [`PREREGISTRO_ROBUSTEZ.md`](PREREGISTRO_ROBUSTEZ.md) (`1f63ad8`) | criterio del barrido y del nulo, **antes** de calcularlos |
| [`REPORT_ROBUSTEZ.md`](REPORT_ROBUSTEZ.md) | el barrido de 2.184 configuraciones y el nulo de 50 permutaciones |

## Lo que se encontró, en cinco puntos

1. **El gen existe en *D. maidis* y su ortología cierra.** `GITV01002940.1`, CDS de 1.245 nt y
   415 aa, **97,11 % de identidad sobre 415 de 415 aa** contra `XP_054288549.1` (subunidad 11 del
   proteasoma 26S). La **vuelta recíproca** cae en `XM_054432574.1` —el mRNA de la consulta— con
   **un solo acierto y sin competidor**. El control de parálogo `GITV01002972.1` **no cierra**
   (cuatro aciertos empatados), que es para lo que estaba. `[M]`
2. **La región 325-624 iguala a `BicC_Dm` 922-1221, no la supera.** Misma eficacia (26 de 280 las
   dos, 0,0929), limpieza 0,9910 contra 0,9884, cero coincidencias perfectas de 21 nt y cero
   bloques de ≥ 19 nt contra el panel de seis. `[M]`
3. **El nulo desarma la ventaja de limpieza.** La diferencia de 0,0026 cae en el **percentil 51,6**
   del nulo de 50 permutaciones: **no se distingue del azar**. Como `BicC` también cae en ese
   rango, lo correcto es decir que las dos regiones son **indistinguibles en limpieza**. `[M]`
4. **La región es estable y la eficacia depende del marco.** Está entre las de máximo conteo en el
   **67,7 %** de 2.184 configuraciones; en marco recorte gana o empata a `BicC` en el **70,5 %** y
   en marco contexto sólo en el **40,1 %** — y **en el punto por defecto pierde**. `[M]`
5. **Lo que no se movió:** el eje de fenotipo (peso 0,40 en `F3`) sigue medido en *S. titanus* y
   *E. variegatus*, no en *D. maidis*. Se cierra con un bioensayo, no con cómputo. `[R]`

## La lectura para presentar

`Rpn6` 325-624 es un candidato **equivalente** a `BicC_Dm` 922-1221 en los dos ejes que sabemos
medir, **no superior**. Lo que lo distingue es el **mecanismo** —reproducción *y* letalidad, contra
reproducción sola— y de dónde viene la evidencia: uno lo entregó el laboratorio, el otro lo
encontramos nosotros por homología. Lo que le falta es el mismo bioensayo que a todos. `[H]`

## Una corrección propia que quedó registrada

La primera versión de `REPORT.md` decía que la región **ganaba** en limpieza, con 1,0000 contra
0,9884. Estaba mal: esa cifra era una definición mía —ventanas sin bloque de ≥ 19 nt— y no la de
`ranking.ejes()`, que pondera por referencia y criterio e incluye `mm1_21`. Recalculado con la
función oficial da **0,9910**. La corrección está en `REPORT.md` §0, con la frase vieja tachada
(`bb9e666`), y el nulo la terminó de acotar.

## Reproducibilidad

El CDS **no se versiona** (`sin_secuencias.py` rechaza toda racha de 21 nt) y se regenera desde
`work/W5/ref/TSA_GITV01.fasta`; `REPORT.md` §5 dice cómo. Los scripts importan el motor de `M7`
(`grilla_parametros.py`) y `tools/sifi21_port/ranking.py` **sin tocarlos**. Salidas intermedias en
`work/V2/`, no versionado.

**RNAplfold 2.1.5 no corrió** (el único binario del repo es el `.exe` de Windows): el eje del motor
queda declarado como no corrido y **no** como cero.

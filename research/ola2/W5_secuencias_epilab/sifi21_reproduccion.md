# ¿Salen de si-Fi21 los conteos de siRNA eficientes de la planilla?

Fecha: 2026-10-19. Herramienta: `tools/sifi21_port/` (port propio de si-Fi21 a
Python 3, sin interfaz; ver su `CAMBIOS.md`).

**Respuesta corta: no.** Ninguna de las 15.120 configuraciones de si-Fi21 barridas
reproduce a la vez los conteos declarados para los dos genes verificables. El
número de EPILAB, tal como está en la planilla, no es reproducible con si-Fi21 en
su espacio de parámetros documentado.

---

## Qué se pudo verificar y qué no

La planilla declara cuatro conteos de «número de siRNA eficientes» sobre el gen
entero: 114 para `MP_MRFV_full`, 35 para `CP_MRFV_full`, 199 para `BicC_Dm_full` y
33 para `ATPaseD_Dm_full`.

Las copias de trabajo de las secuencias no están en esta máquina —`work/` está
fuera del control de versiones y el corpus se manejó en otro equipo—, así que hubo
que reconstruirlas. Dos se pudieron, dos no:

| Gen | Reconstruible | Cómo |
|---|---|---|
| `MP_MRFV_full` | **sí** | `NC_002786.2`, posiciones 332-1594. Identidad 100 % según W5. |
| `CP_MRFV_full` | **sí** | `NC_002786.2`, posiciones 5674-6201. Identidad 100 % según W5. |
| `BicC_Dm_full` | no | transcrito de 17 bloques exónicos con 97,6-100 % de identidad contra el ensamblado. Reconstruirlo daría una secuencia distinta. |
| `ATPaseD_Dm_full` | no | 3 bloques con 99,3-100 % de identidad. Idem. |

**Verificación de la reconstrucción** `[E]`: las dos secuencias recuperadas
coinciden con lo que W5 registró del archivo original en largo exacto (1.263 y 528
nt) **y** en contenido GC exacto (63,1 % y 65,9 % contra los 63,1 y 65,91
registrados). Son los dos genes virales, que son públicos; no hubo que tocar dato
confidencial y nada salió de la máquina.

Los dos genes de *Dalbulus maidis* quedan pendientes de que alguien con el corpus
corra el mismo comando.

## El barrido

Se barrieron, para los dos genes a la vez: temperatura (22, 25, 37 °C), motor de
plegado (RNAplfold 2.1.5 del instalador de si-Fi contra ViennaRNA 2.7.2), modo
(fiel y corregido), ventana de accesibilidad u (1 a 21), umbral de estabilidad de
extremos (0 a 2 kcal/mol) y umbral de accesibilidad (0,01 a 0,3), con y sin regla
terminal. Son 15.120 configuraciones por gen.

El criterio es **simultáneo**: una configuración solo cuenta si reproduce los dos
conteos. Un acierto en un gen aislado no prueba nada, y de hecho aparece: el modo
corregido con el RNAplfold de si-Fi da exactamente 114 en `MP_MRFV_full`, pero esa
misma configuración da 25 en `CP_MRFV_full` contra 35 declarados. Era casualidad.

**Resultado: ninguna configuración reproduce los dos.** El mejor error acumulado
es 1, y lo alcanzan configuraciones mutuamente incompatibles — una con u=7, 22 °C y
umbral 2,0; otra con u=9, 37 °C y umbral 0,5. Esa dispersión es la firma de la
coincidencia numérica, no de una configuración real: si los 114 y los 35 salieran
de una corrida de si-Fi, habría una configuración única que acertara las dos y
estaría cerca de los valores por defecto.

Resultados con los valores por defecto del programa:

| Gen | Declarado | Fiel + 2.1.5 | Fiel + 2.7.2 | Corregido + 2.1.5 | Corregido + 2.7.2 |
|---|---|---|---|---|---|
| `MP_MRFV_full` (1.243 ventanas) | 114 | 133 | 142 | 114 | 123 |
| `CP_MRFV_full` (508 ventanas) | 35 | 32 | 39 | 25 | 30 |

Los órdenes de magnitud sí son los correctos: entre 5,9 % y 11,4 % de ventanas
eficientes, contra 9,2 % y 6,9 % declarados. El criterio es el de si-Fi; el número
exacto no.

## Qué queda como explicación

`[H]` Las tres hipótesis que sobreviven, en orden de verosimilitud:

1. **El laboratorio corrió una versión modificada.** Es lo que el investigador dijo
   en el checkpoint: que tuvo que cambiar parámetros químicos desactualizados. Si
   los cambió, el número no tiene por qué reproducirse con si-Fi tal como se
   distribuye. Esta es la hipótesis que mejor explica el fracaso del barrido.
2. **El conteo cuenta registros de Bowtie, no siRNA únicos.** En el original el
   bloque de eficiencia está dentro de un `if strand == '+'`, y
   `general_helpers.py:113` cuenta un registro por cada hit. Un siRNA con varios
   hits en el blanco principal se cuenta varias veces. Eso dependería de la base de
   datos usada, que no tenemos, y podría inflar el conteo de forma no reproducible
   sin ella.
3. **El número no viene de si-Fi.** Puede venir de la plataforma propia que están
   construyendo encima, que el investigador mencionó.

Lo que **queda descartado** `[E]`: que los 114 y los 35 salgan de si-Fi21 sin
modificar, con cualquier combinación de sus parámetros documentados, con
cualquiera de las dos versiones de ViennaRNA y a cualquiera de las tres
temperaturas probadas. Eso refuerza, con una herramienta distinta, lo que
`CAMINOS_PROBADOS.md` ya registraba como camino fallido: antes falló nuestra
reimplementación de los criterios publicados, ahora falla un port fiel del
programa mismo.

## Dos hallazgos que no buscábamos

### La regla terminal del original infla el conteo

`[E]` Medido: en modo fiel, de los 133 siRNA que si-Fi declararía eficientes en
`MP_MRFV_full`, **solo 122 pasan los filtros termodinámicos**. Once entran por la
rama de `sifi_pipeline.py:535-541`, que cuando el nucleótido 19 es A/T y el 2 no lo
es devuelve «eficiente» mirando solo la accesibilidad y salteando la selección de
hebra y la estabilidad de extremos. En `CP_MRFV_full` son 3 de 32.

O sea que entre el 8 y el 9 % de los «eficientes» que reporta si-Fi son eficientes
**solo porque la regla terminal se saltea la física**. No es un caso de borde, y es
el motivo por el que el modo corregido existe.

### La región que eligió EPILAB no es la más densa

`[E]` El investigador planteó esto él mismo en el checkpoint —«probate dos, tres
más a ver si, en teoría, debería haber elegido los que más tienen eficientes, pero
tal vez no»— y dijo que no recordaba el criterio. Medido:

| Gen | Región elegida | Eficientes en 1-200 | Región de 200 nt más densa | Eficientes |
|---|---|---|---|---|
| `MP_MRFV_full` | 1-200 | 30 | 490-689 (fiel) / 72-271 (corregido) | 39 / 38 |
| `CP_MRFV_full` | 1-200 | 8-9 | 195-394 (fiel) / 99-298 (corregido) | 21 / 21 |

En `MP_MRFV_full` la región elegida está entre un 23 y un 30 % por debajo del
óptimo por densidad. En `CP_MRFV_full` está **a menos de la mitad**: 8 o 9
eficientes contra 21.

Esto es consistente con la propia duda del investigador, y con su sospecha de que
quizá eligió por off-targets y no por densidad. W5 ya tiene el dato de off-targets
de las regiones elegidas, así que la pregunta se puede cerrar cruzando las dos
cosas: si la región 1-200 de `CP_MRFV_full` es limpia de off-targets y la 195-394
no lo es, la elección se explica. Es el próximo paso, no está hecho.

## Cómo reproducirlo

```bash
# reconstruir las dos secuencias verificables (descarga pública del NCBI)
#   NC_002786.2 -> 332-1594 (MP) y 5674-6201 (CP)

python tools/sifi21_port/barrido.py \
    work/sifi_check/MP_MRFV_full.fasta=114 \
    work/sifi_check/CP_MRFV_full.fasta=35

python tools/sifi21_port/run_sifi.py \
    work/sifi_check/MP_MRFV_full.fasta work/sifi_check/CP_MRFV_full.fasta \
    --modo fiel --backend exe --salida work/sifi_check/salida
```

Las secuencias y los TSV por ventana quedan en `work/sifi_check/`, fuera del
control de versiones. El generador está en el repositorio; el dato derivado del
corpus, no.

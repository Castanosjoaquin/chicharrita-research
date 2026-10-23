# Notas para el meta — M3

## Ya aplicado

- **D54** en `00_meta/DECISIONS.md`: las categorías en vez de los nucleótidos, `seq` detrás
  de `--con-seq`, y la tabla por ventana sin versionar.
- `research/ola4/M1_conteo_y_referencia/scripts/correr_matriz.py` pasa `--con-seq`. Era
  necesario y **silencioso**: sin eso, `conteo_por_acierto.py` lee la columna con
  `fila.get("seq") or ""` y se habría quedado sin consultas sin fallar.

## Para `PREGUNTAS_ABIERTAS.md`

- **Si la preferencia terminal aporta algo por fuera del atajo.** Las ramas 1 y 3 deciden
  las dos por termodinámica, así que para un modelo son la misma condición; lo único que
  las separa es la composición terminal. Si la preferencia tuviera valor predictivo propio,
  la tasa de eficientes debería diferir entre esas dos ramas a igual termodinámica. Y
  difiere, **en los cuatro genes y en la misma dirección**: la rama 1 rinde 15,2 %, 8,6 %,
  9,3 % y 7,9 %, y la rama 3 rinde 7,6 %, 4,1 %, 5,4 % y 5,0 % `[M]` (modo fiel, backend
  vienna). O sea que `nt19` A/T va con casi el doble de tasa que `nt19` G/C a igual regla
  de decisión. **No está testeado** y no se testea acá: es una comparación de proporciones
  que entra en el plan preregistrado de M4, porque elegir el test después de ver los datos
  es justamente lo que el preregistro existe para evitar. Tampoco está controlado por
  composición: una tasa mayor puede venir de que esas ventanas tengan otra termodinámica y
  no de la preferencia terminal `[H]`.
- **Qué pasa con las fracciones de la rama 2 bajo `--backend exe`.** Todo el §3 del REPORT
  está medido con ViennaRNA 2.7.2. M1 mostró que el motor mueve los conteos en direcciones
  distintas según el gen, así que las fracciones podrían moverse; la estructura (toda la
  diferencia entre modos en la rama 2) no puede moverse, porque es consecuencia del código.

## Para M4 (#8), que es quien usa esta tabla

Está en el §8 del REPORT y conviene no perderlo:

1. **La variable que más separa es categórica.** Un modelo que trate los cuatro términos
   como continuos y omita la rama le va a atribuir a la accesibilidad un efecto que en
   realidad es «la rama 2 sólo mira la accesibilidad». La rama entra como covariable o el
   modelo está mal especificado.
2. **El conjunto discordante entre modos coincide exactamente con la rama 2.** Eso hace el
   ensayo discriminante de M4 más barato de lo que el issue suponía: no hay que medir
   siRNA al azar, alcanza con muestrear dentro de la rama 2, que es donde los dos modelos
   difieren y en ningún otro lado.

## Para el entregable, si hace falta

La cifra presentable de esta línea es que **entre el 54 % y el 64 % de los «eficientes»
del original salen de la rama que saltea la termodinámica**. Es la versión medida de lo
que la auditoría venía diciendo en palabras, y Diego ya confirmó que la rama existe.
Conviene decirla junto a la salvedad de que el motor de accesibilidad mueve los totales.

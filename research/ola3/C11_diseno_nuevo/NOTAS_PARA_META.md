# Notas para meta — Fase 2 (diseño nuevo)

## Decisión candidata
Registrar que el cuello de botella del diseño por homología no es la ortología (11 de 14 familias la resuelven por secuencia) sino la conservación de nucleótido entre géneros: 2 de 11 superan 90 % en un tramo de 300 nt. Fecha 2026-10-22.

## Caminos probados
Cruzar por símbolo de gen (GN) deja fuera casi todo el catálogo; hay que cruzar por nombre de proteína. En la base revisada `Rpn6` de *Drosophila* es PSMD11 y PSMD6 se llama `Rpn7`: refuerza D30.
Un primer cálculo de RBH dio 0 pares por un error de formato de identificadores (`ref|XP_..|` contra `sp|..`); se corrigió y no cambia la conclusión.

## Preguntas nuevas
1. ¿El contig TSA de *D. maidis* es el ortólogo? Falta el `tblastn` inverso desde *D. maidis*.
2. ¿Se puede diseñar directamente sobre el contig de *D. maidis* aunque no pase el criterio contra *M. quadrilineatus*?
3. ¿Resuelve el genoma de *D. maidis* los parálogos de actina?

## Incidente de proceso
Un `git rebase --abort` corrido sin verificar `orig-head` movió la rama a un commit anterior y sacó 32 archivos del disco; se restauró con `git merge origin/main` (commit `03a80b7`). La causa fue no comparar `orig-head` con HEAD antes de abortar.

## Actualización del 2026-10-22 (C12)
La decisión candidata quedó formalizada como D37. La validación A (concordancia de anotación 76–86 %) y la B (marafivirus) están en `research/ola3/C12_validacion_homologia/`. Pendientes declarados: búsqueda inversa desde *D. maidis*, genoma en el paso de nucleótido, ventanas contra *Apis mellifera*, par con *N. lugens* en la validación A.

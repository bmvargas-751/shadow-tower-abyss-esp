# Pendientes

La cola del usuario: lo que ninguna regla cubre, las líneas delicadas con su solución provisional, los términos por decidir y los choques entre documentos. Nada de esto cambia el texto hasta que el usuario lo decide.

Formato: `- [ ] \`clave\` (rol, motivo): «fragmento» → «propuesta». Por qué.` `loc.py findings` agrega aquí, solo, los hallazgos sin regla de cada lote. Lo decidido pasa a DECISIONS.md y se borra de aquí.

## Para la prueba en el juego

Se deciden al ver la pantalla, con la versión 0.9.0.

- [ ] `mapa/` (técnico, límite provisional): la caja de los textos de mapa no se midió; el chequeo usa 300 de ancho y 3 renglones (TECH.md, T-3). Ver en el juego si entran o si sobra espacio, y ajustar `hooks.box`. [DECISIONS 2026-11-20]
- [ ] `sys/objetos` (T-3): nombres que pasan de 215 con el término completo del glosario (`loc.py check --all`, aviso `caja`; por ejemplo `#0803` «Espada de combate cercano», 263). Ver en el juego cuánto se lee bajo la barra de desplazamiento; si no alcanza, acortar el término del glosario para toda la serie.
- [ ] `exe#` (lote exe-001, T-3): rótulos del ejecutable que miden más del 125 % del original (aviso `caja`); caben en sus bytes, falta verlos en su barra o botón. Vistos el 2026-11-27: la configuración de botones (se encimaban; ahora el juego los estrecha, TECH «Ejecutable») y el sonido (entran). Faltan la tienda (`1fd830` «COMPRAR OBJETO», `1fe7d0` «COMPRAR»), la pausa y guardar y cargar.
- [ ] `exe#1fd010` イベント (revisor): «EVENTO», literal (E-1); el inglés de apoyo dice «Use». Ver qué hace el botón; quizá «ACCIÓN».
- [ ] `exe#1fd058` 攻撃・銃解除 (revisor): «ATAC./\nENFUNDAR», como el inglés de apoyo («Holster Gun»); 解除 es «soltar» o «cancelar». Ver qué hace el botón. El ajuste de los botones solo mide el primer renglón: «ENFUNDAR» (105) se sale un poco del recuadro (96).
- [ ] `exe#1fd3a0` y `exe#1fd3d0` 敵殲滅率 / 最高殲滅率 (prueba del 2026-11-27): en mayúsculas («ELIMINACIÓN», 163) se salía del recuadro; el japonés y el «Cleared» del inglés miden 108. Quedan en minúscula como el inglés: « Eliminación» (119) y « Máx. elim.» (119), con un espacio delante para que terminen a la misma altura. Ver si entran y si «Máx. elim.» se entiende; si no, «Récord» (80).
- [ ] `exe#1fc980` a `exe#1fc9b8` estados alterados de la pantalla de equipo (estaban en inglés en el original, T-6): provisional «Veneno», «Parálisis», «Ceguera», «Lento», «Maldito», «Sellado», con los términos del glosario. Mezclan sustantivos y adjetivos porque Gravity, Curse y Seal tienen campos de 7 bytes («Lentitud» y «Maldición» no entran). Ver en el juego si caben (aviso `caja` en «Maldito» y «Sellado») y cómo se leen.
- [ ] `exe#1fd660` GAME OVER: «ＦＩＮ ＤＥ ＬＡ ＰＡＲＴＩＤＡ» con espacios normales (con ideográficos no entra en 31 bytes). Ver si se lee bien.

- [ ] `OPENING.PSS`: subtítulos traducidos del inglés fan, con los tiempos ajustados por el usuario [DECISIONS 2026-11-28]. Confirmar en la prueba 9 que van con la voz. Si algún día aparece el texto japonés, revisarlos contra él.

## De los lotes

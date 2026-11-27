# Pendientes

La cola del usuario: lo que ninguna regla cubre, las líneas delicadas con su solución provisional, los términos por decidir y los choques entre documentos. Nada de esto cambia el texto hasta que el usuario lo decide.

Formato: `- [ ] \`clave\` (rol, motivo): «fragmento» → «propuesta». Por qué.` `loc.py findings` agrega aquí, solo, los hallazgos sin regla de cada lote. Lo decidido pasa a DECISIONS.md y se borra de aquí.

## Para la prueba en el juego

Se deciden al ver la pantalla, con la versión 0.9.0.

- [ ] `mapa/` (técnico, límite provisional): la caja de los textos de mapa no se midió; el chequeo usa 300 de ancho y 3 renglones (TECH.md, T-3). Ver en el juego si entran o si sobra espacio, y ajustar `hooks.box`. [DECISIONS 2026-11-20]
- [ ] `sys/objetos` (T-3): nombres que pasan de 215 con el término completo del glosario (`loc.py check --all`, aviso `caja`; por ejemplo `#0803` «Espada de combate cercano», 263). Ver en el juego cuánto se lee bajo la barra de desplazamiento; si no alcanza, acortar el término del glosario para toda la serie.
- [ ] `exe#` (lote exe-001, T-3): 41 rótulos del ejecutable miden más del 125 % del original (aviso `caja`); caben en sus bytes, falta verlos en su barra o botón. Los más anchos: `1fd000` «CAMBIAR ARMA», `1fcea0` «VOLUMEN EFECTOS», `1fd830` «COMPRAR OBJETO», `1fe7d0` «COMPRAR».
- [ ] `exe#1fd010` イベント (revisor): «EVENTO», literal (E-1); el inglés de apoyo dice «Use». Ver qué hace el botón; quizá «ACCIÓN».
- [ ] `exe#1fd058` 攻撃・銃解除 (revisor): «ATAC./\nENFUNDAR», como el inglés de apoyo («Holster Gun»); 解除 es «soltar» o «cancelar». Ver qué hace el botón.
- [ ] `exe#1fd3a0` y `exe#1fd3d0` 敵殲滅率 / 最高殲滅率 (revisor): « ELIMINACIÓN» y « MÁXIMA ELIM.», con un espacio delante en vez de los ideográficos del original. Ver si quedan alineados con el porcentaje.
- [ ] `exe#1fd660` GAME OVER: «ＦＩＮ ＤＥ ＬＡ ＰＡＲＴＩＤＡ» con espacios normales (con ideográficos no entra en 31 bytes). Ver si se lee bien.

## De los lotes

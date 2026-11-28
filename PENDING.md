# Pendientes

La cola del usuario: lo que ninguna regla cubre, las líneas delicadas con su solución provisional, los términos por decidir y los choques entre documentos. Nada de esto cambia el texto hasta que el usuario lo decide.

Formato: `- [ ] \`clave\` (rol, motivo): «fragmento» → «propuesta». Por qué.` `loc.py findings` agrega aquí, solo, los hallazgos sin regla de cada lote. Lo decidido pasa a DECISIONS.md y se borra de aquí.

## Para la prueba en el juego

Se deciden al ver la pantalla. Los que quedan los verá el usuario al avanzar en el juego con la 0.9.1 (2026-11-28).

- [ ] `mapa/` (técnico, límite provisional): la caja de los textos de mapa no se midió; el chequeo usa 300 de ancho y 3 renglones (TECH.md, T-3). Ver en el juego si entran o si sobra espacio, y ajustar `hooks.box`. [DECISIONS 2026-11-20]
- [ ] `exe#` (lote exe-001, T-3): rótulos del ejecutable que miden más del 125 % del original (aviso `caja`); caben en sus bytes, falta verlos en su barra o botón. Vistos y bien: la configuración de botones, el sonido, guardar y cargar, y la pausa (2026-11-28). Falta la tienda (`1fd830` «COMPRAR OBJETO», `1fd840` «VENDER OBJETO», `1fd850` «DEPOSITAR OBJ.», `1fd860` «RETIRAR OBJETO», `1fe7d0` «COMPRAR», `1fe7d8` «VENDER»): el usuario la verá al avanzar.
- [ ] `exe#1fc980` a `exe#1fc9b8` estados alterados de la pantalla de equipo (estaban en inglés en el original, T-6): provisional «Veneno», «Parálisis», «Ceguera», «Lento», «Maldito», «Sellado», con los términos del glosario. Mezclan sustantivos y adjetivos porque Gravity, Curse y Seal tienen campos de 7 bytes («Lentitud» y «Maldición» no entran). Ver en el juego si caben (aviso `caja` en «Maldito» y «Sellado») y cómo se leen.
- [ ] `exe#1fd660` GAME OVER: «ＦＩＮ ＤＥ ＬＡ ＰＡＲＴＩＤＡ» con espacios normales (con ideográficos no entra en 31 bytes). Ver si se lee bien.


## De los lotes

# Decisiones

Lo que el usuario decidió, con fecha, para no volver a discutirlo. Una regla de STYLE.md, TECH.md o GLOSSARY.md que sale de aquí lo cita: [DECISIONS fecha].

- **AAAA-MM-DD** Proyecto creado con el kit de traducción de juegos.
- **2026-11-20** Proyecto creado con el kit de traducción de juegos. Repo en GitHub, público: `bmvargas-751/shadow-tower-abyss-esp`. Reglas del repo iguales a `shadow-tower-esp` y Ys: `main` solo por pull request (con revisión del code owner e historial lineal), etiquetas `v*` protegidas, solo squash merge y borrado de la rama al fusionar.
- **2026-11-20** Original: la versión japonesa de PS2, imagen `Shadow Tower Abyss.iso` (1 561 624 576 bytes). Se traduce desde el japonés.
- **2026-11-20** Versión de apoyo: la traducción fan al inglés `STATest0.3.ppf` (PPF 3.0, en progreso). Solo se consulta, no es el original.
- **2026-11-20** Shadow Tower PS1 (`shadow-tower-esp`): solo referencia. No se copia ni su glosario ni su estilo ni sus decisiones hasta ver cómo está armado Abyss.
- **2026-11-20** Pruebas en PCSX2. El formato de entrega queda abierto hasta la fase 1.
- **2026-11-20** STYLE.md: se deja la base completa y solo se ajusta E-1 (el original es el japonés y el inglés fan es de consulta). El cambio es solo de este repo; el kit no se toca.
- **2026-11-20** Entrega: parche xdelta sobre la ISO japonesa. Hace falta porque `STAZ.STZ` tiene que crecer y moverse dentro de la ISO (TECH.md, T-4).
- **2026-11-20** Alcance: todo el texto del juego, en este orden: 1) tablas de texto, 2) subtítulos de los vídeos, 3) texturas con texto. La versión 0.9.0 sale con las tablas de texto traducidas.
- **2026-11-20** Pruebas: el usuario prueba en PCSX2 cuando las tablas estén traducidas al 100%, con el xdelta aplicado a su ISO. Antes, una ISO de prueba (pseudolocalización) para revisar las cajas y que se dibujen todas las letras.
- **2026-11-20** No se traducen (`excluded` de `loc.json`): los 46 textos vacíos del original, el copyright (`sys/menu#0128`), el resto de la demo (`sys/menu#0401`) y el mensaje de error para los programadores (`sys/menu#0099`).
- **2026-11-20** El límite de los textos de mapa (300 de ancho, 3 renglones) queda provisional: en la ISO de prueba no se llegó a ver ninguno. Se confirma en la prueba en el juego (TECH.md, T-3).
- **2026-11-20** Nombres inventados en katakana (criaturas, personajes): se toma la forma del inglés fan cuando es fiel a la pronunciación japonesa; si no, una transcripción propia legible en español. Caso por caso.
- **2026-11-20** Armas y armaduras con nombre en katakana de palabras inglesas o latinas: se traducen al español (espada, yelmo, alfanje); los nombres latinos o históricos quedan (lorica hamata). Las armas de fuego reales mantienen su modelo (Government M1911, Ingram).
- **2026-11-20** Glosario de Shadow Tower PS1 (`shadow-tower-esp/GLOSSARY.md`): se usa el mismo término cuando el concepto es el mismo en los dos juegos (HP, MP, estadísticas, magia, tipos de daño), por coherencia de la serie. Lo que cambia de sentido va a PENDING.md.
- **2026-11-20** Glosario (fase 3): se aprueban las 73 filas que salen de Shadow Tower PS1 y las propuestas del terminólogo para lo propio de Abyss (264 filas). En los puntos dudosos: sufijos de elemento como en ST1 (ブレイズ ígneo, リキッド cáustico, グリター radiante, シェイド oscuro); criaturas ガレ «Gare», パラ «Para», ガルディア «Gardia»; クィドル «Quiddle» como el inglés fan; スニーカー «tenis».
- **2026-11-20** Fichas de los mapas (`characters/`, 8 voces según `characters/hablantes.json`): se aprueban el trato (tú con el jugador, ustedes en plural), la voz quebrada en infinitivo y sin artículos, la voz deformada en MAYÚSCULAS, la voz solemne con vocabulario culto y sin vosotros, los silencios con tres puntos y フフフ → «Je, je, je». 我が主 y 主 → «amo» (no «señor», que es 長); 神様 → «Dios», 神 → «dios».
- **2026-11-20** Jugador: masculino, aunque el japonés no lo remarque. Lo que se le dice va en masculino («NECIO», «MALDITO»). Ficha: `characters/jugador.md`.
- **2026-11-20** Set de oro (`golden.jsonl`, 16 casos): aprobado. Pruebas: oro-001, 15 de 16, y oro-002, 14 de 16, aceptadas las dos; En oro-002, O-7 falló porque el traductor no gritó la palabra entera («LAN...ZA...AAA»), y O-13 porque el revisor y el corrector marcaron «NECIO» cuando todavía no estaba decidido el género del jugador; con la ficha del jugador, el caso queda bien planteado.
- **2026-11-22** El kit ya acepta el japonés como original: `source.jsonl` lleva el original en el campo `ja` (antes iba en `en`), y el inglés fan (`ref_en.jsonl`, campo `en`) pasa a ser la versión de apoyo (`support` de `loc.json`), así que llega a cada línea del lote. Sigue siendo solo de consulta (E-1). STYLE.md suma E-31 (honoríficos) de la plantilla del kit.
- **2026-11-22** Set de oro otra vez, por los prompts nuevos del kit y el inglés de apoyo en el lote: oro-003, 16 de 16.
- **2026-11-22** Set de oro otra vez, por los prompts nuevos del kit y el inglés de apoyo en el lote: oro-003, 16 de 16.

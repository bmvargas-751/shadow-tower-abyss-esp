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

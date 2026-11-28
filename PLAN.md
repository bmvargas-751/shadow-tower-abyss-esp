# Plan

## Decisiones

Se cierran en la fase 0, porque son caras de cambiar después.

- **Variante:** español neutro (*tú*/*ustedes*, sin regionalismos de ningún país).
- **Original:** versión japonesa de PS2 (única edición), imagen `Shadow Tower Abyss.iso`. [DECISIONS 2026-11-20]
- **Versión en inglés:** la traducción fan `STATest0.3.ppf` (en progreso), solo de consulta (E-1). Va en `support` de `loc.json`, con el campo `en`. [DECISIONS 2026-11-20] [DECISIONS 2026-11-22]
- **Nombres:** los inventados en katakana toman la forma del inglés fan si es fiel a la pronunciación japonesa; si no, una transcripción propia legible en español, caso por caso. [DECISIONS 2026-11-20]
- **Texto en inglés dentro del original:** se traduce (*ITEM* → *OBJETO*). [DECISIONS 2026-11-20] (TECH.md, T-6)
- **Terminología oficial:** no hay traducción oficial al español. Shadow Tower PS1 (`shadow-tower-esp`) es solo referencia hasta comparar cómo está armado Abyss. [DECISIONS 2026-11-20]
- **Pruebas:** PCSX2; la traducción se instala con un parche xdelta sobre la ISO japonesa. [DECISIONS 2026-11-20]
- **Alcance:** tablas de texto (0.9.0), después subtítulos de los vídeos y al final texturas con texto. [DECISIONS 2026-11-20]
- **Sin spoilers:** los documentos, los commits y el chat nombran zonas o archivos, nunca hechos de la historia.
- **Contenido del repo:** solo la traducción y las herramientas propias; nunca archivos del juego.

## Fases

### Fase 0. Antes de empezar

- [x] Cerrar las decisiones de arriba con el usuario.
- [x] Revisar con el usuario la base de STYLE.md: lo que no aplique se borra.

### Fase 1. Prueba técnica

Antes de esto no se decide nada más.

- [x] Extraer los archivos del juego, a una carpeta fuera del repo.
- [x] Adaptador: exportar el texto al formato común (`source` de `loc.json`) e importarlo de vuelta.
- [x] Ida y vuelta idéntica: exportar e importar sin cambios da los mismos archivos.
- [x] Caracteres: si la fuente tiene las letras españolas, o cómo se agregan (T-5). Agregadas con `tools/sta_font.py`; se ven bien en PCSX2.
- [x] Límites: bytes, ancho y renglones de cada tipo de texto (T-3, T-4), y sus chequeos en `hooks`. Medidos y en `hooks.check`; el de los mapas es provisional (PENDING.md).
- [x] Pseudolocalización: todo el texto más largo y con letras españolas, en el juego, para ver cortes y glifos que faltan. ISO de prueba (`tools/pseudo.py`) probada en PCSX2.
- [x] Completar TECH.md y `loc.json` (`codes`, `fixed_break`, `excluded`, `sections`).

### Fase 2. Inventario y presupuesto

- [x] Volumen por sección (`loc.py progress`).
- [x] Costo estimado por sección, antes de empezarla.

Estimación (2026-11-20), con la misma cuenta que `shadow-tower-esp`: ~43 000 tokens por agente cada 250 líneas de ~60 caracteres en español, más ~15 000 fijos por lote y agente (documentos); tres agentes por lote (traductor, revisor y corrector). Se cuentan los textos únicos, porque el kit copia los repetidos, y sin los excluidos. El largo en español se estima en 2,4 caracteres por cada carácter japonés (el inglés fan ocupa ~2 veces el japonés, y el español ~20% más que el inglés). Se suma un 15% a la parte variable, porque el japonés gasta más tokens por carácter.

| Sección | Líneas | Únicas | Caracteres (japonés) | Caracteres (español, estimado) | Lotes | Tokens estimados |
|---|---:|---:|---:|---:|---:|---:|
| Interfaz (menú y ayudas) | 131 | 117 | 2166 | ~5200 | 1 | ~96k |
| Lugares | 30 | 30 | 420 | ~1000 | 1 | ~55k |
| Criaturas | 136 | 135 | 2029 | ~4900 | 1 | ~93k |
| Objetos y equipo | 1210 | 920 | 13732 | ~33000 | 4 | ~506k |
| Historia (eventos y diálogos de los mapas) | 212 | 205 | 4371 | ~10500 | 1 | ~149k |
| **Total** | **1719** | **1407** | **22718** | **~54500** | **8** | **~900k** |

Más el editor, las líneas delicadas, el terminólogo y el perfilador (fase 3) y el set de oro (fase 4). Lugares es chica: conviene ir en el mismo lote que la interfaz (`loc.py prepare --prefix sys/menu# --prefix sys/lugares#`) para no pagar dos veces el costo fijo (~45k menos).

### Fase 3. Documentos

- [x] Glosario: el terminólogo propone las filas. 337 términos: 73 de Shadow Tower PS1 y 264 decididos (2026-11-20).
- [x] Fichas de personajes: el perfilador, antes de cada sección. 8 voces de los mapas (`characters/hablantes.json`). Solo hacen falta para los mapas: el menú, los lugares, las criaturas y los objetos no tienen personajes que hablen.
- [x] DECISIONS.md y PENDING.md al día.

### Fase 4. Set de oro

Obligatorio: sin él, `loc.py prepare` no arma lotes.

- [x] Elegir con el usuario los casos reales (al menos uno de cada tipo; mejor dos o tres). 16 casos.
- [x] Aprobarlo (`loc.py golden approve`).
- [x] Probar a los agentes (`loc.py golden prepare`, traductor, revisor y corrector, `loc.py golden score`) hasta que pase. oro-002, 14 de 16, aceptada (DECISIONS 2026-11-20).

### Fase 5. Piloto

- [x] Un primer lote de cada tipo de texto con el equipo completo. 4 lotes de 40 (2026-11-22).
- [x] Ajustar documentos y roles con lo que salga (y volver a pasar el set de oro si cambia un prompt). Ni los documentos ni los roles cambiaron. Las dudas quedan en PENDING.md y se deciden al final de la traducción [DECISIONS 2026-11-22].

### Fase 6. Traducción
- [x] Interfaz
- [x] Objetos y equipo
- [x] Criaturas
- [x] Lugares
- [x] Historia
- [x] Imágenes con texto (`tools/sta_tex.py`) y subtítulos de los videos de apertura y del prólogo (`tools/pss_sub.py`) [DECISIONS 2026-11-28]

### Fase 7. Prueba en el juego

- [ ] Jugar con la traducción completa y anotar cortes, cajas que se pasan, glifos que faltan y texto que quedó sin traducir.

### Fase 8. Entrega

- [ ] Instalador, registro de cambios y publicación.

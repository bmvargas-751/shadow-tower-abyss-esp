# shadow-tower-abyss-esp

Traducción al español neutro de *Shadow Tower Abyss* (PlayStation 2, versión japonesa, SLPS-25217), hecha desde el japonés con el kit de traducción de juegos. El repo tiene solo la traducción, los documentos y las herramientas propias: ningún archivo del juego.

- Método y decisiones: [PLAN.md](PLAN.md), [DECISIONS.md](DECISIONS.md)
- Estilo y términos: [STYLE.md](STYLE.md), [GLOSSARY.md](GLOSSARY.md), [characters/](characters)
- Técnica (formatos, fuente, cajas, pruebas en el juego): [TECH.md](TECH.md)
- Pendientes del usuario: [PENDING.md](PENDING.md)

## Herramientas

Hace falta la ISO japonesa (SHA-1 `3448ba2ebf69250eb01854f7d1e75d2e18ff987d`) con sus archivos extraídos en `../shadow-tower-abyss-esp-local/iso-jp/`. Lo que se genera va en `../shadow-tower-abyss-esp-local/build/`.

- `python3 tools/sta_text.py export` → el original para el kit (`source.jsonl`) y el inglés fan de consulta (`ref_en.jsonl`).
- `python3 tools/sta_text.py import` → `STAZ.STZ` con la traducción de `translation/`.
- `python3 tools/ps2iso.py ISO_ORIGINAL STAZ_NUEVO ISO_SALIDA` → la ISO con el contenedor nuevo.
- `python3 tools/pseudo.py ISO_ORIGINAL ISO_SALIDA` → ISO de prueba con todo el texto pseudolocalizado.

La entrega será un parche xdelta sobre la ISO japonesa.

## Avance

Actualizado: 2026-11-20.

### Fases

| Fase | Estado |
|---|---|
| 0. Decisiones | ✅ |
| 1. Prueba técnica | ✅ (límite de los textos de mapa provisional, PENDING.md) |
| 2. Inventario y costo | ✅ 1719 líneas (1407 únicas), ~900k tokens estimados |
| 3. Glosario y fichas | ✅ 341 términos, 3 personajes y 5 voces |
| 4. Set de oro | ✅ 16 casos; oro-002, 14 de 16 (aceptada) |
| 5. Piloto | ⬜ |
| 6. Traducción | ⬜ |
| 7. Prueba en el juego | ⬜ |
| 8. Entrega (parche xdelta) | ⬜ 0.9.0 con las tablas de texto |

### Secciones

<!-- loc:progress -->
**Etapa actual:** Fase 5. Piloto: Un primer lote de cada tipo de texto con el equipo completo.

| Sección | Líneas | Traducidas | Avance |
|---|---:|---:|---:|
| Interfaz y ayudas del menú | 131 | 0 | 0,0 % |
| Lugares | 30 | 0 | 0,0 % |
| Criaturas | 136 | 0 | 0,0 % |
| Objetos y equipo | 1.210 | 0 | 0,0 % |
| Mapas (eventos y diálogos) | 212 | 0 | 0,0 % |
| **Total** | **1.719** | **0** | **0,0 %** |
<!-- /loc:progress -->

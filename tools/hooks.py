"""Chequeos de Shadow Tower Abyss para el kit (loc.json, "hooks").

- encode: bytes que ocupa el texto en el juego (Shift-JIS con las letras
  españolas en códigos prestados, TECH.md T-4 y T-5).
- missing_chars: caracteres que la fuente no tiene (T-5).
- check: ancho de cada renglón y cantidad de renglones de cada caja (T-3).
"""
import functools
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sta_font  # noqa: E402
import sta_text  # noqa: E402


def encode(key, es):
    return sta_font.encode(es) if not sta_font.missing(es) else es.encode("utf-8")


def missing_chars(key, es):
    return sorted(set(sta_font.missing(es)))


# ---------------------------------------------------------------- cajas (T-3)

@functools.lru_cache(None)
def _advances():
    """Avances de la fuente, leídos de STAZ.STZ (fuera del repo) y guardados
    en build/ de la carpeta local para no volver a leerlos."""
    cache = os.path.join(sta_text.LOCAL, "build", "advances.json")
    if os.path.exists(cache):
        return json.load(open(cache, encoding="utf-8"))
    with open(sta_text.STZ, "rb") as f:
        f.seek(16 + 32 * sta_font.FONT_TABLE)
        _mg, size, _b, _c, _h1, _h2, sec, _x = struct.unpack("<4sIIIIIII", f.read(32))
        f.seek(sec * sta_text.SECTOR)
        adv = sta_font.advances(f.read(size))
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    json.dump(adv, open(cache, "w", encoding="utf-8"), ensure_ascii=False)
    return adv


# Ranuras del equipo (WEAPON, HEAD, RING...): al 80%, centradas en el panel de
# la derecha; lo que pasa del panel se sale de la pantalla.
SLOTS = {"sys/menu#%04d" % i for i in range(79, 91)}


# Rótulos del ejecutable (exe_text.py): cada barra o botón tiene su ancho, sin
# medir. Aviso si un renglón crece más que esto respecto del original, para
# verlo en el juego (TECH.md, T-3).
EXE_GROWTH = 1.25


def box(key, en):
    """(ancho máximo, renglones máximos o None, nota) de la caja del texto.
    Unidades de la fuente = píxeles del cuadro de 512 de ancho (TECH.md, T-3)."""
    if key.startswith("exe#"):
        widest = max(sta_font.width(ln, _advances()) for ln in en.split("\n"))
        return int(widest * EXE_GROWTH), en.count("\n") + 1, \
            "rótulo del ejecutable: el original mide %d; ver en el juego" % widest
    if key.startswith("mapa/"):
        return 300, 3, "provisional: falta ver un diálogo de mapa"
    if key.startswith(("sys/objetos#", "sys/criaturas#", "sys/lugares#")):
        if key.endswith("/nombre"):
            return 215, 1, "barra de la lista"
        lines = 4 if key.startswith("sys/objetos#") else 3
        return 320, lines, "descripción"
    if key in SLOTS:
        return 125, 1, "ranura del equipo, centrada en el panel"
    if "：" in en:
        return 680, 1, "línea de botones (al 70%)"
    return 480, None, "ancho de la pantalla"


def check(key, item, es):
    adv = _advances()
    width, lines, note = box(key, item["src"])
    out = []
    for n, ln in enumerate(es.split("\n"), 1):
        w = sta_font.width(ln, adv)
        if w > width:
            out.append(("caja", "T-3", "renglón %d: %d de ancho, el máximo es %d (%s)" % (n, w, width, note)))
    if lines and es.count("\n") + 1 > lines:
        out.append(("caja", "T-3", "%d renglones, el máximo es %d (%s)" % (es.count("\n") + 1, lines, note)))
    return out

"""Chequeos de Shadow Tower Abyss para el kit (loc.json, "hooks").

- encode: bytes que ocupa el texto en el juego (Shift-JIS con las letras
  españolas en códigos prestados, TECH.md T-4 y T-5).
- missing_chars: caracteres que la fuente no tiene (T-5).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sta_font  # noqa: E402


def encode(key, es):
    return sta_font.encode(es) if not sta_font.missing(es) else es.encode("utf-8")


def missing_chars(key, es):
    return sorted(set(sta_font.missing(es)))

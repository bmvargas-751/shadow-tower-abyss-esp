#!/usr/bin/env python3
"""ISO de prueba (pseudolocalización) de Shadow Tower Abyss.

Cada texto pasa a ser: [número] + el inglés del PPF (o un relleno si no hay)
con las vocales acentuadas y cada renglón ~30% más largo, más ¿¡ñÑü para
probar todos los glifos nuevos. Las tablas de los mapas tienen un límite: lo que no entra baja de nivel
(ver main).

    python3 tools/pseudo.py ISO_ORIGINAL ISO_SALIDA
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ps2iso  # noqa: E402
import sta_font  # noqa: E402
import sta_text as S  # noqa: E402

ACC = str.maketrans("aeiouAEIOUnN", "áéíóúÁÉÍÓÚñÑ")
PAD = " ñandú pingüino ÑÜ"


def tag(key):
    return "[%s]" % key.split("#", 1)[1].replace("/nombre", "n").replace("/desc", "d")


def pseudo(key, base, grow=1.3):
    base = "".join("?" if ch in sta_font.BORROWED else ch for ch in base)
    lines = base.split("\n")
    out = []
    for i, ln in enumerate(lines):
        s = ln.translate(ACC)
        target = int(len(ln) * grow + 0.999)
        k = 0
        while len(s) < target:
            s += PAD[k % len(PAD)]
            k += 1
        out.append(s)
    out[0] = ("¿¡" if grow > 1 else "") + tag(key) + out[0]
    return "\n".join(out)


def main(iso_in, iso_out):
    src = [json.loads(l) for l in open(S.SOURCE, encoding="utf-8")]
    ref = {}
    if os.path.exists(S.REF_EN):
        ref = {d["key"]: d["ref_en"] for d in map(json.loads, open(S.REF_EN, encoding="utf-8"))}
    texts = {}
    for d in src:
        k = d["key"]
        base = ref.get(k) or "Texto de prueba"
        texts[k] = pseudo(k, base)
    # las tablas de los mapas tienen límite: cada una baja de nivel por separado
    #   1: número + «á» + inglés del PPF; 2: inglés del PPF tal cual; 3: solo el número
    steps = ("con el inglés, el número y una á", "con el inglés tal cual", "solo con el número")
    level = {}
    while True:
        try:
            data, free = S.build_stz(texts)
            break
        except SystemExit as e:
            name = str(e).split(":")[0]
            lv = level[name] = level.get(name, 0) + 1
            if lv > 3:
                raise
            for d in src:
                if d["key"].startswith(name + "#"):
                    k = d["key"]
                    en = ref.get(k) or "Prueba"
                    en = "".join("?" if ch in sta_font.BORROWED else ch for ch in en)
                    texts[k] = (tag(k) + "á" + en, en, tag(k))[lv - 1]
    for name, lv in sorted(level.items()):
        print("  %s: %s" % (name, steps[lv - 1]))
    os.makedirs(os.path.join(S.LOCAL, "build"), exist_ok=True)
    stz = os.path.join(S.LOCAL, "build", "pseudo.STZ")
    with open(stz, "wb") as f:
        f.write(data)
    with open(os.path.join(S.LOCAL, "build", "pseudo.jsonl"), "w", encoding="utf-8") as f:
        for d in src:
            f.write(json.dumps({"key": d["key"], "es": texts[d["key"]]}, ensure_ascii=False) + "\n")
    ps2iso.build(iso_in, stz, iso_out)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    main(*sys.argv[1:])

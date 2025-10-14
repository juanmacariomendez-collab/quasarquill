import os, json
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
BASE = os.path.dirname(ROOT)
NOTES = os.path.join(BASE, "notes")
META  = os.path.join(BASE, "data", "meta")

def run():
    p = os.path.join(META, "index.json")
    if not os.path.exists(p): return False, "index.json not found"
    idx = json.load(open(p, "r", encoding="utf-8"))
    for fn in list(idx.keys()):
        fp = os.path.join(NOTES, fn)
        if os.path.exists(fp):
            txt = open(fp, "r", encoding="utf-8").read()
            idx[fn]["chars"] = len(txt)
    json.dump(idx, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return True, "sample plugin updated 'chars'"
# tweak 2025-10-14T18:49:34.110874+00:00

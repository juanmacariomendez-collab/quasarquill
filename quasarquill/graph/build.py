import os, json, re
from typing import Dict, List

ROOT = os.path.dirname(os.path.dirname(__file__))
BASE = os.path.dirname(ROOT)
META = os.path.join(BASE, "data", "meta")

def slug(s: str) -> str:
    s = re.sub(r"\s+", "-", s.strip().lower())
    s = re.sub(r"[^a-z0-9\-_]+", "", s)
    return s

def load_index():
    p = os.path.join(META, "index.json")
    return json.load(open(p, "r", encoding="utf-8")) if os.path.exists(p) else {}

def load_backlinks():
    p = os.path.join(META, "backlinks.json")
    return json.load(open(p, "r", encoding="utf-8")) if os.path.exists(p) else {}

def build_graph() -> Dict[str, List[str]]:
    idx = load_index()
    title2file = {slug(fn.rsplit(".",1)[0]): fn for fn in idx.keys()}
    g = {fn: [] for fn in idx.keys()}
    for fn, meta in idx.items():
        for link in meta.get("links", []):
            t = title2file.get(slug(link))
            if t and t != fn and t in g:
                g[fn].append(t)
    return g

# autosave 2025-10-06T10:53:50.609328+00:00

# autosave 2025-12-19T17:23:03.636115+00:00

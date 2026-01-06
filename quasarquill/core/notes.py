import os, re, json
from typing import List, Dict, Optional

ROOT = os.path.dirname(os.path.dirname(__file__))
BASE = os.path.dirname(ROOT)
NOTES = os.path.join(BASE, "notes")
META  = os.path.join(BASE, "data", "meta")

RX_LINK = re.compile(r"\[\[([^\[\]]+)\]\]")
RX_TAG  = re.compile(r"(?<!\w)#([a-zA-Z0-9_\-]+)")

def ensure():
    os.makedirs(NOTES, exist_ok=True)
    os.makedirs(META,  exist_ok=True)

def slug(s: str) -> str:
    import re
    s = s.strip().lower()
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[^a-z0-9\-_]+", "", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "note"

def list_notes(max_mb: int = 1) -> List[str]:
    ensure()
    out = []
    for name in os.listdir(NOTES):
        if name.startswith('.') or name.startswith('_'): continue
        if not name.endswith('.md'): continue
        if name.endswith(('.swp','.tmp','.bak','~')): continue
        p = os.path.join(NOTES, name)
        if not os.path.isfile(p): continue
        try:
            if os.path.getsize(p) > max_mb*1024*1024: continue
        except OSError:
            continue
        out.append(name)
    return sorted(out)

def read_note(filename: str) -> Optional[str]:
    p = os.path.join(NOTES, filename)
    return open(p, "r", encoding="utf-8").read() if os.path.exists(p) else None

def write_note(title: str, content: str) -> str:
    ensure()
    fname = slug(title) + ".md"
    p = os.path.join(NOTES, fname)
    with open(p, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n{content.strip()}\n")
    return p

def extract(text: str) -> Dict[str, List[str]]:
    return {
        "links": sorted(set(RX_LINK.findall(text or ""))),
        "tags":  sorted(set(RX_TAG.findall(text or ""))),
    }

def build_index() -> str:
    ensure()
    idx = {}
    for fn in list_notes():
        idx[fn] = extract(read_note(fn) or "")
    out = os.path.join(META, "index.json")
    json.dump(idx, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return out

def build_backlinks() -> str:
    """Создаёт обратные ссылки {target: [sources,...]} на основе index.json"""
    ensure()
    idxp = os.path.join(META, "index.json")
    idx = json.load(open(idxp, "r", encoding="utf-8")) if os.path.exists(idxp) else {}
    bl: Dict[str, List[str]] = {fn: [] for fn in idx.keys()}
    # file slug map
    def _slug_base(fn): return slug(fn.rsplit(".",1)[0])
    by_slug = { _slug_base(fn): fn for fn in idx.keys() }
    for src, meta in idx.items():
        for link in meta.get("links", []):
            tgt = by_slug.get(slug(link))
            if tgt and tgt in bl and tgt != src:
                bl[tgt].append(src)
    out = os.path.join(META, "backlinks.json")
    json.dump(bl, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return out

def search(query: str) -> List[str]:
    """Очень простой фуллтекст: регистронезависимый поиск подстроки по notes/*.md"""
    ensure()
    q = (query or "").strip().lower()
    if not q: return []
    hits = []
    for fn in list_notes():
        txt = (read_note(fn) or "").lower()
        if q in txt:
            hits.append(fn)
    return hits
# tweak 2025-10-24T14:01:36.980344+00:00

# autosave 2025-12-23T17:23:09.344927+00:00

# autosave 2026-01-06T10:35:26.335412+00:00

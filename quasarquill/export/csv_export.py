import os, csv, collections
from ..graph.build import load_index

ROOT = os.path.dirname(os.path.dirname(__file__))
BASE = os.path.dirname(ROOT)
REPORTS = os.path.join(BASE, "reports")

def export_tags_csv() -> str:
    os.makedirs(REPORTS, exist_ok=True)
    idx = load_index()
    p = os.path.join(REPORTS, "tags.csv")
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["file","tags"])
        for fn, meta in idx.items():
            w.writerow([fn, ",".join(meta.get("tags", []))])
    return p

def export_tagfreq_csv() -> str:
    """Частоты тегов по всем заметкам."""
    os.makedirs(REPORTS, exist_ok=True)
    idx = load_index()
    counter = collections.Counter()
    for meta in idx.values():
        counter.update(meta.get("tags", []))
    p = os.path.join(REPORTS, "tagfreq.csv")
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["tag","count"])
        for tag, cnt in counter.most_common():
            w.writerow([tag, cnt])
    return p

import os, json
from ..graph.build import build_graph, load_index, load_backlinks

ROOT = os.path.dirname(os.path.dirname(__file__))
BASE = os.path.dirname(ROOT)
REPORTS = os.path.join(BASE, "reports")

def export_json() -> str:
    os.makedirs(REPORTS, exist_ok=True)
    data = {"index": load_index(), "backlinks": load_backlinks(), "graph": build_graph()}
    p = os.path.join(REPORTS, "export.json")
    json.dump(data, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return p

# autosave 2025-10-07T18:23:13.288888+00:00
# tweak 2025-10-31T21:20:34.085690+00:00
# tweak 2025-12-30T13:24:01.186609+00:00
# tweak 2026-02-03T21:39:01.392222+00:00

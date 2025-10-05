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

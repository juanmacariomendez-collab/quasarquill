import os
from ..graph.build import build_graph

ROOT = os.path.dirname(os.path.dirname(__file__))
BASE = os.path.dirname(ROOT)
REPORTS = os.path.join(BASE, "reports")

def export_graph_dot() -> str:
    """Экспорт графа в Graphviz DOT."""
    os.makedirs(REPORTS, exist_ok=True)
    g = build_graph()
    p = os.path.join(REPORTS, "graph.dot")
    with open(p, "w", encoding="utf-8") as f:
        f.write("digraph quasarquill {\n")
        f.write('  rankdir=LR;\n  node [shape=box, style="rounded"];\n')
        for src, outs in g.items():
            srcq = src.replace('"','\\"')
            if not outs:
                f.write(f'  "{srcq}";\n')
            for dst in outs:
                dstq = dst.replace('"','\\"')
                f.write(f'  "{srcq}" -> "{dstq}";\n')
        f.write("}\n")
    return p

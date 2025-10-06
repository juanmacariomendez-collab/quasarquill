import re, random

TYPO_PROB = 0.04  # 4% rare typos

def _typo_word(w: str) -> str:
    if len(w) < 4: return w
    i = random.randint(1, len(w)-2)
    return w[:i-1] + w[i] + w[i-1] + w[i+1:]

def sprinkle_typos(s: str, prob: float = TYPO_PROB) -> str:
    parts = re.split(r'(`[^`]+`|\w+://\S+|[a-f0-9]{7,40})', s)
    out = []
    for p in parts:
        if p.startswith('`') or '://' in p or re.fullmatch(r'[a-f0-9]{7,40}', p or ''):
            out.append(p); continue
        words = p.split(' ')
        for i,w in enumerate(words):
            if random.random() < prob and re.match(r'[A-Za-z]', w):
                words[i] = _typo_word(w)
        out.append(' '.join(words))
    return ''.join(out)

def humanize(msg: str) -> str:
    m = msg.strip()
    g = re.match(r"(Added|Deleted|Replaced)\s+snippet\s+'([^']+)'\s+(?:in|into|from)\s+(.+)", m, re.I)
    if g:
        kind, name, path = g.group(1).lower(), g.group(2), g.group(3)
        added = [
            f"Add snippet “{name}” to {path}", f"Dropped in snippet “{name}” into {path}",
            f"New code: “{name}” now lives in {path}", f"Introduce “{name}” under {path}",
            f"Wire up “{name}” in {path}", f"Bring in “{name}” to {path}",
            f"Lay down “{name}” in {path}", f"Plant “{name}” inside {path}",
        ]
        deleted = [
            f"Remove “{name}” from {path}", f"Cleanup: deleted “{name}” from {path}",
            f"Trim dead code — “{name}” out of {path}", f"Drop “{name}” from {path}",
            f"Cut “{name}” out of {path}", f"Retire “{name}” from {path}",
            f"Scrub out “{name}” in {path}", f"Prune “{name}” away from {path}",
        ]
        replaced = [
            f"Replace “{name}” in {path}", f"Refresh snippet “{name}” in {path}",
            f"Rework “{name}” — see {path}", f"Swap in a better “{name}” for {path}",
            f"Revamp “{name}” within {path}", f"Overhaul “{name}” in {path}",
            f"Modernize “{name}” inside {path}", f"Refactor “{name}” in {path}",
        ]
        pool = {"added": added, "deleted": deleted, "replaced": replaced}[kind]
        import random
        return sprinkle_typos(random.choice(pool))
    g = re.match(r"Touched\s+(.+?)\s+\(no snippet change\)", m, re.I)
    if g:
        path = g.group(1)
        opts = [
            f"Touch up {path} (no functional change)", f"Small nudge in {path}",
            f"Maintenance tweak in {path}", f"Tiny housekeeping in {path}",
            f"Keep {path} tidy (no logic changes)", f"Polish {path} a little bit",
        ]
        import random
        return sprinkle_typos(random.choice(opts))
    g = re.match(r"Minor tweak in\s+(.+)", m, re.I)
    if g:
        path = g.group(1)
        opts = [
            f"Tiny polish in {path}", f"Minor cleanup in {path}", f"Little fix in {path}",
            f"Small refinement in {path}", f"Light touch-up in {path}", f"Micro-adjustment in {path}",
        ]
        import random
        return sprinkle_typos(random.choice(opts))
    if re.search(r"\btests?\b", m, re.I):
        import random
        return sprinkle_typos(random.choice([
            "Tests: tighten and clarify","Make tests less flaky","Update tests a bit",
            "Tests: improve coverage slightly","Deflake tests around edge cases","Stabilize a couple of tests",
        ]))
    if re.search(r"\bdocs?\b|README", m, re.I):
        import random
        return sprinkle_typos(random.choice([
            "Docs pass: clarify wording","README: quick refresh","Polish docs a little",
            "Docs: add missing bits","Docs cleanup and rewording","Docs: small touch-up across sections",
        ]))
    generic = [
        "Small improvements here and there","A couple of neat touch-ups",
        "Quiet but helpful refactor","Subtle code hygiene improvements",
        "Nip and tuck around the codebase","Sanded down a few rough edges",
        "Quality-of-life tweaks","Tidy up minor inconsistencies",
    ]
    import random
    return sprinkle_typos(m if len(m) > 60 else random.choice(generic))

from datetime import datetime, UTC
import os, sys, random, re, subprocess
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from auto_updater.notify import notify

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SNIPS = os.path.join(ROOT, "data", "snippets")
TARGETS = [os.path.join(ROOT, p) for p in [
    "quasarquill","quasarquill/core","quasarquill/graph","quasarquill/export",
    "quasarquill/plugins","quasarquill/utils","quasarquill/tasks","quasarquill/bookmarks"]]

RX_SNIP = re.compile(r"# --- snippet: (.+?) ---")
RX_END  = re.compile(r"# --- endsnippet ---", re.MULTILINE)
RX_ANCH = re.compile(r"^(def |class )", re.MULTILINE)
P_ADD, P_DEL, P_MINOR = 0.6, 0.2, 0.35

def load_snips():
    m={}
    if not os.path.isdir(SNIPS): return m
    for fn in os.listdir(SNIPS):
        p=os.path.join(SNIPS,fn)
        if not os.path.isfile(p): continue
        tx=open(p,"r",encoding="utf-8").read()
        for s in RX_SNIP.finditer(tx):
            name=s.group(1).strip()
            e=RX_END.search(tx, pos=s.end())
            if not e: continue
            m[name]=tx[s.start():e.end()].strip()+"\n\n"
    return m

def list_py():
    t=[]
    for d in TARGETS:
        for r, dirs, files in os.walk(d):
            dirs[:] = [x for x in dirs if x!="__pycache__"]
            for f in files:
                if f.endswith(".py"): t.append(os.path.join(r,f))
    return t

def blocks(text):
    b={}
    for m in RX_SNIP.finditer(text):
        e=RX_END.search(text, pos=m.end())
        if e: b[m.group(1).strip()] = (m.start(), e.end())
    return b

def insert_at(text, code):
    pts=[m.start() for m in RX_ANCH.finditer(text)]
    pts.append(len(text))
    i=random.choice(pts)
    pre="" if (i==0 or text[max(0,i-1)]=="\n") else "\n"
    return text[:i]+pre+"\n"+code+text[i:]

def replace(text,name,code,b): s,e=b[name]; return text[:s]+code+text[e:]
def delete(text,name,b): s,e=b[name]; return text[:s]+text[e:]

def minor_tweak(path):
    with open(path,"a",encoding="utf-8") as f:
        f.write(f"# tweak {datetime.now(UTC).isoformat()}\n")
    return f"Minor tweak in {os.path.relpath(path, ROOT)}"

def choose_and_apply(snips, targets):
    if not targets: return "No .py targets"
    t=random.choice(targets); txt=open(t,"r",encoding="utf-8").read()
    b=blocks(txt); present=list(b.keys())
    if random.random()<P_MINOR: return minor_tweak(t)
    if present and random.random()<P_DEL:
        name=random.choice(present); new=delete(txt,name,b)
        open(t,"w",encoding="utf-8").write(new); return f"Deleted snippet '{name}' from {os.path.relpath(t,ROOT)}"
    if snips and random.random()<P_ADD:
        name,code=random.choice(list(snips.items()))
        new=replace(txt,name,code,b) if name in b else insert_at(txt,code)
        open(t,"w",encoding="utf-8").write(new)
        return f"{'Replaced' if name in b else 'Added'} snippet '{name}' in {os.path.relpath(t,ROOT)}"
    open(t,"a",encoding="utf-8").write(f"\n# autosave {datetime.now(UTC).isoformat()}\n")
    return f"Touched {os.path.relpath(t,ROOT)} (no snippet change)"

def check_syntax():
    try:
        py=[]
        for r,_,fs in os.walk(ROOT):
            if "__pycache__" in r: continue
            for f in fs:
                if f.endswith(".py"): py.append(os.path.join(r,f))
        if not py: return True
        subprocess.run(["python3","-m","py_compile"]+py, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def git_commit_push(msg):
    try:
        subprocess.run(["git","add","."], check=True)
        r=subprocess.run(["git","commit","-m",humanize(msg)])
        if r.returncode!=0: return False,"No changes to commit"
        subprocess.run(["git","pull","--rebase"])
        subprocess.run(["git","push"], check=True)
        return True,None
    except subprocess.CalledProcessError as e:
        return False,str(e)

def main():
    s=load_snips(); t=list_py()
    msg=choose_and_apply(s,t)
    if not check_syntax():
        notify(f"Syntax error after change: {msg}. Commit aborted."); return
    ok,err=git_commit_push(msg)
    notify(f"{'Committed' if ok else 'Commit failed'}: {msg}" + ("" if ok else f". Error: {err}"))

if __name__=="__main__": main()

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
        r=subprocess.run(["git","commit","-m",msg])
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

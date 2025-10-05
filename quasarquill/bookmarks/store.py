import os, json
from datetime import datetime
from typing import List, Optional, Dict

BASE = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MARKS = os.path.join(BASE, "bookmarks")

def ensure(): os.makedirs(MARKS, exist_ok=True)

def add(url: str, title: Optional[str]=None, tags: Optional[List[str]]=None, note: str="") -> str:
    ensure()
    day = datetime.now().strftime("%Y-%m-%d")
    p = os.path.join(MARKS, f"{day}.json")
    data: Dict[str, list] = {"bookmarks": []}
    if os.path.exists(p): data = json.load(open(p,"r",encoding="utf-8"))
    data["bookmarks"].append({"ts": datetime.now().isoformat(),"url":url,"title":title or "","tags":tags or [],"note":note})
    json.dump(data, open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    return p

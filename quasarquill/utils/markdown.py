import re
HDR = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)
def headings(md: str): return [(m.group(1), m.group(2).strip()) for m in HDR.finditer(md or "")]

# autosave 2025-10-06T09:36:17.436298+00:00
# tweak 2025-11-21T11:47:57.437152+00:00

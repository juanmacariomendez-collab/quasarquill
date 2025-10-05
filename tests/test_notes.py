from quasarquill.core.notes import extract, search
def test_parse_and_search(tmp_path, monkeypatch):
    # локальная папка notes
    d = tmp_path/"notes"; d.mkdir()
    (d/"a.md").write_text("# A\nSee [[B]] #x #y\n", encoding="utf-8")
    (d/"b.md").write_text("# B\nBack to [[A]] #y #z\n", encoding="utf-8")
    from quasarquill.core import notes as N
    monkeypatch.setattr(N, "NOTES", str(d))
    # парсинг
    meta = extract((d/"a.md").read_text(encoding="utf-8"))
    assert "B" in meta["links"] and "x" in meta["tags"]
    # поиск
    monkeypatch.setattr(N, "read_note", lambda fn: (d/fn).read_text(encoding="utf-8"))
    monkeypatch.setattr(N, "list_notes", lambda max_mb=1: ["a.md","b.md"])
    hits = search("back to")
    assert "b.md" in hits

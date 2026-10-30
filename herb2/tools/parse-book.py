#!/usr/bin/env python3
"""원고를 PDF와 별도로 분해해 저장한다(수정·보완용).  사용: python3 tools/parse-book.py
입력 : chapters/chNN.md  (+ figures/chNN/make-figures.py, figures/chNN/data/*.csv)
출력 : parsed/chNN/{body.md, sections.json, refs.json, figures.json, tables.json}
       refs/chNN.md (APA 참고문헌만)  tables/chNN-표N-M.csv  herb2.db(chapters, refs, figures, tables_meta 갱신)"""
import re, json, csv, sqlite3, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
BOOK = json.load(open(ROOT / "book.json", encoding="utf-8"))
CH = [ROOT / "chapters" / f"{k}.md" for k in BOOK["order"] if (k.startswith("ch") or k.startswith("ap")) and (ROOT / "chapters" / f"{k}.md").exists()]
PART_OF = {c: (f"제{v['no']}부 {v['name']}") for v in BOOK["parts"].values() for c in v["chapters"]}
db = sqlite3.connect(ROOT / "herb2.db")
db.executescript("""
create table if not exists chapters(no integer primary key, part text, title text, scope_region text, pages_target int, md_path text, body text, status text default '목차미정');
create table if not exists refs(id integer primary key, chapter_no int, apa7 text, doi text, herbdb_id text);
create table if not exists figures(id integer primary key, label text, chapter_no int, title text, kind text, src_path text, data_path text, bw_variant text, status text);
create table if not exists tables_meta(id integer primary key, label text, chapter_no int, title text, csv_path text, fits_one_page int default 1, status text);
create table if not exists parse_log(ts text, chapter text, n_sections int, n_refs int, n_figs int, n_tables int, chars int);
""")
for t in ("refs", "figures", "tables_meta"):
    db.execute(f"delete from {t}")


def parse_table(lines):
    rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in lines if ln.strip().startswith("|")]
    rows = [r for r in rows if not all(re.fullmatch(r":?-{2,}:?", c) for c in r)]
    return rows


for f in CH:
    stem = f.stem; no = int(re.sub(r"\D", "", stem)) + (100 if stem.startswith("ap") else 0)
    text = f.read_text(encoding="utf-8")
    out = ROOT / "parsed" / stem; out.mkdir(parents=True, exist_ok=True)
    # 장 제목, 절
    title = re.search(r"^# (.+)$", text, re.M).group(1)
    secs = [m.group(1) for m in re.finditer(r"^## (.+)$", text, re.M)]
    # 참고문헌
    refs = []
    m = re.search(r"^## 참고문헌\s*$(.*)", text, re.M | re.S)
    if m:
        for ln in m.group(1).splitlines():
            if ln.startswith("- "):
                r = ln[2:].strip(); doi = re.search(r"https://doi\.org/\S+", r)
                refs.append({"apa7": r, "doi": doi.group(0) if doi else None})
    (ROOT / "refs").mkdir(exist_ok=True)
    (ROOT / "refs" / f"{stem}.md").write_text("# 참고문헌 — " + title + "\n\n" + "\n".join("- " + r["apa7"] for r in refs) + "\n", encoding="utf-8")
    # 그림
    figs = []
    for fm in re.finditer(r"<strong>(그림 [0-9\-]+)\.\s*(.*?)\.?</strong>", text):
        label, ttl = fm.group(1), fm.group(2)
        key = label.replace(" ", "")
        base = ROOT / "figures" / stem
        figs.append({"label": label, "title": ttl, "color": f"figures/{stem}/{key}.png", "bw": f"figures/{stem}/{key}-bw.png",
                     "script": f"figures/{stem}/make-figures.py", "data": f"figures/{stem}/data/",
                     "exists": (base / f"{key}.png").exists()})
    # 표
    tabs = []
    for tm in re.finditer(r"<strong>(표 [A-Z0-9\-]+)\.\s*(.*?)</strong></p>\s*\n(.*?)(?=<p class=\"note\"|</div>)", text, re.S):
        label, ttl, body = tm.group(1), tm.group(2), tm.group(3)
        rows = parse_table(body.splitlines())
        note = re.search(r'<p class="note">(.*?)</p>', text[tm.end():tm.end() + 800], re.S)
        csvp = ROOT / "tables" / f"{stem}-{label.replace(' ', '')}.csv"
        csvp.parent.mkdir(exist_ok=True)
        with open(csvp, "w", encoding="utf-8", newline="") as cf:
            csv.writer(cf).writerows(rows)
        tabs.append({"label": label, "title": ttl, "csv": str(csvp.relative_to(ROOT)), "cols": len(rows[0]) if rows else 0,
                     "rows": len(rows) - 1, "note": note.group(1).strip() if note else ""})
    (out / "body.md").write_text(text, encoding="utf-8")
    json.dump({"title": title, "sections": secs}, open(out / "sections.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(refs, open(out / "refs.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(figs, open(out / "figures.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(tabs, open(out / "tables.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # DB
    db.execute("insert or replace into chapters(no,part,title,pages_target,md_path,body,status) values(?,?,?,?,?,?,?)", (no, ("부록" if stem.startswith("ap") else PART_OF.get(stem, "서장")), title, BOOK["target_pages"].get(stem), f"chapters/{f.name}", text, "초고"))
    for r in refs:
        db.execute("insert into refs(chapter_no,apa7,doi) values(?,?,?)", (no, r["apa7"], r["doi"]))
    for g in figs:
        db.execute("insert into figures(label,chapter_no,title,kind,src_path,data_path,bw_variant,status) values(?,?,?,?,?,?,?,?)",
                   (g["label"], no, g["title"], "그림", g["script"], g["data"], g["bw"], "있음" if g["exists"] else "없음"))
    for t in tabs:
        db.execute("insert into tables_meta(label,chapter_no,title,csv_path,status) values(?,?,?,?,?)", (t["label"], no, t["title"], t["csv"], "초고"))
    db.execute("insert into parse_log values(?,?,?,?,?,?,?)", (datetime.datetime.now().isoformat(timespec="seconds"), stem, len(secs), len(refs), len(figs), len(tabs), len(text)))
    print(f"{stem}: 절 {len(secs)}, 참고문헌 {len(refs)}, 그림 {len(figs)}, 표 {len(tabs)}, {len(text):,}자")
db.commit()

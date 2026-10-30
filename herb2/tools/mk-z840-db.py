#!/usr/bin/env python3
"""herb2 책 DB 패키지 생성 (z840 HDD 보관용).
사용: python3 tools/mk-z840-db.py v1
결과: z840db/herb2bookdb-<ver>/  (폴더 안에 DB + 원본 소스 + PDF + SHA256SUMS + README)
내용: 원고·절·참고문헌·그림(컬러/흑백 PNG 포함)·표·검증목록·조판 규칙(CSS·판형·글꼴)·빌드 스크립트·쪽별 지도·빈칸 점검·PDF 해시."""
import sys, re, json, pathlib, sqlite3, subprocess, hashlib, shutil, datetime, tempfile, glob, os
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
VER = sys.argv[1] if len(sys.argv) > 1 else "v1"
OUT = ROOT / "z840db" / f"herb2bookdb-{VER}"
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir(parents=True)
DB = OUT / f"herb2bookdb-{VER}.db"
now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
rd = lambda p: pathlib.Path(p).read_text(encoding="utf-8")
sha = lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
book = json.loads(rd(ROOT / "book.json"))
git = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()

c = sqlite3.connect(DB)
c.executescript("""
create table meta(key text primary key, value text);
create table parts(no int primary key, key text, name text, sub text, chapters text);
create table chapters(no int primary key, code text, title text, part_no int, md text, verify_md text, chars int, n_sections int, n_figs int, n_tables int, n_refs int, page_start_color int, page_end_color int, page_start_bw int, page_end_bw int);
create table sections(id integer primary key, chapter_no int, seq int, heading text, page_color int, page_bw int);
create table refs(id integer primary key, chapter_no int, seq int, apa7 text, doi text);
create table figures(id integer primary key, label text, chapter_no int, seq int, title text, caption text, alt text, png_color blob, png_bw blob, width_px int, height_px int, data_csv text, page_color int, page_bw int);
create table tables_(id integer primary key, label text, chapter_no int, seq int, title text, markdown text, csv text, page_color int, page_bw int);
create table figscripts(chapter_no int primary key, script text);
create table figdata(chapter_no int, name text, csv text);
create table typeset(key text primary key, value text, note text);
create table scripts(name text primary key, content text);
create table docs(name text primary key, content text);
create table pagemap(edition text, page int, chapter_no int, first_line text, bottom_blank_pct real, flagged int, captions text, headings text, primary key(edition, page));
create table files(path text primary key, bytes int, sha256 text, role text);
""")
M = lambda k, v: c.execute("insert or replace into meta values(?,?)", (k, str(v)))
for k, v in {"title": book["title"], "subtitle": book["subtitle"], "version": VER, "built": now, "git_commit": git,
             "format": "B5 182x257mm", "engine": "markdown + WeasyPrint", "editions": "color,bw",
             "purpose": "허브책 내용+조판 데이터 보존(z840 dball2). 향후 수정·재조판·지역별 책 제작용"}.items(): M(k, v)
for k, p in book["parts"].items():
    c.execute("insert into parts values(?,?,?,?,?)", (p["no"], k, p["name"], p["sub"], ",".join(p["chapters"])))
part_of = {ch: p["no"] for p in book["parts"].values() for ch in p["chapters"]}

# ---------- 쪽 지도 ----------
def pages_of(pdf):
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout).group(1))
    d = tempfile.mkdtemp(); subprocess.run(["pdftoppm", "-r", "40", "-png", str(pdf), d + "/p"], check=True)
    blank = {}
    for f in sorted(glob.glob(d + "/p-*.png")):
        im = Image.open(f).convert("L"); w, h = im.size; top = int(h*.085); bot = int(h*.90); last = top
        for y in range(bot, top, -1):
            if min(im.crop((0, y, w, y+1)).getdata()) < 200: last = y; break
        blank[int(os.path.basename(f)[2:-4])] = ((bot-last)/(bot-top), last > top)
    txt = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout.split("\f")
    return n, blank, txt
pm = {}
cur_ch = {}
for ed in ("color", "bw"):
    pdf = ROOT / "build" / f"herb2-world-{VER}-{ed}.pdf"
    if not pdf.exists(): pdf = ROOT / "build" / f"herb2-world-v1-{ed}.pdf"
    n, blank, txt = pages_of(pdf); ch = -1
    pm[ed] = {}
    # 장 시작 쪽: 쪽의 첫 줄이 장 제목으로 시작하는 쪽(순서대로 탐색)
    starts = {}; nxt = 1
    titles = {}
    for code in [x for x in book["order"] if x.startswith(("ch", "ap"))]:
        mp = ROOT / "chapters" / f"{code}.md"
        if mp.exists(): titles[int(code[2:]) + (100 if code.startswith("ap") else 0)] = re.sub(r"^\d+장\.\s*", "", re.search(r"^#\s+(.+)$", rd(mp), re.M).group(1))[:10].replace(" ", "")
    for no in sorted(titles):
        for i in range(nxt, n+1):
            t = txt[i-1] if i-1 < len(txt) else ""
            fl = next((l.strip() for l in t.split("\n") if l.strip()), "")
            if titles[no] in fl.replace(" ", "") and not fl.startswith("목"):
                starts[no] = i; nxt = i + 1; break
    for i in range(1, n+1):
        ch = max([no for no, sp in starts.items() if sp <= i], default=-1)
        t = txt[i-1] if i-1 < len(txt) else ""
        caps = re.findall(r"^\s*((?:그림|표) [A-Z\d]+-\d+)\.", t, re.M)
        heads = re.findall(r"^\s*(\d+\. [^\n]{2,40}|이 장을 읽기 전에|이 장을 마치며|참고문헌)\s*$", t, re.M)
        b, nonempty = blank.get(i, (0, False))
        pm[ed][i] = dict(ch=ch, caps=caps, heads=heads)
        c.execute("insert into pagemap values(?,?,?,?,?,?,?,?)", (ed, i, ch, next((l.strip() for l in t.split("\n") if l.strip()), ""), round(b*100, 1), int(b > .15 and nonempty), ",".join(caps), "|".join(h.strip() for h in heads)))
    c.execute("insert or replace into files values(?,?,?,?)", (f"pdf/{pdf.name}", pdf.stat().st_size, sha(pdf), f"pdf-{ed}"))
    (OUT / "pdf").mkdir(exist_ok=True); shutil.copy2(pdf, OUT / "pdf" / pdf.name)
def page_of(ed, key):
    for p, d in pm[ed].items():
        if key in d["caps"]: return p
def head_page(ed, ch, head):
    for p, d in pm[ed].items():
        if d["ch"] == ch and any(head in h for h in d["heads"]): return p

# ---------- 장 ----------
CODES = [x for x in book["order"] if x.startswith(("ch", "ap"))]
for code in CODES:
    no = int(code[2:]) + (100 if code.startswith("ap") else 0); mdp = ROOT / "chapters" / f"{code}.md"
    if not mdp.exists(): continue
    md = rd(mdp); vp = ROOT / "chapters" / f"verify-{code}.md"
    title = re.search(r"^#\s+(.+)$", md, re.M).group(1)
    secs = re.findall(r"^##\s+(.+)$", md, re.M)
    figs = re.findall(r'<figcaption><strong>(그림 \d+-\d+)\.\s*(.*?)</strong>\s*(.*?)</figcaption>', md, re.S)
    opener = re.search(r'<p class="fig-cap"><strong>(그림 \d+-\d+)\.\s*(.*?)</strong>\s*(.*?)</p>', md, re.S)
    figl = ([opener.groups()] if opener else []) + figs
    tbls = re.findall(r'<div class="tblwrap" markdown="1">\s*<p class="cap"><strong>(표 [A-Z\d]+-\d+)\.\s*(.*?)</strong></p>\s*(.*?)</div>', md, re.S)
    refpart = md.split("## 참고문헌")[-1] if "## 참고문헌" in md else ""
    refs = [l[2:].strip() for l in refpart.splitlines() if l.startswith("- ")]
    ps = [p for p, d in pm["color"].items() if d["ch"] == no]; pb = [p for p, d in pm["bw"].items() if d["ch"] == no]
    c.execute("insert into chapters values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (no, code, title, part_of.get(code), md, rd(vp) if vp.exists() else None, len(md), len(secs), len(figl), len(tbls), len(refs), min(ps, default=None), max(ps, default=None), min(pb, default=None), max(pb, default=None)))
    for i, h in enumerate(secs, 1):
        c.execute("insert into sections(chapter_no,seq,heading,page_color,page_bw) values(?,?,?,?,?)", (no, i, h, head_page("color", no, h.split(". ", 1)[-1] if re.match(r"\d+\. ", h) else h), head_page("bw", no, h.split(". ", 1)[-1] if re.match(r"\d+\. ", h) else h)))
    for i, r in enumerate(refs, 1):
        d = re.search(r"https?://doi\.org/\S+", r)
        c.execute("insert into refs(chapter_no,seq,apa7,doi) values(?,?,?,?)", (no, i, r, d.group(0) if d else None))
    fd = ROOT / "figures" / code
    for i, (lab, ttl, cap) in enumerate(figl, 1):
        f1 = fd / f"그림{lab.split()[1]}.png"; f2 = fd / f"그림{lab.split()[1]}-bw.png"
        alt = re.search(r'alt="([^"]*)"', md[md.find(lab) - 400: md.find(lab)] if lab in md else "")
        csvp = None
        w = h = None
        if f1.exists(): w, h = Image.open(f1).size
        c.execute("insert into figures(label,chapter_no,seq,title,caption,alt,png_color,png_bw,width_px,height_px,page_color,page_bw) values(?,?,?,?,?,?,?,?,?,?,?,?)",
                  (lab, no, i, ttl, re.sub(r"<[^>]+>", "", cap).strip(), alt.group(1) if alt else None, f1.read_bytes() if f1.exists() else None, f2.read_bytes() if f2.exists() else None, w, h, page_of("color", lab), page_of("bw", lab)))
    for i, (lab, ttl, body) in enumerate(tbls, 1):
        c.execute("insert into tables_(label,chapter_no,seq,title,markdown,csv,page_color,page_bw) values(?,?,?,?,?,?,?,?)",
                  (lab, no, i, ttl, body.strip(), None, page_of("color", lab), page_of("bw", lab)))
        cp = ROOT / "tables" / f"{code}-{lab}.csv"
        if cp.exists(): c.execute("update tables_ set csv=? where label=?", (rd(cp), lab))
    if (fd / "make-figures.py").exists(): c.execute("insert into figscripts values(?,?)", (no, rd(fd / "make-figures.py")))
    if (fd / "data").exists():
        for cp in sorted((fd / "data").glob("*.csv")): c.execute("insert into figdata values(?,?,?)", (no, cp.name, rd(cp)))

# ---------- 조판 데이터 ----------
bp = rd(ROOT / "tools" / "build-pdf.py")
css = re.search(r'CSS = """(.*?)"""', bp, re.S)
bwx = re.search(r'BW_EXTRA = "(.*?)"', bp)
T = lambda k, v, n="": c.execute("insert or replace into typeset values(?,?,?)", (k, v, n))
T("css", css.group(1) if css else "", "tools/build-pdf.py 의 CSS")
T("css-bw-extra", bwx.group(1) if bwx else "", "흑백판 추가 CSS")
T("page-size", "182mm x 257mm (B5)", "")
T("margins", "위20 바깥/안쪽 18/22 아래22mm, 홀짝 쪽 좌우 반전", "@page 규칙")
T("body-font", "Noto Serif CJK KR 10.5pt, 줄간격 1.72, 양끝맞춤, keep-all", "")
T("heading-font", "Noto Sans CJK KR, 장 22pt, 절 13.5pt", "")
T("ref-font", "본문-1pt(9.5pt), 줄간격 1.45", "bookrule2")
T("figure-font", "matplotlib Noto Sans CJK KR, 300dpi, 컬러+흑백(-bw)", "figures/chNN/make-figures.py")
T("rules", "그림·표 번호+제목, 표는 쪽 나뉨 금지, 아래 빈칸 15% 초과 점검, 컬러/흑백 2판, 파일명 언더바 금지", "bookrule2")
T("layout-check-threshold", "15% (check-layout.py)", "")
T("page-count-color", str(len(pm["color"])), ""); T("page-count-bw", str(len(pm["bw"])), "")
T("fonts", subprocess.run("fc-list | grep -i 'NotoSansCJK\\|NotoSerifCJK' | cut -d: -f1 | sort -u", shell=True, capture_output=True, text=True).stdout, "빌드 환경 글꼴 파일")
T("book-json", rd(ROOT / "book.json"), "장 순서·부 구분")
for p in sorted((ROOT / "tools").glob("*.py")): c.execute("insert or replace into scripts values(?,?)", (f"tools/{p.name}", rd(p)))
for p in sorted((ROOT / "docs").glob("*.md")): c.execute("insert or replace into docs values(?,?)", (f"docs/{p.name}", rd(p)))
for p in sorted((ROOT / "chapters").glob("toc*.md")): c.execute("insert or replace into docs values(?,?)", (f"chapters/{p.name}", rd(p)))
# 기존 herb2.db(규칙·할 일 등) 사본 테이블
old = ROOT / "herb2.db"
if old.exists():
    c.execute("attach database ? as o", (str(old),))
    for t in ("rules", "layout", "cover_spec", "todo", "sources_db"):
        try: c.execute(f"create table old_{t} as select * from o.{t}")
        except Exception as e: print("skip", t, e)
    c.commit(); c.execute("detach database o")
c.commit(); c.execute("vacuum")

# ---------- 원본 소스 사본 + 해시 ----------
SRC = OUT / "src"
for d in ("chapters", "figures", "refs", "tables", "tools", "docs", "cover"):
    if (ROOT / d).exists(): shutil.copytree(ROOT / d, SRC / d)
shutil.copy2(ROOT / "book.json", SRC / "book.json")
corp = ROOT / "corpus" / "herbcorpus-rel-v1.jsonl"
if corp.exists(): M("corpus_sha256", sha(corp)); M("corpus_file", "corpus/herbcorpus-rel-v1.jsonl (7,182편, 패키지에는 미포함 — 저장소·herb_db에 있음)")
c.commit()
(OUT / "README.txt").write_text(f"""herb2bookdb-{VER} — 《{book['title']}》 {book['subtitle']}
만든 때 {now} / 저장소 커밋 {git}

폴더 구성
  herb2bookdb-{VER}.db  SQLite 한 파일. 표: meta parts chapters sections refs figures(PNG 컬러·흑백 포함) tables_ figscripts figdata typeset(CSS·판형·글꼴) scripts docs pagemap(쪽별 지도·아래 빈칸) old_* files
  pdf/                  컬러판·흑백판 PDF
  src/                  원고·그림 스크립트·표 CSV·빌드 도구 원본 (이대로 python3 tools/build-pdf.py both 로 재조판 가능; 코퍼스 제외)
  SHA256SUMS            전체 파일 해시

조회 예
  sqlite3 herb2bookdb-{VER}.db "select no,title,page_start_color,page_end_color from chapters"
  python3 -c "import sqlite3;c=sqlite3.connect('herb2bookdb-{VER}.db');print(c.execute('select label,title,page_color from figures limit 5').fetchall())"
""", encoding="utf-8")
c.close()
rows = []
for p in sorted(OUT.rglob("*")):
    if p.is_file() and p.name != "SHA256SUMS": rows.append((str(p.relative_to(OUT)), p.stat().st_size, sha(p)))
c = sqlite3.connect(DB)
for r in rows:
    if not r[0].endswith(".db"): c.execute("insert or replace into files values(?,?,?,?)", (r[0], r[1], r[2], "pack"))
c.commit(); c.close()
(OUT / "SHA256SUMS").write_text("".join(f"{h}  {p}\n" for p, s, h in rows if not p.endswith(".db")) + f"{sha(DB)}  {DB.name}\n")
print("완료", OUT, "DB", DB.stat().st_size, "bytes")

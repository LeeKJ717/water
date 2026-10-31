#!/usr/bin/env python3
"""herb2 PDF 빌드 v1.  사용: python3 tools/build-pdf.py [color|bw|both]
chapters/ch*.md -> build/herb2-world-v1-color.pdf, build/herb2-world-v1-bw.pdf
B5(182x257mm), 쪽번호, 목차(쪽번호), 그림·표 쪼개짐 방지, 참고문헌 1pt 작게."""
import re, sys, pathlib, markdown, weasyprint

ROOT = pathlib.Path(__file__).resolve().parent.parent
VER = next((a.split("=",1)[1] for a in sys.argv if a.startswith("--ver=")), "v1")
TITLE = "풀이 약이 되기까지"
SUB = "세계 허브의 과학사 (가제)"
MODE = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "both"
OPT = "--noopt" not in sys.argv

CSS = """
@page { size:182mm 257mm; margin:20mm 18mm 22mm 22mm;
  @bottom-center { content:counter(page); font:9pt 'Noto Sans CJK KR'; color:#444 } }
@page :right { margin-left:22mm; margin-right:18mm }
@page :left  { margin-left:18mm; margin-right:22mm }
@page cover { @bottom-center { content:none } }
body { font-family:'Noto Serif CJK KR','Noto Sans CJK KR'; font-size:10.5pt; line-height:1.72; color:#111; text-align:justify; word-break:keep-all }
h1 { font-family:'Noto Sans CJK KR'; font-size:22pt; margin:0 0 10mm; page-break-before:always }
h2 { font-family:'Noto Sans CJK KR'; font-size:13.5pt; margin:8mm 0 3mm; border-bottom:.6pt solid #888; padding-bottom:1mm; page-break-after:avoid }
p { margin:0 0 2.6mm; orphans:3; widows:3 }
ul { margin:0 0 3mm 5mm; padding:0 }
.cover { page:cover; page-break-after:always; text-align:center; padding-top:70mm }
.cover .t { font:900 34pt 'Noto Sans CJK KR'; margin-bottom:8mm } .cover .s { font:16pt 'Noto Sans CJK KR'; color:#444 }
.cover .a { margin-top:60mm; font:13pt 'Noto Sans CJK KR' }
nav.toc { page-break-after:always } nav.toc h1 { page-break-before:avoid }
nav.toc a { color:#111; text-decoration:none }
nav.toc li { list-style:none; margin:0 0 2mm } nav.toc ul { margin:0; padding:0 }
nav.toc li.l0 { font:900 12.5pt 'Noto Sans CJK KR'; margin-top:5mm } nav.toc li.l1 { font:700 11.5pt 'Noto Sans CJK KR'; margin-top:3mm }
nav.toc li.l2 { margin-left:6mm; font-size:10pt }
nav.toc a::after { content:leader('.') target-counter(attr(href), page) }
figure.fig, div.tblwrap { page-break-inside:avoid; margin:4mm 0 5mm; text-align:center }
figure.fig img { max-width:100%; max-height:76mm }
figcaption, p.cap, p.fig-cap { font:9pt/1.5 'Noto Sans CJK KR'; text-align:left; margin-top:2mm }
p.cap { margin:0 0 1.5mm } p.note { font:8.5pt/1.5 'Noto Sans CJK KR'; color:#444; text-align:left; margin:1.5mm 0 0 }
table { border-collapse:collapse; width:100%; font:8.8pt/1.45 'Noto Sans CJK KR'; page-break-inside:avoid; text-align:left }
th, td { border:.5pt solid #777; padding:1.2mm 1.8mm; vertical-align:top } th { background:#e6e6e6 }
.opener { page-break-after:always; text-align:center }
.opener img { width:142mm; margin-top:12mm } .mini-toc { font:9.5pt 'Noto Sans CJK KR'; margin:8mm 15mm; text-align:left }
.pagebreak { page-break-after:always }
.idx { column-count:2; column-gap:8mm; list-style:none; padding:0; margin:0; font:8.6pt/1.4 'Noto Sans CJK KR' } .idx li { break-inside:avoid; margin:0 0 .6mm }
.partpage { page-break-before:always; page-break-after:always; text-align:center; padding-top:70mm }
.partpage h1.parth { font-size:26pt; page-break-before:avoid; margin-bottom:6mm }
.partsub { font:13pt 'Noto Sans CJK KR'; color:#444 } .partpage ul { list-style:none; margin-top:14mm; font:11pt 'Noto Sans CJK KR' } .partpage li { margin-bottom:3mm }
div.refs { font-size:9.5pt; line-height:1.45 } div.refs li { margin-bottom:1.6mm; padding-left:6mm; text-indent:-6mm; list-style:none; text-align:left; word-break:break-all }
div.refs h2 { font-size:12pt }
"""
BW_EXTRA = "img { filter:grayscale(1) }"


def md_to_html(text):
    return markdown.markdown(text, extensions=["tables", "md_in_html", "sane_lists"], output_format="html5")


def post(h, bw):
    # 그림: <p><img ...></p><p><strong>그림 ...</strong> ...</p> -> figure
    h = re.sub(r'<p>(<img[^>]*/?>)</p>\s*<p>(<strong>그림.*?)</p>', r'<figure class="fig">\1<figcaption>\2</figcaption></figure>', h, flags=re.S)
    # 참고문헌 섹션을 div.refs 로
    h = re.sub(r'(<h2[^>]*>참고문헌</h2>)(.*?)(?=<h1|\Z)', r'<div class="refs">\1\2</div>', h, flags=re.S)
    if bw:
        h = re.sub(r'(src="[^"]*?)\.png"', r'\1-bw.png"', h)
    return h



# ---------------- 자동 배치: 쪽 아래 빈칸이 큰 곳에서 그림·표와 뒤 문단 자리를 바꿔 본다 ----------------
import subprocess, tempfile, glob, os
from bs4 import BeautifulSoup
from PIL import Image


def _gaps(pdf):
    d = tempfile.mkdtemp()
    subprocess.run(["pdftoppm", "-r", "40", "-png", pdf, d + "/p"], check=True)
    out = []
    for f in sorted(glob.glob(d + "/p-*.png")):
        im = Image.open(f).convert("L"); w, h = im.size
        top, bot = int(h * .085), int(h * .90)
        px = im.load(); last = top
        for y in range(bot, top, -1):
            if any(px[x, y] < 200 for x in range(0, w, 2)):
                last = y; break
        out.append((bot - last) / (bot - top))
    return out


def _first_line(pdf, page):
    t = subprocess.run(["pdftotext", "-f", str(page), "-l", str(page), "-layout", pdf, "-"], capture_output=True, text=True).stdout
    for ln in t.splitlines():
        if ln.strip():
            return ln.strip()
    return ""


def optimize_chapter(html, bw):
    soup = BeautifulSoup(html, "html.parser")
    kids = [str(c) for c in soup.contents if str(c).strip()]

    def kind(x):
        return "float" if ('class="fig"' in x[:40] or 'class="tblwrap"' in x[:40]) else ("p" if x.startswith("<p") or x.startswith("<ul") else "other")

    def render(ks):
        full = f'<html lang="ko"><head><meta charset="utf-8"><style>{CSS}{BW_EXTRA if bw else ""}</style></head><body>{"".join(ks)}</body></html>'
        tmp = tempfile.mktemp(suffix=".pdf")
        weasyprint.HTML(string=full, base_url=str(ROOT / "chapters") + "/").write_pdf(tmp)
        g = _gaps(tmp)
        return tmp, g

    def score(g):
        # 첫 쪽(장 머리)·마지막 쪽(참고문헌 끝)은 제외
        return sum(max(0.0, x - .12) for x in g[1:-1])

    tmp, g = render(kids)
    best, bests = kids, score(g)
    tried = set()
    for _ in range(30):
        cand = None
        for pg in range(1, len(g) - 1):
            if g[pg] > .15:
                fl = _first_line(tmp, pg + 2)
                for i, x in enumerate(best):
                    if kind(x) == "float":
                        m = re.search(r"<strong>((?:그림|표) [0-9\-]+)", x)
                        if m and fl.startswith(m.group(1)) and (m.group(1) not in tried):
                            cand = (i, m.group(1)); break
            if cand: break
        if not cand: break
        i, name = cand; tried.add(name)
        j = next((k for k in range(i + 1, len(best)) if kind(best[k]) == "p"), None)
        if j is None: continue
        trial = list(best); trial[i], trial[j] = trial[j], trial[i]
        # 문단 하나를 그림 앞으로 옮기는 효과: i 위치에 p, 그림은 한 칸 뒤로
        trial = list(best); blk = trial.pop(j); trial.insert(i, blk)
        t2, g2 = render(trial)
        if score(g2) < bests:
            best, bests, tmp, g = trial, score(g2), t2, g2
            tried.discard(name)
    return "".join(best)


def toc(html):
    items = []
    for m in re.finditer(r'<h([12])[^>]*>(.*?)</h\1>', html, flags=re.S):
        items.append((m.group(1), re.sub('<.*?>', '', m.group(2))))
    return items


def build(bw):
    import json
    book = json.load(open(ROOT / "book.json", encoding="utf-8"))
    titles = {}
    for f in (ROOT / "chapters").glob("ch[0-9]*.md"):
        m = re.search(r"^# (.+)$", f.read_text(encoding="utf-8"), re.M)
        titles[f.stem] = m.group(1) if m else f.stem
    chap_files = []
    parts = []
    for key in book["order"]:
        if key.startswith("part"):
            pt = book["parts"][key]
            lis = "".join(f"<li>{titles.get(c) or book.get("titles", {}).get(c, c)}</li>" for c in pt["chapters"])
            parts.append(f'<div class="partpage"><h1 class="parth">제{pt["no"]}부 {pt["name"]}</h1><p class="partsub">{pt["sub"]}</p><ul>{lis}</ul></div>')
            continue
        f = ROOT / "chapters" / f"{key}.md"
        if not f.exists():
            continue
        hh = post(md_to_html(f.read_text(encoding="utf-8")), bw)
        parts.append(optimize_chapter(hh, bw) if OPT else hh)
    body = "\n".join(parts)
    # id 부여 + 목차
    n = [0]; entries = []
    def rep(m):
        n[0] += 1; i = f"s{n[0]}"; lvl = m.group(1)
        txt = re.sub('<.*?>', '', m.group(3))
        if lvl == "1" and 'class="parth"' in m.group(2):
            entries.append(("0", i, txt))
        elif lvl == "1" or txt in ("참고문헌",):
            entries.append((lvl, i, txt))
        elif lvl == "2":
            entries.append((lvl, i, txt))
        return f'<h{lvl} id="{i}"{m.group(2)}>{m.group(3)}</h{lvl}>'
    body = re.sub(r'<h([12])([^>]*)>(.*?)</h\1>', rep, body, flags=re.S)
    toc_html = '<nav class="toc"><h1 style="font-size:18pt">목 차</h1><ul>' + "".join(
        f'<li class="l{l}"><a href="#{i}">{t}</a></li>' for l, i, t in entries if not (l == "2" and t.startswith("이 장을"))) + "</ul></nav>"
    cover = f'<div class="cover"><div class="t">{TITLE}</div><div class="s">{SUB}</div><div class="a">이광조 지음<br/><br/>과학과영성출판사</div></div>'
    html = f'<html lang="ko"><head><meta charset="utf-8"><style>{CSS}{BW_EXTRA if bw else ""}</style></head><body>{cover}{toc_html}{body}</body></html>'
    out = ROOT / "build" / f"herb2-world-{VER}-{'bw' if bw else 'color'}.pdf"
    out.parent.mkdir(exist_ok=True)
    weasyprint.HTML(string=html, base_url=str(ROOT / "chapters") + "/").write_pdf(str(out))
    print("wrote", out)


if __name__ == "__main__":
    if MODE in ("color", "both"): build(False)
    if MODE in ("bw", "both"): build(True)

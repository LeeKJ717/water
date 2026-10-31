import json, re, glob, sys, unicodedata
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
meta = {}
for l in open(ROOT/"corpus/crossref-meta-v1.jsonl", encoding="utf-8"):
    d = json.loads(l); meta[d["doi"].lower()] = d
def fold(s): return re.sub(r"[^a-z]", "", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower())
def pg(s): return (s or "").replace("-", "–").replace("—", "–").strip()
rows = []; nodoi = []
for f in sorted(glob.glob(str(ROOT/"chapters/ch*.md"))):
    code = Path(f).stem; txt = Path(f).read_text(encoding="utf-8")
    if "## 참고문헌" not in txt: continue
    for ln in txt.split("## 참고문헌", 1)[1].splitlines():
        if not ln.startswith("- "): continue
        m = re.search(r"https://doi\.org/(\S+?)\s*$", ln)
        if not m: nodoi.append((code, ln[:90])); continue
        doi = m.group(1).lower(); d = meta.get(doi)
        if not d: rows.append((code, doi, "메타 없음", ln[:80])); continue
        pr = []
        ym = re.search(r"\((\d{4})[a-z]?\)", ln)
        if ym and d["year"] and int(ym.group(1)) != d["year"]: pr.append(f"연도 {ym.group(1)}→{d['year']}")
        jm = re.search(r"\*([^*]+?),\s*([^*]+)\*(?:\((\w+)\))?,?\s*([^.]*?)\.\s*https", ln)
        if jm:
            vol = jm.group(2).strip(); iss = jm.group(3); rest = jm.group(4).strip()
            if d["volume"] and vol != d["volume"]: pr.append(f"권 {vol}→{d['volume']}")
            if d["issue"] and iss != d["issue"]: pr.append(f"호 {iss}→{d['issue']}")
            want = pg(d["page"]) or (f"Article {d['article']}" if d["article"] else "")
            if want and pg(rest) != want: pr.append(f"쪽 {rest}→{want}")
        else: pr.append("서지 형식 해석 불가")
        # 저자: 성 비교(첫 저자와 수)
        am = ln.split("(")[0]
        mine = [fold(x.split(",")[0]) for x in re.split(r",\s*(?:&\s*)?(?=[^,]+,\s*[A-Z]\.)", am.replace(" & ", ", & ")) if x.strip()]
        theirs = [fold(a[0]) for a in d["authors"]]
        if theirs and mine and mine[0] != theirs[0][:len(mine[0])] and not theirs[0].startswith(mine[0][:6]): pr.append(f"첫저자 {mine[0]}≠{theirs[0]}")
        n_alt = len(d["authors"])
        if n_alt <= 20 and abs(len(mine) - n_alt) > 0 and ". . ." not in ln: pr.append(f"저자수 {len(mine)}→{n_alt}")
        if pr: rows.append((code, doi, "; ".join(pr), ""))
print("문제", len(rows), "DOI 없음", len(nodoi))
for r in rows: print(*r, sep=" | ")
print("--- DOI 없는 항목"); [print(*n, sep=" | ") for n in nodoi]

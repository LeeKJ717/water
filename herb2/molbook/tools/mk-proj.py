#!/usr/bin/env python3
"""molbook 프로젝트 골격 생성. TOC(v3) -> book.json, chapters/chNN.md 뼈대, evidence/chNN.md(장별 근거 목록), refs/chNN.md.
사용: python3 herb2/molbook/tools/mk-proj.py   (재실행 시 chapters/*.md 본문은 덮어쓰지 않음)"""
import re, json, gzip, pathlib, collections
R = pathlib.Path(__file__).resolve().parent.parent
toc = (R.parent / "docs" / "molbook-toc-v3.md").read_text(encoding="utf-8").splitlines()
parts, chs, cur_part, cur = [], {}, None, None
for ln in toc:
    m = re.match(r"## (제(\d)부\. (.+))", ln)
    if m: cur_part = {"no": int(m[2]), "name": m[3], "chapters": []}; parts.append(cur_part); continue
    if ln.startswith("## "): cur_part = None; continue
    m = re.match(r"### (서장|(\d+)장)\. (.+)", ln)
    if m:
        code = "ch00" if m[1] == "서장" else f"ch{int(m[2]):02d}"
        cur = chs[code] = {"title": ("서장. " if code == "ch00" else f"{int(m[2])}장. ") + m[3], "herbs": "", "signal": [], "fig": ""}
        if cur_part: cur_part["chapters"].append(code)
        continue
    if cur is None: continue
    if ln.startswith("- 배정 허브:"): cur["herbs"] = ln.split(":", 1)[1].strip()
    elif ln.startswith("  - "): cur["signal"].append(ln[4:].strip())
    elif ln.startswith("- 그림 계획:"): cur["fig"] = ln.split(":", 1)[1].strip()
order = ["ch00"]
for p in parts: order += [f"part{p['no']}"] + p["chapters"]
order += ["ap1", "ap2", "ap3"]
book = {"title": "인체 속 허브의 분자생물학", "subtitle": "풀의 분자가 몸의 세포에 말을 거는 방식 (가제)", "version": "v1",
        "author": "이광조", "publisher": "과학과영성출판사", "toc": "v3", "order": order,
        "parts": {f"part{p['no']}": {"no": p["no"], "name": p["name"], "chapters": p["chapters"]} for p in parts},
        "titles": {k: v["title"] for k, v in chs.items()} | {"ap1": "부록 A. 분자생물학 용어집", "ap2": "부록 B. 표적 도감표", "ap3": "부록 C. 참고문헌 색인"}}
(R / "book.json").write_text(json.dumps(book, ensure_ascii=False, indent=1), encoding="utf-8")
for d in ("chapters", "refs", "evidence", "figures"): (R / d).mkdir(exist_ok=True)

P = [json.loads(l) for l in gzip.open(R / "corpus" / "molbook-papers-v1.jsonl.gz", "rt", encoding="utf-8")]
P = [p for p in P if not p["retracted"] and p["title"]]
bych = collections.defaultdict(lambda: collections.defaultdict(dict))
for p in P:
    for ch, herb, q in p["tags"]:
        bych[f"ch{int(ch):02d}"][(herb, q)][p["id"]] = p
GEN = {"herbal","compounds","compound","natural","products","product","extract","extracts","mechanism","mechanisms","plant","plants","medicine","clinical","trial","trials","review","and","of","in","the","from"}
def core(q): return [t for t in re.findall(r"[a-z0-9κβα\-]+", q.lower()) if t not in GEN]
def frac(p, toks):
    t = ((p["title"] or "") + " " + (p["abstract"] or "")).lower()
    return sum(1 for k in toks if k[:6] in t) / len(toks) if toks else 0
def apa_auth(a):
    if isinstance(a, str):
        try: a = json.loads(a)
        except Exception: a = [a]
    a = a or []
    return (", ".join(a[:3]) + (" 외" if len(a) > 3 else "")) if a else "(저자 미상)"
for code, c in chs.items():
    stub = R / "chapters" / f"{code}.md"
    if not stub.exists():
        sig = "\n".join(f"  - {s}" for s in c["signal"])
        stub.write_text(f"# {c['title']}\n\n<!-- 배정 허브: {c['herbs']}\n세포신호:\n{sig}\n그림 계획: {c['fig']} -->\n\n"
                        "## 이 장을 읽기 전에\n\n(집필 전)\n\n## 참고문헌\n\n", encoding="utf-8")
    (R / "refs" / f"{code}.md").touch()
    out = [f"# 근거 목록 — {c['title']}\n", f"배정 허브: {c['herbs']}\n"]
    n = 0
    for (herb, q), D in sorted(bych.get(code, {}).items()):
        tk = core(q)
        cand = [(frac(p, tk), p) for p in D.values()]
        cand = [x for x in cand if x[0] >= 0.99] or [x for x in cand if x[0] >= 0.5]
        top = [p for _, p in sorted(cand, key=lambda x: (-x[0], -(x[1]["cited"] or 0)))[:10]]
        out.append(f"\n## [{herb}] {q} (후보 {len(D)}편 중 질의어 일치 {len(cand)}편, 상위 {len(top)})\n")
        for p in top:
            ab = (p["abstract"] or "")[:350].replace("\n", " ")
            out.append(f"- {apa_auth(p['authors'])} ({p['year']}). {p['title']}. *{p['journal']}*. {p['doi'] or p['id']} · 인용 {p['cited']}\n  > {ab}")
            n += 1
    (R / "evidence" / f"{code}.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(code, c["title"][:30], "질의", len(bych.get(code, {})), "근거", n)

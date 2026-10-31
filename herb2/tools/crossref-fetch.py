# 실행: python crossref-fetch.py refdois-v1.txt crossref-meta-v1.jsonl  (표준 라이브러리만 사용, 인터넷 필요)
import sys, json, time, urllib.request, urllib.parse
src, dst = sys.argv[1], sys.argv[2]
dois = [l.strip() for l in open(src, encoding="utf-8") if l.strip()]
done = set()
try:
    done = {json.loads(l)["doi"] for l in open(dst, encoding="utf-8")}
except FileNotFoundError: pass
out = open(dst, "a", encoding="utf-8"); bad = 0
for i, d in enumerate(dois, 1):
    if d in done: continue
    url = "https://api.crossref.org/works/" + urllib.parse.quote(d) + "?mailto=sanbada136@gmail.com"
    try:
        m = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "herb2-check/1.0 (mailto:sanbada136@gmail.com)"}), timeout=30))["message"]
        rec = {"doi": d, "title": (m.get("title") or [""])[0], "journal": (m.get("container-title") or [""])[0], "volume": m.get("volume"), "issue": m.get("issue"), "page": m.get("page"), "article": m.get("article-number"), "year": ((m.get("issued") or {}).get("date-parts") or [[None]])[0][0], "authors": [(a.get("family") or a.get("name") or "", a.get("given") or "") for a in m.get("author", [])], "retracted": [r.get("type") for r in (m.get("update-to") or [])], "relation": list((m.get("relation") or {}).keys())}
        out.write(json.dumps(rec, ensure_ascii=False) + "\n"); out.flush()
    except Exception as e:
        bad += 1; print("실패", d, e)
    print(i, "/", len(dois), d, flush=True); time.sleep(0.3)
print("완료, 실패", bad)

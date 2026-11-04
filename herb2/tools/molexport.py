#!/usr/bin/env python3
"""molbook DB -> compact jsonl.gz (paper + chapter/herb/query tags). usage: molexport.py <dbdir>"""
import sqlite3, gzip, json, sys, os, hashlib

d = sys.argv[1]
db = sqlite3.connect(os.path.join(d, "molbook-db-v1.sqlite"))
tags = {}
for pid, ch, herb, q in db.execute(
    "select h.paper_id, qu.chapter, qu.herb, qu.q from hits h join queries qu on qu.qid=h.qid"
):
    tags.setdefault(pid, []).append([ch, herb, q])
os.makedirs(os.path.join(d, "export"), exist_ok=True)
out = os.path.join(d, "export", "molbook-papers-v1.jsonl.gz")
n = 0
with gzip.open(out, "wt", encoding="utf-8") as f:
    for r in db.execute("select id,doi,title,year,journal,authors,cited,abstract,is_retracted,type from papers"):
        o = dict(zip(["id", "doi", "title", "year", "journal", "authors", "cited", "abstract", "retracted", "type"], r))
        o["tags"] = tags.get(o["id"], [])
        f.write(json.dumps(o, ensure_ascii=False) + "\n")
        n += 1
h = hashlib.sha256(open(out, "rb").read()).hexdigest()
print("papers", n, "size", os.path.getsize(out), "sha256", h)

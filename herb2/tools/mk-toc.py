import re, sys, json, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
pdf = sys.argv[1]; out = sys.argv[2]
book = json.loads((ROOT/"book.json").read_text())
txt = subprocess.run(["pdftotext","-layout",pdf,"-"],capture_output=True,text=True).stdout.split("\f")
n = len(txt)-1 if txt[-1].strip()=="" else len(txt)
codes = [c for c in book["order"] if c.startswith(("ch","ap"))]
def rd(p): return p.read_text(encoding="utf-8")
titles = {}
for c in codes:
    m = re.search(r"^#\s+(.+)$", rd(ROOT/"chapters"/f"{c}.md"), re.M); titles[c] = m.group(1)
def norm(s): return re.sub(r"\s+","",s)
starts = {}; nxt = 1
for c in codes:
    t = norm(re.sub(r"^\d+장\.\s*","",titles[c]))[:10]
    for i in range(nxt, n+1):
        fl = next((l.strip() for l in txt[i-1].split("\n") if l.strip()), "")
        if t in norm(fl) and not fl.startswith("목"):
            starts[c] = i; nxt = i+1; break
    else: print("NOT FOUND", c); sys.exit(1)
ends = {}
for k,c in enumerate(codes):
    ends[c] = (starts[codes[k+1]] if k+1 < len(codes) else n+1)
res = {"n": n, "starts": starts, "len": {c: ends[c]-starts[c] for c in codes}, "sec": {}}
for c in codes:
    secs = re.findall(r"^##\s+(\d+\.\s+.+)$", rd(ROOT/"chapters"/f"{c}.md"), re.M)
    for s in secs:
        key = norm(s)[:14]
        for i in range(starts[c], ends[c]):
            if any(norm(l).startswith(key) for l in txt[i-1].split("\n")):
                res["sec"][f"{c}|{s}"] = i; break
Path(out).write_text(json.dumps(res, ensure_ascii=False, indent=1))
print(n, len(res["sec"]), "sections")

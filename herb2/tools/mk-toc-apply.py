import re, sys, json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
d = json.loads(Path(sys.argv[1]).read_text()); src = ROOT/"chapters"/sys.argv[2]; dst = ROOT/"chapters"/sys.argv[3]; pages = sys.argv[4]
codes = list(d["starts"]); secs = {}
for k,v in d["sec"].items():
    c,s = k.split("|",1); secs.setdefault(c,[]).append((s,v))
out=[]; ci=-1; si=0; miss=0
for ln in src.read_text(encoding="utf-8").splitlines():
    if ln.startswith("# 목차"): ln = f"# {dst.stem.replace('toc-','목차 ')} (컬러판 PDF, {d['n']}쪽 기준)"
    elif re.match(r"- \*\*.*\*\* … \d+쪽$", ln):
        ci += 1; si = 0; ln = re.sub(r"\d+쪽$", f"{d['starts'][codes[ci]]}쪽", ln)
    elif re.match(r"\s+- .* … \d+쪽$", ln):
        c = codes[ci]; lst = secs.get(c, [])
        if si < len(lst): ln = re.sub(r"\d+쪽$", f"{lst[si][1]}쪽", ln)
        else: miss += 1
        si += 1
    out.append(ln)
dst.write_text("\n".join(out)+"\n", encoding="utf-8")
# Table 0-2
p = ROOT/"chapters"/"ch00.md"; t = p.read_text(encoding="utf-8")
names = ["서장"]+[str(i) for i in range(1,15)]+["부록 A","부록 B","부록 C"]
for c,nm in zip(codes, names):
    t = re.sub(rf"^(\| {re.escape(nm)} \| [^|]+\| )\d+( \| )\d+( \|)", lambda m: f"{m.group(1)}{d['starts'][c]}{m.group(2)}{d['len'][c]}{m.group(3)}", t, flags=re.M)
t = t.replace("컬러판 PDF(v1) 기준", f"컬러판 PDF({pages}) 기준")
p.write_text(t, encoding="utf-8"); print("miss", miss)

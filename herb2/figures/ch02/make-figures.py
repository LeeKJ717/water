import csv, json, pathlib, re, collections
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib import font_manager
from PIL import Image

HERE = pathlib.Path(__file__).parent
DATA = HERE / "data"; DATA.mkdir(exist_ok=True)
CORPUS = HERE.parent.parent / "corpus" / "herbcorpus-rel-v1.jsonl"
for f in font_manager.findSystemFonts():
    if "NotoSansCJK" in f:
        font_manager.fontManager.addfont(f)
plt.rcParams.update({"font.family": "Noto Sans CJK KR", "axes.unicode_minus": False, "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, GREEN, RED, PURPLE, GRAY, GOLD = "#2b6cb0", "#dd6b20", "#2f855a", "#c53030", "#6b46c1", "#718096", "#b08a3e"


def save(fig, name):
    p = HERE / f"{name}.png"
    fig.savefig(p, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    Image.open(p).convert("L").save(HERE / f"{name}-bw.png")


def box(ax, x, y, w, h, text, fc, fs=8.5, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12", fc=fc, ec="#2d3748", lw=1))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, fontweight="bold" if bold else "normal")


def arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color="#2d3748", lw=1.2))


# ---- 그림 2-1 : 광합성에서 약 성분까지 (개념도) ----
def fig21():
    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    ax.set_xlim(0, 12); ax.set_ylim(0, 9.2); ax.axis("off")
    box(ax, 0.2, 3.4, 2.0, 1.4, "광합성\n(CO2 + 물 + 빛)\n→ 당", "#c6f6d5", bold=True)
    box(ax, 3.0, 3.4, 2.1, 1.4, "일차 대사\n아미노산\n아세틸-CoA", "#bee3f8", bold=True)
    paths = [("시키미산 경로", "#fefcbf", 6.6), ("메발론산·MEP 경로", "#fed7aa", 4.3), ("아미노산에서 직접", "#e9d8fd", 2.0), ("아세트산 경로", "#fed7d7", 0.0)]
    outs = [("페놀류\n(플라보노이드 등)", 6.6), ("테르페노이드\n(정유·사포닌 등)", 4.3), ("알칼로이드\n(질소 함유)", 2.0), ("폴리케타이드\n(안트라퀴논 등)", 0.0)]
    for (p, c, y), (o, _) in zip(paths, outs):
        yy = y + 0.1
        box(ax, 6.0, yy, 2.5, 1.3, p, c, fs=8)
        box(ax, 9.2, yy, 2.6, 1.3, o, "#edf2f7", fs=8, bold=True)
        arrow(ax, 5.1, 4.1, 6.0, yy + .65)
        arrow(ax, 8.5, yy + .65, 9.2, yy + .65)
    arrow(ax, 2.2, 4.1, 3.0, 4.1)
    ax.text(6, 8.8, "식물의 이차 대사: 당에서 약 성분까지", ha="center", fontsize=11, fontweight="bold")
    ax.text(6.0, 8.3 - 8.2, "", fontsize=1)
    save(fig, "그림2-1")


# ---- 그림 2-2 : 코퍼스에서 화합물 계열이 언급된 논문 수 ----
CLS = [("폴리페놀·페놀류", r"polyphenol|phenolic|phenolics"), ("플라보노이드", r"flavonoid"), ("테르펜·테르페노이드", r"terpen|terpenoid"),
       ("알칼로이드", r"alkaloid"), ("사포닌·배당체", r"saponin|glycoside|ginsenoside"), ("정유(에센셜 오일)", r"essential oil")]
def fig22():
    rows = [json.loads(l) for l in open(CORPUS, encoding="utf-8")]
    cnt = {}
    for name, pat in CLS:
        rx = re.compile(pat, re.I)
        cnt[name] = sum(1 for r in rows if rx.search((r["title"] or "") + " " + (r["abstract"] or "")))
    with open(DATA / "계열별논문수.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["class", "papers"]); [w.writerow([k, v]) for k, v in cnt.items()]
    order = sorted(cnt, key=lambda k: cnt[k])
    fig, ax = plt.subplots(figsize=(6.2, 3.3))
    hat = ["//" if i % 2 == 0 else "" for i in range(len(order))]
    bars = ax.barh(order, [cnt[k] for k in order], color=BLUE, hatch=hat, edgecolor="white")
    for b, k in zip(bars, order):
        ax.text(cnt[k] + 20, b.get_y() + b.get_height() / 2, f"{cnt[k]:,}", va="center", fontsize=9, fontweight="bold")
    ax.set_xlim(0, max(cnt.values()) * 1.15); ax.set_xlabel(f"제목·초록에 언급된 논문 수(편, 약초 관련 {len(rows):,}편 중)")
    save(fig, "그림2-2")
    return cnt


# ---- 그림 2-3 : 같은 식물의 성분이 달라지는 이유 (개념도) ----
def fig23():
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.set_xlim(0, 12); ax.set_ylim(0, 9.2); ax.axis("off")
    box(ax, 4.3, 3.2, 3.4, 1.6, "약용식물의\n이차 대사산물\n(함량·조성)", "#fefcbf", fs=9.5, bold=True)
    ext = [("빛", 0.3, 6.2), ("온도", 4.6, 6.6), ("토양 수분", 8.9, 6.2), ("토양 비옥도", 0.3, 0.6), ("염분", 4.6, 0.2), ("병해충·상처", 8.9, 0.6)]
    for t, x, y in ext:
        box(ax, x, y, 2.8, 1.2, t, "#bee3f8", fs=9)
        arrow(ax, x + 1.4, y + (0 if y > 4 else 1.2), 6.0, 4.0 + (0.8 if y > 4 else -0.8))
    box(ax, 0.0, 3.3, 2.8, 1.4, "유전형·계통", "#c6f6d5", fs=9)
    box(ax, 9.2, 3.3, 2.8, 1.4, "생장 단계\n(발달·부위)", "#c6f6d5", fs=9)
    arrow(ax, 2.8, 4.0, 4.3, 4.0); arrow(ax, 9.2, 4.0, 7.7, 4.0)
    ax.text(6, 8.8, "성분을 바꾸는 요인: 환경(파랑)과 내부 요인(초록)", ha="center", fontsize=10.5, fontweight="bold")
    save(fig, "그림2-3")


if __name__ == "__main__":
    fig21(); print(fig22()); fig23()

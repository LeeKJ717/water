import csv, json, pathlib, collections
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image

HERE = pathlib.Path(__file__).parent
DATA = HERE / "data"; DATA.mkdir(exist_ok=True)
CORPUS = HERE.parent.parent / "corpus" / "herbcorpus-rel-v1.jsonl"
for f in font_manager.findSystemFonts():
    if "NotoSansCJK" in f:
        font_manager.fontManager.addfont(f)
plt.rcParams.update({"font.family": "Noto Sans CJK KR", "axes.unicode_minus": False,
                     "font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, GREEN, RED, PURPLE, GRAY, GOLD = "#2b6cb0", "#dd6b20", "#2f855a", "#c53030", "#6b46c1", "#718096", "#b08a3e"


def save(fig, name):
    p = HERE / f"{name}.png"
    fig.savefig(p, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    Image.open(p).convert("L").save(HERE / f"{name}-bw.png")


rows = [json.loads(l) for l in open(CORPUS, encoding="utf-8")]

# ---------- 그림 0-1 : 풀에서 약까지 (개념도, 연표) ----------
def fig01():
    ev = [  # 연도, 식물, 성분, 약, 사람 (표 0-1과 같은 값)
        (1763, "버드나무 껍질", "살리신", "아스피린(1897)", "에드워드 스톤"),
        (1785, "디기탈리스", "디기톡신 등", "강심제", "윌리엄 위더링"),
        (1804, "양귀비", "모르핀", "진통제", "프리드리히 제르튀르너"),
        (1820, "기나나무 껍질", "퀴닌", "말라리아약", "펠르티에·카방투"),
        (1971, "태평양주목", "탁솔(파클리탁셀)", "항암제", "월·와니"),
        (1972, "개똥쑥", "아르테미시닌", "말라리아약", "도유유"),
    ]
    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    ax.set_xlim(0, 12); ax.set_ylim(0, 8); ax.axis("off")
    ax.plot([0.6, 11.4], [4, 4], color=GRAY, lw=2)
    cols = [BLUE, ORANGE, GREEN, RED, PURPLE, GOLD]
    mk = ["o", "s", "D", "^", "v", "P"]
    for i, (yr, pl, co, dr, who) in enumerate(ev):
        x = 1.2 + i * 1.92
        up = i % 2 == 0
        ax.plot([x], [4], marker=mk[i], ms=11, color=cols[i], mec="black", zorder=3)
        yb = 5.0 if up else 3.0
        ax.plot([x, x], [4, yb + (0.0 if up else 0.0)], color=GRAY, lw=1)
        ty = 5.15 if up else 2.85
        va = "bottom" if up else "top"
        ax.text(x, ty, f"{yr}", ha="center", va=va, fontsize=11, fontweight="bold", color=cols[i])
        lines = [pl, "→ " + co, "→ " + dr]
        yy = ty + (0.55 if up else -0.55)
        for k, s in enumerate(lines):
            ax.text(x, yy + (k * 0.62 if up else -k * 0.62), s, ha="center", va=va, fontsize=8.5)
    ax.text(6, 7.7, "식물 한 포기에서 약 한 알까지: 여섯 번의 전환점", ha="center", fontsize=11, fontweight="bold")
    ax.text(6, 0.25, "개념도(연표). 연도와 인물은 표 0-1과 같다.", ha="center", fontsize=8.5, color=GRAY)
    save(fig, "그림0-1")


# ---------- 그림 0-2 : 5년 단위 논문 수 (코퍼스) ----------
def fig02():
    c = collections.Counter()
    for r in rows:
        y = r["year"]
        if y and 1995 <= y <= 2026:
            c[(y // 5) * 5] += 1
    keys = sorted(c)
    labels = [f"{k}–{k+4}" if k < 2025 else "2025–26" for k in keys]
    vals = [c[k] for k in keys]
    with open(DATA / "논문수-5년단위.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["period", "papers"]); w.writerows(zip(labels, vals))
    fig, ax = plt.subplots(figsize=(6.2, 3.3))
    hat = ["", "//", "", "//", "", "//", "", "//"][:len(vals)]
    bars = ax.bar(labels, vals, color=[BLUE] * len(vals), hatch=hat, edgecolor="white")
    bars[-1].set_alpha(0.55)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + max(vals) * 0.015, f"{v:,}", ha="center", fontsize=9, fontweight="bold")
    ax.set_ylabel("논문 수(편)"); ax.set_xlabel("출판 연도(5년 단위)")
    ax.set_ylim(0, max(vals) * 1.12)
    ax.yaxis.grid(True, color="#e2e8f0"); ax.set_axisbelow(True)
    save(fig, "그림0-2")
    return dict(zip(labels, vals))


# ---------- 그림 0-3 : 지역별 논문 수 ----------
REG = {"global": "세계 공통 주제", "east-asia": "동아시아", "south-asia": "남아시아", "middle-east": "중동",
       "africa": "아프리카", "europe": "유럽", "americas": "아메리카", "oceania": "오세아니아"}


def region_counts():
    s = collections.defaultdict(set)
    for r in rows:
        for t in set((r["tags"] or "").split(",")):
            s[t.split("/")[0]].add(r["id"])
    return {k: len(v) for k, v in s.items()}


def fig03():
    rc = region_counts()
    order = sorted(rc, key=lambda k: rc[k])
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    cols = [GRAY if k == "global" else BLUE for k in order]
    hat = ["xx" if k == "global" else "" for k in order]
    bars = ax.barh([REG[k] for k in order], [rc[k] for k in order], color=cols, hatch=hat, edgecolor="white")
    for b, k in zip(bars, order):
        ax.text(rc[k] + 25, b.get_y() + b.get_height() / 2, f"{rc[k]:,}", va="center", fontsize=9, fontweight="bold")
    ax.set_xlim(0, max(rc.values()) * 1.15); ax.set_xlabel("논문 수(편, 약초 관련 초록 확인분)")
    with open(DATA / "지역별논문수.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["region", "papers"]); [w.writerow([REG[k], rc[k]]) for k in order[::-1]]
    save(fig, "그림0-3")
    return rc


if __name__ == "__main__":
    fig01(); print(fig02()); print(fig03()); print(len(rows))

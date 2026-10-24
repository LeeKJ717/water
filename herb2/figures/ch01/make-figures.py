import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib import font_manager
from PIL import Image

HERE = pathlib.Path(__file__).parent
DATA = HERE / "data"; DATA.mkdir(exist_ok=True)
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


# ---- 그림 1-1 : 증거의 시간 사다리 (현재로부터 거슬러 올라간 햇수, 로그 눈금) ----
EVID = [  # 이름, 중심(년 전), 하한, 상한, 증거 종류
    ("네안데르탈인 치석\n(엘시드론 동굴)", 46000, 42000, 50000, "화학·DNA 분석"),
    ("얼음인간 뢰치\n(알프스 빙하)", 5300, 5300, 5300, "유해와 소지품"),
    ("수메르 점토판", 5000, 5000, 5000, "문자 기록"),
    ("에버스 파피루스\n(이집트)", 3576, 3576, 3576, "문자 기록"),
    ("테오프라스토스\n(그리스)", 2300, 2300, 2300, "문자 기록"),
    ("디오스코리데스\n(로마 제국)", 1960, 1960, 1960, "문자 기록"),
]
def fig11():
    with open(DATA / "증거연대.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["evidence", "years_before_present", "low", "high", "kind"])
        for n, c, lo, hi, k in EVID: w.writerow([n.replace("\n", " "), c, lo, hi, k])
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    kinds = {"화학·DNA 분석": (BLUE, "o"), "유해와 소지품": (GREEN, "s"), "문자 기록": (ORANGE, "D")}
    for i, (n, c, lo, hi, k) in enumerate(EVID):
        col, mk = kinds[k]
        if hi > lo:
            ax.plot([lo, hi], [0, 0], color=col, lw=6, solid_capstyle="butt", alpha=.85)
        ax.plot([c], [0], marker=mk, ms=9, color=col, mec="black", zorder=3)
        cfg = {0: (1.0, "center", 1), 1: (2.9, "center", 1), 2: (-.35, "center", -1), 3: (1.9, "left", 1), 4: (1.0, "center", 1), 5: (-.35, "center", -1)}[i]
        y, ha, sg = cfg
        ax.plot([c, c], [0, y - .05 * sg], color=GRAY, lw=.8)
        ax.text(c, y, n, ha=ha, va="bottom" if sg > 0 else "top", fontsize=8)
    for k, (col, mk) in kinds.items():
        ax.plot([], [], marker=mk, ls="", color=col, mec="black", label=k)
    ax.axhline(0, color=GRAY, lw=1.2)
    ax.set_xscale("log"); ax.set_xlim(1000, 80000); ax.invert_xaxis()
    ax.set_ylim(-1.5, 3.9); ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xticks([50000, 20000, 10000, 5000, 2000, 1000])
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{int(v):,}"))
    ax.minorticks_off()
    ax.set_xlabel("지금부터 거슬러 올라간 햇수(년 전, 로그 눈금)")
    ax.legend(loc="upper left", fontsize=8, frameon=False, ncol=1, bbox_to_anchor=(0.0, 1.0))
    save(fig, "그림1-1")


# ---- 그림 1-2 : 고대 문헌이 담은 식물·약재의 규모 ----
DOCS = [  # 문헌, 수, 이상여부, 출처설명
    ("수메르 점토판(약 5000년 전)", 250, True),
    ("에버스 파피루스(기원전 1550년경)", 700, False),
    ("신농본초경 전승(기원전 2500년경 전승)", 365, False),
    ("히포크라테스 전집(기원전 459–370)", 300, False),
    ("테오프라스토스(기원전 371–287)", 500, True),
    ("디오스코리데스(기원후 77년경)", 657, False),
    ("이븐 바이타르(13세기)", 1000, True),
]
def fig12():
    with open(DATA / "고대문헌규모.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["document", "count", "or_more"]); w.writerows(DOCS)
    fig, ax = plt.subplots(figsize=(6.4, 3.5))
    names = [d[0] for d in DOCS][::-1]; vals = [d[1] for d in DOCS][::-1]; more = [d[2] for d in DOCS][::-1]
    cols = [ORANGE if m else BLUE for m in more]
    hat = ["//" if m else "" for m in more]
    bars = ax.barh(names, vals, color=cols, hatch=hat, edgecolor="white")
    for b, v, m in zip(bars, vals, more):
        ax.text(v + 15, b.get_y() + b.get_height() / 2, f"{v:,}{'+' if m else ''}", va="center", fontsize=9, fontweight="bold")
    ax.set_xlim(0, 1200); ax.set_xlabel("수록된 식물·약재의 수(종류)")
    ax.xaxis.grid(True, color="#e2e8f0"); ax.set_axisbelow(True)
    ax.barh([], [], color=BLUE, label="기록된 수"); 
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(facecolor=BLUE, label="문헌이 말하는 수"), Patch(facecolor=ORANGE, hatch="//", edgecolor="white", label="'이상'으로 적힌 수")],
              loc="upper right", fontsize=8, frameon=False)
    save(fig, "그림1-3")


# ---- 그림 1-3 : 치석에서 식물을 읽는 방법 (개념도) ----
def box(ax, x, y, w, h, text, fc, fs=8.5, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12", fc=fc, ec="#2d3748", lw=1))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, fontweight="bold" if bold else "normal")

def arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color="#2d3748", lw=1.2))

def fig13():
    fig, ax = plt.subplots(figsize=(6.6, 3.8))
    ax.set_xlim(0, 12); ax.set_ylim(0, 7); ax.axis("off")
    box(ax, .1, 3.0, 2.3, 1.2, "치석 채취\n(이빨에 굳은\n플라크)", "#edf2f7", bold=True)
    box(ax, 3.2, 5.0, 2.7, 1.3, "① 현미경\n녹말 알갱이 모양", "#bee3f8")
    box(ax, 3.2, 2.9, 2.7, 1.3, "② 화학 분석\n열분해 GC-MS\n분자 표지 찾기", "#c6f6d5")
    box(ax, 3.2, 0.8, 2.7, 1.3, "③ 고대 DNA\n염기서열 읽기\n(2017 연구)", "#fed7aa")
    box(ax, 7.0, 3.0, 2.3, 1.2, "식물 후보\n목록", "#fefcbf", bold=True)
    box(ax, 10.0, 3.9, 1.9, 1.5, "먹었다\n(검출)", "#e2e8f0")
    box(ax, 10.0, 1.6, 1.9, 1.5, "약으로 썼다?\n(해석)", "#fed7d7")
    arrow(ax, 2.2, 3.7, 3.2, 5.6); arrow(ax, 2.2, 3.6, 3.2, 3.55); arrow(ax, 2.2, 3.4, 3.2, 1.5)
    arrow(ax, 5.9, 5.6, 7.0, 3.9); arrow(ax, 5.9, 3.55, 7.0, 3.6); arrow(ax, 5.9, 1.5, 7.0, 3.3)
    arrow(ax, 9.3, 3.8, 10.0, 4.5); arrow(ax, 9.3, 3.4, 10.0, 2.5)
    ax.text(11.0, 0.7, "여기서부터는\n증거가 아니라 추론", ha="center", fontsize=8, color=RED, fontweight="bold")
    ax.text(6, 6.75, "치석에서 식물을 읽는 세 갈래 길", ha="center", fontsize=11, fontweight="bold")
    save(fig, "그림1-2")


if __name__ == "__main__":
    fig11(); fig12(); fig13(); print("ok")

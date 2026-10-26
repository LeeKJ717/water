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
BLUE, ORANGE, GREEN, RED, GRAY = "#2b6cb0", "#dd6b20", "#2f855a", "#c53030", "#718096"

def save(fig, name):
    p = HERE / f"{name}.png"
    fig.savefig(p, dpi=300, bbox_inches="tight", facecolor="white"); plt.close(fig)
    Image.open(p).convert("L").save(HERE / f"{name}-bw.png")

def box(ax, x, y, w, h, text, fc, fs=8, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12", fc=fc, ec="#2d3748", lw=1))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, fontweight="bold" if bold else "normal")

def arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color="#2d3748", lw=1.2))

def wcsv(name, header, rows):
    with open(DATA / name, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)

def rows():
    return [json.loads(l) for l in open(CORPUS, encoding="utf-8")]


# 그림 5-1: 지식의 이동 (개념도)
def fig51():
    fig, ax = plt.subplots(figsize=(6.8, 3.4)); ax.set_xlim(0, 14); ax.set_ylim(0, 7.5); ax.axis("off")
    box(ax, .2, 2.9, 3.0, 1.8, "그리스·로마의\n약물학과 의학", "#bee3f8", 8.5, True)
    box(ax, 4.6, 2.9, 3.4, 1.8, "아랍·페르시아 의학\n(번역·집대성)\n이븐 시나 등", "#fefcbf", 8.5, True)
    box(ax, 9.6, 4.9, 4.0, 1.5, "유럽의 약초학(6장)", "#c6f6d5", 8.5)
    box(ax, 9.6, 1.2, 4.0, 1.5, "남아시아의 유나니(4장)", "#fed7aa", 8.5)
    arrow(ax, 3.2, 3.8, 4.6, 3.8); arrow(ax, 8.0, 4.2, 9.6, 5.6); arrow(ax, 8.0, 3.4, 9.6, 2.0)
    ax.text(7, 7.1, "중동은 약초 지식이 지나간 다리였다(개념도)", ha="center", fontsize=10.5, fontweight="bold")
    save(fig, "그림5-1")

# 그림 5-2: 의학정전 속 약초를 현대 연구로 대조
def fig52():
    wcsv("정전대조.csv", ["item", "value"], [("간 보호 후보 식물(종)", 18), ("현대 연구에서 간 보호 보고(%)", 85), ("보고 없음(%)", 15), ("심장 약초(종)", 50), ("효과가 더 확인된 식물(종)", 7)])
    fig, axs = plt.subplots(1, 2, figsize=(6.8, 2.9), gridspec_kw={"width_ratios": [1.1, 1]})
    ax = axs[0]
    ax.barh([0], [85], color=GREEN, edgecolor="white"); ax.barh([0], [15], left=[85], color=GRAY, edgecolor="white")
    ax.text(42, 0, "85%\n근거 있음", ha="center", va="center", color="white", fontweight="bold", fontsize=9)
    ax.text(92.5, 0, "15%", ha="center", va="center", color="white", fontweight="bold", fontsize=8)
    ax.set_xlim(0, 100); ax.set_yticks([]); ax.set_xlabel("%"); ax.spines["left"].set_visible(False)
    ax.set_title("『의학정전』의 간 보호 식물 18종\n현대 연구 대조", fontsize=8.5)
    ax = axs[1]
    ax.bar(["이븐 시나가\n꼽은 심장 약초", "그중 효과가\n더 확인된 식물"], [50, 7], color=[BLUE, ORANGE], hatch=["", "xx"], edgecolor="white", width=.55)
    for i, v in enumerate([50, 7]): ax.text(i, v + 1.5, f"{v}종", ha="center", fontweight="bold")
    ax.set_ylim(0, 60); ax.set_ylabel("식물 수(종)"); ax.set_title("심장 질환 약초 50종의 현대 검증", fontsize=8.5)
    fig.tight_layout(); save(fig, "그림5-2")

# 그림 5-3: 사프란 시험 설계
def fig53():
    fig, ax = plt.subplots(figsize=(6.8, 3.3)); ax.set_xlim(0, 14); ax.set_ylim(0, 7); ax.axis("off")
    box(ax, .2, 2.6, 3.0, 1.8, "경증~중등도\n우울증 외래 환자\n40명(해밀턴 우울\n척도 18점 이상)", "#edf2f7", 7.8, True)
    box(ax, 4.6, 4.2, 3.4, 1.6, "사프란 암술머리\n하루 30 mg 캡슐", "#fefcbf", 8)
    box(ax, 4.6, 1.2, 3.4, 1.6, "위약 캡슐", "#e2e8f0", 8)
    arrow(ax, 3.2, 3.8, 4.6, 5.0); arrow(ax, 3.2, 3.2, 4.6, 2.0)
    arrow(ax, 8.0, 5.0, 9.2, 3.9); arrow(ax, 8.0, 2.0, 9.2, 3.1)
    box(ax, 9.2, 2.5, 4.6, 2.0, "6주 후 해밀턴 우울 척도\n사프란군이 위약군보다\n유의하게 더 좋음\n(P < 0.001), 부작용 차이 없음", "#c6f6d5", 7.8)
    ax.text(7, 6.6, "사프란 이중맹검 시험의 설계", ha="center", fontsize=10.5, fontweight="bold")
    save(fig, "그림5-3")

# 그림 5-4: 세 시험의 규모
def fig54():
    trials = [("사프란·우울증\n(Akhondzadeh 2005)", [("사프란+위약\n합계", 40)], "6주"), ("호두잎·당뇨\n(Hosseini 2014)", [("호두잎", 30), ("위약", 28)], "2개월"),
              ("다약초 처방·COVID-19\n(Karimi 2021)", [("처방+표준 치료", 184), ("표준 치료", 174)], "7일")]
    wcsv("세시험규모.csv", ["trial", "group", "n", "duration"], [(t.replace("\n", " "), g.replace("\n", " "), n, d) for t, gs, d in trials for g, n in gs])
    fig, ax = plt.subplots(figsize=(6.6, 3.1))
    ypos = [2, 1, 0]; cols = [BLUE, GREEN, ORANGE]
    for (t, gs, d), y in zip(trials, ypos):
        left = 0
        for k, (g, n) in enumerate(gs):
            ax.barh(y, n, left=left, color=cols[y] if k == 0 else "#a0aec0", hatch="" if k == 0 else "//", edgecolor="white", height=.55)
            ax.text(left + n / 2, y, f"{g.replace(chr(10), ' ')} {n}명" if n > 100 else f"{n}명", ha="center", va="center", color="white" if (n > 100 and k == 0) else "black", fontsize=8, fontweight="bold")
            left += n
        ax.text(left + 6, y, f"합계 {left}명 · {d}", va="center", fontsize=8)
    ax.set_yticks(ypos); ax.set_yticklabels([t for t, _, _ in trials], fontsize=8)
    ax.set_xlim(0, 520); ax.set_xlabel("참가자 수(명)")
    save(fig, "그림5-4")

# 그림 5-5: 연도별
def fig55():
    me = [r for r in rows() if "middle-east" in (r["tags"] or "")]
    by = collections.Counter(r["year"] for r in me)
    yrs = list(range(2000, 2023)); vals = [by.get(y, 0) for y in yrs]
    wcsv("중동연도별논문수.csv", ["year", "papers"], zip(yrs, vals))
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    ax.bar([str(y) for y in yrs], vals, color=BLUE, width=.7)
    ax.set_xticks(range(0, len(yrs), 2)); ax.set_xticklabels([str(y) for y in yrs[::2]])
    ax.set_ylabel("논문 수(편)"); ax.yaxis.grid(True, color="#e2e8f0"); ax.set_axisbelow(True)
    save(fig, "그림5-5"); return len(me)

# 그림 5-6: 주제어
TOP = [("사프란", r"saffron|crocus"), ("당뇨", r"diabet"), ("임상시험", r"clinical trial|randomi[sz]ed"), ("페르시아 의학", r"persian medicine|iranian medicine"),
       ("니겔라(검은깨풀)", r"nigella"), ("이븐 시나", r"avicenna|ibn sina|canon"), ("민족식물학", r"ethnobotan"), ("장미(다마스크)", r"rosa damascena|damask")]
def fig56():
    me = [r for r in rows() if "middle-east" in (r["tags"] or "")]
    cnt = {n: sum(1 for r in me if re.search(p, (r["title"] or "") + " " + (r["abstract"] or ""), re.I)) for n, p in TOP}
    wcsv("중동주제별논문수.csv", ["topic", "papers"], cnt.items())
    order = sorted(cnt, key=lambda k: cnt[k])
    fig, ax = plt.subplots(figsize=(6.2, 3.3))
    b = ax.barh(order, [cnt[k] for k in order], color=BLUE, hatch=["//" if i % 2 == 0 else "" for i in range(len(order))], edgecolor="white")
    for r, k in zip(b, order): ax.text(cnt[k] + 4, r.get_y() + r.get_height() / 2, f"{cnt[k]:,}", va="center", fontsize=9, fontweight="bold")
    ax.set_xlim(0, max(cnt.values()) * 1.15); ax.set_xlabel(f"제목·초록에 언급된 논문 수(편, 중동 약초 논문 {len(me):,}편 중)")
    save(fig, "그림5-6"); return cnt, len(me)

if __name__ == "__main__":
    fig51(); fig52(); fig53(); fig54(); print(fig55()); print(fig56())

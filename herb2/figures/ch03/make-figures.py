import csv, json, pathlib, re, collections
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Patch
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


# ---- 그림 3-1 : 동아시아 약초 문헌과 제도의 연표 ----
EV = [  # 연도, 이름, 층(위/아래 높이), 종류
    (120, "신농본초경\n(후한, 365종)", 1.0, "중국"),
    (659, "신수본초\n(당, 850종)", 2.2, "중국"),
    (1596, "본초강목\n(명, 1,892종)", 1.0, "중국"),
    (1613, "동의보감\n(조선, 25권)", -1.0, "한국"),
    (1724, "동의보감 일본판", -2.3, "일본"),
    (1868, "메이지 유신\n(서양 의학만 허용)", 2.2, "일본"),
    (1971, "개똥쑥에서\n아르테미시닌 분리", -1.0, "중국"),
    (2009, "동의보감\n유네스코 기록유산", 1.0, "한국"),
]
def fig31():
    with open(DATA / "연표.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["year", "event", "country"]); [w.writerow([y, n.replace("\n", " "), c]) for y, n, _, c in EV]
    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    col = {"중국": BLUE, "한국": GREEN, "일본": ORANGE}; mk = {"중국": "o", "한국": "s", "일본": "D"}
    lane = {"중국": 2, "한국": 1, "일본": 0}
    for c, y in lane.items():
        ax.axhline(y, color="#cbd5e0", lw=1.2, zorder=0)
    cnt = collections.Counter()
    for y, n, h, c in EV:
        k = cnt[c]; cnt[c] += 1
        up = (k % 2 == 0)
        ax.plot([y], [lane[c]], marker=mk[c], ms=9, color=col[c], mec="black", zorder=3)
        ax.text(y, lane[c] + (.16 if up else -.16), f"{y}\n{n}", ha="center", va="bottom" if up else "top", fontsize=7.2)
    ax.set_yticks([2, 1, 0]); ax.set_yticklabels(["중국", "한국", "일본"])
    ax.set_ylim(-.9, 2.9); ax.set_xlim(-100, 2250); ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
    ax.set_xlabel("서기 연도"); save(fig, "그림3-1")


# ---- 그림 3-2 : 본초서의 수록 약물 수 ----
def fig32():
    names = ["신농본초경\n(후한)", "신수본초\n(659)", "본초강목\n(1596)"]; vals = [365, 850, 1892]
    with open(DATA / "본초서규모.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["book", "entries"]); [w.writerow([n.replace("\n", " "), v]) for n, v in zip(names, vals)]
    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    bars = ax.bar(names, vals, color=[BLUE, ORANGE, GREEN], hatch=["", "//", "xx"], edgecolor="white", width=.55)
    for b, v in zip(bars, vals): ax.text(b.get_x() + b.get_width() / 2, v + 30, f"{v:,}", ha="center", fontweight="bold")
    ax.set_ylabel("수록 약물 수(가지)"); ax.set_ylim(0, 2200); ax.yaxis.grid(True, color="#e2e8f0"); ax.set_axisbelow(True)
    save(fig, "그림3-2")


# ---- 그림 3-3 : 개똥쑥에서 약이 되기까지 ----
def fig33():
    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    ax.set_xlim(0, 14); ax.set_ylim(0, 6); ax.axis("off")
    steps = [("4세기\n갈홍의 처방\n(찬물에 담가\n짜낸 즙)", "#bee3f8"), ("11세기 이후\n두 종(황화호·\n청호) 구별 논의", "#c6f6d5"),
             ("1971년\n잎에서 유효\n물질 분리", "#fefcbf"), ("분자 구조\n과산화 결합의\n세스퀴테르펜\n락톤", "#fed7aa"),
             ("1980년대\n유도체와\n임상시험", "#fed7d7")]
    for i, (t, c) in enumerate(steps):
        x = .2 + i * 2.75
        box(ax, x, 1.4, 2.35, 2.6, t, c, fs=7)
        if i: arrow(ax, x - .38, 2.7, x - .02, 2.7)
    ax.text(7, 5.3, "전통 기록에서 새로운 약 분자까지", ha="center", fontsize=11, fontweight="bold")
    ax.text(7, .6, "출처: Hsü(2006), Klayman(1985)", ha="center", fontsize=8, color=GRAY)
    save(fig, "그림3-3")


# ---- 그림 3-4 : 일본의 캄포 사용 현황 ----
def fig34():
    fig, axs = plt.subplots(1, 2, figsize=(6.8, 3.2), gridspec_kw={"width_ratios": [1, 1.2]})
    ax = axs[0]
    labels = ["캄포 처방을\n받은 환자", "그중 양약과\n함께 받은 환자"]; vals = [1.34, 92.2]
    ax.bar(["전체 환자 중\n캄포 처방 비율", "캄포 환자 중\n양약 병용 비율"], vals, color=[BLUE, ORANGE], hatch=["", "//"], edgecolor="white", width=.6)
    for i, v in enumerate(vals): ax.text(i, v + 2, f"{v}%", ha="center", fontweight="bold")
    ax.set_ylim(0, 105); ax.set_ylabel("%"); ax.set_title("건강보험 청구 6,711만 건(2009)", fontsize=8.5)
    ax = axs[1]
    labs = ["1회 이상", "4회 이상", "8회 이상", "16회 이상"]; v2 = [98, 84, 44, 5]
    b = ax.bar(labs, v2, color=GREEN, hatch="xx", edgecolor="white", width=.6)
    for r, v in zip(b, v2): ax.text(r.get_x() + r.get_width() / 2, v + 2, f"{v}%", ha="center", fontweight="bold")
    ax.set_ylim(0, 105); ax.set_title("캄포 수업을 개설한 의대 비율(80개교)", fontsize=8.5); ax.set_xlabel("6년 과정 중 수업 횟수")
    with open(DATA / "캄포사용.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["item", "value_percent"]); w.writerow(["환자 중 캄포 처방", 1.34]); w.writerow(["캄포 환자 중 양약 병용", 92.2])
        for l, v in zip(labs, v2): w.writerow(["의대 캄포 수업 " + l, v])
    fig.tight_layout(); save(fig, "그림3-4")


# ---- 그림 3-5 : 갈근금련탕 임상시험 설계 ----
def fig35():
    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    ax.set_xlim(0, 14); ax.set_ylim(0, 7.5); ax.axis("off")
    box(ax, 0.2, 2.9, 2.6, 1.5, "제2형 당뇨병 환자\n187명\n(무작위 배정)", "#edf2f7", fs=8.5, bold=True)
    groups = [("고용량 갈근금련탕\n44명", "#bee3f8", 5.6), ("중간 용량\n52명", "#c6f6d5", 4.0), ("저용량\n50명", "#fefcbf", 2.4), ("위약\n41명", "#fed7d7", .8)]
    for t, c, y in groups:
        box(ax, 4.3, y, 3.0, 1.3, t, c, fs=8)
        arrow(ax, 2.8, 3.65, 4.3, y + .65)
        arrow(ax, 7.3, y + .65, 8.0, y + .65)
    box(ax, 8.0, 3.6, 5.8, 3.3, "12주 후\n· 공복 혈당, 당화혈색소: 고용량·중간 용량군이\n   위약군·저용량군보다 유의하게 감소\n· 장내 세균 조성이 용량에 비례해 변화\n  (증상 호전 이전에 먼저 변화)", "#edf2f7", fs=7.8)
    box(ax, 8.0, .8, 5.8, 2.4, "16S rRNA 유전자 V3 영역\n파이로시퀀싱\n→ 갈근금련탕에 늘어난 47개 계통형\n→ Faecalibacterium prausnitzii 증가", "#e9d8fd", fs=7.8)
    ax.text(7, 7.2, "갈근금련탕 이중맹검 임상시험의 설계", ha="center", fontsize=10.5, fontweight="bold")
    with open(DATA / "갈근금련탕군.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["group", "n"]); [w.writerow(r) for r in [("고용량", 44), ("중간 용량", 52), ("저용량", 50), ("위약", 41)]]
    save(fig, "그림3-5")


# ---- 그림 3-6 : 대건중탕 후향 연구 결과 ----
def fig36():
    fig, axs = plt.subplots(1, 3, figsize=(6.8, 3.0))
    spec = [("장관 감압 성공률(%)", (84.7, 78.5), "P = 0.224\n(차이 없음)", (0, 100)),
            ("감압 기간(일)", (8, 10), "P = 0.012", (0, 12)),
            ("입원 비용(달러)", (23086, 26950), "P = 0.018", (0, 30000))]
    for ax, (t, v, p, lim) in zip(axs, spec):
        b = ax.bar(["사용군", "미사용군"], v, color=[BLUE, GRAY], hatch=["", "//"], edgecolor="white", width=.6)
        for r, x in zip(b, v): ax.text(r.get_x() + r.get_width() / 2, x + lim[1] * .02, f"{x:,}", ha="center", fontsize=8, fontweight="bold")
        ax.set_title(t + "\n" + p.replace("\n", " "), fontsize=8); ax.set_ylim(*lim); ax.set_ylim(0, lim[1] * 1.12)
    with open(DATA / "대건중탕.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["outcome", "users", "nonusers", "p"])
        w.writerow(["LTD success %", 84.7, 78.5, 0.224]); w.writerow(["LTD days", 8, 10, 0.012]); w.writerow(["hospital charges USD", 23086, 26950, 0.018])
    fig.tight_layout(); save(fig, "그림3-6")


# ---- 그림 3-7 : 동아시아 논문의 주제 ----
TOP = [("인삼(ginseng)", r"ginseng|panax|ginsenoside"), ("네트워크 약리학", r"network pharmacology"), ("탕·처방(decoction·formula)", r"decoction|formula"),
       ("아르테미시닌", r"artemisinin|qinghaosu|artemisia annua"), ("캄포", r"kampo"), ("감초(licorice)", r"licorice|liquorice|glycyrrhiz")]
def fig37():
    rows = [json.loads(l) for l in open(CORPUS, encoding="utf-8")]
    ea = [r for r in rows if "east-asia" in (r["tags"] or "")]
    cnt = {}
    for n, pat in TOP:
        rx = re.compile(pat, re.I)
        cnt[n] = sum(1 for r in ea if rx.search((r["title"] or "") + " " + (r["abstract"] or "")))
    with open(DATA / "동아시아주제별논문수.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["topic", "papers"]); [w.writerow(kv) for kv in cnt.items()]
    order = sorted(cnt, key=lambda k: cnt[k])
    fig, ax = plt.subplots(figsize=(6.2, 3.3))
    b = ax.barh(order, [cnt[k] for k in order], color=BLUE, hatch=["//" if i % 2 == 0 else "" for i in range(len(order))], edgecolor="white")
    for r, k in zip(b, order): ax.text(cnt[k] + 8, r.get_y() + r.get_height() / 2, f"{cnt[k]:,}", va="center", fontsize=9, fontweight="bold")
    ax.set_xlim(0, max(cnt.values()) * 1.15); ax.set_xlabel(f"제목·초록에 언급된 논문 수(편, 동아시아 약초 논문 {len(ea):,}편 중)")
    save(fig, "그림3-7"); return cnt, len(ea)


if __name__ == "__main__":
    fig31(); fig32(); fig33(); fig34(); fig35(); fig36(); print(fig37())

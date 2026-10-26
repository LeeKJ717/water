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


# 그림 4-1: 사건 순서(간격은 연도에 비례하지 않음)
EV = [("기원전 1500년경", "아유르베다의\n기원으로 인용", 2, "전통"), ("1931", "인도 학술지에서\n라우볼피아 연구", 1, "연구"),
      ("1949", "바킬의 임상 보고\n(영국 심장학회지)", 1, "연구"), ("1957", "바킬, 래스커\n임상의학연구상", 1, "연구"),
      ("2008", "인터넷 판매 제품\n중금속 조사", 0, "안전"), ("2008 ", "체질(프라크리티)의\n유전자 발현 연구", 1, "연구"),
      ("2015", "아슈와간다\n무작위 대조 시험", 1, "연구"), ("2018", "IMPPAT\n데이터베이스", 2, "자료")]
def fig41():
    wcsv("연표.csv", ["when", "event", "lane"], [(a, b.replace("\n", " "), d) for a, b, c, d in EV])
    fig, ax = plt.subplots(figsize=(6.8, 3.7))
    names = {2: "전통·자료", 1: "연구", 0: "품질·안전"}
    col = {"전통": BLUE, "연구": GREEN, "안전": RED, "자료": ORANGE}
    for y in names: ax.axhline(y, color="#cbd5e0", lw=1.2, zorder=0)
    for i, (when, txt, lane, kind) in enumerate(EV):
        ax.plot([i], [lane], marker="o", ms=9, color=col[kind], mec="black", zorder=3)
        up = (i % 2 == 0)
        ax.text(i, lane + (.14 if up else -.14), f"{when.strip()}\n{txt}", ha="center", va="bottom" if up else "top", fontsize=6.8)
    ax.set_yticks(list(names)); ax.set_yticklabels(list(names.values())); ax.tick_params(axis="y", length=0)
    ax.set_ylim(-.9, 2.9); ax.set_xlim(-.7, len(EV) - .3); ax.set_xticks([]); ax.spines["left"].set_visible(False)
    ax.set_xlabel("사건 순서(가로 간격은 실제 연대에 비례하지 않음)"); save(fig, "그림4-1")


# 그림 4-2: 연도별 논문 수
def rows():
    return [json.loads(l) for l in open(CORPUS, encoding="utf-8")]
def fig42():
    sa = [r for r in rows() if "south-asia" in (r["tags"] or "")]
    by = collections.Counter(r["year"] for r in sa)
    yrs = list(range(2000, 2023)); vals = [by.get(y, 0) for y in yrs]
    wcsv("남아시아연도별논문수.csv", ["year", "papers"], zip(yrs, vals))
    fig, ax = plt.subplots(figsize=(6.4, 3.1))
    ax.bar([str(y) for y in yrs], vals, color=BLUE, width=.7)
    ax.set_xticks(range(0, len(yrs), 2)); ax.set_xticklabels([str(y) for y in yrs[::2]])
    ax.set_ylabel("논문 수(편)"); ax.yaxis.grid(True, color="#e2e8f0"); ax.set_axisbelow(True)
    save(fig, "그림4-2"); return len(sa)


# 그림 4-3: 체질과 처방의 개념도
def fig43():
    fig, ax = plt.subplots(figsize=(6.8, 3.4)); ax.set_xlim(0, 14); ax.set_ylim(0, 7.5); ax.axis("off")
    box(ax, .2, 2.9, 3.0, 1.7, "개인의 체질\n(프라크리티, Prakriti)\n일곱 가지 유형", "#edf2f7", 8, True)
    for t, c, y in [("바타(Vata)", "#bee3f8", 5.4), ("피타(Pitta)", "#fed7aa", 3.3), ("카파(Kapha)", "#c6f6d5", 1.2)]:
        box(ax, 5.0, y, 2.9, 1.3, t, c, 8.5); arrow(ax, 3.2, 3.75, 5.0, y + .65); arrow(ax, 7.9, y + .65, 9.2, 3.75)
    box(ax, 9.2, 2.7, 4.6, 2.1, "체질에 맞춘 처방과 생활 지침\n여러 약초를 섞은 다약초 처방\n회춘 약초군(라사야나)", "#e9d8fd", 8, True)
    ax.text(7, 7.1, "아유르베다에서 체질과 처방이 이어지는 구조(개념도)", ha="center", fontsize=10, fontweight="bold")
    ax.text(5.0, .3, "일곱 유형 중 가장 대조적인 세 유형", fontsize=7.5, color=GRAY)
    save(fig, "그림4-3")


# 그림 4-4: 라우볼피아에서 레세르핀까지
def fig44():
    fig, ax = plt.subplots(figsize=(6.8, 3.2)); ax.set_xlim(0, 14); ax.set_ylim(0, 6); ax.axis("off")
    steps = [("수 세기에 걸친\n아유르베다\n전통 사용", "#bee3f8"), ("1931년 이후\n인도 학술지의\n정신과·고혈압\n보고", "#c6f6d5"), ("1949년\n바킬의 임상 요약\n(10년·의사 약 50명\n의견)", "#fefcbf"),
             ("알칼로이드\n레세르핀\n(강한 진정 작용)", "#fed7aa"), ("1957년\n래스커상", "#fed7d7")]
    for i, (t, c) in enumerate(steps):
        x = .2 + i * 2.75; box(ax, x, 1.3, 2.35, 2.8, t, c, 7)
        if i: arrow(ax, x - .38, 2.7, x - .02, 2.7)
    ax.text(7, 5.3, "전통 약초가 서양 의학에 들어간 경로", ha="center", fontsize=10.5, fontweight="bold")
    ax.text(7, .5, "출처: Lasker Foundation의 바킬 소개문, Vakil(1949)", ha="center", fontsize=7.5, color=GRAY)
    save(fig, "그림4-4")


# 그림 4-5: 사퍼 2008
def fig45():
    wcsv("중금속조사.csv", ["group", "percent_with_metal"], [("전체", 20.7), ("미국 제조", 21.7), ("인도 제조", 19.5), ("라사 샤스트라", 40.6), ("비 라사 샤스트라", 17.1)])
    fig, axs = plt.subplots(1, 2, figsize=(6.8, 3.1), gridspec_kw={"width_ratios": [1.3, 1]})
    ax = axs[0]; v = [20.7, 21.7, 19.5]
    b = ax.bar(["전체", "미국\n제조", "인도\n제조"], v, color=[BLUE, GREEN, ORANGE], hatch=["", "//", "xx"], edgecolor="white", width=.6)
    for r, x in zip(b, v): ax.text(r.get_x() + r.get_width() / 2, x + 1.5, f"{x}%", ha="center", fontweight="bold", fontsize=8.5)
    ax.set_ylim(0, 55); ax.set_ylabel("금속 검출 제품 비율(%)"); ax.set_title("제조 국가별(P = 0.86)", fontsize=8.5)
    ax = axs[1]; v = [40.6, 17.1]
    b = ax.bar(["라사 샤스트라\n제품", "그 밖의\n제품"], v, color=[RED, GRAY], hatch=["", "//"], edgecolor="white", width=.6)
    for r, x in zip(b, v): ax.text(r.get_x() + r.get_width() / 2, x + 1.5, f"{x}%", ha="center", fontweight="bold", fontsize=8.5)
    ax.set_ylim(0, 55); ax.set_title("제조 방식별(P = 0.007)", fontsize=8.5)
    fig.tight_layout(); save(fig, "그림4-5")


# 그림 4-6: 아슈와간다 임상시험
def fig46():
    wcsv("아슈와간다.csv", ["measure", "placebo_kg", "ashwagandha_kg"], [("bench press gain", 26.4, 46.0), ("leg extension gain", 9.8, 14.5)])
    fig, axs = plt.subplots(1, 3, figsize=(6.8, 3.1), gridspec_kw={"width_ratios": [1.15, 1, 1]})
    ax = axs[0]; ax.axis("off")
    box(ax, 0, .1, 1, .8, "", "#edf2f7"); ax.set_xlim(-.05, 1.05); ax.set_ylim(0, 1)
    ax.text(.5, .5, "건강한 젊은 남성 57명\n(저항 운동 초보자)\n\n8주 · 이중맹검\n아슈와간다 뿌리 추출물\n300 mg 하루 2회(29명)\n전분 위약(28명)", ha="center", va="center", fontsize=7.6)
    for ax, t, v, p in [(axs[1], "벤치프레스\n근력 증가(kg)", (26.4, 46.0), "P = 0.001"), (axs[2], "레그 익스텐션\n근력 증가(kg)", (9.8, 14.5), "P = 0.04")]:
        b = ax.bar(["위약", "아슈와간다"], v, color=[GRAY, GREEN], hatch=["//", ""], edgecolor="white", width=.6)
        for r, x in zip(b, v): ax.text(r.get_x() + r.get_width() / 2, x + 1, f"{x}", ha="center", fontweight="bold", fontsize=8.5)
        ax.set_title(t + "\n" + p, fontsize=8); ax.set_ylim(0, 58); ax.tick_params(axis="x", labelsize=8)
    fig.tight_layout(); save(fig, "그림4-6")


# 그림 4-7: 주제어
TOP = [("아유르베다", r"ayurved"), ("임상시험", r"clinical trial"), ("커큐민·강황", r"curcumin|turmeric"), ("유나니", r"unani"),
       ("민족식물학", r"ethnobotan"), ("아슈와간다", r"ashwagandha|withania"), ("시다", r"siddha"), ("툴시", r"tulsi|ocimum")]
def fig47():
    sa = [r for r in rows() if "south-asia" in (r["tags"] or "")]
    cnt = {n: sum(1 for r in sa if re.search(p, (r["title"] or "") + " " + (r["abstract"] or ""), re.I)) for n, p in TOP}
    wcsv("남아시아주제별논문수.csv", ["topic", "papers"], cnt.items())
    order = sorted(cnt, key=lambda k: cnt[k])
    fig, ax = plt.subplots(figsize=(6.2, 3.3))
    b = ax.barh(order, [cnt[k] for k in order], color=BLUE, hatch=["//" if i % 2 == 0 else "" for i in range(len(order))], edgecolor="white")
    for r, k in zip(b, order): ax.text(cnt[k] + 6, r.get_y() + r.get_height() / 2, f"{cnt[k]:,}", va="center", fontsize=9, fontweight="bold")
    ax.set_xlim(0, max(cnt.values()) * 1.15); ax.set_xlabel(f"제목·초록에 언급된 논문 수(편, 남아시아 약초 논문 {len(sa):,}편 중)")
    save(fig, "그림4-7"); return cnt, len(sa)


if __name__ == "__main__":
    fig41(); print(fig42()); fig43(); fig44(); fig45(); fig46(); print(fig47())

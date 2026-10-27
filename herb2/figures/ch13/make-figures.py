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





import numpy as np
def lab(ax,x,y,t,fs=8,**k): ax.text(x,y,t,ha="center",va="center",fontsize=fs,**k)

# 그림 13-1: 품질 사슬
def fig131():
    fig,ax=plt.subplots(figsize=(7.2,3.6)); ax.set_xlim(0,12); ax.set_ylim(0,10); ax.axis("off")
    steps=["종 확인","재배·채취","가공·법제","추출·제형","시험·출하"]
    fails=["종 대체·위조","환경에 따른\n성분 변동","가공 방법의\n차이","제품 간\n함량 차이","중금속·\n이물 오염"]
    for i,(s,f) in enumerate(zip(steps,fails)):
        x=0.2+i*2.35
        box(ax,x,6.2,2.0,1.8,s,"#ebf8ff",fs=9,bold=True)
        if i<4: arrow(ax,x+2.05,7.1,x+2.4,7.1)
        arrow(ax,x+1.0,6.2,x+1.0,4.9)
        ax.add_patch(FancyBboxPatch((x,2.8),2.0,2.0,boxstyle="round,pad=0.02,rounding_size=0.1",fc="#fed7d7",ec="#2d3748",hatch="//"))
        lab(ax,x+1.0,3.8,f,fs=8,bbox=dict(fc="white",ec="none",pad=1.5))
    ax.add_patch(FancyBboxPatch((0.2,0.4),11.4,1.5,boxstyle="round,pad=0.02,rounding_size=0.1",fc="#c6f6d5",ec="#2d3748"))
    lab(ax,5.9,1.15,"약전(모노그래프)·규제·표준화가 각 단계에 기준을 건다",fs=9,fontweight="bold")
    save(fig,"그림13-1")

# 그림 13-2: 말뭉치 용어
def fig132():
    R=rows()
    kw=[("표준화","standardi[sz]"),("규제·법령","regulatory|legislation"),("HPLC","HPLC|high.performance liquid"),("품질관리","quality control"),("위조·진위 확인","adulterat|authenticat"),("약전","pharmacopo[e]?ia"),("지문 분석","fingerprint"),("품질 표지자","marker compound|quality marker|Q-marker|chemical marker"),("모노그래프","monograph"),("우수제조기준(GMP)","good manufacturing|\\bGMP\\b")]
    kc=[(n,sum(1 for r in R if re.search(p,(r["title"] or "")+" "+(r["abstract"] or ""),re.I))) for n,p in kw]
    kc.sort(key=lambda x:-x[1])
    wcsv("품질용어언급.csv",["용어","편수"],kc)
    fig,ax=plt.subplots(figsize=(6.4,3.6))
    ax.barh([k for k,_ in kc][::-1],[v for _,v in kc][::-1],color=BLUE,hatch="\\\\",edgecolor="white")
    for i,(k,v) in enumerate(kc[::-1]): ax.text(v+4,i,str(v),va="center",fontsize=8)
    ax.set_xlabel("제목·초록에서 언급된 논문 수(말뭉치 7,182편 중)"); ax.set_xlim(0,320)
    fig.tight_layout(); save(fig,"그림13-2"); return kc

# 그림 13-3: 입증 책임의 방향
def fig133():
    fig,ax=plt.subplots(figsize=(7,3.4)); ax.set_xlim(0,12); ax.set_ylim(0,10); ax.axis("off")
    lab(ax,6,9.4,"누가 증명해야 하는가",fs=10,fontweight="bold")
    # 의약품 줄
    lab(ax,1.1,7.0,"의약품",fs=9,fontweight="bold")
    box(ax,2.2,6.0,2.6,2.0,"제조사가\n안전성·유효성 입증","#bee3f8",fs=8)
    arrow(ax,4.9,7.0,5.7,7.0)
    box(ax,5.8,6.0,2.4,2.0,"승인","#e2e8f0",fs=8)
    arrow(ax,8.3,7.0,9.1,7.0)
    box(ax,9.2,6.0,2.5,2.0,"시판","#c6f6d5",fs=8)
    # 보충제 줄
    lab(ax,1.1,3.0,"식이보충제\n(1994년 법 이후)",fs=8.5,fontweight="bold")
    box(ax,2.2,2.0,2.6,2.0,"제조사가\n시판","#c6f6d5",fs=8)
    arrow(ax,4.9,3.0,5.7,3.0)
    box(ax,5.8,2.0,2.4,2.0,"시판 중\n문제 발생","#fed7d7",fs=8)
    arrow(ax,8.3,3.0,9.1,3.0)
    box(ax,9.2,2.0,2.5,2.0,"FDA가 위험을\n입증해야 제재","#bee3f8",fs=8)
    save(fig,"그림13-3")

# 그림 13-4: 러시아 약전
def fig134():
    fig,ax=plt.subplots(figsize=(6.4,2.4))
    ax.barh(["USSR 약전 제11판\n식물 모노그래프 83종"],[51],color=BLUE,hatch="//",edgecolor="white",label="유럽 약전에도 수록 51종")
    ax.barh(["USSR 약전 제11판\n식물 모노그래프 83종"],[32],left=[51],color=ORANGE,hatch="xx",edgecolor="white",label="USSR 약전에만 수록 32종")
    ax.text(25.5,0,"51",ha="center",va="center",color="white",fontsize=11,fontweight="bold",bbox=dict(fc="#2d3748",ec="none",pad=2))
    ax.text(67,0,"32",ha="center",va="center",color="white",fontsize=11,fontweight="bold",bbox=dict(fc="#2d3748",ec="none",pad=2))
    ax.set_xlim(0,83); ax.set_xlabel("식물 종 수"); ax.legend(loc="upper center",bbox_to_anchor=(0.5,-0.4),ncol=2,fontsize=8,frameon=False)
    wcsv("러시아약전.csv",["구분","종수"],[("유럽약전에도 수록",51),("USSR 약전에만 수록",32)])
    fig.tight_layout(); save(fig,"그림13-4")

# 그림 13-5: 지표 성분 → 지문 → Q-marker
def fig135():
    fig,ax=plt.subplots(figsize=(7.2,3.4)); ax.set_xlim(0,12); ax.set_ylim(0,10); ax.axis("off")
    cols=[("지표 성분 정량","특정 화합물 하나 또는 몇 개의\n함량만 확인",BLUE,"//"),("화학 지문","전체 성분 패턴이\n기준과 같은지 확인",ORANGE,"xx"),("품질 표지자(Q-marker)","성질·효능·성분을 이론과\n연결해 표지자를 고름",GREEN,"\\\\")]
    for i,(t,d,c,h) in enumerate(cols):
        x=0.3+i*3.95
        ax.add_patch(FancyBboxPatch((x,5.6),3.5,2.2,boxstyle="round,pad=0.02,rounding_size=0.1",fc=c,ec="#2d3748",hatch=h,alpha=0.9))
        lab(ax,x+1.75,6.7,t,fs=8.5,fontweight="bold",color="white",bbox=dict(fc="#2d3748",ec="none",pad=2))
        box(ax,x,2.6,3.5,2.2,d,"white",fs=8)
        if i<2: arrow(ax,x+3.55,6.7,x+3.9,6.7)
    lab(ax,6,1.0,"일관성 보증의 범위가 넓어지는 방향",fs=9,fontweight="bold")
    arrow(ax,1.5,0.4,10.5,0.4)
    save(fig,"그림13-5")

# 그림 13-6: Luo 2021 중금속 기준 초과율
def fig136():
    d=[("납(Pb)",5.75),("카드뮴(Cd)",4.96),("비소(As)",4.17),("수은(Hg)",3.78),("구리(Cu)",1.75)]
    wcsv("중금속기준초과율.csv",["금속","초과율(%)"],d)
    fig,(a,b)=plt.subplots(1,2,figsize=(7,3.2),gridspec_kw={"width_ratios":[1,2.2]})
    b0=a.bar(["하나 이상\n초과"],[30.51],color=RED,hatch="//",edgecolor="white"); a.set_ylim(0,36); a.set_ylabel("시료 비율(%)")
    a.text(0,31.2,"30.5%",ha="center",fontsize=9,fontweight="bold")
    b.bar([k for k,_ in d],[v for _,v in d],color=BLUE,hatch="\\\\",edgecolor="white"); b.set_ylim(0,8)
    for i,(k,v) in enumerate(d): b.text(i,v+0.2,f"{v}%",ha="center",fontsize=8.5)
    b.set_ylabel("금속별 기준 초과 시료 비율(%)")
    fig.tight_layout(); save(fig,"그림13-6")

# 그림 13-7: 일본 약전 DNA 바코드
def fig137():
    d=[("데이터베이스가\n포괄하는 종(약전 수록종 중)",95),("시판·재배 시료 100개 중\n라벨 종과 일치",78)]
    wcsv("일본약전바코드.csv",["항목","비율(%)"],d)
    fig,ax=plt.subplots(figsize=(6.4,3.0))
    ax.bar([k for k,_ in d],[v for _,v in d],color=[GREEN,ORANGE],hatch="//",edgecolor="white",width=0.5)
    for i,(k,v) in enumerate(d): ax.text(i,v+2,f"{v}%",ha="center",fontsize=10,fontweight="bold")
    ax.set_ylim(0,110); ax.set_ylabel("%")
    fig.tight_layout(); save(fig,"그림13-7")

if __name__=="__main__":
    fig131(); kc=fig132(); fig133(); fig134(); fig135(); fig136(); fig137(); print(kc)

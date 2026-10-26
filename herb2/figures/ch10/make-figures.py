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




# 그림 10-1: 한 표적 대 네트워크
def fig101():
    fig,axs=plt.subplots(1,2,figsize=(6.8,3.2))
    ax=axs[0]; ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis("off")
    ax.add_patch(plt.Circle((2.2,5),1.1,color="#fefcbf",ec="#2d3748")); ax.text(2.2,5,"약\n1개",ha="center",va="center",fontsize=8)
    ax.add_patch(plt.Circle((7.8,5),1.1,color="#bee3f8",ec="#2d3748")); ax.text(7.8,5,"표적\n1개",ha="center",va="center",fontsize=8)
    arrow(ax,3.3,5,6.7,5); ax.text(5,8.7,"한 약, 한 표적",ha="center",fontsize=9.5,fontweight="bold")
    ax=axs[1]; ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis("off")
    import numpy as np
    L=[(1.3,8),(1.3,5),(1.3,2)]; Rr=[(8.5,8.3),(8.5,6.2),(8.5,4.1),(8.5,2)]
    for (x,y) in L: ax.add_patch(plt.Circle((x,y),.8,color="#fefcbf",ec="#2d3748"))
    for (x,y) in Rr: ax.add_patch(plt.Circle((x,y),.8,color="#bee3f8",ec="#2d3748"))
    for (x,y) in L:
        for (u,v) in Rr: ax.plot([x+.8,u-.8],[y,v],color="#a0aec0",lw=.8,zorder=0)
    ax.text(1.3,9.3,"성분",ha="center",fontsize=8); ax.text(8.5,9.3,"표적",ha="center",fontsize=8)
    ax.text(5,.2,"여러 성분 · 여러 표적 · 질환",ha="center",fontsize=8)
    ax.text(5,10.2,"네트워크",ha="center",fontsize=9.5,fontweight="bold")
    fig.suptitle("약리학의 두 관점(개념도)",fontsize=10.5,fontweight="bold",y=1.03)
    save(fig,"그림10-1")

# 그림 10-2: TCMSP 규모
def fig102():
    items=[("등재 약초(종)",499),("성분",29384),("표적",3311),("연관 질환",837)]
    wcsv("TCMSP규모.csv",["item","n"],items)
    fig,ax=plt.subplots(figsize=(6.2,2.9)); k=[a for a,_ in items][::-1]; v=[b for _,b in items][::-1]
    b=ax.barh(k,v,color=[ORANGE,GREEN,BLUE,GRAY][::-1],hatch=["xx","","//",""][::-1],edgecolor="white"); ax.set_xscale("log")
    for r,x in zip(b,v): ax.text(x*1.15,r.get_y()+r.get_height()/2,f"{x:,}",va="center",fontweight="bold")
    ax.set_xlim(100,200000); ax.set_xlabel("개수(로그 눈금)")
    save(fig,"그림10-2"); 

# 그림 10-3: 연도별 네트워크 약리학 논문
def fig103():
    net=[r for r in rows() if "network-pharm" in (r["tags"] or "")]
    by=collections.Counter(int(r["year"]) for r in net if r["year"])
    yrs=list(range(2012,2026)); vals=[by.get(y,0) for y in yrs]
    wcsv("네트워크약리학연도별.csv",["year","papers"],zip(yrs,vals))
    fig,ax=plt.subplots(figsize=(6.4,3.0))
    ax.bar([str(y) for y in yrs],vals,color=BLUE,width=.7)
    ax.set_ylabel("논문 수(편)"); ax.yaxis.grid(True,color="#e2e8f0"); ax.set_axisbelow(True)
    ax.text(0.02,.9,"2024·2025년은 말뭉치 수집 시점상 일부만 포함됐을 수 있음",transform=ax.transAxes,fontsize=7.5)
    ax.tick_params(axis="x",labelsize=8)
    save(fig,"그림10-7"); return len(net)

# 그림 10-4: 커큐민 생쥐 용량 반응
def fig104():
    ends=["산화된 단백질","인터루킨-1베타","GFAP(성상세포 표지)","불용성·가용성\n아밀로이드 베타","플라크 부담"]
    low=[1,1,1,1,1]; high=[1,1,0,0,0]
    wcsv("커큐민용량반응.csv",["endpoint","low_160ppm","high_5000ppm"],[(e.replace("\n"," "),l,h) for e,l,h in zip(ends,low,high)])
    fig,ax=plt.subplots(figsize=(6.4,3.1)); ax.set_xlim(0,10); ax.set_ylim(0,6.4); ax.axis("off")
    ax.text(5.1,6.0,"유의하게 감소했는가",ha="center",fontsize=8.5,fontweight="bold"); ax.text(6.5,5.5,"저용량(160 ppm)",ha="center",fontsize=8); ax.text(8.8,5.5,"고용량(5,000 ppm)",ha="center",fontsize=8)
    for i,(e,l,h) in enumerate(zip(ends,low,high)):
        y=4.6-i*.95; ax.text(.1,y,e,va="center",fontsize=8)
        for x,v in ((6.5,l),(8.8,h)):
            ax.add_patch(FancyBboxPatch((x-.6,y-.33),1.2,.66,boxstyle="round,pad=0.02,rounding_size=0.1",fc="#c6f6d5" if v else "#e2e8f0",ec="#2d3748"))
            ax.text(x,y,"감소" if v else "변화 없음",ha="center",va="center",fontsize=7.8,fontweight="bold" if v else "normal")
    ax.text(.1,-.3,"저용량에서 불용성·가용성 아밀로이드 베타와 플라크 부담이 43~50% 감소(Lim 2001)",fontsize=7.5)
    save(fig,"그림10-6")

# 그림 10-5: 커큐민 연표
def fig105():
    ev=[("1815","분리\n(Vogel·Pelletier)","up"),("1937","첫 임상시험\n(Lancet)","down"),("1949","항균 활성\n(Nature)","up"),("1990","논문 100편\n미만","down"),("2016","논문 약 9,000편\n임상시험 100건+","up")]
    xs=[0,2.2,2.9,4.6,7.2]
    wcsv("커큐민연표.csv",["year","event"],[(a,b.replace("\n"," ")) for a,b,_ in ev])
    fig,ax=plt.subplots(figsize=(6.8,2.9)); ax.set_xlim(-.9,9); ax.set_ylim(-2.4,2.4); ax.axis("off")
    ax.plot([-.5,8.5],[0,0],color="#2d3748",lw=2)
    for x,(y,t,d) in zip(xs,ev):
        s=1 if d=="up" else -1; ax.plot([x,x],[0,s*.9],color=GRAY,lw=1); ax.plot([x],[0],"o",color=BLUE,ms=7)
        ax.text(x,s*1.0,f"{y}\n{t}",ha="center",va="bottom" if s>0 else "top",fontsize=7.5)
    ax.text(4,2.35,"커큐민 연구의 이정표(Kunnumakkara 2017)",ha="center",fontsize=10,fontweight="bold")
    save(fig,"그림10-5")

# 그림 10-6: 시너지의 세 층위
def fig106():
    fig,ax=plt.subplots(figsize=(6.8,3.0)); ax.set_xlim(0,14); ax.set_ylim(0,6); ax.axis("off")
    box(ax,.2,1.5,3.6,3.0,"약초 사이의\n시너지\n(복합 처방)","#fefcbf",8)
    box(ax,5.2,1.5,3.6,3.0,"유효 분획 사이의\n시너지","#fed7aa",8)
    box(ax,10.2,1.5,3.6,3.0,"순수 화합물 사이의\n시너지","#c6f6d5",8,True)
    arrow(ax,3.8,3,5.2,3); arrow(ax,8.8,3,10.2,3)
    ax.text(7,5.5,"시너지의 세 층위: 신약 개발은 현재 오른쪽에 집중(Yuan 2017)",ha="center",fontsize=9.5,fontweight="bold")
    ax.text(7,.5,"증거의 수준은 낮고 임상적 의미는 대부분 미확정(Zhou 2016)",ha="center",fontsize=8,color="#c53030")
    save(fig,"그림10-4")

# 그림 10-7: 천연물 화학 공간
def fig107():
    fig,ax=plt.subplots(figsize=(6.8,3.0)); ax.set_xlim(0,14); ax.set_ylim(0,6); ax.axis("off")
    box(ax,.2,1.5,3.6,3.0,"천연물 구조\n약 20만 개\n수집","#c6f6d5",8)
    box(ax,5.2,3.4,3.8,1.8,"화학 공간이\nFDA 승인 약물과\n크게 겹침","#fefcbf",7.5)
    box(ax,5.2,.6,3.8,1.8,"332개 표적 단백질에\n가상 도킹","#bee3f8",7.5)
    box(ax,10.3,1.5,3.5,3.0,"다표적 작용이\n많은 화합물에\n집중(폴리파마콜로지)","#fed7aa",7.5)
    arrow(ax,3.8,3.4,5.2,4.3); arrow(ax,3.8,2.6,5.2,1.5); arrow(ax,9.0,4.3,10.3,3.6); arrow(ax,9.0,1.5,10.3,2.4)
    ax.text(7,5.7,"천연물을 화학 라이브러리로 읽다(Gu 2013)",ha="center",fontsize=10,fontweight="bold")
    save(fig,"그림10-3")

if __name__=="__main__":
    fig101();fig102();print(fig103());fig104();fig105();fig106();fig107()

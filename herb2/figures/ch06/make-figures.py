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



# 그림 6-1: 유럽 약초학 연표
def fig61():
    ev=[(60,"1세기","디오스코리데스\n『약물지』","up",1.0),(512,"약 512년","빈 디오스코리데스\n사본 제작","down",1.0),(1763,"1763","스톤: 버드나무 껍질\n편지","up",1.0),(1828,"1828","뷔흐너: 살리신\n결정","down",1.0),(1838,"1838","피리아: 살리실산","up",1.6),(1897,"1897","호프만: 아세틸\n살리실산(아스피린)","down",1.0)]
    wcsv("유럽연표.csv",["year","label"],[(y,l.replace("\n"," ")) for y,_,l,_,_ in ev])
    xs=[0,1.2,5.0,6.2,7.1,8.6]
    fig,ax=plt.subplots(figsize=(6.8,3.0)); ax.set_xlim(-.8,9.9); ax.set_ylim(-2.4,2.4); ax.axis("off")
    ax.plot([-.5,9.5],[0,0],color="#2d3748",lw=2)
    for x,(y,lab,t,d,h) in zip(xs,ev):
        s=1 if d=="up" else -1
        ax.plot([x,x],[0,s*h*.9],color=GRAY,lw=1); ax.plot([x],[0],"o",color=BLUE,ms=7)
        ax.text(x,s*(h*.9+.1),f"{lab}\n{t}",ha="center",va="bottom" if s>0 else "top",fontsize=7.5)
    save(fig,"그림6-1")

# 그림 6-2: 버드나무에서 아스피린까지
def fig62():
    fig,ax=plt.subplots(figsize=(6.8,2.6)); ax.set_xlim(0,15); ax.set_ylim(0,5); ax.axis("off")
    xs=[.1,3.2,6.3,9.4,12.5]; tx=["버드나무 껍질\n(학질 치료,\n1763)","살리신 결정\n(1828)","살리실산\n(1838)","아세틸살리실산\n합성(1897)","의약품\n아스피린"]
    cs=["#c6f6d5","#fefcbf","#fed7aa","#bee3f8","#e9d8fd"]
    for x,t,c in zip(xs,tx,cs): box(ax,x,1.4,2.4,2.2,t,c,7.8)
    for x in xs[:-1]: arrow(ax,x+2.4,2.5,x+3.2,2.5)
    ax.text(7.5,4.5,"약초에서 의약품으로: 버드나무에서 아스피린까지",ha="center",fontsize=9.5,fontweight="bold")
    save(fig,"그림6-2")

# 그림 6-3: 세인트존스워트 약물 상호작용
def fig63():
    wcsv("세인트존스워트상호작용.csv",["measure","before_or_placebo","after_or_hypericum"],[("알프라졸람 반감기(시간)",12.4,6.0),("디곡신 AUC(마이크로그램 시간/L)",17.2,12.9)])
    fig,axs=plt.subplots(1,3,figsize=(6.8,2.9),gridspec_kw={"width_ratios":[1.25,1,1]})
    ax=axs[0]; ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(0,10)
    for y,t,c in [(8,"히페리포린\n(성분)","#fefcbf"),(5.2,"PXR 활성화\n(Ki 27 nM)","#fed7aa"),(2.4,"CYP3A4 증가\n약물 분해 빨라짐","#fed7d7")]: box(ax,1,y-1,8,2,t,c,7.5)
    arrow(ax,5,7,5,6.2); arrow(ax,5,4.2,5,3.4); ax.set_title("기전(Moore 2000)",fontsize=8.5)
    ax=axs[1]; ax.bar(["복용 전","14일 복용 후"],[12.4,6.0],color=[BLUE,ORANGE],hatch=["","xx"],edgecolor="white",width=.55)
    for i,v in enumerate([12.4,6.0]): ax.text(i,v+.3,f"{v}",ha="center",fontweight="bold")
    ax.set_ylim(0,15); ax.set_ylabel("알프라졸람 반감기(시간)"); ax.set_title("건강인 12명\n(Markowitz 2003)",fontsize=8.5)
    ax=axs[2]; ax.bar(["위약군","세인트존스\n워트군"],[17.2,12.9],color=[BLUE,ORANGE],hatch=["","xx"],edgecolor="white",width=.55)
    for i,v in enumerate([17.2,12.9]): ax.text(i,v+.4,f"{v}",ha="center",fontweight="bold")
    ax.set_ylim(0,21); ax.set_ylabel("디곡신 AUC(0-24, 마이크로그램 시간/L)",fontsize=7.5); ax.set_title("25명, 10일 병용\n(Johne 1999)",fontsize=8.5)
    fig.tight_layout(); save(fig,"그림6-3")

# 그림 6-4: Permixon vs finasteride
def fig64():
    items=[("증상 점수(IPSS) 변화",-37,-39),("삶의 질 개선",38,41),("최대 요속 증가",25,30),("전립선 부피 변화",-6,-18),("혈청 PSA 변화",0,-41)]
    wcsv("퍼믹손피나스테리드.csv",["item","permixon_pct","finasteride_pct"],items)
    fig,ax=plt.subplots(figsize=(6.6,3.2)); import numpy as np
    y=np.arange(len(items))[::-1]
    ax.barh(y+.2,[a for _,a,_ in items],height=.36,color=GREEN,label="퍼믹손 320 mg(톱야자 추출물)")
    ax.barh(y-.2,[b for _,_,b in items],height=.36,color=GRAY,hatch="//",edgecolor="white",label="피나스테리드 5 mg")
    for yy,(n,a,b) in zip(y,items):
        ax.text(a+(1.5 if a>=0 else -1.5),yy+.2,f"{a:+d}%",va="center",ha="left" if a>=0 else "right",fontsize=7.5)
        ax.text(b+(1.5 if b>=0 else -1.5),yy-.2,f"{b:+d}%",va="center",ha="left" if b>=0 else "right",fontsize=7.5)
    ax.set_yticks(y); ax.set_yticklabels([n for n,_,_ in items],fontsize=8); ax.axvline(0,color="#2d3748",lw=.8)
    ax.set_xlim(-60,60); ax.set_xlabel("변화율(%)"); ax.legend(fontsize=7.5,loc="lower right")
    save(fig,"그림6-4")

# 그림 6-5: 어린이 에키네시아 시험
def fig65():
    wcsv("어린이에키네시아.csv",["item","echinacea","placebo"],[("감기 횟수(건)",337,370),("발진 비율(%)",7.1,2.7),("증상 심각도 점수(중앙값)",33,33)])
    fig,axs=plt.subplots(1,3,figsize=(6.8,2.8))
    for ax,(t,a,b,u,ylim) in zip(axs,[("치료한 감기 횟수",337,370,"건",430),("증상 심각도 점수\n(양 군 중앙값)",33,33,"점",45),("발진이 생긴 비율",7.1,2.7,"%",9)]):
        ax.bar(["에키네시아","위약"],[a,b],color=[ORANGE,BLUE],hatch=["xx",""],edgecolor="white",width=.55)
        for i,v in enumerate([a,b]): ax.text(i,v+ylim*.02,f"{v}{u}",ha="center",fontweight="bold",fontsize=8)
        ax.set_ylim(0,ylim); ax.set_title(t,fontsize=8.5)
    axs[1].text(.5,.88,"차이 없음(P=0.69)",transform=axs[1].transAxes,ha="center",fontsize=8)
    axs[2].text(.5,.82,"P=0.008",transform=axs[2].transAxes,ha="center",fontsize=8)
    fig.tight_layout(); save(fig,"그림6-5")

# 그림 6-6: 은행나무 코크란
def fig66():
    wcsv("은행나무코크란.csv",["item","n"],[("포함된 시험(편)",36),("6개월 시험(편)",9),("6개월 시험 환자(명)",2016),("알츠하이머 하위분석 시험(편)",9),("알츠하이머 하위분석 환자(명)",925)])
    fig,axs=plt.subplots(1,2,figsize=(6.8,2.9),gridspec_kw={"width_ratios":[1,1.2]})
    ax=axs[0]; ax.bar(["포함된\n시험","6개월\n시험","알츠하이머\n하위분석"],[36,9,9],color=[BLUE,GREEN,ORANGE],hatch=["","//","xx"],edgecolor="white",width=.6)
    for i,v in enumerate([36,9,9]): ax.text(i,v+.8,f"{v}편",ha="center",fontweight="bold")
    ax.set_ylim(0,44); ax.set_ylabel("시험 수(편)"); ax.set_title("시험의 수",fontsize=8.5)
    ax=axs[1]; ax.bar(["6개월 시험\n환자","알츠하이머\n하위분석 환자"],[2016,925],color=[GREEN,ORANGE],hatch=["//","xx"],edgecolor="white",width=.5)
    for i,v in enumerate([2016,925]): ax.text(i,v+50,f"{v:,}명",ha="center",fontweight="bold")
    ax.set_ylim(0,2400); ax.set_ylabel("환자 수(명)"); ax.set_title("환자의 수(결론: 일관된 이득 없음)",fontsize=8.5)
    fig.tight_layout(); save(fig,"그림6-6")

TOP=[("세인트존스워트",r"st\.? john|hypericum"),("약물 상호작용",r"interaction"),("임상시험",r"randomi[sz]ed|clinical trial"),("은행나무",r"ginkgo"),("에키네시아",r"echinacea"),("실리마린·엉겅퀴",r"silymarin|silybum|milk thistle"),("카모마일",r"chamomile|matricaria"),("발레리안",r"valerian")]
def fig67():
    eu=[r for r in rows() if "europe/" in (r["tags"] or "")]
    cnt={n:sum(1 for r in eu if re.search(p,(r["title"] or "")+" "+(r["abstract"] or ""),re.I)) for n,p in TOP}
    wcsv("유럽주제별논문수.csv",["topic","papers"],cnt.items())
    order=sorted(cnt,key=lambda k:cnt[k])
    fig,ax=plt.subplots(figsize=(6.2,3.2))
    b=ax.barh(order,[cnt[k] for k in order],color=BLUE,hatch=["//" if i%2==0 else "" for i in range(len(order))],edgecolor="white")
    for r,k in zip(b,order): ax.text(cnt[k]+1.5,r.get_y()+r.get_height()/2,f"{cnt[k]:,}",va="center",fontsize=9,fontweight="bold")
    ax.set_xlim(0,max(cnt.values())*1.15); ax.set_xlabel(f"제목·초록에 언급된 논문 수(편, 유럽 식물요법 논문 {len(eu):,}편 중)")
    save(fig,"그림6-7"); return cnt,len(eu)

if __name__=="__main__":
    fig61();fig62();fig63();fig64();fig65();fig66()
    print(fig67())

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





import numpy as np, textwrap

def lab(ax,x,y,t,fs=8,**k): ax.text(x,y,t,ha="center",va="center",fontsize=fs,**k)

# 그림 12-1: 위험의 세 갈래(개념도)
def fig121():
    fig,ax=plt.subplots(figsize=(7,3.4)); ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis("off")
    cols=[("성분 자체의 독성",RED,"//",["아리스톨로크산","간 손상(HILI)"]),
          ("약물과의 상호작용",ORANGE,"xx",["효소(CYP3A4) 유도","P-당단백 유도"]),
          ("제품의 품질",BLUE,"\\\\",["중금속 오염","종 대체·위조"])]
    box(ax,3.4,8.3,3.2,1.4,"약초 제품을\n복용하는 사람","#edf2f7",fs=9,bold=True)
    for i,(t,c,h,items) in enumerate(cols):
        x=0.2+i*3.2
        arrow(ax,5,8.3,x+1.5,6.7)
        ax.add_patch(FancyBboxPatch((x,5.2),3.0,1.4,boxstyle="round,pad=0.02,rounding_size=0.1",fc=c,ec="#2d3748",hatch=h,alpha=0.9))
        ax.text(x+1.5,5.9,t,ha="center",va="center",fontsize=8.5,fontweight="bold",color="white",bbox=dict(fc="#2d3748",ec="none",pad=2))
        for j,it in enumerate(items):
            box(ax,x,3.2-j*1.9,3.0,1.4,it,"white",fs=8)
    save(fig,"그림12-1")

# 그림 12-2: 말뭉치 안전성 논문
def fig122():
    R=rows()
    kw=[("약초-약물(herb-drug)","herb-drug"),("이상반응","adverse event"),("간독성","hepatotox"),("오염","contaminat"),("사례 보고","case report"),("위조·불순물 혼입","adulterat"),("중금속","heavy metal"),("DNA 바코드","DNA barcod"),("약물감시","pharmacovigilance"),("약물 유발 간 손상","DILI"),("아리스톨로크산","aristolochic"),("피롤리지딘","pyrrolizidine")]
    kc=[(n,sum(1 for r in R if re.search(p,(r["title"] or "")+" "+(r["abstract"] or ""),re.I))) for n,p in kw]
    kc.sort(key=lambda x:-x[1])
    safe=[r for r in R if "global/safety" in (r["tags"] or "")]
    wcsv("안전성키워드언급.csv",["키워드","편수"],kc)
    fig,ax=plt.subplots(figsize=(6.4,3.8))
    ax.barh([k for k,_ in kc][::-1],[v for _,v in kc][::-1],color=RED,hatch="//",edgecolor="white")
    for i,(k,v) in enumerate(kc[::-1]): ax.text(v+3,i,str(v),va="center",fontsize=8)
    ax.set_xlabel("제목·초록에서 언급된 논문 수(말뭉치 7,182편 중)"); ax.set_xlim(0,290)
    fig.tight_layout(); save(fig,"그림12-2"); return len(safe),kc

# 그림 12-3: Nortier 2000
def fig123():
    d=[("요로상피암",18),("경도~중등도 이형성",19),("정상 요로상피",2)]
    wcsv("노르티에예방수술.csv",["소견","환자 수"],d)
    fig,ax=plt.subplots(figsize=(6.4,2.8))
    cs=[RED,ORANGE,GRAY]; hs=["//","xx",".."]; left=0
    for (n,v),c,h in zip(d,cs,hs):
        ax.barh(["예방적 수술\n39명"],[v],left=left,color=c,hatch=h,edgecolor="white",label=f"{n} {v}명")
        ax.text(left+v/2,0,str(v),ha="center",va="center",color="black",fontweight="bold",fontsize=10,bbox=dict(fc="white",ec="none",pad=2)); left+=v
    ax.set_xlim(0,39); ax.set_xlabel("환자 수(명)"); ax.legend(fontsize=7.5,frameon=False,loc="upper center",bbox_to_anchor=(0.5,-0.3),ncol=3)
    fig.tight_layout(); save(fig,"그림12-3")

# 그림 12-4: Ng 2017
def fig124():
    d=[("대만(2개 병원, 98예)",78),("중국",47),("동남아시아",29),("한국",13),("북미",4.8),("일본",2.7),("유럽",1.7)]
    wcsv("아리스톨로크산서명간암.csv",["지역","서명 보인 비율(%)"],d)
    fig,ax=plt.subplots(figsize=(6.4,3.4))
    ax.barh([k for k,_ in d][::-1],[v for _,v in d][::-1],color=RED,hatch="//",edgecolor="white")
    for i,(k,v) in enumerate(d[::-1]): ax.text(v+1.2,i,f"{v:g}%",va="center",fontsize=9,fontweight="bold")
    ax.set_xlim(0,92); ax.set_xlabel("간세포암에서 아리스톨로크산 돌연변이 서명을 보인 비율(%)")
    fig.tight_layout(); save(fig,"그림12-4")

# 그림 12-5: Durr 2000
def fig125():
    rat=[("장 P-당단백",3.8),("간 CYP3A2",2.5)]
    hum=[("십이지장 P-당단백",1.4),("십이지장 CYP3A4",1.5),("간 CYP3A4 활성",1.4)]
    wcsv("세인트존스워트효소유도.csv",["대상","지표","배수"],[("쥐",a,b) for a,b in rat]+[("사람 8명",a,b) for a,b in hum])
    fig,axs=plt.subplots(1,2,figsize=(7,3.2),gridspec_kw={"width_ratios":[2,3]})
    for ax,dd,t,c,h in [(axs[0],rat,"쥐(14일 투여)",ORANGE,"//"),(axs[1],hum,"건강한 남성 8명(14일 투여)",BLUE,"xx")]:
        ax.bar([textwrap.fill(a,8) for a,_ in dd],[b for _,b in dd],color=c,hatch=h,edgecolor="white")
        for i,(a,b) in enumerate(dd): ax.text(i,b+0.08,f"{b}배",ha="center",fontsize=9,fontweight="bold")
        ax.axhline(1,color="#2d3748",lw=1,ls="--"); ax.set_ylim(0,4.4); ax.set_title(t,fontsize=9); ax.set_ylabel("대조 대비 발현·활성(배)",fontsize=8)
    fig.tight_layout(); save(fig,"그림12-5")

# 그림 12-6: Fugh-Berman & Ernst 2001
def fig126():
    d=[("평가 불가",68.5),("가능한 상호작용",18.5),("잘 문서화된 상호작용",13)]
    wcsv("약초약물보고신뢰도.csv",["분류","비율(%)"],d)
    fig,ax=plt.subplots(figsize=(6.4,2.9))
    cs=[GRAY,ORANGE,RED]; hs=["..","xx","//"]; left=0
    for (n,v),c,h in zip(d,cs,hs):
        ax.barh(["의심 사례\n108건"],[v],left=left,color=c,hatch=h,edgecolor="white",label=f"{n} {v}%")
        ax.text(left+v/2,0,f"{v}%",ha="center",va="center",fontweight="bold",fontsize=10,bbox=dict(fc="white",ec="none",pad=2)); left+=v
    ax.set_xlim(0,100); ax.set_xlabel("비율(%)"); ax.legend(fontsize=7.5,frameon=False,loc="upper center",bbox_to_anchor=(0.5,-0.3),ncol=3)
    fig.tight_layout(); save(fig,"그림12-6")

# 그림 12-7: Saper 2004
def fig127():
    wcsv("아유르베다중금속.csv",["항목","값"],[("제품 수",70),("중금속 검출 제품",14),("납",13),("수은",6),("비소",6)])
    fig,axs=plt.subplots(1,2,figsize=(7,3.2),gridspec_kw={"width_ratios":[1,1.3]})
    ax=axs[0]; ax.bar(["중금속\n검출","미검출"],[14,56],color=[RED,GRAY],hatch="//",edgecolor="white")
    for i,v in enumerate([14,56]): ax.text(i,v+1.2,f"{v}개",ha="center",fontweight="bold"); 
    ax.text(0,7,"20%",ha="center",color="black",fontweight="bold",fontsize=10,bbox=dict(fc="white",ec="none",pad=2)); ax.set_ylim(0,66); ax.set_ylabel("제품 수(전체 70개)"); ax.set_title("보스턴 식료품점 제품",fontsize=9)
    ax=axs[1]; names=["납","수은","비소"]; n=[13,6,6]; med=[40,20225,430]
    ax.bar(names,n,color=[GRAY,ORANGE,BLUE],hatch=["..","xx","\\\\"][0],edgecolor="white")
    for i,(v,m) in enumerate(zip(n,med)): ax.text(i,v+0.3,f"{v}개\n중앙값 {m:,} µg/g",ha="center",fontsize=7.5)
    ax.set_ylim(0,18); ax.set_ylabel("검출 제품 수"); ax.set_title("금속별(중복 포함)",fontsize=9)
    fig.tight_layout(); save(fig,"그림12-7")

# 그림 12-8: DNA 바코드 식별률
def fig128():
    d=[("rbcL+matK\n(907시료·550종)",72),("ITS2\n(6,600시료·4,800종)",92.7)]
    wcsv("바코드종식별률.csv",["바코드","종 수준 식별률(%)"],[("rbcL+matK",72),("ITS2",92.7)])
    fig,ax=plt.subplots(figsize=(6,3.2))
    ax.bar([a for a,_ in d],[b for _,b in d],color=[GRAY,GREEN],hatch=["..","//"],edgecolor="white",width=0.5)
    for i,(a,b) in enumerate(d): ax.text(i,b+2,f"{b:g}%",ha="center",fontweight="bold",fontsize=10)
    ax.set_ylim(0,110); ax.set_ylabel("종 수준 식별 성공률(%)")
    ax.text(0.5,-0.27,"서로 다른 시료 집합에서의 수치이며 직접 비교한 결과가 아님",ha="center",transform=ax.transAxes,fontsize=7.5,color=RED)
    fig.tight_layout(); save(fig,"그림12-8")

if __name__=="__main__":
    fig121(); n,kc=fig122(); fig123(); fig124(); fig125(); fig126(); fig127(); fig128(); print(n,kc)

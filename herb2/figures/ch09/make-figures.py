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




# 그림 9-1: 카바의 여정
def fig91():
    fig,ax=plt.subplots(figsize=(6.8,3.0)); ax.set_xlim(0,15); ax.set_ylim(0,6.2); ax.axis("off")
    labels=["태평양 섬의\n의례·일상의 음료\n(수 세기)","유럽에서\n항불안 약초\n추출물로 사용","미국에서는\n건강 보조 식품,\n서구에서 기호 음료","간독성 보고\n(여러 나라)","서구 여러 나라의\n판매 금지 보도\n(2007 논문 서술)"]
    cs=["#c6f6d5","#fefcbf","#fed7aa","#fed7d7","#e2e8f0"]
    for i,(t,c) in enumerate(zip(labels,cs)):
        box(ax,.1+i*3.0,1.4,2.5,2.9,t,c,6.8)
        if i<4: arrow(ax,2.6+i*3.0,2.85,3.1+i*3.0,2.85)
    ax.text(7.5,5.6,"카바(Piper methysticum)의 여정",ha="center",fontsize=10.5,fontweight="bold")
    save(fig,"그림9-1")

# 그림 9-2: 증거의 사다리
def fig92():
    rows_=[("1996","증례","54세 남성\n알프라졸람\n병용"),("2001","증례","33세 여성\n카바 제제\n후 황달"),("2005·2007","사람 시험","건강인\n12명·16명\n대사 효소"),("2007","동물(쥐)","피페르\n메티스틴\n2주"),("2014","동물(생쥐)","카바+\n아세트\n아미노펜"),("2020","종설","표준화\n부재가\n핵심 과제")]
    wcsv("카바증거사다리.csv",["year","type","content"],[(a,b,c.replace("\n"," ")) for a,b,c in rows_])
    fig,ax=plt.subplots(figsize=(6.8,3.3)); ax.set_xlim(0,12.2); ax.set_ylim(0,7.4); ax.axis("off")
    cols=["#fed7d7","#fed7d7","#bee3f8","#c6f6d5","#c6f6d5","#e2e8f0"]
    for i,((y,t,c),cl) in enumerate(zip(rows_,cols)):
        x=.1+i*2.0; h=2.0+i*.6
        ax.add_patch(FancyBboxPatch((x,.3),1.8,h,boxstyle="round,pad=0.02,rounding_size=0.1",fc=cl,ec="#2d3748",lw=1))
        ax.text(x+.9,.3+h+.25,f"{y}\n{t}",ha="center",va="bottom",fontsize=7.5,fontweight="bold")
        ax.text(x+.9,.3+h/2,c,ha="center",va="center",fontsize=6.8)
    ax.text(6.1,6.8,"카바 안전성 근거가 쌓인 순서",ha="center",fontsize=10.5,fontweight="bold")
    save(fig,"그림9-2")

# 그림 9-3: 생쥐 실험 설계
def fig93():
    fig,ax=plt.subplots(figsize=(6.8,3.4)); ax.set_xlim(0,14); ax.set_ylim(0,7.9); ax.axis("off")
    box(ax,.1,3.0,2.8,1.8,"C57BL/6\n생쥐","#edf2f7",8,True)
    box(ax,4.0,5.2,4.4,1.5,"카바 단독\n(500 mg/kg, 장기)","#c6f6d5",7.5)
    box(ax,4.0,3.1,4.4,1.5,"카바 3일 전처리\n+ 아세트아미노펜","#fed7aa",7.5)
    box(ax,4.0,.8,4.4,1.5,"카바 성분을\n따로 투여 + 아세트아미노펜","#fefcbf",7.5)
    box(ax,9.4,5.2,4.3,1.5,"이상 반응 없음","#c6f6d5",7.5)
    box(ax,9.4,3.1,4.3,1.5,"ALT·AST 상승,\n간 병변 악화","#fed7d7",7.5)
    box(ax,9.4,.5,4.3,2.1,"플라보카와인 A·B: 상승\n디하이드로메티스티신: 변화 없음","#fed7d7",7)
    for y in (6.15,3.85,1.55): arrow(ax,2.9,3.9,4.0,y)
    for y in (6.15,3.85,1.55): arrow(ax,8.4,y,9.4,y if y!=1.55 else 1.55)
    ax.text(7,7.3,"카바·아세트아미노펜 병용 실험 설계(Narayanapillai 2014)",ha="center",fontsize=9,fontweight="bold")
    save(fig,"그림9-3")

# 그림 9-4: 사람의 약물 대사 효소
def fig94():
    wcsv("카바사람CYP.csv",["item","value"],[("골든실 CYP2D6 억제(약 %)",40),("골든실 CYP3A4/5 억제(약 %)",40),("카바 CYP2E1 감소(약 %)",40),("골든실 미다졸람 AUC 전",107.9),("골든실 미다졸람 AUC 후",175.3)])
    fig,axs=plt.subplots(1,2,figsize=(6.8,3.0),gridspec_kw={"width_ratios":[1.25,1]})
    ax=axs[0]; k=["골든실\nCYP2D6","골든실\nCYP3A4/5","카바\nCYP2E1","카바\nCYP3A4/5·\n2D6·1A2"]; v=[40,40,40,0]
    ax.bar(k,v,color=[ORANGE,ORANGE,GREEN,GRAY],hatch=["xx","xx","","//"],edgecolor="white",width=.6)
    for i,x in enumerate(v): ax.text(i,x+1.5,"약 40%\n억제" if x else "유의한\n변화 없음",ha="center",fontsize=7.5,fontweight="bold")
    ax.set_ylim(0,58); ax.set_ylabel("효소 활성 억제(약 %)"); ax.set_title("건강인 12명, 28일 보충(Gurley 2005)",fontsize=8.5); ax.tick_params(axis="x",labelsize=7)
    ax=axs[1]; ax.bar(["보충 전","골든실\n14일 후"],[107.9,175.3],color=[BLUE,ORANGE],hatch=["","xx"],edgecolor="white",width=.55)
    for i,x in enumerate([107.9,175.3]): ax.text(i,x+4,f"{x}",ha="center",fontweight="bold")
    ax.set_ylim(0,215); ax.set_ylabel("미다졸람 AUC(ng·h/mL)"); ax.set_title("건강인 16명(Gurley 2007)\n카바는 영향 없음",fontsize=8.5)
    fig.tight_layout(); save(fig,"그림9-4")

# 그림 9-5: 호주 설문
def fig95():
    wcsv("호주설문.csv",["survey","item","percent"],[("2019명","보완 의약품 사용",50.3),("2019명","비타민·무기질",47.8),("2019명","동종요법",6.8),("400명","불안에 약초 사용(평생)",72.8),("400명","처방 의약품 사용",55.3),("400명","약초·처방약 병용",27.5),("400명","의사에게 알리지 않음",48)])
    fig,axs=plt.subplots(1,2,figsize=(6.8,3.0))
    ax=axs[0]; k=["보완 의약품\n사용","비타민·\n무기질","동종요법"]; v=[50.3,47.8,6.8]
    ax.bar(k,v,color=[BLUE,GREEN,GRAY],hatch=["","//","xx"],edgecolor="white",width=.6)
    for i,x in enumerate(v): ax.text(i,x+1.5,f"{x}%",ha="center",fontweight="bold")
    ax.set_ylim(0,62); ax.set_ylabel("%"); ax.set_title("호주 성인 2,019명\n(Harnett 2019)",fontsize=8.5)
    ax=axs[1]; k=["불안에\n약초 사용","처방약\n사용","약초·처방약\n병용","의사에게\n알리지 않음"]; v=[72.8,55.3,27.5,48]
    ax.bar(k,v,color=[GREEN,BLUE,ORANGE,RED],hatch=["","//","xx","++"],edgecolor="white",width=.6)
    for i,x in enumerate(v): ax.text(i,x+1.5,f"{x}%",ha="center",fontweight="bold")
    ax.set_ylim(0,88); ax.set_ylabel("%"); ax.set_title("불안을 겪은 약초 사용 성인 400명\n(McIntyre 2016)",fontsize=8.5); ax.tick_params(axis="x",labelsize=7.5)
    fig.tight_layout(); save(fig,"그림9-5")

GEO=r"fiji|pacific|samoa|tonga|maori|aborigin|australia|new zealand|papua|polynesia|hawai|melanesia|vanuatu|tahiti|solomon island|torres"
TOP=[("설문·이용 실태",r"survey|prevalence|cross-sectional"),("원주민 의학",r"aborigin|maori|indigenous"),("약물 상호작용",r"interaction|cytochrome|CYP"),("카바",r"kava|piper methysticum"),("간독성",r"hepatotox|liver injury"),("노니",r"noni|morinda citrifolia"),("티트리",r"tea tree|melaleuca")]
def fig96():
    R=rows(); oc=[r for r in R if "oceania/" in (r["tags"] or "")]
    f=lambda r: re.search(GEO,(r["title"] or "")+" "+(r["abstract"] or ""),re.I)
    og=[r for r in oc if f(r)]; ag=[r for r in R if f(r)]
    cnt={n:sum(1 for r in ag if re.search(p,(r["title"] or "")+" "+(r["abstract"] or ""),re.I)) for n,p in TOP}
    wcsv("오세아니아말뭉치.csv",["item","papers"],[("오세아니아 태그",len(oc)),("그중 지명 언급",len(og)),("전체 말뭉치에서 지명 언급",len(ag))]+list(cnt.items()))
    fig,axs=plt.subplots(1,2,figsize=(6.8,3.1),gridspec_kw={"width_ratios":[.9,1.4]})
    ax=axs[0]; ax.bar(["태그","태그 중\n지명 언급","전체에서\n지명 언급"],[len(oc),len(og),len(ag)],color=[GRAY,ORANGE,BLUE],hatch=["//","xx",""],edgecolor="white",width=.6)
    for i,v in enumerate([len(oc),len(og),len(ag)]): ax.text(i,v+4,str(v),ha="center",fontweight="bold")
    ax.set_ylim(0,215); ax.set_ylabel("논문 수(편)"); ax.set_title("태그와 실제 지명",fontsize=8.5); ax.tick_params(axis="x",labelsize=7.5)
    ax=axs[1]; order=sorted(cnt,key=lambda k:cnt[k])
    b=ax.barh(order,[cnt[k] for k in order],color=BLUE,hatch=["//" if i%2==0 else "" for i in range(len(order))],edgecolor="white")
    for r,k in zip(b,order): ax.text(cnt[k]+.3,r.get_y()+r.get_height()/2,str(cnt[k]),va="center",fontsize=8.5,fontweight="bold")
    ax.set_xlim(0,max(cnt.values())*1.2); ax.set_xlabel(f"지명이 나온 논문 {len(ag)}편 중 언급 편수"); ax.set_title("주제어",fontsize=8.5)
    fig.tight_layout(); save(fig,"그림9-6"); return len(oc),len(og),len(ag),cnt

if __name__=="__main__":
    fig91();fig92();fig93();fig94();fig95()
    print(fig96())

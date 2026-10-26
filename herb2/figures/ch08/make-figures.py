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




# 그림 8-1: 네 지역의 기록 규모
def fig81():
    fig,ax=plt.subplots(figsize=(6.8,3.2)); ax.set_xlim(0,14); ax.set_ylim(0,7); ax.axis("off")
    box(ax,.2,3.9,6.4,2.2,"북아메리카 원주민\n식물 4,000종 이상, 용도 44,000건\n(모어먼의 정리)","#bee3f8",8)
    box(ax,7.4,3.9,6.4,2.2,"멕시코 원주민 약초\n54종을 NF-κB 억제로 선별\n(1997)","#fefcbf",8)
    box(ax,.2,.6,6.4,2.2,"안데스·북부 페루\n약용 식물 510종, 2천 년의 전통\n(2006)","#c6f6d5",8)
    box(ax,7.4,.6,6.4,2.2,"브라질\n카팅가 48종, 약전 속 토착 식물의 감소\n(2006)","#fed7aa",8)
    ax.text(7,6.75,"이 장이 다루는 아메리카의 기록과 연구",ha="center",fontsize=10.5,fontweight="bold")
    save(fig,"그림8-1")

# 그림 8-2: 북부 페루 510종의 용도
def fig82():
    items=[("마술·의례",207),("호흡기",95),("요로",85),("여성 생식기 감염",66),("간",61),("염증",59),("위",51),("류머티즘",45)]
    wcsv("북부페루용도.csv",["use","species"],items)
    fig,ax=plt.subplots(figsize=(6.2,3.1)); k=[a for a,_ in items][::-1]; v=[b for _,b in items][::-1]
    cols=[BLUE]*7+[ORANGE]
    b=ax.barh(k,v,color=cols[::-1][::-1],hatch=["","","","","","","","xx"][::-1][::-1],edgecolor="white")
    # highlight top bar (last in reversed list)
    for r,x in zip(b,v): ax.text(x+3,r.get_y()+r.get_height()/2,f"{x}종",va="center",fontweight="bold",fontsize=8.5)
    b[-1].set_color(ORANGE); b[-1].set_hatch("xx")
    for r in b[:-1]: r.set_color(BLUE)
    ax.set_xlim(0,245); ax.set_xlabel("해당 용도에 쓰인 식물 종 수(전체 510종)")
    save(fig,"그림8-2")

# 그림 8-3: 시장과 혼합 처방
def fig83():
    wcsv("시장과혼합처방.csv",["item","value"],[("보고타 과",122),("보고타 속",319),("보고타 종",409),("페루 혼합 처방",974),("혼합에 쓰인 식물 종",330),("치료 대상 증상",164)])
    fig,axs=plt.subplots(1,2,figsize=(6.8,2.9))
    ax=axs[0]; ax.bar(["과","속","종"],[122,319,409],color=[GRAY,BLUE,GREEN],hatch=["//","",""],edgecolor="white",width=.6)
    for i,v in enumerate([122,319,409]): ax.text(i,v+8,str(v),ha="center",fontweight="bold")
    ax.set_ylim(0,470); ax.set_ylabel("개수"); ax.set_title("보고타 24개 시장에서 만난\n약용 식물(Bussmann 2018)",fontsize=8.5)
    ax=axs[1]; ax.bar(["혼합\n처방","쓰인\n식물 종","치료 대상\n증상"],[974,330,164],color=[ORANGE,GREEN,GRAY],hatch=["xx","","//"],edgecolor="white",width=.6)
    for i,v in enumerate([974,330,164]): ax.text(i,v+20,str(v),ha="center",fontweight="bold")
    ax.set_ylim(0,1100); ax.set_ylabel("개수"); ax.set_title("북부 페루의 약초 혼합 처방\n(Bussmann 2010)",fontsize=8.5)
    fig.tight_layout(); save(fig,"그림8-3")

# 그림 8-4: 항균 시험
def fig84():
    wcsv("항균시험.csv",["group","extracts","active"],[("전통 항균 용도",225,166),("전통 항균 용도 없음",300,96)])
    wcsv("항균세균별.csv",["bacteria","ethanolic_active"],[("황색포도상구균",193),("대장균",36),("장티푸스균",3),("녹농균",3)])
    fig,axs=plt.subplots(1,2,figsize=(6.8,3.0),gridspec_kw={"width_ratios":[1,1.1]})
    ax=axs[0]
    for y,(t,n,a) in enumerate([("전통 항균 용도\n없는 식물",300,96),("전통 항균 용도\n있는 식물",225,166)]):
        p=a/n*100; ax.barh(y,p,color=GREEN if y else GRAY,hatch="" if y else "//",edgecolor="white",height=.5); ax.barh(y,100-p,left=p,color="#e2e8f0",edgecolor="white",height=.5)
        ax.text(p/2,y,f"{p:.1f}%\n({a}/{n})",ha="center",va="center",color="white" if y else "black",fontweight="bold",fontsize=8)
    ax.set_yticks([0,1]); ax.set_yticklabels(["전통 용도\n없음","전통 용도\n있음"],fontsize=8); ax.set_xlim(0,100); ax.set_xlabel("1종 이상 세균에 활성을 보인 추출물(%)")
    ax.set_title("전통 용도별 활성 비율",fontsize=8.5)
    ax=axs[1]; k=["황색\n포도상구균","대장균","장티푸스균","녹농균"]; v=[193,36,3,3]
    ax.bar(k,v,color=[BLUE,ORANGE,GRAY,GRAY],hatch=["","xx","//","//"],edgecolor="white",width=.6)
    for i,x in enumerate(v): ax.text(i,x+4,str(x),ha="center",fontweight="bold")
    ax.set_ylim(0,225); ax.set_ylabel("활성을 보인 에탄올 추출물(개)"); ax.set_title("세균별 활성(에탄올 추출물)",fontsize=8.5); ax.tick_params(axis="x",labelsize=7.5)
    fig.tight_layout(); save(fig,"그림8-4")

# 그림 8-5: NF-kB 선별
def fig85():
    fig,ax=plt.subplots(figsize=(6.8,2.9)); ax.set_xlim(0,15); ax.set_ylim(0,6); ax.axis("off")
    box(ax,.1,2.0,2.8,2.0,"멕시코 원주민\n약초 54종\n(에탄올 잎 추출물)","#edf2f7",7.5,True)
    box(ax,3.7,2.0,3.0,2.0,"NF-κB 활성\n억제 시험\n(겔 이동 분석)","#fefcbf",7.5)
    box(ax,7.5,3.4,3.4,1.8,"3종 추출물이\n25 μg/mL까지 억제","#c6f6d5",7.5)
    box(ax,7.5,.6,3.4,1.8,"공통점: 세스퀴테르펜\n락톤이 풍부","#fed7aa",7.5)
    box(ax,11.6,2.0,3.2,2.0,"이소헬레닌·\n파르테놀리드\n5 μM에서 완전 억제","#bee3f8",7.5,True)
    arrow(ax,2.9,3.0,3.7,3.0); arrow(ax,6.7,3.3,7.5,4.2); arrow(ax,6.7,2.7,7.5,1.6); arrow(ax,10.9,4.0,11.6,3.6); arrow(ax,10.9,1.6,11.6,2.4)
    ax.text(7.5,5.65,"약초 선별에서 활성 성분 후보까지(Bork 1997)",ha="center",fontsize=10,fontweight="bold")
    save(fig,"그림8-5")

# 그림 8-6: 브라질 항암 후보 탐색
def fig86():
    fig,ax=plt.subplots(figsize=(6.8,3.0)); ax.set_xlim(0,15); ax.set_ylim(0,6.2); ax.axis("off")
    labels=["남아메리카 약용\n식물 수집\n(민족약리·화학계통·\n생태 정보로 선택)","건조 후 유기용매,\n이어서 증류수로\n추출","50 μg/mL에서\n세포 1종 증식 억제\n(50% 이상)","미국 NCI의\n질병 지향 선별","생물활성 유도\n분리·구조 결정\n작용 기전 연구"]
    cs=["#c6f6d5","#fefcbf","#fed7aa","#bee3f8","#e9d8fd"]
    for i,(t,c) in enumerate(zip(labels,cs)):
        box(ax,.1+i*3.0,1.4,2.5,2.9,t,c,6.6)
        if i<4: arrow(ax,2.6+i*3.0,2.85,3.1+i*3.0,2.85)
    ax.text(7.5,5.6,"브라질의 항암 후보 탐색 경로(Mans 2000)",ha="center",fontsize=10,fontweight="bold")
    save(fig,"그림8-6")

GEO=r"peru|amazon|andean|andes|brazil|mexic|colombia|ecuador|bolivia|argentin|chile|venezuel|north america|native american|first nations|american indian|latin america|caribbean|united states|canad|cree\b|navajo"
TOP=[("브라질",r"brazil"),("페루",r"peru"),("보전·재배",r"conserv|cultivat"),("항균·항미생물",r"antibacterial|antimicrobial"),("멕시코",r"mexic"),("민족식물학",r"ethnobotan"),("시장·판매",r"market"),("항암",r"cancer|antiproliferative|antitumou?r")]
def fig87():
    am=[r for r in rows() if "americas/" in (r["tags"] or "")]
    g=[r for r in am if re.search(GEO,(r["title"] or "")+" "+(r["abstract"] or ""),re.I)]
    cnt={n:sum(1 for r in g if re.search(p,(r["title"] or "")+" "+(r["abstract"] or ""),re.I)) for n,p in TOP}
    wcsv("아메리카말뭉치.csv",["item","papers"],[("아메리카 태그 논문",len(am)),("아메리카 지명이 제목·초록에 나온 논문",len(g))]+list(cnt.items()))
    fig,axs=plt.subplots(1,2,figsize=(6.8,3.1),gridspec_kw={"width_ratios":[.8,1.4]})
    ax=axs[0]; ax.bar(["아메리카\n태그","지명이\n나온 논문"],[len(am),len(g)],color=[GRAY,BLUE],hatch=["//",""],edgecolor="white",width=.55)
    for i,v in enumerate([len(am),len(g)]): ax.text(i,v+15,f"{v:,}",ha="center",fontweight="bold")
    ax.set_ylim(0,1050); ax.set_ylabel("논문 수(편)"); ax.set_title("태그와 실제 지명",fontsize=8.5)
    ax=axs[1]; order=sorted(cnt,key=lambda k:cnt[k])
    b=ax.barh(order,[cnt[k] for k in order],color=BLUE,hatch=["//" if i%2==0 else "" for i in range(len(order))],edgecolor="white")
    for r,k in zip(b,order): ax.text(cnt[k]+.6,r.get_y()+r.get_height()/2,str(cnt[k]),va="center",fontsize=8.5,fontweight="bold")
    ax.set_xlim(0,max(cnt.values())*1.2); ax.set_xlabel(f"지명이 나온 논문 {len(g)}편 중 언급 편수"); ax.set_title("주제어",fontsize=8.5)
    fig.tight_layout(); save(fig,"그림8-7"); return len(am),len(g),cnt

if __name__=="__main__":
    fig81();fig82();fig83();fig84();fig85();fig86()
    print(fig87())

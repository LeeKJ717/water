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




# 그림 7-1: 두 의료 체계 사이의 환자
def fig71():
    fig,ax=plt.subplots(figsize=(6.8,3.2)); ax.set_xlim(0,14); ax.set_ylim(0,7); ax.axis("off")
    box(ax,5.2,2.6,3.6,1.8,"환자와 가족","#edf2f7",9,True)
    box(ax,.2,4.6,4.4,1.8,"전통 치료사\n식물·의례·가족 유산","#c6f6d5",8)
    box(ax,9.4,4.6,4.4,1.8,"보건소·병원\n의사·약","#bee3f8",8)
    box(ax,.2,.3,4.4,1.5,"약초 시장·마당의 식물","#fefcbf",8)
    box(ax,9.4,.3,4.4,1.5,"항레트로바이러스제 등","#fed7aa",8)
    arrow(ax,5.5,4.4,4.6,5.2); arrow(ax,8.5,4.4,9.4,5.2); arrow(ax,5.5,2.6,4.6,1.3); arrow(ax,8.5,2.6,9.4,1.3)
    ax.text(7,5.7,"의료진 90%는\n환자의 약초 복용을\n모름(남아공 618명)",ha="center",va="center",fontsize=7.5,color="#c53030",fontweight="bold")
    ax.text(7,6.75,"환자는 두 체계를 오간다(개념도)",ha="center",fontsize=10.5,fontweight="bold")
    save(fig,"그림7-1")

# 그림 7-2: 두 지역 조사
def fig72():
    wcsv("두지역조사.csv",["item","value"],[("에티오피아 식물 종",230),("야생 채집 비율(%)",90.4),("삼림 파괴 위협(%)",90),("농지 확장 위협(%)",85),("화재 위협(%)",53),("짐바브웨 식물 종",93),("관목(%)",38),("교목(%)",38),("초본(%)",21),("덩굴(%)",3)])
    fig,axs=plt.subplots(1,2,figsize=(6.8,3.0))
    ax=axs[0]; k=["삼림 파괴","농지 확장","화재"]; v=[90,85,53]
    ax.barh(k[::-1],v[::-1],color=ORANGE,hatch=["","//",""],edgecolor="white")
    for i,x in enumerate(v[::-1]): ax.text(x+2,i,f"{x}%",va="center",fontweight="bold")
    ax.set_xlim(0,110); ax.set_xlabel("위협으로 꼽은 응답(%)"); ax.set_title("에티오피아 마나 앙게투\n식물 230종의 위협 요인",fontsize=8.5)
    ax=axs[1]; k=["관목","교목","초본","덩굴"]; v=[38,38,21,3]
    ax.bar(k,v,color=[GREEN,GREEN,BLUE,GRAY],hatch=["","","//","xx"],edgecolor="white",width=.6)
    for i,x in enumerate(v): ax.text(i,x+1,f"{x}%",ha="center",fontweight="bold")
    ax.set_ylim(0,46); ax.set_ylabel("식물 종 비율(%)"); ax.set_title("짐바브웨 중남부 93종의\n생활형",fontsize=8.5)
    fig.tight_layout(); save(fig,"그림7-2")

# 그림 7-3: 말라리아
def fig73():
    wcsv("말라리아.csv",["item","value"],[("치료사 수(명)",14),("식물 종(개)",28),("뿌리 사용(%)",55.3),("병원 의뢰 치료사(%)",25),("알칼로이드·테르페노이드 화합물(개)",171),("기타 화합물(개)",107)])
    fig,axs=plt.subplots(1,2,figsize=(6.8,2.8),gridspec_kw={"width_ratios":[1.3,1]})
    ax=axs[0]
    for y,(t,a) in enumerate([("치료 실패 시 병원으로\n보내는 치료사",25),("사용 부위가 뿌리인\n비율",55.3)]):
        ax.barh(y,a,color=GREEN,edgecolor="white"); ax.barh(y,100-a,left=a,color="#cbd5e0",edgecolor="white")
        ax.text(a/2,y,f"{a}%",ha="center",va="center",color="white",fontweight="bold")
    ax.set_yticks([0,1]); ax.set_yticklabels(["병원 의뢰","뿌리 사용"],fontsize=8.5); ax.set_xlim(0,100); ax.set_xlabel("%")
    ax.set_title("짐바브웨 치프잉게 치료사 14명",fontsize=8.5)
    ax=axs[1]; ax.bar(["알칼로이드·\n테르페노이드","기타 계열"],[171,107],color=[BLUE,GRAY],hatch=["","//"],edgecolor="white",width=.55)
    for i,v in enumerate([171,107]): ax.text(i,v+4,f"{v}",ha="center",fontweight="bold")
    ax.set_ylim(0,205); ax.set_ylabel("항말라리아 활성 화합물(개)"); ax.set_title("아프리카 식물 유래\n화합물 278개",fontsize=8.5)
    fig.tight_layout(); save(fig,"그림7-3")

# 그림 7-4: HIV와 전통 치료
def fig74():
    wcsv("HIV전통치료.csv",["item","value"],[("TCAM 사용(%)",51.3),("약초 단독(%)",29.6),("의료진이 모름(%)",90),("치료사 조사(명)",192),("HIV 치료 주장(명)",110)])
    fig,axs=plt.subplots(1,2,figsize=(6.8,2.9),gridspec_kw={"width_ratios":[1.2,1]})
    ax=axs[0]; k=["TCAM 사용","약초 사용","의료진이\n약초 복용을 모름"]; v=[51.3,29.6,90]
    ax.bar(k,v,color=[BLUE,GREEN,ORANGE],hatch=["","//","xx"],edgecolor="white",width=.6)
    for i,x in enumerate(v): ax.text(i,x+2,f"{x}%",ha="center",fontweight="bold")
    ax.set_ylim(0,105); ax.set_ylabel("%"); ax.set_title("남아공 HIV 환자 618명\n(KwaZulu-Natal)",fontsize=8.5)
    ax=axs[1]; ax.bar(["조사한\n치료사","HIV 치료를\n주장한 치료사"],[192,110],color=[GRAY,GREEN],hatch=["","//"],edgecolor="white",width=.55)
    for i,x in enumerate([192,110]): ax.text(i,x+4,f"{x}명",ha="center",fontweight="bold")
    ax.set_ylim(0,225); ax.set_ylabel("치료사 수(명)"); ax.set_title("탄자니아 아루샤·다르에스살람",fontsize=8.5)
    fig.tight_layout(); save(fig,"그림7-4")

# 그림 7-5: 사더랜디아 시험 둘
def fig75():
    wcsv("사더랜디아.csv",["trial","group","n"],[("2007 건강인","사더랜디아",12),("2007 건강인","위약",13),("2015 HIV","사더랜디아",54),("2015 HIV","위약",53)])
    fig,axs=plt.subplots(1,2,figsize=(6.8,2.9),gridspec_kw={"width_ratios":[1.3,1]})
    ax=axs[0]
    for y,(t,a,b,d) in enumerate([("2007 건강인\n(3개월, 800 mg/일)",12,13,""),("2015 HIV 감염인\n(24주, 1,200 mg 2회/일 군 분석)",54,53,"")][::-1]):
        ax.barh(y,a,color=GREEN,edgecolor="white",height=.5); ax.barh(y,b,left=a,color=GRAY,hatch="//",edgecolor="white",height=.5)
        ax.text(a/2,y,f"{a}명",ha="center",va="center",color="white",fontweight="bold",fontsize=8); ax.text(a+b/2,y,f"{b}명",ha="center",va="center",color="black",fontweight="bold",fontsize=8)
    ax.set_yticks([0,1]); ax.set_yticklabels(["2015 HIV 감염인\n(24주)","2007 건강인\n(3개월)"],fontsize=8)
    ax.set_xlim(0,120); ax.set_xlabel("참가자(명): 녹색=사더랜디아, 회색=위약"); ax.set_title("두 시험의 규모",fontsize=8.5)
    ax=axs[1]; ax.bar(["위약군","사더랜디아군"],[5.0,9.0],color=[BLUE,ORANGE],hatch=["","xx"],edgecolor="white",width=.55)
    for i,v in enumerate([5.0,9.0]): ax.text(i,v+.3,f"{v}일",ha="center",fontweight="bold")
    ax.set_ylim(0,11.5); ax.set_ylabel("감염 관련 사건 일수(평균)"); ax.set_title("HIV 시험의 감염 부담\n(P=0.045)",fontsize=8.5)
    fig.tight_layout(); save(fig,"그림7-5")

# 그림 7-6: 탄자니아 전통 의약 이용
def fig76():
    items=[("지난 1년 사용",56),("이용자를 아는 사람",68),("증상 완화 목적",42),("만성 질환",15),("생식 건강",11),("말라리아·열병",11)]
    wcsv("탄자니아이용.csv",["item","percent"],items)
    fig,ax=plt.subplots(figsize=(6.2,3.0)); k=[a for a,_ in items][::-1]; v=[b for _,b in items][::-1]
    b=ax.barh(k,v,color=[BLUE if i>=2 else GREEN for i in range(6)][::-1],hatch=["" if i>=2 else "//" for i in range(6)][::-1],edgecolor="white")
    for r,x in zip(b,v): ax.text(x+1,r.get_y()+r.get_height()/2,f"{x}%",va="center",fontweight="bold")
    ax.set_xlim(0,80); ax.set_xlabel("응답자 비율(%, 무작위 성인 655명)")
    save(fig,"그림7-6")

TOP=[("독성·안전",r"toxic|safety"),("민족식물학 조사",r"ethnobotan"),("보전·지속가능성",r"conserv|threat|sustainab"),("전통 치료사",r"traditional (healer|health practi)|herbalist"),("말라리아",r"malaria|plasmodium"),("당뇨",r"diabet"),("HIV·에이즈",r"HIV|AIDS"),("임상시험",r"randomi[sz]ed|clinical trial"),("모링가",r"moringa")]
def fig77():
    af=[r for r in rows() if "africa/" in (r["tags"] or "")]
    cnt={n:sum(1 for r in af if re.search(p,(r["title"] or "")+" "+(r["abstract"] or ""),re.I)) for n,p in TOP}
    wcsv("아프리카주제별논문수.csv",["topic","papers"],cnt.items())
    order=sorted(cnt,key=lambda k:cnt[k])
    fig,ax=plt.subplots(figsize=(6.2,3.3))
    b=ax.barh(order,[cnt[k] for k in order],color=BLUE,hatch=["//" if i%2==0 else "" for i in range(len(order))],edgecolor="white")
    for r,k in zip(b,order): ax.text(cnt[k]+3,r.get_y()+r.get_height()/2,f"{cnt[k]:,}",va="center",fontsize=9,fontweight="bold")
    ax.set_xlim(0,max(cnt.values())*1.15); ax.set_xlabel(f"제목·초록에 언급된 논문 수(편, 아프리카 논문 {len(af):,}편 중)")
    save(fig,"그림7-7"); return cnt,len(af)

if __name__=="__main__":
    fig71();fig72();fig73();fig74();fig75();fig76()
    print(fig77())

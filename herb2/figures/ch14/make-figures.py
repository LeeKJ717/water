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

# 그림 14-1: 책이 걸어온 길
def fig141():
    fig,ax=plt.subplots(figsize=(7.4,3.6)); ax.set_xlim(0,12); ax.set_ylim(0,10); ax.axis("off")
    parts=[("1부 뿌리","1~2장\n기원·식물화학","#ebf8ff"),("2부 아시아","3~4장\n동아시아·남아시아","#fefcbf"),("3부 서쪽과 남쪽","5~7장\n중동·유럽·아프리카","#c6f6d5"),("4부 신대륙과 바다","8~9장\n아메리카·오세아니아","#fed7d7"),("5부 과학의 눈","10~14장\n약리·임상·안전\n표준·오늘","#e9d8fd")]
    for i,(t,d,c) in enumerate(parts):
        x=0.2+i*2.35
        box(ax,x,5.4,2.1,2.8,"",c)
        lab(ax,x+1.05,7.5,t,fs=8,fontweight="bold")
        lab(ax,x+1.05,6.2,d,fs=7.5)
        if i<4: arrow(ax,x+2.12,6.8,x+2.4,6.8)
    arrow(ax,10.9,5.3,9.5,4.2)
    box(ax,2.2,2.2,7.6,1.9,"14장 오늘의 허브와 내일의 과제","#fbd38d",fs=10,bold=True)
    lab(ax,6,1.2,"기원에서 증거·안전·표준까지 걸어온 길 위에서 앞으로의 과제를 가늠한다",fs=8)
    save(fig,"그림14-1")

# 그림 14-2: 연도별 논문 수
def fig142():
    R=rows(); yc=collections.Counter(int(r["year"]) for r in R if r.get("year") and int(r["year"])>=1995)
    ys=list(range(1995,2026)); vs=[yc.get(y,0) for y in ys]
    wcsv("연도별논문수.csv",["연도","편수"],list(zip(ys,vs)))
    fig,ax=plt.subplots(figsize=(6.6,3.2))
    ax.bar(ys,vs,color=BLUE,hatch="//",edgecolor="white")
    ax.set_xlabel("출판 연도"); ax.set_ylabel("말뭉치 논문 수(편)")
    ax.annotate("최대 622편(2021)",xy=(2021,622),xytext=(2005,560),arrowprops=dict(arrowstyle="-|>"),fontsize=8)
    fig.tight_layout(); save(fig,"그림14-2")

# 그림 14-3: 주제 용어 비율의 추이
def fig143():
    R=rows()
    bins=[("~2004",0,2004),("2005~09",2005,2009),("2010~14",2010,2014),("2015~19",2015,2019),("2020~",2020,2026)]
    terms=[("네트워크 약리학","network pharmacology","o","-"),("인공지능·기계학습","artificial intelligence|machine learning|deep learning","s","--"),("대사체학","metabolomic","^","-."),("합성생물학·대사공학","synthetic biology|metabolic engineering|heterologous","D",":"),("보전·남획","conservation|endangered|overharvest|over-?exploit|threatened","v","-")]
    out=[]; fig,ax=plt.subplots(figsize=(6.6,3.6)); cols=[BLUE,RED,GREEN,ORANGE,GRAY]
    for (k,p,m,ls),c in zip(terms,cols):
        ys=[]
        for _,a,b in bins:
            S=[r for r in R if r.get("year") and a<=int(r["year"])<=b]
            n=sum(1 for r in S if re.search(p,r["title"]+" "+(r["abstract"] or ""),re.I)); ys.append(round(100*n/max(1,len(S)),1)); out.append((k,_,len(S),n,ys[-1]))
        ax.plot([b[0] for b in bins],ys,marker=m,ls=ls,color=c,label=k,lw=1.8)
    wcsv("주제용어추이.csv",["용어","기간","기간내논문수","언급논문수","비율(%)"],out)
    ax.set_ylabel("해당 기간 논문 중 언급 비율(%)"); ax.legend(fontsize=7.5,loc="upper center",bbox_to_anchor=(0.5,-0.14),ncol=3,frameon=False)
    fig.tight_layout(); save(fig,"그림14-3"); return out

# 그림 14-4: 네트워크 약리학에서 인공지능까지
def fig144():
    fig,ax=plt.subplots(figsize=(7.4,3.2)); ax.set_xlim(0,12); ax.set_ylim(0,10); ax.axis("off")
    st=["약초 혼합물\n(수백 성분)","성분–표적\n네트워크","대사체학\n전체 프로필","AI가 패턴을\n찾아 예측","실험·임상으로\n검증"]
    cs=["#ebf8ff","#fefcbf","#c6f6d5","#e9d8fd","#fed7d7"]
    for i,(s,c) in enumerate(zip(st,cs)):
        x=0.2+i*2.35; box(ax,x,4.4,2.1,2.8,s,c,fs=8.5,bold=(i==4))
        if i<4: arrow(ax,x+2.12,5.8,x+2.4,5.8)
    lab(ax,6,2.4,"예측은 가설이다 — 마지막 칸을 거치지 않으면 근거가 되지 못한다",fs=9,fontweight="bold",bbox=dict(fc="#edf2f7",ec="#2d3748",pad=4))
    save(fig,"그림14-4")

# 그림 14-5: 식물에서 미생물 공장으로
def fig145():
    fig,ax=plt.subplots(figsize=(7.4,3.4)); ax.set_xlim(0,12); ax.set_ylim(0,10); ax.axis("off")
    st=[("식물\n(함량이 낮음)","#c6f6d5"),("생합성 경로\n규명","#ebf8ff"),("경로를 미생물\n숙주에 이식","#fefcbf"),("효소 개량\n(빠진 단계 보완)","#e9d8fd"),("의약품·원료\n생산","#fed7d7")]
    for i,(s,c) in enumerate(st):
        x=0.2+i*2.35; box(ax,x,5.0,2.1,2.8,s,c,fs=8.5)
        if i<4: arrow(ax,x+2.12,6.4,x+2.4,6.4)
    box(ax,0.2,1.2,5.2,2.0,"식물 쪽: 조직배양·재배·보전","#f7fafc",fs=8.5)
    box(ax,6.6,1.2,5.2,2.0,"공장 쪽: 대사공학·합성생물학","#f7fafc",fs=8.5)
    save(fig,"그림14-5")

# 그림 14-6: 위협받는 약용 식물의 위급 단계
def fig146():
    d=[("위급(CR)",22),("위기(EN)",16),("취약(VU)",27)]
    wcsv("히말라야위협식물.csv",["단계","위협 약용식물 중 비율(%)"],d)
    fig,ax=plt.subplots(figsize=(6.2,3.0))
    ax.bar([k for k,_ in d],[v for _,v in d],color=[RED,ORANGE,BLUE],hatch=["//","xx","\\\\"],edgecolor="white",width=0.55)
    for i,(k,v) in enumerate(d): ax.text(i,v+0.8,f"{v}%",ha="center",fontsize=10,fontweight="bold")
    ax.set_ylim(0,34); ax.set_ylabel("위협받는 약용 식물 60종 중 비율(%)")
    fig.tight_layout(); save(fig,"그림14-6")

# 그림 14-7: 내일의 과제 지도
def fig147():
    fig,ax=plt.subplots(figsize=(7.4,3.8)); ax.set_xlim(0,12); ax.set_ylim(0,10); ax.axis("off")
    rows_=[("증거","11장","시험 3,137편 중\n인정된 무작위 6.8%\n(Wu et al., 2009)","엄밀한 설계와 보고"),
           ("안전","12장","상호작용 보고\n68.5% 평가 불가\n(Fugh-Berman\n& Ernst, 2001)","약물감시와 인과성 평가"),
           ("품질","13장","약재 1,773개 중\n30.51% 금속 한도 초과\n(Luo et al., 2021)","표준화·약전·종 확인"),
           ("보전","14장","위협 약용식물 60종\n위급·위기·취약 65%\n(Kala, 2005)","보전과 지속 가능한 공급")]
    for j,(h,c,f,t) in enumerate(rows_):
        x=0.2+j*2.95
        ax.add_patch(FancyBboxPatch((x,7.6),2.7,1.6,boxstyle="round,pad=0.02,rounding_size=0.1",fc=[BLUE,RED,GREEN,ORANGE][j],ec="#2d3748",hatch=["//","xx","\\\\","++"][j],alpha=0.9))
        lab(ax,x+1.35,8.4,f"{h} ({c})",fs=9,fontweight="bold",color="white",bbox=dict(fc="#2d3748",ec="none",pad=2))
        arrow(ax,x+1.35,7.5,x+1.35,6.6)
        box(ax,x,3.9,2.7,2.6,f,"white",fs=7.8)
        arrow(ax,x+1.35,3.8,x+1.35,2.9)
        box(ax,x,1.0,2.7,1.9,t,"#f7fafc",fs=8,bold=True)
    save(fig,"그림14-7")

if __name__=="__main__":
    fig141(); fig142(); o=fig143(); fig144(); fig145(); fig146(); fig147(); print(o)

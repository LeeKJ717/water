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

# 그림 11-1: 증거의 사다리 (개념도)
def fig111():
    fig,ax=plt.subplots(figsize=(6.4,3.6)); ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis("off")
    lv=[("체계적 고찰·메타분석",GREEN,"//"),("무작위 대조 임상시험",BLUE,"\\\\"),("코호트·환자-대조 연구",ORANGE,"xx"),("증례 보고·전통 용례·전문가 의견",GRAY,"..")]
    for i,(t,c,h) in enumerate(lv):
        w=2.6+i*1.9; x=(10-w)/2; y=7.6-i*2.3
        ax.add_patch(FancyBboxPatch((x,y),w,1.9,boxstyle="round,pad=0.02,rounding_size=0.1",fc=c,ec="#2d3748",lw=1,alpha=0.85,hatch=h))
        ax.text(5,y+0.95,t,ha="center",va="center",fontsize=8.5,fontweight="bold",color="white",bbox=dict(fc="#2d3748",ec="none",pad=2,alpha=0.85))
    ax.annotate("",xy=(9.6,9.2),xytext=(9.6,0.8),arrowprops=dict(arrowstyle="-|>",lw=1.4,color="#2d3748"))
    ax.text(9.75,5,"증거의 수준 높음",rotation=90,va="center",ha="left",fontsize=8)
    save(fig,"그림11-1")

# 그림 11-2: 말뭉치 임상 논문
def fig112():
    R=rows(); cl=[r for r in R if "global/clinical" in (r["tags"] or "")]
    yc=collections.Counter(int(r["year"]) for r in cl if r["year"])
    ys=list(range(2000,2026))
    kw=[("무작위(randomized)","randomi[sz]ed"),("체계적 고찰","systematic review"),("플라세보","placebo"),("이중맹검","double-blind"),("코크란","Cochrane"),("메타분석","meta-analysis"),("CONSORT","CONSORT"),("비뚤림 위험","risk of bias")]
    kc=[(n,sum(1 for r in R if re.search(p,(r["title"] or "")+" "+(r["abstract"] or ""),re.I))) for n,p in kw]
    kc.sort(key=lambda x:-x[1])
    wcsv("임상논문연도별.csv",["연도","편수"],[(y,yc.get(y,0)) for y in ys])
    wcsv("임상키워드언급.csv",["키워드","편수"],kc)
    fig,axs=plt.subplots(1,2,figsize=(7.2,3.2),gridspec_kw={"width_ratios":[1.3,1]})
    axs[0].bar(ys,[yc.get(y,0) for y in ys],color=BLUE); axs[0].set_xlabel("연도"); axs[0].set_ylabel("논문 수(편)"); axs[0].set_title("임상 태그 논문",fontsize=9)
    axs[0].set_xticks(range(2000,2026,5))
    hs=["//","\\\\","xx","..","++","oo","--","**"]
    axs[1].barh([k for k,_ in kc][::-1],[v for _,v in kc][::-1],color=ORANGE,hatch="//",edgecolor="white")
    for i,(k,v) in enumerate(kc[::-1]): axs[1].text(v+4,i,str(v),va="center",fontsize=8)
    axs[1].set_xlabel("제목·초록에서 언급된 논문 수"); axs[1].set_title("방법론 용어",fontsize=9); axs[1].set_xlim(0,330)
    fig.tight_layout(); save(fig,"그림11-2"); return len(cl),kc

# 그림 11-3: Wilt 1998
def fig113():
    wcsv("톱야자메타분석.csv",["항목","값"],[("무작위 시험 수",18),("대상 남성 수",2939),("배정 은닉 적절",9),("이중맹검",16),("평균 기간(주)",9),("발기부전 피나스테리드(%)",4.9),("발기부전 톱야자(%)",1.1)])
    fig,axs=plt.subplots(1,2,figsize=(7,3.1),gridspec_kw={"width_ratios":[1.4,1]})
    ax=axs[0]; labs=["이중맹검","배정 은닉 적절"]; yes=[16,9]
    ax.barh(labs,yes,color=GREEN,hatch="//",edgecolor="white",label="해당")
    ax.barh(labs,[18-y for y in yes],left=yes,color="#e2e8f0",edgecolor="#2d3748",label="그 외")
    for i,y in enumerate(yes): ax.text(y/2,i,f"{y}편",ha="center",va="center",color="white",fontweight="bold",fontsize=9)
    ax.set_xlim(0,18); ax.set_xlabel("무작위 시험 18편 중"); ax.legend(fontsize=7,loc="upper center",bbox_to_anchor=(0.5,-0.28),ncol=2,frameon=False); ax.set_title("시험의 방법론",fontsize=9)
    ax=axs[1]; ax.bar(["톱야자","피나스테리드"],[1.1,4.9],color=[GREEN,RED],hatch="//",edgecolor="white")
    for i,v in enumerate([1.1,4.9]): ax.text(i,v+0.1,f"{v}%",ha="center",fontsize=9,fontweight="bold")
    ax.set_ylim(0,6); ax.set_ylabel("발기부전 발생(%)"); ax.set_title("이상반응 비교",fontsize=9)
    fig.tight_layout(); save(fig,"그림11-3")

# 그림 11-4: CONSORT 확장
def fig114():
    wcsv("CONSORT확장.csv",["지침","전체 항목","보완된 항목"],[("CONSORT 약초 확장(2006)",22,9),("CONSORT-CHM 처방 확장(2017)",25,7)])
    fig,ax=plt.subplots(figsize=(6.4,2.6))
    names=["약초 중재 확장\n(Gagnier 2006)","중의 처방 확장\n(Cheng 2017)"]; tot=[22,25]; el=[9,7]
    ax.barh(names,el,color=ORANGE,hatch="xx",edgecolor="white",label="약초에 맞게 보완한 항목")
    ax.barh(names,[t-e for t,e in zip(tot,el)],left=el,color="#e2e8f0",edgecolor="#2d3748",label="기존 CONSORT 그대로")
    for i,(t,e) in enumerate(zip(tot,el)): ax.text(e/2,i,f"{e}",ha="center",va="center",color="black",fontweight="bold",fontsize=10,bbox=dict(fc="white",ec="none",pad=2)); ax.text(t+0.3,i,f"전체 {t}항목",va="center",fontsize=8)
    ax.set_xlim(0,31); ax.set_xlabel("CONSORT 점검표 항목 수"); ax.legend(fontsize=7,frameon=False,loc="upper center",bbox_to_anchor=(0.5,-0.28),ncol=2)
    fig.tight_layout(); save(fig,"그림11-4")

# 그림 11-5: Wu 2009 깔때기
def fig115():
    st=[("CNKI 검색 논문",37313),("무작위로 보이는 시험",3137),("저자 면담 완료",2235),("무작위 방법이 인정된 시험",207)]
    wcsv("중국무작위시험진위.csv",["단계","편수"],st)
    fig,ax=plt.subplots(figsize=(6.4,3.3)); ax.set_xlim(0,10); ax.set_ylim(0,len(st)*1.3); ax.axis("off")
    cols=["#bee3f8","#fefcbf","#fed7aa","#c6f6d5"]; hs=["","//","xx","\\\\"]
    for i,(n,v) in enumerate(st):
        w=max(1.6,8*np.log10(v)/np.log10(37313)); y=(len(st)-1-i)*1.3
        ax.add_patch(FancyBboxPatch(((10-w)/2,y),w,1.0,boxstyle="round,pad=0.02,rounding_size=0.1",fc=cols[i],ec="#2d3748",hatch=hs[i]))
        ax.text(5,y+0.5,f"{n}  {v:,}편",ha="center",va="center",fontsize=8.5,fontweight="bold",bbox=dict(fc="white",ec="none",pad=1.5,alpha=0.85))
    ax.text(5,-0.8,"면담한 2,235편 중 207편(6.8%, 95% CI 5.9–7.7)만 인정  ·  폭은 로그 눈금",ha="center",fontsize=8,color=RED)
    save(fig,"그림11-5")

# 그림 11-6: Zhong 2010
def fig116():
    items=["CONSORT 항목\n보고율","피험자 동의서\n보고","윤리위원회\n승인 보고"]; ch=[39.7,33.02,10.49]; nc=[50.2,92.16,82.35]
    wcsv("중국대비중국외보고.csv",["항목","중국 시험(324편)","중국 외 시험(51편)"],list(zip(items,ch,nc)))
    fig,ax=plt.subplots(figsize=(6.4,3.2)); x=np.arange(3); w=0.36
    ax.bar(x-w/2,ch,w,color=RED,hatch="//",edgecolor="white",label="중국 시험 324편"); ax.bar(x+w/2,nc,w,color=BLUE,hatch="xx",edgecolor="white",label="중국 외 시험 51편")
    for i in range(3): ax.text(i-w/2,ch[i]+1.5,f"{ch[i]:.1f}",ha="center",fontsize=8); ax.text(i+w/2,nc[i]+1.5,f"{nc[i]:.1f}",ha="center",fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels(items); ax.set_ylabel("보고한 시험 비율(%)"); ax.set_ylim(0,110); ax.legend(fontsize=8,frameon=False)
    fig.tight_layout(); save(fig,"그림11-6")

# 그림 11-7: 양성 결과 사례
def fig117():
    wcsv("양성결과사례.csv",["시험","지표","약초군","대조군"],[("기력강심(Qili Qiangxin) 심부전(n=512)","NT-proBNP 30%이상 감소(%)",47.95,31.98),("커큐민 당뇨 전단계(n=240)","9개월 내 제2형 당뇨 진단(%)",0,16.4)])
    fig,axs=plt.subplots(1,2,figsize=(7,3.2))
    for ax,(t,v,yl,ylim) in zip(axs,[("기력강심 캡슐\n만성 심부전(n=512)",(47.95,31.98),"NT-proBNP 30% 이상 감소(%)",60),("커큐민\n당뇨 전단계(n=240)",(0,16.4),"9개월 내 제2형 당뇨 진단(%)",22)]):
        ax.bar(["시험약","위약"],v,color=[GREEN,GRAY],hatch="//",edgecolor="white")
        for i,x in enumerate(v): ax.text(i,x+ylim*0.02,f"{x:g}%",ha="center",fontweight="bold",fontsize=9)
        ax.set_ylim(0,ylim); ax.set_title(t,fontsize=9); ax.set_ylabel(yl,fontsize=8)
    fig.tight_layout(); save(fig,"그림11-7")

# 그림 11-8: 판정 사다리
def fig118():
    cols=[("단기 효능 보고",GREEN,"//",["카바: 불안(단기)","톱야자: 전립선비대 증상(단기)","세인트존스워트: 경증~중등도 우울"]),
          ("일부 효과·증거 불충분",ORANGE,"xx",["은행잎: 치매·간헐 파행에 일부 효과","에키네시아: 상기도 감염, 완전히 설득적이지 않음"]),
          ("근거 의문·불인정",RED,"\\\\",["은행잎: 기억력 감퇴·이명은 의문","인삼: 어떤 질환에도 효능 불인정"])]
    wcsv("에른스트판정.csv",["판정","약초와 질환"],[(c[0],"; ".join(c[3])) for c in cols])
    fig,ax=plt.subplots(figsize=(7,3.6)); ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis("off")
    for i,(t,c,h,items) in enumerate(cols):
        x=0.2+i*3.3
        ax.add_patch(FancyBboxPatch((x,8.0),3.1,1.5,boxstyle="round,pad=0.02,rounding_size=0.1",fc=c,ec="#2d3748",hatch=h,alpha=0.9))
        ax.text(x+1.55,8.75,t,ha="center",va="center",fontsize=8.5,fontweight="bold",color="white",bbox=dict(fc="#2d3748",ec="none",pad=2))
        for j,it in enumerate(items):
            import textwrap
            y=6.3-j*2.4
            ax.add_patch(FancyBboxPatch((x,y-0.6),3.1,1.9,boxstyle="round,pad=0.02,rounding_size=0.1",fc="white",ec="#2d3748"))
            ax.text(x+1.55,y+0.35,"\n".join(textwrap.wrap(it,15)),ha="center",va="center",fontsize=7.5)
    ax.text(5,0.2,"Ernst 2002의 서술 판정을 세 범주로 묶은 것. 어떤 약초도 이상반응이 없다고 평가되지 않음",ha="center",fontsize=7.5,color="#2d3748")
    save(fig,"그림11-8")

if __name__=="__main__":
    fig111(); n,kc=fig112(); fig113(); fig114(); fig115(); fig116(); fig117(); fig118(); print(n,kc)

#!/usr/bin/env python3
"""목차 v3(세포신호 추가) 생성: python3 tools/mk-molbook-toc.py v3 -> docs/molbook-toc-v3.md, build/인체속허브분자생물학목차v3.pdf"""
import sys, html, os
from weasyprint import HTML
VER = sys.argv[1] if len(sys.argv) > 1 else "v3"
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
TITLE = "인체 속 허브의 분자생물학"
SUB = "풀의 분자가 몸의 세포에 말을 거는 방식 (가제)"

# (id, 제목, [(허브, 분자→표적)], 세포신호 [경로 줄], 그림 제목)
PARTS = [
 ("서장", [
  ("s0", "서장. 풀 한 줌이 세포에 닿기까지",
   [("개똥쑥 (Artemisia annua)", "아르테미시닌"), ("버드나무 (Salix spp.)", "살리신")],
   ["세포신호의 공통 문법: 리간드 → 수용체 → 전달자 → 이차전령 → 키나아제 연쇄 → 전사인자 → 반응",
    "신호가 켜지는 네 가지 입구: GPCR, 이온채널, 효소 연결 수용체, 핵수용체"],
   "세포신호의 공통 지도(이 책 전체의 길잡이)"),
 ]),
 ("제1부. 몸으로 들어가는 길", [
  ("c1", "1장. 맛과 향이 먼저 말을 건다",
   [("고추 (Capsicum annuum)", "캡사이신 → TRPV1"), ("박하 (Mentha × piperita)", "멘톨 → TRPM8"), ("마늘 (Allium sativum)", "알리신 → TRPA1"), ("용담 (Gentiana lutea)", "겐티오피크린 → 쓴맛 수용체 TAS2R")],
   ["쓴맛: TAS2R(GPCR) → 거스트듀신 → PLCβ2 → IP3 → Ca²⁺ → TRPM5",
    "TRP 채널: 양이온(Ca²⁺) 유입 → 탈분극 → 감각 신경 활동전위, 칼모듈린·CaMKII"],
   "TAS2R와 TRP 채널의 두 감각 신호 경로"),
  ("c2", "2장. 장벽을 넘는 분자",
   [("강황 (Curcuma longa)", "커큐민(낮은 생체이용률)"), ("후추 (Piper nigrum)", "피페린(흡수 증진)"), ("녹차 (Camellia sinensis)", "EGCG(장 흡수 한계)")],
   ["장 상피 밀착연접 조절: MLCK → 근육 미오신 경쇄 인산화, ZO-1·occludin",
    "유출 수송체와 대사 효소가 만드는 신호 이전의 농도 장벽"],
   "장 상피를 건너는 경로와 밀착연접 신호"),
  ("c3", "3장. 장내 미생물이라는 또 하나의 약제사",
   [("인삼 (Panax ginseng)", "진세노사이드 Rb1 → compound K"), ("석류 (Punica granatum)", "엘라그산 → 우롤리틴"), ("센나 (Senna alexandrina)", "센노사이드의 장내 활성화"), ("감초 (Glycyrrhiza uralensis)", "글리시리진 → 글리시레티닉산")],
   ["미생물 대사산물이 켜는 수용체: 단쇄지방산 → GPR41·GPR43, 담즙산 → TGR5·FXR, 인돌 → AhR",
    "장내분비 세포 → GLP-1 분비 → 전신 신호"],
   "미생물 대사산물에서 숙주 수용체까지"),
  ("c4", "4장. 간과 수송체",
   [("세인트존스워트 (Hypericum perforatum)", "하이퍼포린 → PXR, CYP3A4, P-당단백질"), ("밀크시슬 (Silybum marianum)", "실리마린 → CYP·UGT 억제 논쟁")],
   ["이물질 감지 핵수용체: PXR·CAR → 반응 요소 → CYP3A4·MDR1 유도(1상·2상·3상 반응)",
    "신호가 켜진 뒤 약물 농도가 바뀌는 되먹임"],
   "PXR이 켜는 해독 프로그램"),
 ]),
 ("제2부. 세포 표면에서 세포 안으로", [
  ("c5", "5장. 막 수용체와 이온채널",
   [("카바 (Piper methysticum)", "카바락톤 → GABA-A, 이온채널"), ("발레리안 (Valeriana officinalis)", "발레렌산 → GABA-A"), ("대마 (Cannabis sativa)", "THC·CBD → CB1·CB2"), ("양귀비 (Papaver somniferum)", "모르핀 → μ 오피오이드 수용체")],
   ["GABA-A: 리간드 개폐 Cl⁻ 채널 → 과분극 → 신경 억제",
    "CB1·μ 오피오이드: GPCR(Gi/o) → 아데닐산 고리화효소 억제 → cAMP 감소, GIRK 활성, β-arrestin 경로"],
   "이온채널형과 GPCR형 수용체의 신호 비교"),
  ("c6", "6장. 효소를 막는 풀",
   [("버드나무", "살리실산 → COX"), ("생강 (Zingiber officinale)", "진저롤 → COX·LOX"), ("갈란투스 (Galanthus spp.)", "갈란타민 → 아세틸콜린에스터라아제"), ("개똥쑥", "아르테미시닌의 철-헴 활성화")],
   ["에이코사노이드 신호: PLA₂ → 아라키돈산 → COX/LOX → 프로스타글란딘·류코트리엔 → EP 수용체(GPCR)",
    "콜린성 시냅스: 아세틸콜린 ↔ AChE 분해 ↔ 니코틴·무스카린 수용체"],
   "아라키돈산 연쇄와 효소 억제 지점"),
  ("c7", "7장. 에너지와 성장의 스위치",
   [("황련 (Coptis chinensis)", "베르베린 → AMPK"), ("계피 (Cinnamomum cassia)", "신남알데히드·폴리페놀 → 인슐린 신호"), ("녹차", "EGCG → AMPK·mTOR")],
   ["에너지 센서: AMP/ATP 상승 → LKB1 → AMPK → ACC 인산화, mTORC1 억제",
    "성장 신호: 인슐린 → IRS → PI3K → Akt → mTORC1, Ras → Raf → MEK → ERK"],
   "AMPK–mTOR 에너지·성장 스위치"),
  ("c8", "8장. 염증의 신호망",
   [("황금 (Scutellaria baicalensis)", "바이칼린 → NF-κB"), ("보스웰리아 (Boswellia serrata)", "보스웰릭산 → 5-LOX·NF-κB"), ("뇌공등 (Tripterygium wilfordii)", "트립톨라이드 → NF-κB(독성 동반)"), ("감초", "글리시리진 → HMGB1·TLR4")],
   ["TLR4 → MyD88 → IKK → IκB 분해 → NF-κB 핵 이동 → TNF·IL-6 전사",
    "NLRP3 인플라마좀 → 카스파아제-1 → IL-1β / IL-6 → JAK → STAT3"],
   "TLR4–NF-κB와 인플라마좀"),
 ]),
 ("제3부. 핵과 소기관", [
  ("c9", "9장. 핵 수용체",
   [("홉 (Humulus lupulus)", "8-프레닐나린제닌 → 에스트로겐 수용체"), ("칡 (Pueraria lobata)·대두 (Glycine max)", "이소플라본 → ERβ"), ("인삼", "진세노사이드 → 스테로이드 수용체")],
   ["리간드 → 핵수용체 → 공동조절자 → 반응 요소(ERE·PPRE) → 전사",
    "비유전체 경로: 막 결합 ER → PI3K·MAPK 신속 신호"],
   "핵수용체의 유전체 경로와 비유전체 경로"),
  ("c10", "10장. 항산화는 청소부가 아니라 신호다",
   [("브로콜리 (Brassica oleracea)", "설포라판 → Nrf2"), ("로즈마리 (Rosmarinus officinalis)", "카르노식산 → Nrf2"), ("강황", "커큐민 → Nrf2")],
   ["Keap1 시스테인 감지 → Nrf2 안정화 → 핵 이동 → ARE → HO-1·NQO1·GCL 전사",
    "ROS는 해로운 부산물이자 이차전령: 호르메시스 곡선"],
   "Keap1–Nrf2–ARE 경로"),
  ("c11", "11장. 후성유전의 스위치",
   [("호장근 (Reynoutria japonica)", "레스베라트롤 → SIRT1(논쟁 포함)"), ("녹차", "EGCG → DNMT"), ("브로콜리", "설포라판 → HDAC")],
   ["신호에서 염색질로: HAT·HDAC의 아세틸화, DNMT의 메틸화, SIRT1의 NAD⁺ 의존 탈아세틸화",
    "AMPK → NAD⁺ → SIRT1, miRNA 생합성(Dicer)과 표적 mRNA 억제"],
   "대사 신호가 염색질을 바꾸는 길"),
  ("c12", "12장. 미토콘드리아, 자가포식, 세포자멸",
   [("황련", "베르베린 → 미토콘드리아 복합체 I"), ("개똥쑥", "아르테미시닌 → 암세포 철 의존 사멸"), ("강황", "커큐민 → 카스파아제·p53")],
   ["내인성 세포자멸: Bcl-2/Bax → 시토크롬 c → Apaf-1 → 카스파아제-9 → 카스파아제-3, p53 ↔ MDM2",
    "자가포식: AMPK → ULK1, mTORC1 억제 해제 → LC3 / 철 의존 사멸: GPX4"],
   "세포 운명을 가르는 세 경로"),
 ]),
 ("제4부. 기관에서 읽다", [
  ("c13", "13장. 뇌와 신경",
   [("은행 (Ginkgo biloba)", "은행잎 플라보노이드·징코라이드"), ("브라미 (Bacopa monnieri)", "바코사이드"), ("인삼", "진세노사이드"), ("세인트존스워트", "우울증과 세로토닌 재흡수")],
   ["시냅스 신호: GABA·글루타메이트(NMDA), 세로토닌 재흡수(SERT)",
    "BDNF → TrkB → ERK·PI3K → CREB / 소교세포 TLR4 → NF-κB 신경염증"],
   "시냅스에서 신경 가소성까지"),
  ("c14", "14장. 대사",
   [("황련", "베르베린"), ("여주 (Momordica charantia)", "카란틴 → AMPK"), ("호로파 (Trigonella foenum-graecum)", "4-하이드록시이소류신 → 인슐린 분비"), ("계피", "인슐린 신호")],
   ["인슐린 → IRS → PI3K → Akt → GLUT4 이동, AMPK → 포도당 흡수",
    "PPAR 전사 신호, 장내분비 TGR5 → GLP-1"],
   "인슐린·AMPK·GLP-1 신호의 교차"),
  ("c15", "15장. 심혈관",
   [("디기탈리스 (Digitalis purpurea)", "디곡신 → Na⁺/K⁺-ATPase"), ("단삼 (Salvia miltiorrhiza)", "단삼 페놀산·탄시논"), ("산사 (Crataegus spp.)", "플라보노이드"), ("마늘", "알리신·황화물 → 혈관 내피, 혈소판")],
   ["혈관 내피: eNOS → NO → sGC → cGMP → PKG → 이완",
    "심근: Na⁺/K⁺-ATPase 억제 → NCX → 세포내 Ca²⁺ 상승 / 혈소판: TXA₂·ADP(P2Y12) 신호"],
   "NO–cGMP와 Ca²⁺ 신호"),
  ("c16", "16장. 암",
   [("태평양주목 (Taxus brevifolia)", "파클리탁셀 → 미세소관"), ("일일초 (Catharanthus roseus)", "빈크리스틴 → 튜불린"), ("희수 (Camptotheca acuminata)", "캄프토테신 → 토포아이소머라아제 I"), ("메이애플 (Podophyllum peltatum)", "에토포사이드 → 토포아이소머라아제 II")],
   ["미세소관 동역학 교란 → 스핀들 체크포인트 → M기 정지 → 세포자멸",
    "토포아이소머라아제 독성 → DNA 손상 → ATM/ATR → p53"],
   "세포주기 체크포인트와 항암 표적"),
 ]),
 ("제5부. 분자 수준의 증거를 읽는 법", [
  ("c17", "17장. 예측과 실증",
   [("단삼", "네트워크 약리학·도킹 사례"), ("황금", "다표적 사례"), ("강황", "범용 활성 사례")],
   ["약물–표적–경로 네트워크와 경로 농축(KEGG 등): 연결은 결합을 뜻하지 않는다",
    "도킹은 결합 가능성만 말하고 신호의 방향(작용·억제)은 말하지 못한다"],
   "예측 네트워크에서 실증 실험까지"),
  ("c18", "18장. 시험관에서 사람까지",
   [("강황", "커큐민 PAINS 논쟁"), ("녹차", "EGCG"), ("호장근", "레스베라트롤의 농도 문제")],
   ["농도–반응 곡선과 수용체 점유: 시험관 농도와 혈중 농도의 간격",
    "분석 간섭 화합물(PAINS)이 가짜 신호를 만드는 방식, 다표적 효과의 잡음"],
   "시험관 농도와 혈중 농도의 간격"),
  ("c19", "19장. 안전성의 분자 기전",
   [("카바", "간독성"), ("광방기 (Aristolochia fangchi)", "아리스톨로크산 DNA 부가체"), ("콤프리 (Symphytum officinale)", "피롤리지딘 알칼로이드"), ("마황 (Ephedra sinica)", "에페드린"), ("뇌공등", "독성")],
   ["반응성 대사물 → 글루타티온 고갈 → 미토콘드리아 손상·JNK 활성 → 간세포 사멸",
    "DNA 부가체 → 손상 반응 → TP53 변이 / 에페드린 → 아드레날린 수용체 → cAMP"],
   "독성 신호의 세 경로"),
  ("c20", "20장. 남은 질문",
   [("앞 장 허브 전체", "표적 지도(부록 B)"), ("인삼", "compound K 반응자 사례")],
   ["신호의 개인차: 유전 다형(CYP2D6·CYP2C19), 장내 미생물 반응자",
    "오믹스와 시스템 수준 신호 모델"],
   "개인 간 신호 차이를 만드는 변수들"),
 ]),
]
APP = ["A. 분자생물학 용어집", "B. 표적 도감표 (표적 · 허브 · 성분 · 근거 수준 · 신호 경로)", "C. 참고문헌 색인"]
GAP = [("충분", "항산화/산화 스트레스 2,520, 세포자멸 688, TNF·IL-6 486, MAPK 295, NF-κB 284, 장내 미생물 280, 미토콘드리아 272, CYP450 271, 네트워크 약리학 232, PI3K/Akt 232, 분자 도킹 231"),
       ("보통(보강 권장)", "COX-2 166, 호르몬 수용체 164, 인슐린 신호 153, 자가포식 147, Nrf2 135, 세로토닌·도파민 113, AChE 112, P-gp 109, 후성유전 105, 핵수용체 96, AMPK 89, PPAR 86, mTOR 86"),
       ("부족(신규 수집 필요)", "TRP 채널 14, SIRT1 36, HIF 41, Wnt/Notch/Hedgehog 44, GABA 46, STAT3 52, p53 64")]

# --- markdown
md = [f"# 《{TITLE}》 (가제) 목차 {VER} — 장별 세포신호 추가\n", f"{SUB} · 이광조 · 과학과영성출판사\n"]
for pn, chs in PARTS:
    md.append(f"\n## {pn}\n")
    for cid, t, herbs, sig, fig in chs:
        md.append(f"### {t}")
        md.append("- 배정 허브: " + " / ".join(f"{h} — {m}" for h, m in herbs))
        md.append("- 세포신호:")
        for s in sig: md.append(f"  - {s}")
        md.append(f"- 그림 계획: {fig}\n")
md.append("\n## 부록\n" + "\n".join(f"- {a}" for a in APP))
open(os.path.join(ROOT, "docs", f"molbook-toc-{VER}.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")

# --- html
E = html.escape
svg = '''<svg viewBox="0 0 640 330" xmlns="http://www.w3.org/2000/svg" font-family="Noto Sans CJK KR" font-size="13">
<defs><marker id="a" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 Z" fill="#1f4d3a"/></marker></defs>
<rect x="0" y="0" width="640" height="330" fill="#fbf8ef" stroke="#cfc6a8"/>
<rect x="0" y="86" width="640" height="26" fill="#d8ccaa" opacity=".6"/><text x="12" y="104" fill="#5a4a22">세포막</text>
<rect x="14" y="20" width="110" height="46" rx="6" fill="#d9764a"/><text x="69" y="40" fill="#fff" text-anchor="middle">허브 분자</text><text x="69" y="57" fill="#fff" text-anchor="middle">(리간드)</text>
<rect x="160" y="64" width="130" height="78" rx="6" fill="#5e9a6f"/><text x="225" y="88" fill="#fff" text-anchor="middle">수용체</text><text x="225" y="108" fill="#fff" text-anchor="middle" font-size="11">GPCR · 이온채널</text><text x="225" y="126" fill="#fff" text-anchor="middle" font-size="11">효소 연결 수용체</text>
<rect x="330" y="150" width="130" height="44" rx="6" fill="#7fb88a"/><text x="395" y="170" text-anchor="middle">전달자</text><text x="395" y="186" text-anchor="middle" font-size="11">G단백질 · 어댑터</text>
<rect x="490" y="150" width="136" height="44" rx="6" fill="#7fb88a"/><text x="558" y="170" text-anchor="middle">이차전령</text><text x="558" y="186" text-anchor="middle" font-size="11">cAMP · Ca²⁺ · IP3 · PIP3</text>
<rect x="490" y="222" width="136" height="44" rx="6" fill="#a8d2ae"/><text x="558" y="242" text-anchor="middle">키나아제 연쇄</text><text x="558" y="258" text-anchor="middle" font-size="11">AMPK · Akt · MAPK · IKK</text>
<rect x="330" y="222" width="130" height="44" rx="6" fill="#a8d2ae"/><text x="395" y="242" text-anchor="middle">전사인자</text><text x="395" y="258" text-anchor="middle" font-size="11">NF-κB · Nrf2 · STAT3</text>
<rect x="160" y="222" width="130" height="44" rx="6" fill="#f3ecd9" stroke="#1f4d3a"/><text x="225" y="242" text-anchor="middle">유전자 반응</text><text x="225" y="258" text-anchor="middle" font-size="11">단백질·세포 운명</text>
<rect x="14" y="222" width="110" height="44" rx="6" fill="#143427"/><text x="69" y="242" fill="#fff" text-anchor="middle">핵수용체</text><text x="69" y="258" fill="#fff" text-anchor="middle" font-size="11">막을 지나 직접</text>
<g stroke="#1f4d3a" stroke-width="2" fill="none" marker-end="url(#a)">
<path d="M124 50 L160 90"/><path d="M290 110 L330 165"/><path d="M460 172 L490 172"/><path d="M558 194 L558 222"/><path d="M490 244 L460 244"/><path d="M330 244 L290 244"/><path d="M69 66 L69 222" stroke-dasharray="5 4"/><path d="M124 244 L160 244" stroke-dasharray="5 4"/></g>
<text x="12" y="300" font-size="11" fill="#555">실선: 막 수용체 경로 · 점선: 지용성 분자가 막을 통과해 핵수용체에 직접 결합하는 경로</text></svg>'''

CSS = '''@page { size: A4; margin: 20mm 18mm 22mm; @bottom-center { content: counter(page); font: 9pt "Noto Sans CJK KR"; color:#555 } }
body { font-family: "Noto Sans CJK KR"; font-size: 10pt; line-height: 1.55; color:#222 }
h1 { font-size: 22pt; margin: 0 0 4mm } h2 { font-size: 14pt; color:#1f4d3a; border-bottom: .4mm solid #1f4d3a; padding-bottom: 1mm; margin-top: 9mm; page-break-after: avoid }
h3 { font-size: 11.5pt; margin: 6mm 0 1.5mm; page-break-after: avoid } .sub { color:#555; margin-bottom: 6mm }
.chap { page-break-inside: avoid; margin-bottom: 3mm } .chap p { margin: 0 0 1mm } .lbl { font-weight: 700; color:#1f4d3a }
ul { margin: 0 0 1mm 5mm; padding:0 } li { margin: 0 }
.toc a { color:#222; text-decoration:none } .toc li { list-style:none; margin: 0 0 1mm } .toc a::after { content: leader('.') target-counter(attr(href), page) }
.toc li.p { font-weight:700; margin-top: 3mm } .toc ul { margin:0; padding:0 }
table { border-collapse: collapse; width:100%; font-size: 8.8pt; margin: 2mm 0 5mm } th, td { border: .2mm solid #999; padding: 1.2mm 2mm; vertical-align: top } th { background:#e9e2cc }
.cap { font-weight: 700; font-size: 9.5pt; margin: 3mm 0 1mm } figure { margin: 3mm 0; page-break-inside: avoid } figure svg { width:100% } figcaption { font-weight:700; font-size: 9.5pt; margin-top: 1mm }
.pb { page-break-before: always }'''

h = [f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>']
h.append(f'<h1>《{TITLE}》 목차</h1><div class="sub">{E(SUB)} · 이광조 · 과학과영성출판사 · 장별 세포신호 추가판</div>')
h.append('<p>각 장은 허브 사례(분자와 표적)와 함께 그 표적이 속한 세포신호 경로를 한 장의 그림으로 설명한다. 허브 이름은 한국어 독음 기준이며, 같은 허브가 여러 장에 나오면 장마다 다른 표적을 맡는다.</p>')
h.append('<h2>목차</h2><div class="toc"><ul>')
h.append('<li><a href="#fig1">그림 0-1. 세포신호의 공통 지도</a></li>')
idx = 0
for pn, chs in PARTS:
    if pn != "서장": h.append(f'<li class="p">{E(pn)}</li>')
    for cid, t, *_ in chs:
        h.append(f'<li><a href="#{cid}">{E(t)}</a></li>')
h.append('<li class="p">부록</li>')
for i, a in enumerate(APP): h.append(f'<li><a href="#app{i}">{E(a)}</a></li>')
h.append('<li class="p">표</li><li><a href="#t1">표 1. 장별 배정 허브와 핵심 세포신호</a></li><li><a href="#t2">표 2. 기존 말뭉치의 분자 표적별 근거 건수</a></li>')
h.append('</ul></div>')

h.append('<div class="pb"></div><h2>세포신호의 공통 지도</h2>')
h.append(f'<figure id="fig1">{svg}<figcaption>그림 0-1. 세포신호의 공통 지도. 허브 분자가 수용체에서 시작해 이차전령, 키나아제, 전사인자를 거쳐 유전자 반응에 이르는 순서(개념도)</figcaption></figure>')

h.append('<h2>장별 요약</h2>')
h.append('<div class="cap" id="t1">표 1. 장별 배정 허브와 핵심 세포신호</div><table><tr><th>장</th><th>배정 허브</th><th>핵심 세포신호</th></tr>')
for pn, chs in PARTS:
    for cid, t, herbs, sig, fig in chs:
        hs = ", ".join(h_.split(" (")[0] for h_, _ in herbs)
        h.append(f'<tr><td>{E(t.split(". ")[0])}</td><td>{E(hs)}</td><td>{E(sig[0])}</td></tr>')
h.append('</table>')

for pn, chs in PARTS:
    h.append(f'<div class="pb"></div>' if False else '')
    if pn != "서장": h.append(f'<h2>{E(pn)}</h2>')
    for cid, t, herbs, sig, fig in chs:
        h.append(f'<div class="chap"><h3 id="{cid}">{E(t)}</h3>')
        h.append('<p><span class="lbl">배정 허브</span></p><ul>' + "".join(f'<li>{E(a)} — {E(b)}</li>' for a, b in herbs) + '</ul>')
        h.append('<p><span class="lbl">세포신호</span></p><ul>' + "".join(f'<li>{E(s)}</li>' for s in sig) + '</ul>')
        num = cid[1:] if cid.startswith("c") else "0"
        h.append(f'<p><span class="lbl">그림 계획</span> 그림 {num}-1. {E(fig)}</p></div>')
h.append('<h2>부록</h2><ul>' + "".join(f'<li id="app{i}">{E(a)}</li>' for i, a in enumerate(APP)) + '</ul>')
h.append('<h2>근거 점검</h2><div class="cap" id="t2">표 2. 기존 말뭉치(12,155편)의 분자 표적별 근거 건수(초록 키워드 기준)</div><table><tr><th>구분</th><th>건수</th></tr>')
for a, b in GAP: h.append(f'<tr><td>{E(a)}</td><td>{E(b)}</td></tr>')
h.append('</table><p>이 말뭉치는 허브 일반 논문이라 표적별 근거가 얕다. 집필 전에 z840 수집기로 표적별 질의 확장 수집을 하고, 각 허브-표적 쌍의 근거가 부족하면 다른 허브로 교체하거나 "근거 약함"으로 표기한다.</p></body></html>')
out = os.path.join(ROOT, "build", f"molbook-toc-{VER}.pdf")
HTML(string="".join(h)).write_pdf(out)
print(out)

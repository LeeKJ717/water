#!/usr/bin/env python3
"""부록 3종을 본문(chapters/ch*.md)에서 장 번호를 계산해 생성한다.  사용: python3 tools/mk-appendix.py
출력: chapters/ap1.md(용어집) ap2.md(허브 도감표) ap3.md(참고문헌 색인)"""
import re, glob, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
TXT = {}
for f in sorted(glob.glob(str(ROOT / "chapters" / "ch[0-9]*.md"))):
    n = int(re.search(r"ch(\d+)", f).group(1))
    TXT[n] = re.sub(r"<[^>]+>|\*", "", open(f, encoding="utf-8").read().split("## 참고문헌")[0])


def fmt(got, cap=6):
    got = sorted(got)
    more = len(got) > cap
    got = got[:cap]
    names = [str(n) if n else "서장" for n in got]
    if names and names[0] == "서장":
        s = "서장" + ("·" + "·".join(names[1:]) + "장" if len(names) > 1 else "")
    else:
        s = "·".join(names) + "장"
    return s + (" 외" if more else "")


def chs(kws):
    got = sorted({n for n, t in TXT.items() for k in kws if k in t})
    return fmt(got)


# ---------- 부록 A 용어집 ----------
G = [
 ("식물과 성분", [
  ("이차 대사산물", "secondary metabolite", "식물이 생장에 직접 필요하지 않은 이차 대사로 만드는 물질. 약초의 약효 성분은 대부분 여기에 속한다.", ["이차 대사산물"]),
  ("알칼로이드", "alkaloid", "질소를 가진 식물 성분의 한 부류. 양귀비의 모르핀, 기나나무의 퀴닌, 커피의 카페인이 해당한다.", ["알칼로이드"]),
  ("테르페노이드", "terpenoid", "탄소 다섯 개짜리 조각이 이어 붙어 만들어지는 계열. 정유의 대부분과 인삼의 사포닌이 이 계열이다.", ["테르페노이드"]),
  ("배당체", "glycoside", "당이 붙은 분자. 디기탈리스의 강심배당체가 대표적이다.", ["배당체"]),
  ("사포닌", "saponin", "비눗물처럼 거품을 내는 배당체. 인삼의 대표 성분 계열이다.", ["사포닌"]),
  ("정유", "essential oil", "식물에서 증류해 얻는 향기 나는 기름.", ["정유"]),
  ("폴리페놀", "polyphenol", "플라보노이드, 탄닌, 강황의 커큐민 같은 페놀 계열 성분의 총칭.", ["폴리페놀"]),
  ("글루코시놀레이트", "glucosinolate", "겨자 특유의 매운맛을 내는 황 함유 화합물.", ["글루코시놀레이트"]),
  ("세스퀴테르펜 락톤", "sesquiterpene lactone", "테르페노이드 계열의 한 부류. 8장의 연구에서 NF-κB를 억제한 식물 추출물에 풍부했다.", ["세스퀴테르펜 락톤"]),
  ("아르테미시닌", "artemisinin", "개똥쑥(청호, Artemisia annua)에서 얻는 항말라리아 성분. 중국어로 칭하오쑤(靑蒿素)이다.", ["아르테미시닌"]),
  ("커큐민", "curcumin", "강황의 노란 색소. 남아시아 약초 가운데 가장 많이 연구된 성분 중 하나이다.", ["커큐민"]),
 ]),
 ("전통 지식의 체계", [
  ("민족의학", "ethnomedicine", "한 사회가 전해 온 병과 치료의 지식.", ["민족의학"]),
  ("본초", "bencao", "약물의 이름, 기원, 효능을 적은 동아시아 약물서의 전통. 『신농본초경』이 대표적이다.", ["본초"]),
  ("처방", "formula", "여러 약재를 정해진 구성으로 짜 맞춘 약. 갈근금련탕은 갈근, 황금, 황련, 감초 네 가지 약재로 이루어진다.", ["처방"]),
  ("약전", "pharmacopoeia", "약의 이름, 기원, 품질 기준을 국가가 정하는 책.", ["약전"]),
  ("캄포", "Kampo", "일본에서 전해져 의료에 쓰이는 한방 처방의 체계.", ["캄포"]),
  ("아유르베다", "Ayurveda", "인도의 전통 의학. 체질을 먼저 판정하고 다약초 처방과 생활 지침을 고른다.", ["아유르베다"]),
  ("라사야나", "rasayana", "아유르베다의 회춘 약초군.", ["라사야나"]),
 ]),
 ("연구 방법과 증거", [
  ("네트워크 약리학", "network pharmacology", "한 분자가 여러 표적에 닿고 여러 성분이 한 경로에 모이는 복잡성을 성분-표적 네트워크로 다루는 방법.", ["네트워크 약리학"]),
  ("대사체학", "metabolomics", "생물계 안의 대사물질 전체를 측정해 혼합물의 효과를 보려는 접근.", ["대사체학"]),
  ("시너지", "synergy", "여러 성분을 섞으면 단일 성분보다 효과가 커진다는 주장. 근거는 약하고 논쟁적이다.", ["시너지"]),
  ("위약", "placebo", "활성 성분이 없는 대조 물질.", ["위약"]),
  ("무작위 대조 시험", "randomized controlled trial", "참가자를 무작위로 시험군과 대조군에 배정해 비교하는 시험.", ["무작위 대조"]),
  ("이중맹검", "double blind", "참가자와 평가자 모두 어느 군인지 모르게 하는 설계.", ["이중맹검"]),
  ("체계적 고찰", "systematic review", "정해진 방법으로 관련 연구를 찾아 평가하고 종합하는 연구.", ["체계적 고찰"]),
  ("메타분석", "meta-analysis", "여러 연구의 결과를 통계적으로 합쳐 하나의 추정치로 만드는 분석.", ["메타분석"]),
  ("CONSORT", "CONSORT", "무작위 시험의 보고 지침.", ["CONSORT"]),
  ("비뚤림 위험", "risk of bias", "연구의 설계나 수행의 결함이 결과를 한쪽으로 기울일 가능성.", ["비뚤림 위험"]),
  ("신뢰구간", "confidence interval", "추정치가 있을 법한 범위. 11장의 우(Wu) 등의 조사에서 6.8%의 95% 신뢰구간은 5.9~7.7이었다.", ["신뢰구간"]),
  ("검출과 해석", "detection and interpretation", "이 책의 서술 방식. 연구가 실제로 측정한 것(검출)과 그로부터 읽어 내는 의미(해석)를 나누어 적는다.", ["검출과 해석"]),
 ]),
 ("안전성과 품질", [
  ("약물감시", "pharmacovigilance", "시판된 약의 이상 반응을 모으고 평가하는 활동.", ["약물감시"]),
  ("RUCAM", "RUCAM", "약물 유발 간 손상과 약초 유발 간 손상에 쓰는 간독성 특화 진단 방법. 항목별 점수로 인과성의 등급을 낸다.", ["RUCAM"]),
  ("약초-약물 상호작용", "herb–drug interaction", "약초 성분이 함께 먹는 약의 효과를 바꾸는 현상. 세인트존스워트가 대표적이다.", ["상호작용"]),
  ("CYP3A4와 PXR", "CYP3A4 / PXR", "CYP3A4는 약물 대사 효소이고, PXR은 그 발현을 조절하는 핵 수용체이다.", ["CYP3A4", "PXR"]),
  ("아리스톨로크산", "aristolochic acid", "광방기(Aristolochia fangchi)로 잘못 바뀐 환약의 신독성과 발암성에서 문제가 된 계열의 성분.", ["아리스톨로크산"]),
  ("DNA 바코드", "DNA barcode", "짧은 DNA 서열로 종을 확인하는 방법.", ["DNA 바코드"]),
  ("지표 성분", "marker compound", "약재의 품질을 확인하려고 정량하는 기준 성분.", ["지표 성분"]),
  ("화학 지문", "chemical fingerprint", "한두 가지 표지자 대신 전체 화학 프로필을 평가하고 공통 패턴을 뽑아 기준으로 삼는 분석.", ["화학 지문"]),
  ("품질 표지자", "quality marker", "지표 성분에서 화학 지문을 거쳐 일관성을 보증하는 범위를 넓힌 개념.", ["품질 표지자"]),
  ("위조와 불순물 혼입", "adulteration", "제품에 표기되지 않은 식물이나 성분이 들어 있는 문제.", ["불순물", "위조"]),
  ("멸종 위기 단계", "threat category", "위급(CR), 위기(EN), 취약(VU)의 세 단계. 14장의 히말라야 약용 식물 60종은 이 단계로 나뉘었다.", ["위급"]),
  ("합성생물학", "synthetic biology", "생물에 경로를 넣어 원하는 물질을 만들게 하는 방법. 식물 천연물을 미생물에서 만드는 데 쓰인다.", ["합성생물학"]),
 ]),
]
out = ["# 부록 A. 용어집", "", "본문에서 정의하거나 처음 설명한 용어를 가나다순이 아니라 주제별로 모았다. 괄호 안의 장은 용어가 본문에 나오는 장이다.", ""]
for grp, items in G:
    out += [f"## {grp}", ""]
    for ko, en, df, kws in items:
        c = chs(kws)
        out.append(f"**{ko}**({en}) — {df} ({c})")
        out.append("")
open(ROOT / "chapters" / "ap1.md", "w", encoding="utf-8").write("\n".join(out))

# ---------- 부록 B 허브 도감표 ----------
T = [
 ("표 B-1. 허브 도감표 1: 1~4장에서 만난 식물", [
  ("베르노니아 아미그달리나", "Vernonia amygdalina", ["Vernonia amygdalina"], "쓴맛이 강한 식물. 침팬지가 속살을 씹어 장내 선충 감염을 다스린다"),
  ("대마", "Cannabis sativa", ["Cannabis sativa"], "한 종에서 칸나비노이드, 테르펜, 페놀류가 보고된 식물"),
  ("개똥쑥(청호)", "Artemisia annua", ["Artemisia annua", "개똥쑥"], "아르테미시닌의 식물. 전통 지식에서 출발해 실제 약이 된 사례"),
  ("인삼", "Panax ginseng", ["Panax ginseng"], "동아시아 약초 가운데 가장 많이 연구된 풀 중 하나"),
  ("뱀뿌리풀", "Rauwolfia serpentina", ["Rauwolfia serpentina"], "전통 약초가 서양 의학의 약(레세르핀)으로 들어간 대표적인 경로"),
  ("아슈와간다", "Withania somnifera", ["Withania somnifera"], "아유르베다의 대표적인 라사야나 약초. 무작위 대조 시험의 대상"),
  ("강황", "Curcuma longa", ["Curcuma longa"], "노란 색소 커큐민의 식물. 성분의 흡수 문제가 논점"),
 ]),
 ("표 B-2. 허브 도감표 2: 5~6장에서 만난 식물", [
  ("사프란", "Crocus sativus", ["Crocus sativus"], "이란에서 가장 귀한 약초이자 향신료. 우울증 임상시험의 대상"),
  ("계피", "Cinnamomum cassia", ["Cinnamomum cassia"], "이븐 시나의 심장 약초 50종 가운데 효과가 더 큰 것으로 확인된 식물로 열거"),
  ("레몬밤", "Melissa officinalis", ["Melissa officinalis"], "같은 심장 약초 연구에서 열거된 식물"),
  ("암라", "Phyllanthus emblica", ["Phyllanthus emblica"], "같은 심장 약초 연구에서 열거된 식물"),
  ("세인트존스워트", "Hypericum perforatum", ["Hypericum perforatum"], "우울증에 쓰는 유럽 약초. 다른 약의 효과를 바꾼다는 점이 논점"),
  ("은행나무", "Ginkgo biloba", ["Ginkgo biloba"], "가장 많이 시험된 약초 가운데 하나. 시험 결과가 엇갈린다"),
  ("에키네시아", "Echinacea (속)", ["에키네시아"], "감기와 상기도 감염에 쓰는 약초. 어린이 시험에서 효과가 확인되지 않았다"),
  ("톱야자", "Serenoa repens", ["Serenoa repens"], "전립선비대증에 쓰는 추출물. 표준 약과 직접 비교한 시험과 메타분석이 있다"),
 ]),
 ("표 B-3. 허브 도감표 3: 7~9장에서 만난 식물", [
  ("사더랜디아", "Lessertia frutescens", ["Lessertia frutescens"], "남아프리카의 약초. 안전성 관점의 임상시험 두 건"),
  ("카시아 압브레비아타", "Cassia abbreviata", ["Cassia abbreviata"], "짐바브웨 치료사 면담에서 가장 많이 언급된 식물"),
  ("칼레아 자카테치코이", "Calea zacatechichi", ["Calea zacatechichi"], "멕시코 약초 추출물 연구에서 NF-κB를 억제한 식물의 하나"),
  ("폴림니아 마쿨라타", "Polymnia maculata", ["Polymnia maculata"], "같은 연구에서 NF-κB를 억제한 식물의 하나"),
  ("골든실", "Hydrastis canadensis", ["Hydrastis canadensis"], "건강인 12명을 대상으로 한 약물 대사 효소 시험의 대상"),
  ("카바", "Piper methysticum", ["Piper methysticum"], "태평양 섬의 오랜 음료에서 항불안 추출물과 간독성 논쟁의 대상으로 옮겨 간 약초"),
  ("노니", "Morinda citrifolia", ["Morinda citrifolia"], "퍼진 약초의 근거를 다룬 사례"),
  ("티트리", "Melaleuca alternifolia", ["Melaleuca alternifolia"], "호주 토착 식물. 증류한 정유의 성분 기준이 정의된다"),
 ]),
 ("표 B-4. 허브 도감표 4: 12~13장에서 만난 식물", [
  ("분방기(粉防己)", "Stephania tetrandra", ["Stephania tetrandra"], "환약에 들어가야 할 약재. 잘못 바뀐 사건의 원래 약재"),
  ("광방기(廣防己)", "Aristolochia fangchi", ["Aristolochia fangchi"], "신독성과 발암성이 있는 식물. 분방기 자리에 잘못 들어갔다"),
  ("개족도리", "Asarum europaeum", ["Asarum europaeum"], "시판 제품에 들어 있을 수 있는 불법 성분의 예로 언급"),
  ("질경이 전초", "Plantaginis herba", ["Plantaginis herba"], "중금속 위해도 평가에서 위험 지수가 한도의 11배를 넘은 약재"),
 ]),
]
out = ["# 부록 B. 허브 도감표", "", "본문에 학명과 함께 등장한 식물을 장별로 정리했다. 설명은 본문에서 다룬 맥락만 적었으며 식물의 전체 효능을 뜻하지 않는다.", ""]
for cap, rows in T:
    out += [f'<div class="tblwrap" markdown="1">', f'<p class="cap"><strong>{cap}</strong></p>', "", "| 허브 | 학명 | 나오는 장 | 본문에서 다룬 맥락 |", "|---|---|---|---|"]
    for ko, sci, kws, ctx in rows:
        out.append(f"| {ko} | *{sci}* | {chs(kws)} | {ctx} |")
    out += ["", "</div>", ""]
open(ROOT / "chapters" / "ap2.md", "w", encoding="utf-8").write("\n".join(out))

# ---------- 부록 C 참고문헌 색인 ----------
ent = {}
for f in sorted(glob.glob(str(ROOT / "chapters" / "ch[0-9]*.md"))):
    n = int(re.search(r"ch(\d+)", f).group(1))
    t = open(f, encoding="utf-8").read()
    m = re.search(r"^## 참고문헌\s*$(.*)", t, re.M | re.S)
    if not m:
        continue
    for ln in m.group(1).splitlines():
        if not ln.startswith("- "):
            continue
        r = ln[2:].strip()
        mm = re.match(r"(.+?)\s\((\d{4}[a-z]?|n\.d\.)\)", r)
        if not mm:
            continue
        au, yr = mm.group(1), mm.group(2)
        sur = au.split(",")[0].strip().rstrip(".")
        n_au = len(re.findall(r"\b[A-Z]\.(?:\s?[A-Z]\.)*(?:-[A-Z]\.)?", au)) if "," in au else 1
        doi = re.search(r"https://doi\.org/(\S+)", r)
        key = doi.group(1).lower() if doi else (sur + yr + r[:90])
        if n_au <= 1:
            lab = f"{sur} ({yr})"
        elif n_au == 2:
            s2 = re.split(r",\s*&\s*|\s&\s", au)[-1].split(",")[0].strip()
            lab = f"{sur} & {s2} ({yr})"
        else:
            lab = f"{sur} 등 ({yr})"
        e = ent.setdefault(key, {"lab": lab, "sur": sur, "yr": yr, "ch": set()})
        e["ch"].add(n)
rows = sorted(ent.values(), key=lambda e: (e["sur"].lower(), e["yr"]))
out = ["# 부록 C. 참고문헌 색인", "", f"각 장 끝의 참고문헌 {len(rows)}편을 첫 저자 이름순으로 정리했다. 오른쪽은 그 문헌이 실린 장이다. 전체 서지 정보는 해당 장의 참고문헌에 있다.", "", '<ul class="idx" markdown="1">']
for e in rows:
    out.append(f"- {e['lab']} — " + fmt(e["ch"], 12))
out += ["</ul>", ""]
open(ROOT / "chapters" / "ap3.md", "w", encoding="utf-8").write("\n".join(out))
print("용어", sum(len(i) for _, i in G), "도감", sum(len(r) for _, r in T), "색인", len(rows))

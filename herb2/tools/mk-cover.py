#!/usr/bin/env python3
"""표지 생성: python3 tools/mk-cover.py <ver> [spine_mm]
산출: cover/herb2-world-표지앞-<ver>.png (앞표지만, 폭 1400px), cover/herb2-world-표지펼침-<ver>.pdf (날개 100mm, 재단여유 3mm)
책등 두께는 용지·쪽수에 따라 달라지므로 인자로 받는다(기본 12mm, 잠정)."""
import sys, os, math
from playwright.sync_api import sync_playwright
VER = sys.argv[1] if len(sys.argv) > 1 else "v1"
SPINE = float(sys.argv[2]) if len(sys.argv) > 2 else 12.0
W, H, FLAP, BL = 182.0, 257.0, 100.0, 3.0
OUT = os.path.join(os.path.dirname(__file__), "..", "cover"); os.makedirs(OUT, exist_ok=True)
TITLE, SUB, AUTH, PUB = "풀이 약이 되기까지", "세계 허브의 과학사", "이광조 지음", "과학과영성출판사"
GREEN, DEEP, CREAM, ACC = "#1f4d3a", "#143427", "#f3ecd9", "#d9764a"

def art():
    # 독창적 식물 문양: 줄기 + 잎 + 여섯 개의 전환점(마디)
    leaves = ""
    for i in range(7):
        y = 640 - i*70; s = 1 - i*0.06
        leaves += f'<path d="M500 {y} C {500-150*s} {y-20*s}, {500-170*s} {y-95*s}, 500 {y-60*s} C {500-60*s} {y-60*s}, {500-100*s} {y-30*s}, 500 {y} Z" fill="#5e9a6f" opacity=".92"/>'
        leaves += f'<path d="M500 {y-25} C {500+150*s} {y-45*s}, {500+170*s} {y-120*s}, 500 {y-85*s} C {500+60*s} {y-85*s}, {500+100*s} {y-55*s}, 500 {y-25} Z" fill="#7fb88a" opacity=".92"/>'
    nodes = "".join(f'<circle cx="{500+ (i-2.5)*0}" cy="{690-i*118}" r="0"/>' for i in range(6))
    return f'''<svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMax meet">
<circle cx="500" cy="520" r="360" fill="none" stroke="{CREAM}" stroke-opacity=".18" stroke-width="2"/>
<circle cx="500" cy="520" r="290" fill="none" stroke="{CREAM}" stroke-opacity=".12" stroke-width="2"/>
<path d="M500 760 C 495 560, 505 360, 500 190" stroke="#3f7a55" stroke-width="9" fill="none" stroke-linecap="round"/>
{leaves}
<circle cx="500" cy="170" r="30" fill="{ACC}"/>
<g fill="{CREAM}">{"".join(f'<circle cx="{500+math.cos(math.radians(-90+60*i))*360:.1f}" cy="{520+math.sin(math.radians(-90+60*i))*360:.1f}" r="11"/>' for i in range(6))}</g>
</svg>'''

def front(extra=""):
    return f'''<div class="front" style="{extra}">
<div class="tag">대중과학</div>
<div class="artbox">{art()}</div>
<div class="ttl"><div class="sub">{SUB}</div><h1>{TITLE}</h1></div>
<div class="au">{AUTH} · {PUB}</div></div>'''

CSS = f'''
@page {{ margin:0 }} *{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:"Noto Sans CJK KR","Malgun Gothic",sans-serif;color:{CREAM}}}
.front{{position:relative;width:{W}mm;height:{H}mm;background:linear-gradient(180deg,{DEEP} 0%,{GREEN} 70%,#2b6048 100%);overflow:hidden}}
.front .tag{{position:absolute;left:16mm;top:16mm;background:{ACC};color:#fff;font-size:9pt;padding:1.2mm 3.5mm;border-radius:1mm}}
.front .ttl{{position:absolute;left:16mm;right:12mm;top:30mm}}
.front h1{{font-size:40pt;line-height:1.18;font-weight:900;letter-spacing:-.5pt}}
.front .sub{{font-size:15pt;color:#e6d9b8;margin-bottom:5mm;font-weight:500}}
.front .artbox{{position:absolute;left:0;right:0;bottom:20mm;height:185mm}}
.front .artbox svg{{width:100%;height:100%}}
.front .au{{position:absolute;left:16mm;bottom:12mm;font-size:12pt;color:#e6d9b8}}
.panel{{position:absolute;top:{BL}mm;height:{H}mm;overflow:hidden}}
.flap{{background:{CREAM};color:#2a2a2a;padding:14mm 11mm;font-size:8.8pt;line-height:1.6}}
.flap h3{{font-size:10.5pt;color:{DEEP};border-bottom:.4mm solid {DEEP};padding-bottom:2mm;margin-bottom:6mm}}
.bk{{display:flex;gap:4mm;margin-bottom:6mm;align-items:center}}
.bk .th{{width:17mm;height:24mm;background:#dccfae;border:.2mm solid #bda86c;font-size:6pt;text-align:center;display:flex;align-items:center;justify-content:center;color:#6a5a2c;padding:1mm;flex:none}}
.bk b{{display:block;font-size:9.5pt;color:{DEEP}}} .bk span{{font-size:8pt;color:#555}}
.back{{background:{DEEP};padding:18mm 16mm;font-size:9.5pt;line-height:1.75}}
.back .tag{{display:inline-block;background:{ACC};color:#fff;font-size:8pt;padding:1mm 3mm;border-radius:1mm;margin-bottom:6mm}}
.back h2{{font-size:15pt;margin-bottom:6mm;line-height:1.4}}
.back p{{margin-bottom:4mm}}
.back .toc{{margin-top:8mm;font-size:8.5pt;color:#d9cfae;border-top:.2mm solid #ffffff44;padding-top:5mm}}
.bar{{position:absolute;right:16mm;bottom:14mm;width:48mm;height:26mm;background:#fff;color:#222;font-size:7pt;text-align:center;padding-top:7mm}}
.spine{{background:{DEEP};display:flex;align-items:center;justify-content:center}}
.spine div{{writing-mode:vertical-rl;font-size:12pt;font-weight:700;white-space:nowrap;letter-spacing:1pt}}
.spine i{{font-style:normal;font-weight:400;color:#e6d9b8;font-size:9pt;margin-top:6mm}}
'''
OTHER = [("채식치유학","식물성 식이의 치유 원리"),("역사속의 채식인","채식 전통의 인물사"),("과학과 초월의 길목에서","과학과 영성의 접점")]
others = "".join(f'<div class="bk"><div class="th">{t}</div><div><b>{t}</b><span>{s}</span></div></div>' for t,s in OTHER)
AUTHOR = ("서울대학교 식품영양학 박사(학위논문: 홍삼 연구). 한국식품영양연구소 대표, 한국생활건강학원을 운영하며 약 30년간 식물성 영양·단식 생리·동양 수행 전통을 현대 과학과 연결해 연구해왔다.<br><br>저서로 『채식치유학』, 『역사속의 채식인』, 『과학과 초월의 길목에서』 등이 있다.<br><br>연락처: contact@ssbook.kr (예정)<br>홈페이지: www.ssbook.kr")
BLURB = ("사람은 아플 때 풀을 찾았다. 약국도 병원도 없던 시절, 몸이 아픈 사람이 손을 뻗을 수 있었던 것은 발밑의 식물이었다.",
 "수천 년 쌓인 전통의 경험과 지난 이십 년 사이 폭발적으로 늘어난 실험 논문은 서로의 언어를 잘 알지 못한다. 이 책은 두 세계를 잇는다. 개똥쑥 한 줌에서 노벨상까지 이어진 이야기를 따라가며, 동아시아·남아시아·중동·유럽·아프리카·아메리카·오세아니아의 약초 전통을 한 줄로 꿰고, 약리학·임상시험·안전성·표준화의 눈으로 허브를 다시 읽는다.",
 "논문 12,155편의 근거 위에서, 믿을 수 있는 것과 아직 모르는 것을 구분해 말한다.")
TOCS = "1부 뿌리 · 2부 아시아의 약초 전통 · 3부 서쪽과 남쪽의 약초 전통 · 4부 신대륙과 바다의 약초 전통 · 5부 과학의 눈으로 허브를 읽다 · 부록 용어집·도감표·참고문헌 색인"

TW = W*2 + SPINE + FLAP*2 + BL*2; TH = H + BL*2
x_lf = BL; x_back = BL+FLAP; x_sp = x_back+W; x_fr = x_sp+SPINE; x_rf = x_fr+W
html = f'''<html><head><meta charset="utf-8"><style>{CSS}
body{{width:{TW}mm;height:{TH}mm;position:relative;background:{DEEP}}}
.bgl{{position:absolute;left:0;top:0;width:{BL+FLAP}mm;height:{TH}mm;background:{CREAM}}}
.bgr{{position:absolute;right:0;top:0;width:{BL+FLAP}mm;height:{TH}mm;background:{CREAM}}}
</style></head><body><div class="bgl"></div><div class="bgr"></div>
<div class="panel flap" style="left:{x_lf}mm;width:{FLAP}mm"><h3>지은이의 다른 책</h3>{others}</div>
<div class="panel back" style="left:{x_back}mm;width:{W}mm"><div class="tag">SCIENCE &amp; SPIRIT</div><h2>{TITLE}<br><span style="font-size:11pt;font-weight:400;color:#e6d9b8">{SUB}</span></h2>
<p>{BLURB[0]}</p><p>{BLURB[1]}</p><p>{BLURB[2]}</p><div class="toc">{TOCS}</div><div class="bar">ISBN (추후 기입)<br>바코드 자리</div></div>
<div class="panel spine" style="left:{x_sp}mm;width:{SPINE}mm"><div>{TITLE} <i>{AUTH.split()[0]}</i></div></div>
<div class="panel" style="left:{x_fr}mm;width:{W}mm">{front()}</div>
<div class="panel flap" style="left:{x_rf}mm;width:{FLAP}mm"><h3>지은이 소개</h3><b style="font-size:11pt">이광조</b><br><br>{AUTHOR}</div>
</body></html>'''
fhtml = f'<html><head><meta charset="utf-8"><style>{CSS} body{{width:{W}mm;height:{H}mm;background:{DEEP}}}</style></head><body>{front()}</body></html>'
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(); pg.set_content(html); pg.wait_for_timeout(300)
    pg.pdf(path=f"{OUT}/herb2-world-표지펼침-{VER}.pdf", width=f"{TW}mm", height=f"{TH}mm", print_background=True)
    sc = 1400 / (W/25.4*96)
    pg2 = b.new_page(viewport={"width":int(W/25.4*96)+1,"height":int(H/25.4*96)+1}, device_scale_factor=sc)
    pg2.set_content(fhtml); pg2.wait_for_timeout(300)
    pg2.locator(".front").screenshot(path=f"{OUT}/herb2-world-표지앞-{VER}.png")
    b.close()
print("spread %.1f x %.1f mm, spine %.1f" % (TW, TH, SPINE))

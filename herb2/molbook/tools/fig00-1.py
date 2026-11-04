#!/usr/bin/env python3
"""그림 0-1 세포신호의 공통 지도. 출력: figures/ch00/그림0-1.svg, 그림0-1.png"""
import pathlib, asyncio
R = pathlib.Path(__file__).resolve().parent.parent / "figures" / "ch00"
F = "font-family:'Noto Sans CJK KR','Noto Sans KR',sans-serif"
o = []
def T(x, y, s, size=24, w=400, anchor="middle", fill="#111"):
    o.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="{F};font-size:{size}px;font-weight:{w}" fill="{fill}">{s}</text>')
def hexa(cx, cy, r=26):
    import math
    pts = " ".join(f"{cx + r*math.cos(math.radians(60*i+30)):.1f},{cy + r*math.sin(math.radians(60*i+30)):.1f}" for i in range(6))
    o.append(f'<polygon points="{pts}" fill="#f2a33c" stroke="#7a4a00" stroke-width="3"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.45}" fill="none" stroke="#7a4a00" stroke-width="2.5"/>')
def arrow(pts, dash=False, w=4, col="#222"):
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    o.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" {"stroke-dasharray=\'10 8\'" if dash else ""} marker-end="url(#ah)"/>')
W, H = 1800, 1040
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
o.append('<defs><marker id="ah" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="16" refY="9" orient="auto"><path d="M0,1 L18,9 L0,17 z" fill="#222"/></marker></defs>')
o.append(f'<rect width="{W}" height="{H}" fill="#fff"/>')
# zones
o.append(f'<rect x="0" y="0" width="{W}" height="330" fill="#eef5fb"/>')
o.append(f'<rect x="0" y="400" width="{W}" height="300" fill="#fbf6ea"/>')
T(20, 38, "세포 밖", 26, 700, "start"); T(20, 440, "세포질", 26, 700, "start")
# membrane bilayer
for x in range(10, W, 28):
    for yy, ty in ((338, 347), (392, 383)):
        o.append(f'<circle cx="{x}" cy="{yy}" r="9" fill="#e4c97a" stroke="#8a6d1d" stroke-width="1.5"/>')
        o.append(f'<line x1="{x-3}" y1="{ty}" x2="{x-3}" y2="{365 if yy==338 else 370}" stroke="#8a6d1d" stroke-width="2"/>')
        o.append(f'<line x1="{x+3}" y1="{ty}" x2="{x+3}" y2="{365 if yy==338 else 370}" stroke="#8a6d1d" stroke-width="2"/>')
T(W-20, 316, "세포막(지질 이중층)", 22, 700, "end", "#5a4510")
# 1 GPCR
T(230, 70, "① G 단백질 연결 수용체", 28, 700); T(230, 104, "(GPCR)", 24, 400)
hexa(230, 190); arrow([(230, 222), (230, 262)])
for i in range(7):
    o.append(f'<rect x="{168+i*17}" y="318" width="14" height="94" rx="6" fill="#6b8fd6" stroke="#1f3f86" stroke-width="2"/>')
T(230, 292, "막을 일곱 번 가로지르는 수용체", 20, 400)
for cx, cy, rx, ry, f in ((200, 452, 34, 20, "#8bc28b"), (255, 452, 26, 18, "#c28bc2"), (292, 452, 20, 16, "#c2a28b")):
    o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{f}" stroke="#333" stroke-width="2"/>')
T(200, 457, "α", 22, 700); T(255, 457, "β", 20, 700); T(292, 456, "γ", 18, 700)
T(250, 500, "G 단백질(α·β·γ)이 켜진다", 21, 400)
# 2 ion channel
T(620, 70, "② 이온채널", 28, 700); T(620, 104, "(리간드 개폐)", 24, 400)
hexa(620, 190); arrow([(620, 222), (620, 292)])
o.append('<rect x="580" y="316" width="28" height="98" rx="8" fill="#6b8fd6" stroke="#1f3f86" stroke-width="2"/>')
o.append('<rect x="632" y="316" width="28" height="98" rx="8" fill="#6b8fd6" stroke="#1f3f86" stroke-width="2"/>')
for yy in (330, 372, 414, 456):
    o.append(f'<circle cx="620" cy="{yy}" r="9" fill="#e05a5a" stroke="#7a1f1f" stroke-width="2"/>')
T(690, 462, "Ca²⁺", 22, 700, "start", "#7a1f1f")
T(620, 500, "문이 열려 이온이 흐른다", 21, 400)
# 3 enzyme-linked
T(1010, 70, "③ 효소 연결 수용체", 28, 700); T(1010, 104, "(키나아제형)", 24, 400)
hexa(1010, 190); arrow([(1010, 222), (1010, 280)])
for dx in (-26, 26):
    o.append(f'<rect x="{1010+dx-7}" y="320" width="14" height="92" rx="6" fill="#6b8fd6" stroke="#1f3f86" stroke-width="2"/>')
    o.append(f'<ellipse cx="{1010+dx}" cy="306" rx="18" ry="12" fill="#6b8fd6" stroke="#1f3f86" stroke-width="2"/>')
    o.append(f'<rect x="{1010+dx-17}" y="420" width="34" height="26" rx="8" fill="#9fbf6b" stroke="#3b5a12" stroke-width="2"/>')
for dx in (-48, 48):
    o.append(f'<circle cx="{1010+dx}" cy="470" r="13" fill="#ffd84d" stroke="#8a6d00" stroke-width="2"/>')
    T(1010+dx, 477, "P", 18, 700)
T(1010, 515, "둘이 짝을 지어 서로 인산화한다", 21, 400)
# 4 nuclear receptor
T(1470, 70, "④ 핵수용체", 28, 700); T(1470, 104, "(지용성 리간드)", 24, 400)
hexa(1360, 190); arrow([(1360, 222), (1360, 290)], dash=True)
o.append('<path d="M1360,300 L1360,420" fill="none" stroke="#222" stroke-width="4" stroke-dasharray="10 8"/>')
arrow([(1360, 395), (1360, 452)], dash=True)
o.append('<ellipse cx="1360" cy="478" rx="44" ry="30" fill="#c28bc2" stroke="#4a1f4a" stroke-width="2.5"/>'); T(1360, 486, "수용체", 20, 700)
T(1330, 270, "막을 그대로 통과", 20, 400, "end")
o.append('<ellipse cx="1560" cy="590" rx="190" ry="78" fill="#ffffff" stroke="#555" stroke-width="3" stroke-dasharray="3 7"/>')
T(1560, 540, "핵", 22, 700)
o.append('<path d="M1430,590 q24,-34 48,0 t48,0 t48,0 t48,0" fill="none" stroke="#2f6f3f" stroke-width="5"/>')
o.append('<rect x="1498" y="606" width="86" height="30" rx="6" fill="#ffe7b0" stroke="#7a4a00" stroke-width="2"/>'); T(1541, 628, "반응 요소", 18, 700)
arrow([(1392, 500), (1440, 560)], dash=True)
# convergence strip
steps = [("전달자", "G 단백질·어댑터 단백질"), ("이차전령", "cAMP·IP₃·Ca²⁺"), ("키나아제 연쇄", "PKA·ERK·Akt 등"), ("전사인자", "CREB·NF-κB·Nrf2"), ("세포 반응", "유전자 발현·분비·증식·사멸")]
bx = [30, 390, 750, 1110, 1470]
for (a, b), x in zip(steps, bx):
    o.append(f'<rect x="{x}" y="730" width="300" height="130" rx="20" fill="#eaf3ea" stroke="#2f6f3f" stroke-width="3.5"/>')
    T(x+150, 785, a, 30, 700); T(x+150, 828, b, 21, 400)
for i in range(4):
    arrow([(bx[i]+304, 795), (bx[i+1]-6, 795)], w=5)
arrow([(250, 520), (180, 722)]); arrow([(620, 520), (540, 722)]); arrow([(1010, 540), (900, 722)])
arrow([(1500, 668), (1340, 722)], dash=True)
T(1330, 706, "핵수용체는 리간드가 직접 켜는 전사인자", 20, 400, "end")
T(900, 910, "리간드 → 수용체 → 전달자 → 이차전령 → 키나아제 연쇄 → 전사인자 → 반응", 30, 700)
T(900, 952, "네 입구(①~④)는 달라도, 안쪽으로 가는 길은 이 순서를 따라 합쳐진다", 24, 400)
hexa(60, 1000, 20); T(96, 1008, "= 허브 성분(리간드)", 20, 400, "start")
o.append('<circle cx="420" cy="1000" r="12" fill="#ffd84d" stroke="#8a6d00" stroke-width="2"/>'); T(420, 1006, "P", 14, 700); T(445, 1008, "= 인산기", 20, 400, "start")
o.append('</svg>')
svg = "\n".join(o)
(R / "그림0-1.svg").write_text(svg, encoding="utf-8")
from playwright.async_api import async_playwright
async def go():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        await pg.set_content(f"<body style='margin:0'>{svg}</body>"); await pg.screenshot(path=str(R / "그림0-1.png")); await b.close()
asyncio.run(go()); print("ok")

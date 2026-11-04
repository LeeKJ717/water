#!/usr/bin/env python3
"""그림 1-1 (세 TRP 채널), 그림 1-2 (쓴맛 신호). 출력: figures/ch01/그림1-1.png, 그림1-2.png (+svg)"""
import pathlib, asyncio, math
R = pathlib.Path(__file__).resolve().parent.parent / "figures" / "ch01"; R.mkdir(parents=True, exist_ok=True)
F = "font-family:'Noto Sans CJK KR','Noto Sans KR',sans-serif"
HEAD = '<defs><marker id="ah" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="16" refY="9" orient="auto"><path d="M0,1 L18,9 L0,17 z" fill="#222"/></marker></defs>'
class S:
    def __init__(s, W, H): s.W, s.H, s.o = W, H, [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{HEAD}<rect width="{W}" height="{H}" fill="#fff"/>']
    def T(s, x, y, t, size=24, w=400, a="middle", fill="#111"): s.o.append(f'<text x="{x}" y="{y}" text-anchor="{a}" style="{F};font-size:{size}px;font-weight:{w}" fill="{fill}">{t}</text>')
    def hexa(s, cx, cy, r=28):
        pts = " ".join(f"{cx+r*math.cos(math.radians(60*i+30)):.1f},{cy+r*math.sin(math.radians(60*i+30)):.1f}" for i in range(6))
        s.o.append(f'<polygon points="{pts}" fill="#f2a33c" stroke="#7a4a00" stroke-width="3"/><circle cx="{cx}" cy="{cy}" r="{r*.45}" fill="none" stroke="#7a4a00" stroke-width="2.5"/>')
    def arrow(s, pts, dash=False, w=4): s.o.append(f'<path d="M{" L".join(f"{x},{y}" for x,y in pts)}" fill="none" stroke="#222" stroke-width="{w}" {"stroke-dasharray=\'10 8\'" if dash else ""} marker-end="url(#ah)"/>')
    def rect(s, x, y, w, h, fill, stroke, rx=10, sw=2.5): s.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def circ(s, x, y, r, fill, stroke, sw=2): s.o.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def membrane(s, y0, y1):
        for x in range(10, s.W, 28):
            for yy, ty, my in ((y0+8, y0+17, y0+35), (y1-8, y1-17, y1-40)):
                s.circ(x, yy, 9, "#e4c97a", "#8a6d1d", 1.5)
                for dx in (-3, 3): s.o.append(f'<line x1="{x+dx}" y1="{ty}" x2="{x+dx}" y2="{my}" stroke="#8a6d1d" stroke-width="2"/>')
    def end(s): s.o.append("</svg>"); return "\n".join(s.o)
async def png(svg, W, H, path):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": W, "height": H})
        await pg.set_content(f"<body style='margin:0'>{svg}</body>"); await pg.screenshot(path=str(path)); await b.close()
# ---------- 그림 1-1
s = S(1800, 980)
s.o.append('<rect width="1800" height="330" fill="#eef5fb"/><rect x="0" y="420" width="1800" height="560" fill="#fbf6ea"/>')
s.T(20, 36, "세포 밖", 24, 700, "start"); s.T(20, 462, "감각 신경 말단(세포 안)", 24, 700, "start")
s.membrane(330, 420)
cols = [(300, "고추", "캡사이신", "TRPV1", "뜨겁고 아린 느낌", "캡사이신 · 유해한 열", "#6b8fd6"),
        (900, "박하", "멘톨", "TRPM8", "서늘하고 시원한 느낌", "멘톨 · 시원함~차가움", "#6bbf9f"),
        (1500, "마늘", "알리신", "TRPA1", "찌르는 듯 매운 자극", "알리신 · 겨자 기름 성분", "#c28bc2")]
for x, herb, mol, ch, sens, stim, col in cols:
    s.T(x, 70, f"{herb} → {mol}", 30, 700); s.hexa(x, 160); s.T(x+60, 168, mol, 22, 400, "start")
    s.arrow([(x, 196), (x, 262)])
    s.rect(x-60, 318, 38, 116, col, "#1f3f86"); s.rect(x+22, 318, 38, 116, col, "#1f3f86")
    s.T(x, 300, ch + " 채널", 24, 700)
    for yy in (350, 392, 434, 476): s.circ(x, yy, 9, "#e05a5a", "#7a1f1f")
    s.T(x+60, 480, "Ca²⁺·Na⁺ 유입", 20, 700, "start", "#7a1f1f")
    s.arrow([(x, 500), (x, 580)])
    s.T(x, 612, "막 전위가 올라간다(탈분극)", 22, 400)
    s.o.append(f'<polyline points="{x-150},730 {x-90},730 {x-70},640 {x-50},760 {x-30},730 {x+10},730 {x+30},650 {x+50},750 {x+70},730 {x+150},730" fill="none" stroke="#222" stroke-width="4"/>')
    s.T(x, 790, "활동전위가 뇌로 전해진다", 22, 400)
    s.rect(x-210, 830, 420, 56, "#ffffff", "#2f6f3f", 14, 3.5); s.T(x, 868, sens, 26, 700)
    s.T(x, 925, "열쇠: " + stim, 21, 400)
s.T(900, 970, "세 풀의 분자는 서로 다른 이온채널을 열지만, 신호의 출발 형식은 같다: 채널 개방 → 이온 유입 → 전기 신호", 22, 700)
svg = s.end(); (R/"그림1-1.svg").write_text(svg, encoding="utf-8"); asyncio.run(png(svg, 1800, 980, R/"그림1-1.png"))
# ---------- 그림 1-2
s = S(1800, 900)
s.o.append('<rect width="1800" height="250" fill="#eef5fb"/><rect x="0" y="330" width="1800" height="570" fill="#fbf6ea"/>')
s.T(20, 36, "세포 밖(입 안 또는 장·기도의 내용물)", 24, 700, "start"); s.T(20, 372, "세포 안", 24, 700, "start")
s.membrane(250, 330)
s.T(330, 96, "용담 뿌리: 아마로젠틴", 28, 700); s.hexa(330, 160); s.arrow([(330, 192), (330, 236)])
s.T(620, 110, "쓴 분자는 25종의 사람 TAS2R 수용체 중 일부에", 22, 400, "start"); s.T(620, 144, "넓게 또는 좁게 맞는다", 22, 400, "start")
for i in range(7): s.rect(268+i*18, 238, 15, 106, "#6b8fd6", "#1f3f86", 6, 2)
s.T(330, 232, "", 10)
s.T(330, 392, "TAS2R (GPCR)", 24, 700)
steps = [("G 단백질", "거스트듀신\n(Gα) · Gβγ"), ("PLCβ2", "인지질\n분해 효소"), ("IP₃", "소포체의\nIP₃ 수용체"), ("Ca²⁺ 상승", "세포질\n칼슘 이온"), ("TRPM5", "양이온 채널\n열림"), ("반응", "신경 전달 물질\n·사이토카인 방출")]
x0 = 40
for i, (a, b) in enumerate(steps):
    x = x0 + i*290
    s.rect(x, 470, 250, 170, "#eaf3ea", "#2f6f3f", 18, 3.5); s.T(x+125, 520, a, 29, 700)
    for j, ln in enumerate(b.split("\n")): s.T(x+125, 568+j*30, ln, 21, 400)
    if i: s.arrow([(x-36, 555), (x-4, 555)], w=5)
s.arrow([(330, 410), (165, 462)])
s.T(900, 700, "입 안의 맛세포에서는 이 연쇄가 쓴맛 신호를 만들고, 장 점막 솔 세포와 기도 평활근에서도 같은 부품이 확인된다", 23, 700)
s.T(900, 745, "(Zhang 외, 2013; Luo 외, 2019)", 21, 400)
s.rect(120, 790, 1560, 80, "#ffffff", "#555", 12, 2); s.T(900, 840, "버드나무의 살리신도 장 솔 세포의 Tas2r을 켜 IL-25 분비를 일으킨다(생쥐 실험, Luo 외, 2019)", 24, 400)
svg = s.end(); (R/"그림1-2.svg").write_text(svg, encoding="utf-8"); asyncio.run(png(svg, 1800, 900, R/"그림1-2.png"))
print("ok")

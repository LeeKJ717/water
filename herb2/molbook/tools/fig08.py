#!/usr/bin/env python3
"""그림 8-1 (TLR4-NF-κB 경로와 인플라마좀). 출력 figures/ch08/그림8-1.png"""
import pathlib, asyncio, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
src = (pathlib.Path(__file__).resolve().parent / "fig01.py").read_text(encoding="utf-8").split("# ---------- 그림 1-1")[0]
exec(src.replace('"figures" / "ch01"', '"figures" / "ch08"'))
s = S(1800, 1100)
s.o.append('<line x1="900" y1="30" x2="900" y2="720" stroke="#999" stroke-width="3" stroke-dasharray="12 8"/>')
s.T(450, 45, "① TLR4에서 NF-κB까지", 27, 700)
chain = [("LPS · HMGB1", "#e8f0fb", "#1f3f86"), ("TLR4 / MD-2", "#e8f0fb", "#1f3f86"), ("MyD88", "#fff3c9", "#8a6d1d"),
         ("IKKβ → IκBα 인산화·분해", "#fff3c9", "#8a6d1d"), ("NF-κB(p65) 핵으로 이동", "#eaf5ea", "#2f6f3f"),
         ("TNF · IL-6 · IL-8 · COX-2 전사", "#ffffff", "#555")]
for i, (t, f, c) in enumerate(chain):
    y = 80 + i*105
    s.rect(30, y, 380, 66, f, c, 12, 3); s.T(220, y+42, t, 21, 700)
    if i < len(chain)-1: s.arrow([(220, y+70), (220, y+101)], w=4)
notes = [(80, "감초 글리시리진: HMGB1 억제제로 쓰인다", "(Paudel 외, 2020)"),
         (185, "황금 바이칼레인: MD-2 주머니에 결합,", "LPS가 만드는 MD-2/TLR4 복합체 억제 (Luo 외, 2017)"),
         (395, "생강 D10G: IKKβ의 Cys179와 상호작용", "(Lee 외, 2012; 세포·효소 수준)"),
         (500, "뇌공등 트립톨라이드: DNA 결합은 그대로,", "전사 활성화를 억제 (Qiu 외, 1999; Zhao 외, 2000)"),
         (605, "같은 경로 위에서도 성분마다 닿는 지점이 다르다", "(위 네 곳은 서로 다른 보고이다)")]
for y, a, b in notes:
    s.T(650, y+30, a, 18, 700); s.T(650, y+56, b, 17, 400)
# 오른쪽
s.T(1350, 45, "② 인플라마좀과 STAT3", 27, 700)
chain2 = [("신호 1: NF-κB → pro-IL-1β·NLRP3 발현", "#eaf5ea", "#2f6f3f"), ("신호 2: NLRP3 + NEK7 조립", "#fff3c9", "#8a6d1d"),
          ("카스파아제-1 활성", "#fff3c9", "#8a6d1d"), ("IL-1β 성숙 · GSDMD 절단", "#ffffff", "#555"),
          ("IL-6 → JAK2 → STAT3", "#e8f0fb", "#1f3f86")]
for i, (t, f, c) in enumerate(chain2):
    y = 80 + i*105
    s.rect(930, y, 400, 66, f, c, 12, 3); s.T(1130, y+42, t, 20, 700)
    if i < len(chain2)-1: s.arrow([(1130, y+70), (1130, y+101)], w=4)
n2 = [(80, "Luo 외(2017): 바이칼레인이 NLRP3 활성과", "IL-1β 발현도 줄였다 (생쥐 장염 모델)"),
      (185, "오리도닌: NLRP3 Cys279에 공유결합, NEK7 상호작용 차단", "(He 외, 2018; 허브 성분의 예)"),
      (290, "파르테놀리드: 카스파아제-1 단백분해 활성을 직접 억제", "(Juliana 외, 2010)"),
      (395, "GSDMD 절단형이 세포사(pyroptosis)와 IL-1β 분비에 필요", "(He 외, 2015)"),
      (500, "보스웰리아 AKBA: SHP-1을 늘려 STAT3 탈인산화", "(Kunnumakkara 외, 2009; 다발골수종 세포)")]
for y, a, b in n2:
    s.T(1560, y+30, a, 16, 700); s.T(1560, y+54, b, 15, 400)
# 아래: 사람
s.o.append('<line x1="30" y1="735" x2="1770" y2="735" stroke="#555" stroke-width="3" stroke-dasharray="12 8"/>')
s.T(900, 775, "③ 사람에서 잰 결과와 독성", 26, 700)
cards = [("황금 바이칼린", "관상동맥질환+류마티스 374명", "500 mg, 12주, 위약 대조 (Hang 외, 2018)"),
         ("뇌공등 추출물", "당뇨병성 신증 65명, 6개월", "발사르탄과 비교 (Ge 외, 2013)"),
         ("강황+보스웰릭산 혼합", "골관절염 201명, 12주", "혼합 제제라 단독 효과 분리 불가 (Haroyan 외, 2018)"),
         ("트립톨라이드 독성", "동물·세포: 간독성 보고 다수", "LPS·TNF-α 감수성 (Yuan 외, 2020)")]
for i, (a, b, c) in enumerate(cards):
    x = 40 + i*440
    s.rect(x, 805, 400, 150, "#ffffff", "#555", 14, 2.5); s.T(x+200, 850, a, 24, 700); s.T(x+200, 893, b, 19, 400); s.T(x+200, 930, c, 15, 400)
s.rect(60, 985, 1680, 90, "#ffffff", "#555", 14, 2.5)
s.T(900, 1027, "NF-κB를 누르는 성분은 염증을 줄이지만, 같은 경로가 세포의 생존 신호이기도 하다", 22, 700)
s.T(900, 1060, "트립톨라이드는 NF-κB 의존 생존 신호(FLIP)를 낮춰 간을 TNF-α에 민감하게 만들었다 (동물, Yuan 외, 2020)", 18, 400)
svg = s.end(); (R/"그림8-1.svg").write_text(svg, encoding="utf-8"); asyncio.run(png(svg, 1800, 1100, R/"그림8-1.png")); print("ok")

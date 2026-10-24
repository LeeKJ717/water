#!/usr/bin/env python3
"""쪽별 아래 빈 비율 점검: python3 tools/check-layout.py build/x.pdf  (15% 초과 쪽 표시)"""
import sys, subprocess, tempfile, glob, os
from PIL import Image
pdf = sys.argv[1]; d = tempfile.mkdtemp()
subprocess.run(['pdftoppm', '-r', '40', '-png', pdf, d + '/p'], check=True)
for f in sorted(glob.glob(d + '/p-*.png')):
    im = Image.open(f).convert('L'); w, h = im.size
    top = int(h * .085); bot = int(h * .90)   # 본문 영역(여백·쪽번호 제외)
    last = top
    for y in range(bot, top, -1):
        if min(im.crop((0, y, w, y + 1)).getdata()) < 200: last = y; break
    blank = (bot - last) / (bot - top)
    n = int(os.path.basename(f)[2:-4])
    print(f'쪽 {n:3d} 아래 빈칸 {blank*100:4.0f}%' + ('  <-- 15% 초과' if blank > .15 and last > top else ('  (빈 쪽)' if last == top else '')))

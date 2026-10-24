import re, subprocess, weasyprint
md=open('herb2-handoff-v1.md',encoding='utf-8').read()
html=subprocess.run(['pandoc','-f','markdown','-t','html5','--toc','--toc-depth=2','-s','--metadata','title=herb2 작업 인수인계서 (v1)','-o','-'],input=md,capture_output=True,text=True,encoding='utf-8').stdout
# TOC -> own block with page numbers
html=re.sub(r'<nav id="TOC".*?</nav>',lambda m:m.group(0).replace('<nav id="TOC"','<nav id="TOC"'),html,flags=re.S)
css='''
@page{size:A4;margin:20mm 18mm 22mm 18mm;@bottom-center{content:counter(page);font-size:9pt;font-family:"Noto Sans CJK KR"}}
body{font-family:"Noto Sans CJK KR";font-size:10pt;line-height:1.55;max-width:none}
h1.title{font-size:20pt;margin:0 0 6mm}
h2{font-size:14pt;border-bottom:1px solid #888;padding-bottom:2pt;margin-top:8mm}
h3{font-size:11.5pt}
table{border-collapse:collapse;width:100%;margin:3mm 0 1mm;page-break-inside:avoid;font-size:9pt}
th,td{border:1px solid #777;padding:2pt 5pt;vertical-align:top}th{background:#e8e8e8}
pre{background:#f1f1f1;padding:4pt;white-space:pre-wrap;word-break:break-all;font-size:8.5pt}
code{font-size:9pt}
nav#TOC{page-break-after:always}
nav#TOC ul{list-style:none;padding-left:1em}nav#TOC>ul{padding-left:0}
nav#TOC a::after{content:leader('.') target-counter(attr(href),page)}
nav#TOC a{text-decoration:none;color:#000}
header#title-block-header{margin-bottom:6mm}
'''
html=html.replace('</head>','<style>'+css+'</style></head>')
html=html.replace('<nav id="TOC" role="doc-toc">','<nav id="TOC" role="doc-toc"><h2 style="border:0">목차</h2>')
weasyprint.HTML(string=html).write_pdf('herb2-handoff-v1.pdf')

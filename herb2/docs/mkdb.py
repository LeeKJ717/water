import sqlite3, re, os
db=sqlite3.connect('herb2.db')
db.executescript('''
create table if not exists rules(id integer primary key, section text, item text, detail text, src text default 'bookrule2 v1');
create table if not exists layout(key text primary key, value text, status text, note text);
create table if not exists cover_spec(key text primary key, value text, note text);
create table if not exists chapters(no integer primary key, part text, title text, scope_region text, pages_target int, md_path text, body text, status text default '목차미정');
create table if not exists refs(id integer primary key, chapter_no int, apa7 text, doi text, herbdb_id text);
create table if not exists figures(id integer primary key, label text, chapter_no int, title text, kind text, src_path text, data_path text, bw_variant text, status text);
create table if not exists tables_meta(id integer primary key, label text, chapter_no int, title text, csv_path text, fits_one_page int default 1, status text);
create table if not exists sources_db(snapshot text, key text, value text);
create table if not exists docs(name text primary key, mime text, saved text, content blob);
create table if not exists todo(id integer primary key, seq int, task text, status text default '대기');
''')
md=open('bookrule2.md',encoding='utf-8').read() if os.path.exists('bookrule2.md') else ''
sec=None
for l in md.splitlines():
    m=re.match(r'## (.+)',l)
    if m: sec=m.group(1); continue
    m=re.match(r'- (.+)',l)
    if m and sec: db.execute('insert into rules(section,item,detail) values(?,?,?)',(sec,'',m.group(1)))
    m=re.match(r'\d+\. (.+)',l)
    if m and sec: db.execute('insert into rules(section,item,detail) values(?,?,?)',(sec,'',m.group(1)))
L=[('trim','','미정','판형(예: 신국판 152x225mm) 결정 필요'),('body_font','','미정','본문 글꼴·크기'),('ref_font','본문-1pt','확정','bookrule2 5'),('ref_leading','본문보다 좁게','확정',''),('page_target','300-400','확정','쪽'),('page_numbers','every page bottom + TOC','확정',''),('table_break','금지(한 쪽 안)','확정',''),('editions','color + bw','확정',''),('margin','','미정','')]
db.executemany('insert or ignore into layout values(?,?,?,?)',L)
C=[('flap_width_mm','100','양쪽 날개'),('front_cover_px','1400','앞표지만'),('back_flap','과학과영성출판사 대중서 썸네일+제목','목록 미수령'),('spread','앞표지+뒤표지+책등+날개','책등 폭은 쪽수·용지 확정 후')]
db.executemany('insert or ignore into cover_spec values(?,?,?)',C)
S=[('2026-10-23','works_total','2706'),('2026-10-23','with_pdf_url','2378'),('2026-10-23','pdf_downloaded','0'),('2026-10-23','global','1619'),('2026-10-23','east-asia','577'),('2026-10-23','south-asia','349'),('2026-10-23','americas','330'),('2026-10-23','oceania','200'),('2026-10-23','middle-east','200'),('2026-10-23','europe','200'),('2026-10-23','africa','200')]
db.executemany('insert into sources_db values(?,?,?)',S)
T=['z840에서 meta finished 확인','pdf 단계 백그라운드 실행','질의·지역별 논문 집계 후 전세계서 목차 확정(chapters에 입력)','비논문 데이터셋 내려받기(probe2 결과 먼저 확인)','판형·글꼴 등 layout 미정값 결정','장별 집필(APA·그림·표 번호)','컬러/흑백 PDF 빌드','표지 펼침면 제작','지역별 책 반복']
db.executemany('insert into todo(seq,task) values(?,?)',list(enumerate(T,1)))
for f in ['herb2-handoff-v1.md','herb2-handoff-v1.pdf','bookrule2.md']:
    if os.path.exists(f): db.execute('insert or replace into docs values(?,?,?,?)',(f,'',  '2026-10-23',open(f,'rb').read()))
db.commit()
for t in ['rules','layout','cover_spec','chapters','refs','figures','tables_meta','sources_db','docs','todo']:
    print(t,db.execute(f'select count(*) from {t}').fetchone()[0])

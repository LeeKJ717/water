#!/usr/bin/env python3
"""molbook 표적별 논문 확장 수집기 (OpenAlex, z840에서 실행, 표준 라이브러리만 사용).
사용: python3 molcrawl.py <출력폴더> [페이지수=2] [--dry]
출력폴더 안에 molbook-db-v1.sqlite(papers, queries, hits), raw/*.jsonl, logs/ 를 만든다. 재실행하면 끝난 질의는 건너뛴다."""
import sys, os, json, time, sqlite3, urllib.request, urllib.parse, urllib.error

Q = [
# (장, 허브, 영문 질의)
("0","개똥쑥","artemisinin mechanism heme iron activation"),("0","버드나무","salicin salicylic acid cyclooxygenase mechanism willow"),
("1","고추","capsaicin TRPV1"),("1","박하","menthol TRPM8"),("1","마늘","allicin TRPA1 garlic"),("1","용담","bitter taste receptor TAS2R plant bitter compounds"),("1","공통","TRP channels plant natural products"),
("2","강황","curcumin bioavailability"),("2","후추","piperine bioavailability enhancer"),("2","녹차","EGCG green tea catechin bioavailability absorption"),("2","공통","herbal glycoside intestinal absorption tight junction"),
("3","인삼","ginsenoside compound K gut microbiota"),("3","석류","ellagic acid urolithin gut microbiota"),("3","센나","sennoside gut bacteria activation"),("3","감초","glycyrrhizin glycyrrhetinic acid gut bacteria"),("3","공통","short-chain fatty acids GPR43 GPR41"),("3","공통","bile acids TGR5 FXR plant polyphenols"),("3","공통","polyphenol metabolites aryl hydrocarbon receptor"),
("4","세인트존스워트","hyperforin PXR CYP3A4 St John's wort"),("4","세인트존스워트","St John's wort P-glycoprotein drug interaction"),("4","밀크시슬","silymarin CYP inhibition drug interaction"),("4","공통","herb-drug interaction cytochrome P450 review"),("4","공통","pregnane X receptor herbal"),
("5","카바","kavalactones GABA-A receptor"),("5","발레리안","valerenic acid GABA-A receptor"),("5","발레리안","valerian GABA receptor mechanism"),("5","대마","cannabidiol receptor mechanism CB1 CB2"),("5","대마","THC CB1 receptor signaling"),("5","양귀비","morphine mu opioid receptor signaling"),("5","카바","kava sodium channel"),("5","공통","serotonin receptor herbal"),
("6","버드나무","salicylic acid cyclooxygenase inhibition"),("6","생강","gingerol cyclooxygenase lipoxygenase"),("6","갈란투스","galantamine acetylcholinesterase Galanthus"),("6","개똥쑥","artemisinin heme iron activation"),("6","공통","plant natural product acetylcholinesterase inhibitor"),
("7","황련","berberine AMPK"),("7","계피","cinnamon insulin signaling cinnamaldehyde"),("7","녹차","EGCG AMPK mTOR"),("7","공통","AMPK mTOR natural product"),("7","공통","PI3K Akt herbal medicine"),
("8","황금","baicalin NF-kappaB"),("8","보스웰리아","boswellic acid 5-lipoxygenase NF-kB"),("8","뇌공등","triptolide NF-kB"),("8","감초","glycyrrhizin HMGB1 TLR4"),("8","공통","NLRP3 inflammasome natural product"),("8","공통","STAT3 herbal compounds"),("8","공통","TLR4 plant polyphenol"),
("9","홉","8-prenylnaringenin estrogen receptor hops"),("9","칡대두","isoflavone estrogen receptor beta"),("9","인삼","ginsenoside steroid receptor glucocorticoid estrogen"),("9","공통","phytoestrogen nuclear receptor"),("9","공통","PPAR natural products"),
("10","브로콜리","sulforaphane Nrf2 Keap1"),("10","로즈마리","carnosic acid Nrf2 rosemary"),("10","강황","curcumin Nrf2"),("10","공통","hormesis polyphenols"),("10","공통","antioxidant response element phytochemicals"),
("11","호장근","resveratrol SIRT1"),("11","녹차","EGCG DNA methyltransferase"),("11","브로콜리","sulforaphane histone deacetylase"),("11","공통","plant polyphenols epigenetic microRNA"),("11","호장근","Polygonum cuspidatum resveratrol"),
("12","황련","berberine mitochondrial complex I"),("12","개똥쑥","artemisinin apoptosis cancer cells ferroptosis"),("12","강황","curcumin apoptosis caspase p53"),("12","공통","autophagy natural products AMPK ULK1"),("12","공통","Bcl-2 Bax natural compounds apoptosis"),
("13","은행","Ginkgo biloba neuroprotection mechanism"),("13","브라미","Bacopa monnieri bacoside cognitive"),("13","인삼","ginsenoside neuroprotection"),("13","세인트존스워트","St John's wort depression serotonin reuptake"),("13","공통","BDNF TrkB herbal"),("13","공통","neuroinflammation microglia plant compounds"),
("14","황련","berberine glucose lipid metabolism"),("14","여주","Momordica charantia charantin AMPK"),("14","호로파","fenugreek 4-hydroxyisoleucine insulin"),("14","계피","cinnamon type 2 diabetes"),("14","공통","GLUT4 translocation natural products"),("14","공통","GLP-1 secretion plant compounds"),
("15","디기탈리스","digoxin Na/K ATPase digitalis"),("15","단삼","Salvia miltiorrhiza tanshinone cardiovascular"),("15","산사","hawthorn Crataegus heart"),("15","마늘","garlic allicin endothelial nitric oxide"),("15","단삼","warfarin herb interaction danshen"),("15","공통","platelet aggregation herbal"),
("16","주목","paclitaxel microtubule Taxus"),("16","일일초","vincristine tubulin Catharanthus"),("16","희수","camptothecin topoisomerase I"),("16","메이애플","podophyllotoxin etoposide topoisomerase II"),("16","공통","spindle assembly checkpoint natural products"),
("17","공통","network pharmacology traditional medicine critique"),("17","공통","molecular docking natural products limitations"),("17","단삼","Salvia miltiorrhiza network pharmacology"),("17","황금","baicalein network pharmacology"),("17","공통","PAINS natural products"),
("18","강황","curcumin PAINS"),("18","강황","curcumin clinical trials bioavailability"),("18","녹차","EGCG clinical trial"),("18","호장근","resveratrol bioavailability concentration"),("18","공통","in vitro to in vivo extrapolation natural products"),("18","공통","synergy multi-component herbal medicine"),
("19","카바","kava hepatotoxicity mechanism"),("19","광방기","aristolochic acid DNA adducts"),("19","콤프리","pyrrolizidine alkaloids comfrey hepatotoxicity"),("19","마황","ephedrine adrenergic ephedra safety"),("19","뇌공등","Tripterygium hepatotoxicity"),("19","공통","herb-induced liver injury mechanism"),
("20","공통","pharmacogenomics herbal CYP2D6 CYP2C19"),("20","인삼","gut microbiome responders ginsenoside"),("20","공통","multi-omics herbal medicine"),("20","공통","precision herbal medicine"),
]
API = "https://api.openalex.org/works"
SEL = "id,doi,title,publication_year,primary_location,authorships,cited_by_count,abstract_inverted_index,is_retracted,type"

def abstract(inv):
    if not inv: return ""
    pos = {}
    for w, ps in inv.items():
        for p in ps: pos[p] = w
    return " ".join(pos[k] for k in sorted(pos))

class Quota(Exception): pass

def fetch(q, page, tries=5):
    params = {"search": q, "filter": "type:article,has_abstract:true", "sort": "cited_by_count:desc", "per-page": "100", "page": str(page), "select": SEL}
    if os.environ.get("OPENALEX_KEY"): params["api_key"] = os.environ["OPENALEX_KEY"]
    url = API + "?" + urllib.parse.urlencode(params)
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "molbook-crawler/1"}), timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                ra = int(e.headers.get("Retry-After", "0") or 0)
                if ra > 600: raise Quota(f"daily limit, reset in {ra}s")
                time.sleep(5 * (i + 1)); continue
            if e.code in (500, 502, 503, 504): time.sleep(5 * (i + 1)); continue
            raise
        except Exception:
            time.sleep(3 * (i + 1))
    return None

def main():
    out = sys.argv[1]; pages = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 2
    dry = "--dry" in sys.argv
    os.makedirs(os.path.join(out, "raw"), exist_ok=True); os.makedirs(os.path.join(out, "logs"), exist_ok=True)
    db = sqlite3.connect(os.path.join(out, "molbook-db-v1.sqlite"))
    db.executescript("""CREATE TABLE IF NOT EXISTS papers(id TEXT PRIMARY KEY, doi TEXT, title TEXT, year INT, journal TEXT, authors TEXT, cited INT, abstract TEXT, is_retracted INT, type TEXT);
CREATE TABLE IF NOT EXISTS queries(qid INTEGER PRIMARY KEY, chapter TEXT, herb TEXT, q TEXT UNIQUE, n INT, done INT DEFAULT 0);
CREATE TABLE IF NOT EXISTS hits(qid INT, paper_id TEXT, rnk INT, PRIMARY KEY(qid, paper_id));""")
    for ch, herb, q in Q:
        db.execute("INSERT OR IGNORE INTO queries(chapter,herb,q) VALUES(?,?,?)", (ch, herb, q))
    db.commit()
    if dry: print(len(Q), "queries"); return
    log = open(os.path.join(out, "logs", "molcrawl.log"), "a", encoding="utf-8")
    for qid, ch, herb, q in db.execute("SELECT qid,chapter,herb,q FROM queries WHERE done=0 ORDER BY qid").fetchall():
        rank = 0; n = 0
        raw = open(os.path.join(out, "raw", f"q{qid:03d}.jsonl"), "w", encoding="utf-8")
        for p in range(1, pages + 1):
            try: d = fetch(q, p)
            except Quota as e:
                raw.close(); db.commit(); print("STOP", e, flush=True); sys.exit(2)
            if d is None: raw.close(); print("FAIL", qid, flush=True); sys.exit(3)
            if not d.get("results"): break
            for w in d["results"]:
                rank += 1; raw.write(json.dumps(w, ensure_ascii=False) + "\n")
                loc = (w.get("primary_location") or {}).get("source") or {}
                au = [(a.get("author") or {}).get("display_name") for a in (w.get("authorships") or [])][:12]
                db.execute("INSERT OR IGNORE INTO papers VALUES(?,?,?,?,?,?,?,?,?,?)", (w["id"], w.get("doi"), w.get("title"), w.get("publication_year"), loc.get("display_name"), json.dumps(au, ensure_ascii=False), w.get("cited_by_count"), abstract(w.get("abstract_inverted_index")), 1 if w.get("is_retracted") else 0, w.get("type")))
                db.execute("INSERT OR IGNORE INTO hits VALUES(?,?,?)", (qid, w["id"], rank)); n += 1
            time.sleep(0.3)
        raw.close()
        db.execute("UPDATE queries SET n=?, done=1 WHERE qid=?", (n, qid)); db.commit()
        log.write(f"{qid}\t{ch}\t{herb}\t{q}\t{n}\n"); log.flush()
        print(qid, ch, q, n, flush=True)
    tot = db.execute("SELECT COUNT(*) FROM papers").fetchone()[0]; print("papers", tot)

main()

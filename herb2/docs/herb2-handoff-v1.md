# herb2 작업 인수인계서 (v1)

작성일: 2026-10-23 · 대상: 전세계 허브 대중서 제작 프로젝트(herb_db → herb2)

## 1. 프로젝트 목표

전 세계에서 약리적으로 사용해 온 전통 허브와 현대에도 널리 쓰이는 허브를 다룬 대중서(300~400쪽, 대중서이나 전문적)를 만든다. 순서는 다음과 같다.

1. 먼저 **전세계 허브서** 1권을 만든다.
2. 이후 **지역별 허브서**를 지역마다 각각 만든다(동아시아, 남아시아, 중동, 아프리카, 유럽, 아메리카, 오세아니아).

제작 규칙은 `bookrule2.md`(v1)에 있고, 이 폴더의 `herb2.db`에 규칙 항목별로 저장해 두었다(6장 참조).

## 2. 접속 경로와 환경

| 구분 | 내용 |
|---|---|
| 작업 노트북 | win14 (Windows, PowerShell), 바탕화면 `daily3` |
| 중계 서버 | z440 (`z440@100.90.3.79`, Tailscale) |
| 수집 서버 | z840 (`z840@192.168.0.84`) |
| 접속 형식 | `ssh -J z440@100.90.3.79 z840@192.168.0.84 '명령'` (비밀번호 2회: z440, z840) |
| 파일 전송 | `scp -J z440@100.90.3.79 파일 z840@192.168.0.84:/home/z840/이름` |
| DB 위치 | `/data/safe/dball2/herb_db/herbdb-v1.sqlite` |
| 로그 | `/data/safe/dball2/herb_db/logs/` (meta.out, meta2.out, meta3.out, herbcrawl.log) |

표 1. 작업 환경 요약

## 3. 지금까지 한 일

### 3.1 데이터 소스 조사

공개 데이터셋 후보를 제시했고 z840에서 접속 가능 여부를 점검했다(probe1: 18개 사이트). 비논문 데이터셋(LOTUS, COCONUT, CMAUP, IMPPAT, HERB, KampoDB, OASIS 등)의 실제 내려받기는 아직 시작하지 않았다. probe2(브라우저 UA·API 엔드포인트 점검) 결과는 아직 보고되지 않았다.

### 3.2 herb_db 폴더 구조 (z840)

`/data/safe/dball2/herb_db/` 아래에 `pdf/`, `raw/`, `logs/`가 있고 논문 DB는 `herbdb-v1.sqlite`이다.

### 3.3 논문 수집기 herbcrawl (OpenAlex)

| 버전 | z840 위치 | 상태 |
|---|---|---|
| v1 | `/home/z840/herbcrawl.py` | cursor 방식, 401 오류와 status 버그 |
| v2 | `/home/z840/herbcrawl2.py` | 401 처리 추가, status 수정 |
| v3 | `/home/z840/herbcrawl3.py` | **현재 사용.** 키 없이 `page=` 방식 |

표 2. 수집기 버전

실행: `python3 /home/z840/herbcrawl3.py meta|pdf|status`

- `meta`: OpenAlex에서 20개 질의별로 인용수 내림차순 최대 1,000편(PERQ)의 서지·초록을 저장한다.
- `pdf`: 오픈액세스 PDF 주소가 있는 논문을 200편씩 내려받아 `pdf/<id>.pdf`로 저장한다(최대 40MB, `%PDF` 시작 확인, 4스레드, sha256 기록).
- `status`: 전체·지역별·질의별 건수를 출력한다.

### 3.4 DB 현황 (마지막 확인 시점)

| 항목 | 값 |
|---|---|
| 논문 전체 | 2,706 |
| 초록 있음 | 2,706 |
| PDF 주소 있음 | 2,378 |
| PDF 내려받음 | 0 |

표 3. herbdb-v1 논문 수 (마지막 확인 시점, 수집 진행 중이라 계속 증가)

| 지역 태그 | 논문 수 |
|---|---|
| global | 1,619 |
| east-asia | 577 |
| south-asia | 349 |
| americas | 330 |
| oceania | 200 |
| middle-east | 200 |
| europe | 200 |
| africa | 200 |

표 4. 지역별 논문 수 (마지막 확인 시점)

20개 질의 전체 구성: global 9개(약리, 민족식물학, 임상, 약물상호작용, 식물화학, 네트워크약리, 안전성, 역사, 표준화), east-asia 3개(중국, 일본 캄포, 한국), south-asia 2개(아유르베다, 유나니·시다), middle-east 1개, africa 1개, europe 1개, americas 2개, oceania 1개. 질의가 끝나면 로그에 `meta finished`가 찍힌다. 마지막 확인 시 global/pharmacology가 800편 지점이었고 페이지당 약 16~18초였다.

## 4. 해결한 문제와 교훈

| 문제 | 원인 | 해결 |
|---|---|---|
| status 오류 `no such column: region` | progress 테이블에 region 열 없음 | `select qkey,n,done from progress`로 수정 |
| HTTP 401 | OpenAlex가 cursor 방식에 API 키를 요구 (`API key required for cursor paging`) | `page=` 방식(v3), 키는 선택 |
| 출력이 비어 보임 | 명령이 아직 실행 중 | PowerShell 프롬프트가 돌아올 때까지 기다림 |
| 원격 셸 종료 | ssh 한 줄 안의 `pkill -f 패턴`이 자기 명령줄과 일치 | `pkill`을 쓰지 않음 |
| Downloads에서 파일명이 달라짐 | 다운로드 시 밑줄·하이픈 제거 | 와일드카드 `*herbcrawl*v3*` 사용 |

표 5. 오류와 해결

OpenAlex 사정: 2026년 2월부터 API 키와 사용 예산제가 적용되었다(키 없이 하루 0.10달러, 목록 호출 1,000회당 0.10달러). 목록 호출은 약 100회라 키 없이도 하루 예산 안이다. `page=` 방식은 질의당 10,000건까지, 페이지당 최대 200건이다.

## 5. 책 제작 규칙 요약 (bookrule2 v1)

1. 작업은 `Desktop\daily3\<책제목 폴더>`에서 하고 `git init` 후 수정마다 커밋한다.
2. 순서는 DB 논문 수 확인 → 목차 → 장별 집필이다.
3. 새 용어는 처음 나올 때 full name을 쓰고, 발견·연구 과정을 소설처럼 서술한다.
4. 한자어는 한국어 발음으로 표기한다.
5. 출처는 APA 7th, 매 장 끝에 넣고 글자는 본문보다 1pt 작게, 줄간격은 좁게 해도 된다.
6. 모든 그림과 표에 번호와 제목을 붙이고, 표는 두 쪽에 걸치지 않게 한다.
7. 쪽 위아래에 큰 빈 여백이 없게 한다. 목차에 쪽번호, 모든 쪽 하단에 쪽번호.
8. 내지는 컬러판과 흑백 인쇄판을 모두 만든다.
9. 표지는 펼침면, 날개 100mm, 앞표지 1400px, 뒤날개에 과학과영성출판사 대중서 썸네일과 제목.
10. 원고는 장별 마크다운, 참고문헌, 그림 원본·데이터, 표 데이터를 PDF와 별도로 저장해 PDF를 재빌드할 수 있게 한다.

## 6. herb2 폴더와 조판 DB

`Desktop\daily3\herb2` 구조:

| 폴더/파일 | 용도 |
|---|---|
| `herb2.db` | 조판 관련 모든 데이터(SQLite) |
| `chapters/` | 장별 원고 마크다운 (`ch01.md` …) |
| `refs/` | 장별 APA 참고문헌 |
| `figures/` | 그림 원본·데이터 |
| `tables/` | 표 데이터(CSV) |
| `cover/` | 표지 자료 |
| `build/` | 빌드 산출물(컬러·흑백 PDF) |
| `docs/` | 인수인계서, bookrule2 |
| `bookrule2.md` | 제작 규칙 사본 |

표 6. herb2 폴더 구조

`herb2.db` 테이블: `rules`(규칙 항목), `layout`(판형·글꼴·여백 등 조판 변수), `cover_spec`(표지 사양), `chapters`(장 골격과 원고), `refs`(참고문헌), `figures`, `tables_meta`, `sources_db`(herb_db 수집 통계 스냅샷), `docs`(MD·PDF 원본 BLOB), `todo`(남은 일). 실제 판형·글꼴·쪽수 등 미정 값은 `layout`에서 `value`가 비어 있고 `status='미정'`이다.

## 7. 남은 일 (이어서 할 순서)

1. z840에서 `meta finished` 확인 후 `pdf` 단계를 백그라운드로 실행한다.
2. 질의·지역별 논문 수를 집계하여 **전세계 허브서 목차(300~400쪽)** 를 확정한다. 확정된 목차는 `herb2.db`의 `chapters`에 넣는다.
3. 비논문 데이터셋(LOTUS, COCONUT, CMAUP, NPASS, IMPPAT, HERB, KampoDB, OASIS, KTKP, EMA HMPC, WHO 모노그래프, DSLD, POWO·WFO·GBIF)을 `raw/`에 내려받고 출처·라이선스·일자를 기록한다. probe2 결과를 먼저 확인한다.
4. 판형·글꼴 등 조판 변수를 정하고, 장별 집필(APA 참고문헌, 그림·표 번호) 후 컬러/흑백 PDF를 빌드한다.
5. 표지 펼침면(날개 100mm, 앞표지 1400px, 뒤날개 썸네일)을 제작한다.
6. 전세계서 완료 후 지역별 책을 지역 태그별로 반복한다.

## 8. 이어서 시작하는 명령

z840 수집 상태 확인:

```
ssh -J z440@100.90.3.79 z840@192.168.0.84 'tail -n 1 /data/safe/dball2/herb_db/logs/meta3.out; python3 /home/z840/herbcrawl3.py status | head -n 12'
```

`meta finished`가 보이면 PDF 수집 시작:

```
ssh -J z440@100.90.3.79 z840@192.168.0.84 'nohup python3 /home/z840/herbcrawl3.py pdf > /data/safe/dball2/herb_db/logs/pdf.out 2>&1 &'
```

import json
import re

with open('bayflow/sellerbox_reversed/draw-radar/data/items.json', 'r', encoding='utf-8') as f:
    draw_items = json.load(f)

with open('bayflow/sellerbox_reversed/redeem-radar/data/finds.json', 'r', encoding='utf-8') as f:
    finds = json.load(f)['items']

print(f"Loaded {len(draw_items)} draw items and {len(finds)} finds items.")

# Special high-margin curated viral & reselling items
curated_celeb = [
    {
        "id": "celeb-curated-01",
        "region": "kr",
        "regionBadge": "🇰🇷 한국",
        "source": "instagram",
        "sourceLabel": "인스타그램 바이럴",
        "kind": "celeb",
        "title": "뉴진스 X 파워퍼프걸 한정 인형 키링 글로벌 리셀가 4배 폭등",
        "summary": "라인프렌즈 스퀘어 성수 현장 전량 품절 · 정가 2.2만 원 ➔ eBay $135.00 체결 · 미국/호주/동남아 바이어 오더 집중.",
        "url": "https://www.instagram.com/explore/tags/newjeans/",
        "startAt": "2026-11-01T00:00:00+09:00",
        "endAt": "2026-11-20T23:59:00+09:00",
        "brand": "NewJeans x LineFriends",
        "place": "성수 라인프렌즈 스퀘어 / 온라인",
        "tags": ["연예인", "아이돌", "뉴진스", "키링", "글로벌리셀", "인스타바이럴"]
    },
    {
        "id": "celeb-curated-02",
        "region": "kr",
        "regionBadge": "🇰🇷 한국",
        "source": "x_twitter",
        "sourceLabel": "X(트위터) 트렌드",
        "kind": "celeb",
        "title": "방탄소년단(BTS) 진 솔로 앨범 발메 기념 오피셜 팝업 공식 MD 드랍",
        "summary": "하이브 오피셜 한정판 키링·후드·포토카드 럭키드로우 세트. 첫날 번개장터/크림 프리미엄 +85% 형성, 해외 배송 수요 급증.",
        "url": "https://x.com/search?q=BTS%20POPUP",
        "startAt": "2026-11-05T10:00:00+09:00",
        "endAt": "2026-11-22T20:00:00+09:00",
        "brand": "BTS Jin x HYBE",
        "place": "서울 성수동 팝업스토어",
        "tags": ["연예인", "아이돌", "방탄소년단", "bts", "한정판MD", "포토카드", "팝업스토어"]
    },
    {
        "id": "celeb-curated-03",
        "region": "kr",
        "regionBadge": "🇰🇷 한국",
        "source": "threads",
        "sourceLabel": "스레드 핫토픽",
        "kind": "celeb",
        "title": "에스파(aespa) 'Whiplash' 성수 팝업 익스클루시브 의류 & 아크릴 스탠드",
        "summary": "SM 엔터테인먼트 공식 성수 팝업. 오프라인 현장 단독 미공개 포토카드(미공포) 럭키드로우로 글로벌 팬덤 오픈런 대란.",
        "url": "https://www.threads.net/search?q=aespa%20popup",
        "startAt": "2026-10-31T10:00:00+09:00",
        "endAt": "2026-11-12T20:00:00+09:00",
        "brand": "aespa x SM ENTERTAINMENT",
        "place": "성수동 무신사 스퀘어",
        "tags": ["연예인", "아이돌", "에스파", "aespa", "포카", "성수팝업"]
    },
    {
        "id": "celeb-curated-04",
        "region": "kr",
        "regionBadge": "🇰🇷 한국",
        "source": "tiktok",
        "sourceLabel": "틱톡 K-POP",
        "kind": "celeb",
        "title": "세븐틴(SEVENTEEN) 스타디움 투어 공식 캐럿봉 ver.3 및 한정판 트레카",
        "summary": "월드투어 현장 수령 한정판 트레이딩 카드 팩. 이베이 10팩 번들 $180~$220에 실거래 완료, K-Packet 100g 최적화.",
        "url": "https://www.tiktok.com/tag/seventeen",
        "startAt": "2026-11-02T00:00:00+09:00",
        "endAt": "2026-11-25T23:59:00+09:00",
        "brand": "PLEDIS / HYBE",
        "place": "위버스샵 / 현장 부스",
        "tags": ["연예인", "아이돌", "세븐틴", "캐럿봉", "포토카드", "트레카"]
    },
    {
        "id": "celeb-curated-05",
        "region": "kr",
        "regionBadge": "🇰🇷 한국",
        "source": "kream",
        "sourceLabel": "크림 K-POP",
        "kind": "celeb",
        "title": "아이브(IVE) 공식 캐릭터 '미니브(MINIVE)' 봉제인형 키링 시즌2 오프라인 한정",
        "summary": "스타쉽 스퀘어 팝업 단독 발매. 안유진·장원영 캐릭터 키링 당일 완판, 해외 리셀가 정가 2.4만 원 대비 3배 이상 호가.",
        "url": "https://kream.co.kr/",
        "startAt": "2026-11-04T10:30:00+09:00",
        "endAt": "2026-11-17T20:00:00+09:00",
        "brand": "IVE x STARSHIP",
        "place": "더현대 서울 지하 2층 아이코닉스퀘어",
        "tags": ["연예인", "아이돌", "아이브", "미니브", "장원영", "키링"]
    },
    {
        "id": "celeb-curated-06",
        "region": "kr",
        "regionBadge": "🇰🇷 한국",
        "source": "x_twitter",
        "sourceLabel": "X(트위터) 트렌드",
        "kind": "celeb",
        "title": "스트레이키즈(Stray Kids) 'dominATE' 월드투어 공식 SKZOO 오프라인 팝업 인형",
        "summary": "JYP 오피셜 SKZOO 미니 플러시 키링 8종. 북미/남미/유럽 바이어 수요 폭발, 이베이 풀세트 $320 호가.",
        "url": "https://x.com/search?q=SKZOO",
        "startAt": "2026-11-03T10:00:00+09:00",
        "endAt": "2026-11-19T20:00:00+09:00",
        "brand": "JYP ENTERTAINMENT",
        "place": "롯데백화점 잠실점 팝업존",
        "tags": ["연예인", "아이돌", "스트레이키즈", "skzoo", "jyp", "인형키링"]
    },
    {
        "id": "celeb-curated-07",
        "region": "kr",
        "regionBadge": "🇰🇷 한국",
        "source": "gnews",
        "sourceLabel": "언론 보도",
        "kind": "celeb",
        "title": "우정사업본부, T1 '페이커' 롤드컵 기념우표 굿즈 & 507개 한정판 메탈카드 출시",
        "summary": "e스포츠 사상 최초 공식 우표 굿즈. 전 세계 507개 한정 메탈 넘버링 카드는 이베이 $350~$500 호가 예상 수집형 고마진 매물.",
        "url": "https://www.epost.go.kr/",
        "startAt": "2026-10-23T09:00:00+09:00",
        "endAt": "2026-11-15T18:00:00+09:00",
        "brand": "T1 x 우정사업본부",
        "place": "인터넷우체국 / 중앙우체국",
        "tags": ["연예인", "e스포츠", "페이커", "t1", "한정판굿즈", "우표"]
    },
    {
        "id": "celeb-curated-08",
        "region": "kr",
        "regionBadge": "🇰🇷 한국",
        "source": "popply",
        "sourceLabel": "팝플리(Popply)",
        "kind": "celeb",
        "title": "보이넥스트도어(BOYNEXTDOOR) 더현대 서울 '쁘넥도 in Sweet Dreams' 팝업스토어",
        "summary": "하이브 산하 KOZ 엔터 공식 캐릭터 굿즈. 오프라인 단독 수면안대 인형키링 및 파자마 세트 해외 리셀 프리미엄 +110%.",
        "url": "https://popply.co.kr/",
        "startAt": "2026-10-21T10:30:00+09:00",
        "endAt": "2026-11-06T20:00:00+09:00",
        "brand": "BOYNEXTDOOR x HYBE",
        "place": "더현대 서울 지하 1층 대행사장",
        "tags": ["연예인", "아이돌", "보이넥스트도어", "보넥도", "쁘넥도", "더현대서울"]
    },
    {
        "id": "celeb-curated-09",
        "region": "kr",
        "regionBadge": "🇰🇷 한국",
        "source": "popply",
        "sourceLabel": "팝플리(Popply)",
        "kind": "celeb",
        "title": "TWS(투어스) 컴백 기념 하이브 사옥 팝업스토어 오픈 및 한정 오프라인 럭키드로우",
        "summary": "용산 하이브 본사 사옥 인근 단독 팝업존. 현장 앨범 구매자 대상 미공개 셀카 홀로그램 포토카드 세트 증정.",
        "url": "https://popply.co.kr/",
        "startAt": "2026-11-01T11:00:00+09:00",
        "endAt": "2026-11-14T20:00:00+09:00",
        "brand": "TWS x PLEDIS",
        "place": "서울 용산구 하이브 사옥 팝업 스페이스",
        "tags": ["연예인", "아이돌", "투어스", "tws", "하이브", "럭키드로우"]
    },
    {
        "id": "celeb-curated-10",
        "region": "kr",
        "regionBadge": "🇰🇷 한국",
        "source": "popply",
        "sourceLabel": "팝플리(Popply)",
        "kind": "celeb",
        "title": "아일릿(ILLIT) 'BREAK EVEN' 명동 & 홍대 릴레이 오프라인 팝업스토어",
        "summary": "빌리프랩 공식 MD. 글리터 키링 및 오버핏 그래픽 후디 한정 발매. 일본/중국 관광객 현장 사입 대란.",
        "url": "https://popply.co.kr/",
        "startAt": "2026-10-25T11:00:00+09:00",
        "endAt": "2026-11-10T21:00:00+09:00",
        "brand": "ILLIT x BELIFT LAB",
        "place": "명동 플래그십 스토어 & 홍대 스퀘어",
        "tags": ["연예인", "아이돌", "아일릿", "illit", "하이브", "명동팝업"]
    }
]

curated_fashion = [
    {
        "id": "fashion-curated-01",
        "region": "kr",
        "regionBadge": "🇰🇷 한국",
        "source": "instagram",
        "sourceLabel": "인스타그램 바이럴",
        "kind": "fashion",
        "title": "저스틴 비버 스트릿 브랜드 '스카이라크(SKYLRK)' 성수 팝업 서울 익스클루시브 드랍",
        "summary": "13년 만의 깜짝 방한으로 새벽 1시부터 영하권 오픈런 대란. 서울 단독 한정 후디/비니 이베이 $280~$350 즉시 체결 중.",
        "url": "https://www.instagram.com/skylrk/",
        "startAt": "2026-10-22T11:00:00+09:00",
        "endAt": "2026-11-10T20:00:00+09:00",
        "brand": "SKYLRK by Justin Bieber",
        "place": "서울 성수동 연무장길 스카이라크 팝업룸",
        "tags": ["패션", "스트릿", "스카이라크", "저스틴비버", "성수팝업", "오픈런"]
    },
    {
        "id": "fashion-curated-02",
        "region": "kr",
        "regionBadge": "🇰🇷 한국",
        "source": "kream",
        "sourceLabel": "크림 KREAM",
        "kind": "fashion",
        "title": "산산기어(SANSAN GEAR) 26FW 2차 드랍 고프코어 윈드브레이커 & 테크 팬츠",
        "summary": "국내 고프코어 원탑 브랜드. 발매 3분 만에 전 사이즈 품절, 해외 셀러박스 소싱 타깃 1순위. 이베이 180~240달러 수출 효자 아이템.",
        "url": "https://kream.co.kr/",
        "startAt": "2026-11-04T18:00:00+09:00",
        "endAt": "2026-11-15T23:59:00+09:00",
        "brand": "SANSAN GEAR",
        "place": "무신사 / 산산기어 공식 온라인 / 성수 쇼룸",
        "tags": ["패션", "스트릿", "고프코어", "산산기어", "윈드브레이커", "크림"]
    },
    {
        "id": "fashion-curated-03",
        "region": "kr",
        "regionBadge": "🇰🇷 한국",
        "source": "tiktok",
        "sourceLabel": "틱톡 패션",
        "kind": "fashion",
        "title": "떠그클럽(Thug Club) 드래곤 레더 자켓 글로벌 한정 100벌 드랍",
        "summary": "에이셉 라키 등 미국 탑 래퍼 착용으로 글로벌 바이럴. 국내 정가 58만 원 ➔ 해외 이베이 호가 $1,200선 돌파, 고마진 역소싱 매물.",
        "url": "https://www.tiktok.com/tag/thugclub",
        "startAt": "2026-11-02T20:00:00+09:00",
        "endAt": "2026-11-12T23:59:00+09:00",
        "brand": "Thug Club",
        "place": "떠그클럽 이태원 쇼룸 / 글로벌 온라인",
        "tags": ["패션", "스트릿", "떠그클럽", "레더자켓", "틱톡바이럴"]
    },
    {
        "id": "fashion-curated-04",
        "region": "kr",
        "regionBadge": "🇰🇷 한국",
        "source": "popply",
        "sourceLabel": "팝플리(Popply)",
        "kind": "fashion",
        "title": "'승리의 여신: 니케' 4주년 기념 무신사 컬래버 성수 팝업 한정 MA-1 & 이타백 발매",
        "summary": "11월 6일 성수동 무신사 테라스 그랜드 오픈. 한정판 자켓, 그래픽 후디, 이타백 현장 단독 판매. 서브컬처 해외 바이어 오픈런 예고.",
        "url": "https://popply.co.kr/",
        "startAt": "2026-11-06T11:00:00+09:00",
        "endAt": "2026-11-19T20:00:00+09:00",
        "brand": "NIKKE x MUSINSA",
        "place": "무신사 테라스 성수",
        "tags": ["패션", "스트릿", "무신사", "니케", "성수팝업", "한정판자켓"]
    },
    {
        "id": "fashion-curated-05",
        "region": "kr",
        "regionBadge": "🇰🇷 한국",
        "source": "nike",
        "sourceLabel": "NIKE SNKRS",
        "kind": "fashion",
        "title": "코르테이즈(Corteiz) X 나이키 샥스 R419 및 협업 스트릿 어패럴 캡슐",
        "summary": "영국 스트릿 씬 최고 인기 브랜드 코르테이즈의 나이키 협업. 국내 스니커헤드 및 해외 리셀 시장 $260~$320 프리미엄 형성.",
        "url": "https://www.nike.com/kr/launch",
        "startAt": "2026-11-01T10:00:00+09:00",
        "endAt": "2026-11-10T23:59:00+09:00",
        "brand": "Corteiz x NIKE",
        "place": "나이키 SNKRS 드로우",
        "tags": ["패션", "스트릿", "나이키", "코르테이즈", "스니커즈", "드로우"]
    },
    {
        "id": "fashion-curated-06",
        "region": "kr",
        "regionBadge": "🇰🇷 한국",
        "source": "kream",
        "sourceLabel": "크림 KREAM",
        "kind": "fashion",
        "title": "마틴킴(Matin Kim) 아코디언 미니 레더 지갑 & 시그니처 로고 볼캡 성수 리스탁",
        "summary": "성수 하우스바이 오픈런 1순위. 일본/중국/대만 관광객 쓸어가기 아이템, 해외 이베이 $85~$120 마진율 45% 안정적 출하.",
        "url": "https://kream.co.kr/",
        "startAt": "2026-11-03T11:00:00+09:00",
        "endAt": "2026-11-18T20:00:00+09:00",
        "brand": "Matin Kim",
        "place": "성수 플래그십 하우스바이 / 한남 쇼룸",
        "tags": ["패션", "스트릿", "마틴킴", "지갑", "성수쇼룸", "해외직구대란"]
    },
    {
        "id": "fashion-curated-07",
        "region": "kr",
        "regionBadge": "🇰🇷 한국",
        "source": "nike",
        "sourceLabel": "NIKE SNKRS",
        "kind": "fashion",
        "title": "나이키 크라이오샷 티엠포 '94 OG 남성 스니커즈 글로벌 리트로그린 드로우",
        "summary": "축구화 아카이브에서 영감받은 테라스 컬처 스트릿 슈즈. 블록코어 패션 트렌드 직격탄, 황금 사이즈 270~285mm 리셀가 급등.",
        "url": "https://www.nike.com/kr/launch",
        "startAt": "2026-11-02T10:00:00+09:00",
        "endAt": "2026-11-08T10:30:00+09:00",
        "brand": "NIKE",
        "place": "나이키 공식 온라인 SNKRS",
        "tags": ["패션", "스트릿", "나이키", "티엠포", "블록코어", "스니커즈"]
    },
    {
        "id": "fashion-curated-08",
        "region": "kr",
        "regionBadge": "🇰🇷 한국",
        "source": "popply",
        "sourceLabel": "팝플리(Popply)",
        "kind": "fashion",
        "title": "노스페이스 화이트라벨 성수 팝업 : PROJECT DOWN 한정판 패딩 쇼룸",
        "summary": "한국 독점 기획 라인 노스페이스 화이트라벨. 일본/유럽 바이어 타깃 숏패딩 눕시 및 한정 컬러웨이 이베이 $380 체결 매물.",
        "url": "https://popply.co.kr/",
        "startAt": "2026-10-24T11:00:00+09:00",
        "endAt": "2026-11-15T20:00:00+09:00",
        "brand": "THE NORTH FACE WHITE LABEL",
        "place": "서울 성동구 성수이로 팝업스토어",
        "tags": ["패션", "스트릿", "노스페이스", "화이트라벨", "패딩", "성수팝업"]
    }
]

# Classification keywords
celeb_keys = [
    '아이돌', '연예인', 'bts', '방탄', '뉴진스', '에스파', '블랙핑크', '세븐틴', '스트레이키즈',
    '아이브', '르세라핌', '라이즈', '투어스', 'tws', '보이넥스트도어', '보넥도', '엔하이픈',
    '투모로우바이투게더', '아일릿', '포카', '포토카드', '팬덤', '응원봉', '하이브', '페이커',
    'kpop', '콘서트', '김동현', '변우석', '손석구', '정은채', '미야오', '최강희', '전지현',
    '포레스텔라', '스텔라이브', '김나영', '리센느', '엔시티', 'nct', '트와이스', '뮤직', '엠디'
]

fashion_keys = [
    '패션', '스트릿', '나이키', '아디다스', '슈프림', '스투시', '무신사', '크림', 'kream',
    '스니커즈', '신발', '의류', '자켓', '후드', '고프코어', '산산기어', '떠그클럽', '조던',
    '코르테이즈', '아워레가시', '코치', '스카이라크', '저스틴비버', '버버리', '노스페이스',
    '안다르', '지그재그', '에어맥스', '보메로', '다운', '패딩', '아웃도어', '어패럴',
    '던스트', '마리떼', '마틴킴', '아더에러', '인사일런스', '살로몬', '아식스', '르시스',
    '컨템포러리', '여성복', '남성복', '쇼룸', '블록코어', '에어포스', '조던11', '부츠', '코트'
]

acc_keys = ['키링', '인형', '악세사리', '텀블러', '머그', '산리오', '스타벅스', '치이카와', '먼작귀', '라부부', '모남희', '가방', '백팩', '지갑', '키체인', '베어리스타']
viral_keys = ['바이럴', '틱톡', '인스타', '스레드', '트위터', '품절대란', '오픈런', '대란', '핫이슈', '줄서기']
draw_keys = ['드로우', '래플', '발매', '응모', '당첨', 'snkrs', '릴리즈']

def clean_text(s):
    if not s: return ""
    return re.sub(r'\s+', ' ', str(s)).strip()

processed_items = []
seen_titles = set()

# First add curated items
for item in curated_celeb + curated_fashion:
    processed_items.append(item)
    seen_titles.add(item['title'].lower()[:20])

# Process raw draw_items and finds
raw_pool = draw_items + finds
for idx, r in enumerate(raw_pool):
    title = clean_text(r.get('title') or r.get('name') or '')
    if not title or len(title) < 4:
        continue
    
    t_short = title.lower()[:25]
    if t_short in seen_titles:
        continue
    seen_titles.add(t_short)

    summary = clean_text(r.get('summary') or r.get('content') or r.get('desc') or '')
    if not summary:
        summary = f"실시간 발매·팝업·트렌드 정보: {title}"

    matched_tags = r.get('matched', []) or []
    full_text = (title + " " + summary + " " + " ".join(matched_tags)).lower()

    # Determine kind
    kind = 'news'
    if any(k in full_text for k in celeb_keys):
        kind = 'celeb'
    elif any(k in full_text for k in fashion_keys):
        kind = 'fashion'
    elif any(k in full_text for k in acc_keys):
        kind = 'acc'
    elif any(k in full_text for k in viral_keys):
        kind = 'viral'
    elif any(k in full_text for k in draw_keys):
        kind = 'draw'
    else:
        orig_k = (r.get('kind') or '').lower()
        if orig_k in ['popup', 'reserve']:
            kind = 'popup'
        elif orig_k in ['goods', 'event']:
            kind = 'goods'
        else:
            kind = 'news'

    source = r.get('source') or 'popply'
    if 'nike' in full_text or 'snkrs' in full_text: source = 'nike'
    elif 'kream' in full_text or '크림' in full_text: source = 'kream'
    elif 'instagram' in full_text or '인스타' in full_text: source = 'instagram'
    elif 'tiktok' in full_text or '틱톡' in full_text: source = 'tiktok'
    elif 'threads' in full_text or '스레드' in full_text: source = 'threads'
    elif 'cgv' in full_text or '메가박스' in full_text or '롯데시네마' in full_text: source = 'cinema'
    elif 'news' in str(r.get('link', '')) or 'naver' in str(r.get('link', '')): source = 'gnews'

    # Build tags
    tags = list(set(matched_tags))
    if kind == 'celeb': tags.extend(['연예인', '아이돌', 'kpop', '팬덤굿즈'])
    elif kind == 'fashion': tags.extend(['패션', '스트릿', '의류', '스니커즈'])
    elif kind == 'acc': tags.extend(['악세사리', '키링', '인형'])
    elif kind == 'viral': tags.extend(['바이럴', 'sns트렌드', '품절대란'])
    elif kind == 'draw': tags.extend(['드로우', '래플'])
    elif kind == 'popup': tags.extend(['팝업', '성수팝업'])
    elif kind == 'goods': tags.extend(['영화관md', '캐릭터굿즈'])
    else: tags.extend(['실시간뉴스'])

    item_obj = {
        "id": f"radar-{kind}-{len(processed_items) + 1}",
        "region": "kr",
        "regionBadge": "🇰🇷 한국",
        "source": source,
        "sourceLabel": r.get('sourceLabel') or source.upper(),
        "kind": kind,
        "title": title,
        "summary": summary[:220] + ("..." if len(summary) > 220 else ""),
        "url": r.get('link') or r.get('url') or '#',
        "startAt": r.get('startAt') or "2026-11-01T10:00:00+09:00",
        "endAt": r.get('endAt') or "2026-11-20T20:00:00+09:00",
        "brand": r.get('brand') or "TREND RADAR",
        "place": r.get('place') or r.get('location') or "온·오프라인",
        "tags": tags[:6]
    }
    processed_items.append(item_obj)

print(f"Total processed radar items: {len(processed_items)}")

kind_counts = {}
for item in processed_items:
    k = item['kind']
    kind_counts[k] = kind_counts.get(k, 0) + 1

print("Final kind breakdown:")
for k, count in sorted(kind_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  - {k}: {count}건")

with open('bayflow/data/draw_radar_items.json', 'w', encoding='utf-8') as f:
    json.dump(processed_items, f, ensure_ascii=False, indent=2)

print("Saved to bayflow/data/draw_radar_items.json successfully!")

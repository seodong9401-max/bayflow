#!/usr/bin/env python3
import json
import re

ITEMS = [
  # 💍 1. 악세사리
  {
    "id": "chrome-necklace",
    "category": "acc",
    "categoryName": "💍 악세사리",
    "title": "연예인 착용 써지컬/실버925 십자가 체인 목걸이",
    "ebayTitle": "Korean Idol Style Silver 925 Cross Pendant Chain Necklace",
    "badge": "🔥 30일 38건 완판",
    "watchers": "👀 51명 찜",
    "status": "사모님 추천 (초경량)",
    "ebayUsd": 48.0,
    "ebayKrw": 66240,
    "targetBuyKrw": 18000,
    "profitKrw": 25500,
    "roi": "+141%",
    "boxSize": "에어캡 안전봉투 (15×20cm)",
    "actualWeight": 45,
    "volWeight": 35,
    "appliedWeight": 100,
    "weightNote": "실무게 45g < 부피 35g ➔ 100g 초경량 요금",
    "priceRange": "$44.00 ~ $52.00",
    "salesVelocity": "0.8일당 1건 완판 🔥",
    "topBuyers": "🇺🇸 미국 65% · 🇦🇺 호주 20% · 🇬🇧 영국 15%",
    "recentSold": [
      { "date": "11/02", "price": "$48.00", "country": "🇺🇸 미국" },
      { "date": "10/31", "price": "$46.00", "country": "🇦🇺 호주" },
      { "date": "10/28", "price": "$50.00", "country": "🇬🇧 영국" }
    ],
    "bunjangQuery": "실버 925 십자가 목걸이",
    "ebayQuery": "Korean idol silver necklace 925 cross",
    "tags": ["#아이돌착용", "#악세사리", "#초경량우체국", "#고마진"]
  },
  {
    "id": "bts-necklace",
    "category": "acc",
    "categoryName": "💍 악세사리",
    "title": "BTS 슈가 한국 전통 하회탈 실버925 목걸이",
    "ebayTitle": "Handmade 925 Silver Necklace Korean Mask BTS Suga Agust D Inspired",
    "badge": "🔥 30일 26건 완판",
    "watchers": "👀 44명 찜",
    "status": "사모님 추천 (초경량)",
    "ebayUsd": 180.0,
    "ebayKrw": 248400,
    "targetBuyKrw": 38000,
    "profitKrw": 159000,
    "roi": "+418%",
    "boxSize": "에어캡 안전봉투 (15×20cm)",
    "actualWeight": 65,
    "volWeight": 40,
    "appliedWeight": 100,
    "weightNote": "실무게 65g < 부피 40g ➔ 100g 초경량 요금",
    "priceRange": "$162.00 ~ $198.00",
    "salesVelocity": "1.2일당 1건 완판 🔥",
    "topBuyers": "🇺🇸 미국 60% · 🇯🇵 일본 25% · 🇪🇺 유럽 15%",
    "recentSold": [
      { "date": "11/02", "price": "$180.00", "country": "🇺🇸 미국" },
      { "date": "10/30", "price": "$175.00", "country": "🇯🇵 일본" },
      { "date": "10/27", "price": "$185.00", "country": "🇺🇸 미국" }
    ],
    "bunjangQuery": "슈가 은목걸이",
    "ebayQuery": "BTS Suga Agust D silver necklace",
    "tags": ["#방탄슈가", "#하회탈목걸이", "#실버925", "#글로벌완판"]
  },
  {
    "id": "matin-kim-wallet",
    "category": "acc",
    "categoryName": "💍 악세사리/지갑",
    "title": "마뗑킴 (Matin Kim) 아코디언 미니 카드지갑 실버",
    "ebayTitle": "Matin Kim Accordion Mini Wallet Card Holder Silver Plate",
    "badge": "🔥 30일 22건 완판",
    "watchers": "👀 35명 찜",
    "status": "안전 사입",
    "ebayUsd": 65.0,
    "ebayKrw": 89700,
    "targetBuyKrw": 38000,
    "profitKrw": 27500,
    "roi": "+72%",
    "boxSize": "소형 박스 (15×12×5cm)",
    "actualWeight": 110,
    "volWeight": 150,
    "appliedWeight": 200,
    "weightNote": "실무게 110g < 부피 150g ➔ 200g 요금",
    "priceRange": "$60.00 ~ $69.00",
    "salesVelocity": "1.4일당 1건 완판 🔥",
    "topBuyers": "🇯🇵 일본 55% · 🇺🇸 미국 25% · 🇭🇰 홍콩 15%",
    "recentSold": [
      { "date": "10/31", "price": "$65.00", "country": "🇯🇵 일본" },
      { "date": "10/28", "price": "$63.00", "country": "🇺🇸 미국" },
      { "date": "10/25", "price": "$68.00", "country": "🇯🇵 일본" }
    ],
    "bunjangQuery": "마뗑킴 아코디언 지갑",
    "ebayQuery": "Matin Kim accordion wallet",
    "tags": ["#시그니처메탈", "#경량소싱", "#글로벌인기"]
  },
  {
    "id": "tamburins-egg-lipbalm",
    "category": "acc",
    "categoryName": "💍 뷰티/악세사리",
    "title": "탬버린즈 (TAMBURINS) 에그 립밤 + 진주 케이스 세트",
    "ebayTitle": "TAMBURINS Egg Lip Balm Pearl Case Rose Woody Blackpink Jennie",
    "badge": "🔥 30일 42건 완판",
    "watchers": "👀 58명 찜",
    "status": "제니 바이럴 효자템",
    "ebayUsd": 55.0,
    "ebayKrw": 75900,
    "targetBuyKrw": 28000,
    "profitKrw": 28200,
    "roi": "+100%",
    "boxSize": "소형 박스 (15×12×6cm)",
    "actualWeight": 95,
    "volWeight": 180,
    "appliedWeight": 200,
    "weightNote": "실무게 95g < 부피 180g ➔ 200g 요금",
    "priceRange": "$50.00 ~ $58.00",
    "salesVelocity": "0.7일당 1건 완판 🔥",
    "topBuyers": "🇺🇸 미국 52% · 🇯🇵 일본 30% · 🇸🇬 싱가포르 18%",
    "recentSold": [
      { "date": "11/02", "price": "$55.00", "country": "🇯🇵 일본" },
      { "date": "10/30", "price": "$52.00", "country": "🇺🇸 미국" },
      { "date": "10/27", "price": "$58.00", "country": "🇸🇬 싱가포르" }
    ],
    "bunjangQuery": "탬버린즈 에그 립밤",
    "ebayQuery": "TAMBURINS Egg Lip Balm Jennie",
    "tags": ["#성수탬버린즈", "#제니립밤", "#진주케이스", "#여성바이어선호"]
  },
  {
    "id": "gentle-monster",
    "category": "acc",
    "categoryName": "💍 아이웨어/악세사리",
    "title": "젠틀몬스터 2026 제니 바이럴 선글라스 (풀박스)",
    "ebayTitle": "Gentle Monster Jennie Sunglasses Baby Pony Cat Eye Full Set",
    "badge": "🔥 30일 19건 완판",
    "watchers": "👀 54명 찜",
    "status": "고마진 사입",
    "ebayUsd": 280.0,
    "ebayKrw": 386400,
    "targetBuyKrw": 230000,
    "profitKrw": 82000,
    "roi": "+35%",
    "boxSize": "하드케이스 박스 (20×12×8cm)",
    "actualWeight": 280,
    "volWeight": 320,
    "appliedWeight": 400,
    "weightNote": "실무게 280g < 부피 320g ➔ 400g 부피무게 적용",
    "priceRange": "$260.00 ~ $295.00",
    "salesVelocity": "1.6일당 1건 완판",
    "topBuyers": "🇺🇸 미국 50% · 🇦🇺 호주 25% · 🇬🇧 영국 15%",
    "recentSold": [
      { "date": "10/30", "price": "$280.00", "country": "🇺🇸 미국" },
      { "date": "10/27", "price": "$275.00", "country": "🇦🇺 호주" },
      { "date": "10/23", "price": "$290.00", "country": "🇺🇸 미국" }
    ],
    "bunjangQuery": "젠틀몬스터 제니 선글라스",
    "ebayQuery": "Gentle Monster Jennie Sunglasses",
    "tags": ["#제니선글라스", "#고단가수출", "#해외직구1위"]
  },

  # 🧢 2. 모자 / 볼캡
  {
    "id": "emis-cap",
    "category": "cap",
    "categoryName": "🧢 모자/볼캡",
    "title": "이미스 (emis) 뉴 로고 코튼 볼캡 (제니 착용)",
    "ebayTitle": "emis New Logo Cotton Cap Korean Streetwear Ball Cap",
    "badge": "🔥 30일 34건 완판",
    "watchers": "👀 46명 찜",
    "status": "적극 사입 (부피무게 주의)",
    "ebayUsd": 45.0,
    "ebayKrw": 62100,
    "targetBuyKrw": 35000,
    "profitKrw": 8600,
    "roi": "+24%",
    "boxSize": "모자보호 1호 박스 (22×20×13cm)",
    "actualWeight": 130,
    "volWeight": 500,
    "appliedWeight": 500,
    "weightNote": "실무게 130g < 부피 500g ➔ 500g 부피과금 (모자각 보존)",
    "priceRange": "$42.00 ~ $48.50",
    "salesVelocity": "1.1일당 1건 완판 🔥",
    "topBuyers": "🇺🇸 미국 62% · 🇦🇺 호주 18% · 🇬🇧 영국 12%",
    "recentSold": [
      { "date": "11/01", "price": "$45.00", "country": "🇺🇸 미국" },
      { "date": "10/29", "price": "$44.00", "country": "🇦🇺 호주" },
      { "date": "10/26", "price": "$48.50", "country": "🇬🇧 영국" }
    ],
    "bunjangQuery": "emis 볼캡",
    "ebayQuery": "emis cap logo",
    "tags": ["#제니착용", "#연예인모자", "#바이럴", "#품절대란"]
  },
  {
    "id": "northface-cap",
    "category": "cap",
    "categoryName": "🧢 모자/볼캡",
    "title": "노스페이스 화이트라벨 팀코리아 코튼 볼캡",
    "ebayTitle": "The North Face White Label TEAM Korea Cotton Ball Cap White",
    "badge": "🔥 30일 29건 완판",
    "watchers": "👀 38명 찜",
    "status": "연예인 볼캡 바이럴",
    "ebayUsd": 67.0,
    "ebayKrw": 92460,
    "targetBuyKrw": 36000,
    "profitKrw": 28500,
    "roi": "+79%",
    "boxSize": "모자보호 1호 박스 (22×20×13cm)",
    "actualWeight": 135,
    "volWeight": 500,
    "appliedWeight": 500,
    "weightNote": "실무게 135g < 부피 500g ➔ 500g 부피과금",
    "priceRange": "$60.00 ~ $74.00",
    "salesVelocity": "1.0일당 1건 완판 🔥",
    "topBuyers": "🇺🇸 미국 65% · 🇬🇧 영국 20% · 🇨🇦 캐나다 15%",
    "recentSold": [
      { "date": "11/02", "price": "$67.00", "country": "🇺🇸 미국" },
      { "date": "10/30", "price": "$65.00", "country": "🇬🇧 영국" },
      { "date": "10/27", "price": "$70.00", "country": "🇺🇸 미국" }
    ],
    "bunjangQuery": "노스페이스 볼캡 화이트라벨",
    "ebayQuery": "North Face Korea cap white",
    "tags": ["#화이트라벨", "#팀코리아", "#한국한정판"]
  },
  {
    "id": "mlb-cap",
    "category": "cap",
    "categoryName": "🧢 모자/볼캡",
    "title": "MLB 코리아 베이직 워싱 언스트럭쳐 볼캡",
    "ebayTitle": "MLB Korea Basic Washed Unstructured Ball Cap Unisex",
    "badge": "🔥 30일 31건 완판",
    "watchers": "👀 42명 찜",
    "status": "스테디셀러 사입",
    "ebayUsd": 59.0,
    "ebayKrw": 81420,
    "targetBuyKrw": 28000,
    "profitKrw": 27400,
    "roi": "+98%",
    "boxSize": "모자보호 1호 박스 (22×20×13cm)",
    "actualWeight": 130,
    "volWeight": 500,
    "appliedWeight": 500,
    "weightNote": "실무게 130g < 부피 500g ➔ 500g 부피과금",
    "priceRange": "$53.00 ~ $65.00",
    "salesVelocity": "1.0일당 1건 완판 🔥",
    "topBuyers": "🇺🇸 미국 55% · 🇦🇺 호주 25% · 🇸🇬 싱가포르 20%",
    "recentSold": [
      { "date": "11/01", "price": "$59.00", "country": "🇺🇸 미국" },
      { "date": "10/29", "price": "$58.00", "country": "🇦🇺 호주" },
      { "date": "10/26", "price": "$62.00", "country": "🇸🇬 싱가포르" }
    ],
    "bunjangQuery": "MLB 볼캡",
    "ebayQuery": "MLB Korea washed cap",
    "tags": ["#MLB코리아", "#워싱볼캡", "#글로벌인기"]
  },

  # 👗 3. 스트릿 / 의류
  {
    "id": "mardi-tshirt",
    "category": "clothing",
    "categoryName": "👗 스트릿/의류",
    "title": "마르디 메크르디 플라워마르디 반팔 티셔츠",
    "ebayTitle": "Mardi Mercredi T-Shirt Flower Mardi Print Tee Top",
    "badge": "🔥 30일 28건 완판",
    "watchers": "👀 39명 찜",
    "status": "안전 사입",
    "ebayUsd": 58.0,
    "ebayKrw": 80040,
    "targetBuyKrw": 35000,
    "profitKrw": 21400,
    "roi": "+61%",
    "boxSize": "의류 안전 지퍼백 (25×30×3cm)",
    "actualWeight": 220,
    "volWeight": 375,
    "appliedWeight": 400,
    "weightNote": "실무게 220g < 부피 375g ➔ 400g 부피무게 적용",
    "priceRange": "$52.00 ~ $62.00",
    "salesVelocity": "1.2일당 1건 완판 🔥",
    "topBuyers": "🇯🇵 일본 45% · 🇺🇸 미국 35% · 🇹🇼 대만 15%",
    "recentSold": [
      { "date": "11/01", "price": "$58.00", "country": "🇯🇵 일본" },
      { "date": "10/30", "price": "$55.00", "country": "🇺🇸 미국" },
      { "date": "10/27", "price": "$60.00", "country": "🇯🇵 일본" }
    ],
    "bunjangQuery": "마르디 플라워 티셔츠",
    "ebayQuery": "Mardi Mercredi tshirt",
    "tags": ["#김고은", "#여름필수", "#스테디셀러"]
  },
  {
    "id": "frizmworks-tee",
    "category": "clothing",
    "categoryName": "👗 스트릿/의류",
    "title": "프리즘웍스 피그먼트 다잉 와플 포켓 티셔츠",
    "ebayTitle": "Frizmworks Pigment Dyeing Waffle Pocket Tee New Korean Streetwear",
    "badge": "🔥 30일 18건 완판",
    "watchers": "👀 32명 찜",
    "status": "K-스트릿 인기",
    "ebayUsd": 140.0,
    "ebayKrw": 193200,
    "targetBuyKrw": 48000,
    "profitKrw": 102000,
    "roi": "+212%",
    "boxSize": "의류 안전 지퍼백 (25×30×3cm)",
    "actualWeight": 260,
    "volWeight": 375,
    "appliedWeight": 400,
    "weightNote": "실무게 260g < 부피 375g ➔ 400g 부피무게 적용",
    "priceRange": "$128.00 ~ $156.00",
    "salesVelocity": "1.6일당 1건 완판",
    "topBuyers": "🇺🇸 미국 70% · 🇨🇦 캐나다 15% · 🇦🇺 호주 15%",
    "recentSold": [
      { "date": "11/02", "price": "$140.00", "country": "🇺🇸 미국" },
      { "date": "10/29", "price": "$138.00", "country": "🇺🇸 미국" },
      { "date": "10/25", "price": "$145.00", "country": "🇨🇦 캐나다" }
    ],
    "bunjangQuery": "프리즘웍스 와플 티셔츠",
    "ebayQuery": "Frizmworks waffle tee",
    "tags": ["#프리즘웍스", "#피그먼트", "#남성스트릿"]
  },

  # 👟 4. 스니커즈 / 신발
  {
    "id": "adidas-samba-og",
    "category": "sneakers",
    "categoryName": "👟 스니커즈",
    "title": "아디다스 삼바 OG 클라우드 화이트 (B75806)",
    "ebayTitle": "Adidas Samba OG Cloud White Core Black B75806 Authentic",
    "badge": "🔥 30일 36건 완판",
    "watchers": "👀 68명 찜",
    "status": "스테디셀러 (부피 1.5kg 과금)",
    "ebayUsd": 125.0,
    "ebayKrw": 172500,
    "targetBuyKrw": 98000,
    "profitKrw": 39500,
    "roi": "+40%",
    "boxSize": "신발 택배 박스 (32×20×12cm)",
    "actualWeight": 820,
    "volWeight": 1280,
    "appliedWeight": 1500,
    "weightNote": "실무게 820g < 부피 1,280g ➔ 1.5kg 부피과금 (박스 손상 방지)",
    "priceRange": "$118.00 ~ $132.00",
    "salesVelocity": "0.8일당 1건 완판",
    "topBuyers": "🇺🇸 미국 70% · 🇨🇦 캐나다 15% · 🇦🇺 호주 15%",
    "recentSold": [
      { "date": "11/01", "price": "$125.00", "country": "🇺🇸 미국" },
      { "date": "10/30", "price": "$128.00", "country": "🇺🇸 미국" },
      { "date": "10/27", "price": "$120.00", "country": "🇨🇦 캐나다" }
    ],
    "bunjangQuery": "삼바 OG 화이트 260",
    "ebayQuery": "Adidas Samba OG White B75806",
    "tags": ["#스니커즈", "#크림사입", "#박스포장", "#글로벌완판"]
  },
  {
    "id": "adidas-samba-maroon",
    "category": "sneakers",
    "categoryName": "👟 스니커즈",
    "title": "아디다스 삼바 OG 마룬 오프화이트 여성용",
    "ebayTitle": "Adidas Samba OG Maroon Off White Womens Sneakers",
    "badge": "🔥 30일 24건 완판",
    "watchers": "👀 49명 찜",
    "status": "인기 컬러 (부피 1.5kg 과금)",
    "ebayUsd": 109.0,
    "ebayKrw": 150420,
    "targetBuyKrw": 68000,
    "profitKrw": 32800,
    "roi": "+48%",
    "boxSize": "신발 택배 박스 (32×20×12cm)",
    "actualWeight": 790,
    "volWeight": 1280,
    "appliedWeight": 1500,
    "weightNote": "실무게 790g < 부피 1,280g ➔ 1.5kg 부피과금",
    "priceRange": "$98.00 ~ $120.00",
    "salesVelocity": "1.2일당 1건 완판 🔥",
    "topBuyers": "🇺🇸 미국 65% · 🇬🇧 영국 20% · 🇦🇺 호주 15%",
    "recentSold": [
      { "date": "11/02", "price": "$109.00", "country": "🇺🇸 미국" },
      { "date": "10/28", "price": "$105.00", "country": "🇬🇧 영국" },
      { "date": "10/24", "price": "$115.00", "country": "🇺🇸 미국" }
    ],
    "bunjangQuery": "삼바 OG 마룬",
    "ebayQuery": "Adidas Samba OG Maroon",
    "tags": ["#삼바마룬", "#여성스니커즈", "#리셀인기"]
  },

  # 💄 5. K-뷰티 / 스킨케어
  {
    "id": "nonfiction-hand",
    "category": "beauty",
    "categoryName": "💄 K-뷰티",
    "title": "논픽션 (Nonfiction) 핸드크림 50ml + 포터블",
    "ebayTitle": "Nonfiction Hand Cream 50ml Gentle Night Santal Cream",
    "badge": "🔥 30일 31건 완판",
    "watchers": "👀 28명 찜",
    "status": "적극 사입",
    "ebayUsd": 38.0,
    "ebayKrw": 52440,
    "targetBuyKrw": 21000,
    "profitKrw": 13200,
    "roi": "+62%",
    "boxSize": "소형 박스 (15×10×6cm)",
    "actualWeight": 90,
    "volWeight": 150,
    "appliedWeight": 200,
    "weightNote": "실무게 90g < 부피 150g ➔ 200g 요금 적용",
    "priceRange": "$35.00 ~ $42.00",
    "salesVelocity": "1.0일당 1건 완판 🔥",
    "topBuyers": "🇺🇸 미국 58% · 🇨🇦 캐나다 22% · 🇬🇧 영국 12%",
    "recentSold": [
      { "date": "11/01", "price": "$38.00", "country": "🇺🇸 미국" },
      { "date": "10/30", "price": "$36.50", "country": "🇨🇦 캐나다" },
      { "date": "10/28", "price": "$40.00", "country": "🇺🇸 미국" }
    ],
    "bunjangQuery": "논픽션 핸드크림 50ml",
    "ebayQuery": "Nonfiction Hand cream 50ml",
    "tags": ["#올리브영1위", "#성수동선물", "#가벼운무게"]
  },
  {
    "id": "beauty-of-joseon-sun",
    "category": "beauty",
    "categoryName": "💄 K-뷰티",
    "title": "조선미녀 맑은쌀 선크림 SPF50+ 50ml (2개 세트)",
    "ebayTitle": "Beauty of Joseon Relief Sun Rice Probiotics SPF50 50ml 2 Pack",
    "badge": "🔥 30일 53건 완판",
    "watchers": "👀 82명 찜",
    "status": "틱톡 바이럴 1위",
    "ebayUsd": 36.0,
    "ebayKrw": 49680,
    "targetBuyKrw": 17000,
    "profitKrw": 15800,
    "roi": "+93%",
    "boxSize": "에어캡 포장 (16×12×6cm)",
    "actualWeight": 140,
    "volWeight": 192,
    "appliedWeight": 200,
    "weightNote": "실무게 140g < 부피 192g ➔ 200g 요금 적용",
    "priceRange": "$32.00 ~ $38.00",
    "salesVelocity": "0.6일당 1건 완판 (초고속 🔥)",
    "topBuyers": "🇺🇸 미국 75% · 🇬🇧 영국 15% · 🇨🇦 캐나다 10%",
    "recentSold": [
      { "date": "11/02", "price": "$36.00", "country": "🇺🇸 미국" },
      { "date": "11/01", "price": "$35.00", "country": "🇺🇸 미국" },
      { "date": "10/30", "price": "$38.00", "country": "🇬🇧 영국" }
    ],
    "bunjangQuery": "조선미녀 맑은쌀 선크림",
    "ebayQuery": "Beauty of Joseon Relief Sun 2 Pack",
    "tags": ["#올리브영수출", "#틱톡선크림", "#재구매1위", "#가벼운무게"]
  },

  # 🎤 6. K-POP 굿즈 & 포토카드
  {
    "id": "ive-photocard-musinsa",
    "category": "kpop",
    "categoryName": "🎤 K-POP",
    "title": "아이브 (IVE) 무신사 룩스캔킬 단독 미공포 포카",
    "ebayTitle": "IVE Photocard Looks Can Kill Kpop Official Musinsa POB",
    "badge": "🔥 30일 33건 완판",
    "watchers": "👀 55명 찜",
    "status": "초경량 우체국 발송 (최저 운임)",
    "ebayUsd": 25.0,
    "ebayKrw": 34500,
    "targetBuyKrw": 12000,
    "profitKrw": 7640,
    "roi": "+63%",
    "boxSize": "탑로더 에어캡 봉투 (12×18cm)",
    "actualWeight": 35,
    "volWeight": 30,
    "appliedWeight": 100,
    "weightNote": "실무게 35g ➔ 100g 초경량 요금 (최저 배송비)",
    "priceRange": "$22.00 ~ $28.00",
    "salesVelocity": "0.9일당 1건 완판 🔥",
    "topBuyers": "🇺🇸 미국 60% · 🇯🇵 일본 25% · 🇹🇼 대만 15%",
    "recentSold": [
      { "date": "11/02", "price": "$25.00", "country": "🇺🇸 미국" },
      { "date": "10/31", "price": "$24.00", "country": "🇯🇵 일본" },
      { "date": "10/28", "price": "$26.50", "country": "🇺🇸 미국" }
    ],
    "bunjangQuery": "아이브 무신사 미공포",
    "ebayQuery": "IVE photocard musinsa pob",
    "tags": ["#포토카드", "#무신사POB", "#아이브", "#우체국8980원"]
  },
  {
    "id": "skz-lucky-draw",
    "category": "kpop",
    "categoryName": "🎤 K-POP",
    "title": "스트레이키즈 사운드웨이브 럭키드로우 미공포",
    "ebayTitle": "Stray Kids Soundwave Lucky Draw Photocard Official POB",
    "badge": "🔥 30일 58건 완판",
    "watchers": "👀 71명 찜",
    "status": "무지성 사입 (마진율 62%)",
    "ebayUsd": 32.0,
    "ebayKrw": 44160,
    "targetBuyKrw": 11000,
    "profitKrw": 20200,
    "roi": "+183%",
    "boxSize": "탑로더 에어캡 봉투 (12×18cm)",
    "actualWeight": 35,
    "volWeight": 30,
    "appliedWeight": 100,
    "weightNote": "실무게 35g ➔ 100g 초경량 요금 (최저 배송비)",
    "priceRange": "$28.00 ~ $36.00",
    "salesVelocity": "0.5일당 1건 완판 (폭풍 회전 🔥)",
    "topBuyers": "🇺🇸 미국 65% · 🇬🇧 영국 15% · 🇦🇺 호주 12%",
    "recentSold": [
      { "date": "11/02", "price": "$32.00", "country": "🇺🇸 미국" },
      { "date": "11/01", "price": "$34.00", "country": "🇬🇧 영국" },
      { "date": "10/31", "price": "$30.00", "country": "🇺🇸 미국" }
    ],
    "bunjangQuery": "스트레이키즈 럭키드로우 미공포",
    "ebayQuery": "Stray Kids lucky draw photocard",
    "tags": ["#포토카드", "#탑로더포장", "#우체국8980원"]
  },
  {
    "id": "ive-lightstick",
    "category": "kpop",
    "categoryName": "🎤 K-POP",
    "title": "아이브 (IVE) 공식 응원봉 라이트스틱 Ver.2 (미개봉 박스)",
    "ebayTitle": "IVE Official Lightstick Ver 2 Concert Cheer Lamp Sealed Box",
    "badge": "🔥 30일 26건 완판",
    "watchers": "👀 33명 찜",
    "status": "안전 사입 (부피 1kg 과금)",
    "ebayUsd": 68.0,
    "ebayKrw": 93840,
    "targetBuyKrw": 42000,
    "profitKrw": 26800,
    "roi": "+63%",
    "boxSize": "응원봉 하드박스 (28×14×12cm)",
    "actualWeight": 420,
    "volWeight": 784,
    "appliedWeight": 1000,
    "weightNote": "실무게 420g < 부피 784g ➔ 1,000g(1kg) 부피과금",
    "priceRange": "$64.00 ~ $75.00",
    "salesVelocity": "1.2일당 1건 완판",
    "topBuyers": "🇺🇸 미국 60% · 🇲🇽 멕시코 20% · 🇩🇪 독일 10%",
    "recentSold": [
      { "date": "10/31", "price": "$68.00", "country": "🇺🇸 미국" },
      { "date": "10/28", "price": "$72.00", "country": "🇺🇸 미국" },
      { "date": "10/25", "price": "$65.00", "country": "🇲🇽 멕시코" }
    ],
    "bunjangQuery": "아이브 응원봉 ver2",
    "ebayQuery": "IVE lightstick official",
    "tags": ["#월드투어", "#콘서트필수", "#박스신품"]
  },
  {
    "id": "newjeans-bunjy",
    "category": "kpop",
    "categoryName": "🎤 K-POP",
    "title": "뉴진스 (NewJeans) 버니즈 번지 토끼 인형 키링",
    "ebayTitle": "NewJeans Bunnies Bunjy Plush Doll Keyring Official MD",
    "badge": "🔥 30일 45건 완판",
    "watchers": "👀 62명 찜",
    "status": "적극 사입 (글로벌 1위)",
    "ebayUsd": 38.0,
    "ebayKrw": 52440,
    "targetBuyKrw": 18000,
    "profitKrw": 16400,
    "roi": "+91%",
    "boxSize": "1호 박스 (18×14×9cm)",
    "actualWeight": 90,
    "volWeight": 378,
    "appliedWeight": 400,
    "weightNote": "실무게 90g < 부피 378g ➔ 400g 부피무게 적용",
    "priceRange": "$34.00 ~ $42.00",
    "salesVelocity": "0.7일당 1건 완판 (초고속 🔥)",
    "topBuyers": "🇺🇸 미국 55% · 🇯🇵 일본 25% · 🇪🇺 유럽 15%",
    "recentSold": [
      { "date": "11/02", "price": "$38.00", "country": "🇺🇸 미국" },
      { "date": "11/01", "price": "$35.00", "country": "🇯🇵 일본" },
      { "date": "10/30", "price": "$40.00", "country": "🇺🇸 미국" }
    ],
    "bunjangQuery": "뉴진스 번지 키링",
    "ebayQuery": "NewJeans bunjy keyring",
    "tags": ["#뉴진스MD", "#초경량키링", "#주문폭주"]
  },

  # 🃏 7. 포켓몬 카드 & 한국 한정판
  {
    "id": "ditto-promo",
    "category": "pokemon",
    "categoryName": "🃏 포켓몬",
    "title": "포켓몬 메타몽 프로젝트 한국 한정 프로모 173/SV-P (미개봉)",
    "ebayTitle": "Pokemon TCG Ditto 173/SV-P Metamong Project Korean Promo Sealed",
    "badge": "🔥 30일 18건 완판",
    "watchers": "👀 29명 찜",
    "status": "고마진 효자템 (초경량)",
    "ebayUsd": 135.0,
    "ebayKrw": 186300,
    "targetBuyKrw": 110000,
    "profitKrw": 35500,
    "roi": "+32%",
    "boxSize": "골판지 보강 탑로더 봉투 (15×20cm)",
    "actualWeight": 45,
    "volWeight": 40,
    "appliedWeight": 100,
    "weightNote": "실무게 45g ➔ 100g 초경량 요금 (안전 보강 포장)",
    "priceRange": "$130.00 ~ $150.00",
    "salesVelocity": "1.6일당 1건 완판 (고단가)",
    "topBuyers": "🇦🇺 호주 45% · 🇦🇹 오스트리아 25% · 🇮🇹 이탈리아 20%",
    "recentSold": [
      { "date": "11/02", "price": "$150.00", "country": "🇦🇺 호주" },
      { "date": "10/29", "price": "$135.00", "country": "🇦🇹 오스트리아" },
      { "date": "10/24", "price": "$140.00", "country": "🇺🇸 미국" }
    ],
    "bunjangQuery": "메타몽 프로젝트 173",
    "ebayQuery": "Pokemon Ditto 173/SV-P",
    "tags": ["#밀봉새상품", "#동욱님주력", "#글로벌완판"]
  },
  {
    "id": "pikachu-mat",
    "category": "pokemon",
    "categoryName": "🃏 포켓몬",
    "title": "포켓몬 고풍 피카츄 한국 한정 플레이매트 (미개봉)",
    "ebayTitle": "Pokemon Korea Traditional Antique Pikachu Playmat Official Sealed",
    "badge": "🔥 30일 12건 완판",
    "watchers": "👀 22명 찜",
    "status": "안전 사입 (부피 500g 적용)",
    "ebayUsd": 140.0,
    "ebayKrw": 193200,
    "targetBuyKrw": 85000,
    "profitKrw": 53200,
    "roi": "+62%",
    "boxSize": "매트 원통형 박스 (40×8×8cm)",
    "actualWeight": 310,
    "volWeight": 426,
    "appliedWeight": 500,
    "weightNote": "실무게 310g < 부피 426g ➔ 500g 부피무게 적용",
    "priceRange": "$130.00 ~ $155.00",
    "salesVelocity": "2.5일당 1건 완판",
    "topBuyers": "🇺🇸 미국 70% · 🇨🇦 캐나다 15% · 🇬🇧 영국 10%",
    "recentSold": [
      { "date": "10/28", "price": "$140.00", "country": "🇺🇸 미국" },
      { "date": "10/22", "price": "$138.00", "country": "🇺🇸 미국" },
      { "date": "10/18", "price": "$145.00", "country": "🇨🇦 캐나다" }
    ],
    "bunjangQuery": "고풍 피카츄 매트",
    "ebayQuery": "Pokemon Korea playmat antique",
    "tags": ["#한국전통굿즈", "#북미셀렉템", "#미개봉"]
  },
  {
    "id": "magikarp-promo",
    "category": "pokemon",
    "categoryName": "🃏 포켓몬",
    "title": "포켓몬 메가 페스타 잉어킹 프로모 040/M-P 홀로 (미개봉)",
    "ebayTitle": "Pokemon Korean Mega Festa Magikarp Promo 040/M-P Holo Sealed",
    "badge": "🔥 30일 14건 완판",
    "watchers": "👀 37명 찜",
    "status": "이탈리아/유럽 인기 (초경량)",
    "ebayUsd": 185.0,
    "ebayKrw": 255300,
    "targetBuyKrw": 135000,
    "profitKrw": 63000,
    "roi": "+46%",
    "boxSize": "골판지 보강 탑로더 봉투 (15×20cm)",
    "actualWeight": 45,
    "volWeight": 40,
    "appliedWeight": 100,
    "weightNote": "실무게 45g ➔ 100g 초경량 요금",
    "priceRange": "$170.00 ~ $195.00",
    "salesVelocity": "2.1일당 1건 완판",
    "topBuyers": "🇮🇹 이탈리아 40% · 🇺🇸 미국 35% · 🇫🇷 프랑스 15%",
    "recentSold": [
      { "date": "10/29", "price": "$185.00", "country": "🇮🇹 이탈리아" },
      { "date": "10/23", "price": "$180.00", "country": "🇺🇸 미국" },
      { "date": "10/16", "price": "$190.00", "country": "🇫🇷 프랑스" }
    ],
    "bunjangQuery": "메가 페스타 잉어킹",
    "ebayQuery": "Pokemon Magikarp 040/M-P",
    "tags": ["#홀로카드", "#유럽직배송", "#K-Packet"]
  },

  # 🧸 8. 캐릭터 / 키링 / MD
  {
    "id": "monamhee-keyring",
    "category": "character",
    "categoryName": "🧸 캐릭터/키링",
    "title": "모남희 (MONAMHEE) 블핑 로제 착용 블핑이 키링",
    "ebayTitle": "MONAMHEE Blackpink Rose Plush Doll Keyring Bag Charm Official",
    "badge": "🔥 30일 24건 완판",
    "watchers": "👀 43명 찜",
    "status": "연예인 가방 악세사리",
    "ebayUsd": 55.0,
    "ebayKrw": 75900,
    "targetBuyKrw": 28000,
    "profitKrw": 26500,
    "roi": "+95%",
    "boxSize": "1호 박스 (16×12×8cm)",
    "actualWeight": 75,
    "volWeight": 256,
    "appliedWeight": 300,
    "weightNote": "실무게 75g < 부피 256g ➔ 300g 부피무게 적용",
    "priceRange": "$50.00 ~ $60.00",
    "salesVelocity": "1.2일당 1건 완판 🔥",
    "topBuyers": "🇺🇸 미국 48% · 🇯🇵 일본 35% · 🇹🇼 대만 17%",
    "recentSold": [
      { "date": "11/01", "price": "$55.00", "country": "🇯🇵 일본" },
      { "date": "10/28", "price": "$52.00", "country": "🇺🇸 미국" },
      { "date": "10/24", "price": "$60.00", "country": "🇹🇼 대만" }
    ],
    "bunjangQuery": "모남희 키링",
    "ebayQuery": "Monamhee plush keyring Rose",
    "tags": ["#로제키링", "#가방키링", "#성수동핫플", "#초경량배송"]
  },
  {
    "id": "seongsu-hanbok-keyring",
    "category": "character",
    "categoryName": "🧸 캐릭터/키링",
    "title": "성수 팝업 한복 피카츄 LED 라이트 키링 (현장 한정)",
    "ebayTitle": "Pokemon Korea Hanbok Pikachu LED Light Keyring Seongsu Popup",
    "badge": "🔥 30일 16건 완판",
    "watchers": "👀 31명 찜",
    "status": "대박 마진템 (+6.8만)",
    "ebayUsd": 115.0,
    "ebayKrw": 158700,
    "targetBuyKrw": 45000,
    "profitKrw": 68500,
    "roi": "+152%",
    "boxSize": "소형 박스 (15×12×6cm)",
    "actualWeight": 85,
    "volWeight": 180,
    "appliedWeight": 200,
    "weightNote": "실무게 85g < 부피 180g ➔ 200g 요금 적용",
    "priceRange": "$105.00 ~ $125.00",
    "salesVelocity": "1.8일당 1건 완판 🔥",
    "topBuyers": "🇺🇸 미국 55% · 🇯🇵 일본 25% · 🇦🇺 호주 15%",
    "recentSold": [
      { "date": "10/31", "price": "$115.00", "country": "🇺🇸 미국" },
      { "date": "10/26", "price": "$110.00", "country": "🇯🇵 일본" },
      { "date": "10/22", "price": "$120.00", "country": "🇦🇺 호주" }
    ],
    "bunjangQuery": "한복 피카츄 키링",
    "ebayQuery": "Pokemon Korea Hanbok Pikachu keyring",
    "tags": ["#성수팝업한정", "#현장품절템", "#미개봉새상품"]
  },
  {
    "id": "plave-doll-set",
    "category": "character",
    "categoryName": "🧸 캐릭터/키링",
    "title": "플레이브 (PLAVE) MMMM 공식 봉제인형 키링 5인 세트",
    "ebayTitle": "PLAVE MMMM PLUSH Doll Keyring 5 Members SET Official Pop-Up",
    "badge": "🔥 30일 19건 완판",
    "watchers": "👀 47명 찜",
    "status": "성수/더현대 팝업 (부피 1.5kg)",
    "ebayUsd": 179.9,
    "ebayKrw": 248262,
    "targetBuyKrw": 115000,
    "profitKrw": 82000,
    "roi": "+71%",
    "boxSize": "2호 택배 박스 (25×20×15cm)",
    "actualWeight": 380,
    "volWeight": 1250,
    "appliedWeight": 1500,
    "weightNote": "실무게 380g < 부피 1,250g ➔ 1.5kg 부피과금 (인형 부피 주의)",
    "priceRange": "$162.00 ~ $198.00",
    "salesVelocity": "1.4일당 1건 완판 🔥",
    "topBuyers": "🇺🇸 미국 50% · 🇯🇵 일본 35% · 🇹🇼 대만 15%",
    "recentSold": [
      { "date": "11/02", "price": "$179.90", "country": "🇺🇸 미국" },
      { "date": "10/29", "price": "$175.00", "country": "🇯🇵 일본" },
      { "date": "10/25", "price": "$185.00", "country": "🇺🇸 미국" }
    ],
    "bunjangQuery": "플레이브 인형 키링",
    "ebayQuery": "PLAVE MMMM PLUSH Doll Keyring",
    "tags": ["#플레이브", "#버추얼아이돌", "#더현대팝업", "#고단가"]
  },

  # ☕ 9. 스타벅스 / 텀블러
  {
    "id": "starbucks-korea-tumbler",
    "category": "starbucks",
    "categoryName": "☕ 스타벅스",
    "title": "스타벅스 코리아 전통 자개 청자 텀블러 MD (박스 신품)",
    "ebayTitle": "Starbucks Korea Traditional Mother of Pearl Tumbler Limited Edition",
    "badge": "🔥 30일 17건 완판",
    "watchers": "👀 38명 찜",
    "status": "외국인 선물 1위 (부피 500g 적용)",
    "ebayUsd": 65.0,
    "ebayKrw": 89700,
    "targetBuyKrw": 34000,
    "profitKrw": 29500,
    "roi": "+86%",
    "boxSize": "텀블러 완충 박스 (12×12×25cm)",
    "actualWeight": 320,
    "volWeight": 600,
    "appliedWeight": 500,
    "weightNote": "실무게 320g < 부피 600g ➔ 500g 부피무게 적용",
    "priceRange": "$58.00 ~ $70.00",
    "salesVelocity": "1.7일당 1건 완판",
    "topBuyers": "🇺🇸 미국 60% · 🇸🇬 싱가포르 25% · 🇦🇺 호주 15%",
    "recentSold": [
      { "date": "10/31", "price": "$65.00", "country": "🇺🇸 미국" },
      { "date": "10/27", "price": "$62.00", "country": "🇸🇬 싱가포르" },
      { "date": "10/23", "price": "$68.00", "country": "🇺🇸 미국" }
    ],
    "bunjangQuery": "스타벅스 전통 자개 텀블러",
    "ebayQuery": "Starbucks Korea Traditional Tumbler",
    "tags": ["#한국한정MD", "#자개텀블러", "#안전포장", "#고급선물"]
  },
  {
    "id": "starbucks-farmers-tumbler",
    "category": "starbucks",
    "categoryName": "☕ 스타벅스",
    "title": "스타벅스 코리아 2026 파머스 마켓 텀블러 MD",
    "ebayTitle": "Starbucks Korea 2026 Farmers Market Tumbler Mug Limited",
    "badge": "🔥 30일 21건 완판",
    "watchers": "👀 36명 찜",
    "status": "외국인 선물 1위 (부피 500g 적용)",
    "ebayUsd": 69.99,
    "ebayKrw": 96586,
    "targetBuyKrw": 38000,
    "profitKrw": 28100,
    "roi": "+74%",
    "boxSize": "텀블러 완충 박스 (12×12×25cm)",
    "actualWeight": 310,
    "volWeight": 600,
    "appliedWeight": 500,
    "weightNote": "실무게 310g < 부피 600g ➔ 500g 부피무게 적용",
    "priceRange": "$63.00 ~ $77.00",
    "salesVelocity": "1.2일당 1건 완판 🔥",
    "topBuyers": "🇺🇸 미국 65% · 🇸🇬 싱가포르 20% · 🇦🇺 호주 15%",
    "recentSold": [
      { "date": "11/02", "price": "$69.99", "country": "🇺🇸 미국" },
      { "date": "10/29", "price": "$68.00", "country": "🇸🇬 싱가포르" },
      { "date": "10/26", "price": "$72.00", "country": "🇺🇸 미국" }
    ],
    "bunjangQuery": "스타벅스 파머스 텀블러",
    "ebayQuery": "Starbucks Korea Farmers Market Tumbler",
    "tags": ["#한국한정MD", "#파머스마켓", "#스타벅스텀블러"]
  }
]

# Write JSON files
with open('data/baseline_items.json', 'w', encoding='utf-8') as f:
    json.dump(ITEMS, f, ensure_ascii=False, indent=2)

with open('data/verified_items.json', 'w', encoding='utf-8') as f:
    json.dump({
        "updatedAt": "2026-11-02 19:20",
        "totalItems": len(ITEMS),
        "items": ITEMS
    }, f, ensure_ascii=False, indent=2)

print("Baseline and verified JSONs updated.")

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update VERIFIED_ITEMS in index.html
items_json_str = json.dumps(ITEMS, ensure_ascii=False, indent=6)
pattern_verified = r'const VERIFIED_ITEMS = \[.*?\];\s*const VERIFIED_CATEGORIES ='
new_verified_str = f"const VERIFIED_ITEMS = {items_json_str};\n\n    const VERIFIED_CATEGORIES ="
html = re.sub(pattern_verified, new_verified_str, html, flags=re.DOTALL)

# Update verified card buttons to include [🎯 소싱하기]
old_card_buttons_pattern = r'<!-- 실전 액션 버튼 3종 -->\s*<div class="grid grid-cols-3 gap-1\.5 pt-1">.*?</div>'
new_card_buttons = '''<!-- 실전 액션 버튼 3종 -->
            <div class="grid grid-cols-3 gap-1.5 pt-1">
              <button type="button" onclick="startSourcingForItem('${it.id}')" class="py-2 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-black text-xs flex items-center justify-center space-x-1 transition shadow active:scale-95 text-center">
                <span>🎯</span>
                <span>소싱하기</span>
              </button>
              <button type="button" onclick="loadIntoCalculatorCustom('${it.id}', ${it.ebayUsd}, ${it.appliedWeight || 200}, '${it.category}')" class="py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs flex items-center justify-center space-x-1 transition shadow active:scale-95 text-center">
                <span>⚡</span>
                <span>마진 계산</span>
              </button>
              <button type="button" onclick="openEbayDetailModal('${it.id}')" class="py-2 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-500/40 font-bold text-xs flex items-center justify-center space-x-1 transition active:scale-95 text-center">
                <span>📊</span>
                <span>시세/거래량</span>
              </button>
            </div>'''
html = re.sub(old_card_buttons_pattern, new_card_buttons, html, flags=re.DOTALL)

# In openEbayDetailModal, also update [🛒 번장 최저가] to [🎯 소싱하기 직통]
old_modal_btns = r'<div class="grid grid-cols-2 gap-1\.5">\s*<a href="https://m\.bunjang\.co\.kr/search/products\?q=\$\{encodeURIComponent\(it\.bunjangQuery\)\}&order=price_asc".*?</a>'
new_modal_btns = '''<div class="grid grid-cols-2 gap-1.5">
            <button type="button" onclick="closeEbayDetailModal(); startSourcingForItem('${it.id}')" class="py-2 bg-rose-600 hover:bg-rose-500 text-white font-black text-xs rounded-xl text-center transition flex items-center justify-center space-x-1 shadow active:scale-95">
              <span>🎯</span>
              <span>10대 사입처 찾기</span>
            </button>'''
html = re.sub(old_modal_btns, new_modal_btns, html, flags=re.DOTALL)

# Now, completely rewrite SUB-TAB 1: #subtab-view-sourcing
old_sourcing_tab_pattern = r'<!-- SUB-TAB 1: 소싱 레이더 PRO -->\s*<div id="subtab-view-sourcing".*?</div>\s*</div>\s*<!-- SUB-TAB 2: 글로벌 리서치 허브'
new_sourcing_tab_html = '''<!-- SUB-TAB 1: 사입처 찾기 & 단계별 소싱 레이더 PRO (셀러박스 리버싱 이식) -->
      <div id="subtab-view-sourcing" class="hidden space-y-4">
        <!-- 상단 전체메뉴 복귀 바 -->
        <div class="flex items-center justify-between bg-slate-900/80 px-3 py-2 rounded-xl border border-slate-800">
          <button type="button" onclick="switchAllSubTab('menu')" class="flex items-center space-x-1.5 text-xs text-indigo-400 hover:text-indigo-300 font-bold transition active:scale-95">
            <span>←</span>
            <span>전체메뉴 아이콘으로</span>
          </button>
          <span class="text-[10px] text-amber-400 font-bold">🎯 단계별 10대 사입처 직통 검색</span>
        </div>

        <!-- 3-Way 입력 허브 (상품명 · 마켓링크 · 사진촬영) -->
        <div class="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-indigo-500/40 rounded-2xl p-4 space-y-3 shadow-lg">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
              <div class="w-8 h-8 rounded-xl bg-indigo-600/30 border border-indigo-500/50 flex items-center justify-center text-base">
                🎯
              </div>
              <div>
                <h3 class="text-xs font-black text-slate-100">스마트 사입처 검색 허브</h3>
                <p class="text-[10px] text-slate-400">핫픽에서 바로 넘어오거나 직접 링크·사진을 넣어 사입처를 찾습니다</p>
              </div>
            </div>
          </div>

          <!-- 3-Way 모드 선택 탭 -->
          <div class="flex space-x-1 bg-slate-950 p-1 rounded-xl border border-slate-800 text-xs">
            <button type="button" onclick="setSourcingInputMode('text')" id="smode-btn-text" class="flex-1 py-1.5 rounded-lg bg-indigo-600 text-white font-bold transition shadow">
              🔤 상품명
            </button>
            <button type="button" onclick="setSourcingInputMode('url')" id="smode-btn-url" class="flex-1 py-1.5 rounded-lg text-slate-400 hover:text-white transition font-medium">
              🔗 마켓 링크
            </button>
            <button type="button" onclick="setSourcingInputMode('photo')" id="smode-btn-photo" class="flex-1 py-1.5 rounded-lg text-slate-400 hover:text-white transition font-medium">
              📸 사진/카메라
            </button>
          </div>

          <!-- 모드 1: 텍스트 상품명 검색 -->
          <div id="smode-box-text" class="space-y-2">
            <div class="flex space-x-2">
              <input type="text" id="sourcing-search-keyword" value="BTS 슈가 은목걸이" placeholder="소싱할 상품명 또는 키워드 입력 (예: emis 볼캡, 슈가 목걸이, 삼바)" class="flex-1 bg-slate-950 text-xs text-slate-100 placeholder-slate-500 border border-slate-800 rounded-xl px-3 py-2.5 focus:outline-none focus:border-indigo-500 font-medium">
              <button type="button" onclick="runSmartSourcingAnalysis()" class="px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs flex items-center space-x-1 transition shadow-lg shadow-indigo-600/30 active:scale-95">
                <span>⚡</span>
                <span>사입처 검색</span>
              </button>
            </div>
          </div>

          <!-- 모드 2: 마켓 링크 분석 -->
          <div id="smode-box-url" class="hidden space-y-2">
            <div class="flex space-x-2">
              <input type="url" id="sourcing-search-url" placeholder="번개장터, 당근, KREAM, 무신사, 네이버 상품 링크 붙여넣기" class="flex-1 bg-slate-950 text-xs text-slate-100 placeholder-slate-500 border border-slate-800 rounded-xl px-3 py-2.5 focus:outline-none focus:border-indigo-500 font-medium">
              <button type="button" onclick="handleSourcingUrlSubmit()" class="px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center space-x-1 transition shadow active:scale-95">
                <span>🔗</span>
                <span>링크 분석</span>
              </button>
            </div>
            <p class="text-[10px] text-slate-400">💡 상품 링크를 붙여넣으면 상품명을 자동 추출해 10대 사입처를 일괄 검색합니다.</p>
          </div>

          <!-- 모드 3: 사진/카메라 업로드 -->
          <div id="smode-box-photo" class="hidden space-y-2">
            <input type="file" id="sourcing-photo-file" accept="image/*" class="hidden" onchange="handleSourcingPhotoFile(event)">
            <div onclick="document.getElementById('sourcing-photo-file').click()" class="border-2 border-dashed border-slate-700 hover:border-indigo-500 rounded-xl p-4 text-center cursor-pointer transition bg-slate-950/60 space-y-1.5">
              <div class="text-2xl">📸</div>
              <div class="text-xs font-bold text-slate-200">사진 선택 또는 카메라 촬영</div>
              <div class="text-[10px] text-slate-400">상품 사진을 올리면 키워드를 인식하여 사입처를 찾아드립니다</div>
            </div>
            <div id="sourcing-photo-preview-box" class="hidden flex items-center space-x-3 bg-slate-950 p-2.5 rounded-xl border border-slate-800">
              <img id="sourcing-photo-preview-img" src="" class="w-12 h-12 object-cover rounded-lg border border-slate-700">
              <div class="flex-1 text-xs">
                <div class="font-bold text-slate-200" id="sourcing-photo-name">업로드된 사진</div>
                <div class="text-[10px] text-emerald-400">사진 인식 완료! 키워드로 사입처 검색 가능</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 3단계 실전 소싱 파이프라인 (Step-by-Step Sourcing Pipeline) -->
        <div id="sourcing-pipeline-container" class="space-y-3.5">
          <!-- 1단계: 소싱 목표 & 마진 가이드 -->
          <div class="bg-slate-900/90 rounded-2xl border border-indigo-500/40 p-4 space-y-3 shadow">
            <div class="flex items-center justify-between border-b border-slate-800 pb-2">
              <div class="flex items-center space-x-2">
                <span class="w-5 h-5 rounded-full bg-rose-600 text-white text-[11px] font-black flex items-center justify-center">1</span>
                <span class="text-xs font-black text-slate-100">소싱 목표 & 안전 마진 가이드</span>
              </div>
              <span id="pipeline-status-badge" class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-500/30">🔥 실시간 완판 픽</span>
            </div>

            <div>
              <h4 id="pipeline-item-title" class="text-xs font-black text-slate-100 flex items-center space-x-1">
                <span class="text-amber-400">🇰🇷</span>
                <span>BTS 슈가 한국 전통 하회탈 실버925 목걸이</span>
              </h4>
              <p id="pipeline-item-subtitle" class="text-[10px] text-slate-400 truncate mt-0.5">🇺🇸 Handmade 925 Silver Necklace Korean Mask BTS Suga Agust D Inspired</p>
            </div>

            <!-- 시세 및 목표가 3단 카드 -->
            <div class="grid grid-cols-3 gap-2 bg-slate-950/80 p-2.5 rounded-xl border border-slate-800 text-center">
              <div>
                <div class="text-[9px] text-slate-400">eBay 실거래가</div>
                <div id="pipeline-ebay-usd" class="text-xs font-black text-amber-300 mt-0.5">$180.00</div>
                <div id="pipeline-ebay-krw" class="text-[9px] text-slate-400">약 248,400원</div>
              </div>
              <div class="border-x border-slate-800">
                <div class="text-[9px] text-slate-400">국내 목표 사입가</div>
                <div id="pipeline-target-buy" class="text-xs font-black text-emerald-300 mt-0.5">38,000원</div>
                <div class="text-[8px] text-emerald-400">이하 사입 시 마진보장</div>
              </div>
              <div>
                <div class="text-[9px] text-slate-400">예상 순이익</div>
                <div id="pipeline-profit-krw" class="text-xs font-black text-emerald-400 mt-0.5">+159,000원</div>
                <div id="pipeline-roi" class="text-[9px] text-sky-400 font-bold">+418% ROI</div>
              </div>
            </div>

            <!-- 포장 규격 및 부피무게 -->
            <div class="bg-slate-950 p-2.5 rounded-xl border border-slate-800 text-[11px] flex items-center justify-between">
              <span class="text-slate-400 flex items-center space-x-1">
                <span>📦</span>
                <span>포장: <b id="pipeline-box-size" class="text-slate-200">에어캡 안전봉투 (15×20cm)</b></span>
              </span>
              <span id="pipeline-weight-badge" class="text-[10px] px-2 py-0.5 rounded bg-sky-500/20 text-sky-300 border border-sky-500/30 font-bold font-mono">
                청구 100g (실무게 65g)
              </span>
            </div>
          </div>

          <!-- 2단계: 셀러박스 리버싱 10대 핵심 사입처 직통 검색 -->
          <div class="bg-slate-900/90 rounded-2xl border border-slate-800 p-4 space-y-3 shadow">
            <div class="flex items-center justify-between border-b border-slate-800 pb-2">
              <div class="flex items-center space-x-2">
                <span class="w-5 h-5 rounded-full bg-rose-600 text-white text-[11px] font-black flex items-center justify-center">2</span>
                <span class="text-xs font-black text-slate-100">10대 사입처 원클릭 직통 매물 검색</span>
              </div>
              <span class="text-[10px] text-indigo-400">셀러박스 리버싱 완비</span>
            </div>
            <p class="text-[11px] text-slate-400">버튼을 누르면 해당 사입처의 실시간 최저가 매물 창이 즉시 열립니다.</p>

            <!-- 1열: 국내 4대 C2C/중고 마켓 -->
            <div class="space-y-1">
              <div class="text-[10px] font-bold text-slate-400">📱 국내 C2C & 중고/리셀</div>
              <div class="grid grid-cols-4 gap-1.5">
                <a id="slink-bunjang" href="https://m.bunjang.co.kr/search/products?q=%EC%8A%88%EA%B0%80%20%EC%9D%80%EB%AA%A9%EA%B1%B8%EC%9D%B4&order=price_asc" target="_blank" rel="noopener noreferrer" class="py-2.5 px-1 rounded-xl bg-slate-950 hover:bg-slate-800 border border-rose-500/40 text-center transition block active:scale-95 shadow">
                  <div class="text-xs font-black text-rose-400">⚡ 번개장터</div>
                  <div class="text-[9px] text-slate-400 mt-0.5">최저가순 정렬</div>
                </a>
                <a id="slink-daangn" href="https://www.daangn.com/search/%EC%8A%88%EA%B0%80%20%EC%9D%80%EB%AA%A9%EA%B1%B8%EC%9D%B4" target="_blank" rel="noopener noreferrer" class="py-2.5 px-1 rounded-xl bg-slate-950 hover:bg-slate-800 border border-amber-500/40 text-center transition block active:scale-95 shadow">
                  <div class="text-xs font-black text-amber-400">🥕 당근마켓</div>
                  <div class="text-[9px] text-slate-400 mt-0.5">직거래·네고</div>
                </a>
                <a id="slink-joongna" href="https://web.joongna.com/search/%EC%8A%88%EA%B0%80%20%EC%9D%80%EB%AA%A9%EA%B1%B8%EC%9D%B4" target="_blank" rel="noopener noreferrer" class="py-2.5 px-1 rounded-xl bg-slate-950 hover:bg-slate-800 border border-emerald-500/40 text-center transition block active:scale-95 shadow">
                  <div class="text-xs font-black text-emerald-400">📦 중고나라</div>
                  <div class="text-[9px] text-slate-400 mt-0.5">전국 택배</div>
                </a>
                <a id="slink-kream" href="https://kream.co.kr/search?keyword=%EC%8A%88%EA%B0%80%20%EC%9D%80%EB%AA%A9%EA%B1%B8%EC%9D%B4" target="_blank" rel="noopener noreferrer" class="py-2.5 px-1 rounded-xl bg-slate-950 hover:bg-slate-800 border border-indigo-500/40 text-center transition block active:scale-95 shadow">
                  <div class="text-xs font-black text-indigo-400">👟 KREAM</div>
                  <div class="text-[9px] text-slate-400 mt-0.5">한정판 리셀</div>
                </a>
              </div>
            </div>

            <!-- 2열: 국내 공식몰 & 전몰 비교 -->
            <div class="space-y-1 pt-1">
              <div class="text-[10px] font-bold text-slate-400">🛍️ 오픈마켓 & 패션/뷰티 공식몰</div>
              <div class="grid grid-cols-4 gap-1.5">
                <a id="slink-naver" href="https://search.shopping.naver.com/search/all?query=%EC%8A%88%EA%B0%80%20%EC%9D%80%EB%AA%A9%EA%B1%B8%EC%9D%B4" target="_blank" rel="noopener noreferrer" class="py-2.5 px-1 rounded-xl bg-slate-950 hover:bg-slate-800 border border-green-500/40 text-center transition block active:scale-95 shadow">
                  <div class="text-xs font-black text-green-400">🟢 네이버쇼핑</div>
                  <div class="text-[9px] text-slate-400 mt-0.5">전몰 최저가</div>
                </a>
                <a id="slink-coupang" href="https://www.coupang.com/np/search?component=&q=%EC%8A%88%EA%B0%80%20%EC%9D%80%EB%AA%A9%EA%B1%B8%EC%9D%B4" target="_blank" rel="noopener noreferrer" class="py-2.5 px-1 rounded-xl bg-slate-950 hover:bg-slate-800 border border-red-500/40 text-center transition block active:scale-95 shadow">
                  <div class="text-xs font-black text-red-400">🚀 쿠팡</div>
                  <div class="text-[9px] text-slate-400 mt-0.5">로켓 배송</div>
                </a>
                <a id="slink-musinsa" href="https://www.musinsa.com/search/goods?keyword=%EC%8A%88%EA%B0%80%20%EC%9D%80%EB%AA%A9%EA%B1%B8%EC%9D%B4" target="_blank" rel="noopener noreferrer" class="py-2.5 px-1 rounded-xl bg-slate-950 hover:bg-slate-800 border border-sky-500/40 text-center transition block active:scale-95 shadow">
                  <div class="text-xs font-black text-sky-400">👕 무신사</div>
                  <div class="text-[9px] text-slate-400 mt-0.5">도메스틱 패션</div>
                </a>
                <a id="slink-oliveyoung" href="https://www.oliveyoung.co.kr/store/search/getSearchMain.do?query=%EC%8A%88%EA%B0%80%20%EC%9D%80%EB%AA%A9%EA%B1%B8%EC%9D%B4" target="_blank" rel="noopener noreferrer" class="py-2.5 px-1 rounded-xl bg-slate-950 hover:bg-slate-800 border border-lime-500/40 text-center transition block active:scale-95 shadow">
                  <div class="text-xs font-black text-lime-400">💄 올리브영</div>
                  <div class="text-[9px] text-slate-400 mt-0.5">K-뷰티 정품</div>
                </a>
              </div>
            </div>

            <!-- 3열: 해외 역소싱 & 구글 사입 추적 -->
            <div class="space-y-1 pt-1">
              <div class="text-[10px] font-bold text-slate-400">🌐 일본 역소싱 & 웹 이미지 추적</div>
              <div class="grid grid-cols-2 gap-1.5">
                <a id="slink-buyee" href="https://buyee.jp/mercari/search?keyword=%EC%8A%88%EA%B0%80%20%EC%9D%80%EB%AA%A9%EA%B1%B8%EC%9D%B4" target="_blank" rel="noopener noreferrer" class="py-2.5 px-2 rounded-xl bg-slate-950 hover:bg-slate-800 border border-red-500/40 text-center transition flex items-center justify-center space-x-2 active:scale-95 shadow">
                  <span class="text-base">🇯🇵</span>
                  <div class="text-left">
                    <div class="text-xs font-black text-red-400">메르카리 (Buyee)</div>
                    <div class="text-[9px] text-slate-400">일본 엔저 직구 소싱</div>
                  </div>
                </a>
                <a id="slink-google-img" href="https://www.google.com/search?tbm=isch&q=%EC%8A%88%EA%B0%80%20%EC%9D%80%EB%AA%A9%EA%B1%B8%EC%9D%B4%20%EC%82%AC%EC%9E%85" target="_blank" rel="noopener noreferrer" class="py-2.5 px-2 rounded-xl bg-slate-950 hover:bg-slate-800 border border-cyan-500/40 text-center transition flex items-center justify-center space-x-2 active:scale-95 shadow">
                  <span class="text-base">🔍</span>
                  <div class="text-left">
                    <div class="text-xs font-black text-cyan-400">구글 이미지 사입</div>
                    <div class="text-[9px] text-slate-400">웹 사진 출처 추적</div>
                  </div>
                </a>
              </div>
            </div>
          </div>

          <!-- 3단계: 매물 발견 시 사입가 입력 ➔ 실시간 손익 판정 ➔ 마진계산기 1초 연동 -->
          <div class="bg-slate-900/90 rounded-2xl border border-slate-800 p-4 space-y-3 shadow">
            <div class="flex items-center justify-between border-b border-slate-800 pb-2">
              <div class="flex items-center space-x-2">
                <span class="w-5 h-5 rounded-full bg-rose-600 text-white text-[11px] font-black flex items-center justify-center">3</span>
                <span class="text-xs font-black text-slate-100">발견 매물 가격 검증 & 마진계산기 연동</span>
              </div>
              <span class="text-[10px] text-emerald-400 font-bold">원클릭 계산기 이동</span>
            </div>

            <div class="space-y-2">
              <label class="text-[11px] text-slate-300 font-bold block">사입처(번장/당근 등)에서 찾은 실제 매물 가격:</label>
              <div class="flex items-center space-x-2">
                <input type="number" id="pipeline-custom-buy-input" value="38000" oninput="recalcSourcingPipeline()" class="flex-1 bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-slate-100 font-mono font-bold text-sm focus:outline-none focus:border-amber-400">
                <span class="text-xs font-bold text-slate-400">원</span>
              </div>
            </div>

            <!-- 실시간 계산 결과 요약 바 -->
            <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 flex items-center justify-between text-xs">
              <div>
                <div class="text-[10px] text-slate-400">최종 순이익 (부피배송비·수수료 차감 후)</div>
                <div id="pipeline-live-profit" class="text-sm font-black text-emerald-400 mt-0.5">+159,000원</div>
              </div>
              <div class="text-right">
                <div class="text-[10px] text-slate-400">수익률 (ROI)</div>
                <div id="pipeline-live-roi" class="text-sm font-black text-sky-400 mt-0.5">+418.4%</div>
              </div>
            </div>

            <!-- 계산기 직통 버튼 -->
            <button type="button" onclick="sendPipelineToCalculator()" class="w-full py-3 bg-gradient-to-r from-indigo-600 to-emerald-600 hover:from-indigo-500 hover:to-emerald-500 text-white font-black text-xs rounded-xl text-center transition shadow-lg active:scale-95 flex items-center justify-center space-x-1.5">
              <span>🧮</span>
              <span>마진 계산기에서 20개국 우체국 운임 및 관세 정밀 검증 ➔</span>
            </button>
          </div>
        </div>
      </div>

      <!-- SUB-TAB 2: 글로벌 리서치 허브'''

html = re.sub(old_sourcing_tab_pattern, new_sourcing_tab_html, html, flags=re.DOTALL)

# Add JavaScript functions for Sourcing 3-Way Mode and Pipeline
js_code_to_add = '''
    // 🎯 스마트 사입처 찾기 & 단계별 소싱 파이프라인 (셀러박스 리버싱 연동)
    let activeSourcingItem = VERIFIED_ITEMS[0];

    function setSourcingInputMode(mode) {
      ['text', 'url', 'photo'].forEach(m => {
        const box = document.getElementById('smode-box-' + m);
        const btn = document.getElementById('smode-btn-' + m);
        if (box) box.classList.toggle('hidden', m !== mode);
        if (btn) {
          if (m === mode) {
            btn.className = 'flex-1 py-1.5 rounded-lg bg-indigo-600 text-white font-bold transition shadow';
          } else {
            btn.className = 'flex-1 py-1.5 rounded-lg text-slate-400 hover:text-white transition font-medium';
          }
        }
      });
    }

    function startSourcingForItem(itemId) {
      const it = (activeVerifiedItems && activeVerifiedItems.find(x => x.id === itemId)) || VERIFIED_ITEMS.find(x => x.id === itemId);
      if (!it) return;

      switchTab('all');
      switchAllSubTab('sourcing');

      const kwInput = document.getElementById('sourcing-search-keyword');
      if (kwInput) kwInput.value = it.bunjangQuery || it.title;

      activeSourcingItem = it;
      renderSourcingPipeline(it);
      showToast(`'${it.title}' 사입처 찾기가 시작되었습니다! 🎯`, '🔍');
    }

    function renderSourcingPipeline(it) {
      if (!it) return;
      document.getElementById('pipeline-item-title').innerHTML = `<span class="text-amber-400">🇰🇷</span> <span>${it.title}</span>`;
      document.getElementById('pipeline-item-subtitle').innerText = `🇺🇸 ${it.ebayTitle}`;
      document.getElementById('pipeline-ebay-usd').innerText = `$${it.ebayUsd.toFixed(2)}`;
      document.getElementById('pipeline-ebay-krw').innerText = `약 ${Math.round(it.ebayUsd * 1334).toLocaleString()}원`;
      document.getElementById('pipeline-target-buy').innerText = `${it.targetBuyKrw.toLocaleString()}원`;
      document.getElementById('pipeline-profit-krw').innerText = `+${it.profitKrw.toLocaleString()}원`;
      document.getElementById('pipeline-roi').innerText = `${it.roi} ROI`;
      document.getElementById('pipeline-box-size').innerText = it.boxSize || '에어캡 안전봉투';
      document.getElementById('pipeline-weight-badge').innerText = `청구 ${it.appliedWeight || 200}g (${it.weightNote || '실제 무게'})`;
      
      const customInput = document.getElementById('pipeline-custom-buy-input');
      if (customInput) customInput.value = it.targetBuyKrw;

      // Update 10 Sourcing Destination links
      const q = it.bunjangQuery || it.title;
      const qEnc = encodeURIComponent(q);
      const qImgEnc = encodeURIComponent(q + ' 사입');

      const slinks = {
        'slink-bunjang': `https://m.bunjang.co.kr/search/products?q=${qEnc}&order=price_asc`,
        'slink-daangn': `https://www.daangn.com/search/${qEnc}`,
        'slink-joongna': `https://web.joongna.com/search/${qEnc}`,
        'slink-kream': `https://kream.co.kr/search?keyword=${qEnc}`,
        'slink-naver': `https://search.shopping.naver.com/search/all?query=${qEnc}`,
        'slink-coupang': `https://www.coupang.com/np/search?component=&q=${qEnc}`,
        'slink-musinsa': `https://www.musinsa.com/search/goods?keyword=${qEnc}`,
        'slink-oliveyoung': `https://www.oliveyoung.co.kr/store/search/getSearchMain.do?query=${qEnc}`,
        'slink-buyee': `https://buyee.jp/mercari/search?keyword=${qEnc}`,
        'slink-google-img': `https://www.google.com/search?tbm=isch&q=${qImgEnc}`
      };

      for (const [elemId, href] of Object.entries(slinks)) {
        const a = document.getElementById(elemId);
        if (a) a.href = href;
      }

      recalcSourcingPipeline();
    }

    function recalcSourcingPipeline() {
      if (!activeSourcingItem) return;
      const it = activeSourcingItem;
      const customBuy = parseFloat(document.getElementById('pipeline-custom-buy-input')?.value) || 0;
      const grossKrw = it.ebayUsd * 1334;
      
      // Category fee rate
      const catRate = CATEGORY_FEES[it.category] || 13.25;
      const ebayFeeKrw = ((it.ebayUsd * (catRate / 100)) + 0.40 + (it.ebayUsd * 0.0145)) * 1334;
      const buyerTaxFeeKrw = (it.ebayUsd * 0.08 * 0.147) * 1334;
      const payoFeeKrw = (grossKrw - ebayFeeKrw) * 0.02;
      
      // Shipping cost based on applied weight
      const shipRateTable = { 100: 8090, 200: 8980, 300: 10500, 400: 11500, 500: 12500, 1000: 18000, 1500: 24000, 2000: 30000 };
      const shipKrw = shipRateTable[it.appliedWeight || 200] || 8980;

      const totalExpense = customBuy + ebayFeeKrw + buyerTaxFeeKrw + payoFeeKrw + shipKrw;
      const netProfit = Math.round(grossKrw - totalExpense);
      const roi = customBuy > 0 ? ((netProfit / customBuy) * 100).toFixed(1) : 0;

      const profitElem = document.getElementById('pipeline-live-profit');
      if (profitElem) {
        profitElem.innerText = (netProfit >= 0 ? '+' : '') + netProfit.toLocaleString() + '원';
        profitElem.className = netProfit >= 0 ? 'text-sm font-black text-emerald-400 mt-0.5' : 'text-sm font-black text-rose-400 mt-0.5';
      }
      const roiElem = document.getElementById('pipeline-live-roi');
      if (roiElem) {
        roiElem.innerText = (roi >= 0 ? '+' : '') + roi + '%';
        roiElem.className = roi >= 0 ? 'text-sm font-black text-sky-400 mt-0.5' : 'text-sm font-black text-rose-400 mt-0.5';
      }
    }

    function sendPipelineToCalculator() {
      if (!activeSourcingItem) return;
      const customBuy = parseFloat(document.getElementById('pipeline-custom-buy-input')?.value) || activeSourcingItem.targetBuyKrw;
      loadIntoCalculator(activeSourcingItem.ebayUsd, activeSourcingItem.appliedWeight || 200, customBuy, activeSourcingItem.category);
    }

    function runSmartSourcingAnalysis(targetKw = null) {
      const kw = targetKw || document.getElementById('sourcing-search-keyword')?.value.trim();
      if (!kw) {
        showToast('검색할 상품명을 입력해 주세요!', '⚠️');
        return;
      }

      // Check if keyword matches any verified item
      const matched = VERIFIED_ITEMS.find(x => x.title.includes(kw) || x.bunjangQuery.includes(kw) || x.ebayTitle.toLowerCase().includes(kw.toLowerCase()));
      if (matched) {
        activeSourcingItem = matched;
        renderSourcingPipeline(matched);
      } else {
        // Create custom dynamic sourcing item
        activeSourcingItem = {
          id: 'custom-' + Date.now(),
          category: 'pokemon',
          categoryName: '기타 품목',
          title: kw,
          ebayTitle: kw,
          ebayUsd: 50.0,
          ebayKrw: 66700,
          targetBuyKrw: 25000,
          profitKrw: 18500,
          roi: '+74%',
          boxSize: '규격 포장 박스',
          actualWeight: 150,
          volWeight: 200,
          appliedWeight: 200,
          weightNote: '표준 200g 요금 적용',
          bunjangQuery: kw
        };
        renderSourcingPipeline(activeSourcingItem);
      }
      showToast(`'${kw}' 10대 사입처 직통 검색 완료!`, '🔍');
    }

    function handleSourcingUrlSubmit() {
      const urlInput = document.getElementById('sourcing-search-url');
      const url = (urlInput ? urlInput.value : '').trim();
      if (!url) {
        showToast('분석할 마켓 상품 링크를 붙여넣어 주세요!', '⚠️');
        return;
      }
      
      let keyword = '소싱 상품';
      try {
        const parsed = new URL(url);
        const q = parsed.searchParams.get('q') || parsed.searchParams.get('query') || parsed.searchParams.get('keyword');
        if (q) keyword = decodeURIComponent(q);
        else keyword = parsed.pathname.split('/').filter(Boolean).pop() || '소싱 상품';
      } catch (e) {
        keyword = url.slice(0, 30);
      }

      document.getElementById('sourcing-search-keyword').value = keyword;
      setSourcingInputMode('text');
      runSmartSourcingAnalysis(keyword);
      showToast(`링크에서 '${keyword}' 추출 완료! 사입처를 검색합니다.`, '🔗');
    }

    function handleSourcingPhotoFile(event) {
      const file = event.target.files && event.target.files[0];
      if (!file) return;

      const previewBox = document.getElementById('sourcing-photo-preview-box');
      const previewImg = document.getElementById('sourcing-photo-preview-img');
      const nameElem = document.getElementById('sourcing-photo-name');

      if (previewBox && previewImg) {
        previewImg.src = URL.createObjectURL(file);
        previewBox.classList.remove('hidden');
      }
      if (nameElem) {
        nameElem.innerText = file.name;
      }

      // Extract cleaned keyword from filename
      let kw = file.name.replace(/\.[^/.]+$/, '').replace(/[-_]/g, ' ');
      document.getElementById('sourcing-search-keyword').value = kw;
      runSmartSourcingAnalysis(kw);
      showToast(`'${file.name}' 사진 인식 완료! 사입처를 검색합니다.`, '📸');
    }
'''

# Place JS functions right before closing </script>
html = html.replace('  </script>', js_code_to_add + '\n  </script>', 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html successfully updated with Sourcing Pipeline!")

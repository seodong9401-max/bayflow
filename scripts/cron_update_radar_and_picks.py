#!/usr/bin/env python3
"""
BayFlow 30m Auto Radar & Verified Picks Updater (GitHub Actions Server)
- Runs automatically every 30 minutes on GitHub Actions.
- Crawls Google News RSS for Popups, Celeb/Idol Merch, Keyrings, Fashion, TCG.
- Updates data/draw_radar_items.json with fresh live radar news.
- Evaluates and tags '💎 대박마진' (ROI 150%+ / Profit 30,000 KRW+) in data/verified_items.json.
- Generates data/super_margin_alerts.json for instant high-margin alerts.
- Standard library only (no external pip dependencies needed).
"""

import os
import re
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
NOW_KST = datetime.now(KST)
NOW_STR = NOW_KST.strftime("%Y-%m-%d %H:%M")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BAYFLOW_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(BAYFLOW_DIR, "data")

USD_KRW = 1380.0
EBAY_FEE_RATE = 0.1325
PAYONEER_FEE_RATE = 0.0425
TOTAL_FEE_RATE = EBAY_FEE_RATE + PAYONEER_FEE_RATE

SEARCH_QUERIES = [
    {
        "query": "성수 팝업스토어 OR 팝업스토어 한정판",
        "kind": "popup",
        "sourceLabel": "성수 팝업 레이더",
        "defaultPlace": "서울 성수동 팝업스퀘어",
        "tags": ["팝업스토어", "성수동", "한정판MD", "오픈런"]
    },
    {
        "query": "아이돌 굿즈 한정판 OR K-POP 팝업스토어 MD",
        "kind": "celeb",
        "sourceLabel": "아이돌 굿즈 레이더",
        "defaultPlace": "온라인 / 공식 팝업스토어",
        "tags": ["연예인", "아이돌", "K-POP", "포토카드", "한정판굿즈"]
    },
    {
        "query": "콜라보 키링 한정판 OR 캐릭터 키링 품절",
        "kind": "acc",
        "sourceLabel": "악세사리·키링 레이더",
        "defaultPlace": "공식 스토어 / C2C",
        "tags": ["악세사리", "키링", "콜라보", "가방키링", "바이럴"]
    },
    {
        "query": "스트릿웨어 드로우 한정판 OR 성수 패션 팝업",
        "kind": "fashion",
        "sourceLabel": "스트릿·패션 레이더",
        "defaultPlace": "성수 / 무신사 / 크림",
        "tags": ["패션", "스트릿웨어", "드로우", "한정발매", "성수"]
    },
    {
        "query": "포켓몬 카드 프로모 한정판 OR 포켓몬 팝업",
        "kind": "viral",
        "sourceLabel": "포켓몬·TCG 레이더",
        "defaultPlace": "포켓몬 스토어 / 전국",
        "tags": ["포켓몬", "TCG", "프로모카드", "한정판", "수집품"]
    },
    {
        "query": "스니커즈 드로우 한정판 OR 나이키 드로우",
        "kind": "draw",
        "sourceLabel": "스니커즈 드로우 레이더",
        "defaultPlace": "나이키 / 크림 / 무신사",
        "tags": ["스니커즈", "드로우", "응모", "래플", "한정판"]
    }
]

def clean_html(text):
    if not text:
        return ""
    clean = re.sub(r'<[^>]+>', ' ', text)
    return ' '.join(clean.split()).strip()

def crawl_rss_news():
    new_items = []
    seen_titles = set()

    for conf in SEARCH_QUERIES:
        q = conf["query"]
        kind = conf["kind"]
        url = f"https://news.google.com/rss/search?q={urllib.parse.quote(q)}&hl=ko&gl=KR&ceid=KR:ko"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=12) as resp:
                xml_data = resp.read()
            root = ET.fromstring(xml_data)
            items = root.findall('.//item')

            for item in items[:6]:
                title = clean_html(item.findtext('title', ''))
                link = item.findtext('link', '')
                pub_date = item.findtext('pubDate', '')
                source = item.find('source')
                source_name = source.text if source is not None else conf["sourceLabel"]

                norm_title = re.sub(r'\s+', '', title).lower()
                if norm_title in seen_titles or not title:
                    continue
                seen_titles.add(norm_title)

                clean_title = re.sub(r'\s*-\s*[^-]+$', '', title).strip()

                brand_match = re.search(r'([A-Za-z0-9가-힣]+(?:\s*[xX×]\s*[A-Za-z0-9가-힣]+)?)', clean_title)
                brand = brand_match.group(1) if brand_match else "HOT IP"

                item_id = f"live-{kind}-{abs(hash(clean_title)) % 10000000:07d}"

                item_obj = {
                    "id": item_id,
                    "region": "kr",
                    "regionBadge": "🇰🇷 한국",
                    "source": "gnews",
                    "sourceLabel": f"실시간 {source_name}",
                    "kind": kind,
                    "title": clean_title,
                    "summary": f"{source_name} 보도: {clean_title} 발매 및 글로벌 관심 집중. 국내외 매니아층 리셀 수요 유입.",
                    "url": link,
                    "startAt": NOW_KST.isoformat(),
                    "endAt": (NOW_KST + timedelta(days=14)).isoformat(),
                    "brand": brand,
                    "place": conf["defaultPlace"],
                    "tags": conf["tags"] + [source_name, "실시간속보"]
                }
                new_items.append(item_obj)
        except Exception as e:
            print(f"Error crawling query '{q}': {e}")

    print(f"Crawled {len(new_items)} fresh news items from Google News RSS.")
    return new_items

def update_draw_radar():
    radar_file = os.path.join(DATA_DIR, "draw_radar_items.json")
    existing_items = []
    if os.path.exists(radar_file):
        try:
            with open(radar_file, "r", encoding="utf-8") as f:
                existing_items = json.load(f)
        except Exception as e:
            print(f"Error loading {radar_file}: {e}")

    fresh_items = crawl_rss_news()

    combined = []
    seen = set()

    for item in fresh_items:
        key = item["title"].strip().lower()
        if key not in seen:
            seen.add(key)
            combined.append(item)

    for item in existing_items:
        key = item.get("title", "").strip().lower()
        if key not in seen:
            seen.add(key)
            combined.append(item)

    combined = combined[:2000]

    with open(radar_file, "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)

    print(f"Updated {radar_file}: total {len(combined)} items.")
    return len(fresh_items), len(combined)

def update_verified_picks():
    picks_file = os.path.join(DATA_DIR, "verified_items.json")
    if not os.path.exists(picks_file):
        print(f"File not found: {picks_file}")
        return []

    with open(picks_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = data.get("items", [])
    super_margin_items = []

    for it in items:
        ebay_usd = float(it.get("ebayUsd", 0))
        target_buy_krw = int(it.get("targetBuyKrw", 0))
        applied_weight = int(it.get("appliedWeight", 100))

        if applied_weight <= 100:
            shipping_krw = 8130
        elif applied_weight <= 250:
            shipping_krw = 10200
        elif applied_weight <= 450:
            shipping_krw = 12500
        else:
            shipping_krw = 15000

        ebay_krw = round(ebay_usd * USD_KRW)
        it["ebayKrw"] = ebay_krw

        payout_krw = ebay_krw * (1.0 - TOTAL_FEE_RATE)
        net_profit_krw = round(payout_krw - shipping_krw - target_buy_krw)
        it["profitKrw"] = max(0, net_profit_krw)

        if target_buy_krw > 0:
            roi_pct = round((net_profit_krw / target_buy_krw) * 100)
            it["roi"] = f"+{roi_pct}%"
        else:
            roi_pct = 0
            it["roi"] = "+0%"

        is_super = (roi_pct >= 150 or net_profit_krw >= 30000)
        it["isSuperMargin"] = is_super
        if is_super:
            it["superBadge"] = f"💎 대박마진 ({it['roi']})"
            super_margin_items.append(it)
        else:
            it.pop("superBadge", None)

    super_margin_items.sort(key=lambda x: int(x.get("profitKrw", 0)), reverse=True)

    data["updatedAt"] = NOW_STR
    data["totalItems"] = len(items)
    data["superMarginCount"] = len(super_margin_items)
    data["items"] = items

    with open(picks_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated {picks_file}: total {len(items)} items, super margin items: {len(super_margin_items)}.")

    alerts_file = os.path.join(DATA_DIR, "super_margin_alerts.json")
    alerts_data = {
        "updatedAt": NOW_STR,
        "superMarginCount": len(super_margin_items),
        "items": [
            {
                "id": it["id"],
                "category": it.get("categoryName", ""),
                "title": it["title"],
                "ebayTitle": it["ebayTitle"],
                "ebayUsd": it["ebayUsd"],
                "ebayKrw": it["ebayKrw"],
                "targetBuyKrw": it["targetBuyKrw"],
                "profitKrw": it["profitKrw"],
                "roi": it["roi"],
                "badge": it.get("badge", ""),
                "bunjangQuery": it.get("bunjangQuery", it["title"])
            }
            for it in super_margin_items
        ]
    }
    with open(alerts_file, "w", encoding="utf-8") as f:
        json.dump(alerts_data, f, ensure_ascii=False, indent=2)

    print(f"Saved {alerts_file} with {len(super_margin_items)} super margin picks.")
    return super_margin_items

def main():
    print(f"=== BayFlow 30m Auto Updater Starting: {NOW_STR} KST ===")
    fresh_cnt, total_radar = update_draw_radar()
    super_items = update_verified_picks()
    print(f"=== BayFlow 30m Auto Updater Finished Successfully ===")
    print(f"Radar items: {fresh_cnt} fresh news added, total {total_radar}")
    print(f"Super margin items identified: {len(super_items)}")

if __name__ == "__main__":
    main()

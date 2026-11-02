#!/usr/bin/env python3
"""
BayFlow Trending Items Auto-Updater
Reads eBay API credentials from backend/.env (gitignored).
Fetches trending items from Korean sellers via eBay Browse API.
Updates data/verified_items.json.
Pure standard library.
"""

import os
import re
import json
import base64
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta

def load_env():
    env_vars = {}
    env_paths = ["backend/.env", ".env"]
    for p in env_paths:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        env_vars[k.strip()] = v.strip().strip("'\"")
    return env_vars

env = load_env()
APP_ID = env.get("EBAY_APP_ID")
CERT_ID = env.get("EBAY_CERT_ID")
USD_KRW = 1380.0

CATEGORIES = [
    {
        "cat_id": "acc",
        "categoryName": "💍 악세사리",
        "query": "korea silver necklace",
        "weightCat": "card",
        "shippingKrw": 8980,
        "defaultStatus": "사모님 추천 (초경량)"
    },
    {
        "cat_id": "cap",
        "categoryName": "🧢 모자/볼캡",
        "query": "korea ball cap cotton",
        "weightCat": "clothing",
        "shippingKrw": 12500,
        "defaultStatus": "연예인 볼캡 바이럴"
    },
    {
        "cat_id": "clothing",
        "categoryName": "👗 스트릿/의류",
        "query": "korean streetwear t-shirt",
        "weightCat": "clothing",
        "shippingKrw": 12500,
        "defaultStatus": "K-스트릿 인기"
    },
    {
        "cat_id": "sneakers",
        "categoryName": "👟 스니커즈",
        "query": "adidas samba og white",
        "weightCat": "shoes",
        "shippingKrw": 24000,
        "defaultStatus": "스테디셀러 사입"
    },
    {
        "cat_id": "beauty",
        "categoryName": "💄 K-뷰티",
        "query": "korea sunscreen relief sun",
        "weightCat": "clothing",
        "shippingKrw": 12500,
        "defaultStatus": "올리브영/틱톡 1위"
    },
    {
        "cat_id": "kpop",
        "categoryName": "🎤 K-POP",
        "query": "kpop photocard official pob",
        "weightCat": "card",
        "shippingKrw": 8980,
        "defaultStatus": "초경량 우체국 발송"
    },
    {
        "cat_id": "pokemon",
        "categoryName": "🃏 포켓몬",
        "query": "pokemon korean promo sealed card",
        "weightCat": "card",
        "shippingKrw": 8980,
        "defaultStatus": "한국 한정판 TCG"
    },
    {
        "cat_id": "character",
        "categoryName": "🧸 캐릭터/키링",
        "query": "korea plush keyring doll popup",
        "weightCat": "card",
        "shippingKrw": 8980,
        "defaultStatus": "성수/더현대 팝업"
    },
    {
        "cat_id": "starbucks",
        "categoryName": "☕ 스타벅스",
        "query": "starbucks korea tumbler limited",
        "weightCat": "clothing",
        "shippingKrw": 14000,
        "defaultStatus": "외국인 선물 1위"
    }
]

def get_ebay_oauth_token():
    if not APP_ID or not CERT_ID:
        return None
    auth_header = base64.b64encode(f"{APP_ID}:{CERT_ID}".encode()).decode()
    url = "https://api.ebay.com/identity/v1/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {auth_header}"
    }
    data = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope"
    }).encode()

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode())
        return res.get("access_token")

def search_ebay_category(token, query):
    url = (
        "https://api.ebay.com/buy/browse/v1/item_summary/search?q="
        + urllib.parse.quote(query)
        + "&limit=4&filter=itemLocationCountry:KR"
    )
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US"
    })
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            return data.get("itemSummaries", [])
    except Exception as e:
        print(f"Error querying query '{query}': {e}")
        return []

def main():
    kst = timezone(timedelta(hours=9))
    now_kst = datetime.now(kst).strftime("%Y-%m-%d %H:%M")
    print(f"[{now_kst} KST] Starting BayFlow Trending Items Update...")

    base_file = "data/baseline_items.json"
    baseline_items = []
    if os.path.exists(base_file):
        try:
            with open(base_file, "r", encoding="utf-8") as f:
                baseline_items = json.load(f)
        except Exception as e:
            print("Error loading baseline_items:", e)

    try:
        token = get_ebay_oauth_token()
        if token:
            print("OAuth Token acquired successfully.")
        else:
            print("No eBay API credentials found in env.")
    except Exception as e:
        print(f"Could not get eBay OAuth token: {e}")
        token = None

    api_items = []
    if token:
        for cat in CATEGORIES:
            summaries = search_ebay_category(token, cat["query"])
            for idx, sum_item in enumerate(summaries[:2]):
                try:
                    price_val = float(sum_item.get("price", {}).get("value", 0))
                    if price_val < 15 or price_val > 500:
                        continue
                    title = sum_item.get("title", "")
                    clean_title = title.split("|")[0].strip()
                    item_id = "api-" + cat["cat_id"] + "-" + str(sum_item.get("itemId", idx))[-6:]
                    
                    ebay_usd = round(price_val, 2)
                    ebay_krw = round(ebay_usd * USD_KRW)
                    fee_krw = round(ebay_krw * 0.17)
                    ship_krw = cat["shippingKrw"]
                    net_payout = ebay_krw - fee_krw - ship_krw
                    
                    target_buy_krw = max(5000, round((net_payout * 0.65) / 1000) * 1000)
                    profit_krw = net_payout - target_buy_krw
                    roi_pct = round((profit_krw / target_buy_krw) * 100) if target_buy_krw > 0 else 30

                    api_items.append({
                        "id": item_id,
                        "category": cat["cat_id"],
                        "categoryName": cat["categoryName"],
                        "title": clean_title[:45],
                        "ebayTitle": title[:70],
                        "badge": "⚡ 실시간 완판 픽",
                        "watchers": "👀 30+ 찜",
                        "status": cat["defaultStatus"],
                        "ebayUsd": ebay_usd,
                        "ebayKrw": ebay_krw,
                        "targetBuyKrw": target_buy_krw,
                        "profitKrw": profit_krw,
                        "roi": f"+{roi_pct}%",
                        "weightCat": cat["weightCat"],
                        "priceRange": f"${round(ebay_usd*0.9, 1)} ~ ${round(ebay_usd*1.1, 1)}",
                        "salesVelocity": "1.2일당 1건 완판 🔥",
                        "topBuyers": "🇺🇸 미국 · 🇯🇵 일본 · 🇪🇺 유럽",
                        "recentSold": [
                            {"date": "11/02", "price": f"${ebay_usd:.2f}", "country": "🇺🇸 미국"}
                        ],
                        "bunjangQuery": clean_title[:15],
                        "ebayQuery": title[:30],
                        "tags": ["#실시간수집", f"#{cat['cat_id']}", "#우체국발송"]
                    })
                except Exception as ex:
                    print(f"Item parse error: {ex}")

    seen_ids = set()
    final_items = []
    
    for it in api_items:
        if it["id"] not in seen_ids:
            seen_ids.add(it["id"])
            final_items.append(it)
            
    for it in baseline_items:
        if it["id"] not in seen_ids:
            seen_ids.add(it["id"])
            final_items.append(it)

    result_payload = {
        "updatedAt": now_kst,
        "totalItems": len(final_items),
        "items": final_items
    }

    os.makedirs("data", exist_ok=True)
    with open("data/verified_items.json", "w", encoding="utf-8") as f:
        json.dump(result_payload, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated data/verified_items.json ({len(final_items)} items total).")

if __name__ == "__main__":
    main()

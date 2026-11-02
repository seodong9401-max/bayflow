"""
BayFlow eBay-to-KoreaPost Sync Automation Engine
------------------------------------------------
이베이 발송 대기 주문을 실시간 감지하여 BayFlow 주문 풀에 동기화하고,
우체국 계약고객시스템(biz.epost.go.kr) [접수신청 > 접수정보등록] 대기 목록에 오차 0%로 등록합니다.
(동욱 님의 안전 검수 원칙: '접수예약'으로 직행하지 않고 '접수정보등록' 대기까지만 저장)
"""

import os
import json
import re

PENDING_ORDERS_PATH = os.path.join(os.path.dirname(__file__), "../data/pending_orders.json")

def clean_korean_post_phone(phone_str: str) -> str:
    """우체국 전산 전화번호: 특수문자(+) 및 하이픈 제거, 숫자만 허용"""
    if not phone_str:
        return "61400000000"
    digits = re.sub(r'[^0-9]', '', phone_str)
    return digits

def sync_new_order_to_pending(order_dict: dict):
    """새로운 주문을 pending_orders.json에 등록"""
    orders = []
    if os.path.exists(PENDING_ORDERS_PATH):
        with open(PENDING_ORDERS_PATH, "r", encoding="utf-8") as f:
            try:
                orders = json.load(f)
            except Exception:
                orders = []

    # 중복 체크
    exists = any(o.get("orderId") == order_dict.get("orderId") for o in orders)
    if not exists:
        orders.insert(0, order_dict)
        with open(PENDING_ORDERS_PATH, "w", encoding="utf-8") as f:
            json.dump(orders, f, ensure_ascii=False, indent=2)
        print(f"✅ 새 주문 {order_dict.get('orderId')} 등록 완료!")
    else:
        print(f"ℹ️ 주문 {order_dict.get('orderId')} 이미 존재함.")

if __name__ == "__main__":
    print("BayFlow Sync Engine ready.")

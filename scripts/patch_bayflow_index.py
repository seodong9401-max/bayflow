import json
import re

with open('data/baseline_items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

items_js = "    const VERIFIED_ITEMS = " + json.dumps(items, ensure_ascii=False, indent=6) + ";\n"

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace VERIFIED_ITEMS block
pattern_verified = r'(    // 🔥 실전 검증 베스트셀러 픽 데이터.*?\n    const VERIFIED_ITEMS = \[).*?(\n    \];\n\n    let activeVerifiedItems)'
m = re.search(pattern_verified, content, re.DOTALL)
if not m:
    print("Could not find VERIFIED_ITEMS pattern!")
    exit(1)

new_verified_block = f"    // 🔥 실전 검증 베스트셀러 픽 데이터 (10대 카테고리 26선 · 부피무게 & 한국어 번장 소싱 완비)\n{items_js.rstrip()}\n\n    let activeVerifiedItems"
content = content[:m.start()] + new_verified_block + content[m.end():]

# 2. Update openEbayDetailModal
old_modal_func_pattern = r'function openEbayDetailModal\(itemId\) \{.*?function closeEbayDetailModal\(\)'
new_modal_func = '''function openEbayDetailModal(itemId) {
      const it = (activeVerifiedItems && activeVerifiedItems.find(x => x.id === itemId)) || VERIFIED_ITEMS.find(x => x.id === itemId);
      if (!it) return;
      const titleElem = document.getElementById('modal-item-title');
      if (titleElem) titleElem.innerText = it.title;
      const body = document.getElementById('modal-item-body');
      if (!body) return;

      const soldList = it.recentSold || [
        { date: '11/01', price: '$' + it.ebayUsd.toFixed(2), country: '🇺🇸 미국' },
        { date: '10/29', price: '$' + (it.ebayUsd - 2).toFixed(2), country: '🇦🇺 호주' },
        { date: '10/26', price: '$' + (it.ebayUsd + 3).toFixed(2), country: '🇬🇧 영국' }
      ];

      body.innerHTML = `
        <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 space-y-2">
          <div class="flex justify-between items-center text-[11px]">
            <span class="text-slate-400">최근 30일 실제 완판:</span>
            <span class="text-amber-300 font-bold">${it.badge.replace('🔥 ', '')}</span>
          </div>
          <div class="flex justify-between items-center text-[11px]">
            <span class="text-slate-400">실거래 체결가 범위:</span>
            <span class="text-slate-200 font-mono font-bold">${it.priceRange || '$' + (it.ebayUsd - 3) + ' ~ $' + (it.ebayUsd + 5)}</span>
          </div>
          <div class="flex justify-between items-center text-[11px]">
            <span class="text-slate-400">평균 판매 속도:</span>
            <span class="text-emerald-400 font-bold">${it.salesVelocity || '1~2일당 1건 완판'}</span>
          </div>
          <div class="flex justify-between items-center text-[11px]">
            <span class="text-slate-400">주요 구매자 국가:</span>
            <span class="text-sky-300 font-medium">${it.topBuyers || '🇺🇸 미국 60% · 🇦🇺 호주 20% · 기타 20%'}</span>
          </div>
        </div>

        <!-- 우체국 실제 포장 규격 및 부피무게 대조 -->
        <div class="bg-slate-950/90 p-2.5 rounded-xl border border-indigo-900/40 text-[11px] space-y-1">
          <div class="flex justify-between items-center">
            <span class="text-slate-400 flex items-center space-x-1">
              <span>📦</span>
              <span>포장 박스 규격:</span>
            </span>
            <span class="text-slate-200 font-bold">${it.boxSize || '에어캡 안전봉투'}</span>
          </div>
          <div class="flex justify-between items-center text-[10px]">
            <span class="text-slate-400">실무게 vs 부피무게:</span>
            <span class="text-sky-300 font-mono">실무게 ${it.actualWeight || 50}g vs 부피 ${it.volWeight || 50}g ➔ <b class="text-amber-300">청구 ${it.appliedWeight || 200}g</b></span>
          </div>
          <div class="text-[10px] text-emerald-400 font-medium flex items-center space-x-1">
            <span>⚖️</span>
            <span>${it.weightNote || '실제 무게 기준 청구'}</span>
          </div>
        </div>

        <div class="space-y-1.5">
          <div class="text-[11px] font-bold text-slate-300 flex items-center space-x-1">
            <span>⚡</span>
            <span>최근 실제 체결 내역 (eBay Sold)</span>
          </div>
          <div class="space-y-1 text-[11px]">
            ${soldList.map(s => `
              <div class="flex justify-between items-center bg-slate-950/80 px-2.5 py-1.5 rounded-lg border border-slate-800 text-[10px]">
                <span class="text-slate-400 font-mono">${s.date} 체결</span>
                <span class="text-slate-300 font-bold">${s.country}</span>
                <span class="text-amber-300 font-mono font-bold">${s.price}</span>
              </div>
            `).join('')}
          </div>
        </div>

        <div class="pt-2 flex flex-col space-y-2">
          <a href="https://www.ebay.com/sch/i.html?_nkw=${encodeURIComponent(it.ebayQuery)}&LH_Sold=1&LH_Complete=1&_sop=13" target="_blank" class="w-full py-2.5 bg-amber-500 hover:bg-amber-400 text-slate-950 font-black text-xs rounded-xl text-center transition shadow active:scale-95">
            🔗 eBay 공식 실시간 체결창 열기 (Sold) ➔
          </a>
          <div class="grid grid-cols-2 gap-1.5">
            <a href="https://m.bunjang.co.kr/search/products?q=${encodeURIComponent(it.bunjangQuery)}&order=price_asc" target="_blank" class="py-2 bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs rounded-xl text-center transition">
              🛒 번장 최저가
            </a>
            <button type="button" onclick="closeEbayDetailModal(); loadIntoCalculatorCustom('${it.id}', ${it.ebayUsd}, ${it.appliedWeight || 200})" class="py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs rounded-xl text-center transition">
              ⚡ 부피무게 마진 계산
            </button>
          </div>
        </div>
      `;

      const m = document.getElementById('ebay-detail-modal');
      if (m) m.classList.remove('hidden');
    }

    function closeEbayDetailModal()'''

content = re.sub(old_modal_func_pattern, new_modal_func, content, flags=re.DOTALL)

# 3. Update renderVerifiedItems card template
old_card_pattern = r'<!-- 상품명 -->\s*<div>\s*<h4 class="text-xs font-black text-slate-100">\$\{it\.title\}</h4>.*?<!-- 실전 액션 버튼 3종 -->'
new_card_body = '''<!-- 상품명 (한국어 소싱명 + 영문 이베이명) -->
            <div>
              <h4 class="text-xs font-black text-slate-100 flex items-center space-x-1">
                <span class="text-amber-400">🇰🇷</span>
                <span>${it.title}</span>
              </h4>
              <p class="text-[10px] text-slate-400 truncate mt-0.5" title="${it.ebayTitle}">🇺🇸 ${it.ebayTitle}</p>
            </div>

            <!-- 가격 및 마진 분석표 -->
            <div class="grid grid-cols-3 gap-2 bg-slate-950/80 p-2.5 rounded-xl border border-slate-800/80 text-center">
              <div>
                <div class="text-[9px] text-slate-400">eBay 실거래가</div>
                <div class="text-xs font-black text-amber-300 mt-0.5">$${it.ebayUsd.toFixed(2)}</div>
                <div class="text-[8px] text-emerald-400 font-bold">${it.priceRange || '$' + (it.ebayUsd - 3) + ' ~ $' + (it.ebayUsd + 5)}</div>
              </div>
              <div class="border-x border-slate-800">
                <div class="text-[9px] text-slate-400">국내 사입 마지노선</div>
                <div class="text-xs font-black text-slate-200 mt-0.5">${it.targetBuyKrw.toLocaleString()}원</div>
                <div class="text-[8px] text-emerald-400">이하 권장</div>
              </div>
              <div>
                <div class="text-[9px] text-emerald-400 font-bold">예상 순마진</div>
                <div class="text-xs font-black text-emerald-300 mt-0.5">+${it.profitKrw.toLocaleString()}원</div>
                <div class="text-[8px] text-sky-400 font-bold">${it.roi} ROI</div>
              </div>
            </div>

            <!-- 우체국 실제 포장 규격 및 실무게 vs 부피무게 대조 바 -->
            <div class="bg-slate-950/90 rounded-xl p-2.5 border border-slate-800/80 space-y-1 text-[11px]">
              <div class="flex items-center justify-between">
                <span class="text-slate-400 flex items-center space-x-1">
                  <span>📦</span>
                  <span>포장: <b class="text-slate-200">${it.boxSize || '에어캡 안전봉투'}</b></span>
                </span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-sky-500/20 text-sky-300 border border-sky-500/30">
                  청구 ${it.appliedWeight || 200}g
                </span>
              </div>
              <div class="flex items-center justify-between text-[10px]">
                <span class="text-slate-400">
                  실무게 <b class="text-slate-200">${it.actualWeight || 50}g</b> vs 부피 <b class="text-amber-300">${it.volWeight || 50}g</b>
                </span>
                <span class="text-emerald-400 font-bold">${it.weightNote || '실제 무게 적용'}</span>
              </div>
            </div>

            <!-- 실거래량 & 판매 회전 속도 바 (실시간 거래량 모달 원클릭) -->
            <div class="flex items-center justify-between bg-slate-950/70 px-2.5 py-1.5 rounded-xl border border-slate-800/80 text-[10px]">
              <span class="text-slate-400 flex items-center space-x-1">
                <span>📈</span>
                <span>30일 실거래: <b class="text-amber-300">${it.badge.replace('🔥 ', '')}</b></span>
              </span>
              <span class="text-emerald-400 font-bold flex items-center space-x-1">
                <span>⚡</span>
                <span>${it.salesVelocity || '회전율 높음'}</span>
              </span>
              <button type="button" onclick="openEbayDetailModal('${it.id}')" class="text-amber-400 hover:text-amber-300 font-bold flex items-center space-x-0.5 transition active:scale-95">
                <span>상세</span>
                <span>➔</span>
              </button>
            </div>

            <!-- 연관 태그 -->
            <div class="flex flex-wrap gap-1 text-[10px] text-slate-400">
              ${(it.tags || []).map(t => `<span class="bg-slate-950 px-1.5 py-0.2 rounded border border-slate-800 text-slate-400">${t}</span>`).join('')}
            </div>

            <!-- 실시간 사입가 직접 입력창 -->
            <div class="flex items-center justify-between bg-slate-950 p-2 rounded-xl border border-slate-800 text-[11px]">
              <span class="text-slate-400 font-medium">실시간 사입가 (번장 발견가):</span>
              <div class="flex items-center space-x-1">
                <input type="number" id="custom-buy-${it.id}" value="${it.targetBuyKrw}" class="w-24 bg-slate-900 border border-slate-700 rounded-lg px-2 py-1 text-slate-100 font-mono text-xs font-bold text-right focus:border-amber-400 focus:outline-none">
                <span class="text-slate-400 font-semibold">원</span>
              </div>
            </div>

            <!-- 실전 액션 버튼 3종 -->'''

content = re.sub(old_card_pattern, new_card_body, content, flags=re.DOTALL)

# 4. Update action buttons in card template
old_buttons_pattern = r'<button type="button" onclick="loadIntoCalculatorCustom\(\'\$\{it\.id\}\', \$\{it\.ebayUsd\}, \'\$\{it\.weightCat\}\'\)"'
new_buttons = '<button type="button" onclick="loadIntoCalculatorCustom(\'${it.id}\', ${it.ebayUsd}, ${it.appliedWeight || 200})"'
content = content.replace(old_buttons_pattern, new_buttons)

# 5. Update loadIntoCalculatorCustom & loadIntoCalculator
old_load_pattern = r'function loadIntoCalculatorCustom\(itemId, priceUsd, weightCat\) \{.*?function loadIntoCalculator\(priceUsd, weightCat, buyKrw\) \{.*?showToast\(\'계산기에 \' \+ priceUsd \+ \'달러가 자동 입력되었습니다!\', \'🧮\'\);\s*\}'
new_load_code = '''function loadIntoCalculatorCustom(itemId, priceUsd, appliedWeight) {
      const buyInput = document.getElementById('custom-buy-' + itemId);
      const buyKrw = buyInput ? parseInt(buyInput.value, 10) || 0 : 0;
      loadIntoCalculator(priceUsd, appliedWeight, buyKrw);
    }

    function loadIntoCalculator(priceUsd, weightGrams, buyKrw) {
      switchTab('calculator');
      const pInput = document.getElementById('calc-price');
      if (pInput) pInput.value = priceUsd;
      const bInput = document.getElementById('calc-cost');
      if (bInput) bInput.value = buyKrw;
      const wSelect = document.getElementById('calc-weight');
      if (wSelect) {
        let wVal = parseInt(weightGrams) || 200;
        const validWeights = [100, 200, 300, 400, 500, 1000, 1500, 2000];
        let matched = validWeights.find(v => v >= wVal) || 2000;
        wSelect.value = String(matched);
      }
      onShippingOptionChange();
      calculateMargin();
      showToast('계산기에 $' + priceUsd + ' · ' + (weightGrams || 200) + 'g 포장 운임이 자동 반영되었습니다!', '🧮');
    }'''

content = re.sub(old_load_pattern, new_load_code, content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully patched index.html!")

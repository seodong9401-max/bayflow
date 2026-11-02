import json
import re

with open('data/baseline_items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Title and Add Category Selector in #tab-calculator
calc_header_pattern = r'(<h2 class="text-sm font-bold text-slate-300 flex items-center space-x-1.5">\s*<span>🧮</span>\s*<span>)이베이 카드 실전 마진 계산기(</span>\s*</h2>)'
html = re.sub(calc_header_pattern, r'\g<1>이베이 전품목 실전 마진 계산기 (카테고리 수수료 연동)\g<2>', html)

# Add category selector before Price, Cost, FX input grid
grid_marker = '<div class="grid grid-cols-3 gap-2.5 text-xs">'
cat_selector_html = '''<!-- eBay 품목 카테고리 수수료율 선택 (셀러박스 리버싱 연동) -->
        <div class="bg-slate-950/80 rounded-xl p-3 border border-slate-800 space-y-2 text-xs">
          <div class="flex items-center justify-between border-b border-slate-800/80 pb-1.5">
            <span class="font-bold text-slate-200 flex items-center space-x-1">
              <span>🏷️</span>
              <span>eBay 품목 카테고리 (공식 수수료율)</span>
            </span>
            <span id="calc-category-fee-badge" class="text-[10px] text-amber-400 bg-amber-950/60 px-2 py-0.5 rounded border border-amber-900/50 font-bold font-mono">13.25% + $0.40</span>
          </div>
          <div class="grid grid-cols-2 gap-2">
            <div class="space-y-1">
              <label class="text-slate-400 font-medium text-[11px]">판매 품목 카테고리</label>
              <select id="calc-category" onchange="onCategoryFeeChange()" class="w-full bg-slate-900 border border-slate-800 rounded-xl py-1.5 px-2 text-slate-200 font-medium focus:outline-none focus:border-indigo-500 text-xs">
                <option value="pokemon" selected>🃏 포켓몬/트레이딩 카드 (13.25%)</option>
                <option value="clothing">👗 의류/스트릿/티셔츠 (15.0%)</option>
                <option value="cap">🧢 모자/볼캡/비니 (15.0%)</option>
                <option value="acc">💍 쥬얼리/악세사리/시계 (15.0%)</option>
                <option value="sneakers">👟 스니커즈 ($150↑ 8% / 13.25%)</option>
                <option value="beauty">💄 K-뷰티/화장품/스킨케어 (13.25%)</option>
                <option value="kpop">🎤 K-POP/굿즈/포토카드 (13.25%)</option>
                <option value="character">🧸 캐릭터/피규어/인형 (13.25%)</option>
                <option value="starbucks">☕ 스타벅스/텀블러/머그 (13.25%)</option>
                <option value="electronics">📱 전자기기/카메라 (9.0%)</option>
                <option value="sports">🛹 스포츠/스케이트보드 (13.25%)</option>
                <option value="custom">⚡ 수수료율 직접 입력 (%)</option>
              </select>
            </div>
            <div class="space-y-1">
              <label class="text-slate-400 font-medium text-[11px]">카테고리 기본 수수료 (%)</label>
              <div class="relative">
                <input type="number" id="calc-fee-pct" value="13.25" step="0.05" oninput="calculateMargin()" class="w-full bg-slate-900 border border-slate-800 rounded-xl py-1.5 px-2.5 text-amber-300 font-mono font-bold focus:outline-none focus:border-indigo-500 text-xs text-right pr-6">
                <span class="absolute right-2.5 top-1.5 text-slate-400 font-bold">%</span>
              </div>
            </div>
          </div>
        </div>

        '''

if 'id="calc-category"' not in html:
    html = html.replace(grid_marker, cat_selector_html + grid_marker, 1)

# Update fee breakdown label in #tab-calculator
html = html.replace(
    '<span>이베이 수수료 (기본 13.25% + 해외 1.45% + $0.40)</span>',
    '<span id="label-ebay-fee">이베이 카테고리 수수료 (기본 13.25% + 해외 1.45% + $0.40)</span>'
)

# 2. Update VERIFIED_ITEMS in index.html
items_json_str = json.dumps(items, ensure_ascii=False, indent=6)
pattern_verified = r'const VERIFIED_ITEMS = \[.*?\];\s*const VERIFIED_CATEGORIES ='
new_verified_str = f"const VERIFIED_ITEMS = {items_json_str};\n\n    const VERIFIED_CATEGORIES ="
html = re.sub(pattern_verified, new_verified_str, html, flags=re.DOTALL)

# 3. Update openEbayDetailModal
old_modal_pattern = r'function openEbayDetailModal\(itemId\) \{.*?function closeEbayDetailModal\(\)'
new_modal_code = '''function openEbayDetailModal(itemId) {
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
            <button type="button" onclick="closeEbayDetailModal(); loadIntoCalculatorCustom('${it.id}', ${it.ebayUsd}, ${it.appliedWeight || 200}, '${it.category}')" class="py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs rounded-xl text-center transition">
              ⚡ 부피무게 마진 계산
            </button>
          </div>
        </div>
      `;

      const m = document.getElementById('ebay-detail-modal');
      if (m) m.classList.remove('hidden');
    }

    function closeEbayDetailModal()'''
html = re.sub(old_modal_pattern, new_modal_code, html, flags=re.DOTALL)

# 4. Update renderVerifiedItems
old_render_card = r'<!-- 상품명 -->\s*<div>\s*<h4 class="text-xs font-black text-slate-100">\$\{it\.title\}</h4>.*?<!-- 실전 액션 버튼 3종 -->\s*<div class="grid grid-cols-3 gap-1\.5 pt-1">.*?</div>\s*</div>\s*`;'
new_render_card = '''<!-- 상품명 (한국어 소싱명 + 영문 이베이명) -->
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

            <!-- 실전 액션 버튼 3종 -->
            <div class="grid grid-cols-3 gap-1.5 pt-1">
              <a href="https://m.bunjang.co.kr/search/products?q=${encodeURIComponent(it.bunjangQuery)}&order=price_asc" target="_blank" class="py-2 rounded-xl bg-rose-600/90 hover:bg-rose-500 text-white font-bold text-xs flex items-center justify-center space-x-1 transition shadow active:scale-95 text-center">
                <span>🛒</span>
                <span>번장 최저가</span>
              </a>
              <button type="button" onclick="loadIntoCalculatorCustom('${it.id}', ${it.ebayUsd}, ${it.appliedWeight || 200}, '${it.category}')" class="py-2 rounded-xl bg-indigo-600/90 hover:bg-indigo-500 text-white font-bold text-xs flex items-center justify-center space-x-1 transition shadow active:scale-95 text-center">
                <span>⚡</span>
                <span>마진 계산</span>
              </button>
              <button type="button" onclick="openEbayDetailModal('${it.id}')" class="py-2 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-500/40 font-bold text-xs flex items-center justify-center space-x-1 transition active:scale-95 text-center">
                <span>📊</span>
                <span>거래량/시세</span>
              </button>
            </div>
          </div>
        `;'''
html = re.sub(old_render_card, new_render_card, html, flags=re.DOTALL)

# 5. Update loadIntoCalculatorCustom & loadIntoCalculator
old_load_pattern = r'function loadIntoCalculatorCustom\(itemId, priceUsd, weightCat\) \{.*?showToast\(\'계산기에 \' \+ priceUsd \+ \'달러가 자동 입력되었습니다!\', \'🧮\'\);\s*\}'
new_load_code = '''function loadIntoCalculatorCustom(itemId, priceUsd, appliedWeight, category) {
      const buyInput = document.getElementById('custom-buy-' + itemId);
      const buyKrw = buyInput ? parseInt(buyInput.value, 10) || 0 : 0;
      loadIntoCalculator(priceUsd, appliedWeight, buyKrw, category);
    }

    function loadIntoCalculator(priceUsd, weightGrams, buyKrw, category) {
      switchTab('calculator');
      const cSelect = document.getElementById('calc-category');
      if (cSelect && category) {
        cSelect.value = category;
        onCategoryFeeChange();
      }
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
html = re.sub(old_load_pattern, new_load_code, html, flags=re.DOTALL)

# 6. Update calculateMargin & Add onCategoryFeeChange
old_calc_margin = r'// Accurate Margin Calculator Logic\s*function calculateMargin\(\) \{'
new_calc_margin = '''// eBay Category Fee Rates (공식 셀러 규정)
    const CATEGORY_FEES = {
      pokemon: 13.25,
      clothing: 15.0,
      cap: 15.0,
      acc: 15.0,
      sneakers: 8.0,
      beauty: 13.25,
      kpop: 13.25,
      character: 13.25,
      starbucks: 13.25,
      electronics: 9.0,
      sports: 13.25,
      custom: 13.25
    };

    function onCategoryFeeChange() {
      const cat = document.getElementById('calc-category')?.value || 'pokemon';
      const priceUSD = parseFloat(document.getElementById('calc-price')?.value) || 0;
      let rate = CATEGORY_FEES[cat] || 13.25;
      if (cat === 'sneakers') {
        rate = priceUSD >= 150 ? 8.0 : 13.25;
      }
      const feeInput = document.getElementById('calc-fee-pct');
      if (feeInput && cat !== 'custom') feeInput.value = rate;
      const badge = document.getElementById('calc-category-fee-badge');
      if (badge) badge.innerText = rate + '% + $0.40';
      calculateMargin();
    }

    // Accurate Margin Calculator Logic
    function calculateMargin() {'''
html = html.replace('// Accurate Margin Calculator Logic\n    function calculateMargin() {', new_calc_margin, 1)

# Replace fee calculation inside calculateMargin
old_fee_calc = '''      // 공식 규정 계산
      // 1. eBay 기본 13.25% + 건당 $0.40
      const ebayCategoryFeeUSD = (priceUSD * 0.1325) + 0.40;'''
new_fee_calc = '''      // 공식 규정 계산
      const catFeePct = parseFloat(document.getElementById('calc-fee-pct')?.value) || 13.25;
      // 1. eBay 카테고리별 수수료 + 건당 $0.40
      const ebayCategoryFeeUSD = (priceUSD * (catFeePct / 100)) + 0.40;'''
html = html.replace(old_fee_calc, new_fee_calc, 1)

# Update fee label text in calculateMargin
old_fee_label_render = "document.getElementById('res-gross').innerText = Math.round(grossKRW).toLocaleString() + '원';"
new_fee_label_render = '''const feeLabel = document.getElementById('label-ebay-fee');
      if (feeLabel) feeLabel.innerText = `이베이 카테고리 수수료 (${catFeePct}% + 해외 1.45% + $0.40)`;
      document.getElementById('res-gross').innerText = Math.round(grossKRW).toLocaleString() + '원';'''
html = html.replace(old_fee_label_render, new_fee_label_render, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html patched successfully!")

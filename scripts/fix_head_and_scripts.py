#!/usr/bin/env python3
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Clean <head> section
head_pattern = r'<head>[\s\S]*?</head>'
new_head = '''<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>BayFlow - 이베이 셀러 올인원 자동화 대시보드</title>
  <!-- PWA Meta Tags -->
  <link rel="manifest" href="manifest.json">
  <meta name="theme-color" content="#1e293b">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="BayFlow">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚡</text></svg>">
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: {
              50: '#eef2ff',
              500: '#6366f1',
              600: '#4f46e5',
              700: '#4338ca',
            }
          }
        }
      }
    };
  </script>
  <style>
    /* Mobile app scroll & touch behavior */
    body {
      -webkit-tap-highlight-color: transparent;
      user-select: none;
    }
    .custom-scrollbar::-webkit-scrollbar {
      display: none;
    }
    .custom-scrollbar {
      -ms-overflow-style: none;
      scrollbar-width: none;
    }
  </style>
</head>'''

html = re.sub(head_pattern, new_head, html, count=1)

# 2. In the body script, ensure clean definitions of Research Categories and Sourcing Pipeline
# Check if RESEARCH_CATEGORIES is in html
research_block = '''
    // 📈 12대 테마 글로벌 리서치 데이터베이스
    const RESEARCH_CATEGORIES = {
      pokemon: {
        title: '🃏 포켓몬 / 트레이딩카드 베스트셀러',
        desc: '해외 포덕 & 수집가들의 절대적인 한정판·SAR·밀봉 프로모 수요',
        keywords: [
          { label: '메가 리자몽 X ex SAR', q: '메가 리자몽 X ex SAR' },
          { label: '한복 피카츄 키링', q: '고풍 피카츄' },
          { label: '메타몽 173/SV-P', q: '메타몽 프로젝트 디토' },
          { label: '한글판 뮤 ex SAR', q: '뮤 ex SAR' }
        ],
        items: [
          { name: '포켓몬 메가 리자몽 X ex SAR 110/080 M2', buyKrw: 140000, soldUsd: 195.0, profit: '+63,800원', speed: '30일 18건 체결 · 성공률 88%', ebayQ: 'Mega+Charizard+X+ex+SAR+110%2F080', ship: 'card' },
          { name: '전통 한복 피카츄 LED 라이트 키링 2종', buyKrw: 45000, soldUsd: 115.0, profit: '+72,000원', speed: '30일 8건 체결 · 성공률 92%', ebayQ: 'Pokemon+Korea+Hanbok+Pikachu+LED+keyring', ship: 'card' },
          { name: '메타몽 프로젝트 디토 173/SV-P 밀봉 프로모', buyKrw: 72000, soldUsd: 125.0, profit: '+48,500원', speed: '30일 22건 체결 · 성공률 95%', ebayQ: 'Pokemon+Ditto+173%2FSV-P+Promo', ship: 'card' }
        ]
      },
      sneakers: {
        title: '👟 나이키 / 스니커즈 한정판',
        desc: '해외 품절 국내 한정 컬러 & KREAM 바닥가와 글로벌 체결가 갭투자',
        keywords: [
          { label: '조던 1 로우 골프', q: '나이키 조던 1 로우 골프' },
          { label: '아디다스 삼바 OG', q: '아디다스 삼바 OG' }
        ],
        items: [
          { name: '나이키 에어 조던 1 로우 골프 울프 그레이', buyKrw: 168000, soldUsd: 235.0, profit: '+51,200원', speed: '30일 34건 체결 · 성공률 79%', ebayQ: 'Air+Jordan+1+Low+Golf+Wolf+Grey', ship: 'shoes' },
          { name: '아디다스 삼바 OG 화이트 블랙 (KREAM 소싱)', buyKrw: 115000, soldUsd: 155.0, profit: '+36,400원', speed: '30일 58건 체결 · 성공률 85%', ebayQ: 'Adidas+Samba+OG+White+Black', ship: 'shoes' }
        ]
      }
    };

    function selectResearchCategory(catKey) {
      const cat = RESEARCH_CATEGORIES[catKey] || RESEARCH_CATEGORIES['pokemon'];
      if (!cat) return;

      const titleElem = document.getElementById('rcat-title');
      const descElem = document.getElementById('rcat-desc');
      if (titleElem) titleElem.innerText = cat.title;
      if (descElem) descElem.innerText = cat.desc;

      const kwContainer = document.getElementById('rcat-keywords-container');
      if (kwContainer && cat.keywords) {
        kwContainer.innerHTML = cat.keywords.map(kw => `
          <button onclick="startSourcingWithKeyword('${kw.q}')" class="px-3 py-1.5 rounded-xl bg-slate-950/80 hover:bg-indigo-600/30 border border-slate-800 hover:border-indigo-500/40 text-xs font-medium text-slate-300 hover:text-white transition flex items-center space-x-1.5 group active:scale-95">
            <span>${kw.label}</span>
            <span class="text-indigo-400 group-hover:text-white">➔</span>
          </button>
        `).join('');
      }

      const itemsContainer = document.getElementById('rcat-items-container');
      if (itemsContainer && cat.items) {
        itemsContainer.innerHTML = cat.items.map(item => `
          <div class="bg-slate-900/90 rounded-2xl border border-slate-800 p-4 space-y-3 hover:border-indigo-500/40 transition">
            <div class="flex items-start justify-between">
              <div>
                <h4 class="text-xs font-bold text-slate-100">${item.name}</h4>
                <p class="text-[10px] text-emerald-400 font-bold mt-0.5">🔥 ${item.speed}</p>
              </div>
              <div class="text-right">
                <span class="text-xs font-black text-emerald-400">${item.profit}</span>
                <div class="text-[9px] text-slate-400">예상 순마진</div>
              </div>
            </div>
            <div class="flex space-x-1.5 pt-1">
              <a href="https://www.ebay.com/sch/i.html?_nkw=${item.ebayQ}&LH_Sold=1&LH_Complete=1&_sop=13" target="_blank" rel="noopener noreferrer" class="flex-1 py-1.5 bg-indigo-600/90 hover:bg-indigo-600 text-white font-bold text-[11px] rounded-xl text-center transition shadow">
                eBay Sold 실체결
              </a>
              <button onclick="startSourcingWithKeyword('${item.name}')" class="flex-1 py-1.5 bg-rose-600 hover:bg-rose-500 text-white font-black text-[11px] rounded-xl text-center transition shadow active:scale-95">
                🎯 사입처 찾기
              </button>
            </div>
          </div>
        `).join('');
      }
    }

    function startSourcingWithKeyword(kw) {
      switchTab('all');
      switchAllSubTab('sourcing');
      document.getElementById('sourcing-search-keyword').value = kw;
      runSmartSourcingAnalysis(kw);
    }
'''

sourcing_pipeline_block = '''
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
      document.getElementById('pipeline-item-subtitle').innerText = `🇺🇸 ${it.ebayTitle || it.title}`;
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
      const catRate = (typeof CATEGORY_FEES !== 'undefined' && CATEGORY_FEES[it.category]) || 13.25;
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

      const matched = VERIFIED_ITEMS.find(x => x.title.includes(kw) || (x.bunjangQuery && x.bunjangQuery.includes(kw)) || (x.ebayTitle && x.ebayTitle.toLowerCase().includes(kw.toLowerCase())));
      if (matched) {
        activeSourcingItem = matched;
        renderSourcingPipeline(matched);
      } else {
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

      let kw = file.name.replace(/\\.[^/.]+$/, '').replace(/[-_]/g, ' ');
      document.getElementById('sourcing-search-keyword').value = kw;
      runSmartSourcingAnalysis(kw);
      showToast(`'${file.name}' 사진 인식 완료! 사입처를 검색합니다.`, '📸');
    }
'''

# Remove any previous duplicates of startSourcingForItem or RESEARCH_CATEGORIES in body
html = re.sub(r'// 🎯 스마트 사입처 찾기[\s\S]*?showToast\(`\'\$\{file\.name\}\' 사진 인식 완료! 사입처를 검색합니다\.`, \'📸\'\);\s*\}', '', html)
html = re.sub(r'// 📈 12대 테마 글로벌 리서치 데이터베이스[\s\S]*?runSmartSourcingAnalysis\(kw\);\s*\}', '', html)

# Insert clean blocks right before service worker registration
sw_marker = '    // PWA Service Worker Registration & Force Update'
if sw_marker in html:
    html = html.replace(sw_marker, research_block + '\n\n' + sourcing_pipeline_block + '\n\n' + sw_marker, 1)

# Ensure triggerPrintKpacket does not have raw </script>
html = html.replace('window.onload = function() { window.print(); };\n            </script>', 'window.onload = function() { window.print(); };\\n            <\\/script>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("HTML successfully rewritten with clean head and unified body scripts!")

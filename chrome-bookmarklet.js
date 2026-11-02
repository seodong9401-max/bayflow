// BayFlow Smart Cloud Bookmarklet for Korea Post K-Packet Auto-Fill
// 인터넷우체국 계약고객시스템(biz.epost.go.kr) 실시간 클라우드 연동 1초 자동완성

(async function() {
  try {
    const app = window.application;
    if (!app || !app.mainframe) {
      alert('[BayFlow] 인터넷우체국 계약고객시스템(biz.epost.go.kr) 화면에서 실행해 주세요!');
      return;
    }

    const wfs = app.mainframe.VFrameSet?.HFrameSet?.VFrameSet1?.workFrameSet;
    if (!wfs) {
      alert('[BayFlow] 계약EMS 시스템 화면을 찾을 수 없습니다.');
      return;
    }

    // 개별등록 열려 있는지 확인
    let dw = null;
    for (let i = 0; i < (wfs.all ? wfs.all.length : 0); i++) {
      const f = wfs.all[i];
      if (f.form && f.form.div_contents && f.form.div_contents.div_work) {
        const u = f.form.div_contents.div_work.url || '';
        if (u.includes('pafao07b27')) {
          dw = f.form.div_contents.div_work;
          break;
        }
      }
    }

    if (!dw) {
      if (window.comSys && window.comSys.openMenu) {
        window.comSys.openMenu("ESHIP_1_27");
        alert('[BayFlow] 개별등록 화면을 열었습니다!\n\n화면이 완전히 뜨면 북마크를 한 번 더 눌러주세요.');
        return;
      } else {
        alert('[BayFlow] 우체국 메뉴에서 [접수신청 > 접수정보등록 > 개별등록]을 먼저 열어주세요!');
        return;
      }
    }

    // 1. BayFlow 클라우드에서 실시간 최신 주문 목록 조회
    let orders = [];
    try {
      const res = await fetch('https://seodong9401-max.github.io/bayflow/data/pending_orders.json?t=' + Date.now());
      if (res.ok) orders = await res.json();
    } catch(e) {
      console.warn('API fetch 실패', e);
    }

    // 미발송(등기번호 없는 대기건) 우선 필터
    const unfulfilled = orders.filter(o => !o.tracking || o.status === 'AWAITING_SHIPMENT');
    const targetList = unfulfilled.length > 0 ? unfulfilled : orders;

    if (targetList.length === 0) {
      alert('[BayFlow] 현재 등록 대기 중인 주문이 없습니다!');
      return;
    }

    let o = targetList[0];
    if (targetList.length > 1) {
      let promptMsg = '[BayFlow] 등록할 주문을 선택하세요:\n\n';
      targetList.forEach((item, idx) => {
        promptMsg += (idx + 1) + '. ' + item.buyerName + ' (' + (item.countryName || item.country) + ' / $' + item.totalUsd + ')\n';
      });
      promptMsg += '\n번호를 입력하세요 (기본 1):';
      const choice = prompt(promptMsg, '1');
      if (choice === null) return;
      const selIdx = parseInt(choice) - 1;
      if (selIdx >= 0 && selIdx < targetList.length) o = targetList[selIdx];
    }

    // 2. 수취인 정보 주입 (dsList)
    if (dw.dsList) {
      dw.dsList.setColumn(0, 'countrycd', o.country);
      dw.dsList.setColumn(0, 'countrynm', (o.countryName || o.country).split(' ')[0]);
      dw.dsList.setColumn(0, 'receivezipcode', o.zip);
      dw.dsList.setColumn(0, 'receiveaddr1', o.state || '');
      dw.dsList.setColumn(0, 'receiveaddr2', o.city || '');
      dw.dsList.setColumn(0, 'receiveaddr3', o.addr1 + (o.addr2 ? ' ' + o.addr2 : ''));
      dw.dsList.setColumn(0, 'receivename', o.buyerName || o.buyer);
      dw.dsList.setColumn(0, 'receivetelno', o.tel || '010-0000-0000');
      dw.dsList.setColumn(0, 'receivemail', (o.buyer && o.buyer.includes('@')) ? o.buyer : (o.buyer + '@ebay.com'));
      dw.dsList.setColumn(0, 'orderno', o.orderId);
      dw.dsList.setColumn(0, 'premiumcd', '14'); // K-Packet
      dw.dsList.setColumn(0, 'em_ee', 'rl');       // K-Packet
      dw.dsList.setColumn(0, 'totweight', o.chargeWeight || 100);
    }

    // 3. 세관신고서(CN22) 주입 (dsCustomReport)
    if (dw.dsCustomReport) {
      dw.dsCustomReport.clearData();
      const r = dw.dsCustomReport.addRow();
      dw.dsCustomReport.setColumn(r, 'contents', o.customsDesc || 'Playing cards');
      dw.dsCustomReport.setColumn(r, 'cnt', o.qty || 1);
      dw.dsCustomReport.setColumn(r, 'netwght', o.chargeWeight || 100);
      dw.dsCustomReport.setColumn(r, 'prc', Math.round(o.totalUsd));
      dw.dsCustomReport.setColumn(r, 'hscode', o.hsCode || '9504400000');
      dw.dsCustomReport.setColumn(r, 'origin', 'KR');
      dw.dsCustomReport.setColumn(r, 'EM_gubun', 'Merchandise');
      dw.dsCustomReport.setColumn(r, 'currunitcd', 'USD');
    }

    if (dw.resetCtrl) dw.resetCtrl();

    alert('✅ [BayFlow] 우체국 개별등록 1초 자동입력 완료!\n\n' +
          '• 수취인명: ' + (o.buyerName || o.buyer) + '\n' +
          '• 국가/우편번호: ' + (o.countryName || o.country) + ' / ' + o.zip + '\n' +
          '• 주소: ' + (o.state || '') + ' ' + (o.city || '') + ' ' + o.addr1 + '\n' +
          '• 세관품명: ' + (o.customsDesc || 'Playing cards') + ' ($' + o.totalUsd + ' / ' + (o.chargeWeight || 100) + 'g)\n' +
          '• HS CODE: ' + (o.hsCode || '9504400000') + '\n\n' +
          '내용 눈으로 슥 확인하신 뒤 맨 아래 [등록하고 창닫기]를 누르시면 접수정보등록 목록에 저장됩니다!');

  } catch(e) {
    alert('[BayFlow] 오류 발생: ' + e.message);
  }
})();

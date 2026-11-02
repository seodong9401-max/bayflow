// BayFlow Chrome Bookmarklet for Korea Post K-Packet Auto-Fill
// 인터넷우체국 계약고객시스템(biz.epost.go.kr) 개별등록 1초 자동완성 스크립트
// 동욱 님 PC 실사진(eBay Seller Hub 주문 #02-15385-21929) 100% 실측 매핑

(function() {
  try {
    const orderData = {
      orderId: "02-15385-21929",
      buyer: "darkrain65",
      name: "Patrick Daly-Andrusiak",
      country: "AU",
      countryNm: "호주",
      zip: "3977",
      addr1: "VIC",
      addr2: "Cranbourne North",
      addr3: "10 Sierra Boulevard",
      tel: "61-431-437-335",
      email: "0093f0f3ccd2a17faed5@members.ebay.com",
      item: "Playing cards",
      hsCode: "9504400000",
      qty: 1,
      weight: 100,
      price: 185
    };

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
    let targetWork = null;
    for (let i = 0; i < (wfs.all ? wfs.all.length : 0); i++) {
      const f = wfs.all[i];
      if (f.form && f.form.div_contents && f.form.div_contents.div_work) {
        const u = f.form.div_contents.div_work.url || '';
        if (u.includes('pafao07b27')) {
          targetWork = f.form.div_contents.div_work;
          break;
        }
      }
    }

    if (!targetWork) {
      if (window.comSys && window.comSys.openMenu) {
        window.comSys.openMenu("ESHIP_1_27");
        alert('[BayFlow] 개별등록 화면을 열었습니다!\n\n화면이 완전히 뜨면 북마크를 한 번 더 눌러주세요.');
        return;
      } else {
        alert('[BayFlow] 우체국 메뉴에서 [접수신청 > 접수정보등록 > 개별등록]을 먼저 열어주세요!');
        return;
      }
    }

    // 1. 수취인 정보 주입 (dsList)
    if (targetWork.dsList) {
      targetWork.dsList.setColumn(0, 'countrycd', orderData.country);
      targetWork.dsList.setColumn(0, 'countrynm', orderData.countryNm);
      targetWork.dsList.setColumn(0, 'receivezipcode', orderData.zip);
      targetWork.dsList.setColumn(0, 'receiveaddr1', orderData.addr1);
      targetWork.dsList.setColumn(0, 'receiveaddr2', orderData.addr2);
      targetWork.dsList.setColumn(0, 'receiveaddr3', orderData.addr3);
      targetWork.dsList.setColumn(0, 'receivename', orderData.name);
      targetWork.dsList.setColumn(0, 'receivetelno', orderData.tel);
      targetWork.dsList.setColumn(0, 'receivemail', orderData.email);
      targetWork.dsList.setColumn(0, 'orderno', orderData.orderId);
      targetWork.dsList.setColumn(0, 'premiumcd', '14'); // K-Packet
      targetWork.dsList.setColumn(0, 'em_ee', 'rl');       // K-Packet
      targetWork.dsList.setColumn(0, 'totweight', orderData.weight);
    }

    // 2. 세관신고서(CN22) 주입 (dsCustomReport)
    if (targetWork.dsCustomReport) {
      targetWork.dsCustomReport.clearData();
      const r = targetWork.dsCustomReport.addRow();
      targetWork.dsCustomReport.setColumn(r, 'contents', orderData.item);
      targetWork.dsCustomReport.setColumn(r, 'cnt', orderData.qty);
      targetWork.dsCustomReport.setColumn(r, 'netwght', orderData.weight);
      targetWork.dsCustomReport.setColumn(r, 'prc', orderData.price);
      targetWork.dsCustomReport.setColumn(r, 'hscode', orderData.hsCode);
      targetWork.dsCustomReport.setColumn(r, 'origin', 'KR');
      targetWork.dsCustomReport.setColumn(r, 'EM_gubun', 'Merchandise');
      targetWork.dsCustomReport.setColumn(r, 'currunitcd', 'USD');
    }

    // 3. UI 컴포넌트 강제 갱신
    if (targetWork.resetCtrl) {
      targetWork.resetCtrl();
    }

    alert('✅ [BayFlow] 우체국 개별등록 1초 자동입력 완료!\n\n' +
          '• 수취인명: ' + orderData.name + ' (' + orderData.buyer + ')\n' +
          '• 이메일: ' + orderData.email + '\n' +
          '• 연락처: ' + orderData.tel + '\n' +
          '• 국가/우편번호: 호주 (AU) / ' + orderData.zip + '\n' +
          '• 주소: ' + orderData.addr1 + ' ' + orderData.addr2 + ' ' + orderData.addr3 + '\n' +
          '• 세관신고: ' + orderData.item + ' ($' + orderData.price + ' / ' + orderData.weight + 'g)\n' +
          '• HS CODE: ' + orderData.hsCode + '\n\n' +
          '내용 눈으로 슥 확인하신 뒤 맨 아래 [등록하고 창닫기]를 누르시면 접수정보등록 목록에 저장됩니다!');

  } catch(e) {
    alert('[BayFlow] 자동입력 처리 중 오류: ' + e.message);
  }
})();

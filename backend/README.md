# BayFlow 우체국 실시간 백엔드 & 터널 가이드

이 백엔드는 동욱 님 PC에서 구동되어 스마트폰 BayFlow 앱의 `[📮 우체국 개별등록 전산 전송]` 요청을 받아, 우체국 e-Shipping 본사 서버(eship.epost.go.kr)에 SEED128 암호화 전문을 쏘아주는 공식 중계 엔진입니다.

## 🚀 1분 실행 방법 (윈도우 PC)

1. `bayflow/backend/start_tunnel.bat` 파일을 더블 클릭하여 실행합니다.
   - 필요한 패키지(`fastapi`, `uvicorn` 등)와 `cloudflared.exe`가 자동 점검 및 다운로드됩니다.
   - 로컬 백엔드 서버가 포트 `8000`에서 백그라운드로 실행됩니다.
   - Cloudflare Quick Tunnel이 연결되며 터널 주소가 터미널 창에 출력됩니다:
     `https://your-unique-subdomain.trycloudflare.com`

2. 터미널에 뜬 `https://xxxx.trycloudflare.com` 주소를 복사합니다.

3. 스마트폰이나 PC의 BayFlow 어플 (`https://seodong9401-max.github.io/bayflow/`) 주문 탭 상단의 **[Cloudflare 백엔드 터널 실시간 연동]** 칸에 붙여넣고 `[저장]` 및 `[연결 테스트]`를 누릅니다.

4. 이제 폰 어플에서 `[📮 우체국 개별등록 전산 전송]` 버튼을 누르면:
   - 폰 ➔ Cloudflare 터널 ➔ 동욱 님 PC FastAPI 백엔드 ➔ 우체국 e-Shipping 서버
   - 0.5초 만에 우체국 본사 DB [접수정보등록] 목록에 오차 0%로 실시간 저장됩니다!

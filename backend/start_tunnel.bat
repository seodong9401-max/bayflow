@echo off
chcp 65001 > nul
title BayFlow 우체국 백엔드 & 터널 자동 실행기

echo ========================================================
echo    🚀 BayFlow 우체국 실시간 연동 백엔드 & 터널 실행기
echo ========================================================
echo.

cd /d "%~dp0"

:: 1. 파이썬 라이브러리 확인
echo [1/3] 백엔드 패키지 점검 중...
pip install -r requirements.txt --quiet

:: 2. Cloudflare 터널 프로그램 확인 (없으면 자동 다운로드)
if not exist "cloudflared.exe" (
    echo [2/3] cloudflared.exe 다운로드 중 (약 30MB, 최초 1회만)...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe' -OutFile 'cloudflared.exe'"
) else (
    echo [2/3] cloudflared.exe 확인 완료!
)

:: 3. FastAPI 백엔드 백그라운드 구동
echo [3/3] FastAPI 백엔드 구동 (포트 8000)...
start /b python -m uvicorn main:app --host 0.0.0.0 --port 8000

echo.
echo ========================================================
echo  🌟 Cloudflare 공개 보안 터널을 연결합니다!
echo  잠시 후 아래에 나타나는 [ https://xxxx.trycloudflare.com ] 주소를
echo  BayFlow 어플 상단 '터널 주소' 칸에 복사해 넣으시면 끝납니다.
echo ========================================================
echo.

cloudflared.exe tunnel --url http://localhost:8000
pause

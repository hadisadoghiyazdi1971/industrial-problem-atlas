@echo off
setlocal
cd /d "%~dp0"
echo ============================================================
echo Industrial Problem Atlas - Local Website
echo ============================================================
where py >nul 2>&1
if %errorlevel%==0 (
  start "Industrial Problem Atlas Server" py -3 -m http.server 8000 --bind 127.0.0.1
  goto openweb
)
where python >nul 2>&1
if %errorlevel%==0 (
  start "Industrial Problem Atlas Server" python -m http.server 8000 --bind 127.0.0.1
  goto openweb
)
echo ERROR: Python 3 is required. Install Python, then retry.
pause
exit /b 1
:openweb
timeout /t 2 /nobreak >nul
start "" "http://127.0.0.1:8000/"
echo Browser opened at http://127.0.0.1:8000/
echo To stop the local web server, close its command window.
pause

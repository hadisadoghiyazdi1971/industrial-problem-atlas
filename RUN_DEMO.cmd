@echo off
setlocal
cd /d "%~dp0"
echo ============================================================
echo IPA-001 - SYNTHETIC data only - educational demonstration
echo ============================================================
where py >nul 2>&1
if %errorlevel%==0 (
  py -3 tools\validate_atlas.py && py -3 pilot\synthetic_sensor_demo.py
  goto finished
)
where python >nul 2>&1
if %errorlevel%==0 (
  python tools\validate_atlas.py && python pilot\synthetic_sensor_demo.py
  goto finished
)
echo ERROR: Python 3 is required.
pause
exit /b 1
:finished
if errorlevel 1 (echo DEMO FAILED) else (echo Results folder: pilot\output)
pause

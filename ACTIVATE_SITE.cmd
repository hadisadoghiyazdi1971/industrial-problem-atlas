@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ==================================================
echo Activating the additive KSG briefing links
 echo This only adds a banner to existing pages.
echo Original files are backed up in Documents.
echo ==================================================
py -3 tools\activate_company_briefing.py
if errorlevel 1 python tools\activate_company_briefing.py
echo.
echo Check results and commit via GitHub Desktop.
pause

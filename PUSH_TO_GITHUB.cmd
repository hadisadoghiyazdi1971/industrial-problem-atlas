@echo off
setlocal
cd /d "%~dp0"
set "REMOTE=https://github.com/hadisadoghiyazdi1971/industrial-problem-atlas.git"
echo ============================================================
echo Publish Industrial Problem Atlas to GitHub
 echo Remote: %REMOTE%
echo ============================================================
where git >nul 2>&1
if errorlevel 1 (
  echo ERROR: Git is not installed or not on PATH.
  echo Install Git for Windows or use GitHub Desktop.
  pause
  exit /b 1
)
if not exist "index.html" (
  echo ERROR: Run this script from the extracted project root.
  pause
  exit /b 1
)
if not exist ".git" (
  git init
  if errorlevel 1 goto failure
)
git branch -M main
if errorlevel 1 goto failure
git remote get-url origin >nul 2>&1
if errorlevel 1 (
  git remote add origin "%REMOTE%"
) else (
  echo Existing origin detected. It will be set to the intended repository.
  git remote set-url origin "%REMOTE%"
)
if errorlevel 1 goto failure
git add .
if errorlevel 1 goto failure
git diff --cached --quiet
if errorlevel 1 (
  git commit -m "Launch evidence-driven Industrial Problem Atlas"
  if errorlevel 1 (
    echo If Git asks for a user name or email, configure them and retry.
    goto failure
  )
) else (
  echo Nothing new to commit.
)
git push -u origin main
if errorlevel 1 goto failure
echo.
echo SUCCESS: Files pushed. To publish the website:
echo GitHub repository ^> Settings ^> Pages
echo Deploy from a branch ^> main ^> /(root) ^> Save
echo URL: https://hadisadoghiyazdi1971.github.io/industrial-problem-atlas/
pause
exit /b 0
:failure
echo.
echo FAILED. Your files are still on your computer.
echo Check the message above. No force push was attempted.
pause
exit /b 1

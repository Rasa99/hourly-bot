@echo off
setlocal
title Send the bot to GitHub - FIRST TIME ONLY

rem Uploads this folder to your GitHub repository so it can run hourly on
rem GitHub's computers, free, with your PC off.
rem
rem Read PUT-IT-ONLINE.md first - you need to create the (public, empty)
rem repository yourself before running this.
rem
rem ##########################################################################
rem  FIRST UPLOAD ONLY. To update a bot that is ALREADY running, use
rem  update-cloud-bot.bat instead.
rem
rem  This script ends with `git push --force`, which is right for filling an
rem  empty repository and destructive afterwards: the cloud bot commits to
rem  that same repository every hour, and its trade database, status page and
rem  logs all live there. Forcing this folder over the top replaces the bot's
rem  history with whatever is on this PC, and every trade closed since the
rem  last sync is gone - the bot then restarts from a stale database and
rem  re-opens positions it had already closed.
rem
rem  The check below refuses to run once the repository has real history.
rem ##########################################################################

cd /d "%~dp0"

where git >nul 2>&1
if errorlevel 1 (
  echo.
  echo   Git is not installed.
  echo   Get it from https://git-scm.com/download/win then run this again.
  echo.
  pause
  exit /b 1
)

echo.
echo  ================================================================
echo   SEND THE BOT TO GITHUB
echo  ================================================================
echo.
echo   You need an EMPTY, PUBLIC repository already created at
echo   https://github.com/new  - see PUT-IT-ONLINE.md
echo.

rem A bot that has been running has committed to this repository many times,
rem and those commits are its memory. If they are here, this is not a first
rem upload and the force push below would delete them.
if exist ".git" (
  for /f %%C in ('git log --oneline --author^=hourly-bot 2^>nul ^| find /c /v ""') do set "BOTCOMMITS=%%C"
)
if not "%BOTCOMMITS%"=="" if not "%BOTCOMMITS%"=="0" (
  echo  ================================================================
  echo   STOPPED - THIS BOT IS ALREADY ONLINE
  echo  ================================================================
  echo.
  echo   This repository already contains %BOTCOMMITS% commits made by the
  echo   running bot. They hold its trade database and its history.
  echo.
  echo   This script force-pushes, which would erase them.
  echo.
  echo   To send a code change to a bot that is already running, use:
  echo.
  echo       update-cloud-bot.bat
  echo.
  echo   Nothing has been changed or uploaded.
  echo.
  pause
  exit /b 1
)

set "REPO="
set /p REPO="  Paste your repository address and press Enter: "
if "%REPO%"=="" (
  echo.
  echo   Nothing entered - stopping.
  pause
  exit /b 1
)

echo.
echo   Preparing files...

if not exist ".git" (
  git init -b main
) else (
  git checkout -B main
)

rem Git refuses to commit without a name and email, and on a fresh Windows
rem install neither is set. It then fails with "unable to auto-detect email
rem address", makes no commit, and the push dies with the confusing
rem "src refspec main does not match any" - because there is nothing to push.
rem Set it here, per-repository, so nothing on the rest of the machine changes.
rem
rem Pull the username out of the repo address, and use GitHub's noreply email
rem so a real address never appears in a public commit history.
rem tokens=3 not 4: "for /f" collapses repeated delimiters, so the "//" in
rem https:// counts once and the parts are [https:][github.com][USER][repo.git].
rem Verified against https://github.com/Rasa99/hourly-bot.git -> "Rasa99".
set "GHUSER="
for /f "tokens=3 delims=/" %%U in ("%REPO%") do set "GHUSER=%%U"
if "%GHUSER%"=="" set "GHUSER=hourly-bot-owner"

git config user.name "%GHUSER%"
git config user.email "%GHUSER%@users.noreply.github.com"
echo   Signing commits as: %GHUSER% ^<%GHUSER%@users.noreply.github.com^>

rem Ignore local noise but NOT the bot's memory file - that has to travel.
> .gitignore echo __pycache__/
>> .gitignore echo *.pyc
>> .gitignore echo user_data/backtest_results/
>> .gitignore echo user_data/data/
>> .gitignore echo *.sqlite-wal
>> .gitignore echo *.sqlite-shm
rem desktop.ini is a hidden Google Drive marker that sits in every synced
rem folder. Harmless locally, but it would be published in a public repo.
>> .gitignore echo desktop.ini
>> .gitignore echo Thumbs.db
>> .gitignore echo .DS_Store

git add -A
git commit -m "hourly bot: strategy, config and schedule"

rem Stop here if there is still no commit, rather than letting the push fail
rem with the unhelpful "src refspec main does not match any".
git rev-parse --verify HEAD >nul 2>&1
if errorlevel 1 (
  echo.
  echo   Could not create a commit, so there is nothing to upload.
  echo   Scroll up - the reason is in the git message just above.
  echo.
  pause
  exit /b 1
)

git remote remove origin 2>nul
git remote add origin "%REPO%"

echo.
echo   Uploading... a browser may open asking you to sign in to GitHub.
echo.
git push -u origin main --force

if errorlevel 1 (
  echo.
  echo  ----------------------------------------------------------------
  echo   Upload failed. The usual causes:
  echo     - the address was mistyped
  echo     - the repository was not created yet
  echo     - sign-in was cancelled
  echo   Fix and run this again. Nothing was damaged.
  echo  ----------------------------------------------------------------
  echo.
  pause
  exit /b 1
)

echo.
echo  ================================================================
echo   UPLOADED.
echo.
echo   Now finish it on GitHub:
echo     1. Open your repository
echo     2. Click the ACTIONS tab
echo     3. Enable workflows if it asks
echo     4. Click "hourly-bot" then "Run workflow" to start it now
echo.
echo   After that it runs by itself every hour. Your PC can be off.
echo  ================================================================
echo.
pause

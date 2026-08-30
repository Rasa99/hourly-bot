@echo off
setlocal
title Update the cloud bot (safe)

rem ============================================================================
rem  SEND A CODE CHANGE TO THE RUNNING CLOUD BOT, WITHOUT DESTROYING ITS MEMORY
rem ============================================================================
rem
rem  Use THIS to update a bot that is already online.
rem  Use push-to-github.bat ONLY for the very first upload.
rem
rem  WHY THEY ARE DIFFERENT, AND WHY IT MATTERS
rem
rem  push-to-github.bat finishes with `git push --force`. That is correct for a
rem  first upload into an empty repository and DESTRUCTIVE for anything after
rem  it, because the cloud bot commits to that same repository every hour - the
rem  trade database, the status page, the charts and the logs all live there.
rem  A force push from this PC replaces the bot's history with whatever this
rem  folder happens to hold, and every closed trade recorded since the last
rem  time this folder was synced is gone. The bot then restarts from an old
rem  database and re-opens positions it had already closed.
rem
rem  This script pulls the bot's work down first, replays your local changes on
rem  top, and pushes without --force. If anything conflicts it stops and says
rem  so rather than choosing a winner.
rem ============================================================================

cd /d "%~dp0"

where git >nul 2>&1
if errorlevel 1 (
  echo.
  echo   Git is not installed. Get it from https://git-scm.com/download/win
  echo.
  pause
  exit /b 1
)

if not exist ".git" (
  echo.
  echo   This folder is not connected to GitHub yet.
  echo   Run push-to-github.bat first - that is the one-time setup.
  echo.
  pause
  exit /b 1
)

echo.
echo  ================================================================
echo   UPDATE THE CLOUD BOT
echo  ================================================================
echo.
echo   Local changes about to be sent:
echo.
git status --short
echo.

rem The bot commits as "hourly-bot"; commit as the repo owner so the history
rem stays readable. Reuse whatever identity is already configured here.
git config user.name  >nul 2>&1 || git config user.name "hourly-bot-owner"
git config user.email >nul 2>&1 || git config user.email "hourly-bot-owner@users.noreply.github.com"

echo   Saving your changes...
git add -A
git diff --cached --quiet
if not errorlevel 1 (
  echo   Nothing has changed locally - only fetching the bot's latest work.
) else (
  git commit -q -m "update from PC: strategy and tooling"
  if errorlevel 1 (
    echo.
    echo   Could not create a commit. Scroll up for the reason.
    echo.
    pause
    exit /b 1
  )
)

echo   Fetching what the bot has done since you last synced...
git pull --rebase origin main
if errorlevel 1 (
  echo.
  echo  ----------------------------------------------------------------
  echo   The pull did not complete cleanly, so NOTHING has been sent.
  echo.
  echo   This usually means the same file was changed here and by the
  echo   bot. Nothing is lost - your work is committed locally. To back
  echo   all the way out and try again:
  echo.
  echo       git rebase --abort
  echo.
  echo  ----------------------------------------------------------------
  echo.
  pause
  exit /b 1
)

echo   Uploading...
git push origin main
if errorlevel 1 (
  echo.
  echo   Upload failed - and nothing was forced, so the bot's history is
  echo   untouched. Check the message above, then run this again.
  echo.
  pause
  exit /b 1
)

echo.
echo  ================================================================
echo   SENT. The next hourly cycle picks it up automatically.
echo.
echo   To apply it immediately instead: open the repository on GitHub,
echo   ACTIONS tab, "hourly-bot", "Run workflow".
echo  ================================================================
echo.
pause

@echo off
rem Finds your Telegram chat id and prints it ready to paste into GitHub.
rem Double-click this.
rem
rem -ExecutionPolicy Bypass is required on these machines, otherwise Windows
rem refuses to run the script at all.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0get-telegram-id.ps1"

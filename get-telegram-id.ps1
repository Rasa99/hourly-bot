<#
    Finds your Telegram chat id and prints both values ready to paste into
    GitHub as repository secrets.

    It asks YOUR bot who messaged it, rather than relying on @userinfobot -
    those third-party "get my id" bots come and go, and when one stops replying
    you are stuck. Your own bot always knows.

    Nothing is saved anywhere by this script. It only reads and prints.
#>

$ErrorActionPreference = 'Stop'

Write-Host ""
Write-Host "  ================================================================" -ForegroundColor Cyan
Write-Host "   GET YOUR TELEGRAM DETAILS FOR GITHUB" -ForegroundColor Cyan
Write-Host "  ================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  STEP 1 - create a bot (skip if you already have the token)"
Write-Host "     In Telegram, search for   @BotFather"
Write-Host "     Send:  /newbot"
Write-Host "     Pick any name, then a username ending in 'bot'."
Write-Host "     It replies with a long token like  8123456789:AAF..."
Write-Host ""

$token = (Read-Host "  Paste the TOKEN here").Trim()
if (-not $token) { Write-Host "  Nothing entered." -ForegroundColor Red; Read-Host "  Press Enter"; exit 1 }

Write-Host ""
Write-Host "  Checking the token with Telegram..."
try {
    $me = Invoke-RestMethod -Uri "https://api.telegram.org/bot$token/getMe" -TimeoutSec 25
} catch {
    Write-Host "  Could not reach Telegram, or the token is wrong." -ForegroundColor Red
    Write-Host "  ($($_.Exception.Message))"
    Read-Host "  Press Enter"; exit 1
}
if (-not $me.ok) { Write-Host "  Telegram rejected that token." -ForegroundColor Red; Read-Host "  Press Enter"; exit 1 }

$botName = $me.result.username
Write-Host "  Token is valid. Your bot is  @$botName" -ForegroundColor Green

Write-Host ""
Write-Host "  STEP 2 - say hello to it"
Write-Host "     Open Telegram, search for   @$botName"
Write-Host "     Send it any message (just 'hi')."
Write-Host ""
Write-Host "  Waiting..." -NoNewline

$chatId = $null; $who = $null
for ($i = 0; $i -lt 60; $i++) {
    try {
        $u = Invoke-RestMethod -Uri "https://api.telegram.org/bot$token/getUpdates" -TimeoutSec 20
        if ($u.ok -and $u.result.Count -gt 0) {
            $last = $u.result[-1]
            $msg = if ($last.message) { $last.message } else { $last.edited_message }
            if ($msg -and $msg.chat -and $msg.chat.id) {
                $chatId = [string]$msg.chat.id
                $who = $msg.chat.first_name
                break
            }
        }
    } catch { }
    Write-Host "." -NoNewline
    Start-Sleep -Seconds 3
}
Write-Host ""

if (-not $chatId) {
    Write-Host ""
    Write-Host "  Did not see a message. Make sure you sent one to @$botName," -ForegroundColor Yellow
    Write-Host "  then run this again." -ForegroundColor Yellow
    Read-Host "  Press Enter"; exit 1
}

Write-Host "  Found you: $who" -ForegroundColor Green
Write-Host ""
Write-Host "  ================================================================" -ForegroundColor Cyan
Write-Host "   PASTE THESE INTO GITHUB" -ForegroundColor Cyan
Write-Host "  ================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "   Go to your repository, then:"
Write-Host "     Settings  ->  Secrets and variables  ->  Actions"
Write-Host "     -> New repository secret     (do this twice)"
Write-Host ""
Write-Host "   Secret 1" -ForegroundColor Yellow
Write-Host "     Name:   TELEGRAM_TOKEN"
Write-Host "     Value:  $token" -ForegroundColor White
Write-Host ""
Write-Host "   Secret 2" -ForegroundColor Yellow
Write-Host "     Name:   TELEGRAM_CHAT_ID"
Write-Host "     Value:  $chatId" -ForegroundColor White
Write-Host ""
Write-Host "  ================================================================" -ForegroundColor Cyan
Write-Host ""

try {
    Invoke-RestMethod -Uri "https://api.telegram.org/bot$token/sendMessage" -Method Post -TimeoutSec 25 -Body @{
        chat_id = $chatId
        text    = "Your chat id is $chatId - paste it into GitHub as TELEGRAM_CHAT_ID."
    } | Out-Null
    Write-Host "  I also sent it to you on Telegram, so you can copy it there." -ForegroundColor Green
} catch { }

Write-Host ""
Read-Host "  Press Enter to close"

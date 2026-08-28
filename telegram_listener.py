"""
Answers Telegram commands for as long as the job is alive.

The problem this solves: freqtrade's own Telegram only exists while freqtrade
is running, which is a few minutes per hour. Send it /status at the wrong
moment and nothing answers, because nothing is listening.

This runs alongside the hourly loop for the job's whole 5+ hour life, polling
Telegram every few seconds. So the bot answers essentially whenever a job is
running - which, with the long-loop design, is most of the time.

It only ever READS the database, the market scan and the position file. It
cannot open, close or change a trade, so a stray message can do no harm.

WHY THE BUTTONS USED TO LOOK RANDOM
-----------------------------------
This script answered /status and /closest perfectly well, but it never told
Telegram those commands existed. Telegram's "/" menu is not built from the
messages a bot replies to - it is served from a list the bot must register
itself with setMyCommands. Registering nothing means Telegram falls back to
whatever it has cached for that token, which is why the suggestions looked
arbitrary and tapping them did nothing useful.

Two fixes, and they are separate things:
  setMyCommands  - populates the "/" menu with the real command list
  reply keyboard - a persistent grid of tappable buttons above the text box,
                   so nothing has to be typed on a phone at all

The buttons send plain text ("Status"), not "/status", so every label is mapped
back to its command below. That mapping is why tapping a button and typing the
command reach the same handler.

Commands: /status /pnl /chart /closest /trades /help
"""

import json
import os
import sqlite3
import sys
import time
import urllib.parse
import urllib.request
import uuid

DB = "user_data/live_cloud.sqlite"
SCAN = "market_scan.json"
POSITIONS = "positions.json"
START_BALANCE = 20.0

TOKEN = os.environ.get("TG_TOKEN", "")
CHAT = str(os.environ.get("TG_CHAT", ""))
RUN_SECONDS = int(os.environ.get("LISTEN_SECONDS", "19800"))   # 5h30m


# ------------------------------------------------------------------ api
def api(method, params=None, timeout=40):
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"telegram api {method} failed: {type(e).__name__}", flush=True)
        return None


def send_photo(path, caption=""):
    """
    sendPhoto needs multipart/form-data, which urllib will not build for us.
    Done by hand here rather than adding `requests` for one call.
    """
    if not os.path.exists(path):
        return False
    boundary = "----ftbot" + uuid.uuid4().hex
    body = b""
    for key, val in (("chat_id", CHAT), ("caption", caption)):
        body += (f"--{boundary}\r\n"
                 f'Content-Disposition: form-data; name="{key}"\r\n\r\n'
                 f"{val}\r\n").encode()
    body += (f"--{boundary}\r\n"
             f'Content-Disposition: form-data; name="photo"; '
             f'filename="{os.path.basename(path)}"\r\n'
             f"Content-Type: image/png\r\n\r\n").encode()
    body += open(path, "rb").read() + b"\r\n"
    body += f"--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode()).get("ok", False)
    except Exception as e:
        print(f"sendPhoto failed: {type(e).__name__}", flush=True)
        return False


# ------------------------------------------------ buttons and the "/" menu
KEYBOARD = json.dumps({
    "keyboard": [
        [{"text": "Status"}, {"text": "Charts"}],
        [{"text": "P&L"}, {"text": "Closest"}],
        [{"text": "Trades"}, {"text": "Help"}],
    ],
    "resize_keyboard": True,
    "is_persistent": True,
})

MENU = [
    ("status", "Balance, equity and every open trade"),
    ("pnl", "Live profit on open trades, with prices"),
    ("chart", "A price chart per open trade"),
    ("closest", "Which coin is nearest to triggering, and what blocks it"),
    ("trades", "Recent finished trades"),
    ("help", "What each command does"),
]


def register_menu():
    """Populate the "/" menu. Without this it shows stale or empty entries."""
    ok = api("setMyCommands", {"commands": json.dumps(
        [{"command": c, "description": d} for c, d in MENU])})
    print(f"command menu registered: {bool(ok and ok.get('ok'))}", flush=True)


def send(text, keyboard=False):
    p = {"chat_id": CHAT, "text": text}
    if keyboard:
        p["reply_markup"] = KEYBOARD
    api("sendMessage", p)


# ----------------------------------------------------------------- data
def read_trades():
    if not os.path.exists(DB):
        return [], []
    try:
        c = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
        c.row_factory = sqlite3.Row
        rows = c.execute(
            "select pair,is_open,is_short,open_rate,close_profit_abs,"
            "exit_reason,leverage,stake_amount from trades order by id desc"
        ).fetchall()
        c.close()
    except Exception:
        return [], []
    return [r for r in rows if r["is_open"]], [r for r in rows if not r["is_open"]]


def read_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception:
        return default


# ------------------------------------------------------------- commands
def cmd_status():
    open_, closed = read_trades()
    pos = read_json(POSITIONS, {})
    live = pos.get("positions", [])
    bal = START_BALANCE + sum((r["close_profit_abs"] or 0) for r in closed)
    unreal = pos.get("total_pnl", 0.0)
    equity = pos.get("equity", bal)
    wins = sum(1 for r in closed if (r["close_profit_abs"] or 0) > 0)

    mark = "\U0001F7E2" if equity >= START_BALANCE else "\U0001F534"
    out = [f"{mark} Equity ${equity:.4f}  ({(equity/START_BALANCE-1)*100:+.2f}%)",
           f"Settled ${bal:.4f}   Unrealised {unreal:+.4f}",
           f"Open: {len(open_)}   Finished: {len(closed)}"]
    if closed:
        out.append(f"Wins: {wins}/{len(closed)}  ({wins/len(closed)*100:.0f}%)")

    if live:
        out.append("")
        for p in live:
            dot = "\U0001F7E2" if p["pnl"] >= 0 else "\U0001F534"
            out.append(f"{dot} {p['side']} {p['coin']}  {p['pnl']:+.4f} "
                       f"({p['pnl_pct_margin']:+.1f}%)")
            out.append(f"    {p['entry']} -> {p['now']}  ({p['move_pct']:+.2f}%)")
        ls = len([p for p in live if not p["is_short"]])
        ss = len([p for p in live if p["is_short"]])
        if ls == 0 or ss == 0:
            out.append("")
            out.append(f"⚠ All {len(live)} are "
                       f"{'short' if ss else 'long'} - one bet, "
                       f"{len(live)} places.")
    elif open_:
        out.append("")
        out.append("Live prices unavailable - showing entries only.")
        for r in open_[:8]:
            side = "SHORT" if r["is_short"] else "LONG"
            out.append(f"  {side} {r['pair'].split('/')[0]} @ {r['open_rate']}")
    else:
        out.append("")
        out.append("Nothing open right now.")
    return "\n".join(out)


def cmd_pnl():
    pos = read_json(POSITIONS, {})
    live = pos.get("positions", [])
    if not live:
        return "Nothing open, so nothing to profit or lose on right now."
    out = [f"Unrealised: {pos.get('total_pnl', 0):+.4f} USDT", ""]
    for p in live:
        dot = "\U0001F7E2" if p["pnl"] >= 0 else "\U0001F534"
        room = f"{p['to_stop_pct']:.2f}%" if p.get("to_stop_pct") else "?"
        out.append(f"{dot} {p['side']} {p['coin']}")
        out.append(f"    entry {p['entry']}  ->  now {p['now']}")
        out.append(f"    moved {p['move_pct']:+.2f}%   P&L {p['pnl']:+.4f} "
                   f"({p['pnl_pct_margin']:+.1f}% on margin)")
        out.append(f"    {room} of room before the stop")
    out.append("")
    out.append(f"Gross exposure {pos.get('gross_pct_equity', 0):.0f}% of equity")
    return "\n".join(out)


def _caption(p):
    room = (f"  ·  {p['to_stop_pct']:.2f}% to the stop"
            if p.get("to_stop_pct") else "")
    return (f"{p['coin']} {p['side']}  ·  entry {p['entry']} → now {p['now']} "
            f"({p['move_pct']:+.2f}%)\n"
            f"P&L {p['pnl']:+.4f} USDT ({p['pnl_pct_margin']:+.1f}% on "
            f"margin){room}")


def push_charts():
    """
    Send one chart per open position. Shared by the /chart command and by the
    hourly workflow (`telegram_listener.py sendcharts`), so a chart looks the
    same whether it was asked for or arrived on its own.
    """
    pos = read_json(POSITIONS, {})
    live = pos.get("positions", [])
    sent = 0
    for p in live:
        if send_photo(p.get("chart") or f"pos-{p['coin']}.png", _caption(p)):
            sent += 1
    return len(live), sent


def cmd_chart():
    """Replies with photos rather than text, so it returns None."""
    total, sent = push_charts()
    if not total:
        send("No open trades, so there is nothing to chart.")
    elif not sent:
        send("Charts are not built yet - they appear at the top of each hour.")
    return None


def cmd_closest():
    scan = read_json(SCAN, [])
    if not scan:
        return "No market scan yet - it is built at the top of each hour."
    ready = [r for r in scan if r["ready"]]
    out = [f"Closest to entry ({len(ready)} ready now):"]
    for r in scan[:8]:
        note = "READY" if r["ready"] else (r["blockers"][0] if r["blockers"] else "")
        out.append(f"  {r['coin']} {r['side']} {r['gap']:.2f}% - {note}")
    out.append("")
    out.append("A trade needs all four: breakout, trend, momentum, volume.")
    return "\n".join(out)


def cmd_trades():
    _, closed = read_trades()
    if not closed:
        return "No finished trades yet."
    out = ["Last finished trades:"]
    for r in closed[:10]:
        side = "SHORT" if r["is_short"] else "LONG"
        p = r["close_profit_abs"] or 0
        out.append(f"  {'+' if p > 0 else ''}{p:.4f}  {side} "
                   f"{r['pair'].split('/')[0]} ({r['exit_reason']})")
    return "\n".join(out)


HELP = ("What I can show you:\n\n"
        "Status  - equity, and every open trade with its live profit\n"
        "Charts  - a price chart per open trade: entry, stop, where it is now\n"
        "P&L     - live profit, and how much room is left before each stop\n"
        "Closest - which coin is nearest to triggering, and what blocks it\n"
        "Trades  - recent finished trades\n\n"
        "Use the buttons below, or type the / command.\n\n"
        "I answer while the hourly job is running (most of the time). If I go "
        "quiet, the job is between runs - the hourly summary still arrives.")

HANDLERS = {
    "status": cmd_status,
    "balance": cmd_status,
    "pnl": cmd_pnl,
    "pl": cmd_pnl,            # the "P&L" button label, punctuation stripped
    "profit": cmd_pnl,
    "chart": cmd_chart,
    "charts": cmd_chart,
    "closest": cmd_closest,
    "entry": cmd_closest,
    "trades": cmd_trades,
    "help": lambda: HELP,
}


def resolve(text):
    """
    Map whatever arrived to a handler.

    Three different shapes reach this: buttons send their label as plain text
    ("Charts"), the "/" menu sends "/chart", and phones append "@botname".

    Every word is tried, and each is stripped to letters and digits first. That
    second part is not cosmetic - the "P&L" button silently matched nothing
    until it was added, because "p&l" is not a key and never could be. Stripping
    punctuation means a label can be decorated (an emoji, an ampersand, a
    colon) without quietly becoming a dead button.
    """
    t = (text or "").strip().lower().split("@")[0]
    if not t:
        return None
    for raw in t.lstrip("/").split():
        word = "".join(ch for ch in raw if ch.isalnum())
        if word in HANDLERS:
            return HANDLERS[word]
        if word == "start":
            return lambda: "Ready.\n\n" + HELP
    return None


# ----------------------------------------------------------------- main
def main() -> int:
    if not TOKEN or not CHAT:
        print("no telegram secrets - listener not starting")
        return 0

    register_menu()

    # Skip anything already queued, so restarting does not replay old messages.
    offset = 0
    first = api("getUpdates", {"timeout": 0})
    if first and first.get("ok") and first["result"]:
        offset = first["result"][-1]["update_id"] + 1

    deadline = time.time() + RUN_SECONDS
    print(f"telegram listener up for {RUN_SECONDS}s", flush=True)

    while time.time() < deadline:
        upd = api("getUpdates", {"timeout": 25, "offset": offset})
        if not upd or not upd.get("ok"):
            time.sleep(5)
            continue

        for u in upd["result"]:
            offset = u["update_id"] + 1
            msg = u.get("message") or u.get("edited_message")
            if not msg:
                continue
            # Only obey the configured chat. Anyone else is ignored entirely.
            if str(msg.get("chat", {}).get("id")) != CHAT:
                continue

            text = msg.get("text") or ""
            handler = resolve(text)
            if handler:
                try:
                    reply = handler()
                    # cmd_chart sends its own photos and returns None.
                    if reply:
                        send(reply, keyboard=True)
                except Exception as e:
                    send(f"Could not read that right now ({type(e).__name__}).")
            elif text.startswith("/"):
                send("I do not know that one.\n\n" + HELP, keyboard=True)

    print("listener finished", flush=True)
    return 0


if __name__ == "__main__":
    # `sendcharts` is a one-shot used by the hourly workflow: push the current
    # position charts and exit. It lives here rather than in bot_tools.py
    # because this file already owns the multipart upload and the token.
    if len(sys.argv) > 1 and sys.argv[1] == "sendcharts":
        if not TOKEN or not CHAT:
            print("no telegram secrets - charts not sent")
            sys.exit(0)
        total, sent = push_charts()
        print(f"charts sent: {sent}/{total}")
        sys.exit(0)
    sys.exit(main())

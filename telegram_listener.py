"""
Answers Telegram commands for as long as the job is alive.

The problem this solves: freqtrade's own Telegram only exists while freqtrade
is running, which is a few minutes per hour. Send it /status at the wrong
moment and nothing answers, because nothing is listening.

This runs alongside the hourly loop for the job's whole 5+ hour life, polling
Telegram every few seconds. So the bot answers essentially whenever a job is
running - which, with the long-loop design, is most of the time.

It only ever READS the database and the market scan. It cannot open, close or
change a trade, so a stray message can do no harm.

Commands: /status /closest /balance /trades /help
"""

import json
import os
import sqlite3
import sys
import time
import urllib.parse
import urllib.request

DB = "user_data/live_cloud.sqlite"
SCAN = "market_scan.json"
START_BALANCE = 20.0

TOKEN = os.environ.get("TG_TOKEN", "")
CHAT = str(os.environ.get("TG_CHAT", ""))
RUN_SECONDS = int(os.environ.get("LISTEN_SECONDS", "19800"))   # 5h30m


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


def send(text):
    api("sendMessage", {"chat_id": CHAT, "text": text})


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


def read_scan():
    if not os.path.exists(SCAN):
        return []
    try:
        return json.load(open(SCAN, encoding="utf-8"))
    except Exception:
        return []


def cmd_status():
    open_, closed = read_trades()
    bal = START_BALANCE + sum((r["close_profit_abs"] or 0) for r in closed)
    wins = sum(1 for r in closed if (r["close_profit_abs"] or 0) > 0)
    mark = "\U0001F7E2" if bal >= START_BALANCE else "\U0001F534"
    out = [f"{mark} Balance ${bal:.4f}  ({(bal/START_BALANCE-1)*100:+.2f}%)",
           f"Open: {len(open_)}   Finished: {len(closed)}"]
    if closed:
        out.append(f"Wins: {wins}/{len(closed)}  ({wins/len(closed)*100:.0f}%)")
    for r in open_[:8]:
        side = "SHORT" if r["is_short"] else "LONG"
        out.append(f"  {side} {r['pair'].split('/')[0]} @ {r['open_rate']} "
                   f"({r['leverage']:.0f}x, ${r['stake_amount']:.2f})")
    if not open_:
        out.append("Nothing open right now.")
    return "\n".join(out)


def cmd_closest():
    scan = read_scan()
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


HELP = ("Commands:\n"
        "/status  - balance and open trades\n"
        "/closest - which coin is nearest to triggering, and what is blocking it\n"
        "/trades  - recent finished trades\n"
        "/help    - this list\n\n"
        "I answer while the hourly job is running (most of the time). If I go "
        "quiet, the job is between runs - the hourly summary still arrives.")

HANDLERS = {
    "/status": cmd_status,
    "/balance": cmd_status,
    "/closest": cmd_closest,
    "/entry": cmd_closest,
    "/trades": cmd_trades,
    "/help": lambda: HELP,
    "/start": lambda: "Listening. " + HELP,
}


def main() -> int:
    if not TOKEN or not CHAT:
        print("no telegram secrets - listener not starting")
        return 0

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

            text = (msg.get("text") or "").strip().lower().split("@")[0]
            handler = HANDLERS.get(text.split()[0] if text else "")
            if handler:
                try:
                    send(handler())
                except Exception as e:
                    send(f"Could not read that right now ({type(e).__name__}).")
            elif text.startswith("/"):
                send("Unknown command.\n\n" + HELP)

    print("listener finished", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""
Answers Telegram commands for as long as the job is alive.

The problem this solves: freqtrade's own Telegram only exists while freqtrade
is running, which is a few minutes per hour. Send it /status at the wrong
moment and nothing answers, because nothing is listening.

This runs alongside the hourly loop for the job's whole 5+ hour life, polling
Telegram every few seconds. So the bot answers essentially whenever a job is
running - which, with the long-loop design, is most of the time.

WHAT IT CAN DO TO A TRADE  (changed 2026-08-31 - it used to be read-only)
------------------------------------------------------------------------
It can now CLOSE an open trade, and nothing else. It cannot open one, cannot
change its size, cannot move a stop. Everything else here is still read-only.

Closing goes through freqtrade's own REST API (`POST /api/v1/forceexit`), never
through the database. That distinction is the whole safety story: freqtrade is
holding the position, and writing "closed" into the sqlite file underneath a
running bot would leave the bot's memory and the database disagreeing about
what is open - it would go on managing a stop for a trade that no longer
exists, and overwrite the row again on its next iteration. Through the API,
freqtrade places the exit order itself, updates its own state, and emits the
same notification it would for any other exit.

The API listens on 127.0.0.1 inside the GitHub runner only, and its password is
generated fresh for every job by the workflow. Nothing to leak into a public
repository, nothing to rotate.

Two ways to ask, both landing on the same code path:
  - the Close button, which lists the open trades and closes the one you tap
  - a reaction (double-tap) on a position chart, which closes that position

The reaction path acts IMMEDIATELY, with no confirmation. That is the point of
it - look at the chart, get out. It is also why only ADDING a reaction counts
and taking one off does nothing.

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

Commands: /status /pnl /chart /close /closest /trades /help
"""

import base64
import json
import os
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

SNAPSHOT_DB = "user_data/live_cloud.sqlite"
SCAN = "market_scan.json"
POSITIONS = "positions.json"
START_BALANCE = 20.0

# Which chart message showed which trade, so a reaction can be traced back to
# the position it was aimed at. Telegram's reaction updates carry a message id
# and nothing else - not the caption, not the photo - so without this map there
# is no way to know what was double-tapped.
#
# It lives in user_data/logs/ and the workflow commits it, so a chart sent by
# one job can still be reacted to after the next job takes over. Without that
# it would only work within a single 5-hour run.
CHART_MAP = "user_data/logs/chart_messages.json"
CHART_MAP_KEEP = 60


def db_path():
    """
    Prefer the LIVE database freqtrade is writing to, else the hourly snapshot.

    Resolved per call, not at import. This process starts before the live
    database has been seeded, so deciding once at import would pin it to the
    snapshot for the whole five-hour run and /status would answer with
    hour-old data about trades that opened minutes ago.
    """
    live = os.environ.get("FT_LIVE_DB")
    if live and os.path.exists(live):
        return live
    return SNAPSHOT_DB

TOKEN = os.environ.get("TG_TOKEN", "")
CHAT = str(os.environ.get("TG_CHAT", ""))
RUN_SECONDS = int(os.environ.get("LISTEN_SECONDS", "19800"))   # 5h30m

# freqtrade's local REST API - the only way this file is allowed to change a
# trade. Set by the workflow; absent when running locally, in which case the
# Close button reports that it cannot reach the bot instead of pretending.
FT_API_URL = os.environ.get("FT_API_URL", "http://127.0.0.1:8080").rstrip("/")
FT_API_USER = os.environ.get("FT_API_USER", "")
FT_API_PASS = os.environ.get("FT_API_PASS", "")


# ------------------------------------------------------- freqtrade REST api
def ft_api(path, payload=None, timeout=25):
    """
    Call freqtrade's REST API. Returns (ok, data_or_message).

    Errors are unpacked rather than swallowed: freqtrade answers a refused
    force-exit with a 502 and a JSON `detail` explaining why ("invalid
    argument", "trade not found"), and that sentence is far more useful in
    Telegram than "something went wrong".
    """
    if not FT_API_USER or not FT_API_PASS:
        return False, ("The bot's control channel is not configured, so I "
                       "cannot close trades from here.")

    auth = base64.b64encode(f"{FT_API_USER}:{FT_API_PASS}".encode()).decode()
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        f"{FT_API_URL}/api/v1/{path}", data=data,
        headers={"Authorization": f"Basic {auth}",
                 "Content-Type": "application/json"},
        method="POST" if data is not None else "GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return True, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            detail = json.loads(e.read().decode()).get("detail", "")
        except Exception:
            detail = ""
        print(f"ft api {path} -> HTTP {e.code} {detail}", flush=True)
        if e.code == 401:
            return False, "The bot refused my credentials."
        return False, detail or f"The bot refused that (HTTP {e.code})."
    except Exception as e:
        print(f"ft api {path} failed: {type(e).__name__}", flush=True)
        return False, ("The bot is not answering right now - it restarts "
                       "briefly between cycles. Try again in a moment.")


def force_exit(trade_id):
    """Ask freqtrade to close one trade at market. Returns (ok, message)."""
    return ft_api("forceexit", {"tradeid": str(trade_id),
                                "ordertype": "market"})


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

    Returns the sent message's id (not just True/False) so the caller can
    record which trade this chart belongs to - that mapping is what makes a
    reaction on the photo mean anything.
    """
    if not os.path.exists(path):
        return None
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
            got = json.loads(r.read().decode())
            return (got.get("result") or {}).get("message_id") if got.get("ok") \
                else None
    except Exception as e:
        print(f"sendPhoto failed: {type(e).__name__}", flush=True)
        return None


# ------------------------------------------------ buttons and the "/" menu
KEYBOARD = json.dumps({
    "keyboard": [
        [{"text": "Status"}, {"text": "Charts"}],
        [{"text": "P&L"}, {"text": "Close"}],
        [{"text": "Closest"}, {"text": "Trades"}],
        [{"text": "Help"}],
    ],
    "resize_keyboard": True,
    "is_persistent": True,
})

MENU = [
    ("status", "Balance, equity and every open trade"),
    ("pnl", "Live profit on open trades, with prices"),
    ("chart", "A price chart per open trade"),
    ("close", "Close an open trade yourself, now, at market"),
    ("closest", "Which coin is nearest to triggering, and what blocks it"),
    ("trades", "Recent finished trades"),
    ("help", "What each command does"),
]


# Telegram sends an update type ONLY if it is in this list, and the default
# list leaves out message_reaction entirely - so the double-tap feature does
# not work at all unless it is named here explicitly.
ALLOWED = json.dumps(["message", "edited_message", "callback_query",
                      "message_reaction"])


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
    db = db_path()
    if not os.path.exists(db):
        return [], []
    try:
        c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        c.row_factory = sqlite3.Row
        rows = c.execute(
            "select pair,is_open,is_short,open_rate,close_profit_abs,"
            "exit_reason,leverage,stake_amount from trades order by id desc"
        ).fetchall()
        c.close()
    except Exception:
        return [], []
    return [r for r in rows if r["is_open"]], [r for r in rows if not r["is_open"]]


def open_positions():
    """
    Open trades as plain dicts, with the freqtrade trade id.

    Read from the database rather than positions.json because the id is what
    the API needs and the database is the thing that definitely has it -
    positions.json is rewritten hourly and a chart can outlive it.
    """
    db = db_path()
    if not os.path.exists(db):
        return []
    try:
        c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        c.row_factory = sqlite3.Row
        rows = c.execute(
            "select id,pair,is_short,open_rate,open_date from trades "
            "where is_open=1 order by id"
        ).fetchall()
        c.close()
    except Exception:
        return []
    return [{"id": r["id"], "pair": r["pair"],
             "coin": r["pair"].split("/")[0],
             "side": "SHORT" if r["is_short"] else "LONG",
             "entry": r["open_rate"]} for r in rows]


def live_pnl_by_id():
    """{trade id: position dict} from positions.json, for prices in messages."""
    pos = read_json(POSITIONS, {})
    return {p["id"]: p for p in pos.get("positions", []) if p.get("id")}


# ------------------------------------------------- chart message -> trade map
def _load_chart_map():
    return read_json(CHART_MAP, {})


def remember_chart(message_id, trade_id, coin):
    """Record that this Telegram message is the chart for this trade."""
    if not message_id or not trade_id:
        return
    m = _load_chart_map()
    m[str(message_id)] = {"trade_id": trade_id, "coin": coin,
                          "sent": int(time.time())}
    # Keep it small; only the newest charts are ever reacted to in practice.
    if len(m) > CHART_MAP_KEEP:
        for k in sorted(m, key=lambda k: m[k].get("sent", 0))[:-CHART_MAP_KEEP]:
            m.pop(k, None)
    try:
        os.makedirs(os.path.dirname(CHART_MAP), exist_ok=True)
        tmp = CHART_MAP + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(m, f, indent=1)
        os.replace(tmp, CHART_MAP)      # atomic: two processes write this file
    except Exception as e:
        print(f"could not save chart map: {type(e).__name__}", flush=True)


def trade_for_message(message_id):
    entry = _load_chart_map().get(str(message_id))
    return entry.get("trade_id") if entry else None


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
            f"margin){room}\n"
            f"Double-tap this chart to close the trade.")


# ------------------------------------------------------------- closing out
def cmd_close():
    """List the open trades as buttons. Tapping one closes it."""
    live = open_positions()
    if not live:
        return "Nothing is open, so there is nothing to close."

    prices = live_pnl_by_id()
    rows = []
    for t in live:
        p = prices.get(t["id"])
        if p:
            dot = "\U0001F7E2" if p["pnl"] >= 0 else "\U0001F534"
            label = (f"{dot} {t['side']} {t['coin']}  {p['pnl']:+.4f} "
                     f"({p['pnl_pct_margin']:+.0f}%)")
        else:
            label = f"{t['side']} {t['coin']} @ {t['entry']}"
        rows.append([{"text": label,
                      "callback_data": f"x:{t['id']}"}])

    api("sendMessage", {
        "chat_id": CHAT,
        "text": "Tap a trade to close it now, at market.\n"
                "This cannot be undone - the position is gone once it fills.",
        "reply_markup": json.dumps({"inline_keyboard": rows}),
    })
    return None


def do_close(trade_id, how):
    """
    Close one trade and say what happened. `how` is for the reply wording only.

    The name and price are read BEFORE the call, because once freqtrade has
    closed it the trade is no longer in the open set and the message would
    have nothing to name.
    """
    known = {t["id"]: t for t in open_positions()}
    t = known.get(int(trade_id)) if str(trade_id).isdigit() else None
    if not t:
        return ("That trade is not open any more - it may have closed on its "
                "own stop in the meantime.")

    p = live_pnl_by_id().get(t["id"])
    pnl = f"  P&L was {p['pnl']:+.4f} USDT" if p else ""

    ok, msg = force_exit(t["id"])
    if not ok:
        return f"Could not close {t['side']} {t['coin']}: {msg}"
    return (f"Closing {t['side']} {t['coin']} now, at market ({how}).{pnl}\n"
            f"The fill confirmation follows from the bot itself.")


def push_charts():
    """
    Send one chart per open position. Shared by the /chart command and by the
    hourly workflow (`telegram_listener.py sendcharts`), so a chart looks the
    same whether it was asked for or arrived on its own.
    """
    pos = read_json(POSITIONS, {})
    live = pos.get("positions", [])
    by_pair = {t["pair"]: t["id"] for t in open_positions()}
    sent = 0
    for p in live:
        mid = send_photo(p.get("chart") or f"pos-{p['coin']}.png", _caption(p))
        if mid:
            sent += 1
            # positions.json gained an "id" on 2026-08-31; fall back to the
            # database for charts written by an older build of positions.py.
            remember_chart(mid, p.get("id") or by_pair.get(p.get("pair")),
                           p["coin"])
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
        "Close   - close a trade yourself, now, without waiting for the stop\n"
        "Closest - which coin is nearest to triggering, and what blocks it\n"
        "Trades  - recent finished trades\n\n"
        "Two ways to get out of a trade early:\n"
        "  · tap Close and pick the trade\n"
        "  · double-tap a chart to close that position straight away\n"
        "Both exit at market, immediately, and cannot be undone.\n\n"
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
    # "close" and "closest" both start with "clos" and the buttons send their
    # label as plain text, so these must stay exact-match keys - which resolve()
    # already does. Listed adjacently as a reminder that they are one letter
    # apart and one of them ends positions.
    "close": cmd_close,
    "exit": cmd_close,
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
    # ALLOWED must be passed on every getUpdates call, not just this one -
    # Telegram treats it as per-request, and the default list silently OMITS
    # message_reaction. Leaving it off is exactly why a double-tap would look
    # like it did nothing: the update is never delivered in the first place.
    offset = 0
    first = api("getUpdates", {"timeout": 0, "allowed_updates": ALLOWED})
    if first and first.get("ok") and first["result"]:
        offset = first["result"][-1]["update_id"] + 1

    deadline = time.time() + RUN_SECONDS
    print(f"telegram listener up for {RUN_SECONDS}s", flush=True)

    while time.time() < deadline:
        upd = api("getUpdates", {"timeout": 25, "offset": offset,
                                 "allowed_updates": ALLOWED})
        if not upd or not upd.get("ok"):
            time.sleep(5)
            continue

        for u in upd["result"]:
            offset = u["update_id"] + 1

            # ---- a tapped inline button (the Close list) ------------------
            cb = u.get("callback_query")
            if cb:
                if str((cb.get("message") or {}).get("chat", {})
                       .get("id")) != CHAT:
                    continue
                # Answer first, unconditionally: the button keeps spinning on
                # the phone until this is sent, and a force-exit can take a
                # few seconds.
                api("answerCallbackQuery", {"callback_query_id": cb["id"],
                                            "text": "Closing…"})
                data = cb.get("data") or ""
                if data.startswith("x:"):
                    try:
                        send(do_close(data[2:], "you tapped Close"),
                             keyboard=True)
                    except Exception as e:
                        send(f"Could not close that ({type(e).__name__}).")
                continue

            # ---- a reaction on a chart (double-tap) -----------------------
            react = u.get("message_reaction")
            if react:
                if str(react.get("chat", {}).get("id")) != CHAT:
                    continue
                # Only ADDING a reaction closes a trade. Removing one arrives
                # here too, with an empty new_reaction, and must do nothing -
                # otherwise undoing an accidental tap would close a second
                # position.
                if not react.get("new_reaction"):
                    continue
                trade_id = trade_for_message(react.get("message_id"))
                if trade_id is None:
                    send("I do not know which trade that message was about, "
                         "so I have not closed anything. Ask for Charts again "
                         "and react to a fresh one.")
                    continue
                try:
                    send(do_close(trade_id, "you double-tapped its chart"),
                         keyboard=True)
                except Exception as e:
                    send(f"Could not close that ({type(e).__name__}).")
                continue

            # ---- an ordinary message -------------------------------------
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
                    # cmd_chart and cmd_close send their own messages and
                    # return None.
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

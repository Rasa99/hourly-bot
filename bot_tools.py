"""
Small jobs the hourly workflow needs, as a real file instead of shell heredocs.

Why this exists: the workflow used to embed Python inside bash with `<<'PY'`.
That works at the top level of a YAML `run:` block, and breaks the moment it is
nested inside a loop - YAML strips only the block's base indentation, so the
closing `PY` ends up indented, bash never sees the end of the heredoc, and the
whole step dies with a syntax error before doing anything. That is exactly what
killed run #9.

A file has no indentation rules to get wrong, and can be tested locally.

Usage:
    python bot_tools.py checkpoint    # fold SQLite's side file into the main db
    python bot_tools.py summary       # print the hourly Telegram message
"""

import json
import os
import sqlite3
import sys

DB = "user_data/live_cloud.sqlite"
SCAN = "market_scan.json"
POSITIONS = "positions.json"
SEEN = "user_data/logs/seen_trades.json"
START_BALANCE = 20.0


def checkpoint():
    """Merge the -wal side file in, so the committed database is complete."""
    if not os.path.exists(DB):
        print("no database to checkpoint")
        return
    c = sqlite3.connect(DB)
    c.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    c.close()
    print("database checkpointed")


def summary():
    """One short Telegram message describing where things stand."""
    if not os.path.exists(DB):
        print("Hourly check done. No database yet.")
        return

    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    rows = c.execute(
        "select id,pair,is_open,is_short,close_profit_abs,open_rate,exit_reason "
        "from trades"
    ).fetchall()
    c.close()

    closed = [r for r in rows if not r["is_open"]]
    open_ = [r for r in rows if r["is_open"]]
    balance = START_BALANCE + sum((r["close_profit_abs"] or 0) for r in closed)
    wins = sum(1 for r in closed if (r["close_profit_abs"] or 0) > 0)

    # ---- announce what CHANGED since the last message ----------------
    # freqtrade's own Telegram is switched off (it fought this script for the
    # single getUpdates slot Telegram allows), so trade alerts are produced
    # here by comparing against the ids seen last cycle.
    seen_open, seen_closed = set(), set()
    if os.path.exists(SEEN):
        try:
            prev = json.load(open(SEEN, encoding="utf-8"))
            seen_open = set(prev.get("open", []))
            seen_closed = set(prev.get("closed", []))
        except Exception:
            pass

    now_open = {r["id"] for r in open_}
    now_closed = {r["id"] for r in closed}
    newly_opened = [r for r in open_ if r["id"] not in seen_open and r["id"] not in seen_closed]
    newly_closed = [r for r in closed if r["id"] not in seen_closed]

    try:
        json.dump({"open": sorted(now_open), "closed": sorted(now_closed)},
                  open(SEEN, "w", encoding="utf-8"))
    except Exception:
        pass

    # Live prices for the open trades, if positions.py managed to fetch them.
    # Balance alone counts only CLOSED trades, so with positions open it reads
    # flat while real money is moving - equity is the number worth sending.
    pos = {}
    if os.path.exists(POSITIONS):
        try:
            pos = json.load(open(POSITIONS, encoding="utf-8"))
        except Exception:
            pos = {}
    live = pos.get("positions", [])
    unreal = pos.get("total_pnl", 0.0)
    equity = pos.get("equity", balance)

    mark = "\U0001F7E2" if equity >= START_BALANCE else "\U0001F534"
    out = []

    for r in newly_opened:
        side = "SHORT" if r["is_short"] else "LONG"
        out.append(f"\U0001F535 OPENED {side} {r['pair'].split('/')[0]} @ {r['open_rate']}")
    for r in newly_closed:
        p = r["close_profit_abs"] or 0
        emoji = "\U0001F7E2" if p > 0 else "\U0001F534"
        side = "SHORT" if r["is_short"] else "LONG"
        out.append(f"{emoji} CLOSED {side} {r['pair'].split('/')[0]}  "
                   f"{p:+.4f} USDT ({r['exit_reason']})")
    if out:
        out.append("")

    out += [
        f"{mark} Hourly check done",
        f"Equity: ${equity:.4f}  ({(equity / START_BALANCE - 1) * 100:+.2f}%)",
        f"Settled: ${balance:.4f}   Unrealised: {unreal:+.4f}",
        f"Open: {len(open_)}   Finished: {len(closed)}",
    ]
    if closed:
        out.append(f"Wins: {wins}/{len(closed)}")

    if live:
        for p in live:
            dot = "\U0001F7E2" if p["pnl"] >= 0 else "\U0001F534"
            out.append(f"{dot} {p['side']} {p['coin']}  {p['entry']} -> "
                       f"{p['now']}  {p['pnl']:+.4f} "
                       f"({p['pnl_pct_margin']:+.1f}%)")
    else:
        for r in open_[:5]:
            side = "SHORT" if r["is_short"] else "LONG"
            out.append(f"  {side} {r['pair'].split('/')[0]} @ {r['open_rate']}")

    # ---- closest to entry, so "why has it not traded" is always answered ----
    scan = []
    if os.path.exists(SCAN):
        try:
            scan = json.load(open(SCAN, encoding="utf-8"))
        except Exception:
            scan = []

    if scan:
        ready = [r for r in scan if r["ready"]]
        out.append("")
        out.append(f"Closest to entry  ({len(ready)} ready now):")
        for r in scan[:4]:
            if r["ready"]:
                note = "READY"
            elif r["blockers"]:
                note = r["blockers"][0]
            else:
                note = ""
            out.append(f"  {r['coin']} {r['side']} {r['gap']:.2f}% - {note}")
    elif not open_ and not closed:
        out.append("Nothing has triggered yet - no coin has broken out.")

    print("\n".join(out))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "checkpoint":
        checkpoint()
    elif cmd == "summary":
        summary()
    else:
        print("usage: bot_tools.py [checkpoint|summary]")
        sys.exit(1)

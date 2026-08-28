"""
Turns the bot's database and a live market scan into the repository front page.

The local FreqUI dashboard cannot see this bot - it talks to a bot running on
your PC, and this one lives for a few minutes inside GitHub then disappears.
There is no server to point a dashboard at.

So the bot writes its own status into README.md every hour. GitHub renders
README.md automatically, which makes the repository front page the dashboard:
open it on any phone or computer, no login, no software, never more than an
hour stale.
"""

import json
import os
import sqlite3
import sys

import charts

DB = "user_data/live_cloud.sqlite"
SCAN = "market_scan.json"
POSITIONS = "positions.json"
OUT = "README.md"
START_BALANCE = 20.0


def money(x):
    return f"{x:+.4f}"


def load_scan():
    if not os.path.exists(SCAN):
        return []
    try:
        return json.load(open(SCAN, encoding="utf-8"))
    except Exception:
        return []


def load_positions():
    """Live prices and unrealised P&L, written by positions.py this cycle."""
    if not os.path.exists(POSITIONS):
        return {}
    try:
        return json.load(open(POSITIONS, encoding="utf-8"))
    except Exception:
        return {}


def main() -> int:
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    L = []
    add = L.append

    add("# Hourly Trading Bot")
    add("")
    add(f"**Updated {now}** &nbsp;·&nbsp; refreshes itself every hour")
    add("")
    add("Paper money. $20 simulated, real Gate.io prices, no API keys — it "
        "cannot place a real order.")
    add("")

    rows = []
    if os.path.exists(DB):
        c = sqlite3.connect(DB)
        c.row_factory = sqlite3.Row
        rows = c.execute(
            "select id,pair,is_open,is_short,open_date,close_date,open_rate,"
            "close_rate,close_profit_abs,close_profit,exit_reason,leverage,"
            "stake_amount from trades order by id desc"
        ).fetchall()
        c.close()

    closed = [r for r in rows if not r["is_open"]]
    open_ = [r for r in rows if r["is_open"]]
    realised = sum((r["close_profit_abs"] or 0) for r in closed)
    balance = START_BALANCE + realised
    wins = [r for r in closed if (r["close_profit_abs"] or 0) > 0]
    scan = load_scan()
    pos = load_positions()
    live = pos.get("positions", [])
    unreal = pos.get("total_pnl", 0.0)
    equity = pos.get("equity", balance)

    # ---------------------------------------------------------- headline
    pct = (balance / START_BALANCE - 1) * 100
    epct = (equity / START_BALANCE - 1) * 100
    add("## Money")
    add("")
    add("| | |")
    add("|---|---|")
    # Equity is the honest headline: balance counts only CLOSED trades, so with
    # positions open it can read flat while real money is moving underneath.
    add(f"| **Equity now** | **${equity:.4f}** {'🟢' if epct >= 0 else '🔴'} "
        f"{epct:+.2f}% |")
    add(f"| Settled balance | ${balance:.4f} ({pct:+.2f}%) |")
    if live:
        add(f"| Unrealised (open trades) | {'🟢' if unreal >= 0 else '🔴'} "
            f"{money(unreal)} |")
    add(f"| Started with | $20.0000 |")
    add(f"| Finished trades | {len(closed)} |")
    add(f"| Open now | {len(open_)} |")
    if closed:
        add(f"| Win rate | {len(wins)/len(closed)*100:.0f}% ({len(wins)}/{len(closed)}) |")
    add("")

    try:
        charts.equity(closed, START_BALANCE)
        add("![balance](chart-equity.svg)")
        add("")
    except Exception as e:
        print(f"equity chart skipped: {e}")

    # ---------------------------------------------------------- open now
    add("## Open right now")
    add("")
    if live:
        add("| Coin | Direction | Entry | Price now | Moved | P&L | on margin | "
            "Room to stop |")
        add("|---|---|---|---|---|---|---|---|")
        for p in live:
            side = "SHORT 🔻" if p["is_short"] else "LONG 🔺"
            dot = "🟢" if p["pnl"] >= 0 else "🔴"
            room = f"{p['to_stop_pct']:.2f}%" if p.get("to_stop_pct") else "—"
            add(f"| **{p['coin']}** | {side} | {p['entry']} | {p['now']} | "
                f"{p['move_pct']:+.2f}% | {dot} {money(p['pnl'])} | "
                f"{p['pnl_pct_margin']:+.1f}% | {room} |")
        add(f"| | | | | **total** | **{money(unreal)}** | | |")
        add("")

        # --- what the position set actually is, as one sentence ----------
        # Three shorts is not three bets, it is one bet placed three times.
        # That concentration is invisible in a per-row table, so state it.
        ls = len([p for p in live if not p["is_short"]])
        ss = len([p for p in live if p["is_short"]])
        gross = pos.get("gross_pct_equity", 0)
        if live and (ls == 0 or ss == 0):
            way = "short" if ss else "long"
            add(f"> ⚠️ **All {len(live)} positions are {way}.** That is one bet "
                f"on the same market direction, placed {len(live)} times — "
                f"these coins move together, so they will win together and "
                f"lose together. Gross exposure is **{gross:.0f}% of equity**.")
        else:
            add(f"> {ls} long / {ss} short · gross exposure "
                f"**{gross:.0f}% of equity**.")
        add("")

        # --- one chart per position --------------------------------------
        for p in live:
            if p.get("chart") and os.path.exists(p["chart"]):
                add(f"![{p['coin']}]({p['chart']})")
                add("")
    elif open_:
        # positions.py could not reach the exchange this cycle - still show
        # what is open rather than claiming there is nothing.
        add("*Live prices unavailable this cycle — entries only.*")
        add("")
        add("| Coin | Direction | Entry | Leverage | Money in |")
        add("|---|---|---|---|---|")
        for r in open_:
            side = "SHORT 🔻" if r["is_short"] else "LONG 🔺"
            add(f"| {r['pair'].split('/')[0]} | {side} | {r['open_rate']} | "
                f"{r['leverage']:.1f}x | ${r['stake_amount']:.3f} |")
    else:
        add("Nothing open.")
    add("")

    # ---------------------------------------------------------- closest
    add("## What it is waiting for")
    add("")
    if scan:
        ready = [r for r in scan if r["ready"]]
        add(f"**{len(ready)} coin(s) ready to fire right now.** "
            f"Scanned {len(scan)} coins.")
        add("")
        try:
            charts.closest(scan)
            add("![closest to entry](chart-closest.svg)")
            add("")
            charts.blockers(scan)
            add("![what is blocking entries](chart-blockers.svg)")
            add("")
        except Exception as e:
            print(f"scan charts skipped: {e}")

        add("| Coin | Would be | Needs | Status |")
        add("|---|---|---|---|")
        for r in scan[:10]:
            status = "**READY**" if r["ready"] else "; ".join(r["blockers"][:2])
            add(f"| {r['coin']} | {r['side']} | {r['gap']:.2f}% | {status} |")
        add("")
        add("A trade needs **all four** of: price breaking its 3-day range, the "
            "trend filter agreeing, enough momentum (ADX over 20), and "
            "above-average volume. A coin at 0.00% that still has not traded is "
            "being held back by one of the other three — the table says which.")
    else:
        add("No market scan available this cycle.")
    add("")

    # ---------------------------------------------------------- market
    if scan:
        try:
            charts.market_mood(scan)
            add("![market backdrop](chart-mood.svg)")
            add("")
        except Exception as e:
            print(f"mood chart skipped: {e}")

    # ---------------------------------------------------------- results
    add("## Results")
    add("")
    try:
        charts.winloss(closed)
        add("![wins vs losses](chart-winloss.svg)")
        add("")
    except Exception as e:
        print(f"winloss chart skipped: {e}")

    add("### Last 15 finished trades")
    add("")
    if closed:
        add("| Coin | Direction | Result | Why it closed | When |")
        add("|---|---|---|---|---|")
        for r in closed[:15]:
            side = "SHORT" if r["is_short"] else "LONG"
            p = r["close_profit_abs"] or 0
            when = str(r["close_date"])[:16] if r["close_date"] else ""
            add(f"| {r['pair'].split('/')[0]} | {side} | {'🟢' if p > 0 else '🔴'} "
                f"{money(p)} ({(r['close_profit'] or 0)*100:+.1f}%) | "
                f"{r['exit_reason']} | {when} |")
    else:
        add("None yet.")
    add("")

    # ---------------------------------------------------------- footer
    add("---")
    add("")
    add("### How it works")
    add("")
    add("Watches 47 coins every hour. Goes long when one breaks above its "
        "3-day high, short when one breaks below its 3-day low — but only if "
        "the trend, momentum and volume all agree.")
    add("")
    add("Every trade gets a stop-loss. Winners are left to run on a trailing "
        "stop rather than closed at a fixed target. It risks 1% of the account "
        "per trade and never holds more than 5 positions on the same side, so "
        "one bad day cannot end it.")
    add("")
    add("**It loses more trades than it wins** — about 2-3 winners in 10, by "
        "design, with the winners much larger. Backtested on 2024-2026 it lost "
        "money. This is running on live prices with fake money to see what it "
        "actually does.")

    open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"status written: ${balance:.4f}, {len(open_)} open, "
          f"{len(closed)} closed, {len(scan)} coins scanned")
    return 0


if __name__ == "__main__":
    sys.exit(main())

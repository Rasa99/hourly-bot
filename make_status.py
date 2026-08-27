"""
Turns the bot's database into the repository's front page.

The local FreqUI dashboard cannot see this bot - it talks to a bot running on
your PC, and this one lives for six minutes inside GitHub then disappears.
There is no server to point a dashboard at.

So instead the bot writes its own status into README.md every hour. GitHub
renders README.md automatically, which means the repository front page IS the
dashboard: open it on any phone or computer, no login, no software, always
current to the last hour.
"""

import os
import sqlite3
import sys
from datetime import datetime, timezone

DB = "user_data/live_cloud.sqlite"
OUT = "README.md"
START_BALANCE = 20.0


def money(x):
    return f"{x:+.4f}"


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    L = []
    add = L.append

    add("# Hourly Trading Bot")
    add("")
    add(f"**Last updated:** {now} &nbsp;&nbsp;|&nbsp;&nbsp; updates itself every hour")
    add("")
    add("Paper money only. $20 simulated, real Gate.io prices, no API keys — "
        "it cannot place a real order.")
    add("")

    if not os.path.exists(DB):
        add("> Waiting for the first cycle to finish.")
        open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
        print("no database yet")
        return 0

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
    wins = [r for r in closed if (r["close_profit_abs"] or 0) > 0]
    balance = START_BALANCE + realised

    # ---- headline ----
    pct = (balance / START_BALANCE - 1) * 100
    arrow = "🟢" if pct >= 0 else "🔴"
    add("## Where the money is")
    add("")
    add("| | |")
    add("|---|---|")
    add(f"| **Balance now** | **${balance:.4f}** {arrow} |")
    add(f"| Started with | $20.0000 |")
    add(f"| Change | {pct:+.2f}% |")
    add(f"| Trades finished | {len(closed)} |")
    add(f"| Trades open now | {len(open_)} |")
    if closed:
        wr = len(wins) / len(closed) * 100
        add(f"| Win rate | {wr:.0f}%  ({len(wins)} of {len(closed)}) |")
        avg_w = (sum(r["close_profit_abs"] for r in wins) / len(wins)) if wins else 0
        losses = [r for r in closed if (r["close_profit_abs"] or 0) <= 0]
        avg_l = (sum(r["close_profit_abs"] for r in losses) / len(losses)) if losses else 0
        add(f"| Average win | {money(avg_w)} USDT |")
        add(f"| Average loss | {money(avg_l)} USDT |")
    add("")

    # ---- open ----
    add("## Open right now")
    add("")
    if open_:
        add("| Coin | Direction | Entry | Leverage | Money in |")
        add("|---|---|---|---|---|")
        for r in open_:
            side = "SHORT 🔻" if r["is_short"] else "LONG 🔺"
            add(f"| {r['pair'].split('/')[0]} | {side} | {r['open_rate']} | "
                f"{r['leverage']:.1f}x | ${r['stake_amount']:.3f} |")
    else:
        add("Nothing open. The bot only enters when a coin breaks out of its "
            "3-day range, so quiet stretches are normal.")
    add("")

    # ---- history ----
    add("## Last 15 finished trades")
    add("")
    if closed:
        add("| Coin | Direction | Result | Why it closed | When |")
        add("|---|---|---|---|---|")
        for r in closed[:15]:
            side = "SHORT" if r["is_short"] else "LONG"
            p = r["close_profit_abs"] or 0
            mark = "🟢" if p > 0 else "🔴"
            when = str(r["close_date"])[:16] if r["close_date"] else ""
            add(f"| {r['pair'].split('/')[0]} | {side} | {mark} {money(p)} USDT "
                f"({(r['close_profit'] or 0)*100:+.1f}%) | {r['exit_reason']} | {when} |")
    else:
        add("None yet.")
    add("")

    add("---")
    add("")
    add("### What this bot does")
    add("")
    add("Watches 47 coins on the hour. Buys when one breaks above its 3-day "
        "high, sells short when one breaks below its 3-day low. Every trade "
        "gets a stop-loss, and winners are left to run on a trailing stop "
        "instead of being closed at a fixed target.")
    add("")
    add("It risks 1% of the account per trade and never holds more than 5 "
        "positions on the same side, so a single bad day cannot take the "
        "account out.")
    add("")
    add("**Expect it to lose more trades than it wins** — roughly 2-3 winners "
        "in 10. It is built so the winners are much bigger than the losers. "
        "Backtests on 2024-2026 lost money; this is running to see what it "
        "does on live prices, with money that isn't real.")

    open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"status written: balance ${balance:.4f}, "
          f"{len(open_)} open, {len(closed)} closed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

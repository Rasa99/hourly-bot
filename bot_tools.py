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

import os
import sqlite3
import sys

DB = "user_data/live_cloud.sqlite"
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
        "select pair,is_open,is_short,close_profit_abs,open_rate from trades"
    ).fetchall()
    c.close()

    closed = [r for r in rows if not r["is_open"]]
    open_ = [r for r in rows if r["is_open"]]
    balance = START_BALANCE + sum((r["close_profit_abs"] or 0) for r in closed)
    wins = sum(1 for r in closed if (r["close_profit_abs"] or 0) > 0)

    mark = "\U0001F7E2" if balance >= START_BALANCE else "\U0001F534"
    out = [
        f"{mark} Hourly check done",
        f"Balance: ${balance:.4f}  ({(balance / START_BALANCE - 1) * 100:+.2f}%)",
        f"Open: {len(open_)}   Finished: {len(closed)}",
    ]
    if closed:
        out.append(f"Wins: {wins}/{len(closed)}")
    for r in open_[:5]:
        side = "SHORT" if r["is_short"] else "LONG"
        out.append(f"  {side} {r['pair'].split('/')[0]} @ {r['open_rate']}")
    if not open_ and not closed:
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

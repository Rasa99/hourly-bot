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


# The live database freqtrade writes to. It deliberately lives OUTSIDE the
# repository now, because freqtrade no longer stops between cycles - it runs
# for the job's whole life so that stops are actually managed. A file being
# written continuously cannot also be the file git commits: copying it mid
# transaction captures a torn page, and deleting its -wal out from under an
# open handle loses writes.
LIVE_DB = os.environ.get("FT_LIVE_DB", "")


def seed():
    """
    Copy the committed database to the live working path, once, at job start.

    This is how the bot remembers open trades across runs: the repository holds
    the last snapshot, and each new job starts from it.
    """
    if not LIVE_DB:
        print("FT_LIVE_DB not set - nothing to seed")
        return
    os.makedirs(os.path.dirname(LIVE_DB) or ".", exist_ok=True)
    if os.path.exists(LIVE_DB):
        print(f"live db already present at {LIVE_DB}")
        return
    if not os.path.exists(DB):
        print("no committed database yet - starting fresh")
        return
    src = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    dst = sqlite3.connect(LIVE_DB)
    src.backup(dst)
    dst.close()
    src.close()
    print(f"seeded live db from {DB}")


def snapshot():
    """
    Write a CONSISTENT copy of the live database into the repository.

    Uses SQLite's backup API rather than a file copy. That matters: freqtrade
    is writing to this database at the same moment, and backup() takes a
    transactionally consistent image of it, where `cp` would capture whatever
    half-written state happened to be on disk.
    """
    if not LIVE_DB or not os.path.exists(LIVE_DB):
        print("no live db to snapshot")
        return
    src = sqlite3.connect(f"file:{LIVE_DB}?mode=ro", uri=True)
    tmp = DB + ".tmp"
    dst = sqlite3.connect(tmp)
    src.backup(dst)
    dst.close()
    src.close()
    os.replace(tmp, DB)          # atomic, so a killed job cannot leave a stub
    print(f"snapshot written to {DB}")


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
    # THE BUG THIS GUARDS AGAINST, because it looked exactly like the bot
    # having gone rogue. seen_trades.json used to exist ONLY in the runner's
    # filesystem, which GitHub destroys when a job ends. Every new job - one
    # every 5h40m - therefore started with no memory, concluded that all
    # thirteen trades in the database were brand new, and fired one OPENED or
    # CLOSED alert for each. Rasa, 2026-08-31: "I'm sure I had only two
    # positions open, and I didn't have all the trades that it's mentioning
    # ... all of this closing position that didn't exist in the first place."
    # He had two open. The other eleven had been closed for days.
    #
    # Two things stop it. The workflow now commits this file, so the memory
    # survives a handover; and if it is missing anyway - the very first run,
    # or a lost file - the current state is adopted as the baseline and
    # NOTHING is announced.
    #
    # Missing memory must mean "say nothing", never "say everything". Getting
    # that backwards costs one skipped alert in the first case and a wall of
    # false ones in the second, and only the second makes the bot untrustable.
    known = None
    if os.path.exists(SEEN):
        try:
            prev = json.load(open(SEEN, encoding="utf-8"))
            known = (set(prev.get("open", [])), set(prev.get("closed", [])))
        except Exception:
            known = None            # unreadable counts as missing, not as empty

    now_open = {r["id"] for r in open_}
    now_closed = {r["id"] for r in closed}
    if known is None:
        newly_opened, newly_closed = [], []
        print("(first summary with no memory of previous trades - "
              "adopting current state silently)", file=sys.stderr)
    else:
        seen_open, seen_closed = known
        newly_opened = [r for r in open_
                        if r["id"] not in seen_open and r["id"] not in seen_closed]
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


CONFIG = "user_data/config/config.cloud.json"


def execconfig():
    """
    Print what execution settings are ACTUALLY in force, resolved against
    freqtrade's defaults.

    This exists because a comment in the config claimed the strategy used
    "freqtrade's default MARKET orders" while the real defaults are limit on
    entry, exit AND stoploss. Nobody caught it for weeks, because nothing ever
    printed the effective values - the only description of behaviour was prose
    sitting next to the settings, and prose cannot be wrong loudly.

    Runs once at job start. If a setting ever drifts from what is documented,
    it shows up in the log instead of in a surprise fill.
    """
    from freqtrade.strategy.interface import IStrategy

    cfg = json.load(open(CONFIG, encoding="utf-8"))
    defaults = dict(IStrategy.order_types)
    ot = {**defaults, **cfg.get("order_types", {})}

    def line(label, value, source):
        print(f"  {label:<26} {str(value):<12} ({source})")

    print("=" * 62)
    print("EFFECTIVE EXECUTION CONFIG")
    print("=" * 62)
    for key in ("entry", "exit", "stoploss", "stoploss_on_exchange"):
        src = "config" if key in cfg.get("order_types", {}) else "freqtrade default"
        line(f"order_types.{key}", ot.get(key), src)
    for key in ("trading_mode", "margin_mode", "dry_run", "stake_amount",
                "max_open_trades", "timeframe"):
        line(key, cfg.get(key), "config")
    for side in ("entry_pricing", "exit_pricing"):
        line(f"{side}.price_side", cfg.get(side, {}).get("price_side"), "config")
    line("exchange", cfg.get("exchange", {}).get("name"), "config")

    fee = cfg.get("fee")
    line("fee", fee if fee is not None else "exchange-reported",
         "config" if fee is not None else "ccxt")
    print("=" * 62)
    if not ot.get("stoploss_on_exchange"):
        print("NOTE: the stop is BOT-MANAGED. It is only enforced while the")
        print("      freqtrade process is actually running.")
    print("=" * 62)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "checkpoint":
        checkpoint()
    elif cmd == "summary":
        summary()
    elif cmd == "execconfig":
        execconfig()
    elif cmd == "seed":
        seed()
    elif cmd == "snapshot":
        snapshot()
    else:
        print("usage: bot_tools.py "
              "[checkpoint|summary|execconfig|seed|snapshot]")
        sys.exit(1)

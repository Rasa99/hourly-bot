"""
Scans every coin and works out how close each one is to triggering a trade.

This is the answer to "why has it not entered yet" and "what is closest".
Instead of guessing, it recomputes the strategy's four entry conditions live and
reports the distance to each one.

The strategy enters ONLY when all four agree:

  1. price closes above the 72-hour high  (or below the 72-hour low)
  2. EMA50 is on the matching side of EMA200
  3. ADX above 20 - the move has force behind it, not a drift
  4. volume above its 20-hour average

Most "it should have entered!" moments are condition 1 passing while 2, 3 or 4
quietly does not. This prints which one blocked it, per coin.

Writes market_scan.json for the status page and prints a short block for
Telegram.
"""

import json
import sys

import ccxt
import numpy as np
import pandas as pd
import talib.abstract as ta

BREAKOUT_H = 72
ADX_FLOOR = 20
EMA_FAST, EMA_SLOW = 50, 200
CONFIG = "user_data/config/config.cloud.json"
OUT = "market_scan.json"


def fetch(ex, pair, limit=300):
    """
    Returns candles with the CURRENTLY FORMING one removed.

    This used to return the raw frame and the scan then read `iloc[-1]`, which
    is the candle still being built. That made the dashboard disagree with the
    strategy in a way that looked like a strategy problem and was not:

      - freqtrade drops the incomplete candle before the strategy ever sees it
        (exchange.py: `idx = -2 if drop_incomplete`), so trading was always
        reading closed candles.
      - this scanner did not, so it reported on a partial hour.

    The volume filter is where it showed. The scan runs ~7 minutes past the
    hour, so `volume` held about a tenth of an hour while `vol_sma` averaged
    twenty FULL hours - "volume below average" was almost guaranteed and the
    dashboard blamed a filter that was not actually blocking anything.
    Measured at 46 minutes past the hour, when the distortion is at its
    mildest: 4/10 coins passed on the forming candle, 7/10 on the closed one.

    Dropping it here means every consumer of this file compares like with like.
    """
    o = ex.fetch_ohlcv(pair, timeframe="1h", limit=limit)
    if not o or len(o) < BREAKOUT_H + EMA_SLOW + 1:
        return None
    df = pd.DataFrame(o, columns=["date", "open", "high", "low", "close", "volume"])
    return df.iloc[:-1].reset_index(drop=True)


def main() -> int:
    cfg = json.load(open(CONFIG, encoding="utf-8"))
    pairs = cfg["exchange"]["pair_whitelist"]
    name = cfg["exchange"]["name"]

    ex = getattr(ccxt, name)({"enableRateLimit": True, "options": {"defaultType": "swap"}})
    ex.load_markets()

    rows = []
    for pair in pairs:
        try:
            df = fetch(ex, pair)
        except Exception:
            continue
        if df is None:
            continue

        df["ema_f"] = ta.EMA(df, timeperiod=EMA_FAST)
        df["ema_s"] = ta.EMA(df, timeperiod=EMA_SLOW)
        df["adx"] = ta.ADX(df, timeperiod=14)
        df["vol_sma"] = df["volume"].rolling(20).mean()
        df["dc_hi"] = df["high"].rolling(BREAKOUT_H).max().shift(1)
        df["dc_lo"] = df["low"].rolling(BREAKOUT_H).min().shift(1)

        r = df.iloc[-1]
        if pd.isna(r["ema_s"]) or pd.isna(r["dc_hi"]) or pd.isna(r["adx"]):
            continue

        price = float(r["close"])
        up_gap = (float(r["dc_hi"]) / price - 1) * 100      # % rise needed
        dn_gap = (1 - float(r["dc_lo"]) / price) * 100      # % fall needed
        ema_up = bool(r["ema_f"] > r["ema_s"])
        adx_ok = bool(r["adx"] > ADX_FLOOR)
        vol_ok = bool(r["volume"] > r["vol_sma"])

        # which direction is realistically available, given the trend filter
        if ema_up:
            gap, side = up_gap, "LONG"
        else:
            gap, side = dn_gap, "SHORT"

        blockers = []
        if gap > 0:
            blockers.append(f"needs {gap:.1f}% move")
        if not adx_ok:
            blockers.append(f"trend too weak (ADX {r['adx']:.0f}/{ADX_FLOOR})")
        if not vol_ok:
            blockers.append("volume below average")

        rows.append({
            "coin": pair.split("/")[0],
            "pair": pair,
            "price": price,
            "side": side,
            "gap": round(max(gap, 0.0), 2),
            "adx": round(float(r["adx"]), 1),
            "adx_ok": adx_ok,
            "vol_ok": vol_ok,
            "ema_up": ema_up,
            "ready": gap <= 0 and adx_ok and vol_ok,
            "blockers": blockers,
        })

    rows.sort(key=lambda r: r["gap"])
    json.dump(rows, open(OUT, "w", encoding="utf-8"), indent=1)

    ready = [r for r in rows if r["ready"]]
    print(f"scanned {len(rows)} coins, {len(ready)} ready to fire")

    print("\nCLOSEST TO ENTRY")
    for r in rows[:8]:
        flag = "READY" if r["ready"] else ", ".join(r["blockers"][:2])
        print(f"  {r['coin']:<8} {r['side']:<6} {r['gap']:>6.2f}%   {flag}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

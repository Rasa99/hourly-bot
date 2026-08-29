"""
Live position data and one price chart per open trade.

What was missing before: the status page knew what the bot had ENTERED, but not
what those positions were worth right now. Entry price alone tells you nothing -
"SHORT FIL @ 0.6813" is meaningless without today's price next to it.

This fetches the live price for every open trade, works out the unrealised
profit, and draws a small chart per position showing the last three days of
price with the entry, the stop and where price sits now.

Two outputs, deliberately:
  positions.json   - numbers, for the status page, Telegram and anything later
  pos-<COIN>.png   - one chart per open trade

PNG, not SVG, and that is not an arbitrary choice. The existing charts are SVG
because they only ever had to render on GitHub. Telegram's sendPhoto will not
display an SVG - it arrives as a file attachment nobody opens on a phone. PNG
renders inline in BOTH GitHub markdown and Telegram, so one file feeds both and
there is no second renderer to keep in sync.

Prices come from the same exchange the bot trades on, through the same library
(ccxt/Gate.io). Using a different price source here - TradingView, CoinGecko,
anything - would mean the dashboard and the bot's own P&L disagree, and then
neither number can be trusted.

Never fatal: every failure degrades to "no chart this hour", never to a crash
that would take the trading loop down with it.
"""

import json
import os
import sqlite3
import sys

DB = "user_data/live_cloud.sqlite"
CONFIG = "user_data/config/config.cloud.json"
OUT_JSON = "positions.json"
START_BALANCE = 20.0

HOURS_SHOWN = 72          # three days of context, matching the breakout window

# ---- chart geometry -------------------------------------------------------
W, H = 900, 380
PAD_L, PAD_R, PAD_T, PAD_B = 66, 118, 62, 46

BG = (14, 17, 23)
GRID = (34, 39, 48)
INK = (225, 230, 238)
DIM = (128, 138, 152)
GREEN = (63, 185, 122)
RED = (233, 84, 84)
BLUE = (88, 148, 235)
AMBER = (215, 160, 60)


# ---------------------------------------------------------------- fonts
def _font(size, bold=False):
    """
    Pillow's built-in bitmap font is unreadably small on a phone, so try real
    TrueType first. DejaVu ships on GitHub's ubuntu runners; the rest are
    fallbacks for a Windows dev box. load_default(size) needs Pillow >= 10.1,
    hence the final bare fallback.
    """
    from PIL import ImageFont

    names = (
        ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
         "C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"]
        if bold else
        ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
         "C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"]
    )
    for path in names:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    try:
        return ImageFont.load_default(size)
    except Exception:
        return ImageFont.load_default()


def _fmt(x):
    """Price formatting that survives both 0.03898 and 68000."""
    ax = abs(x)
    if ax >= 1000:
        return f"{x:,.1f}"
    if ax >= 1:
        return f"{x:.4f}"
    if ax >= 0.01:
        return f"{x:.5f}"
    return f"{x:.7f}"


def _dashed_h(draw, x0, x1, y, colour, dash=7, gap=6, width=1):
    x = x0
    while x < x1:
        draw.line([(x, y), (min(x + dash, x1), y)], fill=colour, width=width)
        x += dash + gap


# ---------------------------------------------------------------- data
def open_trades():
    if not os.path.exists(DB):
        return []
    try:
        c = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
        c.row_factory = sqlite3.Row
        rows = c.execute(
            "select id,pair,is_short,open_rate,open_date,amount,leverage,"
            "stake_amount,stop_loss,initial_stop_loss,fee_open,fee_close,"
            "funding_fees from trades where is_open=1"
        ).fetchall()
        c.close()
        return [dict(r) for r in rows]
    except Exception as e:
        print(f"could not read open trades: {type(e).__name__}: {e}")
        return []


def realised_balance():
    if not os.path.exists(DB):
        return START_BALANCE
    try:
        c = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
        got = c.execute(
            "select coalesce(sum(close_profit_abs),0) from trades where is_open=0"
        ).fetchone()[0]
        c.close()
        return START_BALANCE + (got or 0)
    except Exception:
        return START_BALANCE


# ---------------------------------------------------------------- chart
def draw_chart(pos, closes, path):
    """One position: price history, entry, stop, and where it is now."""
    from PIL import Image, ImageDraw

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    f_title = _font(23, bold=True)
    f_body = _font(15)
    f_small = _font(13)
    f_tag = _font(13, bold=True)

    up = pos["pnl"] >= 0
    accent = GREEN if up else RED

    # ---- header -------------------------------------------------------
    side = "SHORT" if pos["is_short"] else "LONG"
    d.text((PAD_L - 24, 18), f"{pos['coin']}  {side}", font=f_title, fill=INK)

    pnl_txt = f"{pos['pnl']:+.4f} USDT  ({pos['pnl_pct_margin']:+.1f}% on margin)"
    right = W - PAD_R + 100
    d.text((right - d.textlength(pnl_txt, font=f_tag), 24),
           pnl_txt, font=f_tag, fill=accent)

    # ---- plot area ----------------------------------------------------
    x0, x1 = PAD_L, W - PAD_R
    y0, y1 = PAD_T, H - PAD_B

    series = list(closes)
    marks = [pos["entry"], pos["now"]]
    if pos.get("stop"):
        marks.append(pos["stop"])
    lo, hi = min(series + marks), max(series + marks)
    if hi - lo < 1e-12:
        hi, lo = hi * 1.001 + 1e-9, lo * 0.999
    pad = (hi - lo) * 0.14
    lo, hi = lo - pad, hi + pad

    def yof(v):
        return y1 - (v - lo) / (hi - lo) * (y1 - y0)

    def xof(i):
        return x0 + (i / max(len(series) - 1, 1)) * (x1 - x0)

    # gridlines + price axis
    for k in range(5):
        v = lo + (hi - lo) * k / 4
        y = yof(v)
        d.line([(x0, y), (x1, y)], fill=GRID, width=1)
        d.text((10, y - 8), _fmt(v), font=f_small, fill=DIM)

    # ---- shaded entry -> now band, coloured by whether we are winning --
    y_entry, y_now = yof(pos["entry"]), yof(pos["now"])
    band = Image.new("RGBA", (x1 - x0, abs(int(y_now - y_entry)) + 1),
                     accent + (40,))
    img.paste(Image.alpha_composite(
        img.crop((x0, int(min(y_entry, y_now)), x1,
                  int(min(y_entry, y_now)) + band.height)).convert("RGBA"),
        band).convert("RGB"), (x0, int(min(y_entry, y_now))))

    # ---- price line ---------------------------------------------------
    pts = [(xof(i), yof(v)) for i, v in enumerate(series)]
    d.line(pts, fill=BLUE, width=2, joint="curve")

    # ---- the three reference lines ------------------------------------
    # Labels are collected rather than drawn immediately: entry, stop and now
    # regularly land within a few pixels of each other (a trade near its stop,
    # or one that has barely moved) and overlapping text is unreadable exactly
    # when the position is most worth reading.
    labels = []

    _dashed_h(d, x0, x1, y_entry, INK)
    labels.append([y_entry, f"entry {_fmt(pos['entry'])}", INK, f_small])

    if pos.get("stop"):
        y_stop = yof(pos["stop"])
        if y0 - 20 <= y_stop <= y1 + 20:
            _dashed_h(d, x0, x1, y_stop, AMBER)
            labels.append([y_stop, f"stop {_fmt(pos['stop'])}", AMBER, f_small])

    d.ellipse([x1 - 5, y_now - 5, x1 + 5, y_now + 5], fill=accent)
    labels.append([y_now, f"now {_fmt(pos['now'])}", accent, f_tag])

    # Push overlapping labels apart, keeping them in price order so a label
    # never crosses the line it belongs to.
    labels.sort(key=lambda l: l[0])
    for i in range(1, len(labels)):
        if labels[i][0] - labels[i - 1][0] < 17:
            labels[i][0] = labels[i - 1][0] + 17
    shift = labels[-1][0] - (y1 + 10)
    if shift > 0:                       # whole stack pushed off the bottom
        for l in labels:
            l[0] -= shift

    for y, text, colour, font in labels:
        d.text((x1 + 8, y - 9), text, font=font, fill=colour)

    # ---- footer -------------------------------------------------------
    # Left: where the net number came from. Right: the position's shape.
    opened = str(pos.get("open_date", ""))[:16]
    foot = f"gross {pos['gross_pnl']:+.4f}  −  fees {pos['fees']:.4f}"
    if pos["funding"]:
        foot += f"  +  funding {pos['funding']:+.4f}"
    foot += f"  =  net {pos['pnl']:+.4f} USDT"
    d.text((PAD_L - 24, H - 31), foot, font=f_body, fill=DIM)

    sub = (f"{pos['leverage']:.0f}x on ${pos['margin']:.3f}  ·  "
           f"moved {pos['move_pct']:+.2f}%  ·  opened {opened}")
    d.text((W - PAD_R + 100 - d.textlength(sub, font=f_small), H - 29),
           sub, font=f_small, fill=(96, 104, 116))

    img.save(path, "PNG", optimize=True)
    return path


# ---------------------------------------------------------------- main
def main() -> int:
    trades = open_trades()

    # Always rewrite the file, even with nothing open, so consumers never read
    # a stale set of positions from an earlier hour.
    if not trades:
        json.dump({"positions": [], "total_pnl": 0.0,
                   "balance": realised_balance()},
                  open(OUT_JSON, "w", encoding="utf-8"), indent=1)
        for f in os.listdir("."):
            if f.startswith("pos-") and f.endswith(".png"):
                os.remove(f)
        print("no open positions")
        return 0

    import ccxt

    cfg = json.load(open(CONFIG, encoding="utf-8"))
    ex = getattr(ccxt, cfg["exchange"]["name"])(
        {"enableRateLimit": True, "options": {"defaultType": "swap"}})
    ex.load_markets()

    out, total = [], 0.0
    for t in trades:
        coin = t["pair"].split("/")[0]
        try:
            ohlcv = ex.fetch_ohlcv(t["pair"], timeframe="1h",
                                   limit=HOURS_SHOWN + 1)
            closes = [c[4] for c in ohlcv][-HOURS_SHOWN:]
            now = float(closes[-1])
        except Exception as e:
            print(f"{coin}: price fetch failed ({type(e).__name__}) - skipped")
            continue

        entry = float(t["open_rate"])
        amount = float(t["amount"] or 0)
        margin = float(t["stake_amount"] or 0)
        short = bool(t["is_short"])

        gross = (entry - now) * amount if short else (now - entry) * amount
        move = (now - entry) / entry * 100

        # ---- costs, so the headline number is what you would actually keep --
        # Fees are charged on NOTIONAL (position value), not on the margin
        # posted. At 10x those differ by a factor of ten, so computing them
        # from notional here rather than reusing freqtrade's stored cost
        # columns - whose scale is inconsistent between the open and close
        # legs - keeps this honest.
        #
        # The exit fee has not been paid yet; it is charged when the trade
        # closes. Including an estimate of it is still right, because the only
        # way to realise this profit is to pay it.
        #
        # funding_fees is SIGNED, per freqtrade: positive means the trade
        # GAINED from funding, negative means it paid. So it adds.
        fee_in = entry * amount * float(t["fee_open"] or 0)
        fee_out = now * amount * float(t["fee_close"] or t["fee_open"] or 0)
        funding = float(t["funding_fees"] or 0)
        costs = fee_in + fee_out
        pnl = gross - costs + funding

        pos = {
            "coin": coin,
            "pair": t["pair"],
            "is_short": short,
            "side": "SHORT" if short else "LONG",
            "entry": entry,
            "now": now,
            "move_pct": round(move, 2),
            # "pnl" is NET - it is the headline everywhere, so it must be the
            # number you would actually keep, not the price move.
            "pnl": round(pnl, 4),
            "gross_pnl": round(gross, 4),
            "fees": round(costs, 4),
            "fee_entry": round(fee_in, 4),
            "fee_exit_est": round(fee_out, 4),
            "funding": round(funding, 4),
            "pnl_pct_margin": round(pnl / margin * 100, 1) if margin else 0.0,
            "leverage": float(t["leverage"] or 1),
            "margin": margin,
            "notional": round(entry * amount, 2),
            "stop": float(t["stop_loss"]) if t.get("stop_loss") else None,
            "open_date": str(t.get("open_date", "")),
        }
        # How far price must move against us to hit the stop - the number that
        # actually says how much room this trade has left.
        if pos["stop"]:
            pos["to_stop_pct"] = round(abs(pos["stop"] - now) / now * 100, 2)

        try:
            pos["chart"] = draw_chart(pos, closes, f"pos-{coin}.png")
        except Exception as e:
            print(f"{coin}: chart failed ({type(e).__name__}: {e})")

        out.append(pos)
        total += pnl

    # Net directional exposure. Three shorts is not three bets, it is one bet
    # in three places, and that is the risk worth showing on the front page.
    longs = sum(p["notional"] for p in out if not p["is_short"])
    shorts = sum(p["notional"] for p in out if p["is_short"])
    balance = realised_balance()

    payload = {
        "positions": out,
        "total_pnl": round(total, 4),                       # net
        "total_gross_pnl": round(sum(p["gross_pnl"] for p in out), 4),
        "total_fees": round(sum(p["fees"] for p in out), 4),
        "total_funding": round(sum(p["funding"] for p in out), 4),
        "balance": balance,
        "equity": round(balance + total, 4),
        "long_notional": round(longs, 2),
        "short_notional": round(shorts, 2),
        "net_notional": round(longs - shorts, 2),
        "gross_notional": round(longs + shorts, 2),
        "gross_pct_equity": round((longs + shorts) / balance * 100, 1) if balance else 0,
    }
    json.dump(payload, open(OUT_JSON, "w", encoding="utf-8"), indent=1)

    # Remove charts for positions that have since closed.
    live = {f"pos-{p['coin']}.png" for p in out}
    for f in os.listdir("."):
        if f.startswith("pos-") and f.endswith(".png") and f not in live:
            os.remove(f)

    print(f"{len(out)} open, unrealised {total:+.4f} USDT, "
          f"gross exposure {payload['gross_pct_equity']:.0f}% of equity")
    return 0


if __name__ == "__main__":
    sys.exit(main())

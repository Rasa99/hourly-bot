# Hourly Trading Bot

**Updated 2026-08-28 04:12 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Balance** | **$20.0000** 🟢 |
| Started with | $20.0000 |
| Change | +0.00% |
| Finished trades | 0 |
| Open now | 1 |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Leverage | Money in |
|---|---|---|---|---|
| UNI | LONG 🔺 | 4.676 | 10.0x | $0.468 |

## What it is waiting for

**0 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| SAND | SHORT | 0.00% | trend too weak (ADX 18/20); volume below average |
| BNB | LONG | 1.44% | needs 1.4% move; volume below average |
| FIL | SHORT | 2.19% | needs 2.2% move; trend too weak (ADX 20/20) |
| BTC | LONG | 2.21% | needs 2.2% move; volume below average |
| LINK | LONG | 2.92% | needs 2.9% move; volume below average |
| ETH | LONG | 3.18% | needs 3.2% move; trend too weak (ADX 12/20) |
| ATOM | LONG | 3.34% | needs 3.3% move; trend too weak (ADX 17/20) |
| ICP | LONG | 3.44% | needs 3.4% move; trend too weak (ADX 16/20) |
| SOL | LONG | 3.47% | needs 3.5% move; volume below average |
| BAT | LONG | 3.65% | needs 3.6% move; volume below average |

A trade needs **all four** of: price breaking its 3-day range, the trend filter agreeing, enough momentum (ADX over 20), and above-average volume. A coin at 0.00% that still has not traded is being held back by one of the other three — the table says which.

![market backdrop](chart-mood.svg)

## Results

![wins vs losses](chart-winloss.svg)

### Last 15 finished trades

None yet.

---

### How it works

Watches 47 coins every hour. Goes long when one breaks above its 3-day high, short when one breaks below its 3-day low — but only if the trend, momentum and volume all agree.

Every trade gets a stop-loss. Winners are left to run on a trailing stop rather than closed at a fixed target. It risks 1% of the account per trade and never holds more than 5 positions on the same side, so one bad day cannot end it.

**It loses more trades than it wins** — about 2-3 winners in 10, by design, with the winners much larger. Backtested on 2024-2026 it lost money. This is running on live prices with fake money to see what it actually does.

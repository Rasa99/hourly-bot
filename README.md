# Hourly Trading Bot

**Updated 2026-08-28 09:12 UTC** &nbsp;·&nbsp; refreshes itself every hour

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
| SAND | SHORT | 1.52% | needs 1.5% move; volume below average |
| BNB | LONG | 1.92% | needs 1.9% move; trend too weak (ADX 17/20) |
| FIL | SHORT | 2.23% | needs 2.2% move; volume below average |
| BTC | LONG | 2.65% | needs 2.7% move; volume below average |
| AVAX | LONG | 2.76% | needs 2.8% move; trend too weak (ADX 15/20) |
| ETH | LONG | 2.99% | needs 3.0% move; trend too weak (ADX 10/20) |
| LINK | LONG | 3.25% | needs 3.2% move; trend too weak (ADX 19/20) |
| BAT | LONG | 3.42% | needs 3.4% move; trend too weak (ADX 18/20) |
| MANA | LONG | 3.51% | needs 3.5% move; trend too weak (ADX 17/20) |
| DOT | LONG | 3.67% | needs 3.7% move; trend too weak (ADX 19/20) |

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

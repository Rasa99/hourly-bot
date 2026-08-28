# Hourly Trading Bot

**Updated 2026-08-28 12:12 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Balance** | **$19.8584** 🔴 |
| Started with | $20.0000 |
| Change | -0.71% |
| Finished trades | 1 |
| Open now | 0 |
| Win rate | 0% (0/1) |

![balance](chart-equity.svg)

## Open right now

Nothing open.

## What it is waiting for

**0 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| SAND | SHORT | 0.33% | needs 0.3% move; volume below average |
| AXS | SHORT | 0.84% | needs 0.8% move; trend too weak (ADX 17/20) |
| BAT | LONG | 1.08% | needs 1.1% move; trend too weak (ADX 20/20) |
| COMP | LONG | 1.16% | needs 1.2% move; trend too weak (ADX 15/20) |
| BNB | LONG | 1.86% | needs 1.9% move; trend too weak (ADX 17/20) |
| AVAX | LONG | 2.44% | needs 2.4% move; trend too weak (ADX 15/20) |
| LINK | LONG | 2.45% | needs 2.4% move; trend too weak (ADX 15/20) |
| FIL | SHORT | 2.46% | needs 2.5% move; volume below average |
| BTC | LONG | 2.53% | needs 2.5% move; trend too weak (ADX 19/20) |
| MANA | LONG | 2.63% | needs 2.6% move; trend too weak (ADX 15/20) |

A trade needs **all four** of: price breaking its 3-day range, the trend filter agreeing, enough momentum (ADX over 20), and above-average volume. A coin at 0.00% that still has not traded is being held back by one of the other three — the table says which.

![market backdrop](chart-mood.svg)

## Results

![wins vs losses](chart-winloss.svg)

### Last 15 finished trades

| Coin | Direction | Result | Why it closed | When |
|---|---|---|---|---|
| UNI | LONG | 🔴 -0.1416 (-30.3%) | trailing_stop_loss | 2026-08-28 10:07 |

---

### How it works

Watches 47 coins every hour. Goes long when one breaks above its 3-day high, short when one breaks below its 3-day low — but only if the trend, momentum and volume all agree.

Every trade gets a stop-loss. Winners are left to run on a trailing stop rather than closed at a fixed target. It risks 1% of the account per trade and never holds more than 5 positions on the same side, so one bad day cannot end it.

**It loses more trades than it wins** — about 2-3 winners in 10, by design, with the winners much larger. Backtested on 2024-2026 it lost money. This is running on live prices with fake money to see what it actually does.

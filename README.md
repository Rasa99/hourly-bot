# Hourly Trading Bot

**Updated 2026-08-28 21:12 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$19.8584** 🔴 -0.71% |
| Settled balance | $19.8584 (-0.71%) |
| Started with | $20.0000 |
| Finished trades | 1 |
| Open now | 3 |
| Win rate | 0% (0/1) |

![balance](chart-equity.svg)

## Open right now

*Live prices unavailable this cycle — entries only.*

| Coin | Direction | Entry | Leverage | Money in |
|---|---|---|---|---|
| AXS | SHORT 🔻 | 0.895 | 10.0x | $0.770 |
| SAND | SHORT 🔻 | 0.03898 | 10.0x | $0.702 |
| FIL | SHORT 🔻 | 0.6813 | 10.0x | $0.709 |

## What it is waiting for

**0 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| SAND | SHORT | 0.55% | needs 0.5% move; volume below average |
| STORJ | SHORT | 1.29% | needs 1.3% move; volume below average |
| FIL | SHORT | 1.84% | needs 1.8% move; volume below average |
| AXS | SHORT | 2.01% | needs 2.0% move; volume below average |
| ATOM | SHORT | 2.16% | needs 2.2% move; volume below average |
| LRC | SHORT | 2.81% | needs 2.8% move; volume below average |
| LTC | LONG | 3.08% | needs 3.1% move; volume below average |
| EGLD | LONG | 3.62% | needs 3.6% move; trend too weak (ADX 14/20) |
| ENJ | SHORT | 3.72% | needs 3.7% move; volume below average |
| MANA | LONG | 3.83% | needs 3.8% move; volume below average |

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

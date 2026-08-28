# Hourly Trading Bot

**Updated 2026-08-28 18:12 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Balance** | **$19.8584** 🔴 |
| Started with | $20.0000 |
| Change | -0.71% |
| Finished trades | 1 |
| Open now | 3 |
| Win rate | 0% (0/1) |

![balance](chart-equity.svg)

## Open right now

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
| FIL | SHORT | 1.15% | needs 1.1% move; volume below average |
| SAND | SHORT | 1.78% | needs 1.8% move; volume below average |
| ATOM | SHORT | 1.89% | needs 1.9% move; volume below average |
| AXS | SHORT | 1.99% | needs 2.0% move; volume below average |
| STORJ | SHORT | 3.14% | needs 3.1% move; trend too weak (ADX 19/20) |
| LRC | SHORT | 3.28% | needs 3.3% move; trend too weak (ADX 19/20) |
| BNB | LONG | 3.88% | needs 3.9% move; volume below average |
| ANKR | LONG | 4.26% | needs 4.3% move; volume below average |
| AVAX | LONG | 4.34% | needs 4.3% move; volume below average |
| MANA | LONG | 4.48% | needs 4.5% move; volume below average |

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

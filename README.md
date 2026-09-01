# Hourly Trading Bot

**Updated 2026-09-01 18:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$18.7072** 🔴 -6.46% |
| Settled balance | $18.7072 (-6.46%) |
| Started with | $20.0000 |
| Finished trades | 13 |
| Open now | 0 |
| Win rate | 23% (3/13) |

![balance](chart-equity.svg)

## Open right now

Nothing open.

## What it is waiting for

**0 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| ANKR | SHORT | 0.67% | needs 0.7% move; volume below average |
| BAT | LONG | 0.70% | needs 0.7% move; trend too weak (ADX 17/20) |
| CRV | LONG | 0.79% | needs 0.8% move; volume below average |
| LRC | SHORT | 1.26% | needs 1.3% move; volume below average |
| DOGE | SHORT | 1.54% | needs 1.5% move; trend too weak (ADX 18/20) |
| ICP | LONG | 1.57% | needs 1.6% move; trend too weak (ADX 17/20) |
| SKL | SHORT | 1.65% | needs 1.6% move; volume below average |
| HBAR | SHORT | 1.90% | needs 1.9% move; trend too weak (ADX 18/20) |
| COMP | LONG | 2.41% | needs 2.4% move; volume below average |
| GRT | SHORT | 2.71% | needs 2.7% move; trend too weak (ADX 14/20) |

A trade needs **all four** of: price breaking its 3-day range, the trend filter agreeing, enough momentum (ADX over 20), and above-average volume. A coin at 0.00% that still has not traded is being held back by one of the other three — the table says which.

![market backdrop](chart-mood.svg)

## Results

![wins vs losses](chart-winloss.svg)

### Last 15 finished trades

| Coin | Direction | Result | Why it closed | When |
|---|---|---|---|---|
| DASH | LONG | 🔴 -0.1861 (-35.0%) | stop_loss | 2026-08-30 20:43 |
| KSM | LONG | 🔴 -0.2021 (-17.9%) | stop_loss | 2026-08-30 20:40 |
| THETA | SHORT | 🔴 -0.2014 (-14.1%) | stop_loss | 2026-08-30 06:59 |
| MANA | LONG | 🔴 -0.2131 (-17.8%) | stop_loss | 2026-08-30 04:42 |
| UNI | LONG | 🟢 +0.1705 (+34.9%) | trailing_stop_loss | 2026-08-30 23:46 |
| CRV | SHORT | 🔴 -0.1984 (-19.6%) | stop_loss | 2026-08-30 12:09 |
| EGLD | LONG | 🟢 +0.3823 (+45.9%) | trailing_stop_loss | 2026-08-30 17:24 |
| ICP | LONG | 🔴 -0.2062 (-24.6%) | stop_loss | 2026-08-30 01:13 |
| BCH | SHORT | 🔴 -0.1922 (-19.8%) | trailing_stop_loss | 2026-08-29 20:06 |
| AXS | SHORT | 🔴 -0.1948 (-25.3%) | trailing_stop_loss | 2026-08-30 12:07 |
| SAND | SHORT | 🟢 +0.0906 (+12.9%) | force_exit | 2026-08-31 18:07 |
| FIL | SHORT | 🔴 -0.2003 (-28.3%) | trailing_stop_loss | 2026-09-01 07:08 |
| UNI | LONG | 🔴 -0.1416 (-30.3%) | trailing_stop_loss | 2026-08-28 10:07 |

---

### How it works

Watches 47 coins every hour. Goes long when one breaks above its 3-day high, short when one breaks below its 3-day low — but only if the trend, momentum and volume all agree.

Every trade gets a stop-loss. Winners are left to run on a trailing stop rather than closed at a fixed target. It risks 1% of the account per trade and never holds more than 5 positions on the same side, so one bad day cannot end it.

**It loses more trades than it wins** — about 2-3 winners in 10, by design, with the winners much larger. Backtested on 2024-2026 it lost money. This is running on live prices with fake money to see what it actually does.

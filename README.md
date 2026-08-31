# Hourly Trading Bot

**Updated 2026-08-31 04:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$19.2643** 🔴 -3.68% |
| Settled balance | $18.8169 (-5.92%) |
| Unrealised (open trades) | 🟢 +0.4474 |
| Started with | $20.0000 |
| Finished trades | 11 |
| Open now | 2 |
| Win rate | 18% (2/11) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **FIL** | SHORT 🔻 | 0.6813 | 0.667 | -2.10% | 🟢 +0.1426 | +20.1% | 4.92% |
| **SAND** | SHORT 🔻 | 0.03898 | 0.03696 | -5.18% | 🟢 +0.3047 | +43.4% | 8.04% |
| | | | | **total** | **+0.4474** | | |

> ⚠️ **All 2 positions are short.** That is one bet on the same market direction, placed 2 times — these coins move together, so they will win together and lose together. Gross exposure is **75% of equity**.

![FIL](pos-FIL.png)

![SAND](pos-SAND.png)


## What it is waiting for

**0 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| HBAR | SHORT | 0.96% | needs 1.0% move; volume below average |
| ALGO | SHORT | 0.97% | needs 1.0% move; volume below average |
| STORJ | SHORT | 1.01% | needs 1.0% move; volume below average |
| SAND | SHORT | 1.11% | needs 1.1% move; volume below average |
| ATOM | SHORT | 1.51% | needs 1.5% move; volume below average |
| DOGE | SHORT | 1.79% | needs 1.8% move; volume below average |
| ETC | SHORT | 1.81% | needs 1.8% move; volume below average |
| DOT | SHORT | 1.95% | needs 1.9% move; volume below average |
| LTC | SHORT | 2.11% | needs 2.1% move; volume below average |
| SKL | SHORT | 2.19% | needs 2.2% move; volume below average |

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
| UNI | LONG | 🔴 -0.1416 (-30.3%) | trailing_stop_loss | 2026-08-28 10:07 |

---

### How it works

Watches 47 coins every hour. Goes long when one breaks above its 3-day high, short when one breaks below its 3-day low — but only if the trend, momentum and volume all agree.

Every trade gets a stop-loss. Winners are left to run on a trailing stop rather than closed at a fixed target. It risks 1% of the account per trade and never holds more than 5 positions on the same side, so one bad day cannot end it.

**It loses more trades than it wins** — about 2-3 winners in 10, by design, with the winners much larger. Backtested on 2024-2026 it lost money. This is running on live prices with fake money to see what it actually does.

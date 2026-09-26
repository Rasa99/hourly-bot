# Hourly Trading Bot

**Updated 2026-09-26 19:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$19.9886** 🔴 -0.06% |
| Settled balance | $20.2059 (+1.03%) |
| Unrealised (open trades) | 🔴 -0.2173 |
| Started with | $20.0000 |
| Finished trades | 53 |
| Open now | 3 |
| Win rate | 36% (19/53) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **MANA** | LONG 🔺 | 0.09099 | 0.0916 | +0.67% | 🟢 +0.0377 | +5.2% | 3.42% |
| **DOT** | LONG 🔺 | 1.285 | 1.251 | -2.65% | 🔴 -0.1411 | -27.4% | 0.64% |
| **SAND** | LONG 🔺 | 0.04623 | 0.04559 | -1.38% | 🔴 -0.1139 | -14.8% | 1.25% |
| | | | | **total** | **-0.2173** | | |

> ⚠️ **All 3 positions are long.** That is one bet on the same market direction, placed 3 times — these coins move together, so they will win together and lose together. Gross exposure is **99% of equity**.

![MANA](pos-MANA.png)

![DOT](pos-DOT.png)

![SAND](pos-SAND.png)


## What it is waiting for

**0 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| BAT | LONG | 0.78% | needs 0.8% move; volume below average |
| ANKR | LONG | 1.20% | needs 1.2% move; volume below average |
| CHZ | LONG | 1.25% | needs 1.2% move; trend too weak (ADX 18/20) |
| SUSHI | LONG | 1.45% | needs 1.5% move |
| BTC | LONG | 1.48% | needs 1.5% move; trend too weak (ADX 11/20) |
| SKL | LONG | 1.50% | needs 1.5% move; volume below average |
| SOL | LONG | 1.57% | needs 1.6% move; volume below average |
| LRC | LONG | 1.61% | needs 1.6% move; volume below average |
| AAVE | LONG | 1.75% | needs 1.8% move; volume below average |
| BAND | LONG | 1.86% | needs 1.9% move; volume below average |

A trade needs **all four** of: price breaking its 3-day range, the trend filter agreeing, enough momentum (ADX over 20), and above-average volume. A coin at 0.00% that still has not traded is being held back by one of the other three — the table says which.

![market backdrop](chart-mood.svg)

## Results

![wins vs losses](chart-winloss.svg)

### Last 15 finished trades

| Coin | Direction | Result | Why it closed | When |
|---|---|---|---|---|
| ICP | LONG | 🔴 -0.2077 (-32.8%) | stop_loss | 2026-09-26 18:45 |
| ALGO | LONG | 🔴 -0.1848 (-31.4%) | trailing_stop_loss | 2026-09-25 14:03 |
| NEAR | LONG | 🟢 +0.1803 (+29.6%) | force_exit | 2026-09-25 15:27 |
| LINK | LONG | 🟢 +0.4337 (+32.3%) | force_exit | 2026-09-25 15:27 |
| LTC | LONG | 🔴 -0.3727 (-51.2%) | stop_loss | 2026-09-25 13:47 |
| NEAR | LONG | 🔴 -0.2758 (-51.5%) | stop_loss | 2026-09-23 14:13 |
| HBAR | LONG | 🔴 -0.1833 (-37.7%) | stop_loss | 2026-09-22 10:24 |
| GRT | LONG | 🟢 +0.1471 (+23.7%) | force_exit | 2026-09-21 03:14 |
| ALGO | LONG | 🔴 -0.1920 (-42.4%) | stop_loss | 2026-09-20 21:11 |
| HBAR | LONG | 🔴 -0.2020 (-32.9%) | stop_loss | 2026-09-20 19:21 |
| DASH | LONG | 🔴 -0.1733 (-45.7%) | stop_loss | 2026-09-19 05:58 |
| CELO | LONG | 🟢 +0.1347 (+11.6%) | force_exit | 2026-09-19 09:28 |
| ADA | LONG | 🔴 -0.0111 (-1.6%) | force_exit | 2026-09-19 09:28 |
| FIL | LONG | 🟢 +0.3452 (+56.0%) | force_exit | 2026-09-19 09:28 |
| AVAX | LONG | 🟢 +0.8187 (+99.7%) | force_exit | 2026-09-19 09:28 |

---

### How it works

Watches 47 coins every hour. Goes long when one breaks above its 3-day high, short when one breaks below its 3-day low — but only if the trend, momentum and volume all agree.

Every trade gets a stop-loss. Winners are left to run on a trailing stop rather than closed at a fixed target. It risks 1% of the account per trade and never holds more than 5 positions on the same side, so one bad day cannot end it.

**It loses more trades than it wins** — about 2-3 winners in 10, by design, with the winners much larger. Backtested on 2024-2026 it lost money. This is running on live prices with fake money to see what it actually does.
